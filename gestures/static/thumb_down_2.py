"""
gestures/static/thumb_down_2.py
────────────────────────────────
Double-hand 👎👎  Thumb Down (both hands)
Action: Previous Workspace (Ctrl+Alt+Left)
"""
from __future__ import annotations

GESTURE_LABEL = "Thumb_Down"
GESTURE_NAME  = "thumb_down_2"


def matches(result) -> bool:
    if not result.gestures or len(result.gestures) != 2:
        return False
    return all(h[0].category_name == GESTURE_LABEL and h[0].score >= 0.70
               for h in result.gestures)


def action() -> None:
    try:
        from pynput.keyboard import Key, Controller
        kb = Controller()
        kb.press(Key.ctrl)
        kb.press(Key.alt)
        kb.press(Key.left)
        kb.release(Key.left)
        kb.release(Key.alt)
        kb.release(Key.ctrl)
    except Exception as exc:
        print(f"[{GESTURE_NAME}] {exc}")