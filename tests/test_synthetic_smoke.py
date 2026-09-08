import json
import os
import sqlite3
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "synthetic_smoke.py"


class SyntheticSmokeTests(unittest.TestCase):
    def run_cli(self, directory, *arguments):
        env = dict(os.environ, DJANGO_SETTINGS_MODULE="must_not_import_real_settings")
        return subprocess.run(
            [sys.executable, str(SCRIPT), *arguments],
            cwd=directory,
            env=env,
            capture_output=True,
            text=True,
            check=False,
            timeout=30,
        )

    def test_fresh_sqlite_generation_ignores_external_settings(self):
        with tempfile.TemporaryDirectory() as directory:
            database = Path(directory) / "synthetic.sqlite3"
            result = self.run_cli(
                directory,
                "--database",
                str(database),
                "--records",
                "4",
                "--start-date",
                "2026-01-01",
                "--end-date",
                "2026-01-03",
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            report = json.loads(result.stdout)
            self.assertEqual(report["transactions"], 4)
            self.assertFalse(report["training_performed"])
            self.assertFalse(report["full_pipeline_validated"])
            with sqlite3.connect(database) as connection:
                self.assertEqual(
                    connection.execute(
                        "SELECT COUNT(*) FROM analyzer_currency"
                    ).fetchone()[0],
                    2,
                )
                self.assertEqual(
                    connection.execute(
                        "SELECT COUNT(*) FROM analyzer_exchangerate"
                    ).fetchone()[0],
                    6,
                )
                self.assertEqual(
                    connection.execute(
                        "SELECT COUNT(*) FROM analyzer_generativeai"
                    ).fetchone()[0],
                    0,
                )
                self.assertEqual(
                    connection.execute("PRAGMA integrity_check").fetchone()[0], "ok"
                )
            self.assertEqual(database.stat().st_mode & 0o777, 0o600)

    def test_existing_output_is_never_modified(self):
        with tempfile.TemporaryDirectory() as directory:
            database = Path(directory) / "existing.sqlite3"
            database.write_bytes(b"existing-data-must-survive")
            result = self.run_cli(directory, "--database", str(database))
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(database.read_bytes(), b"existing-data-must-survive")

    def test_invalid_interval_creates_no_database(self):
        with tempfile.TemporaryDirectory() as directory:
            database = Path(directory) / "invalid.sqlite3"
            result = self.run_cli(
                directory,
                "--database",
                str(database),
                "--start-date",
                "2026-02-01",
                "--end-date",
                "2026-01-01",
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertFalse(database.exists())
