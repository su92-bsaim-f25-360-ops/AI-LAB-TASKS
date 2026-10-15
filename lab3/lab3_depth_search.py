"""Lab 3 - Task 2: depth-limited search (DLS) and iterative deepening (IDDFS). Root has depth 0.

Path-local cycle check: a successor already on the CURRENT path is skipped.
Statuses: FOUND   - goal reached within the limit
          CUTOFF  - the limit stopped expansion of at least one node that still had successors off the path
          FAILURE - search space exhausted within the limit and nothing was cut off (goal not reachable)
"""
from lab3_common import load_graph, arrow


def dls(succ, start, goal, limit):
    visits = []                                   # (node, depth) in visiting order

    def rec(node, path, depth):
        visits.append((node, depth))
        if node == goal:
            return "FOUND", list(path)
        if depth == limit:                        # cannot expand further
            if any(s not in path for s in succ[node]):
                return "CUTOFF", None
            return "FAILURE", None
        cutoff = False
        for s in succ[node]:
            if s in path:                         # path-local cycle check
                continue
            status, p = rec(s, path + [s], depth + 1)
            if status == "FOUND":
                return status, p
            if status == "CUTOFF":
                cutoff = True
        return ("CUTOFF", None) if cutoff else ("FAILURE", None)

    status, path = rec(start, [start], 0)
    return dict(limit=limit, status=status, path=path, visits=visits)


def iddfs(succ, start, goal, max_depth):
    attempted, per_limit, total = [], [], 0
    for limit in range(0, max_depth + 1):
        r = dls(succ, start, goal, limit)
        attempted.append(limit)
        per_limit.append((limit, r["status"], len(r["visits"])))
        total += len(r["visits"])
        if r["status"] == "FOUND":
            return dict(max_depth=max_depth, status="FOUND", path=r["path"], attempted=attempted,
                        per_limit=per_limit, total_visits=total, final_visits=len(r["visits"]))
        if r["status"] == "FAILURE":
            return dict(max_depth=max_depth, status="FAILURE", path=None, attempted=attempted,
                        per_limit=per_limit, total_visits=total, final_visits=len(r["visits"]))
    return dict(max_depth=max_depth, status="CUTOFF", path=None, attempted=attempted,
                per_limit=per_limit, total_visits=total, final_visits=len(r["visits"]))


if __name__ == "__main__":
    start, goal, succ, _ = load_graph()
    print(f"Start {start}, goal {goal}, root depth 0\n")
    print("DLS")
    for limit in (1, 2, 3, 4):
        r = dls(succ, start, goal, limit)
        order = " ".join(f"{n}({d})" for n, d in r["visits"])
        print(f"  limit {limit}: {r['status']:<8} path: {arrow(r['path']):<22} visits {len(r['visits'])}: {order}")
    print("\nIDDFS")
    for m in (1, 2, 3, 4):
        r = iddfs(succ, start, goal, m)
        lim = ", ".join(f"{l}:{s}({v})" for l, s, v in r["per_limit"])
        print(f"  max depth {m}: {r['status']:<8} path: {arrow(r['path']):<22} limits attempted {r['attempted']} "
              f"| per limit [{lim}] | total visits {r['total_visits']} (last iteration {r['final_visits']})")
    print("\nFAILURE demonstration (goal Z does not exist in the graph)")
    for limit in (3, 7):
        r = dls(succ, start, "Z", limit)
        print(f"  limit {limit}: {r['status']}")
