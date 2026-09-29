#!/usr/bin/env python3
"""Contacts ouverts W-DE — équation d'état de l'énergie noire (run).

Chronologie du gel :
1. Protocole W-DE FERMÉ (2026-09-30) avant toute lecture du mot :
   quatre tables gelées depuis DESI DR2 (arXiv:2503.14738v3, eq. 26-28
   et §VII.1) et le compagnon (arXiv:2503.14743v2) ; ligne θ pauvre
   (k = 2) choisie par le propriétaire ; mu_ref = 0 (ΛCDM).
2. Premier run : PP P à 1,4 θ ; U3 P à 1,9 θ ; DESY5 S− à 2,1 θ ;
   FREE P à 1,5 θ (plancher). Mots découverts, pas choisis.
3. Ce test fixe les mots, comme pour tout contact du registre.
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from mvcg.registers import run_registers  # noqa: E402
from mvcg.tables import load_table  # noqa: E402


def _row(cid: str) -> dict:
    return {r["id"]: r for r in run_registers()["rows"]}[cid]


class TestWDE(unittest.TestCase):
    def test_mots_figes(self) -> None:
        self.assertEqual(_row("WDE_PantheonPlus")["verdict"], "P")
        self.assertEqual(_row("WDE_Union3")["verdict"], "P")
        self.assertEqual(_row("WDE_DESY5")["verdict"], "S-")
        self.assertEqual(_row("WDE_FREE")["verdict"], "P")

    def test_mu_figes(self) -> None:
        self.assertAlmostEqual(_row("WDE_PantheonPlus")["mu_loc"], 2.8)
        self.assertAlmostEqual(_row("WDE_Union3")["mu_loc"], 3.8)
        self.assertAlmostEqual(_row("WDE_DESY5")["mu_loc"], 4.2)
        self.assertAlmostEqual(_row("WDE_FREE")["mu_loc"], 3.0)
        for cid in ("WDE_PantheonPlus", "WDE_Union3", "WDE_DESY5", "WDE_FREE"):
            self.assertAlmostEqual(_row(cid)["theta"], 2.0)
            self.assertAlmostEqual(_row(cid)["mu_ref"], 0.0)

    def test_gel_desi_dr2(self) -> None:
        # les valeurs gelées sont celles de la publication DESI DR2
        # (arXiv:2503.14738v3), pas des recalculs
        pp = load_table("wde_pp_LITTERATURE-2025.json")["params"]
        self.assertAlmostEqual(pp["w0"], -0.838)
        self.assertAlmostEqual(pp["wa"], -0.62)
        self.assertAlmostEqual(pp["sigma_comb"], 2.8)
        y5 = load_table("wde_y5_LITTERATURE-2025.json")["params"]
        self.assertAlmostEqual(y5["w0"], -0.752)
        self.assertAlmostEqual(y5["wa"], -0.86)
        self.assertAlmostEqual(y5["sigma_comb"], 4.2)
        free = load_table("wde_free_LITTERATURE-2025.json")["params"]
        self.assertAlmostEqual(free["sigma_lowest_bin"], 3.0)
        # la borne est un plancher, pas une mesure
        self.assertIn("PLANCHER", free["sigma_lowest_bin_semantique"])

    def test_pas_de_pli_cpl(self) -> None:
        # I-D7 : FREE cohérent avec Y5 — la dynamique n'est pas un pli
        # de paramétrisation (FREE est P, Y5 est S-, jamais S+ isolé)
        self.assertNotEqual(_row("WDE_FREE")["verdict"], "S+")
        self.assertEqual(_row("WDE_DESY5")["verdict"], "S-")


if __name__ == "__main__":
    unittest.main(verbosity=2)
