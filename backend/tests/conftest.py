import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


@pytest.fixture
def score_store(tmp_path: Path):
    from app.store import ScoreStore

    return ScoreStore(tmp_path / "scores.json")


@pytest.fixture
def client(score_store, monkeypatch: pytest.MonkeyPatch):
    pytest.importorskip("pydantic")
    from fastapi.testclient import TestClient
    import app.main as main_module

    monkeypatch.setattr(main_module, "STORE", score_store)
    return TestClient(main_module.app)
