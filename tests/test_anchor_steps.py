#!/usr/bin/env python3
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from mvcg.campaign import run_campaign  # noqa: E402
from mvcg.registers import run_registers  # noqa: E402
from mvcg.tables import he_corr, h2plus_de  # noqa: E402


class TestAnchor(unittest.TestCase):
    def test_literature_tables(self) -> None:
        self.assertEqual(h2plus_de()["vintage"], "LITERATURE-2018")
        self.assertEqual(he_corr()["vintage"], "LITERATURE-2018")
        self.assertAlmostEqual(he_corr()["value"], -0.042044)

    def test_p27(self) -> None:
        by = {r["id"]: r for r in run_registers()["rows"]}
        self.assertEqual(by["P27_He_HF"]["verdict"], "S-")
        self.assertEqual(by["P27_He_table"]["verdict"], "S+")
        self.assertFalse(by["P27_He_HF"]["b3_fail"])

    def test_publish_writes_d(self) -> None:
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        run_campaign(Path(tmp.name), offline_ots=True, commit=True)
        bits = list(Path(tmp.name).glob("*.D.json"))
        self.assertGreaterEqual(len(bits), 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
