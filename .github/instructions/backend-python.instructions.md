---
applyTo: "backend/**/*.py,backend/tests/**/*.py"
---

## Instrucciones Backend (Python/FastAPI)

- Mantener endpoints bajo prefijo `/api`.
- Conservar mensajes de error funcionales en espanol salvo requerimiento contrario.
- Cada cambio en logica de negocio debe agregar o actualizar tests en `backend/tests/`.
- Usar typing explicito cuando aporte claridad.
- Evitar side effects globales fuera de inicializacion controlada.

## Validacion local requerida
Ejecutar en `backend/`:

```bash
pytest -rs
flake8 app tests
```

Si el cambio se hace desde la raiz del repo, preferir:

```bash
./run_quality_checks.sh
```
