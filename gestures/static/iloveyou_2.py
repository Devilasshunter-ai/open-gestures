from __future__ import annotations
from pynput.keyboard import Key, Controller

GESTURE_LABEL = "ILoveYou"
GESTURE_NAME  = "iloveyou_2"

def matches(result) -> bool:
    if not result.gestures or len(result.gestures) != 2:
        return False
    return all(h[0].category_name == GESTURE_LABEL and h[0].score >= 0.70
               for h in result.gestures)

def action() -> None:
    try:
        kb = Controller()
        with kb.pressed(Key.cmd):
            kb.press(Key.print_screen)
            kb.release(Key.print_screen)
    except Exception as exc:
        print(f"[{GESTURE_NAME}] {exc}")