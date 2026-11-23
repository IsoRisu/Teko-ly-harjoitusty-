import sys
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))
import main

def test_state_key(): # Tests that the state key actua
    state = [[], [], [], ["X"], [], [], []]
    result = main.state_key(state)
    assert isinstance(result, tuple) # checks that the type is correct
    assert len(result) == 7 # checks that there is the correct amount of columns
    assert min(result, result[::-1]) == result # tests that state key truly returns the lexicographically shortest of the original state and its mirror

def test_bestmove():
    main.node_cache.clear() # just in case
    state = [[] for _ in range(7)]
    available = [6] * 7
    move = main.bestmove(state, True, available)
    assert 0 <= move < 7 # checks that a move is given within legal bounds

def test_heuristic():
    state = [[], [], [], ["X"], [], [], []]
    score = main.heuristic(state, True, None) # Player X with state and no previous moves
    assert score == sys.maxsize # should return the optimal move

def test_check_immediate_win():
    # vertical win for X
    state = [["X", "X", "X", "X"], [], [], [], [], [], []]
    assert main.check_immediate_win(state, 0, 3) is True
    state2 = [[], [], [], ["X"], [], [], []]
    assert main.check_immediate_win(state2, 3, 0) is False

def test_play_piece():
    state = [[] for _ in range(7)]
    result = main.play_piece(state, 3, True)
    assert result[3] == ["X"]
    result = main.play_piece(state, 3, False)
    assert result[3] == ["X", "O"]

def test_check_time():
    import time
    main.deadline = time.time() + 100
    try:
        main.check_time()
    except main.SearchTimeout:
        assert False, "Should not timeout"
    
    main.deadline = time.time() - 1
    try:
        main.check_time()
        assert False, "Should have timed out"
    except main.SearchTimeout:
        pass

def test_is_mirrored():
    state = [[], [], [], ["X"], [], [], []]
    # symmetric - not mirrored (a == a[::-1])
    assert main.is_mirrored(state) is False
    state2 = [["X"], [], [], [], [], [], []]
    assert main.is_mirrored(state2) is True  # reversed is smaller

def test_flip():
    assert main.flip(0, False) == 0
    assert main.flip(0, True) == 6
    assert main.flip(3, True) == 3
    assert main.flip(6, True) == 0

def test_order_children():
    state = [[] for _ in range(7)]
    playable = [3, 2, 4, 1, 5, 0, 6]
    result = main.order_children(state, playable, True)
    assert set(result) == set(playable)

def test_record_child():
    children = {}
    main.record_child(children, 3, 10, 0, 20)
    assert children[3] == (10, True)
    children2 = {}
    main.record_child(children2, 3, 25, 0, 20)
    assert children2[3] == (25, False)  # outside beta

def test_store_node():
    state = [[] for _ in range(7)]
    children = {3: (10, True)}
    main.node_cache.clear()
    main.store_node(state, 10, -100, 100, children)
    key = main.state_key(state)
    assert key in main.node_cache
    assert main.node_cache[key]["flag"] == "exact"

def test_iterative_deepening():
    state = [[] for _ in range(7)]
    available = [6] * 7
    move, score, depth = main.iterative_deepening(state, True, available)
    assert 0 <= move < 7

def test_time_complexity():
    state = [["O", "X", "X"], ["X", "O"], ["X"], ["O", "X", "O", "X"], [], ["O", "X"], ["X", "O", "O"]]
    available = [3,4,5,2,6,4,3]
    result = []
    while main.TIME < 13:
        move, score, depth = main.iterative_deepening(state, False, available)
        main.TIME += 1 # keep a note that modifying this global variable keeps it modified even outside this loop
        result.append(depth)
    main.TIME = 2 # this should match whatever is in main.py
    plot_xy(range(2,12+1),result)

def plot_xy(x, y):
    if len(x) != len(y) or not x:
        raise ValueError("x and y must be non-empty and the same length")

    fig, ax = plt.subplots(figsize=(8, 4.5))

    # ---- data ----
    ax.plot(x, y, color="tab:blue", linewidth=2, marker="o",
            markersize=4, label="y vs time")

    # ---- axes styling ----
    ax.axhline(0, color="black", linewidth=0.8)       # x-axis through y=0
    ax.grid(True, linestyle="--", alpha=0.5)

    # pad the data range a little so points don't sit on the edges
    ax.set_xlim(min(x), max(x) if max(x) > min(x) else min(x) + 1)
    ax.set_ylim(min(y) - 1, max(y) + 1)

    # integer-only ticks (x is whole seconds, y is whole units)
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))

    # ---- labels ----
    ax.set_title("depth reached")
    ax.set_xlabel("time (s)")
    ax.set_ylabel("depth")
    ax.legend(loc="upper right", frameon=True)

    fig.tight_layout()
    plt.show()

def main_func():
    for name, fn in sorted(list(globals().items())):
        if name.startswith("test_") and callable(fn):
            fn()
            print(f"PASSED: {name}")