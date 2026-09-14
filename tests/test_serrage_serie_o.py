"""Campagne SERRAGE-1 — verrous figés (protocole gelé avant run).

Protocole : docs/SERRAGE-PROTOCOLE.md. La couleur du registre n'est pas
modifiée ; θ* et les étages sont des mesures dérivées consignées ici.
"""

from __future__ import annotations

import math
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT))

from campagnes_serrage_serie_o import (  # noqa: E402
    population_serie_o,
    run_serrage_serie_o,
    serrer_contact,
)

POPULATION_FIGEE = [
    "Landau_Vc_He4",
    "NMR_Karplus_Helix",
    "O10_PMMA_Carbonyl",
    "O11_BEC_Healing",
    "O13_CO2_Isotopologue",
    "O14_TK_Fenetre",
    "O15_H2_Harmonique",
    "O16_Cu_Gamma_Eff",
    "O7_Carbon_D_Levier",
    "O8_BEC_Tc",
    # 2026-09-14 : chantier PRINCIPES — PF2/PF3/PF4 rejoignent la
    # population (S+ a theta=0,1 sans budget GUM, meme regle figee)
    "PF2_Graviton_25THz",
    "PF3_Tau5_Jeu",
    "PF4_Vide_Catastrophe",
]


class TestSerrageSerieO(unittest.TestCase):
    def test_population_gelée(self):
        self.assertEqual(population_serie_o(), POPULATION_FIGEE)

    def test_monotonie_et_bascule_en_P(self):
        out = run_serrage_serie_o()
        self.assertEqual(out["n"], 13)  # 10 + PF2/PF3/PF4 (chantier PRINCIPES, 2026-09-14)
        for r in out["resultats"]:
            # monotonie de _adc : serrer un S+ passe par P, jamais S- direct
            self.assertEqual(r["verdict_bascule"], "P")
            self.assertEqual(r["regime"], "theta")
            # theta* est la frontière exacte S+->P
            self.assertEqual(r["theta_etoile"], r["delta"])
            # etages = floor(log2(thr_home / delta))
            self.assertEqual(
                r["etages"], math.floor(math.log2(r["thr_home"] / r["delta"]))
            )
            # trace : k=0 au seuil home, dernier palier = premier non-S+
            self.assertEqual(r["trace"][0]["thr"], r["thr_home"])
            self.assertEqual(r["trace"][0]["verdict"], "S+")
            self.assertNotEqual(r["trace"][-1]["verdict"], "S+")
            self.assertEqual(len(r["trace"]), r["etages"] + 2)

    def test_etages_connus_figés(self):
        attendus = {
            "O10_PMMA_Carbonyl": 3,
            "O11_BEC_Healing": 0,
            "O8_BEC_Tc": 0,
        }
        for cid, etages in attendus.items():
            self.assertEqual(serrer_contact(cid)["etages"], etages)


if __name__ == "__main__":
    unittest.main()
