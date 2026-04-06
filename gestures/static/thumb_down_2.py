from __future__ import annotations
from pynput.keyboard import Key, Controller

GESTURE_LABEL = "Thumb_Down"
GESTURE_NAME  = "thumb_down_2"

def matches(result) -> bool:
    if not result.gestures or len(result.gestures) != 2:
        return False
    return all(h[0].category_name == GESTURE_LABEL and h[0].score >= 0.70 for h in result.gestures)

def action() -> None:
    try:
        kb = Controller()
        # Windows Shortcut: Ctrl + Win + Left Arrow
        with kb.pressed(Key.cmd, Key.ctrl):
            kb.press(Key.left)
            kb.release(Key.left)
    except Exception as exc:
        print(f"[{GESTURE_NAME}] {exc}")