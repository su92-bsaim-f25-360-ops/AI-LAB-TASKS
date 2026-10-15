"""Lab 3 - verification. The EXPECTED values below were derived by hand (manual frontier traces) and are
compared with what the code actually returns. Run: python3 lab3_check.py
All edge weights are synthetic lab assumptions."""
from lab3_common import load_graph
from lab3_bfs_dfs import bfs, dfs
from lab3_depth_search import dls, iddfs
from lab3_ucs import ucs, path_cost

start, goal, succ, weights = load_graph()
checks = []


def check(name, actual, expected):
    ok = actual == expected
    checks.append(ok)
    print(f"{'PASS' if ok else 'FAIL'}  {name}")
    if not ok:
        print(f"      expected: {expected}\n      actual  : {actual}")


# ---- Task 1: manual traces (frontier before each step) ----
b, d = bfs(succ, start, goal), dfs(succ, start, goal)
check("BFS frontier states", [t["before"] for t in b["trace"]],
      [["A"], ["B", "C"], ["C", "D", "E"], ["D", "E", "F"], ["E", "F"], ["F"], ["G"]])
check("BFS visit order", b["order"], list("ABCDEFG"))
check("BFS final path", b["path"], list("ACFG"))
check("DFS frontier states", [t["before"] for t in d["trace"]],
      [["A"], ["C", "B"], ["C", "E", "D"], ["C", "E"], ["C", "F"], ["C", "G", "C"], ["C", "G"]])
check("DFS visit order", d["order"], list("ABDEFCG"))
check("DFS final path", d["path"], list("ABEFG"))

# ---- Task 2: DLS at limits 1-4, IDDFS max depths 1-4 ----
exp_dls = {1: ("CUTOFF", None, 3), 2: ("CUTOFF", None, 6), 3: ("FOUND", list("ACFG"), 9), 4: ("FOUND", list("ABEFG"), 7)}
for lim, (st, p, n) in exp_dls.items():
    r = dls(succ, start, goal, lim)
    check(f"DLS limit {lim}", (r["status"], r["path"], len(r["visits"])), (st, p, n))
exp_id = {1: ("CUTOFF", None, [0, 1]), 2: ("CUTOFF", None, [0, 1, 2]),
          3: ("FOUND", list("ACFG"), [0, 1, 2, 3]), 4: ("FOUND", list("ACFG"), [0, 1, 2, 3])}
for m, (st, p, att) in exp_id.items():
    r = iddfs(succ, start, goal, m)
    check(f"IDDFS max depth {m}", (r["status"], r["path"], r["attempted"]), (st, p, att))
check("IDDFS total visits (max depth 3)", iddfs(succ, start, goal, 3)["total_visits"], 1 + 3 + 6 + 9)
check("DLS goal Z limit 3 is CUTOFF", dls(succ, start, "Z", 3)["status"], "CUTOFF")
check("DLS goal Z limit 7 is FAILURE", dls(succ, start, "Z", 7)["status"], "FAILURE")

# ---- Task 3: UCS, independent cost, BFS comparison ----
u = ucs(succ, weights, start, goal)
check("UCS processing order", u["order"], list("ABCEDFG"))
check("UCS path", u["path"], list("ABEFG"))
check("UCS reported cost", u["cost"], 8)
check("Independent cost of UCS path (2+2+1+3)", path_cost(u["path"], weights), 2 + 2 + 1 + 3)
check("UCS cost equals independent sum", u["cost"], path_cost(u["path"], weights))
check("BFS route cost on weighted graph (4+6+3)", path_cost(b["path"], weights), 4 + 6 + 3)
check("BFS route costs more than UCS route", path_cost(b["path"], weights) > u["cost"], True)

print(f"\n{sum(checks)} of {len(checks)} checks passed")
assert all(checks), "some checks failed"
