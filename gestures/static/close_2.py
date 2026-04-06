from __future__ import annotations
from pynput.keyboard import Key, Controller

GESTURE_LABEL = "Closed_Fist"
GESTURE_NAME  = "close_2"

def matches(result) -> bool:
    if not result.gestures or len(result.gestures) != 2:
        return False
    return all(h[0].category_name == GESTURE_LABEL and h[0].score >= 0.70
               for h in result.gestures)

def action() -> None:
    try:
        kb = Controller()
        with kb.pressed(Key.alt):
            kb.press(Key.f4)
            kb.release(Key.f4)
    except Exception as exc:
        print(f"[{GESTURE_NAME}] {exc}")