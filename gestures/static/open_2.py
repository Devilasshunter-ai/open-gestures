"""
gestures/static/open_2.py
──────────────────────────
Double-hand 👋👋  Open Palm (both hands)
Action: Open Default Web Browser

Fix: webbrowser.open("https://") was passing a literal "https://"
which some browsers reject. Now opens a blank new window instead.
"""
from __future__ import annotations

GESTURE_LABEL = "Open_Palm"
GESTURE_NAME  = "open_2"


def matches(result) -> bool:
    if not result.gestures or len(result.gestures) != 2:
        return False
    return all(h[0].category_name == GESTURE_LABEL and h[0].score >= 0.70
               for h in result.gestures)


def action() -> None:
    try:
        import subprocess
        # xdg-open launches the system default browser — works on all Linux DEs
        subprocess.Popen(
            ["xdg-open", "https://www.google.com &"],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
    except Exception as exc:
        print(f"[{GESTURE_NAME}] {exc}")