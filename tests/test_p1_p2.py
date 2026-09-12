#!/usr/bin/env python3
from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from mvcg.corridor import e64_kappa_window, e68_n_band, e68_n_white  # noqa: E402
from mvcg.registers import run_registers  # noqa: E402


class TestP1Replay(unittest.TestCase):
    def test_p21_p30_p35(self) -> None:
        by = {r["id"]: r for r in run_registers()["rows"]}
        self.assertEqual(by["P21_H2O_dipole"]["verdict"], "S-")
        self.assertEqual(by["P30_Kato_gaussian"]["verdict"], "S-")
        self.assertEqual(by["P30_Kato_1s"]["verdict"], "S+")
        self.assertEqual(by["P35_sigma_spike"]["verdict"], "S-")
        self.assertFalse(by["P35_sigma_spike"]["b3_fail"])
        self.assertEqual(by["P30_Kato_gaussian"]["statut"], "partielle")
        self.assertEqual(by["P35_sigma_spike"]["campaign"], "P35")


class TestP2Corridor(unittest.TestCase):
    def test_e68_white_moves(self) -> None:
        w = e68_n_white()
        b = e68_n_band()
        self.assertEqual(w["prevision"], "mot_change")
        self.assertEqual(b["verdict"], "S+")
        self.assertGreater(w["spread"], b["spread"])

    def test_e64_window(self) -> None:
        self.assertEqual(e64_kappa_window(0.10)["verdict"], "P")
        self.assertEqual(e64_kappa_window(0.40)["verdict"], "S-")


if __name__ == "__main__":
    unittest.main(verbosity=2)
