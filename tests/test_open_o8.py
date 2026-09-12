#!/usr/bin/env python3
"""Contact ouvert O8 — T_c d'un gaz de Bose (condensat idéal).

Chronologie du gel :
1. Protocole écrit et gelé avant toute exécution : règle déclarée
   T_c = (2 pi hbar^2 / m kB) (n/2.612)^(2/3), masse 87Rb et n = 3e19
   m^-3 de la table ; θ = 0,10 figé avant run ; référence = T_c
   observée 170 nK. La référence ne participe jamais au calcul.
2. Premier run : mot = S+ (δ ≈ 5,01 %, tenu de justesse — zone P
   dès 10 %). Découvert, pas choisi.
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
AMU = 1.66053906660e-27


def _tc_nk(m_u: float, n_m3: float) -> float:
    m = m_u * AMU
    return (2.0 * math.pi * HBAR**2 / (m * K_B)) * (n_m3 / 2.612) ** (2.0 / 3.0) * 1e9


class TestOpenContactO8(unittest.TestCase):
    def row(self) -> dict:
        by = {r["id"]: r for r in run_registers()["rows"]}
        return by["O8_BEC_Tc"]

    def test_o8_word_frozen(self) -> None:
        r = self.row()
        self.assertEqual(r["verdict"], "S+")
        self.assertEqual(r["statut"], "ouverte")
        self.assertIsNone(r["expected"])
        self.assertLessEqual(r["delta"], r["theta"])  # 5,01 % ≤ 10 %
        self.assertAlmostEqual(r["mu_loc"], 178.5251927, places=5)

    def test_o8_anti_tautology_tc_never_in_calc(self) -> None:
        t = load_table("bec_tc_LITERATURE-2018.json")
        p = t["params"]
        tc = _tc_nk(float(p["mass_87Rb_u"]), float(p["n_cloud_m-3"]))
        self.assertAlmostEqual(tc, self.row()["mu_loc"], places=9)
        params_sans = {k: v for k, v in p.items() if k != "Tc_observed_nK"}
        self.assertNotIn("Tc_observed_nK", params_sans)
        self.assertAlmostEqual(
            _tc_nk(float(params_sans["mass_87Rb_u"]),
                   float(params_sans["n_cloud_m-3"])),
            tc, places=12,
        )

    def test_o8_lever_n_scaling(self) -> None:
        # Tc ∝ n^(2/3) : monotone, échelle exacte.
        args = (86.909187,)
        self.assertLess(_tc_nk(*args, 2.5e19), _tc_nk(*args, 3.0e19))
        self.assertAlmostEqual(_tc_nk(*args, 6.75e19),
                               _tc_nk(*args, 3.0e19) * (2.25) ** (2.0 / 3.0),
                               places=9)
        # Point de bascule P : δ = 10 % -> Tc = 187 nK -> n ≈ 3,52e19.
        n_p = 3e19 * (187.0 / _tc_nk(*args, 3.0e19)) ** 1.5
        self.assertGreater(n_p, 3.0e19)
        self.assertAlmostEqual(_tc_nk(*args, 3.0e19),
                               self.row()["mu_loc"], places=9)


if __name__ == "__main__":
    unittest.main(verbosity=2)
