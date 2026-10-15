"""Lab 3 - shared helpers: loads graph.json (start, goal, successor order, edge weights).
The graph is undirected; successor lists give the order in which neighbours are tried.
Edge weights are SYNTHETIC LAB ASSUMPTIONS (arbitrary corridor costs)."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def load_graph(path=None):
    with open(path or os.path.join(HERE, "graph.json")) as f:
        data = json.load(f)
    weights = {}
    for key, w in data["weights"].items():
        u, v = key.split("-")
        weights[(u, v)] = w
        weights[(v, u)] = w            # undirected
    return data["start"], data["goal"], data["successors"], weights


def arrow(path):
    return " -> ".join(path) if path else "none"
