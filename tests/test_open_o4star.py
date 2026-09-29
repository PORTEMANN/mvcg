#!/usr/bin/env python3
"""Contact ouvert O4star — loi de Tuinstra–Koenig au point dual.

Chronologie du gel :
1. Protocole écrit et gelé avant toute exécution (TK-DUAL-GELE-
   2026-09-27, MVC-G ext v0.5) : règle déclarée — I_D/I_G = C(λ)/L★
   avec C = 4,4 nm (même constante qu'O4/O14) et L★ = sqrt(3×10) =
   5,477226 nm (point fixe de l'involution φ(L) = 30/L) ; θ = 0,10
   figé (même que O4/O14) ; la référence est la valeur textbook
   DÉCLARÉE par le corpus (2026-09-29) = interpolation géométrique des
   ratios observés des deux ancres (1,2 et 0,45) = 0,7348469, u = 0,15
   déclarée (scatter documenté Knight & White 1989 Fig. 4, r² = 0,84).
   La valeur déclarée NE DOIT JAMAIS entrer dans le calcul (seuls C et
   L★ pilotent la prédiction — anti-tautologie, comme O4/O14).
2. Premier run : mot = S+ (δ ≈ 9,3 %, r = 0,93 θ). Découvert, pas
   choisi. Lecture R5 du protocole : r ≤ 1,05 → classe convexe
   (pôle 1/L — sa prédiction était 0,928, le run donne 0,932).
3. Ce test fixe le mot, comme pour tout contact du registre.
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from mvcg.registers import run_registers  # noqa: E402
from mvcg.tables import load_table  # noqa: E402

L_STAR = 3.0 ** 0.5 * 10.0 ** 0.5  # sqrt(30) = 5.477225575051661


class TestOpenContactO4star(unittest.TestCase):
    def row(self) -> dict:
        by = {r["id"]: r for r in run_registers()["rows"]}
        return by["O4star_TK_Dual"]

    def test_o4star_word_frozen(self) -> None:
        r = self.row()
        self.assertEqual(r["verdict"], "S+")  # mot du premier run, figé
        self.assertEqual(r["statut"], "ouverte")
        self.assertIsNone(r["expected"])
        self.assertLess(r["delta"], r["theta"])  # 9,3 % < 10 %
        self.assertAlmostEqual(r["mu_loc"], 0.8033264176742437, places=12)
        self.assertAlmostEqual(r["delta"], 0.09318878899989724, places=12)
        # r ≤ 1,05 → classe convexe (pôle 1/L) du protocole TK-DUAL
        self.assertLessEqual(r["delta"] / r["theta"], 1.05)

    def test_o4star_anti_tautology_declaree_jamais_dans_calc(self) -> None:
        t = load_table("carbon_tk_dual_LITTERATURE-2026.json")
        p = t["params"]
        pred = float(p["TK_C_lambda514_nm"]) / float(p["La_star_nm"])
        self.assertAlmostEqual(pred, self.row()["mu_loc"], places=12)
        # La valeur déclarée est dans la table mais hors du calcul :
        self.assertNotEqual(pred, float(p["ID_IG_declared"]))
        self.assertAlmostEqual(float(p["ID_IG_declared"]),
                               0.73484692283495345, places=15)
        # u déclarée couvre le scatter documenté (KW Fig. 4, r² = 0,84)
        self.assertEqual(float(p["u_declared"]), 0.15)

    def test_o4star_point_dual_et_ancres(self) -> None:
        # L★ est la moyenne géométrique des ancres O4 (3 nm) et
        # O14 (10 nm) : même constante C, trois points, la loi tient au
        # dual après avoir cassé à 3 nm (O4) et tenu à 10 nm (O14).
        self.assertAlmostEqual(4.4 / 3.0, 1.4666666666666668, places=12)
        self.assertAlmostEqual(4.4 / 10.0, 0.44, places=12)
        self.assertAlmostEqual(4.4 / L_STAR, 0.8033264176742437, places=12)
        self.assertEqual(self.row()["lever"], "La<-recalibrer")


if __name__ == "__main__":
    unittest.main(verbosity=2)
