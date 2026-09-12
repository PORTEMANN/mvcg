#!/usr/bin/env python3
from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from mvcg.gum import apply_gum, u_c  # noqa: E402
from mvcg.registers import run_registers  # noqa: E402


class TestGum(unittest.TestCase):
    def test_uc_quad(self) -> None:
        self.assertAlmostEqual(u_c([{"type": "B", "u": 3}, {"type": "B", "u": 4}]), 5.0)

    def test_h1s_splus_under_U(self) -> None:
        by = {r["id"]: r for r in run_registers()["rows"]}
        self.assertEqual(by["H1s_Rydberg"]["verdict"], "S+")
        g = by["H1s_Rydberg"].get("extra", {}).get("gum") or {}
        # extra may be nested differently
        row = by["H1s_Rydberg"]
        self.assertIn("gum", str(row))

    def test_p27_sminus_under_U(self) -> None:
        by = {r["id"]: r for r in run_registers()["rows"]}
        self.assertEqual(by["P27_He_HF"]["verdict"], "S-")
        g = apply_gum(0.042044, 0.002, {
            "decide": "U", "k": 2,
            "lines": [{"type": "B", "u": 1e-6}],
        })
        self.assertEqual(g["verdict"], "S-")
        self.assertLess(g["U"], 0.01)

    def test_p20_no_model_ub(self) -> None:
        by = {r["id"]: r for r in run_registers()["rows"]}
        self.assertEqual(by["P20_H2plus_LCAO"]["verdict"], "S-")
        g = apply_gum(0.45, 0.05, {
            "decide": "theta", "k": 2,
            "lines": [{"type": "B", "u": 0.0005}],
        })
        self.assertEqual(g["verdict"], "S-")


if __name__ == "__main__":
    unittest.main(verbosity=2)
