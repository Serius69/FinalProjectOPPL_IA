"""Generate academic fixtures into a NEW SQLite file; not the full OPPL pipeline."""

from __future__ import annotations

import argparse
import json
import os
import random
import sys
from contextlib import redirect_stdout
from datetime import date
from io import StringIO
from pathlib import Path


def main(argv=None, *, pipeline=False):
    parser = argparse.ArgumentParser(
        description="Isolated synthetic academic pipeline" if pipeline else __doc__
    )
    parser.add_argument(
        "--database", type=Path, required=True, help="New disposable SQLite output"
    )
    parser.add_argument("--records", type=int, default=20)
    parser.add_argument(
        "--start-date", type=date.fromisoformat, default=date(2026, 1, 1)
    )
    parser.add_argument("--end-date", type=date.fromisoformat, default=date(2026, 1, 7))
    parser.add_argument("--seed", type=int, default=2026)
    if pipeline:
        parser.add_argument("--budget", type=float, default=100000)
        parser.add_argument("--improvement", type=float, default=10)
    args = parser.parse_args(argv)
    if pipeline:
        import math

        if (
            not math.isfinite(args.budget)
            or args.budget <= 0
            or not 0 <= args.improvement <= 100
        ):
            parser.error(
                "budget must be finite and positive; improvement between 0 and 100"
            )
    if not 1 <= args.records <= 10000:
        parser.error("records must be between 1 and 10000")
    if not 0 <= (args.end_date - args.start_date).days <= 366:
        parser.error("date interval must be ordered and at most 366 days")
    database = args.database.absolute()
    try:
        descriptor = os.open(database, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    except FileExistsError:
        parser.error("database already exists; refusing to modify it")
    os.close(descriptor)
    try:
        sys.path.insert(0, str(Path(__file__).resolve().parent / "production_analysis"))
        from django.conf import settings

        settings.configure(
            SECRET_KEY="synthetic-smoke-not-for-serving",
            DATABASES={
                "default": {
                    "ENGINE": "django.db.backends.sqlite3",
                    "NAME": str(database),
                }
            },
            INSTALLED_APPS=["analyzer"],
            DEFAULT_AUTO_FIELD="django.db.models.BigAutoField",
            USE_TZ=True,
            TIME_ZONE="UTC",
        )
        import django

        django.setup()
        from analyzer.models import (
            Currency,
            CurrencyExchangeHouse,
            GenerativeAI,
            Transaction,
        )
        from django.core.management import call_command
        from django.db import connections, transaction
        from scripts import data_generator

        call_command("migrate", interactive=False, verbosity=0)
        random.seed(args.seed)
        with transaction.atomic(), redirect_stdout(StringIO()):
            data_generator.main(
                args.records, args.start_date, args.end_date, include_demo_ai=False
            )
        report = {
            "scope": "SYNTHETIC_GENERATOR_SMOKE_ONLY",
            "database": str(database),
            "exchange_houses": CurrencyExchangeHouse.objects.count(),
            "currencies": Currency.objects.count(),
            "transactions": Transaction.objects.count(),
            "generative_ai_records": GenerativeAI.objects.count(),
            "training_performed": False,
            "full_pipeline_validated": False,
        }
        if pipeline:
            from synthetic_pipeline import run_pipeline

            report.update(run_pipeline(args, database))
        connections.close_all()
    except BaseException:
        try:
            from django.db import connections

            connections.close_all()
        finally:
            database.unlink(missing_ok=True)
        raise
    print(json.dumps(report))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
