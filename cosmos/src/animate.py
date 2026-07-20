"""
Animation loop for Cosmos terminal visualizer.
Handles smooth real-time and time-lapse playback.
"""

import os
import sys
import time
import shutil
from datetime import datetime, timedelta, timezone

from .renderer import full_render, render_frame, CANVAS_W, CANVAS_H

CLEAR = "\033[2J\033[H"


def terminal_size() -> tuple[int, int]:
    size = shutil.get_terminal_size(fallback=(CANVAS_W + 4, CANVAS_H + 20))
    return size.columns, size.lines


def run_animation(
    fps: float = 10.0,
    time_scale: float = 1.0,
    start_dt: datetime | None = None,
    view_au: float = 32.0,
    frames: int | None = None,
    w: int = CANVAS_W,
    h: int = CANVAS_H,
) -> None:
    """
    Animate the solar system in the terminal.

    fps        : frames per second (visual)
    time_scale : 1.0 = real time; 86400.0 = 1 day per second
    start_dt   : starting datetime (default now)
    view_au    : AU radius visible
    frames     : number of frames before exit (None = run forever)
    """
    if start_dt is None:
        start_dt = datetime.now(timezone.utc)

    dt = start_dt
    frame_dt = timedelta(seconds=time_scale / fps)
    sleep_sec = 1.0 / fps
    count = 0

    try:
        while frames is None or count < frames:
            t0 = time.monotonic()

            render = full_render(dt, view_au=view_au, w=w, h=h)
            sys.stdout.write(CLEAR + render + "\n")
            sys.stdout.flush()

            elapsed = time.monotonic() - t0
            sleep = max(0.0, sleep_sec - elapsed)
            time.sleep(sleep)

            dt += frame_dt
            count += 1

    except KeyboardInterrupt:
        print("\n\n  \033[1;97mCosmos: animation stopped.\033[0m\n")
