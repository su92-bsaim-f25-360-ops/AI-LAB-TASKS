"""Lab 2 - percepts and the simple reflex controller (no memory).

All thresholds are SYNTHETIC LAB ASSUMPTIONS for a room heating/cooling controller.
Rules: occupancy has priority. Empty room -> OFF. Occupied room: temperature >= 26 -> COOL,
temperature <= 20 -> HEAT, otherwise IDLE.
"""
import csv

COOL_AT = 26.0   # synthetic assumption
HEAT_AT = 20.0   # synthetic assumption


def make_percept(temperature, occupied):
    return {"temperature": float(temperature), "occupied": bool(occupied)}


def reflex_target(percept):
    """Target mode chosen from the current percept only."""
    if not percept["occupied"]:          # occupancy priority
        return "OFF"
    if percept["temperature"] >= COOL_AT:
        return "COOL"
    if percept["temperature"] <= HEAT_AT:
        return "HEAT"
    return "IDLE"


def load_percepts(path):
    """Read percept rows from a CSV file (step,temperature,occupied,...)."""
    rows = []
    with open(path, newline="") as f:
        for r in csv.DictReader(f):
            r["percept"] = make_percept(r["temperature"], r["occupied"] == "1")
            rows.append(r)
    return rows


if __name__ == "__main__":
    for t, o in [(23, True), (26, True), (20, True), (28, False)]:
        p = make_percept(t, o)
        print(p, "->", reflex_target(p))
