# Lab 4 - Informed Search: A*, UCS Control and a Heuristic Overestimate Experiment

Files
- `campus.json`          - input data: campus graph (start S, goal G, successor order), edge weights and heuristic values
- `lab4_search.py`       - A* / UCS routine (UCS = A* with the zero heuristic), independent path-cost sum, true remaining costs, heuristic audit
- `lab4_astar_audit.py`  - main program: A* vs UCS traces, heuristic audit, h(C)=10 experiment, supplementary h(E)=20 experiment
- `lab4_check.py`        - compares every result with hand-derived expected values (24 checks)
- `outputs/`             - captured outputs (`audit_output.txt`, `check_output.txt`)
- `Lab4_Report.docx`     - report: manual g/h/f calculations, heuristic audit, A*/UCS comparison, overestimate experiment, failure analysis, reflection

Setup: Python 3.8+, standard library only (no packages to install).

Run (from this folder)
```
python3 lab4_astar_audit.py | tee outputs/audit_output.txt
python3 lab4_check.py       | tee outputs/check_output.txt
```
Expected: `24 of 24 checks passed`.

Conventions and assumptions
- Frontier ordered by f = g + h; ties broken first-in-first-out. Successors are tried in the listed order.
- The goal test is applied when a node is processed. Expansions = processed nodes, goal included; stale pops are counted separately.
- Graph, weights and heuristic values are synthetic lab assumptions. No private data or credentials are used.
