"""Lab 3 - Task 3: uniform-cost search (UCS) on the weighted graph in graph.json.

Edge weights are SYNTHETIC LAB ASSUMPTIONS. No corridor is added: the topology is identical to the
original A-G graph; only weights are attached.
Frontier = priority queue ordered by (path cost, insertion order); ties are broken first-in-first-out.
The goal test is applied when a node is PROCESSED (popped), which is what makes UCS optimal.
"""
import heapq
from lab3_common import load_graph, arrow
from lab3_bfs_dfs import bfs


def ucs(succ, weights, start, goal):
    counter = 0
    heap = [(0, counter, start, [start])]
    explored, order, trace = set(), [], []
    step = 0
    while heap:
        step += 1
        before = [f"{n}({c})" for c, _, n, _ in sorted(heap)]
        cost, _, node, path = heapq.heappop(heap)
        if node in explored:
            trace.append(dict(step=step, before=before, processed=None, cost=cost, path=path, added=[], goal=False))
            continue
        explored.add(node)
        order.append(node)
        added = []
        if node == goal:
            trace.append(dict(step=step, before=before, processed=node, cost=cost, path=path, added=added, goal=True))
            return dict(found=True, path=path, cost=cost, order=order, trace=trace)
        for s in succ[node]:
            if s not in explored:
                counter += 1
                heapq.heappush(heap, (cost + weights[(node, s)], counter, s, path + [s]))
                added.append(f"{s}({cost + weights[(node, s)]})")
        trace.append(dict(step=step, before=before, processed=node, cost=cost, path=path, added=added, goal=False))
    return dict(found=False, path=None, cost=None, order=order, trace=trace)


def path_cost(path, weights):
    """Independent check: sum the edge weights along a path straight from the weight table."""
    return sum(weights[(path[i], path[i + 1])] for i in range(len(path) - 1))


def edge_breakdown(path, weights):
    return " + ".join(str(weights[(path[i], path[i + 1])]) for i in range(len(path) - 1))


if __name__ == "__main__":
    start, goal, succ, weights = load_graph()
    print("Weighted edges (undirected, synthetic assumptions):")
    for (u, v), w in sorted(weights.items()):
        if u < v:
            print(f"  {u}-{v}: {w}")
    print("\nUCS trace (frontier shown as node(cost), lowest cost first, ties FIFO)")
    r = ucs(succ, weights, start, goal)
    print(f"{'step':<5}{'frontier before':<34}{'processed':<10}{'cost':<6}{'path':<26}added")
    for t in r["trace"]:
        print(f"{t['step']:<5}{'[' + ', '.join(t['before']) + ']':<34}{str(t['processed']):<10}{t['cost']:<6}"
              f"{arrow(t['path']):<26}{', '.join(t['added']) if t['added'] else '-'}{'   <- GOAL' if t['goal'] else ''}")
    print(f"\nUCS processing order : {' '.join(r['order'])}")
    print(f"UCS path             : {arrow(r['path'])} ({len(r['path']) - 1} edges)")
    print(f"UCS reported cost    : {r['cost']}")
    print(f"Independent sum      : {edge_breakdown(r['path'], weights)} = {path_cost(r['path'], weights)}")
    b = bfs(succ, start, goal)
    print(f"\nBFS route (same topology): {arrow(b['path'])} ({len(b['path']) - 1} edges)")
    print(f"BFS route cost             : {edge_breakdown(b['path'], weights)} = {path_cost(b['path'], weights)}")
    print(f"Cost difference (BFS - UCS): {path_cost(b['path'], weights) - path_cost(r['path'], weights)}")
