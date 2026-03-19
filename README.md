# Falken Games

App web con backend en Python (FastAPI) y frontend en Vue 3. Incluye 6 juegos de un jugador, optimizada para escritorio y movil.

1. Snake
2. Pong Solo
3. Memoria
4. Adivina el Numero
5. Reflejos
6. Agudeza Visual

## Requisitos

- Python 3.10+
- Node.js 16+

## Ejecutar el proyecto completo (recomendado)

Lanza backend y frontend en paralelo con un solo comando desde la raiz:

```bash
./run_project.sh
```

El script crea las dependencias de frontend si no existen y detiene ambos procesos al pulsar Ctrl+C.

Variables de entorno opcionales:

| Variable   | Default      | Descripcion                  |
|------------|--------------|------------------------------|
| `HOST`     | `127.0.0.1`  | Host donde escucha la API    |
| `API_PORT` | `8000`       | Puerto de la API             |
| `RELOAD`   | `true`       | Hot-reload de uvicorn        |

## Ejecutar por separado

### Backend

```bash
./run_api.sh
```

O manualmente:

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Abre [http://localhost:5173](http://localhost:5173).

El frontend consume la API bajo `/api` mediante proxy de Vite apuntando a `http://127.0.0.1:8000`.

## Calidad backend (tests + linter)

Desde la raiz del proyecto:

```bash
./run_quality_checks.sh
```

O manualmente:

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
pytest
flake8 app tests
```

## Calidad frontend

```bash
cd frontend
npm run build
```

## Endpoints

- `GET /api/health`
- `GET /api/games`
- `GET /api/scores/{game_id}?limit=10`
- `POST /api/scores`

IDs de juego validos: `snake`, `pong`, `memory`, `guess-number`, `reflex`, `sharp-eye`.

Payload para score:

```json
{
  "game_id": "snake",
  "player_name": "Player1",
  "score": 120
}
```

## Notas de diseno

- La interfaz es responsive y jugable desde navegador movil.
- Snake y Pong incluyen controles tactiles en pantalla para movil.
- Agudeza Visual escala la dificultad progresivamente en 8 rondas (celdas y contraste de color).
