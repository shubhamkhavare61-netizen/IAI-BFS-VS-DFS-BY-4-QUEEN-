# Contribution Log — SLE-2: BFS vs DFS on 4-Queens

| Date       | Task / Activity                                                        | Contributor                          | Notes |
|------------|------------------------------------------------------------------------|--------------------------------------|-------|
| Sep 2026   | Designed experiment: BFS vs DFS comparison on the 4-Queens problem     | Shubham Chandrakant Khavare (25UAM102, Div B) | Defined the three test cases (Best / Average / Worst) |
| Sep 2026   | Implemented BFS solver (FIFO queue, level-by-level, row-by-row placement rule) | Shubham Chandrakant Khavare | Stops at first solution or enumerates all 2 valid solutions |
| Sep 2026   | Implemented DFS solver (recursion / implicit LIFO stack, backtracking)  | Shubham Chandrakant Khavare | Same 17-node valid state space as BFS |
| Sep 2026   | Wrote `queens_profile.py` batch timing driver                          | Shubham Chandrakant Khavare | `time.perf_counter()`, 10,000 searches per measured run, 3 runs per case — keeps every timing above 1 ms |
| Sep 2026   | Measured batch runtimes for all 3 test cases (Best / Average / Worst)  | Shubham Chandrakant Khavare | BFS 248.47 / 244.40 / 263.25 ms; DFS 112.58 / 182.46 / 240.88 ms |
| Sep 2026   | Counted node expansions per test case                                  | Shubham Chandrakant Khavare | BFS: 17/17/17; DFS: 9/13/17 |
| Sep 2026   | Drew 17-node state-space tree and 4-Queens solution-board diagrams     | Shubham Chandrakant Khavare (with AI assistance for diagram preparation) | Fig. 1–3 of the report |
| Sep 2026   | Attempted py-spy install on Android/Termux (blocked: Rust build required) | Shubham Chandrakant Khavare | Abandoned; switched to native Linux |
| Sep 2026   | Installed py-spy natively on Linux (prebuilt manylinux wheel)          | Shubham Chandrakant Khavare | No Rust toolchain needed |
| Sep 2026   | Captured py-spy flamegraphs at 200 Hz                                   | Shubham Chandrakant Khavare | `bfs_4queens.svg` (339 samples), `dfs_4queens.svg` (245 samples) |
| Sep 2026   | Analyzed hot frames and wrote interpretation                           | Shubham Chandrakant Khavare | BFS → `is_safe()` ~62% + batch loop ~94%; DFS → `recurse()` up to 82% |
| Sep 2026   | Wrote complexity analysis, justification and observation sections      | Shubham Chandrakant Khavare | Runtime, nodes, order, memory, profiling structure |
| Sep 2026   | Wrote SLE-2 profiling report (profiling report document)               | Shubham Chandrakant Khavare | With AI assistance for organization and explanations |
| Sep 2026   | Created README.md and this contribution log                            | Shubham Chandrakant Khavare | — |

## AI Contribution Note

AI assistance was used for report organization, BFS/DFS explanation, diagram preparation, complexity discussion, and troubleshooting the py-spy installation. The measured timings reported are retained from the earlier execution of the experiment.

## Verification

- [x] Same row-by-row valid-placement rule used in both algorithms
- [x] Each test case executed 3 times, 10,000 searches per measured run
- [x] Total valid state space verified as 1 + 4 + 6 + 4 + 2 = 17 nodes
- [x] py-spy flamegraphs captured natively at 200 Hz and referenced in report
