#!/usr/bin/env python3
"""Contact ouvert O11 — longueur de guérison du condensat de Bose.

Chronologie du gel :
1. Protocole écrit et gelé avant toute exécution : règle déclarée
   xi = 1/sqrt(8 pi n a_s), n = 3e19 m^-3 et a_s = 100 a0 (même nuage
   déclaré qu'O5) ; θ = 0,10 figé avant run ; référence = taille
   observée 0,55 um (fourchette usuelle 0,5-1 um, valeur médiane
   déclarée). La référence ne participe jamais au calcul.
2. Premier run : mot = S+ (δ ≈ 8,98 %). Découvert, pas choisi.
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


def _xi_um(n_m3: float, a_s_nm: float) -> float:
    return 1.0 / math.sqrt(8.0 * math.pi * n_m3 * a_s_nm * 1e-9) * 1e6


class TestOpenContactO11(unittest.TestCase):
    def row(self) -> dict:
        by = {r["id"]: r for r in run_registers()["rows"]}
        return by["O11_BEC_Healing"]

    def test_o11_word_frozen(self) -> None:
        r = self.row()
        self.assertEqual(r["verdict"], "S+")
        self.assertEqual(r["statut"], "ouverte")
        self.assertIsNone(r["expected"])
        self.assertLessEqual(r["delta"], r["theta"])  # 8,98 % ≤ 10 %
        self.assertAlmostEqual(r["mu_loc"], 0.5006323169, places=8)

    def test_o11_anti_tautology_xi_never_in_calc(self) -> None:
        t = load_table("bec_healing_LITERATURE-2018.json")
        p = t["params"]
        xi = _xi_um(float(p["n_cloud_m-3"]), float(p["a_s_100a0_nm"]))
        self.assertAlmostEqual(xi, self.row()["mu_loc"], places=12)
        params_sans = {k: v for k, v in p.items() if k != "xi_observed_um"}
        self.assertNotIn("xi_observed_um", params_sans)
        self.assertAlmostEqual(
            _xi_um(float(params_sans["n_cloud_m-3"]),
                   float(params_sans["a_s_100a0_nm"])),
            xi, places=12,
        )

    def test_o11_lever_scaling(self) -> None:
        # xi ∝ 1/sqrt(n a_s) : monotone decroissante en chacun.
        self.assertGreater(_xi_um(2.5e19, 5.291772), _xi_um(3.0e19, 5.291772))
        self.assertGreater(_xi_um(3.0e19, 5.291772), _xi_um(3.0e19, 6.0))
        self.assertAlmostEqual(_xi_um(1.2e20, 5.291772),
                               _xi_um(3.0e19, 5.291772) / 2.0, places=12)
        # Point de bascule P : xi = 0,495 um (δ = 10 %) -> n ≈ 3,08e19.
        n_p = 3e19 * (_xi_um(3.0e19, 5.291772) / 0.495) ** 2
        self.assertGreater(n_p, 3.0e19)
        self.assertAlmostEqual(_xi_um(3.0e19, 5.291772),
                               self.row()["mu_loc"], places=12)


if __name__ == "__main__":
    unittest.main(verbosity=2)
