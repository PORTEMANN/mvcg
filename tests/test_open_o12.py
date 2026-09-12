#!/usr/bin/env python3
"""Contact ouvert O12 — chaleur spécifique électronique du cuivre.

Chronologie du gel :
1. Protocole écrit et gelé avant toute exécution : règle déclarée
   Sommerfeld avec MASSE LIBRE, gamma = pi^2 kB^2 n / (2 E_F),
   E_F = hbar^2 (3 pi^2 n)^(2/3) / (2 m_e) ; densité n = 8,47e28 m^-3
   de la table ; θ = 0,10 figé avant run ; référence = gamma mesuré
   du cuivre 96,6 J m^-3 K^-2. La référence ne participe jamais au
   calcul. Estimation pré-run honnête : le modèle à masse libre
   sous-estime gamma (~27 %) — le S- historique qui a révélé la
   masse effective en physique des solides.
2. Premier run : mot = S- (δ ≈ 26,8 %). Découvert, pas choisi.
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
EV = 1.602176634e-19


def _gamma_sommerfeld(n_m3: float, m_eff_over_me: float = 1.0) -> float:
    m = m_eff_over_me * M_E
    e_f = HBAR**2 * (3.0 * math.pi**2 * n_m3) ** (2.0 / 3.0) / (2.0 * m)
    return math.pi**2 * K_B**2 * n_m3 / (2.0 * e_f)


class TestOpenContactO12(unittest.TestCase):
    def row(self) -> dict:
        by = {r["id"]: r for r in run_registers()["rows"]}
        return by["O12_Cu_Gamma"]

    def test_o12_word_frozen(self) -> None:
        r = self.row()
        self.assertEqual(r["verdict"], "S-")  # mot du premier run, figé
        self.assertEqual(r["statut"], "ouverte")
        self.assertIsNone(r["expected"])
        self.assertGreater(r["delta"], 2.0 * r["theta"])  # 26,8 % > 20 %
        self.assertAlmostEqual(r["mu_loc"], 70.71042618, places=7)

    def test_o12_anti_tautology_gamma_never_in_calc(self) -> None:
        t = load_table("cu_gamma_LITERATURE-2018.json")
        p = t["params"]
        gamma = _gamma_sommerfeld(float(p["n_e_m-3"]))
        self.assertAlmostEqual(gamma, self.row()["mu_loc"], places=9)
        params_sans = {k: v for k, v in p.items() if k != "gamma_observed"}
        self.assertNotIn("gamma_observed", params_sans)
        self.assertAlmostEqual(_gamma_sommerfeld(float(params_sans["n_e_m-3"])),
                               gamma, places=12)

    def test_o12_lever_masse_effective(self) -> None:
        # gamma ∝ m_eff : le levier declare la masse effective.
        n = 8.47e28
        gamma_ref = 96.6
        m_star = gamma_ref / _gamma_sommerfeld(n)  # en unites de m_e
        self.assertGreaterEqual(m_star, 1.3)
        self.assertLessEqual(m_star, 1.45)  # ~1,37 m_e : litterature Cu
        # La masse libre gelée (1,0) est la dette du contact.
        self.assertAlmostEqual(_gamma_sommerfeld(n),
                               self.row()["mu_loc"], places=9)
        # E_F du modele reste la valeur textbook (~7 eV) :
        e_f_ev = HBAR**2 * (3.0 * math.pi**2 * n) ** (2.0 / 3.0) / (2.0 * M_E) / EV
        self.assertGreaterEqual(e_f_ev, 6.8)
        self.assertLessEqual(e_f_ev, 7.3)


if __name__ == "__main__":
    unittest.main(verbosity=2)
