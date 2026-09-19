import copy
import sys

PLY = 2 # depth
computed_states = set() # This set could be in the future replaced by a more efficient data structure that takes mirroring into accoumt

def bestmove(state, player, available):
    move, score = minimax(state, PLY, player, available)
    return move # We return the chosen move
    

def minimax(state, ply, player, available): # available is a list from 0 to 6 where a position is removed when it is full.
    if ply == 0 or available == [0,0,0,0,0,0]:
        return None, heuristic(state, player)

    if player:
        best_score = -sys.maxsize - 1 # Negative value for maxxing
    else:
        best_score = sys.maxsize # Positive Value for minimizing

    best_move = None

    for col, i in enumerate(available): # Available columns
            for j in range(i): # Available rows # This is inefficient but works for now
                newstate = copy.deepcopy(state) # Creates a copy for iteration 
                newstate = play_piece(newstate, j, player) # Prepare new state for iteration
                newavailable = copy.deepcopy(available) # Creates a copy for iteration
                newavailable[col] -= 1

                state_score = minimax(newstate, ply-1, not player, newavailable)[1]
                if player:
                    if state_score > best_score: # Max condition
                        best_score = state_score
                        best_move = col
                else:
                    if state_score < best_score: # Min condition
                        best_score = state_score
                        best_move = col
    return best_move, best_score

    
def heuristic(state: list, player: bool):
    score = 0
    sign = 1
    if not player:
        sign = -1

    if state[3][-1] == "X":
        score += 3 * sign
        
    for col in state

    for col in state:
        window = [state[col][row], state[col+1][row], state[col][row+2], state[col][row+3]]
        if col > 3:
            continue
        for row in state[col]:
            window = [state[col][row], state[col][row+1], state[col][row+2], state[col][row+3]]
            score += evaluate_window(window)

    return score

def play_piece(state:list, row:int, player:bool):
    if player:
        state[row].append("X") # Place an X
    else:
        state[row].append("O") # Place O
    return state

if __name__ == "__main__":
    state = [[] for _ in range(7)]
    count = [0] * 7
    available = [6] * 7 # available slots per row
    turn = True # True for the starting player False for the responding player


    while True: # The game platform loop
        read = input().split(":") # Read the unput from the program
        tag, data = read # KOMENTO:DATA

        match tag:

            case "PLAY": # PLAY: AI TURN
                if sum(count) == 42: # All possible pieces have been played
                    print(f"MOVE: -1")

                else:
                    print("finding move...")
                    choice = bestmove(state, turn, available)
                    count[choice] += 1 # Play a piece
                    state = play_piece(state, choice, turn) # Update the state'
                    available[choice] -= 1 # Remove a slot from the row
                    print(f"MOVE:{choice}")

            case "MOVE": # MOVE:{int} The play command
                row = int(data)
                count[row] += 1   
                state = play_piece(state, row, turn) # Update the state
                available[row] -= 1

            case "BOARD": # BOARD. This is the board set command. It first resets the board and then sets it to a configuration using inputs given as a list of moves. 
                count = [0] * 7 # Reset board for the GUI
                available = [6] * 7 # Available slots per row reset
                if len(data) > 0:
                    for i in data.split(","): # Read stdin for moves
                        count[int(i)] += 1
                print(f"Board set to: {count}") # Print board GUI

            case "CURRENT":
                print(f"Board set to: {count}") # Print board to GUI

            case _:
                print("MOVE: -1")
                print("Unrecognized tag!")

        turn = not turn