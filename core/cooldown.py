"""
core/cooldown.py
────────────────
Per-gesture cooldown registry.

Every gesture name is registered here with its cooldown duration in seconds.
can_trigger() is fail-open: unregistered gestures always return True so new
gestures never silently break — add them here once they're stable.
"""
from __future__ import annotations
import time

# ── Default durations (seconds) ───────────────────────────────────────────
_DEFAULTS: dict[str, float] = {
    # Static — single hand
    "thumb_up_1"    : 0.3,
    "thumb_down_1"  : 0.3,
    "open_1"        : 0.4,
    "close_1"       : 0.4,
    "point_up_1"    : 0.15,
    "point_down_1"  : 0.15,
    "iloveyou_1"    : 2.0,

    # Static — double hand (same gesture performed with both hands)
    "thumb_up_2"    : 0.8,
    "thumb_down_2"  : 0.8,
    "open_2"        : 0.6,
    "close_2"       : 0.6,
    "point_up_2"    : 0.6,
    "point_down_2"  : 0.6,
    "iloveyou_2"    : 1.0,

    # Motion
    "swipe_left"    : 0.6,
    "swipe_right"   : 0.6,
    "swipe_up"      : 0.6,
    "swipe_down"    : 0.6,
}


class Cooldown:
    def __init__(self, overrides: dict[str, float] | None = None) -> None:
        self._durations: dict[str, float] = dict(_DEFAULTS)
        if overrides:
            self._durations.update(overrides)
        self._last_trigger: dict[str, float] = {}

    def can_trigger(self, gesture: str) -> bool:
        """
        True if the gesture's cooldown has elapsed.
        Unknown gestures are treated as always ready (fail-open).
        """
        duration = self._durations.get(gesture, 0.0)
        if duration == 0.0:
            return True
        elapsed = time.monotonic() - self._last_trigger.get(gesture, 0.0)
        return elapsed >= duration

    def record(self, gesture: str) -> None:
        self._last_trigger[gesture] = time.monotonic()

    def remaining(self, gesture: str) -> float:
        """Seconds until ready (0.0 if already ready)."""
        duration = self._durations.get(gesture, 0.0)
        elapsed  = time.monotonic() - self._last_trigger.get(gesture, 0.0)
        return max(0.0, duration - elapsed)

    def set(self, gesture: str, seconds: float) -> None:
        """Override a cooldown at runtime."""
        self._durations[gesture] = seconds