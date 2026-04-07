#!/usr/bin/env python3
"""
Play one random audio clip from assets/audio.

Usage:
    python scripts/play_random_audio.py
    python scripts/play_random_audio.py --assets-dir assets/audio
    python scripts/play_random_audio.py --dry-run
"""

from __future__ import annotations

import argparse
import os
import platform
import random
import subprocess
import sys
from pathlib import Path

SUPPORTED_EXTENSIONS = {".mp3", ".wav", ".m4a", ".aac", ".flac", ".ogg", ".wma"}


def find_audio_files(assets_dir: Path) -> list[Path]:
    return [
        file
        for file in assets_dir.rglob("*")
        if file.is_file() and file.suffix.lower() in SUPPORTED_EXTENSIONS
    ]


def play_file(path: Path) -> None:
    system = platform.system().lower()

    if system == "windows":
        os.startfile(path)  # type: ignore[attr-defined]
        return

    if system == "darwin":
        subprocess.run(["open", str(path)], check=False)
        return

    subprocess.run(["xdg-open", str(path)], check=False)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Play one random audio clip from assets/audio")
    parser.add_argument(
        "--assets-dir",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "assets" / "audio",
        help="Audio assets directory (default: <skill>/assets/audio)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Only print the selected clip path without opening a player",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    assets_dir = args.assets_dir.resolve()

    if not assets_dir.exists():
        print(f"[ERROR] Audio directory not found: {assets_dir}", file=sys.stderr)
        return 1

    files = find_audio_files(assets_dir)
    if not files:
        print(f"[ERROR] No supported audio files found in: {assets_dir}", file=sys.stderr)
        return 2

    selected = random.choice(files)
    print(f"[INFO] Selected clip: {selected}")

    if args.dry_run:
        return 0

    play_file(selected)
    print("[INFO] Playback triggered via system default player.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
