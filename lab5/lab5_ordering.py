"""Lab 5 - Task 3: reorder branches and observe pruning. The root value must never change.

Orderings of the supplied tree:
  original      - tree.json as given
  reversed      - children reversed at every node
  root_swapped  - only the root's two children swapped
  best (oracle) - MAX nodes try the highest-valued child first, MIN nodes the lowest-valued first
  worst (oracle)- MAX nodes try the lowest-valued child first, MIN nodes the highest-valued first
Also: 200 seeded random trees (branching 3, depth 4, leaves in -10..10) to compare average work.
"""
import copy
import random
from lab5_minimax import load_tree, is_leaf, new_stats, minimax, run_minimax, run_alphabeta


def value_of(node, maximizing):
    return minimax(node, maximizing, new_stats())


def reorder(node, mode, maximizing=True, is_root=True):
    node = copy.deepcopy(node)
    if is_leaf(node):
        return node
    kids = [reorder(c, mode, not maximizing, False) for c in node["children"]]
    if mode == "reversed":
        kids.reverse()
    elif mode == "root_swapped" and is_root:
        kids.reverse()
    elif mode in ("best", "worst"):
        vals = [value_of(k, not maximizing) for k in kids]
        high_first = (mode == "best") == maximizing        # best: MAX high-first, MIN low-first
        # ties keep their original relative order
        pairs = sorted(zip(vals, range(len(kids))), key=lambda p: (-p[0] if high_first else p[0], p[1]))
        kids = [kids[i] for _, i in pairs]
    node["children"] = kids
    return node


def random_tree(depth, branching, rng, counter):
    counter[0] += 1
    name = f"n{counter[0]}"                       # unique node name
    if depth == 0:
        return {"name": name, "value": rng.randint(-10, 10)}
    return {"name": name, "children": [random_tree(depth - 1, branching, rng, counter) for _ in range(branching)]}


MODES = ["original", "reversed", "root_swapped", "best", "worst"]


def supplied_tree_results():
    tree = load_tree()
    mv, ms = run_minimax(tree)
    rows = []
    for m in MODES:
        t = reorder(tree, m)
        v, s = run_alphabeta(t)
        rows.append(dict(mode=m, value=v, leaves=s["leaves"], order=s["order"], minimax_value=run_minimax(t)[0]))
    return mv, ms["leaves"], rows


def random_experiment(trials=200, branching=3, depth=4, seed=42):
    rng = random.Random(seed)
    stats = {m: [] for m in ("original", "best", "worst")}
    mm_leaves, agree = [], 0
    for _ in range(trials):
        t = random_tree(depth, branching, rng, [0])
        mv, ms = run_minimax(t)
        mm_leaves.append(ms["leaves"])
        ok = True
        for m in stats:
            v, s = run_alphabeta(reorder(t, m))
            ok = ok and (v == mv)
            stats[m].append(s["leaves"])
        agree += ok
    summ = {m: dict(mean=sum(x) / len(x), min=min(x), max=max(x)) for m, x in stats.items()}
    return dict(trials=trials, branching=branching, depth=depth, seed=seed, agree=agree,
                minimax_leaves=mm_leaves[0], stats=summ)


if __name__ == "__main__":
    mv, ml, rows = supplied_tree_results()
    print("NOTE: tree, leaf values and random leaves are synthetic lab assumptions.\n")
    print(f"Supplied tree: Minimax root value {mv}, leaves evaluated {ml}\n")
    print(f"{'ordering':<14}{'alpha-beta value':<18}{'leaves':<8}{'pruned':<8}leaves evaluated (in order)")
    for r in rows:
        print(f"{r['mode']:<14}{r['value']:<18}{r['leaves']:<8}{ml - r['leaves']:<8}{' '.join(r['order'])}")
    print(f"\nAll alpha-beta values equal the Minimax value: {all(r['value'] == mv and r['minimax_value'] == mv for r in rows)}\n")
    e = random_experiment()
    print(f"Random trees: {e['trials']} trials, branching {e['branching']}, depth {e['depth']}, seed {e['seed']}")
    print(f"  Minimax always evaluates {e['minimax_leaves']} leaves")
    for m, s in e["stats"].items():
        print(f"  alpha-beta, {m:<8} ordering: mean leaves {s['mean']:.1f} (min {s['min']}, max {s['max']})")
    print(f"  trials where alpha-beta value equalled Minimax in every ordering: {e['agree']} of {e['trials']}")
