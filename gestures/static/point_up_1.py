from __future__ import annotations
import screen_brightness_control as sbc

GESTURE_LABEL = "Pointing_Up"
GESTURE_NAME  = "point_up_1"

def matches(result) -> bool:
    if not result.gestures or len(result.gestures) != 1:
        return False
    top = result.gestures[0][0]
    return top.category_name == GESTURE_LABEL and top.score >= 0.70

def action() -> None:
    try:
        sbc.set_brightness('+5')
    except Exception as exc:
        print(f"[{GESTURE_NAME}] {exc}")