#!/usr/bin/env python3
"""Contact SPEC CO isotopologue ¹³CO — règle de la masse réduite.

Chronologie du gel :
1. Protocole écrit avant toute exécution : SPEC-CO-ROT-PROTOCOLE.md
   §3 (gel 2026-09-14, après les deux premiers runs, règle déclarée
   avant SON run) — mu_loc = |B0_pred − B0′(mesure)| en Hz,
   B0_pred = B0(¹²CO) × μ/μ′ (règle de la masse réduite appliquée
   telle quelle au niveau v=0) ; μ, μ′, B0, B0′ déclarés NIST JPCRD 53.
   theta = 12000 Hz = u(B0′) déclarée NIST, gelée avant run. GUM :
   une ligne B, decide=theta, k=2.
2. Estimation pré-run honnête : delta ~ 4,3 MHz, delta/theta ~ 360 ->
   S- attendu SANS suspense (la règle s'applique rigoureusement a
   B_e, pas a B0 ; l'ecart nomme la correction isotopique de la
   vibration-rotation + effets au-dela de Born-Oppenheimer).
3. Premier run : mot découvert : **S-**, delta = 4940938,13 Hz
   (412 theta) — conforme a l'estimation (meme ordre de grandeur).
   La carte dit : a la precision NIST (1e-7 relative), la regle de
   la masse reduite seule ne suffit pas pour le niveau v=0 ; le
   suspense portait sur la taille de l'ecart, pas sur le mot.
   L'ecart mesure nomme la physique au-dela de la regle mu.
4. Figé : mot et valeur à 12 décimales dans ce test.
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from mvcg.registers import run_registers  # noqa: E402
from mvcg.tables import load_table  # noqa: E402


class TestOpenContactCo13RotMuRule(unittest.TestCase):
    def row(self) -> dict:
        by = {r["id"]: r for r in run_registers()["rows"]}
        return by["SPEC_CO13_Rot_MuRule"]

    def test_co13_rot_mu_rule_word_frozen(self) -> None:
        r = self.row()
        self.assertEqual(r["verdict"], "S-")  # mot du premier run, figé
        self.assertEqual(r["statut"], "ouverte")
        self.assertIsNone(r["expected"])
        self.assertGreater(r["delta"], 2.0 * r["theta"])  # 4,9e6 >> 2,4e4
        self.assertAlmostEqual(r["mu_loc"], 4940938.131599978, places=6)

    def test_co13_rot_mu_rule_gum_carried_not_used(self) -> None:
        g = self.row()["extra"]["gum"]
        self.assertEqual(g["decide"], "theta")
        self.assertAlmostEqual(g["uc"], 12000.0, places=12)
        self.assertAlmostEqual(g["U"], 24000.0, places=12)

    def test_co13_rot_mu_rule_reproducible_from_table(self) -> None:
        t = load_table("co_rot_NIST-HH.json")
        p = t["params"]
        b_pred = float(p["B0_MHz"]) * float(p["mu_u"]) / float(p["mu13_u"])
        self.assertAlmostEqual(abs(b_pred - float(p["B0_13_MHz"])) * 1e6,
                               self.row()["mu_loc"], places=6)
        self.assertIn("NIST-JPCRD53", t["vintage"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
