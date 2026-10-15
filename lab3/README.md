# Lab 3 - Uninformed Search: BFS/DFS, DLS/IDDFS and Uniform-Cost Search

Files
- `graph.json`          - input data: A-G graph (start A, goal G, successor order) and synthetic edge weights
- `lab3_common.py`      - loads graph.json
- `lab3_bfs_dfs.py`     - Task 1: BFS and DFS with full frontier traces
- `lab3_depth_search.py`- Task 2: depth-limited search (FOUND / CUTOFF / FAILURE) and IDDFS
- `lab3_ucs.py`         - Task 3: uniform-cost search, independent cost sum, BFS comparison
- `lab3_check.py`       - checks every result against hand-derived expected values (24 checks)
- `outputs/`            - captured outputs (`bfs_dfs_output.txt`, `depth_output.txt`, `ucs_output.txt`, `check_output.txt`)
- `Lab3_Report.docx`    - report: manual traces, DLS/IDDFS results, weighted graph, UCS order and verified costs, failure analysis, reflection

Setup: Python 3.8+, standard library only (no packages to install).

Run (from this folder)
```
python3 lab3_bfs_dfs.py       | tee outputs/bfs_dfs_output.txt
python3 lab3_depth_search.py  | tee outputs/depth_output.txt
python3 lab3_ucs.py           | tee outputs/ucs_output.txt
python3 lab3_check.py         | tee outputs/check_output.txt
```
Expected: `24 of 24 checks passed`.

Assumptions
- The root has depth 0; the graph is undirected and neighbours are tried in the listed order.
- Edge weights are synthetic lab assumptions. No corridor is added to the weighted version.
- No private data or credentials are used.
