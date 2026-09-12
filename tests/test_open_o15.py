#!/usr/bin/env python3
"""Contact ouvert O15 — constante harmonique du H2 par force déclarée.

Chronologie du gel :
1. Protocole écrit et gelé avant toute exécution : règle déclarée —
   oscillateur harmonique, nu_harm = √(k/μ)/(2πc), k = 510 N/m
   (constante de force de Morse au minimum, valeur usuelle déclarée),
   μ = m_H/2 ; comparaison HONNÊTE contre ω_e = 4401,2 cm⁻¹
   (constante harmonique expérimentale), PAS contre le fondamental
   anharmonique (4160) ; la cible ω_e NE DOIT JAMAIS entrer dans le
   calcul ; θ = 0,10 figé avant run ; référence = ω_e mesurée.
   Estimation pré-run honnête : l'harmonique pur sous-estime ω_e
   d'environ 6 % — la dette anharmonique attendue.
2. Premier run : mot = S+ (δ ≈ 5,8 %). Découvert, pas choisi.
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

AMU = 1.66053906660e-27
C_CM = 2.99792458e10  # c en cm/s


def _nu_harm(k_npm: float, m_h_amu: float = 1.007825) -> float:
    mu = m_h_amu * AMU / 2.0
    return math.sqrt(k_npm / mu) / (2.0 * math.pi * C_CM)


class TestOpenContactO15(unittest.TestCase):
    def row(self) -> dict:
        by = {r["id"]: r for r in run_registers()["rows"]}
        return by["O15_H2_Harmonique"]

    def test_o15_word_frozen(self) -> None:
        r = self.row()
        self.assertEqual(r["verdict"], "S+")  # mot du premier run, figé
        self.assertEqual(r["statut"], "ouverte")
        self.assertIsNone(r["expected"])
        self.assertLess(r["delta"], r["theta"])  # 5,8 % < 10 %
        self.assertAlmostEqual(r["mu_loc"], 4144.597896599118, places=9)

    def test_o15_anti_tautology_omega_e_jamais_dans_calc(self) -> None:
        t = load_table("h2_vibration_LITERATURE-2018.json")
        p = t["params"]
        nu = _nu_harm(float(p["k_H2_N_per_m"]))
        self.assertAlmostEqual(nu, self.row()["mu_loc"], places=9)
        # Sans ω_e, le calcul ne change pas :
        params_sans = {k: v for k, v in p.items() if k != "omega_e_cm-1"}
        self.assertAlmostEqual(
            _nu_harm(float(params_sans["k_H2_N_per_m"])),
            nu, places=12)

    def test_o15_honnetete_comparaison_vs_omega_e(self) -> None:
        # Le contrat d'honnêteté : comparer l'harmonique pur à ω_e
        # (constante harmonique expérimentale), jamais au fondamental
        # anharmonique 4160 — qui ferait l'écart paraître plus petit
        # qu'il n'est (~0,4 % au lieu de 5,8 %). La table porte les
        # deux valeurs ; seule ω_e est la référence du contact.
        t = load_table("h2_vibration_LITERATURE-2018.json")
        p = t["params"]
        omega_e = float(p["omega_e_cm-1"])
        nu0 = 4160.0  # fondamental anharmonique, porté par la note de la table
        self.assertAlmostEqual(omega_e, 4401.2, places=6)
        delta_honnete = abs(self.row()["mu_loc"] - omega_e) / omega_e
        delta_malin = abs(self.row()["mu_loc"] - nu0) / nu0
        self.assertAlmostEqual(delta_honnete, self.row()["delta"], places=9)
        self.assertGreater(delta_honnete, 10.0 * delta_malin)
        # La dette anharmonique est réelle et déclarée : ~6 %.
        self.assertGreater(self.row()["delta"], 0.05)
        self.assertLess(self.row()["delta"], 0.07)


if __name__ == "__main__":
    unittest.main(verbosity=2)
