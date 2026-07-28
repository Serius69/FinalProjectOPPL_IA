# Deuda técnica

## DEBT-015-1 — Manifest de dependencias ausente

- **Severidad:** HIGH
- **Categoría:** MAINTAINABILITY
- **Evidencia:** el repositorio no contaba con `requirements.txt` ni `pyproject.toml`.
- **Archivo:** `requirements.txt`
- **Impacto:** no era posible reconstruir de forma reproducible el entorno requerido por Django y el pipeline de análisis.
- **Causa:** las dependencias externas solo estaban expresadas mediante imports en el código.
- **Solución:** reconstruir `requirements.txt` a partir de los imports reales, con especificadores de versión laxos.
- **Riesgo:** LOW_RISK
- **Prueba requerida:** `pip install -r requirements.txt`
- **Estado:** FIXED; el manifest fue reconstruido mediante análisis de imports.

## DEBT-015-2 — Integración continua ausente

- **Severidad:** HIGH
- **Categoría:** CI_CD
- **Evidencia:** el repositorio no contaba con workflows en `.github/workflows/`.
- **Archivo:** `.github/workflows/ci.yml`
- **Impacto:** errores de sintaxis o una configuración inválida de Django podían integrarse sin validación automática.
- **Causa:** ausencia de un pipeline de integración continua.
- **Solución:** ejecutar un smoke de compilación y `manage.py check` con Python 3.12 en cada push y pull request.
- **Riesgo:** LOW_RISK
- **Prueba requerida:** `python -m compileall production_analysis main.py` y `python production_analysis/manage.py check`
- **Estado:** FIXED; pendiente de verificar la primera ejecución remota de GitHub Actions.

## DEBT-015-3 — Suite de tests sin cobertura efectiva

- **Severidad:** MEDIUM
- **Categoría:** TESTING
- **Evidencia:** `production_analysis/analyzer/tests.py` conserva únicamente el import generado por defecto por Django y no define casos de prueba.
- **Archivo:** `production_analysis/analyzer/tests.py`
- **Impacto:** regresiones funcionales en modelos, vistas y procesos de análisis pueden pasar inadvertidas.
- **Causa:** no se desarrolló una suite específica para el comportamiento de la aplicación.
- **Solución propuesta:** incorporar tests unitarios y de integración para modelos, vistas y scripts, con datos deterministas.
- **Riesgo:** MODERATE_RISK
- **Prueba requerida:** `python production_analysis/manage.py test`
- **Estado:** DISCOVERED; requiere trabajo futuro sin alterar la lógica en este baseline.

## DEBT-015-4 — Artefactos generados versionados

- **Severidad:** LOW
- **Categoría:** MAINTAINABILITY
- **Evidencia:** el repositorio contiene archivos PNG y HTML generados dentro de `production_analysis/`.
- **Archivo:** `production_analysis/*.png`, `production_analysis/*.html`, `production_analysis/static/analyzer/images/*.{png,html}`
- **Impacto:** los resultados derivados pueden producir ruido en revisiones y aumentar el tamaño del historial.
- **Causa:** las salidas del pipeline se incorporaron al control de versiones junto con el código fuente.
- **Solución propuesta:** identificar de forma explícita las salidas regenerables y añadirlas a `.gitignore` en un cambio futuro, preservando los artefactos actuales hasta acordar su política.
- **Riesgo:** LOW_RISK
- **Prueba requerida:** ejecutar el pipeline y verificar que las salidas ignoradas puedan regenerarse.
- **Estado:** DISCOVERED; no se borran artefactos ni se modifica `.gitignore` en este baseline.
