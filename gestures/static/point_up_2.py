from __future__ import annotations
from pynput.keyboard import Key, Controller, KeyCode

GESTURE_LABEL = "Pointing_Up"
GESTURE_NAME  = "point_up_2"

def matches(result) -> bool:
    if not result.gestures or len(result.gestures) != 2:
        return False
    return all(h[0].category_name == GESTURE_LABEL and h[0].score >= 0.70
               for h in result.gestures)

def action() -> None:
    try:
        kb = Controller()
        with kb.pressed(Key.ctrl):
            kb.press(KeyCode.from_char('='))
            kb.release(KeyCode.from_char('='))
    except Exception as exc:
        print(f"[{GESTURE_NAME}] {exc}")