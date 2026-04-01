"""
gestures/static/iloveyou_2.py
──────────────────────────────
Double-hand 🤟🤟  ILoveYou (both hands)
Action: Take Screenshot

Fix: Key.print_screen is not reliably mapped on all Linux systems.
Uses gnome-screenshot / scrot / spectacle in order of availability,
falling back to the XF86 key only as a last resort.
"""
from __future__ import annotations
import shutil
import subprocess

GESTURE_LABEL = "ILoveYou"
GESTURE_NAME  = "iloveyou_2"


def matches(result) -> bool:
    if not result.gestures or len(result.gestures) != 2:
        return False
    return all(h[0].category_name == GESTURE_LABEL and h[0].score >= 0.70
               for h in result.gestures)


def action() -> None:
    # Try screenshot tools in order of preference
    tools = [
        ["gnome-screenshot"],          # GNOME
        ["spectacle", "--background", "--fullscreen"],  # KDE
        ["scrot"],                     # lightweight / XFCE
        ["import", "-window", "root", f"/tmp/screenshot_{__import__('time').strftime('%Y%m%d_%H%M%S')}.png"],  # ImageMagick
    ]
    for cmd in tools:
        if shutil.which(cmd[0]):
            try:
                subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                return
            except Exception:
                continue

    # Last resort: XF86 Print key via pynput
    try:
        from pynput.keyboard import Key, Controller
        kb = Controller()
        kb.press(Key.print_screen)
        kb.release(Key.print_screen)
    except Exception as exc:
        print(f"[{GESTURE_NAME}] no screenshot tool found: {exc}")