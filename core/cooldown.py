from __future__ import annotations
import time

_DEFAULTS: dict[str, float] = {
    "thumb_up_1"    : 0.3,
    "thumb_down_1"  : 0.3,
    "open_1"        : 0.4,
    "close_1"       : 0.4,
    "point_up_1"    : 0.15,
    "point_down_1"  : 0.15,
    "iloveyou_1"    : 2.0,
    "thumb_up_2"    : 0.8,
    "thumb_down_2"  : 0.8,
    "open_2"        : 0.6,
    "close_2"       : 0.6,
    "point_up_2"    : 0.6,
    "point_down_2"  : 0.6,
    "iloveyou_2"    : 1.0,
}

class Cooldown:
    def __init__(self, overrides: dict[str, float] | None = None) -> None:
        self._durations: dict[str, float] = dict(_DEFAULTS)
        if overrides:
            self._durations.update(overrides)
        self._last_trigger: dict[str, float] = {}

    def can_trigger(self, gesture: str) -> bool:
        duration = self._durations.get(gesture, 0.0)
        if duration == 0.0:
            return True
        elapsed = time.monotonic() - self._last_trigger.get(gesture, 0.0)
        return elapsed >= duration

    def record(self, gesture: str) -> None:
        self._last_trigger[gesture] = time.monotonic()