import subprocess
import sys
import unittest
from pathlib import Path

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


class TestConnect4(unittest.TestCase):
    def test_fill_board(self):
        out = run(["PLAY:"] * 42)
        moves = [l for l in out if l.startswith("MOVE:")]
        self.assertEqual(len(moves), 42)
        for m in moves:
            col = int(m.split(":")[1])
            self.assertGreaterEqual(col, 0)
            self.assertLessEqual(col, 6)

    def test_full_board_returns_minus_one(self):
        out = run(["PLAY:"] * 43)
        moves = [l for l in out if l.startswith("MOVE:")]
        self.assertEqual(moves[-1], "MOVE: -1")

    def test_full_board_returns_minus_one_works(self):
        out = run(["PLAY:"] * 43)
        moves = [l for l in out if l.startswith("MOVE:")]
        self.assertEqual(len(moves), 43)

    def test_full_board_current(self):
        out = run(["PLAY:"] * 42 + ["CURRENT:"])
        current_line = [l for l in out if l.startswith("Board set to:")][-1]
        self.assertEqual(current_line, "Board set to: [6, 6, 6, 6, 6, 6, 6]")


if __name__ == "__main__":
    unittest.main()