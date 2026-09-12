#!/usr/bin/env python3
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from mvcg.chain import apply_chain, egal  # noqa: E402
from mvcg.met_lib import MetLib15  # noqa: E402
from mvcg.metrics import _verdict  # noqa: E402
from mvcg.rationalization import parse_units  # noqa: E402
from mvcg.registers import run_registers  # noqa: E402
from mvcg.tables import h2plus_de  # noqa: E402


class TestP0Lab(unittest.TestCase):
    def test_table_h2plus(self) -> None:
        t = h2plus_de()
        self.assertIn(t["vintage"], ("DEMO-2026", "LITERATURE-2018"))
        self.assertAlmostEqual(t["value"], 2.6508)

    def test_p20_lcao_is_sminus(self) -> None:
        by = {r["id"]: r for r in run_registers()["rows"]}
        self.assertEqual(by["P20_H2plus_LCAO"]["verdict"], "S-")
        self.assertEqual(by["P20_H2plus_table"]["verdict"], "S+")

    def test_dossier_in_g1_hash(self) -> None:
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        lib = MetLib15(Path(tmp.name), offline_ots=True)
        D = {
            "id": "P20_H2plus_LCAO",
            "s": "De LCAO = table",
            "packet": "si",
            "dimension": "eV",
            "theta": 0.05,
            "sigma": 0.01,
            "mu_ref": 2.6508,
            "lever": "ansatz←table",
            "delta_kind": "rel",
            "register": "micro",
            "orig": "pred",
        }
        rec = lib.freeze("P20_H2plus_LCAO", phys=1, orig="pred", kappa_hat="equilibre", dossier=D)
        self.assertTrue(rec.d_sha256)
        self.assertTrue((Path(tmp.name) / "P20_H2plus_LCAO.D.json").exists())
        lib.measure("P20_H2plus_LCAO", 2)
        g1 = lib.audit_g1("P20_H2plus_LCAO")
        self.assertFalse(g1.kill, g1.reason)

    def test_chain_egal(self) -> None:
        ev_j = {"tau": "E", "src": "eV", "dst": "J", "k": 1.602176634e-19}
        j_p = {"tau": "E", "src": "J", "dst": "planck", "k": 2.0}
        ev_p = {"tau": "E", "src": "eV", "dst": "planck", "k": 1.602176634e-19 * 2.0}
        ok = egal([ev_j, j_p], [ev_p], declared=True)
        self.assertIsNone(ok["kill"])
        bad = egal(
            [{"tau": "B", "src": "G", "dst": "T", "k": 1e-4}],
            [{"tau": "B", "src": "G", "dst": "hl", "k": 0.282}],
            declared=True,
        )
        self.assertIsNotNone(bad["kill"])
        self.assertAlmostEqual(apply_chain(2.0, [ev_j]), 2.0 * 1.602176634e-19)

    def test_sigma_widens_theta(self) -> None:
        self.assertEqual(_verdict(0.02, theta=0.01, sigma=0.03), "S+")
        self.assertEqual(_verdict(0.02, theta=0.01, sigma=None), "P")

    def test_si_eps1_killed(self) -> None:
        with self.assertRaises(ValueError):
            parse_units({"packet": "si", "epsilon0": 1.0, "mu0": 1.0}, dimension="e*g")


if __name__ == "__main__":
    unittest.main(verbosity=2)
