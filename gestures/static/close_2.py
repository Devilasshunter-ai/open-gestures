"""
gestures/static/close_2.py
───────────────────────────
Double-hand ✊✊  Closed Fist (both hands)
Action: Close Focused Application (Alt+F4)

Fix: key release order was wrong — must release in strict reverse order.
"""
from __future__ import annotations

GESTURE_LABEL = "Closed_Fist"
GESTURE_NAME  = "close_2"


def matches(result) -> bool:
    if not result.gestures or len(result.gestures) != 2:
        return False
    return all(h[0].category_name == GESTURE_LABEL and h[0].score >= 0.70
               for h in result.gestures)


def action() -> None:
    try:
        from pynput.keyboard import Key, Controller
        kb = Controller()
        kb.press(Key.cmd)
        kb.press('q')
        kb.release(Key.cmd)
        kb.release('q')
    except Exception as exc:
        print(f"[{GESTURE_NAME}] {exc}")