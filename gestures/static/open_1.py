from __future__ import annotations
from pynput.keyboard import Key, Controller

GESTURE_LABEL = "Open_Palm"
GESTURE_NAME  = "open_1"

def matches(result) -> bool:
    if not result.gestures or len(result.gestures) != 1:
        return False
    top = result.gestures[0][0]
    return top.category_name == GESTURE_LABEL and top.score >= 0.70

def action() -> None:
    try:
        kb = Controller()
        kb.press(Key.media_play_pause)
        kb.release(Key.media_play_pause)
    except Exception as exc:
        print(f"[{GESTURE_NAME}] {exc}")