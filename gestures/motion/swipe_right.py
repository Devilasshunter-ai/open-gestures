from __future__ import annotations
import time
from pynput.keyboard import Key, Controller

GESTURE_LABEL = "Open_Palm"
GESTURE_NAME  = "swipe_right_1"

# ── Swipe state (module-level so it persists across frames) ─────────────────
_history:    list[tuple[float, float]] = []  # (wrist_x, timestamp)
_last_fired: float = 0.0

_WINDOW       = 0.40   # seconds — how long the swipe window is
_MIN_DISTANCE = 0.20   # 20% of frame width minimum travel
_COOLDOWN     = 1.0    # seconds between triggers


def matches(result) -> bool:
    global _history, _last_fired

    # Must have exactly 1 hand detected
    if not result.gestures or len(result.gestures) != 1:
        _history.clear()
        return False

    top = result.gestures[0][0]
    if top.category_name != GESTURE_LABEL or top.score < 0.65:
        _history.clear()
        return False

    # hand_landmarks[0] = first hand, landmark 0 = wrist
    try:
        wrist_x = result.hand_landmarks[0][0].x   # 0.0 = left edge, 1.0 = right edge
    except (IndexError, AttributeError):
        _history.clear()
        return False

    now = time.monotonic()

    # Keep only samples within the time window
    _history = [(x, t) for x, t in _history if now - t <= _WINDOW]
    _history.append((wrist_x, now))

    if len(_history) < 3:   # need at least 3 samples for a reliable swipe
        return False

    # Positive delta = hand moved right (frame is already mirrored in main.py)
    delta = _history[-1][0] - _history[0][0]

    if delta >= _MIN_DISTANCE and now - _last_fired >= _COOLDOWN:
        _last_fired = now
        _history.clear()
        return True

    return False


def action() -> None:
    try:
        kb = Controller()
        # Alt + Tab = cycle forward through open windows
        with kb.pressed(Key.alt):
            kb.press(Key.tab)
            kb.release(Key.tab)
    except Exception as exc:
        print(f"[{GESTURE_NAME}] {exc}")