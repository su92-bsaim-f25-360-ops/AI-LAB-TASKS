# AI Lab Tasks

A collection of lab work for my Artificial Intelligence course. Each lab lives in its own folder with the source code, input data, captured outputs, a README with run commands and a written report (`.docx`). Every result in a report was produced by the code in its folder and can be reproduced with a few commands.

## Labs

| Folder | Topic | What it covers |
|--------|-------|----------------|
| [lab1](lab1) | AI foundations | Sourced timeline of AI milestones, rule-based scholarship eligibility with four tests, why a conversational test is not proof of general intelligence |
| [lab2](lab2) | Agents and environments | PEAS specifications for a delivery robot and an LLM student-support agent, environment classification, a stateful controller that avoids repeated commands |
| [lab3](lab3) | Uninformed search | BFS and DFS frontier traces, depth-limited search and IDDFS, uniform-cost search on a weighted graph |
| [lab4](lab4) | Informed search | A* versus UCS, heuristic audit, an experiment showing how one overestimated heuristic value breaks optimality |
| [lab5](lab5) | Adversarial search | Minimax and alpha-beta pruning with leaf counters, and how branch ordering changes pruning but never the result |

## Highlights

- Every lab has a verification script that compares the program output with hand-derived expected values.
- Each report includes a failure or edge-case analysis, a reflection and responsible-practice notes.
- Results are reproducible: inputs are stored as data files and random experiments use a fixed seed.

## How to run

All code uses Python 3.8 or newer and only the standard library, so there is nothing to install. Open a lab folder and follow the commands in its own `README.md`. For example, in `lab5` run `python3 lab5_check.py`.

## Notes

- All graphs, thresholds, weights and tree values are synthetic lab assumptions, not real data.
- No credentials or private data are stored in this repository.
