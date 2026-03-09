import json
from pathlib import Path

from app.store import ScoreStore


def test_store_creates_empty_file_on_init(tmp_path: Path) -> None:
    file_path = tmp_path / "scores.json"

    ScoreStore(file_path)

    assert file_path.exists()
    assert json.loads(file_path.read_text(encoding="utf-8")) == {}


def test_top_scores_returns_descending_scores_with_limit(tmp_path: Path) -> None:
    store = ScoreStore(tmp_path / "scores.json")

    store.save_score("snake", "Alice", 10)
    store.save_score("snake", "Bob", 35)
    store.save_score("snake", "Carol", 22)

    scores = store.top_scores("snake", limit=2)

    assert [item["player_name"] for item in scores] == ["Bob", "Carol"]
    assert [item["score"] for item in scores] == [35, 22]


def test_non_dict_storage_is_handled_as_empty(tmp_path: Path) -> None:
    file_path = tmp_path / "scores.json"
    file_path.write_text("[]", encoding="utf-8")
    store = ScoreStore(file_path)

    assert store.top_scores("snake") == []
