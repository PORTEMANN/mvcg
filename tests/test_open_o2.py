#!/usr/bin/env python3
"""Contact ouvert O2 — ν₃(CO₂) par transfert de constante de force.

Chronologie du gel :
1. Protocole écrit et gelé avant toute exécution : règle déclarée
   k_r(C=O du CO₂) := k(CO) extraite de la bande CO de la table
   (modèle diatomique harmonique k = μω²) ; θ = 0,10 figé avant run
   (rationale : tolérance « entre labo » × modèle 1D grossier) ;
   référence = bande ν₃ observée du ¹²CO₂, 2349,3 cm⁻¹.
2. Premier run : mot = P (δ ≈ 14,48 %, zone 0,10 < δ ≤ 0,20).
   Découvert, pas choisi.
3. Ce test fixe le mot, comme pour tout contact du registre.

Anti-tautologie : la bande ν₃ du CO₂ ne doit JAMAIS entrer dans le
calcul — seule la bande CO pilote la constante de force transférée.
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

AMU = 1.66053906660e-27  # kg, déclarée locale (comme dans le runner)
C_CM = 2.99792458e10  # cm/s, exact


def _nu3_from_nu_co(nu_co_cm: float, m_c_amu: float = 12.0, m_o_amu: float = 16.0) -> float:
    """Recompute indépendant : k(CO) = μω², puis ν₃ = √(2k/m_O)/(2πc)."""
    m_c = m_c_amu * AMU
    m_o = m_o_amu * AMU
    mu = m_c * m_o / (m_c + m_o)
    omega = 2.0 * math.pi * C_CM * nu_co_cm
    k = mu * omega**2
    return math.sqrt(2.0 * k / m_o) / (2.0 * math.pi * C_CM)


class TestOpenContactO2(unittest.TestCase):
    def row(self) -> dict:
        by = {r["id"]: r for r in run_registers()["rows"]}
        return by["O2_CO2_nu3"]

    def test_o2_word_frozen(self) -> None:
        r = self.row()
        self.assertEqual(r["verdict"], "P")  # mot du premier run, figé
        self.assertEqual(r["statut"], "ouverte")
        self.assertIsNone(r["expected"])  # aucun mot attendu au gel
        self.assertGreater(r["delta"], r["theta"])  # 14,48 % > 10 %
        self.assertLessEqual(r["delta"], 2.0 * r["theta"])  # ... ≤ 20 %
        self.assertAlmostEqual(r["mu_loc"], 2009.2147805263908, places=6)

    def test_o2_anti_tautology_nu3_never_in_calc(self) -> None:
        # Recalcul indépendant depuis la table, bande CO seule :
        t = load_table("co2_bands_LITERATURE-2018.json")
        nu_co = float(t["bands"]["CO_nu01_cm-1"])
        nu3 = _nu3_from_nu_co(nu_co)
        self.assertAlmostEqual(nu3, self.row()["mu_loc"], places=9)
        # La bande cible ν₃ est à plus de 10 % (hors zone S+) :
        self.assertGreater(abs(nu3 / t["bands"]["CO2_nu3_cm-1"] - 1.0), 0.10)
        # Structurelle : retirer ν₃ (et l'isotopologue) ne change rien.
        bands_sans_nu3 = {k: v for k, v in t["bands"].items()
                          if "nu3" not in k}
        self.assertNotIn("CO2_nu3_cm-1", bands_sans_nu3)
        self.assertAlmostEqual(_nu3_from_nu_co(float(bands_sans_nu3["CO_nu01_cm-1"])),
                               nu3, places=12)

    def test_o2_lever_k_monotone(self) -> None:
        # Levier k<-autre-liaison : une constante déclarée plus forte
        # (bande CO plus haute) pousse ν₃ vers le haut, strictement.
        nu_low = _nu3_from_nu_co(2000.0)
        nu_mid = _nu3_from_nu_co(2170.2)
        nu_high = _nu3_from_nu_co(2350.0)
        self.assertLess(nu_low, nu_mid)
        self.assertLess(nu_mid, nu_high)
        self.assertAlmostEqual(nu_mid, self.row()["mu_loc"], places=9)


if __name__ == "__main__":
    unittest.main(verbosity=2)
