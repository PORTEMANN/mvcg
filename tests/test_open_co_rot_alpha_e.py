#!/usr/bin/env python3
"""Contact SPEC CO — levier α_e du rotor rigide ab initio.

Chronologie du gel :
1. Protocole écrit avant toute exécution : SPEC-CO-ROT-PROTOCOLE.md
   §5 (gel 2026-09-14) — mu_loc = |B0,calc − B0,obs| en Hz,
   B0,calc = B_e,calc − α_e/2 (même calcul ab initio que le contact 1,
   correction vibration-rotation H&H 1979 soustraite) ; mu_ref = B0
   mesuré NIST. theta = 3000 Hz = u(B0) déclarée NIST, gelée avant
   run. GUM : une ligne B, decide=theta, k=2.
2. Estimation pré-run honnête : le contact 1 a mesuré B_e,calc − B0 =
   262394407 Hz, écart à α_e/2 attendu = 76007 Hz ; delta ~ 76 kHz,
   delta/theta ~ 25 -> S- attendu SANS suspense. Le levier devait
   réduire l'écart d'un facteur ~3500 ; le résidu nomme la dette de
   vintage (H&H 1979, α_e 3 chiffres, ajustement 1976) vs NIST 2013.
3. Premier run : mot découvert : **S-**, delta = 76006,630088806 Hz
   (25,3 theta) — le résidu annoncé au centième près (le levier est
   coherent par construction ; la machine verifie). La carte dit :
   geste + levier justes (262 MHz -> 76 kHz), la table est la dette —
   exactement la même leçon que le P de Kratzer, lue de l'autre
   cote : la vintage H&H 1979 ne rejoint pas le NIST 2013 dans le
   budget. Schema echec -> levier avec residu nomme, pendant de
   O1 -> O6 (S+) et O3 -> O7 (S+), ici le levier ne blanchit pas
   completement car la table d'entree est la dette.
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


def _b0_calc_hz(t: dict) -> float:
    p = t["params"]
    hbar = float(p["hbar_SI"])
    mu = float(p["mu_u"]) * float(p["u_kg"])
    re = float(p["re_A"]) * 1e-10
    b_e = hbar / (4.0 * math.pi * mu * re**2)
    alpha_half = float(p["alpha_e_cm-1"]) / 2.0 * float(p["cm-1_to_MHz"]) * 1e6
    return float(b_e - alpha_half)


class TestOpenContactCoRotAlphaE(unittest.TestCase):
    def row(self) -> dict:
        by = {r["id"]: r for r in run_registers()["rows"]}
        return by["SPEC_CO_Rot_AlphaE"]

    def test_co_rot_alpha_e_word_frozen(self) -> None:
        r = self.row()
        self.assertEqual(r["verdict"], "S-")  # mot du premier run, figé
        self.assertEqual(r["statut"], "ouverte")
        self.assertIsNone(r["expected"])
        self.assertGreater(r["delta"], 2.0 * r["theta"])  # 76e3 > 6e3
        self.assertAlmostEqual(r["mu_loc"], 76006.63008880615, places=6)

    def test_co_rot_alpha_e_gum_carried_not_used(self) -> None:
        g = self.row()["extra"]["gum"]
        self.assertEqual(g["decide"], "theta")
        self.assertAlmostEqual(g["uc"], 3000.0, places=12)
        self.assertAlmostEqual(g["U"], 6000.0, places=12)

    def test_co_rot_alpha_e_reproducible_from_table(self) -> None:
        t = load_table("co_rot_NIST-HH.json")
        b0 = float(t["params"]["B0_MHz"]) * 1e6
        self.assertAlmostEqual(abs(_b0_calc_hz(t) - b0),
                               self.row()["mu_loc"], places=6)
        self.assertIn("NIST-JPCRD53", t["vintage"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
