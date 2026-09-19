import random
import copy
import sys

PLY = 1 # depth
computed_states = set() # This set could be in the future replaced by a more efficient data structure that takes mirroring into accoumt

def bestmove(state, player, available):
    move, score = minimax(state, PLY, player, available)
    return move # We return the chosen move
    

def minimax(state, ply, player, available): # available is a list from 0 to 6 where a position is removed when it is full.
    if ply == 0 or available == []:
        return None, heuristic(state)

    if player:
        best_score = -sys.maxsize - 1
    else:
        best_score = sys.maxsize

    for 6 - n in available:
            newstate = copy.deepcopy(state) 
            newstate = play_piece(newstate, n, player)
            newavailable = copy.deepcopy(available)

            if newavailable[n] == 6:
                newavailable.remove(6)
            state_score = minimax(newstate, ply-1, not player, newavailable)[1]
            if player:
                if state_score > best_score:
                    best_score = state_score
            else:
                if state_score < best_score:
                    best_score = state_score
    return state, best_score

    
def heuristic(state:list):
    score = 0
    lines = []
    for row in state:
        lines += [row[i:i+4] for i in range(4)]
    for col in range(7):
        lines += [[state[i+j][col] for j in range(4)] for i in range(3)]
    for i in range(3):
        for j in range(4):
            lines.append([state[i+k][j+k] for k in range(4)])
            lines.append([state[i+k][j+3-k] for k in range(4)])
    for w in lines:
        x, o = w.count("X"), w.count("O")
        if x and o: continue
        score += (1, 5, 50)[x-1] if x else -(1, 5, 50)[o-1] if o else 0
    return score

def play_piece(state:list, row:int, player:bool):
    if player:
        state[row].append("X") # Place an X
    else:
        state[row].append("O") # Place 0
    return state

if __name__ == "__main__":
    state = [[] for _ in range(7)]
    count = [0] * 7
    available = [0] * 7
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
                    available[choice] += 1
                    if available[choice] == 6:
                        available.remove(6)
                    print(f"MOVE:{choice}")

            case "MOVE": # MOVE:{int} The play command
                count[int(data)] += 1   
                state = play_piece(state, int(data), turn) # Update the state
                available[data] += 1

            case "BOARD": # BOARD. This is the board set command. It first resets the board and then sets it to a configuration using inputs given as a list of moves. 
                count = [0] * 7
                available = [0] * 7
                if len(data) > 0:
                    for i in data.split(","):
                        count[int(i)] += 1
                print(f"Board set to: {count}")

            case "CURRENT":
                print(f"Board set to: {count}")

            case _:
                print("MOVE: -1")
                print("Unrecognized tag!")

        turn = not turn