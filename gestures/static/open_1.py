"""
gestures/static/open_1.py
──────────────────────────
Single-hand 👋  Open Palm
Action: Play Audio (media play/pause key)

Same key as pause — most media players toggle on the same key.
"""
from __future__ import annotations

GESTURE_LABEL = "Open_Palm"
GESTURE_NAME  = "open_1"


def matches(result) -> bool:
    if not result.gestures or len(result.gestures) != 1:
        return False
    top = result.gestures[0][0]
    return top.category_name == GESTURE_LABEL and top.score >= 0.70


def action() -> None:
    try:
        from pynput.keyboard import Key, Controller
        kb = Controller()
        kb.press(Key.media_play_pause)
        kb.release(Key.media_play_pause)
    except Exception as exc:
        print(f"[{GESTURE_NAME}] {exc}")