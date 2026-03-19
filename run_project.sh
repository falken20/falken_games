#!/usr/bin/env bash

set -u

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="$ROOT_DIR/backend"
FRONTEND_DIR="$ROOT_DIR/frontend"
VENV_PYTHON="$BACKEND_DIR/.venv/bin/python"

HOST="${HOST:-127.0.0.1}"
API_PORT="${API_PORT:-8000}"
RELOAD="${RELOAD:-true}"

cleanup() {
  echo
  echo "Deteniendo procesos..."
  if [[ -n "${API_PID:-}" ]] && kill -0 "$API_PID" 2>/dev/null; then
    kill "$API_PID" 2>/dev/null
    wait "$API_PID" 2>/dev/null
  fi
  if [[ -n "${FRONT_PID:-}" ]] && kill -0 "$FRONT_PID" 2>/dev/null; then
    kill "$FRONT_PID" 2>/dev/null
    wait "$FRONT_PID" 2>/dev/null
  fi
  echo "Proyecto detenido."
}
trap cleanup EXIT INT TERM

# --- Validaciones ---

if [[ ! -d "$BACKEND_DIR" ]]; then
  echo "No se encontro el directorio backend en: $BACKEND_DIR"
  exit 1
fi

if [[ ! -d "$FRONTEND_DIR" ]]; then
  echo "No se encontro el directorio frontend en: $FRONTEND_DIR"
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

if ! command -v npm >/dev/null 2>&1; then
  echo "No se encontro npm. Instala Node.js 16+ para continuar."
  exit 1
fi

# --- Setup frontend si falta node_modules ---

if [[ ! -d "$FRONTEND_DIR/node_modules" ]]; then
  echo "Instalando dependencias de frontend..."
  (cd "$FRONTEND_DIR" && npm install) || { echo "Fallo npm install"; exit 1; }
  echo
fi

# --- Backend ---

if [[ "$RELOAD" == "true" ]]; then
  RELOAD_FLAG="--reload"
else
  RELOAD_FLAG=""
fi

echo "==> Levantando API en http://$HOST:$API_PORT"
"$PYTHON_BIN" -m uvicorn app.main:app \
  --app-dir "$BACKEND_DIR" \
  --host "$HOST" \
  --port "$API_PORT" \
  $RELOAD_FLAG &
API_PID=$!

# Esperar brevemente a que el backend arranque
sleep 2
if ! kill -0 "$API_PID" 2>/dev/null; then
  echo "Error: el backend no pudo arrancar."
  exit 1
fi

# --- Frontend ---

echo "==> Levantando frontend en http://localhost:5173"
(cd "$FRONTEND_DIR" && npm run dev) &
FRONT_PID=$!

echo
echo "Proyecto listo:"
echo "  API:      http://$HOST:$API_PORT"
echo "  Frontend: http://localhost:5173"
echo
echo "Pulsa Ctrl+C para detener ambos servicios."

wait
