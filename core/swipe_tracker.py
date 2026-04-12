"""
core/swipe_tracker.py
─────────────────────
Runs MediaPipe HandLandmarker in LIVE_STREAM mode on a shared camera frame,
tracks wrist position (landmark 0) per hand across a rolling frame window,
and emits swipe directions when displacement + speed thresholds are met.

Swipe gestures produced:
    swipe_left_1  / swipe_right_1  / swipe_up_1  / swipe_down_1   (single hand)
    swipe_left_2  / swipe_right_2  / swipe_up_2  / swipe_down_2   (both hands, same direction)

Thresholds are read from data/config.json:
    swipe.frame_limit            — max frames the motion window spans
    swipe.displacement_threshold — min normalized distance (0–1) to count as a swipe
"""
from __future__ import annotations

import threading
from collections import deque
from pathlib import Path
from typing import Optional

import mediapipe as mp
from mediapipe.tasks import python as mp_python
from mediapipe.tasks.python import vision as mp_vision
from mediapipe.tasks.python.vision.core.vision_task_running_mode import VisionTaskRunningMode

from core.config import get

LANDMARK_MODEL_PATH = Path(__file__).parent.parent / "models" / "hand_landmarker.task"

# Wrist is landmark index 0 in MediaPipe's 21-point hand model
_WRIST = 0


# ── Per-hand position history ──────────────────────────────────────────────

class _HandHistory:
    """
    Stores a rolling window of (x, y) wrist positions for one hand.
    x and y are normalized [0.0, 1.0] — no pixel values used.
    """

    def __init__(self, maxlen: int) -> None:
        self._positions: deque[tuple[float, float]] = deque(maxlen=maxlen)

    def push(self, x: float, y: float) -> None:
        self._positions.append((x, y))

    def clear(self) -> None:
        self._positions.clear()

    def displacement(self) -> tuple[float, float]:
        """
        Returns (dx, dy) from oldest to newest position in the window.
        Positive dx = moved right, positive dy = moved down (y=0 is top).
        Returns (0, 0) if fewer than 2 positions recorded.
        """
        if len(self._positions) < 2:
            return 0.0, 0.0
        x0, y0 = self._positions[0]
        x1, y1 = self._positions[-1]
        return x1 - x0, y1 - y0

    def __len__(self) -> int:
        return len(self._positions)


# ── Thread-safe landmark result slot ──────────────────────────────────────

class _LandmarkSlot:
    def __init__(self) -> None:
        self._lock   = threading.Lock()
        self._result = None

    def put(self, result) -> None:
        with self._lock:
            self._result = result

    def get(self):
        with self._lock:
            return self._result


# ── SwipeTracker ───────────────────────────────────────────────────────────

class SwipeTracker:
    """
    Maintains hand position histories and detects swipe gestures.
    Call feed(mp_image, timestamp_ms) each frame from the main loop.
    Call detect() after feed() to get the swipe gesture name, or None.
    """

    def __init__(self) -> None:
        if not LANDMARK_MODEL_PATH.exists():
            raise FileNotFoundError(
                f"Hand landmarker model not found: {LANDMARK_MODEL_PATH}\n"
                "Download with:\n"
                "  wget https://storage.googleapis.com/mediapipe-models/"
                "hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task"
                " -O models/hand_landmarker.task"
            )

        self._slot     = _LandmarkSlot()
        self._landmarker = self._build_landmarker()

        # Two slots — index 0 and 1 for up to 2 hands
        frame_limit    = get("swipe", "frame_limit", default=20)
        self._histories: list[_HandHistory] = [
            _HandHistory(frame_limit),
            _HandHistory(frame_limit),
        ]

    def _build_landmarker(self) -> mp_vision.HandLandmarker:
        def _on_result(result, _image, _ts) -> None:
            self._slot.put(result)

        options = mp_vision.HandLandmarkerOptions(
            base_options=mp_python.BaseOptions(
                model_asset_path=str(LANDMARK_MODEL_PATH),
            ),
            running_mode=VisionTaskRunningMode.LIVE_STREAM,
            num_hands=2,
            min_hand_detection_confidence=0.5,
            min_hand_presence_confidence=0.5,
            min_tracking_confidence=0.5,
            result_callback=_on_result,
        )
        return mp_vision.HandLandmarker.create_from_options(options)

    def feed(self, mp_image: mp.Image, timestamp_ms: int) -> None:
        """Submit a frame for async landmark detection."""
        self._landmarker.detect_async(mp_image, timestamp_ms)

    def detect(self) -> Optional[str]:
        """
        Read latest landmark result, update position histories,
        and return a swipe gesture name if thresholds are met.
        Clears the history for any hand that triggered a swipe.
        """
        result = self._slot.get()
        if result is None or not result.hand_landmarks:
            # No hands — clear all histories so stale positions don't linger
            for h in self._histories:
                h.clear()
            return None

        threshold = get("swipe", "displacement_threshold", default=0.1)
        num_hands = len(result.hand_landmarks)

        # Update position histories for each detected hand
        for i, landmarks in enumerate(result.hand_landmarks):
            if i >= len(self._histories):
                break
            wrist = landmarks[_WRIST]
            self._histories[i].push(wrist.x, wrist.y)

        # Clear histories for hands that disappeared
        for i in range(num_hands, len(self._histories)):
            self._histories[i].clear()

        # ── Single-hand swipe ──────────────────────────────────────────────
        if num_hands == 1:
            dx, dy = self._histories[0].displacement()
            direction = _classify_swipe(dx, dy, threshold)
            if direction:
                self._histories[0].clear()
                print(f"Swipe detected: swipe_{direction}_1")
                return f"swipe_{direction}_1"

        # ── Double-hand swipe (both hands same direction) ──────────────────
        elif num_hands == 2:
            dx0, dy0 = self._histories[0].displacement()
            dx1, dy1 = self._histories[1].displacement()
            dir0 = _classify_swipe(dx0, dy0, threshold)
            dir1 = _classify_swipe(dx1, dy1, threshold)
            if dir0 and dir0 == dir1:
                self._histories[0].clear()
                self._histories[1].clear()
                print(f"Swipe detected: swipe_{dir0}_2")
                return f"swipe_{dir0}_2"

        return None

    def close(self) -> None:
        """Shut down the landmarker cleanly."""
        self._landmarker.close()


# ── Direction classifier ───────────────────────────────────────────────────

def _classify_swipe(
    dx: float, dy: float, threshold: float
) -> Optional[str]:
    """
    Returns 'left', 'right', 'up', or 'down' if the dominant axis
    displacement exceeds threshold. Returns None if below threshold.

    Note: y increases downward in normalized image coords (0=top, 1=bottom),
    so a negative dy means the hand moved UP on screen.
    """
    abs_dx, abs_dy = abs(dx), abs(dy)

    # Must exceed threshold on at least one axis
    if max(abs_dx, abs_dy) < threshold:
        return None

    # Dominant axis wins
    if abs_dx >= abs_dy:
        return "right" if dx > 0 else "left"
    else:
        return "down" if dy > 0 else "up"