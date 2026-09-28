"""Build the only commands this engine is allowed to run."""

from __future__ import annotations

from pathlib import Path

from hf import PIN
from hf.guard import GuardError, assert_hyperframes

RENDER_QUALITY = "standard"
RENDER_WORKERS = "1"


def doctor_cmd() -> list[str]:
    cmd = ["npx", "--yes", PIN, "doctor"]
    assert_hyperframes(cmd)
    return cmd


def check_cmd(composition: Path) -> list[str]:
    cmd = ["npx", "--yes", PIN, "check", str(composition)]
    assert_hyperframes(cmd)
    return cmd


def render_cmd(composition: Path, mp4: Path, fps: int) -> list[str]:
    if fps < 1 or fps > 60:
        raise GuardError("fps must be between 1 and 60")
    cmd = [
        "npx",
        "--yes",
        PIN,
        "render",
        str(composition),
        "--output",
        str(mp4),
        "--fps",
        str(fps),
        "--quality",
        RENDER_QUALITY,
        "--workers",
        RENDER_WORKERS,
        "--low-memory-mode",
    ]
    assert_hyperframes(cmd)
    return cmd


def poster_cmd(mp4: Path, jpg: Path, at: float) -> list[str]:
    if at < 0:
        raise GuardError("poster timestamp must be >= 0")
    return [
        "ffmpeg",
        "-y",
        "-ss",
        f"{at:.3f}",
        "-i",
        str(mp4),
        "-frames:v",
        "1",
        "-q:v",
        "2",
        "-update",
        "1",
        str(jpg),
    ]
