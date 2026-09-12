#!/usr/bin/env python3
"""Contact ouvert O9 — moment dipolaire de H2O par échelle de Pauling.

Chronologie du gel :
1. Protocole écrit et gelé avant toute exécution : règle déclarée
   q = (chi_O - chi_H)/2,25 (e) ; mu = 2 q r cos(angle/2) ; géométrie
   et électronégativités de la table ; θ = 0,10 figé avant run ;
   référence = moment observé 1,8546 D. La référence ne participe
   jamais au calcul.
2. Premier run : mot = S- (δ ≈ 67,4 %). Découvert, pas choisi.
   Estimation pré-run manuscrite erronée (~11 %, conversion e·Å → D
   oubliée) : le run a révélé l'erreur — exactement la fonction d'un
   contact ouvert. L'échelle de Pauling brute surdéclare l'ionicité
   de l'eau ; la charge effective par liaison est ~0,34 e, pas 0,55 e.
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

E_A_TO_D = 4.80320427  # 1 e·Å en D, déclarée locale


def _mu_pauling(chi_o: float, chi_h: float, scale: float,
                r_oh_a: float, angle_deg: float) -> float:
    q = (chi_o - chi_h) / scale
    return 2.0 * q * r_oh_a * math.cos(math.radians(angle_deg) / 2.0) * E_A_TO_D


class TestOpenContactO9(unittest.TestCase):
    def row(self) -> dict:
        by = {r["id"]: r for r in run_registers()["rows"]}
        return by["O9_H2O_Pauling"]

    def test_o9_word_frozen(self) -> None:
        r = self.row()
        self.assertEqual(r["verdict"], "S-")  # mot du premier run, figé
        self.assertEqual(r["statut"], "ouverte")
        self.assertIsNone(r["expected"])
        self.assertGreater(r["delta"], 2.0 * r["theta"])  # 67,4 % > 20 %
        self.assertAlmostEqual(r["mu_loc"], 3.105069405, places=7)

    def test_o9_anti_tautology_mu_never_in_calc(self) -> None:
        t = load_table("h2o_pauling_LITERATURE-2018.json")
        p = t["params"]
        mu = _mu_pauling(float(p["chi_O"]), float(p["chi_H"]),
                         float(p["pauling_scale_eV"]),
                         float(p["r_OH_A"]), float(p["angle_deg"]))
        self.assertAlmostEqual(mu, self.row()["mu_loc"], places=9)
        params_sans = {k: v for k, v in p.items() if k != "mu_observed_D"}
        self.assertNotIn("mu_observed_D", params_sans)
        self.assertAlmostEqual(
            _mu_pauling(float(params_sans["chi_O"]), float(params_sans["chi_H"]),
                        float(params_sans["pauling_scale_eV"]),
                        float(params_sans["r_OH_A"]),
                        float(params_sans["angle_deg"])),
            mu, places=12,
        )

    def test_o9_lever_q_direction(self) -> None:
        # mu ∝ q : monotone ; la charge gelée (0,551 e) surdéclare.
        base = dict(chi_o=3.44, chi_h=2.20, scale=2.25, r_oh_a=0.958,
                    angle_deg=104.5)
        mu_ref = 1.8546
        self.assertLess(_mu_pauling(**{**base, "chi_h": 2.35}),
                        _mu_pauling(**base))  # moins d'écart -> moins de q
        # Charge effective compatible avec le dipôle observé :
        q_eff = mu_ref / (_mu_pauling(**base) / ((3.44 - 2.20) / 2.25))
        self.assertGreaterEqual(q_eff, 0.30)
        self.assertLessEqual(q_eff, 0.38)  # ~0,34 e, loin du 0,551 gelé
        self.assertAlmostEqual(_mu_pauling(**base),
                               self.row()["mu_loc"], places=9)


if __name__ == "__main__":
    unittest.main(verbosity=2)
