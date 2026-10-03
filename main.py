import copy
import sys
import random

PLY = 1 # depth
computed_states = set() # This set could be in the future replaced by a more efficient data structure that takes mirroring into accoumt
COL_WEIGHTS = [1, 2, 3, 4, 3, 2, 1]

def bestmove(state, player, available):
    move, score = minimax(state, PLY, player, available)
    return move # We return the chosen move
    

def minimax(state, ply, player, available, original_col = None, last_col = None): # last_col is the column of the piece that was just placed
    if ply == 0 or available == [0,0,0,0,0,0,0] or (last_col is not None and check_immediate_win(state, last_col, len(state[last_col]) - 1)): # Also stop if the last move won the game
        change_logic = not player # Fixed a bug at some point
        print("LEAF: ", original_col, state, heuristic(state, change_logic, (last_col, len(state[last_col]) - 1)))
        return original_col, heuristic(state, change_logic, (last_col, len(state[last_col]) - 1)) # Row is the top piece of the column, not available - 1

    if player:
        best_score = -sys.maxsize - 1 # Negative value for maxxing
    else:
        best_score = sys.maxsize # Positive Value for minimizing

    best_move = original_col
    if original_col is None: # At the root, default to the first playable column so we never return None
        best_move = next(c for c, i in enumerate(available) if i > 0)

    for col, i in enumerate(available): # Available columns
        if i == 0: # if a column is full
            continue

        newstate = copy.deepcopy(state) # Creates a copy for iteration 
        newstate = play_piece(newstate, col, player) # Prepare new state for iteration
        newavailable = copy.deepcopy(available) # Creates a copy for iteration
        newavailable[col] -= 1
        if original_col == None: # Save the score for the chosen move tree
            recursive_move, state_score = minimax(newstate, ply-1, not player, newavailable, col, col)
        else:
            recursive_move, state_score = minimax(newstate, ply-1, not player, newavailable, original_col, col)
        if player:
            if state_score > best_score: # Max condition
                best_score = state_score
                if original_col == None: # Check if we are at root
                    best_move = col
                else:
                    best_move = recursive_move
        else:
            if state_score < best_score: # Min condition
                best_score = state_score
                if original_col == None: # Check if we are at root
                    best_move = col
                else:
                    best_move = recursive_move

    return best_move, best_score

def heuristic(state: list, player:bool, last_move:tuple = None): # Last move is given as the column
    # print(state) # Another useful debug print
    if state == [[],[],[],["X"],[],[],[]]: # Hardcoded value to play the first move in the middle as it is the best move
        return sys.maxsize

    combomatrix = [[COL_WEIGHTS[c] for c in range(7)]for _ in range(6)] # This matrix allows us to add score based on overlapping opportunities and a center weight bonus
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]  # vertical, horizontal, diag /, diag \

    win = last_move is not None and check_immediate_win(state, last_move[0], last_move[1]) # No crash if last_move is not given
    if win and player:
        return sys.maxsize
    if win and not player:
        return -1 * sys.maxsize - 1
    
    score = 0
 
    # Heuristics notes
    # Examples from the perspective of X. X is the maxxing player and recieves positive score, the min player recieves negative score.
    # | is a wall _ is a playable space
    # for vertical, horizontal, diag /, diag \ count potential 
    # x_ score well
    # xx_ score highly

    # opponent blocks, vertical, horizontal, diag /, diag \
    #
    #
    
    # Multi theats
    # |xx_ score well
    # _xx_ score better a position _xxx_ is extremely winning

    # favour connected pieces
    # _xx_ > _x_x_

    # Playability
    # take the bottom and the top of the board into account when starting to create threats
    # |_xo no space to create anything
    # |___xo more space is better

    for c in range(7):
        for r in range(6):
            for dc, dr in directions:
                if not (0 <= c + dc * 3 < 7 and 0 <= r + dr * 3 < 6): # A window of 4 has to fit on the board, this is how walls are handled
                    continue
                window = [(c + dc * i, r + dr * i) for i in range(4)]
                cells = [state[wc][wr] if wr < len(state[wc]) else "_" for wc, wr in window]
                x_count = cells.count("X")
                o_count = cells.count("O")
                if (x_count and o_count) or not (x_count or o_count): # Blocked by the opponent or nothing to build on
                    continue
                count = max(x_count, o_count)
                sign = 1 if x_count else -1
                value = [0, 1, 3, 10, 0][count] # x_ well, xx_ highly, xxx_ extremely
                pieces = [i for i in range(4) if cells[i] != "_"]
                if pieces[-1] - pieces[0] == count - 1: # Favour connected pieces _xx_ > _x_x_
                    value *= 2
                for i in range(4):
                    if cells[i] == "_":
                        wc, wr = window[i]
                        combomatrix[wr][wc] += sign * value * COL_WEIGHTS[wc] # Overlapping windows stack on the same tile
    for r in range(6):
        for c in range(7):
            score += combomatrix[r][c]

    return score  # if player else -score

def check_immediate_win(state, col, row):

    if col is None:
        return False
    if not (0 <= col < 7):
        return False
    if row is None or row < 0:
        return False
    if row >= len(state[col]):
        return False

    sign = state[col][row]
    if sign not in ("X", "O"):
        return False
    
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]  # vertical, horizontal, diag /, diag \
    for dc, dr in directions:
        count = 1
        for step in (1, -1): # Ensures that we are moving to both directions in the chocsn axis
            c, r = col + dc * step, row + dr * step
            while 0 <= c < 7 and 0 <= r < 6:
                cell = state[c]
                if r >= len(cell) or (cell[r] != sign):
                    break
                count += 1
                c += dc * step
                r += dr * step
        if count >= 4:
            return True
    return False

def play_piece(state:list, column:int, player:bool):
    if player:
        state[column].append("X") # Place an X
    else:
        state[column].append("O") # Place O
    return state

if __name__ == "__main__":
    state = [[] for _ in range(7)] # Board
    available = [6] * 7 # available slots per row
    turn = True # True for the starting player X False for the responding player O


    while True: # The game platform loop
        read = input().split(":") # Read the unput from the program
        tag, data = read # KOMENTO:DATA

        match tag:

            case "PLAY": # PLAY: AI TURN
                if sum(available) == 0: # All possible pieces have been played
                    print(f"MOVE: -1")

                else:
                    print("finding move...")
                    choice = bestmove(state, turn, available)
                    state = play_piece(state, choice, turn) # Update the state'
                    available[choice] -= 1 # Indicate a played piece for the row
                    print(f"MOVE:{choice}")

                turn = not turn

            case "MOVE": # MOVE:{int} The play command
                row = int(data) 
                state = play_piece(state, row, turn) # Update the state
                available[row] -= 1
                turn = not turn


            case "BOARD": # BOARD. This is the board set command. It first resets the board and then sets it to a configuration using inputs given as a list of moves. 
                available = [6] * 7 # Available slots per row reset
                state = [[] for _ in range(7)] # Reset the board
                if len(data) > 0:
                    for i in data.split(","): # Read stdin for moves
                        state = play_piece(state, int(i), turn)
                        turn = not turn
                        if turn:
                            print("PLAYER X")
                        else:
                            print("PLAYER O")                        

            case "CURRENT":
                print(f"Board set to: {state}") # Print board to Terminal

            case _:
                print("MOVE: -1")
                print("Unrecognized tag!")

        # print(state) # Prints Board to Terminal
        if turn:
            print("PLAYER X")
        else:
            print("PLAYER O")