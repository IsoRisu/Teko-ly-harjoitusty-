import subprocess
import sys
import unittest
from pathlib import Path
import subprocess

MAIN = Path(__file__).parent.parent / "main.py"


def run(commands):
    """Feed a list of commands to main.py, return list of output lines."""
    result = subprocess.run(
        [sys.executable, str(MAIN)],
        input="\n".join(commands) + "\n",
        capture_output=True,
        text=True,
        timeout=10,
    )
    return result.stdout.strip().splitlines()

# Helps with creating victory tests
def ai_move(board_moves, other=None):
    # Set the board with BOARD:<moves>, let the AI PLAY, return the column it chose.
    out = run(["BOARD:" + board_moves, "PLAY:"])
    moves = [l for l in out if l.startswith("MOVE:")]
    assert moves, f"No MOVE: output. Got: {out}"
    return int(moves[-1].split(":")[1])


class TestConnect4(unittest.TestCase):

    # Checks that manual moves work
    def test_move(self):
        out = run(["MOVE:0"] + ["CURRENT:"])
        moves = [l for l in out if l.startswith("Board")]
        col = moves[-1].split("Board set to:")[-1]
        self.assertEqual(col, " [['X'], [], [], [], [], [], []]")

    # Checks that the AI can play a move
    def test_play_first_move(self):
        out = run(["PLAY:"])
        moves = [l for l in out if l.startswith("M")]
        col = moves[-1].split("MOVE:")[1]
        self.assertEqual(col, "3")

    # Checks that the AI can play a full game
    def test_fill_board(self):
        out = run(["PLAY:"] * 42)
        moves = [l for l in out if l.startswith("MOVE:")]
        self.assertEqual(len(moves), 42)
        for m in moves:
            col = int(m.split(":")[1])
            self.assertGreaterEqual(col, 0)
            self.assertLessEqual(col, 6)

    # Checks that when a piece is played when the board is full the correct case is triggered
    def test_full_board_returns_minus_one(self):
        out = run(["PLAY:"] * 43)
        moves = [l for l in out if l.startswith("MOVE:")]
        self.assertEqual(moves[-1], "MOVE: -1")

    # Tests that the board is played to be full and doesn't end before it
    def test_full_board_returns_minus_one_works(self):
        out = run(["PLAY:"] * 43)
        moves = [l for l in out if l.startswith("MOVE:")]
        self.assertEqual(len(moves), 43)

    # Tests that the current command works
    def test_full_board_current(self):
        out = run(["PLAY:"] * 42 + ["CURRENT:"])
        current_line = [l for l in out if l.startswith("Board set to:")][-1]

        self.assertEqual(len(current_line), 238)

    # Tests that an immediate vertical win is chosen
    def test_immediate_vertical_win(self):
        self.assertEqual(ai_move("3,2,3,2,3,2"), 3)

    # Tests that an immediate horizontal win is chosen
    def test_immediate_horizontal_win(self):
        self.assertEqual(ai_move("0,0,1,1,2,2"), 3)

    # Tests that an immediate diagonal win is chosen
    def test_immediate_diagonal_win(self):
        self.assertEqual(ai_move("3,3,2,3,0,2,2,1,1,2"), 3)

    # Tests that the AI knows to block the opponent's immediate win when there is no immediate winning move.
    def test_immediate_vertical_block(self):
        # X has three stacked in column 3 and O (the AI) is to move
        self.assertEqual(ai_move("3,2,3,2,3"), 3)

    # Same for horizontal.
    def test_immediate_horizontal_block(self):
        # X has three in a row on the bottom (columns 0-2), O must take column 3
        self.assertEqual(ai_move("0,0,1,1,2"), 3)

    # Same for diagonal.
    def test_immediate_diagonal_block(self):
        # X threatens to complete a diagonal in column 4, O must take it
        self.assertEqual(ai_move("3,3,1,4,4,2,3,4,0,5,2"), 4)


    # Tests that the first move is played in the middle.
    def test_first_play_middle(self):
        self.assertEqual(ai_move(""), 3)

    # Test that the middle is favoured over other columns in key positions.
    def test_favour_middle(self):
        # Positions where nothing is forced and the side columns are tempting
        for board in ["0,6", "1,5", "2,6", "4,0"]:
            with self.subTest(board=board):
                self.assertEqual(ai_move(board), 3)

    # Test that creating combined threats is favoured over single threats.
    def test_combined_threats(self):
        # X on columns 2 and 4: playing column 3 makes an open three (threats on columns 1 and 5 at once)
        self.assertEqual(ai_move("2,0,4,0"), 3)

    # Test that the sides and the top and opposing pieces are taken into account in threat creation.
    def test_playability(self):
        # Sides: with only edge pieces on the board the AI still prefers the open centre
        self.assertEqual(ai_move("0,6"), 3)
        # Opposing pieces: O blocks column 3, so extending towards the edge cannot make a four
        self.assertNotEqual(ai_move("2,3,1,3"), 0)
        self.assertNotEqual(ai_move("5,3,4,3"), 6)


    # Tests that threats are created using connected pieces.
    def test_favour_connected_pieces(self):
        # X has a piece in the middle; the AI should build next to it, not far away
        for board in ["3,6", "3,0"]:
            with self.subTest(board=board):
                self.assertIn(ai_move(board), (2, 4))

if __name__ == "__main__":
    unittest.main()