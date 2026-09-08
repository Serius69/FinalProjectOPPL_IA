"""Scientific pipeline orchestration, only after isolated synthetic settings bootstrap."""

import json
import os
import shutil
from pathlib import Path


def run_pipeline(args, database):
    import matplotlib

    matplotlib.use("Agg")
    from contextlib import redirect_stdout
    from io import StringIO

    from analyzer.models import LogisticProcess, Transaction
    from scripts.data_visualization import generate_visualizations
    from scripts.efficiency_improvement import improve_efficiency
    from scripts.etl_process import etl_process
    from scripts.performance_analysis import perform_analysis

    output = Path(str(database) + ".artifacts")
    output.mkdir(mode=0o700)  # Never reuse or overwrite existing outputs.
    previous = Path.cwd()
    try:
        before = list(
            Transaction.objects.order_by("pk").values_list(
                "pk", "amount", "exchange_rate_id"
            )
        )
        # Synthetic process dates align with the generated exchange-rate interval.
        LogisticProcess.objects.update(start_date=args.start_date)
        with redirect_stdout(StringIO()):
            etl_process()
            after = list(
                Transaction.objects.order_by("pk").values_list(
                    "pk", "amount", "exchange_rate_id"
                )
            )
            if before != after:
                raise AssertionError(
                    "ETL changed transaction identity or financial values"
                )
            optimized = [
                dict(
                    process_id=p.pk,
                    **improve_efficiency(p.pk, args.budget, args.improvement),
                )
                for p in LogisticProcess.objects.filter(
                    transactions__isnull=False
                ).distinct()
            ]
            os.chdir(output)
            generate_visualizations()
            analysis = perform_analysis()
        # All values are synthetic; statistics are descriptive, not measured AI performance.
        (output / "optimization.json").write_text(json.dumps(optimized, default=str))
        (output / "analysis.json").write_text(
            json.dumps(
                {
                    "kpis": analysis["kpis"],
                    "trends": analysis["tendencias"],
                    "source": "SYNTHETIC_FIXTURES_NO_TRAINING",
                },
                default=float,
                allow_nan=False,
            )
        )
        return {
            "scope": "SYNTHETIC_FULL_PIPELINE",
            "full_pipeline_validated": True,
            "optimized_processes": len(optimized),
            "etl_preserved_transactions": len(after),
            "artifacts": str(output),
            "plots": sorted(p.name for p in output.glob("*.png")),
        }
    except BaseException:
        shutil.rmtree(output)
        raise
    finally:
        os.chdir(previous)
