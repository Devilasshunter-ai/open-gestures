"""
gestures/static/open_1.py
──────────────────────────
Single-hand 👋  Open Palm
Action: PLAY only — will not pause if already playing.
"""
from __future__ import annotations

from gestures.static.media_state import can_fire, mark_fired, is_playing, set_playing

GESTURE_LABEL = "Open_Palm"
GESTURE_NAME  = "open_1"


def matches(result) -> bool:
    if not result.gestures or len(result.gestures) != 1:
        return False
    top = result.gestures[0][0]
    return top.category_name == GESTURE_LABEL and top.score >= 0.70


def action() -> None:
    # Only fire if cooldown has passed AND media is currently paused
    if not can_fire(GESTURE_NAME):
        return
    if is_playing():
        return  # Already playing, do nothing

    mark_fired(GESTURE_NAME)
    set_playing(True)  # Mark as playing

    try:
        from pynput.keyboard import Key, Controller
        kb = Controller()
        kb.press(Key.media_play_pause)
        kb.release(Key.media_play_pause)
    except Exception as exc:
        print(f"[{GESTURE_NAME}] {exc}")