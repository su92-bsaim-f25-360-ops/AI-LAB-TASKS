"""Lab 2 - runs the reflex and stateful controllers on the same percepts and prints the trace.
Usage: python3 lab2_check.py
All thresholds are synthetic lab assumptions.
"""
from lab2_percepts import load_percepts, reflex_target
from lab2_model import StatefulController


def run_trace(path):
    controller = StatefulController()
    rows = []
    for r in load_percepts(path):
        previous = controller.previous_target
        target, send = controller.step(r["percept"])
        rows.append({
            "step": int(r["step"]), "note": r["case_note"], "previous": previous,
            "percept": r["percept"], "target": target, "send": send,
            "reflex_target": reflex_target(r["percept"]),
            "ok": target == r["expected_target"] and send == (r["expected_send"] == "1"),
        })
    return rows


def show(title, path):
    rows = run_trace(path)
    print(title)
    print(f"{'step':<4} {'previous mode':<13} {'percept':<34} {'target':<7} {'stateful outcome':<17} {'reflex outcome':<15} check  note")
    for r in rows:
        p = f"T={r['percept']['temperature']}, occupied={r['percept']['occupied']}"
        print(f"{r['step']:<4} {str(r['previous']):<13} {p:<34} {r['target']:<7} "
              f"{'SEND' if r['send'] else 'NO COMMAND':<17} {'SEND':<15} {'PASS' if r['ok'] else 'FAIL':<6} {r['note']}")
    sent = sum(r["send"] for r in rows)
    print(f"\nstateful commands sent: {sent} of {len(rows)} | reflex commands sent: {len(rows)} of {len(rows)} "
          f"| all checks passed: {all(r['ok'] for r in rows)}\n")
    return rows


if __name__ == "__main__":
    print("NOTE: thresholds (cool >= 26, heat <= 20) are synthetic lab assumptions.\n")
    show("MAIN TRACE (percepts.csv)", "percepts.csv")
    show("EDGE CASE: temperature alternating around 26 (edge_percepts.csv)", "edge_percepts.csv")
