from __future__ import annotations
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

GESTURE_LABEL = "Thumb_Down"
GESTURE_NAME  = "thumb_down_1"

def matches(result) -> bool:
    if not result.gestures or len(result.gestures) != 1:
        return False
    top = result.gestures[0][0]
    return top.category_name == GESTURE_LABEL and top.score >= 0.70

def action() -> None:
    try:
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        current_vol = volume.GetMasterVolumeLevelScalar()
        # Decrease volume by 5% (0.05 scalar)
        volume.SetMasterVolumeLevelScalar(max(0.0, current_vol - 0.05), None)
    except Exception as exc:
        print(f"[{GESTURE_NAME}] {exc}")