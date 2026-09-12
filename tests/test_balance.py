#!/usr/bin/env python3
from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from mvcg.balance import CALIBERS, after_tare, caliber_theta  # noqa: E402
from mvcg.h2plus import lcao_1s  # noqa: E402
from mvcg.registers import run_registers  # noqa: E402


class TestBalance(unittest.TestCase):
    def test_tare_zero(self) -> None:
        self.assertEqual(after_tare(-2.86168, -2.86168), 0.0)

    def test_calibers_named(self) -> None:
        self.assertEqual(caliber_theta("fin", "rel"), 1e-12)
        self.assertEqual(caliber_theta("labo", "rel"), 0.05)
        self.assertIn("grossier", CALIBERS)

    def test_p20_tare_declared(self) -> None:
        s = lcao_1s(2.0)
        self.assertAlmostEqual(s["tare_Ha"], -0.5)
        self.assertEqual(s["caliber"], "labo")
        by = {r["id"]: r for r in run_registers()["rows"]}
        self.assertEqual(by["P20_H2plus_LCAO"]["verdict"], "S-")
        self.assertEqual(by["P27_He_HF"]["verdict"], "S-")
        self.assertEqual(by["P27_He_HF"]["tare"], by["P27_He_HF"]["extra"]["tare_Ha"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
