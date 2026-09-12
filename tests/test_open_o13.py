#!/usr/bin/env python3
"""Contact ouvert O13 — bande ν₃ du 13CO2 par la loi des masses.

Chronologie du gel :
1. Protocole écrit et gelé avant toute exécution : règle déclarée —
   isotopologue plus lourd, fréquence réduite par la masse réduite,
   nu(13) = nu(12)·√(μ12/μ13), μ = m_C·m_O/(m_C+m_O), masses
   conventionnelles 12/16 et 13/16 ; la bande cible du 13CO2
   (2273,7 cm⁻¹) NE DOIT JAMAIS entrer dans le calcul ; θ = 0,10 figé
   avant run ; référence = bande observée du 13CO2. La référence ne
   participe jamais au calcul. Estimation pré-run honnête : écart ~1 %.
2. Premier run : mot = S+ (δ ≈ 1,03 %). Découvert, pas choisi.
3. Ce test fixe le mot, comme pour tout contact du registre.
"""

from __future__ import annotations

import math
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from mvcg.registers import run_registers  # noqa: E402
from mvcg.tables import load_table  # noqa: E402


def _nu13(nu12: float) -> float:
    mu12 = 12.0 * 16.0 / (12.0 + 16.0)
    mu13 = 13.0 * 16.0 / (13.0 + 16.0)
    return nu12 * math.sqrt(mu12 / mu13)


class TestOpenContactO13(unittest.TestCase):
    def row(self) -> dict:
        by = {r["id"]: r for r in run_registers()["rows"]}
        return by["O13_CO2_Isotopologue"]

    def test_o13_word_frozen(self) -> None:
        r = self.row()
        self.assertEqual(r["verdict"], "S+")  # mot du premier run, figé
        self.assertEqual(r["statut"], "ouverte")
        self.assertIsNone(r["expected"])
        self.assertLess(r["delta"], r["theta"])  # 1,03 % < 10 %
        self.assertAlmostEqual(r["mu_loc"], 2297.086814010063, places=9)

    def test_o13_anti_tautology_cible_jamais_dans_calc(self) -> None:
        t = load_table("co2_bands_LITERATURE-2018.json")
        bands = t["bands"]
        nu12 = float(bands["CO2_nu3_cm-1"])
        self.assertAlmostEqual(_nu13(nu12), self.row()["mu_loc"], places=9)
        # La bande cible du 13CO2 est stockée dans la table (c'est la
        # référence) mais hors du calcul : retirée, rien ne change.
        self.assertIn("CO2_nu3_13C_cm-1", bands)
        sans_cible = {k: v for k, v in bands.items()
                      if k != "CO2_nu3_13C_cm-1"}
        self.assertAlmostEqual(_nu13(float(sans_cible["CO2_nu3_cm-1"])),
                               self.row()["mu_loc"], places=12)

    def test_o13_lever_anharmonicite(self) -> None:
        # Le levier déclaré est k←anharmonicité : la loi des masses
        # suppose la constante de force inchangée entre isotopologues.
        # L'écart résiduel (~1 %) est la dette anharmonique, en dessous
        # du θ du contact — c'est ce qui fait le S+.
        self.assertAlmostEqual(_nu13(2349.3), 2297.086814010063, places=9)
        self.assertGreater(self.row()["delta"], 0.005)  # dette réelle, pas zéro
        self.assertLess(self.row()["delta"], 0.02)


if __name__ == "__main__":
    unittest.main(verbosity=2)
