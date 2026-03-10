#!/usr/bin/env bash

set -u

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="$ROOT_DIR/backend"
VENV_PYTHON="$BACKEND_DIR/.venv/bin/python"

HOST="${HOST:-127.0.0.1}"
PORT="${PORT:-8000}"
RELOAD="${RELOAD:-true}"

if [[ ! -d "$BACKEND_DIR" ]]; then
  echo "No se encontro el directorio backend en: $BACKEND_DIR"
  exit 1
fi

if [[ -x "$VENV_PYTHON" ]]; then
  PYTHON_BIN="$VENV_PYTHON"
else
  PYTHON_BIN="${PYTHON_BIN:-python3}"
fi

if ! command -v "$PYTHON_BIN" >/dev/null 2>&1; then
  echo "No se encontro el interprete de Python: $PYTHON_BIN"
  exit 1
fi

if [[ "$RELOAD" == "true" ]]; then
  RELOAD_FLAG="--reload"
else
  RELOAD_FLAG=""
fi

echo "Levantando API en http://$HOST:$PORT"
echo "Usando Python: $PYTHON_BIN"
echo

exec "$PYTHON_BIN" -m uvicorn app.main:app --app-dir "$BACKEND_DIR" --host "$HOST" --port "$PORT" $RELOAD_FLAG
