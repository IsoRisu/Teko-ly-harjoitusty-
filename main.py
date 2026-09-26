import copy
import sys
import random

PLY = 1 # depth
computed_states = set() # This set could be in the future replaced by a more efficient data structure that takes mirroring into accoumt

def bestmove(state, player, available):
    move, score = minimax(state, PLY, player, available)
    return move # We return the chosen move
    

def minimax(state, ply, player, available, original_col = None): # available is a list from 0 to 6 where 0 means no moves are available
    if ply == 0 or available == [0,0,0,0,0,0,0]:
        change_logic = not player
        if change_logic:
            print("X")
        else:
            print("O")
        print("LEAF:", original_col, state, heuristic(state, change_logic)) # Useful
        return original_col, heuristic(state, change_logic) # original_col is the move chosen at the root, carried unchanged down the search tree.

    if player:
        best_score = -sys.maxsize - 1 # Negative value for maxxing
    else:
        best_score = sys.maxsize # Positive Value for minimizing

    best_move = None
    for col, i in enumerate(available): # Available columns
        if i == 0: # if a column is full
            continue

        # for j in range(6-col, 6): # Not sure if this is needed right now
        newstate = copy.deepcopy(state) # Creates a copy for iteration 
        newstate = play_piece(newstate, col, player) # Prepare new state for iteration
        newavailable = copy.deepcopy(available) # Creates a copy for iteration
        newavailable[col] -= 1
        if original_col == None: # Save the score for the chosen move tree
            recursive_move, state_score = minimax(newstate, ply-1, not player, newavailable, col) # recursive_move is the best root move returned by a deeper recursive call.
        else:
            recursive_move, state_score = minimax(newstate, ply-1, not player, newavailable, original_col)
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

    return best_move, best_score # best_move is the best move found by the current minimax call, which is eventually returned upward.

def heuristic(state: list, player): # Current player perspective Implementation
    # print(state) # Another useful debug print
    if state == [[],[],[],["X"],[],[],[]]: # Hardcoded value to play the first move in the middle as it is the best move
        return sys.maxsize

    score = 0

    # The vertical win check
    for i in state: # columns
        vertical_combo = 0
        for row in range(len(i)+1):
            if row >= len(i):
                break
            sign = i[row]                 
            if row == 0:
                vertical_combo += 1
            elif i[row] == i[row-1]:
                vertical_combo += 1
            else:
                vertical_combo = 1

            # Checks for immediate wins and next turn losses
            if  vertical_combo == 4 and player and sign == "X":
                return sys.maxsize # Immediate win for X
            elif    vertical_combo == 4 and not player and sign == "O":
                return -1 * sys.maxsize - 1 # Immeadiate win for O
            elif    vertical_combo == 4 and player and sign == "O":
                return -100 # Next turn is winning for O
            elif    vertical_combo == 4 and not player and sign == "X":
                return 100 # Next turn is winning for X

    # The horizontal win check
    for r in range(6): # board height
        horizontal_combo = 0
        prev = None
        for c in range(len(state)): # columns, left to right
            col = state[c]
            if r >= len(col): # no cell at this height in this column
                horizontal_combo = 0
                prev = None
                continue
            sign = col[r]
            if sign == prev:
                horizontal_combo += 1
            else:
                horizontal_combo = 1
            prev = sign

            if horizontal_combo == 4 and player and sign == "X":
                return sys.maxsize
            elif horizontal_combo == 4 and not player and sign == "O":
                return -1 * sys.maxsize - 1
            elif horizontal_combo == 4 and player and sign == "O":
                return -100
            elif horizontal_combo == 4 and not player and sign == "X":
                return 100

    # Check for immediate blocks

    # Score own good moves

    # Score own bad moves

    return score if player else -score

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