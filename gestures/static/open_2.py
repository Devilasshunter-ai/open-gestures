from __future__ import annotations
import os

GESTURE_LABEL = "Open_Palm"
GESTURE_NAME  = "open_2"

def matches(result) -> bool:
    if not result.gestures or len(result.gestures) != 2:
        return False
    return all(h[0].category_name == GESTURE_LABEL and h[0].score >= 0.70
               for h in result.gestures)

def action() -> None:
    try:
        os.system("start https://www.google.com")
    except Exception as exc:
        print(f"[{GESTURE_NAME}] {exc}")