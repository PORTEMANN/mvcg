#!/usr/bin/env python3
"""Contact SPEC CO rotationnel — cohérence interne du catalogue (Dunham).

Chronologie du gel :
1. Protocole écrit avant toute exécution : SPEC-CO-ROT-PROTOCOLE.md
   (gel 2026-09-14) — règle gelée : mu_loc = |nu_pred - nu_obs| en Hz,
   nu_pred = 2*B0 - 4*D0 (B0, D0 déclarés NIST JPCRD 53) ; mu_ref =
   nu(1-0) NIST. theta = 10000 Hz = u(nu) déclarée NIST, gelée avant
   run. GUM : une ligne B, decide=theta, k=2. Dette écrite :
   circularité — B0, D0 et nu d'un même ajustement global ; ce contact
   calibre le transport de table, pas une prédiction indépendante.
2. Estimation pré-run honnête : nu_pred = 115271,20372 MHz,
   delta ~ 280 Hz, delta/theta ~ 0,03 -> S+ attendu SANS suspense.
3. Premier run : mot découvert : **S+**, delta = 280,0000074785203 Hz
   (0,028 theta). Le catalogue NIST est interne cohérent à 2,8e-6 de
   son budget déclaré : le transport (B0, D0) -> nu ne s'egare pas
   au-dela du budget. La carte dit : le calibre tient — la table se
   transporte sans perte détectable à hauteur de ses incertitudes.
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


class TestOpenContactCoRotDunham(unittest.TestCase):
    def row(self) -> dict:
        by = {r["id"]: r for r in run_registers()["rows"]}
        return by["SPEC_CO_Rot_Dunham"]

    def test_co_rot_dunham_word_frozen(self) -> None:
        r = self.row()
        self.assertEqual(r["verdict"], "S+")  # mot du premier run, figé
        self.assertEqual(r["statut"], "ouverte")
        self.assertIsNone(r["expected"])
        self.assertLessEqual(r["delta"], r["theta"])  # 280 <= 10000
        self.assertAlmostEqual(r["mu_loc"], 280.0000074785203, places=6)

    def test_co_rot_dunham_gum_carried_not_used(self) -> None:
        g = self.row()["extra"]["gum"]
        self.assertEqual(g["decide"], "theta")
        self.assertAlmostEqual(g["uc"], 10000.0, places=12)
        self.assertAlmostEqual(g["U"], 20000.0, places=12)

    def test_co_rot_dunham_reproducible_from_table(self) -> None:
        t = load_table("co_rot_NIST-HH.json")
        p = t["params"]
        nu_pred = 2.0 * float(p["B0_MHz"]) - 4.0 * float(p["D0_kHz"]) / 1000.0
        self.assertAlmostEqual(abs(nu_pred - float(p["nu_10_MHz"])) * 1e6,
                               self.row()["mu_loc"], places=6)
        self.assertIn("NIST-JPCRD53", t["vintage"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
