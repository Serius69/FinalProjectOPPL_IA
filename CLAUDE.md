# CLAUDE.md — FinalProjectOPPL_IA

Proyecto académico (OPPL / IA): **demo web Django** para analizar y optimizar procesos operativos
de la **Casa de Cambios Tromay**. Genera datos sintéticos, corre un ETL, aplica un optimizador
numérico simple (`scipy.optimize.minimize`, SLSQP) de asignación de presupuesto y produce
visualizaciones PNG/HTML. Docs y nombres en **español**.

> **Alcance honesto:** la "IA generativa" (predicción de tasas/demanda, personal, rutas, GANs/RNN/
> algoritmos genéticos con PyTorch) **no está implementada** — el modelo `GenerativeAI` es solo una
> tabla con métricas sintéticas y la única optimización real es el `scipy.optimize`. Objetivo futuro.

## Stack
- **Python 3.8+** · Django (`requirements.txt`: ≥4.2, probado con 5.1; app web `analyzer`) + scripts de análisis.
- **Datos/optimización:** pandas, numpy, scipy (SLSQP), django-pandas. (Sin PyTorch/scikit-learn.)
- **DB:** MySQL vía variables de entorno (`MYSQL_DATABASE`, `MYSQL_USER`, `MYSQL_PASSWORD`, `DB_HOST`, `DB_PORT`).
  ⚠️ `mysqlclient` **no** está en `requirements.txt`; instalarlo aparte.
- **Visualización:** matplotlib, seaborn → PNG y HTML.

## Estructura
```
main.py                          # Pipeline CLI: generación → ETL → eficiencia → viz → análisis (SQLite sintética aislada)
requirements.txt                 # Dependencias reconstruidas de los imports (sin mysqlclient)
TECH_DEBT.md                     # Baseline de deuda técnica (DEBT-015-1..4)
.github/workflows/ci.yml         # CI GitHub Actions: compileall + manage.py check (Python 3.12)
production_analysis/
  manage.py                      # Entrypoint Django
  production_analysis/settings.py# Config del proyecto Django (DB MySQL desde env)
  analyzer/                      # App Django: models, views, urls, migrations, templates
  scripts/                       # Lógica de negocio (usable standalone o desde views)
    data_generator.py            # Genera datos sintéticos en la DB
    etl_process.py               # ETL ORM por clave primaria
    efficiency_improvement.py    # Optimización de eficiencia (con presupuesto)
    performance_analysis.py      # Análisis de desempeño
    data_visualization.py        # Gráficos PNG/HTML
  templates/analyzer/  static/   # Front (base, index, results, visualizations)
```

## Comandos
- **Instalar deps:** `pip install -r requirements.txt` (+ `pip install mysqlclient` para la DB).
- **Servidor web:** `cd production_analysis && python manage.py runserver`.
- **Migraciones:** `python manage.py makemigrations && python manage.py migrate`.
- **Tests:** `python -m unittest discover -s tests -v` (seis pruebas sintéticas CLI; suite web pendiente).
- **CI local (lo que corre GitHub Actions):** `python -m compileall production_analysis main.py` y `python production_analysis/manage.py check`.

## Modelos clave (analyzer/models.py)
`CurrencyExchangeHouse`, `Currency`, `ExchangeRate`, `ProcessType`, `LogisticProcess`,
`Transaction`, `Optimization`, `Outcome`, `Report`, `GenerativeAI`.

## Gotchas
- El generador ya no elige settings ni inicializa Django al importar. `synthetic_smoke.py` configura SQLite nueva de forma explícita.
- La DB requiere variables de entorno MySQL definidas antes de arrancar Django.
- Las vistas de `analyzer` reutilizan los mismos scripts que `main.py`.

## Baseline de deuda técnica — sesión 2026-07-28 (`codex/DEBT-015-baseline`)
Commit `chore(oppl): baseline de deuda — CI + TECH_DEBT + requirements reconstruido [DEBT-015]`.
Añadió `requirements.txt` (de los imports reales), `.github/workflows/ci.yml` (compileall + `manage.py
check` en Python 3.12) y `TECH_DEBT.md`. Hallazgos catalogados: DEBT-015-1 requirements ausente
(FIXED), DEBT-015-2 CI ausente (FIXED), DEBT-015-3 tests sin cobertura (DISCOVERED), DEBT-015-4
artefactos PNG/HTML versionados (DISCOVERED). No se alteró lógica ni se borraron artefactos.

## Auditoría de seguridad — sesión 2026-07-07 (claude/audit-modernize)
Auditoría de seguridad aplicada vía patch (`active__finalprojectoppl-ia.patch`), repo git inicializado
desde cero en esta sesión (no existía `.git` previo).

- **`production_analysis/production_analysis/settings.py`:** `SECRET_KEY`, `DEBUG` y `ALLOWED_HOSTS`
  ahora se leen de `os.getenv()` (`DJANGO_SECRET_KEY`, `DJANGO_DEBUG`, `DJANGO_ALLOWED_HOSTS`).
  `DEBUG` por defecto `False`; `ALLOWED_HOSTS` vacío si no se define (fuerza configurarlo explícito
  en despliegue). `SECRET_KEY` conserva el valor `django-insecure-...` solo como fallback de
  desarrollo local — **rotar el secreto real es una acción operativa pendiente** (generar uno nuevo
  y setear `DJANGO_SECRET_KEY` al desplegar).
- **`production_analysis/analyzer/views.py`:** `generate_data`, `run_etl` e `improve_efficiency`
  ahora exigen `@login_required` + `@require_POST` (antes eran endpoints GET sin auth que mutaban
  datos). `improve_efficiency` lee sus parámetros de `request.POST` en vez de `request.GET`.
- **Limitación conocida (seguimiento pendiente, fuera del alcance del patch):** `base.html` e
  `index.html` usan `<a href="{% url ... %}">` (GET) para estos endpoints — dejarán de funcionar
  hasta reemplazarlos por `<form method="post">{% csrf_token %}...</form>` y hasta que exista un
  flujo de login (no hay `LOGIN_URL` configurado ni `/accounts/login/` registrado en `urls.py`).
- Sin Docker en el repo. `.gitignore` ya cubría `.env`/`venv`/`__pycache__` correctamente.

## Smoke sintético acotado2026-09-08

`python synthetic_smoke.py --database NUEVA.sqlite3` prueba solo generación sintética aislada; exige salida inexistente, no carga MySQL/dotenv y no crea registros ficticios de modelos entrenados.

## Pipeline sintético reparado (2026-09-08)

`python main.py --database /ruta/nueva/pipeline.sqlite3 --records 40` ejecuta
la generación → ETL ORM → optimización SciPy → cinco PNG → análisis descriptivo.
Requiere Django, pandas, NumPy, SciPy, matplotlib y seaborn; usa SQLite nueva,
ignora settings externos y rechaza bases o directorios de artefactos existentes.
`synthetic_smoke.py` conserva el smoke de generación independiente.

Seis pruebas con `python -m unittest discover -s tests -v` cubren integridad,
transacciones del mismo día, óptimo frente a solución analítica, gráficos PNG,
no sobrescritura y parámetros inválidos. Validado con Python 3.12 y Django 5.2.17.
Los resultados son fixtures sintéticos, no evidencia de desempeño económico ni de IA.
No se entrenan modelos, no se presenta una entrega académica y no se valida el flujo web.
Los formularios POST/login web siguen pendientes. Un único día no permite estimar tendencia.
