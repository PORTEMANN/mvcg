#!/usr/bin/env python3
"""Contact ouvert O16 — levier d'O12 activé : la masse effective.

Chronologie du gel :
1. Protocole écrit et gelé avant toute exécution : règle déclarée —
   même modèle de Sommerfeld qu'O12 (gamma = pi^2 k_B^2 n / (2 E_F)),
   même densité n = 8,47e28 m^-3, mais la masse déclarée est la masse
   effective de bande m* = 1,38 m_e (valeur des solides,
   Ashcroft-Mermin), JAMAIS dérivée de la référence — gamma_ref /
   gamma_modèle = 1,37 serait circulaire : la référence entrerait
   dans le calcul. La mesure du cuivre (96,6) NE DOIT JAMAIS entrer
   dans le calcul ; θ = 0,10 figé avant run. Estimation pré-run
   honnête : δ ≈ 1 % — suspense faible assumé au gel : c'est le
   pendant disciplinaire d'O7 (chaque échec a son levier activé,
   θ jamais déplacé).
2. Premier run : mot = S+ (δ ≈ 1,01 %). Découvert, pas choisi.
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

HBAR = 1.054571817e-34
K_B = 1.380649e-23
M_E = 9.1093837015e-31  # kg, déclarée locale
M_STAR_OVER_ME = 1.38  # déclarée (bande), pas calculée depuis gamma_ref


def _gamma_sommerfeld(n_m3: float, m_over_me: float) -> float:
    m = m_over_me * M_E
    e_f = HBAR**2 * (3.0 * math.pi**2 * n_m3) ** (2.0 / 3.0) / (2.0 * m)
    return math.pi**2 * K_B**2 * n_m3 / (2.0 * e_f)


class TestOpenContactO16(unittest.TestCase):
    def row(self) -> dict:
        by = {r["id"]: r for r in run_registers()["rows"]}
        return by["O16_Cu_Gamma_Eff"]

    def test_o16_word_frozen(self) -> None:
        r = self.row()
        self.assertEqual(r["verdict"], "S+")  # mot du premier run, figé
        self.assertEqual(r["statut"], "ouverte")
        self.assertIsNone(r["expected"])
        self.assertLess(r["delta"], r["theta"])  # 1,01 % < 10 %
        self.assertAlmostEqual(r["mu_loc"], 97.58038812719737, places=9)

    def test_o16_anti_tautology_masse_jamais_derivee(self) -> None:
        # La référence gamma_observed est dans la table mais hors du
        # calcul : retirée, la masse déclarée 1,38 ne bouge pas.
        # Le geste circulaire (m* = gamma_ref / gamma(m_e)) est
        # explicitement interdit par le protocole — la valeur 1,37
        # qu'il produirait est un AUTRE nombre que le 1,38 déclaré.
        t = load_table("cu_gamma_LITERATURE-2018.json")
        p = t["params"]
        gamma_obs = float(p["gamma_observed"])
        circulaire = gamma_obs / _gamma_sommerfeld(8.47e28, 1.0)
        self.assertAlmostEqual(circulaire, 1.37, delta=0.005)
        self.assertNotAlmostEqual(circulaire, M_STAR_OVER_ME, places=2)
        # La masse déclarée est indépendante de la référence :
        params_sans = {k: v for k, v in p.items() if k != "gamma_observed"}
        self.assertAlmostEqual(
            _gamma_sommerfeld(float(params_sans["n_e_m-3"]),
                              M_STAR_OVER_ME),
            self.row()["mu_loc"], places=9)

    def test_o16_levier_pendant_d_o7(self) -> None:
        # gamma ∝ m exactement : le levier d'O12 est un simple facteur.
        # O12 (masse libre) × 1,38 = O16 — la dette d'O12 (26,8 %)
        # devient l'écart résiduel d'O16 (1,0 %). Le levier réparé
        # laisse une dette de 1 % : la masse de bande 1,38 n'est pas
        # exactement la masse thermodynamique 1,37 — la machine le dit.
        by = {r["id"]: r for r in run_registers()["rows"]}
        gamma_libre = by["O12_Cu_Gamma"]["mu_loc"]
        self.assertAlmostEqual(gamma_libre * 1.38,
                               self.row()["mu_loc"], places=9)
        self.assertGreater(self.row()["delta"], 0.005)  # dette réelle
        self.assertLess(self.row()["delta"], 0.02)


if __name__ == "__main__":
    unittest.main(verbosity=2)
