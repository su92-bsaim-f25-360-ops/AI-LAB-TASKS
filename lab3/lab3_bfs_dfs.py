"""Lab 3 - Task 1: BFS and DFS with full frontier traces (goal test when a node is PROCESSED).

BFS: FIFO queue; a successor is added only if it is not already processed or in the queue.
DFS: LIFO stack; successors are pushed in reverse so the FIRST listed successor is popped first;
     a successor is pushed if it is not yet processed (duplicates on the stack are allowed).
Frontier lists: BFS front -> back; DFS bottom -> top (top is the right-most item).
"""
from collections import deque
from lab3_common import load_graph, arrow


def bfs(succ, start, goal):
    frontier = deque([(start, [start])])
    in_frontier = {start}
    explored, order, trace = set(), [], []
    step = 0
    while frontier:
        step += 1
        before = [n for n, _ in frontier]
        node, path = frontier.popleft()
        in_frontier.discard(node)
        explored.add(node)
        order.append(node)
        added = []
        if node == goal:
            trace.append(dict(step=step, before=before, processed=node, path=path, added=added, goal=True))
            return dict(found=True, path=path, order=order, trace=trace)
        for s in succ[node]:
            if s not in explored and s not in in_frontier:
                frontier.append((s, path + [s]))
                in_frontier.add(s)
                added.append(s)
        trace.append(dict(step=step, before=before, processed=node, path=path, added=added, goal=False))
    return dict(found=False, path=None, order=order, trace=trace)


def dfs(succ, start, goal):
    stack = [(start, [start])]
    explored, order, trace = set(), [], []
    step = 0
    while stack:
        step += 1
        before = [n for n, _ in stack]
        node, path = stack.pop()
        if node in explored:                     # stale duplicate entry
            trace.append(dict(step=step, before=before, processed=None, path=path, added=[], goal=False))
            continue
        explored.add(node)
        order.append(node)
        added = []
        if node == goal:
            trace.append(dict(step=step, before=before, processed=node, path=path, added=added, goal=True))
            return dict(found=True, path=path, order=order, trace=trace)
        for s in reversed(succ[node]):
            if s not in explored:
                stack.append((s, path + [s]))
                added.append(s)
        trace.append(dict(step=step, before=before, processed=node, path=path, added=added, goal=False))
    return dict(found=False, path=None, order=order, trace=trace)


def show(name, result):
    print(f"{name} trace")
    print(f"{'step':<5}{'frontier before':<22}{'processed':<10}{'path':<26}{'added (push order)'}")
    for t in result["trace"]:
        print(f"{t['step']:<5}{'[' + ', '.join(t['before']) + ']':<22}{str(t['processed']):<10}"
              f"{arrow(t['path']):<26}{', '.join(t['added']) if t['added'] else '-'}"
              f"{'   <- GOAL' if t['goal'] else ''}")
    print(f"{name} visit order : {' '.join(result['order'])}")
    print(f"{name} final path  : {arrow(result['path'])}  ({len(result['path']) - 1} edges)\n")


if __name__ == "__main__":
    start, goal, succ, _ = load_graph()
    print(f"Start {start}, goal {goal}\n")
    show("BFS", bfs(succ, start, goal))
    show("DFS", dfs(succ, start, goal))
