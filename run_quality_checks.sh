#!/usr/bin/env bash

set -u

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="$ROOT_DIR/backend"
VENV_PYTEST="$BACKEND_DIR/.venv/bin/pytest"
VENV_FLAKE8="$BACKEND_DIR/.venv/bin/flake8"
VENV_COV="$BACKEND_DIR/.venv/bin/coverage"

if [[ ! -d "$BACKEND_DIR" ]]; then
  echo "No se encontro el directorio backend en: $BACKEND_DIR"
  exit 1
fi

if [[ -x "$VENV_PYTEST" ]]; then
  PYTEST_CMD="$VENV_PYTEST"
else
  PYTEST_CMD="${PYTEST_CMD:-pytest}"
fi

if [[ -x "$VENV_FLAKE8" ]]; then
  FLAKE8_CMD="$VENV_FLAKE8"
else
  FLAKE8_CMD="${FLAKE8_CMD:-flake8}"
fi

if ! command -v "$PYTEST_CMD" >/dev/null 2>&1; then
  echo "No se encontro pytest. Instala dependencias con:"
  echo "  pip install -r backend/requirements-dev.txt"
  exit 1
fi

if ! command -v "$FLAKE8_CMD" >/dev/null 2>&1; then
  echo "No se encontro flake8. Instala dependencias con:"
  echo "  pip install -r backend/requirements-dev.txt"
  exit 1
fi

echo "Usando pytest: $PYTEST_CMD"
echo "Usando flake8: $FLAKE8_CMD"
echo "Directorio de trabajo: $BACKEND_DIR"
echo

pushd "$BACKEND_DIR" >/dev/null || exit 1

echo "==> Ejecutando tests unitarios con cobertura (pytest + pytest-cov)"
"$PYTEST_CMD" -rs --cov=app --cov-report=term-missing
TEST_EXIT=$?
echo

echo "==> Linter (flake8)"
"$FLAKE8_CMD" --format='%(path)s:%(row)d:%(col)d: %(code)s %(text)s' app tests
LINT_EXIT=$?
echo

popd >/dev/null || exit 1

echo "Resumen:"
if [[ $TEST_EXIT -eq 0 ]]; then
  echo "  [OK] Tests unitarios"
else
  echo "  [FAIL:$TEST_EXIT] Tests unitarios"
fi

if [[ $LINT_EXIT -eq 0 ]]; then
  echo "  [OK] Linter (sin errores)"
else
  echo "  [FAIL:$LINT_EXIT] Linter (revisa errores arriba)"
fi

if [[ $TEST_EXIT -ne 0 || $LINT_EXIT -ne 0 ]]; then
  echo
  echo "Resultado final: NO CUMPLE"
  exit 1
fi

echo
echo "Resultado final: CUMPLE"
