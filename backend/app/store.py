from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from threading import Lock
from typing import Any


class ScoreStore:
    """Small JSON-backed score store for demo purposes."""

    def __init__(self, file_path: Path) -> None:
        self.file_path = file_path
        self._lock = Lock()
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.file_path.exists():
            self._write_raw({})

    def _read_raw(self) -> dict[str, list[dict[str, Any]]]:
        with self.file_path.open("r", encoding="utf-8") as fh:
            data = json.load(fh)
        if not isinstance(data, dict):
            return {}
        return data

    def _write_raw(self, data: dict[str, list[dict[str, Any]]]) -> None:
        with self.file_path.open("w", encoding="utf-8") as fh:
            json.dump(data, fh, ensure_ascii=True, indent=2)

    def save_score(self, game_id: str, player_name: str, score: int) -> dict[str, Any]:
        entry = {
            "player_name": player_name,
            "score": score,
            "timestamp": datetime.utcnow().isoformat(timespec="seconds") + "Z",
        }
        with self._lock:
            data = self._read_raw()
            data.setdefault(game_id, []).append(entry)
            self._write_raw(data)
        return entry

    def top_scores(self, game_id: str, limit: int = 10) -> list[dict[str, Any]]:
        with self._lock:
            entries = list(self._read_raw().get(game_id, []))

        entries.sort(
            key=lambda item: (
                -int(item.get("score", 0)),
                item.get("timestamp", ""),
            )
        )
        return entries[:limit]
