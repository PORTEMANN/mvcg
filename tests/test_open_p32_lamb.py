#!/usr/bin/env python3
"""Contact ouvert P32 — Lamb moderne : la dette se ferme (suite P31).

Chronologie du gel :
1. Protocole ecrit et gele avant toute execution (doc
   P32-LAMB-MODERNE-CONTACT-OUVERT.md) : mu_loc = 1057.842 MHz (calcul
   QED Pachucki 2001 declare, u = 0.004, pour rp = 0.862(12) fm declare
   — dependance ecrite dans la table, pas circularite), mu_ref =
   1057.845 MHz (MEME temoin Lundeen-Pipkin 1981 que P31, gel commun,
   u = 0.009). La reference NE DOIT JAMAIS entrer dans le calcul.
   theta = u_delta = 0.009848857801796104 MHz, decide=U, k=1.
   Estimation pre-run honnete : delta ~ 0.003 MHz, ratio ~ 0.305 ->
   S+ attendu, suspense faible — le suspense est dans l'arc : le temoin
   qui valait P (Mohr, 1.14 theta) et S- (Erickson, 4.71 theta) contre
   les theories vintage devient S+ contre la theorie reevaluee.
2. Premier run : mot = S+ (delta = 0.0029999999999290594 MHz,
   a 0.304604 theta). Decouvert, pas choisi.
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


class TestOpenContactP32LambModern(unittest.TestCase):
    def rows(self) -> dict:
        return {r["id"]: r for r in run_registers()["rows"]}

    def test_p32_word_frozen(self) -> None:
        r = self.rows()["P32_Lamb_Modern"]
        self.assertEqual(r["verdict"], "S+")  # mot du premier run, fige
        self.assertEqual(r["statut"], "ouverte")
        self.assertIsNone(r["expected"])
        self.assertLessEqual(r["delta"], r["theta"])
        self.assertAlmostEqual(r["delta"], 0.0029999999999290594, places=12)
        self.assertAlmostEqual(r["mu_loc"], 1057.842, places=9)
        self.assertAlmostEqual(r["mu_ref"], 1057.845, places=9)
        self.assertAlmostEqual(r["delta"] / r["theta"],
                               0.3046038495328828, places=9)

    def test_p32_meme_temoin_que_p31(self) -> None:
        # L'arc repose sur l'identite du temoin : mu_ref de P32 == mu_ref
        # de P31 au bit pres. Geste interdit : rapprocher la reference.
        by = self.rows()
        self.assertAlmostEqual(by["P32_Lamb_Modern"]["mu_ref"],
                               by["P31_Lamb_Mohr"]["mu_ref"], places=12)
        self.assertAlmostEqual(by["P32_Lamb_Modern"]["mu_ref"],
                               by["P31_Lamb_Erickson"]["mu_ref"],
                               places=12)
        # Le verdict se ferme la ou la campagne P31 portait P et S-.
        self.assertEqual(by["P31_Lamb_Mohr"]["verdict"], "P")
        self.assertEqual(by["P31_Lamb_Erickson"]["verdict"], "S-")
        self.assertEqual(by["P32_Lamb_Modern"]["verdict"], "S+")

    def test_p32_gum_decide_U_k1(self) -> None:
        g = self.rows()["P32_Lamb_Modern"]["extra"]["gum"]
        self.assertEqual(g["decide"], "U")
        self.assertEqual(g["k"], 1.0)
        self.assertAlmostEqual(g["U"], 0.009848857801796104, places=12)
        lines = [{"name": "pachucki2001_QED", "type": "B", "u": 0.004},
                 {"name": "lundeen_pipkin_temoin", "type": "B", "u": 0.009}]
        self.assertAlmostEqual(u_c(lines), 0.009848857801796104, places=12)

    def test_dependance_rp_declaree_dans_la_table(self) -> None:
        # Verrou : la dependance au rayon proton est ecrite dans la
        # table — la presenter comme independante serait une
        # falsification du gel.
        t = load_table("lamb_shift_P32_LITERATURE-2001.json")
        note = t["params"]["note"]
        self.assertIn("rp = 0.862(12)", note)
        self.assertIn("dependance", note.lower())


if __name__ == "__main__":
    unittest.main(verbosity=2)
