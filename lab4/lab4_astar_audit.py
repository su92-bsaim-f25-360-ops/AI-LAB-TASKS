"""Lab 4 - main program: manual-trace data, A* vs UCS, heuristic audit, overestimate experiments.
Run: python3 lab4_astar_audit.py     (all values are synthetic lab assumptions)"""
from lab4_search import load, search, path_cost, breakdown, true_costs, audit


def arrow(p):
    return " -> ".join(p) if p else "none"


def show_trace(r):
    print(f"{'step':<5}{'frontier before (node(g+h=f))':<52}{'processed':<10}{'g+h=f':<9}generated / skipped")
    for t in r["trace"]:
        node = ("STALE " if t["stale"] else "") + t["node"]
        gen = ", ".join(t["generated"]) if t["generated"] else "-"
        if t["skipped"]:
            gen += f"  | skipped (already processed): {', '.join(t['skipped'])}"
        print(f"{t['step']:<5}{'[' + ', '.join(t['before']) + ']':<52}{node:<10}{str(t['g']) + '+' + str(t['h']) + '=' + str(t['f']):<9}{gen}"
              f"{'   <- GOAL' if t['goal'] else ''}")


def summary(name, r, w):
    print(f"{name}: path {arrow(r['path'])} | reported cost {r['cost']} | independent sum {breakdown(r['path'], w)} = {path_cost(r['path'], w)}"
          f" | processed order {' '.join(r['order'])} | expansions (goal included) {r['processed']}"
          f" | excluding goal {r['processed'] - 1} | stale pops {r['stale']}")


def show_audit(title, a):
    print(title)
    for r in a["nodes"]:
        print(f"  {r['node']}: h={r['h']}  h*={r['hstar']}  {'admissible' if r['admissible'] else 'OVERESTIMATE'}")
    bad = [f"{e['u']}->{e['v']}" for e in a["edges"] if not e["ok_uv"]] + [f"{e['v']}->{e['u']}" for e in a["edges"] if not e["ok_vu"]]
    print(f"  admissible: {a['admissible']} | consistent: {a['consistent']}" + (f" | violated: {', '.join(bad)}" if bad else ""))


if __name__ == "__main__":
    start, goal, succ, w, h, labels = load()
    zero = {n: 0 for n in succ}
    hstar = true_costs(succ, w, goal)
    print("NOTE: campus graph, weights and heuristic are synthetic lab assumptions.\n")

    print("=== Heuristic audit (original heuristic) ===")
    show_audit("h versus true remaining cost h* (Dijkstra from G):", audit(succ, w, h, hstar))
    print()

    print("=== A* with the supplied heuristic ===")
    astar = search(succ, w, h, start, goal)
    show_trace(astar)
    summary("A*", astar, w)
    print("\n=== UCS (zero-heuristic control) ===")
    ucs = search(succ, w, zero, start, goal)
    show_trace(ucs)
    summary("UCS", ucs, w)

    print("\n=== Overestimate experiment: h(C) 3 -> 10 (one value changed) ===")
    h2 = dict(h); h2["C"] = 10
    print(f"original h(C) = {h['C']}, modified h(C) = {h2['C']}, true remaining cost h*(C) = {hstar['C']}")
    show_audit("audit of modified heuristic:", audit(succ, w, h2, hstar))
    over = search(succ, w, h2, start, goal)
    show_trace(over)
    summary("A* with h(C)=10", over, w)
    print(f"changed vs baseline A*: path {'changed' if over['path'] != astar['path'] else 'same'}, cost {astar['cost']} -> {over['cost']}, "
          f"expansions {astar['processed']} -> {over['processed']}")

    print("\n=== Supplementary experiment: h(E) 6 -> 20 (one value changed, node off the optimal path) ===")
    h3 = dict(h); h3["E"] = 20
    print(f"original h(E) = {h['E']}, modified h(E) = {h3['E']}, true remaining cost h*(E) = {hstar['E']}")
    show_audit("audit of modified heuristic:", audit(succ, w, h3, hstar))
    sup = search(succ, w, h3, start, goal)
    summary("A* with h(E)=20", sup, w)
    print(f"changed vs baseline A*: path {'changed' if sup['path'] != astar['path'] else 'same'}, cost {astar['cost']} -> {sup['cost']}, "
          f"expansions {astar['processed']} -> {sup['processed']}")
