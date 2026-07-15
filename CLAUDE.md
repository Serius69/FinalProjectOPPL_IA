# CLAUDE.md — FinalProjectOPPL_IA

Sistema de IA generativa para optimizar los procesos operativos de la **Casa de Cambios Tromay**
(predicción de tasas/demanda, asignación de personal, inventario de divisas, rutas de entrega).
Docs y nombres en **español**.

## Stack
- **Python 3.8+** · Django 5.1 (app web `analyzer`) + scripts de análisis/ML.
- **ML/datos:** PyTorch, Pandas, NumPy, Scikit-learn (GANs, RNN, algoritmos genéticos).
- **DB:** MySQL vía variables de entorno (`MYSQL_DATABASE`, `MYSQL_USER`, `MYSQL_PASSWORD`, `DB_HOST`).
- **Visualización:** Matplotlib/Plotly → PNG y HTML.

## Estructura
```
main.py                          # Pipeline CLI: generación → ETL → eficiencia → viz → análisis
production_analysis/
  manage.py                      # Entrypoint Django
  production_analysis/settings.py# Config del proyecto Django (DB MySQL desde env)
  analyzer/                      # App Django: models, views, urls, migrations, templates
  scripts/                       # Lógica de negocio (usable standalone o desde views)
    data_generator.py            # Genera datos sintéticos en la DB
    etl_process.py               # ETL raw → processed CSV
    efficiency_improvement.py    # Optimización de eficiencia (con presupuesto)
    performance_analysis.py      # Análisis de desempeño
    data_visualization.py        # Gráficos PNG/HTML
  templates/analyzer/  static/   # Front (base, index, results, visualizations)
```

## Comandos
- **Pipeline standalone:** `python main.py` (genera `raw_/processed_production_data.csv` + gráficos).
- **Servidor web:** `cd production_analysis && python manage.py runserver`.
- **Migraciones:** `python manage.py makemigrations && python manage.py migrate`.
- **Tests:** `python manage.py test`.

## Modelos clave (analyzer/models.py)
`CurrencyExchangeHouse`, `Currency`, `ExchangeRate`, `ProcessType`, `LogisticProcess`,
`Transaction`, `Optimization`, `Outcome`, `Report`, `GenerativeAI`.

## Gotchas
- Los scripts hacen `django.setup()` con `DJANGO_SETTINGS_MODULE` — algunos aún referencian
  `your_project_name.settings`; debe ser `production_analysis.settings` para correr standalone.
- La DB requiere variables de entorno MySQL definidas antes de arrancar Django.
- Las vistas de `analyzer` reutilizan los mismos scripts que `main.py`.

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
