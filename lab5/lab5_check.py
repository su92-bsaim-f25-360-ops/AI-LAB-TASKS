"""Lab 5 - verification against hand-derived expected values. Run: python3 lab5_check.py"""
import copy
from lab5_minimax import load_tree, run_minimax, run_alphabeta, is_leaf
from lab5_ordering import reorder, supplied_tree_results, random_experiment

tree = load_tree()
checks = []


def check(name, actual, expected):
    ok = actual == expected
    checks.append(ok)
    print(f"{'PASS' if ok else 'FAIL'}  {name}")
    if not ok:
        print(f"      expected: {expected}\n      actual  : {actual}")


# ---- Task 1: hand trace of Minimax ----
trace = []
v, s = run_minimax(tree, trace)
check("Minimax node values D,E,B,F,G,C,A (post-order)", [(t["node"], t["value"]) for t in trace],
      [("D", 5), ("E", 9), ("B", 5), ("F", 2), ("G", 0), ("C", 0), ("A", 5)])
check("Minimax root value", v, 5)

# ---- Task 2: leaf counters ----
check("Minimax leaves evaluated", (s["leaves"], s["order"]), (8, ["L1", "L2", "L3", "L4", "L5", "L6", "L7", "L8"]))
atrace = []
av, ast = run_alphabeta(tree, atrace)
check("Alpha-beta root value equals Minimax", av, v)
check("Alpha-beta leaves evaluated (original order)", (ast["leaves"], ast["order"]), (5, ["L1", "L2", "L3", "L5", "L6"]))
cuts = [(t["node"], t["pruned_leaves"]) for t in atrace if t["ev"] == "cutoff"]
check("Cut-offs: E prunes L4, C prunes L7 and L8", cuts, [("E", ["L4"]), ("C", ["L7", "L8"])])
check("Alpha-beta returns a bound (6) for pruned node E, not its exact value 9",
      [t["value"] for t in atrace if t["ev"] == "return" and t["node"] == "E"], [6])

# ---- Task 3: reordering ----
mv, ml, rows = supplied_tree_results()
exp = {"original": 5, "reversed": 7, "root_swapped": 7, "best": 5, "worst": 8}
for r in rows:
    check(f"ordering {r['mode']}: root value {mv} and {exp[r['mode']]} leaves", (r["value"], r["leaves"]), (5, exp[r["mode"]]))
check("reversed order of leaves evaluated", [r for r in rows if r["mode"] == "reversed"][0]["order"],
      ["L8", "L7", "L6", "L4", "L3", "L2", "L1"])

# ---- edge cases ----
eq = copy.deepcopy(tree)


def flatten(n):
    if is_leaf(n):
        n["value"] = 0
    else:
        for c in n["children"]:
            flatten(c)


flatten(eq)
ev, es = run_alphabeta(eq)
check("all-equal leaves: value 0, 5 leaves evaluated (cut-offs with >= and <=)", (ev, es["leaves"]), (0, 5))
e = random_experiment()
check("random trees: alpha-beta value equals Minimax in all orderings", (e["agree"], e["trials"]), (200, 200))
check("random trees: alpha-beta never evaluates more than Minimax's 81 leaves",
      all(s["max"] <= e["minimax_leaves"] for s in e["stats"].values()), True)
check("random trees: best-ordering evaluates 17 leaves every time", (e["stats"]["best"]["min"], e["stats"]["best"]["max"]), (17, 17))

print(f"\n{sum(checks)} of {len(checks)} checks passed")
assert all(checks), "some checks failed"
