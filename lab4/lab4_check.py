"""Lab 4 - verification against hand-derived expected values. Run: python3 lab4_check.py"""
from lab4_search import load, search, path_cost, true_costs, audit

start, goal, succ, w, h, _ = load()
zero = {n: 0 for n in succ}
hstar = true_costs(succ, w, goal)
checks = []


def check(name, actual, expected):
    ok = actual == expected
    checks.append(ok)
    print(f"{'PASS' if ok else 'FAIL'}  {name}")
    if not ok:
        print(f"      expected: {expected}\n      actual  : {actual}")


# hand-derived first three expansions (selected node g,h,f) and frontier left after each expansion
a = search(succ, w, h, start, goal)
check("expansion 1: S g=0 h=6 f=6", (a["trace"][0]["node"], a["trace"][0]["g"], a["trace"][0]["h"], a["trace"][0]["f"]), ("S", 0, 6, 6))
check("expansion 1 remaining", a["trace"][0]["remaining"], ["A(2+4=6)", "B(3+5=8)"])
check("expansion 2: A g=2 h=4 f=6", (a["trace"][1]["node"], a["trace"][1]["g"], a["trace"][1]["h"], a["trace"][1]["f"]), ("A", 2, 4, 6))
check("expansion 2 remaining", a["trace"][1]["remaining"], ["C(4+3=7)", "B(3+5=8)", "D(6+4=10)"])
check("expansion 3: C g=4 h=3 f=7", (a["trace"][2]["node"], a["trace"][2]["g"], a["trace"][2]["h"], a["trace"][2]["f"]), ("C", 4, 3, 7))
check("expansion 3 remaining", a["trace"][2]["remaining"], ["G(7+0=7)", "B(3+5=8)", "D(6+4=10)"])
check("A* order", a["order"], list("SACG"))
check("A* path", a["path"], list("SACG"))
check("A* expansions / stale", (a["processed"], a["stale"]), (4, 0))
check("A* cost, independent sum 2+2+3", (a["cost"], path_cost(a["path"], w)), (7, 2 + 2 + 3))

u = search(succ, w, zero, start, goal)
check("UCS order", u["order"], list("SABCEDG"))
check("UCS path", u["path"], list("SACG"))
check("UCS expansions / stale", (u["processed"], u["stale"]), (7, 1))
check("UCS cost, independent sum", (u["cost"], path_cost(u["path"], w)), (7, 7))

check("true costs h*", {n: hstar[n] for n in sorted(hstar)}, {"A": 5, "B": 7, "C": 3, "D": 5, "E": 8, "G": 0, "S": 7})
au = audit(succ, w, h, hstar)
check("original heuristic admissible and consistent", (au["admissible"], au["consistent"]), (True, True))

h2 = dict(h); h2["C"] = 10
o = search(succ, w, h2, start, goal)
check("h(C)=10 is an overestimate (10 > 3)", h2["C"] > hstar["C"], True)
check("h(C)=10 order", o["order"], list("SABDEG"))
check("h(C)=10 path", o["path"], list("SBDG"))
check("h(C)=10 cost, independent sum 3+2+5", (o["cost"], path_cost(o["path"], w)), (10, 3 + 2 + 5))
check("h(C)=10 expansions / stale", (o["processed"], o["stale"]), (6, 1))
check("h(C)=10 audit not admissible", audit(succ, w, h2, hstar)["admissible"], False)

h3 = dict(h); h3["E"] = 20
s = search(succ, w, h3, start, goal)
check("h(E)=20 result unchanged (path, cost, expansions)", (s["path"], s["cost"], s["processed"]), (list("SACG"), 7, 4))
check("h(E)=20 audit not admissible", audit(succ, w, h3, hstar)["admissible"], False)

print(f"\n{sum(checks)} of {len(checks)} checks passed")
assert all(checks), "some checks failed"
