# Falken Games

App web con backend en Python (FastAPI) y frontend en Vue 3. Incluye 5 juegos sencillos de un jugador:

1. Snake
2. Pong Solo
3. Memoria
4. Adivina el Numero
5. Reflejos

## Requisitos

- Python 3.10+
- Node.js 16+

## Ejecutar backend

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

## Ejecutar frontend

```bash
cd frontend
npm install
npm run dev
```

Abre [http://localhost:5173](http://localhost:5173).

El frontend consume la API bajo `/api` mediante proxy de Vite.

## Endpoints

- `GET /api/health`
- `GET /api/games`
- `GET /api/scores/{game_id}?limit=10`
- `POST /api/scores`

Payload para score:

```json
{
  "game_id": "snake",
  "player_name": "Player1",
  "score": 120
}
```
