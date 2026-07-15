#!/usr/bin/env python3
"""Copy a finalized DOCX to a collision-safe, timestamped deliverable name."""

from __future__ import annotations

import argparse
import shutil
from datetime import datetime
from pathlib import Path
from zipfile import BadZipFile, ZipFile


def valid_timestamp(value: str) -> str:
    try:
        datetime.strptime(value, "%Y-%m-%d_%H%M%S")
    except ValueError as exc:
        raise argparse.ArgumentTypeError(
            "timestamp must use YYYY-MM-DD_HHMMSS"
        ) from exc
    return value


def verify_docx(path: Path) -> None:
    if path.suffix.lower() != ".docx":
        raise ValueError(f"input must be a .docx file: {path}")
    if not path.is_file():
        raise FileNotFoundError(f"input file not found: {path}")
    try:
        with ZipFile(path) as archive:
            names = set(archive.namelist())
            if "[Content_Types].xml" not in names or "word/document.xml" not in names:
                raise ValueError(f"input is not a valid Word DOCX package: {path}")
            corrupt_member = archive.testzip()
            if corrupt_member:
                raise ValueError(f"corrupt DOCX member: {corrupt_member}")
    except BadZipFile as exc:
        raise ValueError(f"input is not a valid DOCX ZIP package: {path}") from exc


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Copy a finalized DOCX with a _YYYY-MM-DD_HHMMSS suffix."
    )
    parser.add_argument("input", type=Path, help="finalized working DOCX")
    parser.add_argument(
        "--output-dir",
        type=Path,
        help="destination directory (default: input directory)",
    )
    parser.add_argument(
        "--timestamp",
        type=valid_timestamp,
        help="fixed timestamp for reproducible output (default: local current time)",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    source = args.input.expanduser().resolve()
    verify_docx(source)

    timestamp = args.timestamp or datetime.now().strftime("%Y-%m-%d_%H%M%S")
    destination_dir = (
        args.output_dir.expanduser().resolve() if args.output_dir else source.parent
    )
    destination_dir.mkdir(parents=True, exist_ok=True)
    destination = destination_dir / f"{source.stem}_{timestamp}.docx"

    if destination.exists():
        raise FileExistsError(f"refusing to overwrite existing file: {destination}")

    shutil.copy2(source, destination)
    verify_docx(destination)
    print(destination)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
