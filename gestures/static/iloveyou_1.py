"""
gestures/static/iloveyou_1.py
──────────────────────────────
Single-hand 🤟  ILoveYou
Action: Mute / Unmute System Audio (toggle)

Windows: uses pycaw (pythoncom + _dev.Activate)
Linux:   uses pactl
"""
from __future__ import annotations
import sys

GESTURE_LABEL = "ILoveYou"
GESTURE_NAME  = "iloveyou_1"


def matches(result) -> bool:
    if not result.gestures or len(result.gestures) != 1:
        return False
    top = result.gestures[0][0]
    return top.category_name == GESTURE_LABEL and top.score >= 0.70


def action() -> None:
    try:
        if sys.platform == "win32":
            import pythoncom
            from ctypes import cast, POINTER
            from comtypes import CLSCTX_ALL
            from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
            pythoncom.CoInitialize()
            try:
                devices = AudioUtilities.GetSpeakers()
                interface = devices._dev.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
                volume = cast(interface, POINTER(IAudioEndpointVolume))
                volume.SetMute(not volume.GetMute(), None)
            finally:
                pythoncom.CoUninitialize()
        else:
            import subprocess
            subprocess.Popen(
                ["pactl", "set-sink-mute", "@DEFAULT_SINK@", "toggle"],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
            )
    except Exception as exc:
        print(f"[{GESTURE_NAME}] {exc}")