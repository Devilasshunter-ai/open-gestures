"""
gestures/static/thumb_up_1.py
──────────────────────────────
Single-hand 👍  Thumb Up
Action: Volume Up (+5% via pactl)

Fix: Key.media_volume_up is unreliable on many Linux setups without
a physical keyboard mapping. pactl is direct and always works on
PulseAudio / PipeWire regardless of display server.
"""
from __future__ import annotations

GESTURE_LABEL = "Thumb_Up"
GESTURE_NAME  = "thumb_up_1"


def matches(result) -> bool:
    if not result.gestures or len(result.gestures) != 1:
        return False
    top = result.gestures[0][0]
    return top.category_name == GESTURE_LABEL and top.score >= 0.70


def action() -> None:
    try:
        import subprocess
        subprocess.Popen(
            ["pactl", "set-sink-volume", "@DEFAULT_SINK@", "+5%"],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
    except Exception as exc:
        print(f"[{GESTURE_NAME}] {exc}")