"""
gestures/static/point_down_1.py
────────────────────────────────
Single-hand ✌️  Victory
Action: Brightness Down (Windows Compatible)
"""
from __future__ import annotations

GESTURE_LABEL = "Victory"
GESTURE_NAME  = "point_down_1"


def matches(result) -> bool:
    if not result.gestures or len(result.gestures) != 1:
        return False
    top = result.gestures[0][0]
    return top.category_name == GESTURE_LABEL and top.score >= 0.70


def action() -> None:
    try:
        import screen_brightness_control as sbc
        # Get current brightness and decrease by 5%
        current_brightness = sbc.get_brightness(display=0)[0]
        sbc.set_brightness(current_brightness - 5)
    except Exception as exc:
        print(f"[{GESTURE_NAME}] {exc}")