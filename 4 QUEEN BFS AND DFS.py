"""
SLE-2: BFS vs DFS on the 4-Queens Problem
------------------------------------------
Reproduces the algorithms and profiling setup described in the report:
  - Same row-by-row valid-placement rule for both algorithms
  - BFS uses a FIFO queue (collections.deque)
  - DFS uses recursion (implicit LIFO stack)
  - Three test cases: Best / Average / Worst
  - Each case run as a batch of 10,000 complete searches, timed with
    time.perf_counter(), repeated 3 times (R1, R2, R3)

Usage:
    python queens_profile.py bfs      # run BFS batch profiling
    python queens_profile.py dfs      # run DFS batch profiling
    python queens_profile.py both     # run both and print comparison table
"""

import sys
import time
from collections import deque

N = 4  # 4-Queens


def is_safe(state, col):
    """Check if placing a queen in `col` is safe given queens already
    placed in `state` (state[row] = col for each placed row)."""
    row = len(state)
    for r, c in enumerate(state):
        if c == col:                      # same column
            return False
        if abs(c - col) == abs(r - row):  # same diagonal
            return False
    return True


# ---------------------------------------------------------------------
# BFS: level-by-level exploration using a FIFO queue
# ---------------------------------------------------------------------
def bfs_search(target=None, count_only=False):
    """
    If target is given, stop as soon as that solution is found
    (Best/Average case). If target is None, enumerate all solutions
    (Worst case). Returns (solutions_found, nodes_expanded).
    """
    queue = deque([()])   # start from the empty board (root)
    nodes = 0
    solutions = []

    while queue:
        state = queue.popleft()
        nodes += 1

        if len(state) == N:
            solutions.append(state)
            if target is not None and state == target:
                return solutions, nodes
            continue

        for col in range(N):
            if is_safe(state, col):
                queue.append(state + (col,))

    return solutions, nodes


# ---------------------------------------------------------------------
# DFS: depth-first exploration using recursion (implicit stack)
# ---------------------------------------------------------------------
def dfs_search(target=None):
    """
    Same semantics as bfs_search but explores depth-first with
    backtracking. Returns (solutions_found, nodes_expanded).
    """
    solutions = []
    nodes = 0
    found = [False]

    def recurse(state):
        nonlocal nodes
        if found[0]:
            return
        nodes += 1

        if len(state) == N:
            solutions.append(state)
            if target is not None and state == target:
                found[0] = True
            return

        for col in range(N):
            if found[0]:
                return
            if is_safe(state, col):
                recurse(state + (col,))

    recurse(())
    return solutions, nodes


# ---------------------------------------------------------------------
# Batch timing (10,000 searches per measured run, matches report §5)
# ---------------------------------------------------------------------
TEST_CASES = {
    "Best":    (1, 3, 0, 2),   # BFS 17 nodes / DFS 9 nodes
    "Average": (2, 0, 3, 1),   # BFS 17 nodes / DFS 13 nodes
    "Worst":   None,           # enumerate all -> BFS 17 nodes / DFS 17 nodes
}

BATCH_SIZE = 10_000
RUNS_PER_CASE = 3


def time_batch(search_fn, target):
    """Run `search_fn` BATCH_SIZE times and return (elapsed_ms, nodes)."""
    start = time.perf_counter()
    nodes = 0
    for _ in range(BATCH_SIZE):
        _, nodes = search_fn(target)
    elapsed_ms = (time.perf_counter() - start) * 1000
    return elapsed_ms, nodes


def profile(algo_name, search_fn):
    print(f"\n=== {algo_name} — batch profiling ({BATCH_SIZE} searches/run) ===")
    header = f"{'Case':<10}{'R1(ms)':>10}{'R2(ms)':>10}{'R3(ms)':>10}{'Avg(ms)':>10}{'Nodes':>8}"
    print(header)
    print("-" * len(header))

    results = {}
    for case, target in TEST_CASES.items():
        times = []
        nodes = 0
        for _ in range(RUNS_PER_CASE):
            elapsed_ms, nodes = time_batch(search_fn, target)
            times.append(elapsed_ms)
        avg = sum(times) / len(times)
        results[case] = (times, avg, nodes)
        print(f"{case:<10}{times[0]:>10.2f}{times[1]:>10.2f}{times[2]:>10.2f}"
              f"{avg:>10.3f}{nodes:>8}")
    return results


def print_comparison(bfs_results, dfs_results):
    print("\n=== BFS vs DFS — Results and Performance Comparison ===")
    header = f"{'Case':<10}{'BFS Avg(ms)':>14}{'DFS Avg(ms)':>14}{'BFS Nodes':>12}{'DFS Nodes':>12}"
    print(header)
    print("-" * len(header))
    for case in TEST_CASES:
        _, bfs_avg, bfs_nodes = bfs_results[case]
        _, dfs_avg, dfs_nodes = dfs_results[case]
        print(f"{case:<10}{bfs_avg:>14.3f}{dfs_avg:>14.3f}{bfs_nodes:>12}{dfs_nodes:>12}")


if __name__ == "__main__":
    mode = sys.argv[1].lower() if len(sys.argv) > 1 else "both"

    if mode == "bfs":
        profile("BFS", bfs_search)
    elif mode == "dfs":
        profile("DFS", dfs_search)
    elif mode == "both":
        bfs_res = profile("BFS", bfs_search)
        dfs_res = profile("DFS", dfs_search)
        print_comparison(bfs_res, dfs_res)
    else:
        print("Usage: python queens_profile.py [bfs|dfs|both]")
