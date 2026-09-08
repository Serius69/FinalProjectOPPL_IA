import json
import os
import sqlite3
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

MAIN = Path(__file__).resolve().parents[1] / "main.py"


class SyntheticPipelineTests(unittest.TestCase):
    def invoke(self, path, *extra):
        return subprocess.run(
            [sys.executable, str(MAIN), "--database", str(path), *extra],
            env=dict(os.environ, DJANGO_SETTINGS_MODULE="must_not_load_real_settings"),
            text=True,
            capture_output=True,
            check=False,
            timeout=60,
        )

    def test_full_pipeline_preserves_same_day_transactions_and_solves_budget(self):
        with tempfile.TemporaryDirectory() as directory:
            database = Path(directory) / "pipeline.sqlite"
            run = self.invoke(
                database,
                "--records",
                "40",
                "--start-date",
                "2026-01-01",
                "--end-date",
                "2026-01-01",
            )
            self.assertEqual(run.returncode, 0, run.stderr)
            result = json.loads(run.stdout)
            self.assertTrue(result["full_pipeline_validated"])
            self.assertFalse(result["training_performed"])
            self.assertEqual(result["etl_preserved_transactions"], 40)
            output = Path(result["artifacts"])
            self.assertEqual(len(result["plots"]), 5)
            for name in result["plots"]:
                self.assertTrue(
                    (output / name).read_bytes().startswith(b"\x89PNG\r\n\x1a\n")
                )
            solutions = json.loads((output / "optimization.json").read_text())
            self.assertEqual(len(solutions), 5)
            for solution in solutions:
                rate = float(solution["exchange_rate"])
                self.assertAlmostEqual(solution["total_cost"], 100000, delta=0.05)
                self.assertAlmostEqual(
                    solution["max_exchange_volume"], (100000 / rate) * 1.1, delta=0.05
                )
            with sqlite3.connect(database) as db:
                self.assertEqual(
                    db.execute("SELECT COUNT(*) FROM analyzer_transaction").fetchone()[
                        0
                    ],
                    40,
                )
                self.assertEqual(
                    db.execute("SELECT COUNT(*) FROM analyzer_generativeai").fetchone()[
                        0
                    ],
                    0,
                )
                self.assertEqual(
                    db.execute("PRAGMA integrity_check").fetchone()[0], "ok"
                )
            analysis = json.loads((output / "analysis.json").read_text())
            self.assertIsNone(analysis["trends"]["volumen_tendencia"])

    def test_existing_artifact_directory_is_preserved(self):
        with tempfile.TemporaryDirectory() as directory:
            database = Path(directory) / "pipeline.sqlite"
            output = Path(str(database) + ".artifacts")
            output.mkdir()
            sentinel = output / "owner.txt"
            sentinel.write_text("preserve")
            run = self.invoke(database)
            self.assertNotEqual(run.returncode, 0)
            self.assertEqual(sentinel.read_text(), "preserve")
            self.assertFalse(database.exists())

    def test_invalid_budget_creates_no_output(self):
        with tempfile.TemporaryDirectory() as directory:
            database = Path(directory) / "pipeline.sqlite"
            for budget in ["-1", "nan", "inf"]:
                self.assertNotEqual(
                    self.invoke(database, "--budget", budget).returncode, 0
                )
                self.assertFalse(database.exists())
