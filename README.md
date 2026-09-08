# Optimización de Procesos — Casa de Cambios Tromay (FinalProjectOPPL_IA)

Proyecto académico: **demo web Django** para analizar y optimizar procesos operativos de la
Casa de Cambios Tromay. Genera datos sintéticos de transacciones/procesos, corre un ETL
sobre ellos, aplica un **optimizador numérico simple** (`scipy.optimize.minimize`, SLSQP)
de asignación de presupuesto y produce visualizaciones (PNG/HTML).

> **Nota de alcance honesta:** la versión anterior de este README prometía "IA generativa"
> con GANs, RNN y algoritmos genéticos (PyTorch). **Nada de eso está implementado**: el
> modelo `GenerativeAI` es solo una tabla con métricas inventadas (`random.uniform`) y la
> única "optimización" real es un `scipy.optimize` de una variable. Queda como objetivo
> futuro, no como funcionalidad existente.

## Estado real (auditoría 2026-07 · reconciliado 2026-07-29): ~35 %

- ✅ App Django `analyzer` funcional (vistas server-rendered cableadas a los scripts).
- ✅ Generador de datos sintéticos, ETL ORM con identidad preservada, optimizador scipy, gráficos.
- ✅ Seguridad endurecida (aplicado; cierre verificado **2026-07-08**): `SECRET_KEY`/`DEBUG`/
  `ALLOWED_HOSTS` desde variables de entorno; `generate_data`, `run_etl` e
  `improve_efficiency` exigen `@login_required` + `@require_POST`.
- ✅ **Baseline de deuda técnica (2026-07-28, rama `codex/DEBT-015-baseline`):** `requirements.txt`
  reconstruido a partir de los imports reales, CI en GitHub Actions (`.github/workflows/ci.yml`) y
  `TECH_DEBT.md` con 4 hallazgos catalogados (DEBT-015-1..4).
- ❌ Sin GANs/RNN/algoritmos genéticos ni predicción real de tasas/demanda/rutas/personal.
- ❌ Sin tests web efectivos (`analyzer/tests.py` solo tiene el `import` por defecto de Django —
  DEBT-015-3); sin flujo de login (los enlaces GET de los templates dejaron de funcionar al
  exigir POST+auth — seguimiento pendiente).
- ⚠️ `requirements.txt` **no** incluye `mysqlclient` (el driver de la DB configurada); hay que
  instalarlo aparte para arrancar Django contra MySQL (DEBT pendiente).

## Stack

- **Python 3.8+** · **Django 5.1** (app `analyzer`) · MySQL (`mysqlclient`) vía variables de entorno.
- **Datos/optimización:** pandas, numpy, scipy (SLSQP), django-pandas.
- **Visualización:** matplotlib, seaborn → PNG/HTML en `static/analyzer/images/`.
- Sin Docker. Dependencias en `requirements.txt` (Django≥4.2 — probado con 5.1 —, django-pandas,
  pandas, numpy, scipy, matplotlib, seaborn, python-dotenv):

```bash
pip install -r requirements.txt
pip install mysqlclient   # no está en requirements.txt; necesario para la DB MySQL
```

## Cómo correr (servidor web)

```bash
# 1) Variables de entorno (o archivo .env — settings.py carga dotenv)
export MYSQL_DATABASE=tromay MYSQL_USER=... MYSQL_PASSWORD=... DB_HOST=127.0.0.1 DB_PORT=3306
export DJANGO_SECRET_KEY="$(python -c 'import secrets;print(secrets.token_urlsafe(50))')"
export DJANGO_DEBUG=true            # solo desarrollo; por defecto False
export DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

# 2) Migraciones y servidor
cd production_analysis
python manage.py migrate
python manage.py runserver
```

- Los endpoints mutantes (`/generate_data/`, `/run_etl/`, `/improve_efficiency/`) requieren
  sesión autenticada y método POST (`python manage.py createsuperuser` para crear usuario).
  El generador ya no selecciona settings ni ejecuta `django.setup()` al importar.

## Smoke sintético aislado (no es el pipeline completo)

Requiere únicamente Django; no necesita MySQL, pandas, numpy ni entrenamiento.
El archivo de salida debe ser nuevo: nunca modifica una base existente ni carga
el settings web/MySQL del entorno.

```bash
python synthetic_smoke.py --database /ruta/nueva/oppl-smoke.sqlite3 \
  --records 20 --start-date 2026-01-01 --end-date 2026-01-07 --seed 2026
python -m unittest discover -s tests -p test_synthetic_smoke.py -v
```

Aplica las migraciones del modelo académico en SQLite, genera las relaciones y
transacciones sintéticas, y devuelve conteos JSON. No crea registros de IA generativa,
no entrena modelos y no valida ETL, optimización ni visualización. Se probó con
Django5.2.17 usando cuatro transacciones y seis tasas de cambio; salida privada0600.

## Estructura

```
main.py                          # Pipeline CLI: generación → ETL → eficiencia → viz → análisis (SQLite sintética aislada)
requirements.txt                 # Dependencias (sin mysqlclient — instalar aparte)
TECH_DEBT.md                     # Baseline de deuda técnica (DEBT-015-1..4)
.github/workflows/ci.yml         # CI: compileall + manage.py check (Python 3.12)
production_analysis/
  manage.py                      # Entrypoint Django
  production_analysis/settings.py# Config (SECRET_KEY/DEBUG/ALLOWED_HOSTS y MySQL desde env; carga dotenv)
  analyzer/                      # App Django: models, views, urls, migrations
  scripts/                       # Lógica de negocio (usada por las views y por main.py)
  templates/analyzer/  static/   # Front server-rendered (base, index, results, visualizations)
```

## Licencia

Ver [LICENSE](LICENSE).

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
