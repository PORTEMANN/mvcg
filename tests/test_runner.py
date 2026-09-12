#!/usr/bin/env python3
from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from mvcg.h2plus import HA_TO_EV, lcao_1s  # noqa: E402
from mvcg.registers import run_registers  # noqa: E402
from mvcg.runner import execute  # noqa: E402


class TestRunner(unittest.TestCase):
    def test_execute_chain(self) -> None:
        def fn():
            return 2.0, {"u": "Ha"}

        mu, extra = execute(fn, chain=[{"tau": "energy", "src": "Ha", "dst": "eV", "k": 10.0}])
        self.assertEqual(mu, 20.0)
        self.assertEqual(extra["mu_raw"], 2.0)
        self.assertEqual(extra["chain"]["k"], 10.0)

    def test_p20_ha_then_ev(self) -> None:
        by = {r["id"]: r for r in run_registers()["rows"]}
        row = by["P20_H2plus_LCAO"]
        self.assertEqual(row["verdict"], "S-")
        self.assertAlmostEqual(row["mu_loc"], lcao_1s(2.0)["De_eV"], places=6)
        self.assertAlmostEqual(row["extra"]["mu_raw"], lcao_1s(2.0)["De_Ha"], places=6)
        self.assertAlmostEqual(row["extra"]["chain"]["k"], HA_TO_EV, places=6)

    def test_chain_kill_forces_sminus(self) -> None:
        # μ brut == μ_ref : sans le kill, le mot serait S+ sur la mauvaise fibre.
        from mvcg import registers

        registers.RUNNERS["t_kill"] = lambda: (2.6508, {})
        try:
            c = registers.Contact(
                "T_kill", "micro", "pred", "si", "eV", "rel", 0.05,
                2.6508, "—", "—", "kill chaîne → S-", "test régression",
                "t_kill",
                chain=[{"tau": "energy", "src": "Ha", "dst": "eV", "k": 27.2},
                       {"tau": "length", "src": "eV", "dst": "eV", "k": 1.0}],
            )
            row = registers.run_contact(c)
        finally:
            del registers.RUNNERS["t_kill"]
        self.assertEqual(row["verdict"], "S-")
        self.assertIsNotNone(row["chain_kill"])
        self.assertIn("chain:", row["units_kill"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
