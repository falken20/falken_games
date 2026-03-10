# Guia rapida: arrancar y probar Falken Games

## 1) Setup inicial (solo una vez)

Desde la raiz del proyecto:

```bash
cd /Users/u102105/workspace/python/falken_games
python3 -m venv backend/.venv
source backend/.venv/bin/activate
pip install -r backend/requirements-dev.txt
cd frontend && npm install && cd ..
```

## 2) Arranque diario (minimo de comandos)

Abre 2 terminales en la raiz del proyecto.

Terminal 1 (API):

```bash
./run_api.sh
```

Terminal 2 (Frontend):

```bash
cd frontend && npm run dev
```

## 3) Probar que funciona

En otra terminal:

```bash
curl http://localhost:8000/api/health
```

Debe responder:

```json
{"status":"ok"}
```

Luego abre la app en:

- http://localhost:5173

## 4) Validacion automatica (tests + linter)

Desde la raiz:

```bash
./run_quality_checks.sh
```
