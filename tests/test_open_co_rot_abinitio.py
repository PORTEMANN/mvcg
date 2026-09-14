#!/usr/bin/env python3
"""Contact SPEC CO rotationnel — rotor rigide à l'équilibre (ab initio).

Chronologie du gel :
1. Protocole écrit avant toute exécution : SPEC-CO-ROT-PROTOCOLE.md
   (gel 2026-09-14) — règle gelée : mu_loc = |B_e,calc - B0,obs| en Hz,
   B_e,calc = hbar/(4 pi mu r_e^2), mu en kg (NIST JPCRD 53),
   r_e déclaré Huber & Herzberg 1979 (via RIOS FHI-MPG) ;
   mu_ref = B0 mesuré NIST. theta = 3000 Hz = u(B0) déclarée NIST,
   gelée avant run. GUM : une ligne B, decide=theta, k=2.
2. Estimation pré-run honnête : delta ~ 265 MHz ~ alpha_e/2 (zéro
   vibratoire B0 = B_e - alpha_e/2), delta/theta ~ 9e4 -> S- attendu
   SANS suspense.
3. Premier run : mot découvert : **S-**, delta = 262394407,38 Hz
   (87465 theta). B_e,calc = 57 898 363 407 Hz ; l'écart mesuré
   reproduit alpha_e/2 attendu (262318400,75 Hz) à 76 kHz pres
   (0,03 %) : le verdict porte exactement le nom annoncé — le rotor
   rigide a l'equilibre ne predit pas le niveau v=0 ; l'écart
   s'appelle alpha_e. La carte dit : un S- de dette de modele pauvre
   (dans l'esprit O1 grille -> O6) ; l'entree r_e est independante
   des raies micro-ondes, contrairement au contact Dunham voisin.
4. Figé : mot et valeur à 12 décimales dans ce test.
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


def _be_calc_hz(t: dict) -> float:
    p = t["params"]
    hbar = float(p["hbar_SI"])
    mu = float(p["mu_u"]) * float(p["u_kg"])
    re = float(p["re_A"]) * 1e-10
    return float(hbar / (4.0 * math.pi * mu * re**2))


class TestOpenContactCoRotAbInitio(unittest.TestCase):
    def row(self) -> dict:
        by = {r["id"]: r for r in run_registers()["rows"]}
        return by["SPEC_CO_Rot_AbInitio"]

    def test_co_rot_abinitio_word_frozen(self) -> None:
        r = self.row()
        self.assertEqual(r["verdict"], "S-")  # mot du premier run, figé
        self.assertEqual(r["statut"], "ouverte")
        self.assertIsNone(r["expected"])
        self.assertGreater(r["delta"], 2.0 * r["theta"])  # 2,6e8 >> 6e3
        self.assertAlmostEqual(r["mu_loc"], 262394407.3800888, places=6)

    def test_co_rot_abinitio_gum_carried_not_used(self) -> None:
        g = self.row()["extra"]["gum"]
        self.assertEqual(g["decide"], "theta")
        self.assertAlmostEqual(g["uc"], 3000.0, places=12)
        self.assertAlmostEqual(g["U"], 6000.0, places=12)

    def test_co_rot_abinitio_reproducible_from_table(self) -> None:
        t = load_table("co_rot_NIST-HH.json")
        b0 = float(t["params"]["B0_MHz"]) * 1e6
        self.assertAlmostEqual(abs(_be_calc_hz(t) - b0),
                               self.row()["mu_loc"], places=6)
        self.assertIn("NIST-JPCRD53", t["vintage"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
