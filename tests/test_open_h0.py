#!/usr/bin/env python3
"""Contact ouvert H0 — la tension entre deux fabrications déclarées.

Chronologie du gel :
1. Protocole écrit et gelé avant toute exécution : règle déclarée —
   la tension H0 EST l'objet : mu_loc = |H0_SH0ES/H0_Planck - 1|,
   les deux valeurs de la table sont la règle elle-même. À la
   différence des contacts O (référence exclue du calcul), il n'y a
   pas ici de troisième référence cachée : l'identité — un seul H0 —
   est mu_ref = 0. Interdit par la table : moyenner les deux
   fabrications. θ = 0,05 abs gelé avant run ; GUM : deux lignes B
   (Planck 0,5/67,4, SH0ES 1,04/67,4), R identité déclarée,
   decide=theta. Estimation pré-run honnête : δ ≈ 8,4 % — zone P
   [θ, 2θ], à 1,6 point de la zone S− : suspense réel.
2. Premier run : mot = P (δ ≈ 8,37 %). Découvert, pas choisi.
3. Ce test fixe le mot, comme pour tout contact du registre.
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from mvcg.gum import check_R  # noqa: E402
from mvcg.registers import run_registers  # noqa: E402
from mvcg.tables import load_table  # noqa: E402


def _ecart(h0_planck: float, h0_shoes: float) -> float:
    return abs(h0_shoes / h0_planck - 1.0)


class TestOpenContactH0(unittest.TestCase):
    def row(self) -> dict:
        by = {r["id"]: r for r in run_registers()["rows"]}
        return by["H0_Ecart_Planck_SH0ES"]

    def test_h0_word_frozen(self) -> None:
        r = self.row()
        self.assertEqual(r["verdict"], "P")  # mot du premier run, figé
        self.assertEqual(r["statut"], "ouverte")
        self.assertIsNone(r["expected"])
        self.assertGreater(r["delta"], r["theta"])  # 8,4 % > 5 %
        self.assertLess(r["delta"], 2.0 * r["theta"])  # 8,4 % < 10 %
        self.assertAlmostEqual(r["mu_loc"], 0.08367952522255195, places=12)

    def test_h0_anti_tautology_pas_de_moyenne(self) -> None:
        # Les deux fabrications sont la règle — changer l'une change
        # le mot. Le geste interdit est la moyenne : μ ne doit JAMAIS
        # être l'écart à la moyenne des deux (0,0457), qui ferait
        # paraître la tension deux fois plus petite.
        t = load_table("h0_LITERATURE-2018.json")
        p = t["params"]
        hp = float(p["Planck2018_H0"])
        hs = float(p["SH0ES2022_H0"])
        self.assertAlmostEqual(_ecart(hp, hs), self.row()["mu_loc"],
                               places=12)
        moyenne = 0.5 * (hp + hs)
        faux_delta = abs(hs / moyenne - 1.0)  # geste interdit
        self.assertGreater(self.row()["delta"], 1.8 * faux_delta)
        # Sensibilité : 1 sigma SH0ES vers le bas ne change pas le mot
        self.assertEqual(
            "P" if _ecart(hp, hs - 1.04) > 0.05 else "S+",
            "P",
        )

    def test_h0_gum_correle(self) -> None:
        # Budget GUM déclaré : deux lignes B, R identité (SDP),
        # decide=theta — le seuil reste theta, u_c est porté, pas
        # utilisé pour blanchir la tension.
        g = self.row()["extra"]["gum"]
        self.assertEqual(g["decide"], "theta")
        self.assertAlmostEqual(g["uc"], 0.017120916008013836, places=12)
        spec = check_R(g["R"], 2)
        self.assertEqual(spec, [1.0, 1.0])
        # u_c à k=2 reste sous theta : la tension n'est PAS une
        # fluctuation d'incertitude — le P n'est pas un S+ déguisé.
        self.assertLess(g["U"], self.row()["theta"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
