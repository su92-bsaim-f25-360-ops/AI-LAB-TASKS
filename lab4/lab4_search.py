"""Lab 4 - A* and UCS in one routine (UCS = A* with the zero heuristic).

Campus graph, edge weights and heuristic values are SYNTHETIC LAB ASSUMPTIONS (campus.json).
Frontier: priority queue ordered by f = g + h, ties broken first-in-first-out (insertion order).
Goal test when a node is PROCESSED (popped). A popped entry whose node was already processed is a
STALE entry: it is counted separately and is not an expansion.
Counting convention (both algorithms): expansions = processed nodes, the goal included.
"""
import heapq
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def load(path=None):
    with open(path or os.path.join(HERE, "campus.json")) as f:
        d = json.load(f)
    w = {}
    for k, v in d["weights"].items():
        a, b = k.split("-")
        w[(a, b)] = v
        w[(b, a)] = v
    return d["start"], d["goal"], d["successors"], w, dict(d["heuristic"]), d["labels"]


def entry(n, g, h):
    return f"{n}({g}+{h}={g + h})"


def search(succ, w, h, start, goal):
    counter = 0
    heap = [(h[start], counter, 0, start, [start])]          # (f, insertion order, g, node, path)
    explored, order, trace, stale = set(), [], [], 0
    while heap:
        before = [entry(n, g, h[n]) for f, c, g, n, p in sorted(heap)]
        f, _, g, node, path = heapq.heappop(heap)
        step = len(trace) + 1
        if node in explored:
            stale += 1
            trace.append(dict(step=step, before=before, node=node, g=g, h=h[node], f=f, generated=[], skipped=[],
                              goal=False, stale=True, remaining=[entry(n2, g2, h[n2]) for f2, c2, g2, n2, p2 in sorted(heap)]))
            continue
        explored.add(node)
        order.append(node)
        generated, skipped = [], []
        if node == goal:
            trace.append(dict(step=step, before=before, node=node, g=g, h=h[node], f=f, generated=[], skipped=[],
                              goal=True, stale=False, remaining=[entry(n2, g2, h[n2]) for f2, c2, g2, n2, p2 in sorted(heap)]))
            return dict(found=True, path=path, cost=g, order=order, trace=trace, processed=len(order), stale=stale)
        for s in succ[node]:
            if s in explored:
                skipped.append(s)
                continue
            g2 = g + w[(node, s)]
            counter += 1
            heapq.heappush(heap, (g2 + h[s], counter, g2, s, path + [s]))
            generated.append(entry(s, g2, h[s]))
        trace.append(dict(step=step, before=before, node=node, g=g, h=h[node], f=f, generated=generated, skipped=skipped,
                          goal=False, stale=False, remaining=[entry(n2, g2, h[n2]) for f2, c2, g2, n2, p2 in sorted(heap)]))
    return dict(found=False, path=None, cost=None, order=order, trace=trace, processed=len(order), stale=stale)


def path_cost(path, w):
    """Independent check: sum edge weights along the path from the weight table."""
    return sum(w[(path[i], path[i + 1])] for i in range(len(path) - 1))


def breakdown(path, w):
    return " + ".join(str(w[(path[i], path[i + 1])]) for i in range(len(path) - 1))


def true_costs(succ, w, goal):
    """h*(n): true cheapest remaining cost from n to the goal (Dijkstra from the goal)."""
    dist = {goal: 0}
    heap = [(0, goal)]
    while heap:
        d, u = heapq.heappop(heap)
        if d > dist.get(u, float("inf")):
            continue
        for v in succ[u]:
            nd = d + w[(u, v)]
            if nd < dist.get(v, float("inf")):
                dist[v] = nd
                heapq.heappush(heap, (nd, v))
    return dist


def audit(succ, w, h, hstar):
    nodes = [dict(node=n, h=h[n], hstar=hstar[n], admissible=h[n] <= hstar[n]) for n in succ]
    edges = []
    for (u, v), c in sorted(w.items()):
        if u < v:
            edges.append(dict(u=u, v=v, w=c, hu=h[u], hv=h[v], ok_uv=h[u] <= c + h[v], ok_vu=h[v] <= c + h[u]))
    return dict(nodes=nodes, edges=edges,
                admissible=all(r["admissible"] for r in nodes),
                consistent=all(e["ok_uv"] and e["ok_vu"] for e in edges))
