"""Lab 1 - comparison: rule-based decision vs. a transparent weighted-score alternative.

Both are hand-written (no model training). All weights/thresholds are SYNTHETIC LAB ASSUMPTIONS.
Weighted alternative: composite = 0.6*score + 0.2*attendance + 0.2*(100 if conduct clear else 0),
eligible if documents complete AND composite >= 78.
"""
import csv
from lab1_rules import evaluate

W_SCORE, W_ATT, W_CONDUCT, CUTOFF = 0.6, 0.2, 0.2, 78.0


def weighted(a):
    composite = W_SCORE * a["score"] + W_ATT * a["attendance"] + W_CONDUCT * (100 if a["conduct_clear"] else 0)
    return a["docs_complete"] and composite >= CUTOFF, round(composite, 1)


def load(path="applicants.csv"):
    with open(path, newline="") as f:
        for r in csv.DictReader(f):
            yield {"id": r["id"], "score": float(r["score"]), "docs_complete": r["docs_complete"] == "1",
                   "attendance": float(r["attendance"]), "conduct_clear": r["conduct_clear"] == "1"}


def main():
    print("NOTE: weights and thresholds are synthetic lab assumptions.\n")
    print(f"{'ID':<4} {'score':>5} {'att':>4} {'docs':>5} {'cond':>5} | {'rules':<9} {'weighted':<9} {'composite':>9} | agree?")
    disagreements = []
    for a in load():
        r, _ = evaluate(a)
        w, comp = weighted(a)
        agree = r == w
        if not agree:
            disagreements.append((a, r, w, comp))
        print(f"{a['id']:<4} {a['score']:>5.0f} {a['attendance']:>4.0f} {str(a['docs_complete']):>5} {str(a['conduct_clear']):>5} | "
              f"{'ELIGIBLE' if r else 'NO':<9} {'ELIGIBLE' if w else 'NO':<9} {comp:>9} | {'yes' if agree else 'DISAGREE'}")
    print(f"\nDisagreement table ({len(disagreements)} of 10 applicants):")
    for a, r, w, comp in disagreements:
        print(f"  {a['id']}: rules={'ELIGIBLE' if r else 'NO'}, weighted={'ELIGIBLE' if w else 'NO'} "
              f"(composite {comp}) | rules reason: {evaluate(a)[1]}")


if __name__ == "__main__":
    main()
