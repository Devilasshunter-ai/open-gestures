"""
gestures/motion/swipe_right_1.py  —  Swipe right with 1 hand(s)
Detection is handled by core/SwipeTracker — this module only declares
the gesture name so the router and cooldown system can reference it.
matches() is never called by the router for swipe gestures;
SwipeTracker.detect() returns the gesture name directly.
"""
from __future__ import annotations

GESTURE_NAME = "swipe_right_1"


def matches(result) -> bool:
    # Swipe gestures are NOT detected via GestureRecognizer results.
    # SwipeTracker.detect() handles detection via HandLandmarker.
    # The router routes swipe names returned by swipe_tracker.detect()
    # directly — this matches() is intentionally never called.
    return False