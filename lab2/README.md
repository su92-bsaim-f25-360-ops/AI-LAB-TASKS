# Lab 2 - PEAS, Environment Classification and a Stateful Controller

Files
- `lab2_percepts.py` - percept format and the simple reflex controller (thresholds and occupancy priority)
- `lab2_model.py`    - stateful controller that remembers the previous target mode and returns (target, send_command)
- `lab2_check.py`    - runs reflex and stateful controllers on the same percepts and prints the full trace
- `percepts.csv`     - 10 synthetic percepts (repeats, both exact boundaries, a transition, empty room)
- `edge_percepts.csv`- 6 synthetic percepts used for the edge-case analysis
- `outputs/trace_output.txt` - captured output
- `Lab2_Report.docx` - report: PEAS specifications, environment classification, reflex/stateful comparison, full trace, failure analysis, reflection

Setup: Python 3.8+, standard library only (no packages to install).

Run (from this folder)
```
python3 lab2_percepts.py
python3 lab2_check.py | tee outputs/trace_output.txt
```
Expected: both traces print `all checks passed: True`; the main trace shows 6 of 10 commands sent by the stateful controller versus 10 of 10 for the reflex controller.

Assumptions
- Thresholds (cool at >= 26, heat at <= 20) are synthetic lab assumptions, not real building policy.
- All percepts are invented; no private data or credentials are used.
