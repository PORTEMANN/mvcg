#!/usr/bin/env python3
"""Contact ouvert Rydberg voie 2 — R_∞ calculee depuis alpha et me*c^2.

Chronologie du gel :
1. Protocole ecrit et gele avant toute execution (doc
   RYDBERG-VOIE2-CONTACT-OUVERT.md, campagne croisee) : mu_loc = R_∞
   en eV CALCULEE : R_∞ = alpha^2 me*c^2 / (2e), alpha =
   7.2973525693(11)e-3 et me*c^2 = 8.1871057769(25)e-14 J (CODATA
   2018, incertitudes declarees dans la table), e exacte (SI).
   mu_ref = Rydberg_eV declare du meme tableau. GUM : decide=U, k=1,
   theta = u_delta = 5.838364428925748e-9 eV (quadrature propagation
   alpha x2 et me*c^2 + u declaree de la reference, portee par la
   table). DETTE DE CIRCULARITE DECLAREE : alpha, me*c^2 et
   Rydberg_eV participent du MEME ajustement CODATA-2018 — ce
   contact mesure la coherence interne du catalogue, exactement comme
   SPEC_CO_Rot_Dunham ; pas une prediction independante. Suspense
   annonce nul au gel : S+ attendu a ~0.02 U — certification de la
   fibre eV, pas de suspense.
2. Premier run : mot = S+ (delta = 1.00245e-10 eV, a 0.017 U —
   pile l'estimation annoncee). Decouvert, pas choisi.
3. Ce test fixe le mot, comme pour tout contact du registre.
"""

from __future__ import annotations

import math
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from mvcg.gum import u_c  # noqa: E402
from mvcg.registers import run_registers  # noqa: E402
from mvcg.tables import load_table  # noqa: E402


class TestOpenContactRydbergVoie2(unittest.TestCase):
    def row(self) -> dict:
        by = {r["id"]: r for r in run_registers()["rows"]}
        return by["H1s_Rydberg_Voie2"]

    def test_rydberg_voie2_word_frozen(self) -> None:
        r = self.row()
        self.assertEqual(r["verdict"], "S+")  # mot du premier run, fige
        self.assertEqual(r["statut"], "ouverte")
        self.assertIsNone(r["expected"])
        self.assertLess(r["delta"], r["theta"])  # 1e-10 << 5.84e-9
        self.assertAlmostEqual(r["mu_loc"], 13.605693123094245, places=12)
        self.assertAlmostEqual(r["mu_ref"], 13.605693122994, places=12)
        self.assertAlmostEqual(r["delta"] / r["theta"], 0.017170073354999413,
                               places=12)

    def test_rydberg_voie2_calculee_depuis_la_table(self) :
        # mu_loc est le produit alpha^2 * me*c^2 / (2e) calcule depuis
        # les constantes DECLAREES de la table — geste interdit :
        # corriger une constante pour rapprocher la reference (autre D).
        t = load_table("codata2018_rydberg_voie2.json")
        c = t["constants"]
        attendu = (float(c["alpha"]) ** 2 * float(c["me_c2_J"])
                   / (2.0 * float(c["e_C"])))
        self.assertAlmostEqual(self.row()["mu_loc"], attendu, places=12)
        self.assertAlmostEqual(float(c["rydberg_eV"]),
                               self.row()["mu_ref"], places=12)

    def test_rydberg_voie2_gum_decide_U_k1(self) -> None:
        # Le seuil EST l'incertitude propagee : decide=U, k=1 declares.
        # Robustesse : le mot ne change pas quand k varie dans la
        # plage usuelle — un S+ a 0,017 U n'est pas une affaire de
        # couverture.
        g = self.row()["extra"]["gum"]
        self.assertEqual(g["decide"], "U")
        self.assertEqual(g["k"], 1.0)
        self.assertAlmostEqual(g["U"], 5.838364428925748e-9, places=18)
        for k in (1.0, 2.0, 3.0):
            self.assertLessEqual(self.row()["delta"], k * g["uc"])
        # Les lignes B portees recombinent au seuil declare :
        lines = [{"name": "R_inf_calc", "type": "B", "u": 5.838306535712686e-9},
                 {"name": "R_inf_declaree", "type": "B", "u": 2.6e-11}]
        self.assertAlmostEqual(u_c(lines), 5.838364428925748e-9, places=18)

    def test_circularite_declaree_dans_la_table(self) -> None:
        # Verrou : la dette de circularite est ecrite dans la table —
        # retirer la note serait une falsification du gel.
        t = load_table("codata2018_rydberg_voie2.json")
        self.assertIn("CIRCULARITE", t["note"])
        self.assertIn("Dunham", t["note"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
