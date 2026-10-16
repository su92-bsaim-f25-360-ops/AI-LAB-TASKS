"""Lab 5 - Minimax and alpha-beta pruning with a leaf-evaluation counter.

The tree (tree.json) and its leaf values are SYNTHETIC LAB ASSUMPTIONS. The root A is a MAX node and
players alternate by level (A: MAX, B/C: MIN, D/E/F/G: MAX, leaves L1-L8).
Both algorithms take a `stats` dict: stats["leaves"] counts leaf evaluations and stats["order"] records
the leaves evaluated, in order.  Alpha-beta cut-offs: MAX node when v >= beta, MIN node when v <= alpha.
"""
import json
import os

INF = float("inf")
HERE = os.path.dirname(os.path.abspath(__file__))


def load_tree(path=None):
    with open(path or os.path.join(HERE, "tree.json")) as f:
        return json.load(f)


def is_leaf(node):
    return "value" in node


def new_stats():
    return {"leaves": 0, "order": []}


def leaf_names(node):
    return [node["name"]] if is_leaf(node) else [n for c in node["children"] for n in leaf_names(c)]


def minimax(node, maximizing, stats, trace=None):
    if is_leaf(node):
        stats["leaves"] += 1                       # leaf-evaluation counter
        stats["order"].append(node["name"])
        return node["value"]
    values = [minimax(c, not maximizing, stats, trace) for c in node["children"]]
    v = max(values) if maximizing else min(values)
    if trace is not None:
        trace.append(dict(node=node["name"], type="MAX" if maximizing else "MIN",
                          children=[c["name"] for c in node["children"]], child_values=values, value=v))
    return v


def _f(x):
    return "-inf" if x == -INF else ("+inf" if x == INF else str(x))


def alphabeta(node, maximizing, alpha, beta, stats, trace=None):
    if is_leaf(node):
        stats["leaves"] += 1                       # leaf-evaluation counter
        stats["order"].append(node["name"])
        if trace is not None:
            trace.append(dict(ev="leaf", node=node["name"], value=node["value"], count=stats["leaves"]))
        return node["value"]
    kind = "MAX" if maximizing else "MIN"
    if trace is not None:
        trace.append(dict(ev="enter", node=node["name"], type=kind, alpha=_f(alpha), beta=_f(beta)))
    v = -INF if maximizing else INF
    kids = node["children"]
    for i, c in enumerate(kids):
        child_v = alphabeta(c, not maximizing, alpha, beta, stats, trace)
        if maximizing:
            v = max(v, child_v)
            alpha = max(alpha, v)
            cut = v >= beta
            cond = f"v={v} >= beta={_f(beta)}"
        else:
            v = min(v, child_v)
            beta = min(beta, v)
            cut = v <= alpha
            cond = f"v={v} <= alpha={_f(alpha)}"
        if cut and i < len(kids) - 1:
            rest = kids[i + 1:]
            if trace is not None:
                trace.append(dict(ev="cutoff", node=node["name"], cond=cond, pruned=[r["name"] for r in rest],
                                  pruned_leaves=[n for r in rest for n in leaf_names(r)]))
            break
    if trace is not None:
        trace.append(dict(ev="return", node=node["name"], value=v))
    return v


def run_minimax(tree, trace=None):
    s = new_stats()
    return minimax(tree, True, s, trace), s


def run_alphabeta(tree, trace=None):
    s = new_stats()
    return alphabeta(tree, True, -INF, INF, s, trace), s


if __name__ == "__main__":
    tree = load_tree()
    print("NOTE: tree and leaf values are synthetic lab assumptions.\n")
    mt = []
    v, s = run_minimax(tree, mt)
    print("MINIMAX (post-order evaluation)")
    for t in mt:
        print(f"  {t['node']} ({t['type']}): children {t['children']} values {t['child_values']} -> {t['value']}")
    print(f"  root value {v} | leaves evaluated {s['leaves']} | order {' '.join(s['order'])}\n")
    at = []
    v2, s2 = run_alphabeta(tree, at)
    print("ALPHA-BETA trace")
    for t in at:
        if t["ev"] == "enter":
            print(f"  enter {t['node']} ({t['type']}) alpha={t['alpha']} beta={t['beta']}")
        elif t["ev"] == "leaf":
            print(f"  evaluate leaf {t['node']} = {t['value']} (leaf #{t['count']})")
        elif t["ev"] == "cutoff":
            print(f"  CUTOFF at {t['node']}: {t['cond']} -> prune {', '.join(t['pruned'])} (leaves {', '.join(t['pruned_leaves'])})")
        else:
            print(f"  return {t['node']} = {t['value']}")
    print(f"  root value {v2} | leaves evaluated {s2['leaves']} | order {' '.join(s2['order'])}\n")
    print(f"Same root value: {v == v2} | minimax leaves {s['leaves']} vs alpha-beta leaves {s2['leaves']}")
