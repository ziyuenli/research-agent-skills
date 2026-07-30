#!/usr/bin/env python3
"""Query colon-delimited fields from a GAMMA-style parameter file."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Sequence


def parse_parameter_file(path: Path) -> dict[str, str]:
    """Return the first value for each colon-delimited parameter key."""
    if not path.is_file():
        raise FileNotFoundError(f"parameter file not found: {path}")

    parameters: dict[str, str] = {}
    for line_number, raw_line in enumerate(
        path.read_text(encoding="utf-8").splitlines(), start=1
    ):
        line = raw_line.strip()
        if not line or line.startswith(("#", ";")):
            continue
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()
        if not key:
            raise ValueError(f"empty parameter key at line {line_number}")
        parameters.setdefault(key, value)
    return parameters


def select_parameters(
    parameters: dict[str, str], keys: Sequence[str], first_present: bool
) -> list[tuple[str, str]]:
    """Select requested parameters in request order."""
    if first_present:
        for key in keys:
            if key in parameters:
                return [(key, parameters[key])]
        raise KeyError(f"none of the requested keys were found: {', '.join(keys)}")

    missing = [key for key in keys if key not in parameters]
    if missing:
        raise KeyError(f"requested keys not found: {', '.join(missing)}")
    return [(key, parameters[key]) for key in keys]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Query colon-delimited fields from a GAMMA parameter file."
    )
    parser.add_argument("file", type=Path, help="GAMMA-style parameter file")
    parser.add_argument("keys", nargs="+", help="parameter keys in lookup order")
    parser.add_argument(
        "--first-present",
        action="store_true",
        help="return only the first requested key present in the file",
    )
    output = parser.add_mutually_exclusive_group()
    output.add_argument(
        "--value-only",
        action="store_true",
        help="print only the first whitespace-delimited token of each value",
    )
    output.add_argument(
        "--json",
        action="store_true",
        help="print selected keys and complete right-hand-side values as JSON",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        parameters = parse_parameter_file(args.file)
        selected = select_parameters(parameters, args.keys, args.first_present)
    except (FileNotFoundError, KeyError, ValueError) as exc:
        raise SystemExit(str(exc)) from exc

    if args.json:
        print(json.dumps(dict(selected), ensure_ascii=False))
    elif args.value_only:
        for _, value in selected:
            if not value:
                raise SystemExit("selected parameter has an empty value")
            print(value.split()[0])
    else:
        for key, value in selected:
            print(f"{key}\t{value}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
