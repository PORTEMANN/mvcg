#!/usr/bin/env python3
"""Contact ouvert O4 — I_D/I_G par la loi de Tuinstra–Koenig.

Chronologie du gel :
1. Protocole écrit et gelé avant toute exécution : table vintage
   (carbon_disorder_LITERATURE-2018) ; règle déclarée — phase 1 :
   I_D/I_G = C(λ)/L_a, C(514 nm) = 4,4 nm (constante empirique de la
   table), L_a = 3,0 nm (domaine déclaré, fenêtre de validité) ;
   θ = 0,10 figé avant run (répétabilité inter-labo d'un rapport
   d'intensités Raman) ; référence = I_D/I_G observé de l'échantillon,
   1,2. Anti-tautologie : le rapport observé ne participe jamais au
   calcul — seuls C et L_a pilotent la prédiction.
2. Premier run : mot = S− (δ ≈ 22,22 % > 2θ). Découvert, pas choisi.
3. Ce test fixe le mot, comme pour tout contact du registre.

Le levier La<-recalibrer : μ ∝ 1/L_a — monotone décroissante ; la
constante empirique C a une dispersion documentée selon les
échantillons.
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from mvcg.registers import run_registers  # noqa: E402
from mvcg.tables import load_table  # noqa: E402


def _tk_pred(c_nm: float, la_nm: float) -> float:
    return c_nm / la_nm


class TestOpenContactO4(unittest.TestCase):
    def row(self) -> dict:
        by = {r["id"]: r for r in run_registers()["rows"]}
        return by["O4_TK_ID_IG"]

    def test_o4_word_frozen(self) -> None:
        r = self.row()
        self.assertEqual(r["verdict"], "S-")  # mot du premier run, figé
        self.assertEqual(r["statut"], "ouverte")
        self.assertIsNone(r["expected"])  # aucun mot attendu au gel
        self.assertGreater(r["delta"], 2.0 * r["theta"])  # 22,22 % > 20 %
        self.assertAlmostEqual(r["mu_loc"], 1.4666666666666668, places=12)

    def test_o4_anti_tautology_observed_never_in_calc(self) -> None:
        t = load_table("carbon_disorder_LITERATURE-2018.json")
        p = t["params"]
        pred = _tk_pred(float(p["TK_C_lambda514_nm"]), float(p["La_observed_nm"]))
        self.assertAlmostEqual(pred, self.row()["mu_loc"], places=12)
        # Le rapport observé est à plus de 20 % (hors zone P) :
        self.assertGreater(abs(pred / p["ID_IG_observed"] - 1.0), 0.20)
        # Structurelle : retirer le rapport observé ne change rien.
        params_sans_obs = {k: v for k, v in p.items() if k != "ID_IG_observed"}
        self.assertNotIn("ID_IG_observed", params_sans_obs)
        self.assertAlmostEqual(
            _tk_pred(float(params_sans_obs["TK_C_lambda514_nm"]),
                     float(params_sans_obs["La_observed_nm"])),
            pred, places=12,
        )

    def test_o4_lever_la_recalibrer(self) -> None:
        # μ ∝ 1/La : monotone décroissante ; croissante en C.
        self.assertLess(_tk_pred(4.4, 3.5), _tk_pred(4.4, 3.0))
        self.assertLess(_tk_pred(4.4, 3.0), _tk_pred(4.4, 2.5))
        self.assertGreater(_tk_pred(5.0, 3.0), _tk_pred(4.4, 3.0))
        # Points de bascule documentés : vers P (δ = 20 %) puis vers S+.
        la_p = 4.4 / 1.44   # mu = 1,44
        la_sp = 4.4 / 1.2   # mu = 1,2
        self.assertAlmostEqual(_tk_pred(4.4, la_p), 1.44, places=12)
        self.assertAlmostEqual(_tk_pred(4.4, la_sp), 1.2, places=12)
        self.assertGreater(la_p, 3.0)  # il faut agrandir La de ~2 %
        self.assertAlmostEqual(_tk_pred(4.4, 3.0), self.row()["mu_loc"], places=12)


if __name__ == "__main__":
    unittest.main(verbosity=2)
