from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from .store import ScoreStore

app = FastAPI(title="Falken Games API", version="1.0.0")

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
