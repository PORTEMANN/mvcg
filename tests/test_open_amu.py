#!/usr/bin/env python3
"""Contact ouvert AMU — l'écart g-2 porté, en unités de son incertitude.

Chronologie du gel :
1. Protocole écrit et gelé avant toute exécution : règle déclarée —
   mu_loc = delta déclaré de la table (a_exp - a_SM lattice WP25) =
   38e-11, PORTÉ, pas calculé depuis a_SM et a_exp séparément (la
   table ne porte pas a_exp seul). La référence est l'identité (le
   SM complet prédit delta = 0). θ = 63 abs gelé avant run = u_delta
   déclarée : le seuil EST l'incertitude de l'écart. GUM : decide=U,
   k=1 — un S+ ici veut dire « l'écart tient dans une incertitude »,
   jamais « le SM est confirmé ». Autre identification (HVP e+e-)
   déclarée dans la note, jamais choisie après coup (honnêteté O15).
   Estimation pré-run : 38 <= 63, à 0,6 theta — suspense faible :
   contact de calibre de la tension, pas de suspense.
2. Premier run : mot = S+ (delta = 38 <= 63). Découvert, pas choisi.
3. Ce test fixe le mot, comme pour tout contact du registre.
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from mvcg.gum import u_c  # noqa: E402
from mvcg.registers import run_registers  # noqa: E402
from mvcg.tables import load_table  # noqa: E402


class TestOpenContactAMU(unittest.TestCase):
    def row(self) -> dict:
        by = {r["id"]: r for r in run_registers()["rows"]}
        return by["AMU_Delta_WP25"]

    def test_amu_word_frozen(self) -> None:
        r = self.row()
        self.assertEqual(r["verdict"], "S+")  # mot du premier run, figé
        self.assertEqual(r["statut"], "ouverte")
        self.assertIsNone(r["expected"])
        self.assertLess(r["delta"], r["theta"])  # 38 < 63
        self.assertAlmostEqual(r["mu_loc"], 38.0, places=12)

    def test_amu_delta_porte_pas_calcule(self) -> None:
        # mu_loc est la valeur déclarée de la table, portée telle
        # quelle : ce n'est pas a_SM recombiné avec autre chose. Le
        # geste interdit serait de reconstruire l'écart depuis
        # a_sm_wp25 et une valeur a_exp absente — la table ne porte
        # pas a_exp seul, donc le calcul est impossible : porté, pas
        # dérivé.
        t = load_table("amu_LITERATURE-2018.json")
        p = t["params"]
        self.assertEqual(float(p["delta_exp_minus_wp25"]),
                         self.row()["mu_loc"])
        self.assertNotIn("a_exp", p)  # pas de reconstruction possible
        self.assertEqual(float(p["u_delta_wp25"]), self.row()["theta"])

    def test_amu_gum_decide_U_k1(self) -> None:
        # Le seuil EST l'incertitude : decide=U, k=1 déclarés.
        # Robustesse, pas choix : le mot ne change pas quand k varie
        # dans la plage usuelle — un S+ à 0,6 theta n'est pas une
        # affaire de couverture.
        g = self.row()["extra"]["gum"]
        self.assertEqual(g["decide"], "U")
        self.assertEqual(g["k"], 1.0)
        self.assertAlmostEqual(g["U"], 63.0, places=12)
        for k in (1.0, 2.0, 3.0):
            self.assertLessEqual(self.row()["delta"], k * g["uc"])
        # La ligne B portée recombine au seuil déclaré :
        lines = [{"name": "delta_WP25", "type": "B", "u": 63.0}]
        self.assertAlmostEqual(u_c(lines), 63.0, places=12)


if __name__ == "__main__":
    unittest.main(verbosity=2)
