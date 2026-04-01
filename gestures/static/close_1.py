"""
gestures/static/close_1.py
───────────────────────────
Single-hand ✊  Closed Fist
Action: Pause Audio (media pause key)
"""
from __future__ import annotations

GESTURE_LABEL = "Closed_Fist"
GESTURE_NAME  = "close_1"


def matches(result) -> bool:
    if not result.gestures or len(result.gestures) != 1:
        return False
    top = result.gestures[0][0]
    return top.category_name == GESTURE_LABEL and top.score >= 0.70


def action() -> None:
    try:
        from pynput.keyboard import Key, Controller
        kb = Controller()
        kb.press(Key.media_play_pause)
        kb.release(Key.media_play_pause)
    except Exception as exc:
        print(f"[{GESTURE_NAME}] {exc}")