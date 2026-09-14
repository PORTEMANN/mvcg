"""Campagne SERRAGE-2 (détente des P) — verrous figés."""

from __future__ import annotations

import math
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT))

from campagnes_detente_serie_o import (  # noqa: E402
    detendre_contact,
    population_p_sans_gum,
    run_detente_serie_o,
)

POPULATION_FIGEE = [
    "NMR_Karplus_Helix_VogeliBax2007",
    "NMR_Karplus_Sheet",
    "NMR_Karplus_Sheet_VogeliBax2007",
    "O2_CO2_nu3",
    "O3_Carbon_D_Raman",
]


class TestDetenteSerieO(unittest.TestCase):
    def test_population_gelée(self):
        self.assertEqual(population_p_sans_gum(), POPULATION_FIGEE)

    def test_tous_basculent_au_premier_palier(self):
        out = run_detente_serie_o()
        self.assertEqual(out["n"], 5)
        for r in out["resultats"]:
            self.assertEqual(r["regime"], "theta")
            # pos_bande = log2(delta / thr_home), dans [0, 1] pour un P
            self.assertAlmostEqual(
                r["pos_bande"], math.log2(r["delta"] / r["thr_home"])
            )
            self.assertGreaterEqual(r["pos_bande"], 0.0)
            self.assertLessEqual(r["pos_bande"], 1.0)
            # cette population : delta/thr_home < 2 -> détente à k = 1
            self.assertEqual(r["etages_detente"], 1)
            # trace : k=0 au seuil home (P), dernier palier = S+
            self.assertEqual(r["trace"][0]["thr"], r["thr_home"])
            self.assertEqual(r["trace"][0]["verdict"], "P")
            self.assertEqual(r["trace"][-1]["verdict"], "S+")
            self.assertEqual(len(r["trace"]), 2)

    def test_positions_connues_figées(self):
        attendus = {
            "O2_CO2_nu3": 0.534,
            "NMR_Karplus_Helix_VogeliBax2007": 0.902,
        }
        for cid, pos in attendus.items():
            self.assertAlmostEqual(detendre_contact(cid)["pos_bande"], pos, places=3)

    def test_refuse_un_non_P(self):
        with self.assertRaises(ValueError):
            detendre_contact("O10_PMMA_Carbonyl")  # S+, pas P


if __name__ == "__main__":
    unittest.main()
