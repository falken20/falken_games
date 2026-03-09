# Falken Games - Instrucciones de repositorio

Este proyecto es fullstack con:
- Backend: Python + FastAPI (`backend/`)
- Frontend: Vue 3 + Vite (`frontend/`)

## Reglas de trabajo
- Mantener cambios pequenos y enfocados.
- No romper contratos de API existentes en `backend/app/main.py`.
- Para cambios de backend, acompanar con tests unitarios en `backend/tests/`.
- Mantener el codigo compatible con Python 3.10+.
- Evitar introducir dependencias nuevas sin justificacion clara.

## Calidad obligatoria antes de cerrar un cambio
Desde la raiz del repo ejecutar:

```bash
./run_quality_checks.sh
```

Ese script valida:
- Tests unitarios (`pytest`)
- Linter de backend (`flake8`)

Para frontend, ademas ejecutar:

```bash
cd frontend
npm run build
```

## Convenciones de pruebas
- Preferir pruebas deterministas y aisladas.
- Usar `tmp_path` para persistencia temporal en backend.
- Cuando no exista una dependencia de API en entorno local (ej. `pydantic`), permitir `skip` explicito en tests de integracion ligera.
