#!/usr/bin/env python3
from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from mvcg.verdict_register import (  # noqa: E402
    COLORS,
    index_verdicts,
    lcao_unit_street,
    mode_unites,
    street_sweep,
)


class TestVerdictRegister(unittest.TestCase):
    def test_all_fibers(self) -> None:
        idx = index_verdicts()
        self.assertGreaterEqual(len(idx["fibres"]), 2)
        self.assertIn("n'est pas une entrée", idx["warning"])

    def test_mode_eV(self) -> None:
        idx = mode_unites("si", "eV")
        self.assertEqual(idx["filter"]["dimension"], "eV")
        self.assertTrue(idx["fibres"])
        ids = idx["fibres"][0]["ids"]
        self.assertIn("P20_H2plus_LCAO", ids)
        self.assertNotIn("PIR_CO2_nu3_harmonic", ids)

    def test_no_eta_mu(self) -> None:
        idx = index_verdicts()
        self.assertNotIn("eta", idx)
        self.assertNotIn("mu_loc", idx)

    def test_street_p20(self) -> None:
        st = street_sweep("P20_H2plus_LCAO")
        self.assertEqual(st["home_verdict"], "S-")
        by = {r["packet"]: r for r in st["rows"]}
        self.assertEqual(by["si"]["verdict"], "S-")
        self.assertEqual(by[st["home_packet"]]["color"], st["home_packet"])
        self.assertEqual(len(st["rows"]), 4)

    def test_pack_color_maintained(self) -> None:
        self.assertEqual(set(COLORS), {"hl", "gauss", "si", "1"})
        idx = index_verdicts()
        for fib in idx["fibres"]:
            self.assertEqual(fib["color"], fib["packet"])

    def test_lcao_unit_street(self) -> None:
        st = lcao_unit_street()
        self.assertEqual(st["mots"]["eV"], "S-")
        self.assertEqual(st["mots"]["Ha"], "S-")
        self.assertEqual(st["mots"]["cm-1"], "S-")
        ev = next(r for r in st["rows"] if r["dimension"] == "eV")
        ha = next(r for r in st["rows"] if r["dimension"] == "Ha")
        self.assertAlmostEqual(ev["delta"], ha["delta"], places=9)


if __name__ == "__main__":
    unittest.main(verbosity=2)
