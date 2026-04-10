#!/usr/bin/env python3
"""
Play a specific or random audio clip from assets/audio.

Usage:
    python scripts/play_audio.py
    python scripts/play_audio.py --assets-dir assets/audio
    python scripts/play_audio.py --keyword "无糖可乐"  # Plays the first audio matching the keyword
    python scripts/play_audio.py --dry-run
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


def find_audio_files(assets_dir: Path, keyword: str = "") -> list[Path]:
    files = [
        file
        for file in assets_dir.rglob("*")
        if file.is_file() and file.suffix.lower() in SUPPORTED_EXTENSIONS
    ]
    if keyword:
        keyword = keyword.lower()
        files = [f for f in files if keyword in f.name.lower()]
    return files


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
    parser = argparse.ArgumentParser(description="Play a specific or random audio clip from assets/audio")
    parser.add_argument(
        "--assets-dir",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "assets" / "audio",
        help="Audio assets directory (default: <skill>/assets/audio)",
    )
    parser.add_argument(
        "--keyword",
        type=str,
        default="",
        help="Optional keyword to match a specific audio file by name",
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

    files = find_audio_files(assets_dir, args.keyword)
    if not files:
        if args.keyword:
            print(f"[ERROR] No supported audio files found in {assets_dir} matching keyword: {args.keyword}", file=sys.stderr)
        else:
            print(f"[ERROR] No supported audio files found in: {assets_dir}", file=sys.stderr)
        return 2

    # If keyword is given, pick the first match (or random among matches). Let's pick random among matches.
    selected = random.choice(files)
    print(f"[INFO] Selected clip: {selected}")

    if args.dry_run:
        return 0

    play_file(selected)
    print("[INFO] Playback triggered via system default player.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
