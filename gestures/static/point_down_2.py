"""
gestures/static/point_down_2.py
────────────────────────────────
Double-hand ✌️✌️  Victory (both hands)
Action: Zoom Out (Ctrl+-)

Cross-platform: uses explicit press/release which works reliably
on both Windows and Linux (avoids stuck keys on some Linux WMs).
"""
from __future__ import annotations
from pynput.keyboard import Key, Controller

GESTURE_LABEL = "Victory"
GESTURE_NAME  = "point_down_2"


def matches(result) -> bool:
    if not result.gestures or len(result.gestures) != 2:
        return False
    return all(h[0].category_name == GESTURE_LABEL and h[0].score >= 0.70
               for h in result.gestures)


def action() -> None:
    try:
        kb = Controller()
        kb.press(Key.ctrl)
        kb.press('-')
        kb.release('-')
        kb.release(Key.ctrl)
    except Exception as exc:
        print(f"[{GESTURE_NAME}] {exc}")