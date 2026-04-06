from __future__ import annotations
from pynput.keyboard import Key, Controller

GESTURE_LABEL = "Thumb_Up"
GESTURE_NAME  = "thumb_up_2"

def matches(result) -> bool:
    if not result.gestures or len(result.gestures) != 2:
        return False
    return all(h[0].category_name == GESTURE_LABEL and h[0].score >= 0.70 for h in result.gestures)

def action() -> None:
    try:
        kb = Controller()
        # Windows Shortcut: Ctrl + Win + Right Arrow
        with kb.pressed(Key.cmd, Key.ctrl):
            kb.press(Key.right)
            kb.release(Key.right)
    except Exception as exc:
        print(f"[{GESTURE_NAME}] {exc}")