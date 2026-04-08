"""
gestures/static/media_state.py
────────────────────────────────
Shared cooldown / debounce state for static media gestures.
Also tracks whether media is currently playing or paused so that
open/close gestures don't toggle — they set a definite state.
"""
from __future__ import annotations

import time
from typing import Dict

# Seconds between repeated actions for the same gesture.
DEFAULT_COOLDOWN: float = 1.0

# { gesture_name -> last_fired_timestamp }
_last_fired: Dict[str, float] = {}

# Tracks whether we think media is currently playing.
# Starts as True (assume something is playing when app launches).
_is_playing: bool = True


def can_fire(gesture_name: str, cooldown: float = DEFAULT_COOLDOWN) -> bool:
    """Return True if the gesture is allowed to fire right now."""
    now = time.monotonic()
    last = _last_fired.get(gesture_name, 0.0)
    return (now - last) >= cooldown


def mark_fired(gesture_name: str) -> None:
    """Record that a gesture just fired (resets its cooldown timer)."""
    _last_fired[gesture_name] = time.monotonic()


def is_playing() -> bool:
    """Return True if we believe media is currently playing."""
    return _is_playing


def set_playing(state: bool) -> None:
    """Manually set the playing state."""
    global _is_playing
    _is_playing = state


def reset(gesture_name: str) -> None:
    """Manually clear the cooldown for a gesture (useful for testing)."""
    _last_fired.pop(gesture_name, None)


def reset_all() -> None:
    """Clear every gesture's cooldown state."""
    _last_fired.clear()