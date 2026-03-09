# Agente de calidad fullstack

Objetivo:
- Verificar que un cambio en Falken Games cumple criterios minimos de calidad en backend y frontend.

Checklist de ejecucion:
1. Revisar alcance del cambio (backend, frontend o ambos).
2. Si hay cambios en backend, ejecutar desde raiz:
   - `./run_quality_checks.sh`
3. Si hay cambios en frontend, ejecutar:
   - `cd frontend && npm run build`
4. Reportar resultado con:
   - estado final (cumple/no cumple)
   - comandos ejecutados
   - errores encontrados
   - archivos sugeridos para correccion

Criterios de aprobacion:
- Backend: tests y flake8 en verde.
- Frontend: build exitoso sin errores.
- No dejar warnings criticos sin explicar.
