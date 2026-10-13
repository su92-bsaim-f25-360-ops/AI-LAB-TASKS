# Lab 1 - AI Foundations: Timeline, Rule-Based Eligibility, Conversational-Test Comparison

Files
- `lab1_rules.py`   - rule-based scholarship eligibility (4 transparent conditions) + exactly four core test cases
- `lab1_compare.py` - compares the rule-based decision with a weighted-score alternative on `applicants.csv`
- `applicants.csv`  - 10 SYNTHETIC applicants (no real student data)
- `outputs/`        - captured program output (`rules_output.txt`, `compare_output.txt`)
- `Lab1_Report.docx`- report: sourced timeline, rule tests, disagreement table, conversational-test comparison, failure analysis, reflection

Setup (Python 3.8+, standard library only - no packages, no virtual environment is committed)
```
python3 --version
```

Run (from this folder)
```
python3 lab1_rules.py   | tee outputs/rules_output.txt
python3 lab1_compare.py | tee outputs/compare_output.txt
```
Expected: `4/4 test cases matched expectations`, then a 10-row comparison with 5 disagreements (A02, A03, A04, A06, A08).

Assumptions
- All thresholds (score >= 70, attendance >= 75 %, weighted cut-off 78, weights 0.6/0.2/0.2) are synthetic lab assumptions, not real scholarship policy.
- No model training is performed; both decision methods are hand-written and transparent.

Sources and AI-assistance disclosure: see the references and disclosure in `Lab1_Report.docx`.
