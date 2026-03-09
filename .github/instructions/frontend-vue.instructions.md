---
applyTo: "frontend/src/**/*.vue,frontend/src/**/*.js,frontend/src/**/*.css"
---

## Instrucciones Frontend (Vue 3 + Vite)

- Mantener componentes simples y legibles.
- No romper el consumo de API en `frontend/src/services/api.js`.
- Preservar la experiencia en desktop y mobile.
- Evitar introducir librerias nuevas sin necesidad.

## Validacion local recomendada
En `frontend/`:

```bash
npm run build
```

Si se tocan integraciones con backend, ejecutar tambien:

```bash
cd ..
./run_quality_checks.sh
```
