import random
import copy

PLY = 1
computed_states = set()
def bestmove(state, player, opponent):
    

def minimax(state, ply, player, opponent, available): # available is a list from 0 to 6 where a position is removed when it is full.
    if PLY == 0 or sum(state) == 42:
        return
    for n in available:
            newstate = copy.deepcopy(state[n]) 
            newstate[n] += 1
            computed_states.add(minimax(newstate, ply-1, opponent,  player))
            if player:
                
        

def heuristic(state):
    return score

if __name__ == "__main__":
    count = [0] * 7
    available = list(range(0,7))
    turn = True # True for the starting player False for the responding player


    while True: # The game platform loop
        read = input().split(":") # Read the unput from the program
        tag, data = read # KOMENTO:DATA

        match tag:

            case "PLAY": # PLAY: AI TURN
                if sum(count) == 42:
                    print(f"MOVE: -1")

                else:
                    print("finding move...")
                    choice = random.choice(available)
                    while count[choice] == 6:
                        available.remove(choice)
                        choice = random.choice(available)

                    count[choice] += 1
                    print(f"MOVE:{choice}")

            case "MOVE": # MOVE:{int} The play command
                op_move = data  
                count[int(op_move)] += 1   
                print(data)

            case "BOARD": # BOARD. This is the board set command. It first resets the board and then sets it to a configuration using inputs given as a list of moves. 
                count = [0] * 7
                if len(data) > 0:
                    for i in data.split(","):
                        count[int(i)] += 1
                print(f"Board set to: {count}")

            case "CURRENT":
                print(f"Board set to: {count}")

            case _:
                print("MOVE: -1")
                print("Unrecognized tag!")

        not turn