"""Campagne SERRAGE-3 (remontée des S− de bord) — verrous figés."""

from __future__ import annotations

import math
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT))

from campagnes_remontee_bord import (  # noqa: E402
    population_s_moins_bord,
    remonter_contact,
    run_remontee_bord,
)

POPULATION_FIGEE = [
    "Bertsch_Xi_Unitary",
    "O12_Cu_Gamma",
    "O1_Grille_H1s",
    "O4_TK_ID_IG",
    "P21_H2O_dipole",
    "TR_Alpha_ProtonMuonNeuf",  # chantier TRANSVERSALE 2026-09-17 : S- a
    # 3,38 theta (premisse « 200 ») — rouge de bord, fenêtre [2, 4)
]


class TestRemonteeBord(unittest.TestCase):
    def test_population_gelée(self):
        self.assertEqual(population_s_moins_bord(), POPULATION_FIGEE)

    def test_fenetre_et_direction(self):
        out = run_remontee_bord()
        self.assertEqual(out["n"], 6)
        for r in out["resultats"]:
            self.assertEqual(r["regime"], "theta")
            # fenêtre [2, 4) : pos_rouge = log2(delta / (2 thr_home)) in [0,1)
            self.assertAlmostEqual(
                r["pos_rouge"], math.log2(r["delta"] / (2.0 * r["thr_home"]))
            )
            self.assertGreaterEqual(r["pos_rouge"], 0.0)
            self.assertLess(r["pos_rouge"], 1.0)
            # delta/2 < 2 thr partout sur la fenêtre : remontée à k = 1
            self.assertEqual(r["etages_remontee"], 1)
            self.assertEqual(r["verdict_remontee"], "P")
            # frontière exacte de remontée
            self.assertAlmostEqual(r["frontiere_remontee"], r["delta"] / 2.0)
            # trace : k=0 au seuil home (S-), dernier palier = P
            self.assertEqual(r["trace"][0]["thr"], r["thr_home"])
            self.assertEqual(r["trace"][0]["verdict"], "S-")
            self.assertEqual(r["trace"][-1]["verdict"], "P")
            self.assertEqual(len(r["trace"]), 2)

    def test_positions_connues_figées(self):
        attendus = {
            "Bertsch_Xi_Unitary": 0.141,
            "P21_H2O_dipole": 0.935,
        }
        for cid, pos in attendus.items():
            self.assertAlmostEqual(remonter_contact(cid)["pos_rouge"], pos, places=3)

    def test_refuse_un_non_S_moins(self):
        with self.assertRaises(ValueError):
            remonter_contact("O10_PMMA_Carbonyl")  # S+, pas S-


if __name__ == "__main__":
    unittest.main()
