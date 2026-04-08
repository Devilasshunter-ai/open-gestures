"""
gestures/static/thumb_down_2.py
────────────────────────────────
Double-hand 👎👎  Thumb Down (both hands)
Action: Previous virtual desktop / workspace

Cross-platform:
  Windows → Ctrl + Win + Left   (previous virtual desktop)
  Linux   → Ctrl + Alt + Left   (previous workspace, works on most WMs)
"""
from __future__ import annotations
import sys
from pynput.keyboard import Key, Controller

GESTURE_LABEL = "Thumb_Down"
GESTURE_NAME  = "thumb_down_2"


def matches(result) -> bool:
    if not result.gestures or len(result.gestures) != 2:
        return False
    return all(h[0].category_name == GESTURE_LABEL and h[0].score >= 0.70
               for h in result.gestures)


def action() -> None:
    try:
        kb = Controller()
        if sys.platform == "win32":
            # Ctrl + Win + Left = previous virtual desktop
            with kb.pressed(Key.cmd, Key.ctrl):
                kb.press(Key.left)
                kb.release(Key.left)
        else:
            # Ctrl + Alt + Left = previous workspace
            kb.press(Key.ctrl)
            kb.press(Key.alt)
            kb.press(Key.left)
            kb.release(Key.left)
            kb.release(Key.alt)
            kb.release(Key.ctrl)
    except Exception as exc:
        print(f"[{GESTURE_NAME}] {exc}")