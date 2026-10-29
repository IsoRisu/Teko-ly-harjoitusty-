import copy
import sys
import random

PLY = 9 # depth
TIME = 2
COL_WEIGHTS = [1, 2, 3, 4, 3, 2, 1]

cache = {} # checks for mirror cases
def state_key(state): # creates a string and pics the lexicographically smaller one of it and its mirror
    a = tuple("".join(col) for col in state)   
    return min(a, a[::-1])

def bestmove(state, player, available):
    cache.clear() # cache depends on search
    node_cache.clear() # kind of a lazy solution but i don want to mess with the existing minimax
    move, score = iterative_deepening(state, player, available) # Iterative deepening will call minimax 
    return move # We return the chosen move
    

def minimax(state, ply, player, available, original_col = None, last_col = None, alpha=-sys.maxsize - 1,beta=sys.maxsize): # last_col is the column of the piece that was just placed

    check_time()
    if ply == 0 or available == [0,0,0,0,0,0,0] or (last_col is not None and check_immediate_win(state, last_col, len(state[last_col]) - 1)): # Also stop if the last move won the game
        #print("LEAF: ", original_col, state, heuristic(state, not player, (last_col, len(state[last_col]) - 1)))
        key = state_key(state)
        score = cache.get(key)
        if score is None:
            score = heuristic(state, not player, (last_col, len(state[last_col]) - 1))
            cache[key] = score
        return original_col, score

    if player:
        best_score = -sys.maxsize - 1 # Negative value for maxxing
    else:
        best_score = sys.maxsize # Positive Value for minimizing

    best_move = original_col
    if original_col is None: # At the root, default to the first playable column so we never return None
        best_move = next(c for c, i in enumerate(available) if i > 0)

    centre_first = [col for col, slots in enumerate(available) if slots > 0]
    centre_first.sort(key=lambda c: abs(c - (len(available) - 1) / 2))

    centre_first = order_children(state, centre_first, player) # best moves of the previous depth first, unknown ones stay centre first
    children = {} 
    original_alpha, original_beta = alpha, beta 


    for col in centre_first:
        newstate = copy.deepcopy(state)
        newstate = play_piece(newstate, col, player)
        new_available = available.copy()
        new_available[col] -= 1

        next_original = col if original_col is None else original_col
        recursive_move, state_score = minimax(newstate, ply-1, not player, new_available, next_original, col, alpha, beta)
        record_child(children, col, state_score, alpha, beta) 
        if player:
            if state_score > best_score: # Max condition
                best_score = state_score
                if original_col == None: # Check if we are at root
                    best_move = col
                else:
                    best_move = recursive_move

                # MAX node: raise alpha
                alpha = max(alpha, best_score)
        else:
            if state_score < best_score: # Min condition
                best_score = state_score
                if original_col == None: # Check if we are at root
                    best_move = col
                else:
                    best_move = recursive_move
                
                # MIN node: lower beta
                beta = min(beta, best_score)

        # Prune
        if alpha >= beta:
            break

    store_node(state, best_score, original_alpha, original_beta, children)
    return best_move, best_score

def heuristic(state: list, player:bool, last_move:tuple = None): # Last move is given as the column
    # NOTE (see BUGFIX 1): "player" here is the player who just made last_move (True = X), minimax passes "not player"
    # print(state) # Another useful debug print
    if state == [[],[],[],["X"],[],[],[]]: # Hardcoded value to play the first move in the middle as it is the best move
        return sys.maxsize

    combomatrix = [[0 for _ in range(7)] for _ in range(6)] # This matrix allows us to add score based on overlapping opportunities and a center weight bonus
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]  # vertical, horizontal, diag /, diag \

    win = last_move is not None and check_immediate_win(state, last_move[0], last_move[1]) # No crash if last_move is not given
    if win and player:
        return sys.maxsize
    if win and not player:
        return -1 * sys.maxsize - 1
    
    score = 0
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
                        depth = wr - len(state[wc])
                        combomatrix[wr][wc] += int(sign * value * COL_WEIGHTS[wc] / (1 + depth)) # Overlapping windows stack on the same tile
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

import time
 
class SearchTimeout(Exception): # Raised inside minimax when the time is up so the unfinished depth can be thrown away
    pass
 
deadline = 0 # Time (time.time()) when the current search has to stop
nodes = 0 # Node counter, the clock is only checked every few nodes because time.time() is not free
 
node_cache = {} # Node information used to order the next depth. Same mirror key as cache, cleared for every move like cache
# One record per position:
#   "flag"     : "exact", "lower" or "upper". With alpha-beta a cut off node only returns a bound, not the real value
#   "value"    : the score the node returned on the latest depth it was searched
#   "best"     : the column that gave the best score at this node
#   "children" : {column: (score, is_exact)} the score every searched child gave on the latest depth
# Columns are stored in the orientation of the key, so they are flipped when the mirrored board was the key
# This is only used to order the next depth. It is never used to cut off a search so deeper depths can change it freely
 
def check_time(): # Called at the start of every minimax call
    global nodes
    nodes += 1
    if time.time() > deadline:
        raise SearchTimeout
 
def is_mirrored(state): # True when state_key picked the mirrored board
    a = tuple("".join(col) for col in state)
    return a[::-1] < a
 
def flip(col, mirrored): # Converts a column between the real board and the key orientation 
    return 6 - col if mirrored else col
 
def order_children(state, playable, player):
    # playable is centre first. Best move of the last depth goes first, then the rest from best to worst for the side to move
    # Children that were not searched on the last depth have no score, they stay at the end in centre first order
    record = node_cache.get(state_key(state))
    if record is None:
        return playable
    mirrored = is_mirrored(state)
    scored = []
    unscored = []
    for c in playable:
        entry = record["children"].get(flip(c, mirrored))
        if entry is None:
            unscored.append(c)
        else:
            scored.append((c, entry))
    # Max player wants high scores first, min player low scores first. An exact score ranks above a bound with the same value. Sort is stable so centre first stays as the tie break
    scored.sort(key=lambda t: (-t[1][0] if player else t[1][0], 0 if t[1][1] else 1))
    ordered = [c for c, entry in scored] + unscored
 
    best = flip(record["best"], mirrored)
    if best in ordered:
        ordered.remove(best)
        ordered.insert(0, best)
    return ordered
 
def record_child(children, col, score, alpha, beta): # alpha and beta are still the window the child was searched with when this is called
    children[col] = (score, alpha < score < beta) # Inside the window the score is exact, outside it is only a bound
 
def store_node(state, best_score, original_alpha, original_beta, children):
    mirrored = is_mirrored(state)
    if best_score <= original_alpha:
        flag = "upper" # Nothing beat alpha, the real value can only be lower
    elif best_score >= original_beta:
        flag = "lower" # Cut off, the real value can only be higher
    else:
        flag = "exact"
    best = next(iter(children)) # First searched child, used if no child matches the score
    for col, (score, exact) in children.items():
        if score == best_score: # First child that reached the final score, the same one minimax keeps
            best = col
            break
    node_cache[state_key(state)] = {
        "flag": flag,
        "value": best_score,
        "best": flip(best, mirrored),
        "children": {flip(c, mirrored): v for c, v in children.items()}, # Fresh on every search of the node, scores of an older depth are not mixed in
    }
 
def iterative_deepening(state, player, available):
    global deadline, nodes
    deadline = time.time() + TIME
    nodes = 0
 
    best = next(c for c, i in enumerate(available) if i > 0) # Something playable in case even depth 1 would not finish
    score = 0
    for depth in range(1, sum(available) + 1): # No deeper than the amount of empty cells
        if time.time() > deadline:
            break
        try:
            move, depth_score = minimax(state, depth, player, available) # Every depth starts with a fresh alpha-beta window
        except SearchTimeout:
            break # The unfinished depth is discarded, best still holds the move of the last full depth
        # print("DEPTH:", depth, move, depth_score) # Useful debug print
 
        won = depth_score == (sys.maxsize if player else -sys.maxsize - 1)
        lost = depth_score == (-sys.maxsize - 1 if player else sys.maxsize)
        if lost and depth > 1:
            break # Every move loses at this depth, the move of the previous depth resists the longest so we keep it
        best, score = move, depth_score
        if won or lost:
            break # A sure win or loss, searching deeper cannot change it
    return best, score

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
                turn = True # BUGFIX 4: The turn was not reset with the board, so the move list was replayed starting from whoever was to move before (wrong colours). X always starts.
                if len(data) > 0:
                    for i in data.split(","): # Read stdin for moves
                        state = play_piece(state, int(i), turn)
                        available[int(i)] -= 1
                        turn = not turn
                        # if turn:
                        #     print("PLAYER X")
                        # else:
                        #     print("PLAYER O")                        

            case "CURRENT":
                print(f"Board set to: {state}") # Print board to Terminal

            case "RESET":
                state = [[] for _ in range(7)]
                available = [6] * 7
                turn = True

            case _:
                print("MOVE: -1")
                print("Unrecognized tag!")

        print(state) # Prints Board to Terminal
        # if turn:
        #     print("PLAYER X")
        # else:
        #     print("PLAYER O")
