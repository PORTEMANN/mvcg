#!/usr/bin/env python3
"""Mots figés a posteriori — le trou d'audit d'intégrité (2026-09-13).

Chronologie honnête : ces deux contacts sont anciens ; leurs mots
étaient déjà publics via le registre, mais **aucun test ne les
verrouillait** — l'audit complet du registre (chaque contact doit
avoir au moins un test qui affirme son mot) les a déclarés NON FIGÉ.
Ce test bouche le trou. C'est un gel *a posteriori* : le gel avant
run reste la règle pour tout contact nouveau, et ce fichier ne doit
pas servir de précédent pour contourner la chronologie.

- `FRW_lcdm_SH0ES` (S+, δ = 0) : même fermeture Ω, autre étiquette
  H0 — la carte montre que CE μ ignore H0, et déclare déjà où le
  vrai contact doit vivre : « H(z) vs donnée ».
- `AAL_dice_lissage` (S−, δ = 0,6826171875) : partition synthétique,
  pas une carte cérébrale — le lissage 3×3 détruit la partition.
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from mvcg.registers import run_registers  # noqa: E402


class TestPredWordsFrozen(unittest.TestCase):
    def row(self, cid: str) -> dict:
        return {r["id"]: r for r in run_registers()["rows"]}[cid]

    def test_frw_lcdm_sh0es_word_frozen(self) -> None:
        r = self.row("FRW_lcdm_SH0ES")
        self.assertEqual(r["verdict"], "S+")
        self.assertEqual(r["delta"], 0.0)
        self.assertLess(r["delta"], r["theta"])  # θ = 1e-3, identité exacte

    def test_aal_dice_lissage_word_frozen(self) -> None:
        r = self.row("AAL_dice_lissage")
        self.assertEqual(r["verdict"], "S-")
        self.assertAlmostEqual(r["delta"], 0.6826171875, places=12)
        self.assertGreater(r["delta"], 2.0 * r["theta"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
