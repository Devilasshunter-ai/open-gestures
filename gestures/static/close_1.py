"""
gestures/static/close_1.py
───────────────────────────
Single-hand ✊  Closed Fist
Action: PAUSE only — will not unpause if already paused.
"""
from __future__ import annotations

from gestures.static.media_state import can_fire, mark_fired, is_playing, set_playing

GESTURE_LABEL = "Closed_Fist"
GESTURE_NAME  = "close_1"


def matches(result) -> bool:
    if not result.gestures or len(result.gestures) != 1:
        return False
    top = result.gestures[0][0]
    return top.category_name == GESTURE_LABEL and top.score >= 0.70


def action() -> None:
    # Only fire if cooldown has passed AND media is currently playing
    if not can_fire(GESTURE_NAME):
        return
    if not is_playing():
        return  # Already paused, do nothing

    mark_fired(GESTURE_NAME)
    set_playing(False)  # Mark as paused

    try:
        from pynput.keyboard import Key, Controller
        kb = Controller()
        kb.press(Key.media_play_pause)
        kb.release(Key.media_play_pause)
    except Exception as exc:
        print(f"[{GESTURE_NAME}] {exc}")