#!/usr/bin/env python3
"""Inventory local Codex sessions without emitting transcript content."""

from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path


def count_messages(rollout_path: Path) -> tuple[int, int]:
    user_count = 0
    assistant_count = 0
    if not rollout_path.is_file():
        return user_count, assistant_count

    with rollout_path.open(encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, start=1):
            try:
                item = json.loads(line)
            except json.JSONDecodeError as error:
                raise ValueError(
                    f"{rollout_path}:{line_number}: invalid JSON"
                ) from error

            if item.get("type") != "response_item":
                continue
            payload = item.get("payload", {})
            if payload.get("type") != "message":
                continue
            role = payload.get("role")
            if role == "user":
                user_count += 1
            elif role == "assistant":
                assistant_count += 1

    return user_count, assistant_count


def inventory(database: Path) -> list[dict[str, object]]:
    if not database.is_file():
        raise FileNotFoundError(database)

    connection = sqlite3.connect(f"file:{database}?mode=ro", uri=True)
    try:
        rows = connection.execute(
            """
            SELECT id, rollout_path, created_at, updated_at, cwd, title, archived
            FROM threads
            ORDER BY created_at, id
            """
        ).fetchall()
    finally:
        connection.close()

    records: list[dict[str, object]] = []
    for thread_id, rollout, created, updated, cwd, title, archived in rows:
        rollout_path = Path(rollout)
        user_count, assistant_count = count_messages(rollout_path)
        records.append(
            {
                "id": thread_id,
                "rollout_exists": rollout_path.is_file(),
                "created_at_epoch": created,
                "updated_at_epoch": updated,
                "cwd": cwd,
                "title": title,
                "archived": bool(archived),
                "user_messages": user_count,
                "assistant_messages": assistant_count,
            }
        )
    return records


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Inventory local Codex threads without transcript text."
    )
    parser.add_argument("database", type=Path, help="Path to the Codex state SQLite file")
    parser.add_argument(
        "--omit-title",
        action="store_true",
        help="Omit titles when the inventory will be shared.",
    )
    arguments = parser.parse_args()

    records = inventory(arguments.database)
    if arguments.omit_title:
        for record in records:
            record.pop("title", None)

    print(json.dumps({"count": len(records), "threads": records}, indent=2))


if __name__ == "__main__":
    main()

