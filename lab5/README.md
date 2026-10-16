# Lab 5 - Adversarial Search: Minimax, Alpha-Beta Pruning and Branch Ordering

Files
- `tree.json`          - input data: the game tree (root A = MAX, B/C = MIN, D-G = MAX, leaves L1-L8) with leaf values
- `lab5_minimax.py`    - Minimax and alpha-beta pruning, each with a leaf-evaluation counter and a full trace
- `lab5_ordering.py`   - reorders branches (original, reversed, root swapped, best, worst) and runs 200 seeded random trees
- `lab5_check.py`      - compares every result with hand-derived expected values (17 checks)
- `outputs/`           - captured outputs (`minimax_output.txt`, `ordering_output.txt`, `check_output.txt`)
- `Lab5_Report.docx`   - report: hand trace, counters, reordering results, edge cases, learning-outcome link, reflection

Setup: Python 3.8+, standard library only (no packages to install).

Run (from this folder)
```
python3 lab5_minimax.py   | tee outputs/minimax_output.txt
python3 lab5_ordering.py  | tee outputs/ordering_output.txt
python3 lab5_check.py     | tee outputs/check_output.txt
```
Expected: root value 5 everywhere; Minimax evaluates 8 leaves and alpha-beta 5 (original order); `17 of 17 checks passed`.

Assumptions
- The tree and its leaf values are synthetic lab assumptions; random trees use seed 42.
- Alpha-beta cut-offs: MAX node when v >= beta, MIN node when v <= alpha.
- No private data or credentials are used.
