#!/usr/bin/env python3
from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from mvcg.h2plus import lcao_1s  # noqa: E402
from mvcg.protocols import load_protocol, protocol_to_d  # noqa: E402
from mvcg.registers import run_registers  # noqa: E402
from mvcg.tables import load_table  # noqa: E402


class TestOpenRest(unittest.TestCase):
    def test_lcao_lowe_R2(self) -> None:
        s = lcao_1s(2.0)
        self.assertAlmostEqual(s["S"], 0.586, places=2)
        self.assertAlmostEqual(s["E"], -0.554, places=2)
        self.assertGreater(s["De_eV"], 1.4)
        self.assertLess(s["De_eV"], 1.6)

    def test_p20_uses_solver(self) -> None:
        by = {r["id"]: r for r in run_registers()["rows"]}
        self.assertEqual(by["P20_H2plus_LCAO"]["verdict"], "S-")
        self.assertAlmostEqual(by["P20_H2plus_LCAO"]["mu_loc"], lcao_1s(2.0)["De_eV"], places=6)

    def test_codata_extract(self) -> None:
        c = load_table("codata2018_extract.json")["constants"]
        self.assertAlmostEqual(c["Rydberg_eV"], 13.605693122994)

    def test_protocol_import(self) -> None:
        doc = load_protocol("P20.protocol.json")
        d = protocol_to_d(doc, mu_ref=2.6508)
        self.assertEqual(d["id"], "P20_H2plus")
        self.assertEqual(d["packet"], "si")


if __name__ == "__main__":
    unittest.main(verbosity=2)
