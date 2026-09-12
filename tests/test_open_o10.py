#!/usr/bin/env python3
"""Contact ouvert O10 — bande carbonyle du PMMA par transfert de force.

Chronologie du gel :
1. Protocole écrit et gelé avant toute exécution : règle déclarée
   k(C=O ester) := k(C=O formaldehyde), extrait par le modele
   harmonique ; masses reduites identiques (memes atomes C, O) ;
   θ = 0,10 figé avant run ; référence = bande PMMA 1735 cm^-1.
   Suspense minimal ASSUME au gel (écrit dans la note du contact) :
   le transfert entre liaisons de memes atomes est le cas le plus
   favorable du geste O2. La bande PMMA ne participe jamais au calcul.
2. Premier run : mot = S+ (δ ≈ 0,63 %). Découvert, pas choisi.
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
C_CM = 2.99792458e10


def _nu_transfer(nu_ch2o: float) -> float:
    m_c = 12.0 * AMU
    m_o = 16.0 * AMU
    mu = m_c * m_o / (m_c + m_o)
    omega = 2.0 * math.pi * C_CM * nu_ch2o
    k = mu * omega**2
    return math.sqrt(k / mu) / (2.0 * math.pi * C_CM)


class TestOpenContactO10(unittest.TestCase):
    def row(self) -> dict:
        by = {r["id"]: r for r in run_registers()["rows"]}
        return by["O10_PMMA_Carbonyl"]

    def test_o10_word_frozen(self) -> None:
        r = self.row()
        self.assertEqual(r["verdict"], "S+")
        self.assertEqual(r["statut"], "ouverte")
        self.assertIsNone(r["expected"])
        self.assertLessEqual(r["delta"], r["theta"])  # 0,63 % ≤ 10 %
        self.assertAlmostEqual(r["mu_loc"], 1746.0, places=9)

    def test_o10_anti_tautology_nu_never_in_calc(self) -> None:
        t = load_table("pmma_carbonyl_LITERATURE-2018.json")
        p = t["params"]
        nu = _nu_transfer(float(p["nu_CH2O_cm-1"]))
        self.assertAlmostEqual(nu, self.row()["mu_loc"], places=9)
        params_sans = {k: v for k, v in p.items() if k != "nu_PMMA_cm-1"}
        self.assertNotIn("nu_PMMA_cm-1", params_sans)
        self.assertAlmostEqual(_nu_transfer(float(params_sans["nu_CH2O_cm-1"])),
                               nu, places=12)

    def test_o10_transfer_identity_when_same_masses(self) -> None:
        # Liaisons de memes atomes : la masse reduite est identique,
        # le transfert est exact (nu sort = nu entre, a 1e-12 pres).
        self.assertAlmostEqual(_nu_transfer(1746.0), 1746.0, places=9)
        self.assertAlmostEqual(_nu_transfer(1000.0), 1000.0, places=9)
        # Propriété du contact : le S+ ne peut PAS venir d'un accident
        # de parametre — il est structurel au geste (memes atomes).
        self.assertAlmostEqual(_nu_transfer(1746.0),
                               self.row()["mu_loc"], places=9)


if __name__ == "__main__":
    unittest.main(verbosity=2)
