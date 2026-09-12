#!/usr/bin/env python3
"""Contact ouvert O14 — loi de Tuinstra–Koenig DANS sa fenêtre.

Chronologie du gel :
1. Protocole écrit et gelé avant toute exécution : règle déclarée —
   I_D/I_G = C(λ)/L_a avec C = 4,4 nm (même constante empirique qu'O4)
   et L_a = 10 nm (charbon graphitisé, cœur de la fenêtre de phase 1) ;
   le rapport observé (0,45) NE DOIT JAMAIS entrer dans le calcul ;
   θ = 0,10 figé avant run ; référence = rapport observé de
   l'échantillon. La référence ne participe jamais au calcul.
   Estimation pré-run honnête : écart ~2 %.
2. Premier run : mot = S+ (δ ≈ 2,2 %). Découvert, pas choisi.
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


def _tk(c_lambda: float, la_nm: float) -> float:
    return c_lambda / la_nm


class TestOpenContactO14(unittest.TestCase):
    def row(self) -> dict:
        by = {r["id"]: r for r in run_registers()["rows"]}
        return by["O14_TK_Fenetre"]

    def test_o14_word_frozen(self) -> None:
        r = self.row()
        self.assertEqual(r["verdict"], "S+")  # mot du premier run, figé
        self.assertEqual(r["statut"], "ouverte")
        self.assertIsNone(r["expected"])
        self.assertLess(r["delta"], r["theta"])  # 2,2 % < 10 %
        self.assertAlmostEqual(r["mu_loc"], 0.44, places=12)

    def test_o14_anti_tautology_rapport_jamais_dans_calc(self) -> None:
        t = load_table("carbon_tk_window_LITERATURE-2018.json")
        p = t["params"]
        pred = _tk(float(p["TK_C_lambda514_nm"]), float(p["La_nm"]))
        self.assertAlmostEqual(pred, self.row()["mu_loc"], places=12)
        # Le rapport observé est dans la table mais hors du calcul :
        params_sans = {k: v for k, v in p.items()
                       if k != "ID_IG_observed"}
        self.assertNotIn("ID_IG_observed", params_sans)
        self.assertAlmostEqual(
            _tk(float(params_sans["TK_C_lambda514_nm"]),
                float(params_sans["La_nm"])),
            pred, places=12)

    def test_o14_carte_avec_o4(self) -> None:
        # Avec O4 (L_a = 3 nm, S-), la loi devient une carte : échec
        # hors de la fenêtre (nanodiamant), test dans la fenêtre
        # (charbon graphitisé). Même constante C, deux verdicts.
        self.assertAlmostEqual(_tk(4.4, 3.0), 1.4666666666666668, places=12)
        self.assertAlmostEqual(_tk(4.4, 10.0), 0.44, places=12)
        # Le levier déclaré reste La←recalibrer, jamais un θ déplacé.
        self.assertEqual(self.row()["lever"], "La<-recalibrer")


if __name__ == "__main__":
    unittest.main(verbosity=2)
