#!/usr/bin/env python3
"""Campagne SERRAGE-PF — verrous figés (protocole dérivé, pas de contact).

La couleur du registre n'est pas modifiée ; ce test fige les mesures
dérivées de la campagne de balayage θ du corpus PRINCIPES.
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT))

from campagnes_serrage_pf import (  # noqa: E402
    population_pf,
    run_serrage_pf,
)

POPULATION_FIGEE = [
    "PF1_RG_Unification",
    "PF1b_RG_Unification_2Loop",
    "PF2_Graviton_25THz",
    "PF3_Tau5_Jeu",
    "PF4_Vide_Catastrophe",
    "PF5_Psy_Energie",
    "PF6_RMN_DeltaB",
    "PF7_F4_Recompute",
    "PF8_Hz_Filtrage_Ecart",
]


class TestSerragePF(unittest.TestCase):
    def test_population_gelée(self):
        self.assertEqual(population_pf(), POPULATION_FIGEE)

    def test_n_et_mot_domicile(self):
        out = run_serrage_pf()
        self.assertEqual(out["n"], 9)
        by = {r["id"]: r for r in out["resultats"]}
        for cid, mot in (("PF1_RG_Unification", "S-"),
                         ("PF1b_RG_Unification_2Loop", "S-"),
                         ("PF2_Graviton_25THz", "S+"),
                         ("PF3_Tau5_Jeu", "S+"),
                         ("PF4_Vide_Catastrophe", "S+"),
                         ("PF5_Psy_Energie", "S-"),
                         ("PF6_RMN_DeltaB", "S-"),
                         ("PF7_F4_Recompute", "S+"),
                         ("PF8_Hz_Filtrage_Ecart", "S-")):
            self.assertEqual(by[cid]["verdict_home"], mot, cid)

    def test_theta_etoile_gelé(self):
        # frontière exacte S+↔P (θ* = δ en régime θ)
        out = run_serrage_pf()
        by = {r["id"]: r for r in out["resultats"]}
        self.assertAlmostEqual(by["PF7_F4_Recompute"]["theta_etoile"],
                               0.00458225180960059, delta=1e-14)
        self.assertAlmostEqual(by["PF3_Tau5_Jeu"]["theta_etoile"],
                               0.01052855882826187, delta=1e-14)
        self.assertAlmostEqual(by["PF4_Vide_Catastrophe"]["theta_etoile"],
                               0.007749953822161482, delta=1e-14)
        self.assertAlmostEqual(by["PF2_Graviton_25THz"]["theta_etoile"],
                               0.03391692423096471, delta=1e-14)

    def test_bascules_de_la_grille(self):
        # la machine apprend de ses verdicts : où le vert devient ambre
        out = run_serrage_pf()
        by = {r["id"]: r for r in out["resultats"]}
        sw = {r["id"]: {s["theta"]: s["verdict"] for s in r["sweep"]}
              for r in out["resultats"]}
        # PF7 : S+ sur toute la grille (δ = 0,46 % < θ_min = 0,5 %)
        for th in out["theta_grid"]:
            self.assertEqual(sw["PF7_F4_Recompute"][th], "S+")
        # PF4 : P à θ = 0,005 (premier basculement de la grille)
        self.assertEqual(sw["PF4_Vide_Catastrophe"][0.005], "P")
        self.assertEqual(sw["PF4_Vide_Catastrophe"][0.01], "S+")
        # PF3 : P à θ = 0,01
        self.assertEqual(sw["PF3_Tau5_Jeu"][0.01], "P")
        self.assertEqual(sw["PF3_Tau5_Jeu"][0.02], "S+")
        # PF2 : P à θ = 0,02
        self.assertEqual(sw["PF2_Graviton_25THz"][0.02], "P")
        self.assertEqual(sw["PF2_Graviton_25THz"][0.05], "S+")
        # les 5 S− sont invariants sur toute la grille (marge ≥ 9 θ)
        for cid in ("PF1_RG_Unification", "PF1b_RG_Unification_2Loop",
                    "PF5_Psy_Energie", "PF6_RMN_DeltaB",
                    "PF8_Hz_Filtrage_Ecart"):
            for th in out["theta_grid"]:
                self.assertEqual(sw[cid][th], "S-", f"{cid}@{th}")
        # θ de relâchement (frontière P↔S−) hors grille pour tous les S−
        for cid in ("PF1_RG_Unification", "PF1b_RG_Unification_2Loop",
                    "PF5_Psy_Energie", "PF6_RMN_DeltaB",
                    "PF8_Hz_Filtrage_Ecart"):
            self.assertGreater(by[cid]["theta_relachement"],
                               max(out["theta_grid"]), cid)


if __name__ == "__main__":
    unittest.main()
