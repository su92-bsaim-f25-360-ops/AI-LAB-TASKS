"""Lab 1 - Task 2: transparent rule-based scholarship eligibility.

All thresholds are SYNTHETIC LAB ASSUMPTIONS, not real scholarship policy.
Base rules (from the lab example): C1 score >= 70, C2 documents complete.
Added rules (my choice):          C3 attendance >= 75 %, C4 clean conduct record.
"""

MIN_SCORE = 70          # synthetic assumption (retained from the lab example)
MIN_ATTENDANCE = 75     # synthetic assumption (new condition C3)

RULES = [
    ("C1_score_threshold",  lambda a: a.get("score") is not None and a["score"] >= MIN_SCORE,
     f"score must be >= {MIN_SCORE}"),
    ("C2_documents_complete", lambda a: a.get("docs_complete") is True,
     "all required documents must be submitted"),
    ("C3_attendance_minimum", lambda a: a.get("attendance") is not None and a["attendance"] >= MIN_ATTENDANCE,
     f"attendance must be >= {MIN_ATTENDANCE}%"),
    ("C4_clean_conduct_record", lambda a: a.get("conduct_clear") is True,
     "no active disciplinary case"),
]


def evaluate(applicant):
    """Return (eligible: bool, reason: str). Missing fields fail the rule that needs them."""
    failed = [f"{name} ({why})" for name, test, why in RULES if not test(applicant)]
    if failed:
        return False, "FAILED " + "; ".join(failed)
    return True, "all four conditions satisfied"


# Exactly four core test cases (selection rationale is in the report).
TEST_CASES = [
    ("T1 pass (typical)",
     {"score": 82, "docs_complete": True, "attendance": 90, "conduct_clear": True}, True),
    ("T2 fails new condition C3 only",
     {"score": 85, "docs_complete": True, "attendance": 60, "conduct_clear": True}, False),
    ("T3 fails new condition C4 only",
     {"score": 88, "docs_complete": True, "attendance": 95, "conduct_clear": False}, False),
    ("T4 threshold boundary (score=70, attendance=75 exactly)",
     {"score": 70, "docs_complete": True, "attendance": 75, "conduct_clear": True}, True),
]


def main():
    print("NOTE: all thresholds are synthetic lab assumptions.\n")
    ok = 0
    for name, applicant, expected in TEST_CASES:
        actual, reason = evaluate(applicant)
        status = "MATCH" if actual == expected else "MISMATCH"
        ok += actual == expected
        print(f"{name}\n  input    : {applicant}\n  expected : {'ELIGIBLE' if expected else 'NOT ELIGIBLE'}"
              f"\n  actual   : {'ELIGIBLE' if actual else 'NOT ELIGIBLE'}\n  reason   : {reason}\n  result   : {status}\n")
    print(f"{ok}/{len(TEST_CASES)} test cases matched expectations")


if __name__ == "__main__":
    main()
