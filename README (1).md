# IAI-BFS-VS-DFS-BY-4-QUEEN-
> SLE-2: Profiling Report — Comparing Breadth-First Search and Depth-First Search on the 4-Queens problem, with real measured timings and py-spy profiling.

## Project Overview

This project implements **BFS** and **DFS** in Python to solve the **4-Queens problem** and compares them on:

- Execution time (batch runs of 10,000 searches using `time.perf_counter()`)
- Node expansions (for three test cases)
- Traversal order and space behaviour
- Hot frames via real **py-spy** sampling at 200 Hz

For this small search space, **runtime alone is not treated as the deciding metric** — node expansions, exploration order, and profiling structure are also reported.

## Problem: 4-Queens

Place 4 queens on a 4 × 4 board so that no two queens share a column or diagonal. A state is the column position of queens placed row by row.

**Two valid goal states:**

- (1, 3, 0, 2)
- (2, 0, 3, 1)

**State space:** root + valid partial placements = **1 + 4 + 6 + 4 + 2 = 17 nodes**. BFS and DFS traverse the *same* 17-node tree — only the exploration order differs.

## Test Cases

| Case | Search task | BFS nodes | DFS nodes |
| --- | --- | --- | --- |
| Best | Stop at solution (1,3,0,2) | 17 | 9 |
| Average | Stop at solution (2,0,3,1) | 17 | 13 |
| Worst | Enumerate all valid solutions | 17 | 17 |

## Results (10,000 searches per measured batch run, 3 runs each)

| Case | BFS Avg (ms) | DFS Avg (ms) | BFS nodes | DFS nodes |
| --- | --- | --- | --- | --- |
| Best | 248.474 | 112.582 | 17 | 9 |
| Average | 244.400 | 182.458 | 17 | 13 |
| Worst | 263.250 | 240.879 | 17 | 17 |

Raw batch runs (ms):

| Case | BFS R1 | BFS R2 | BFS R3 | DFS R1 | DFS R2 | DFS R3 |
| --- | --- | --- | --- | --- | --- | --- |
| Best | 247.67 | 248.90 | 248.86 | 111.43 | 106.86 | 119.45 |
| Average | 243.62 | 245.37 | 244.21 | 167.42 | 169.62 | 210.33 |
| Worst | 296.71 | 250.64 | 242.39 | 244.29 | 241.54 | 236.81 |

## Py-spy Profiling

Sampled natively on a standard Linux environment (`pip install py-spy`, prebuilt manylinux wheel — no Rust build needed, unlike the earlier Android/Termux attempt) at 200 Hz.

| Algorithm | Dominant frame(s) | Share of samples |
| --- | --- | --- |
| BFS | `is_safe()` column/diagonal checks | ~62% across branch lines |
| BFS | `time_batch()` / `profile()` loop overhead | ~94% (outer batch driver) |
| DFS | `recurse()` recursive descent (line 95) | up to 82% on deepest branch |
| DFS | `recurse()` safety-check branch (line 94) | 13–29% across branches |

Flamegraphs: `bfs_4queens.svg` (339 samples) and `dfs_4queens.svg` (245 samples).

## Complexity

| Metric | BFS | DFS |
| --- | --- | --- |
| Tree-search time | O(b^d) | O(b^d) |
| Typical space | O(b^d) | O(bd) |
| Data structure | Queue | Stack/recursion |
| 4-Queens nodes | 17 | 17 |

## Key Observation

Similar execution times do **not** mean BFS and DFS behave identically. They use different data structures (FIFO queue vs recursion/backtracking) and different exploration orders. A meaningful comparison must consider runtime, nodes explored, search order, memory behaviour, and profiling structure.

## Repository Structure

```javascript
IAI-BFS-VS-DFS-BY-4-QUEEN-/
├── bfs_4queens.py        # BFS implementation
├── dfs_4queens.py        # DFS implementation
├── queens_profile.py     # Batch timing driver (time.perf_counter, 10k runs)
├── bfs_4queens.svg       # py-spy flamegraph, BFS (339 samples @ 200 Hz)
├── dfs_4queens.svg       # py-spy flamegraph, DFS (245 samples @ 200 Hz)
├── README.md
└── CONTRIBUTION_LOG.md
```

## How to Run

```bash
# Batch timing (10,000 searches per measured run, 3 runs)
python queens_profile.py

# Profile with py-spy (200 Hz sampling)
pip install py-spy
py-spy record -o bfs_4queens.svg -r 200 -- python bfs_4queens.py
py-spy record -o dfs_4queens.svg -r 200 -- python dfs_4queens.py
```

## Author

- **PRN:** 25UAM102
- **Name:** Shubham Chandrakant Khavare
- **Division:** B
- **GitHub:** https://github.com/shubhamkhavare61-netizen
