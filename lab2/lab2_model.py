"""Lab 2 - stateful (model-based) controller.

Same thresholds and occupancy priority as lab2_percepts.reflex_target, plus internal
storage of the previous target mode so identical commands are not repeated.
"""
from lab2_percepts import reflex_target


class StatefulController:
    def __init__(self):
        self._previous_target = None     # nothing commanded yet

    @property
    def previous_target(self):
        return self._previous_target

    def step(self, percept):
        """Return (target_mode, send_command). send_command is False when the target
        equals the previously stored target."""
        target = reflex_target(percept)
        send_command = target != self._previous_target
        self._previous_target = target
        return target, send_command
