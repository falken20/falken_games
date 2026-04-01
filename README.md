<div align="center">

# 🎮 Falken Games

Plataforma de juegos web fullstack con backend en Python (FastAPI) y frontend en Vue 3. 6 juegos de un jugador optimizados para escritorio y móvil.

<p>
	<img src="https://img.shields.io/github/languages/count/falken20/falken_games" alt="GitHub language count"/>&nbsp;
	<img src="https://img.shields.io/github/languages/top/falken20/falken_games" alt="GitHub top language"/>&nbsp;
	<img src="https://img.shields.io/github/license/falken20/falken_games" alt="GitHub license"/>&nbsp;
	<img src="https://img.shields.io/static/v1?label=python&message=3.10%2B&color=blue&logo=python&logoColor=white" alt="Python version"/>&nbsp;
	<img src="https://img.shields.io/static/v1?label=node&message=16%2B&color=green&logo=node.js&logoColor=white" alt="Node version"/>&nbsp;
	<img src="https://img.shields.io/badge/release-1.0.0-blue" alt="Release version"/>&nbsp;
	<img src="https://img.shields.io/github/actions/workflow/status/falken20/falken_games/quality.yml?branch=master&label=ci" alt="CI status"/>&nbsp;
	<img src="https://img.shields.io/badge/coverage-95%25-green" alt="Test coverage"/>
</p>

</div>

## Overview

Falken Games es una aplicación web fullstack que combina un robusto backend con FastAPI con un frontend interactivo en Vue 3. La aplicación incluye algoritmos de juego optimizados, gestión de puntuaciones persistente, y una interfaz responsive que se adapta perfectamente a escritorio y dispositivos móviles.

### Juegos incluidos

1. **Snake** - Clásico juego de píxeles con controles táctiles en móvil
2. **Pong Solo** - Modo individual contra IA con físicas realistas
3. **Memoria** - Juego de concentración con dificultad escalable
4. **Adivina el Número** - Juego lógico con feedback dinámico
5. **Reflejos** - Desafío de velocidad de reacción
6. **Agudeza Visual** - 8 rondas progresivas con contraste variable

## Features

- 6 juegos independientes de un jugador
- Sistema de puntuaciones persistente con historial
- API RESTful con endpoints documentados
- Interfaz responsive para escritorio y móvil
- Controles táctiles optimizados para smartphones
- Dificultad progresiva en juegos seleccionados
- Gestión de estado frontend con Vue 3 Composition API
- Ejecución paralela simplificada con scripts auxiliares

## Tech Stack

- **Backend:** Python 3.10+, FastAPI, Uvicorn
- **Frontend:** Vue 3, Vite, CSS3 nativo
- **Base de datos:** JSON persistido en local
- **Herramientas:** pytest (tests), flake8 (linting)
- **Deployment:** Scripts bash para desarrollo local

## Quick Start

### 1. Requisitos previos

- Python `3.10+`
- Node.js `16+`
- `npm`

### 2. Clonar el repositorio

```bash
git clone https://github.com/falken20/falken_games.git
cd falken_games
```

### 3. Opción A: Ejecutar el proyecto completo (recomendado)

Lanza backend y frontend en paralelo con un único comando desde la raíz:

```bash
./run_project.sh
```

El script:
- Crea las dependencias de frontend si no existen
- Inicia backend en `http://127.0.0.1:8000`
- Inicia frontend en `http://localhost:5173`
- Detiene ambos procesos al pulsar `Ctrl+C`

### 3. Opción B: Ejecutar por separado

#### Backend

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

#### Frontend

```bash
cd frontend
npm install
npm run dev
```

Abre [http://localhost:5173](http://localhost:5173). El frontend consume la API bajo `/api` mediante proxy de Vite apuntando a `http://127.0.0.1:8000`.

## Environment Configuration

Las variables de entorno opcionales se establecen al ejecutar los scripts:

| Variable   | Default      | Descripción                  |
|------------|--------------|------------------------------|
| `HOST`     | `127.0.0.1`  | Host donde escucha la API    |
| `API_PORT` | `8000`       | Puerto de la API             |
| `RELOAD`   | `true`       | Hot-reload de uvicorn        |

Para configuración personalizada, edita los scripts `run_api.sh` o `run_project.sh`.

## Run Tests And Quality Checks

### Ejecución completa

Desde la raíz del proyecto:

```bash
./run_quality_checks.sh
```

Este script ejecuta:

- Tests unitarios con `pytest`
- Validación de estilo con `flake8`
- Build del frontend con `npm run build`

### Solo backend

#### Tests

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
pytest -v
```

#### Linting

```bash
flake8 app tests
```

### Solo frontend

```bash
cd frontend
npm run build
```

## API Endpoints

### Salud

- `GET /api/health` - Verificar disponibilidad del API

### Juegos

- `GET /api/games` - Listar todos los juegos disponibles

### Puntuaciones

- `GET /api/scores/{game_id}?limit=10` - Obtener top scores de un juego
- `POST /api/scores` - Registrar nueva puntuación

**IDs de juego válidos:** `snake`, `pong`, `memory`, `guess-number`, `reflex`, `sharp-eye`

**Payload para registrar score:**

```json
{
  "game_id": "snake",
  "player_name": "Player1",
  "score": 120
}
```

## Project Structure

```text
falken_games/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py           # Aplicación FastAPI y endpoints
│   │   ├── store.py          # Gestión persistente de datos
│   │   └── data/
│   │       └── scores.json   # Storage JSON de puntuaciones
│   ├── tests/
│   │   ├── conftest.py       # Configuración pytest
│   │   ├── test_api.py       # Tests de endpoints
│   │   └── test_store.py     # Tests de persistencia
│   ├── requirements.txt      # Dependencias producción
│   └── requirements-dev.txt  # Dependencias desarrollo
├── frontend/
│   ├── src/
│   │   ├── App.vue           # Componente raíz
│   │   ├── main.js           # Punto de entrada Vue
│   │   ├── styles.css        # Estilos globales
│   │   ├── components/       # Componentes reutilizables
│   │   ├── games/            # Componentes de juegos
│   │   └── services/
│   │       └── api.js        # Cliente HTTP para API
│   ├── package.json
│   ├── vite.config.js        # Configuración Vite con proxy API
│   └── index.html
├── run_project.sh            # Script para ejecutar ambos servicios
├── run_api.sh                # Script para ejecutar solo backend
├── run_quality_checks.sh     # Script para validar calidad
├── .github/                  # Workflows, templates, instrucciones
├── README.md                 # Este archivo
└── README_plantilla.md       # Plantilla de referencia
```

## Architecture

El proyecto sigue una arquitectura cliente-servidor simple y mantenible:

```text
Frontend (Vue 3) <-- HTTP Client --> Backend (FastAPI) <-- JSON Store
```

### Backend

- **main.py:** Aplicación FastAPI con endpoints CRUD para juegos y scores
- **store.py:** Abstracción para persistencia en JSON
- **tests/:** Suite de tests unitarios con pytest

### Frontend

- **App.vue:** Enrutamiento entre juegos y gestión de estado
- **games/:** Componentes independientes para cada juego
- **services/api.js:** Cliente HTTP centralizado

## Development Notes

- La interfaz es completamente responsive y jugable desde navegador móvil
- **Snake y Pong:** Incluyen controles táctiles en pantalla para móvil
- **Agudeza Visual:** Escala la dificultad progresivamente en 8 rondas (celdas y contraste de color)
- Código backend compatible con Python 3.10+
- Límite de línea: 127 caracteres (flake8)
- Tests unitarios deterministas y aislados

## GitHub Resources

El repositorio incluye recursos reutilizables bajo `.github/`:

- Instrucciones de desarrollo y convenciones de código
- Scripts de validación de calidad
- Configuración de herramientas (pytest, flake8, Vite)

## Roadmap

- Agregar rankings en línea
- Sistema de logros y badges
- Modo multijugador para juegos seleccionados
- Estadísticas detalladas y análisis de rendimiento
- Temas personalizables (modo oscuro/claro)

## License

Este proyecto está licenciado bajo la Licencia MIT. Ver `LICENSE` para detalles.
