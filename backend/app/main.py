from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

from .store import ScoreStore

app = FastAPI(title="Falken Games API", version="1.0.0")
FRONTEND_DIST = Path(__file__).resolve().parents[2] / "frontend" / "dist"

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

GAMES = [
    {
        "id": "snake",
        "name": "Snake",
        "description": "Mueve la serpiente, come comida y evita chocarte.",
        "controls": "Flechas",
    },
    {
        "id": "pong",
        "name": "Pong Solo",
        "description": "Manten la pelota en juego el mayor tiempo posible.",
        "controls": "Flechas izquierda/derecha",
    },
    {
        "id": "memory",
        "name": "Memoria",
        "description": "Encuentra todas las parejas con el menor numero de intentos.",
        "controls": "Click/Tap",
    },
    {
        "id": "guess-number",
        "name": "Adivina el Numero",
        "description": "Adivina el numero secreto entre 1 y 100.",
        "controls": "Teclado",
    },
    {
        "id": "reflex",
        "name": "Reflejos",
        "description": "Haz click en el momento exacto para medir tu reaccion.",
        "controls": "Click/Tap",
    },
    {
        "id": "sharp-eye",
        "name": "Agudeza Visual",
        "description": "Detecta el cuadro de color distinto antes de que suba la dificultad.",
        "controls": "Click/Tap",
    },
]

GAME_IDS = {game["id"] for game in GAMES}
STORE = ScoreStore(Path(__file__).parent / "data" / "scores.json")


class ScoreIn(BaseModel):
    game_id: str
    player_name: str = Field(min_length=1, max_length=24)
    score: int = Field(ge=0, le=1000000)


class ScoreOut(BaseModel):
    player_name: str
    score: int
    timestamp: str


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/games")
def list_games() -> list[dict[str, str]]:
    return GAMES


@app.get("/api/scores/{game_id}", response_model=list[ScoreOut])
def get_scores(game_id: str, limit: int = Query(default=10, ge=1, le=50)) -> list[dict[str, str | int]]:
    if game_id not in GAME_IDS:
        raise HTTPException(status_code=404, detail="Juego no encontrado")
    return STORE.top_scores(game_id, limit=limit)


@app.post("/api/scores", response_model=ScoreOut, status_code=201)
def save_score(payload: ScoreIn) -> dict[str, str | int]:
    if payload.game_id not in GAME_IDS:
        raise HTTPException(status_code=404, detail="Juego no encontrado")
    player_name = payload.player_name.strip()
    if not player_name:
        raise HTTPException(status_code=422, detail="Nombre de jugador invalido")
    return STORE.save_score(payload.game_id, player_name, payload.score)


def _resolve_frontend_path(request_path: str) -> Path | None:
    if not FRONTEND_DIST.exists():
        return None

    normalized_path = request_path.strip("/")
    if not normalized_path:
        index_file = FRONTEND_DIST / "index.html"
        return index_file if index_file.is_file() else None

    candidate = (FRONTEND_DIST / normalized_path).resolve()
    try:
        candidate.relative_to(FRONTEND_DIST.resolve())
    except ValueError:
        return None

    if candidate.is_file():
        return candidate

    index_file = FRONTEND_DIST / "index.html"
    return index_file if index_file.is_file() else None


@app.get("/", include_in_schema=False)
def serve_frontend_index() -> FileResponse:
    frontend_file = _resolve_frontend_path("")
    if frontend_file is None:
        raise HTTPException(status_code=404, detail="Frontend no disponible")
    return FileResponse(frontend_file)


@app.get("/{full_path:path}", include_in_schema=False)
def serve_frontend(full_path: str) -> FileResponse:
    if full_path == "api" or full_path.startswith("api/"):
        raise HTTPException(status_code=404, detail="Not Found")

    frontend_file = _resolve_frontend_path(full_path)
    if frontend_file is None:
        raise HTTPException(status_code=404, detail="Frontend no disponible")
    return FileResponse(frontend_file)
