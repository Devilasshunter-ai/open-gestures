"""
gestures/static/point_up_1.py
──────────────────────────────
Single-hand ☝️  Pointing Up
Action: Brightness Up
"""
from __future__ import annotations

GESTURE_LABEL = "Pointing_Up"
GESTURE_NAME  = "point_up_1"


def matches(result) -> bool:
    if not result.gestures or len(result.gestures) != 1:
        return False
    top = result.gestures[0][0]
    return top.category_name == GESTURE_LABEL and top.score >= 0.70


def action() -> None:
    try:
        import subprocess
        subprocess.Popen(
            ["brightnessctl", "set", "5%+"],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
    except Exception as exc:
        print(f"[{GESTURE_NAME}] {exc}")