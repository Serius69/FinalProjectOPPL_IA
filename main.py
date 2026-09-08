"""Run the academic generator → ETL → optimization → plots → analysis on NEW synthetic SQLite."""

from synthetic_smoke import main

if __name__ == "__main__":
    raise SystemExit(main(pipeline=True))
