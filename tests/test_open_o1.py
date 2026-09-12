#!/usr/bin/env python3
"""Contact ouvert O1 — le mot a été découvert au premier run, puis figé.

Chronologie du gel :
1. Protocole écrit et gelé (runner n=200, r_max=25, θ=1e-3, chaîne Ha→eV,
   table CODATA-2018) — avant toute exécution.
2. Premier run : mot = S- (δ ≈ 3,8e-3 > θ). Découvert, pas choisi.
3. Ce test fixe le mot, comme pour tout contact du registre.

Le levier (grille←raffiner) est vérifié en diagnostic séparé : il ne
change pas les paramètres gelés du contact, il prouve seulement que le
S- est un artefact de grille, pas une physique nouvelle.
"""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from mvcg.h2plus import HA_TO_EV  # noqa: E402
from mvcg.registers import _fd_h1s_ha, run_registers  # noqa: E402


class TestOpenContactO1(unittest.TestCase):
    def row(self) -> dict:
        by = {r["id"]: r for r in run_registers()["rows"]}
        return by["O1_Grille_H1s"]

    def test_o1_word_frozen(self) -> None:
        r = self.row()
        self.assertEqual(r["verdict"], "S-")  # mot du premier run, figé
        self.assertEqual(r["statut"], "ouverte")
        self.assertIsNone(r["expected"])  # aucun mot attendu au gel
        self.assertGreater(r["delta"], r["theta"])

    def test_o1_provenance_chain(self) -> None:
        r = self.row()
        self.assertAlmostEqual(r["extra"]["mu_raw"] * HA_TO_EV, r["mu_loc"], places=9)
        self.assertAlmostEqual(r["extra"]["chain"]["k"], HA_TO_EV, places=9)
        self.assertIsNone(r["chain_kill"])

    def test_o1_lever_refinement_moves_toward_ref(self) -> None:
        r = self.row()
        mu_ref_ha = -0.5  # E_1s exacte en Ha (R_∞ * n=1)
        d_frozen = abs(_fd_h1s_ha(200, 25.0) - mu_ref_ha)
        d_refined = abs(_fd_h1s_ha(1600, 25.0) - mu_ref_ha)
        # levier grille<-raffiner : direction déclarée, vérifiée hors gel
        self.assertLess(d_refined, d_frozen / 10.0)
        self.assertAlmostEqual(_fd_h1s_ha(1600, 25.0), mu_ref_ha, places=4)


if __name__ == "__main__":
    unittest.main(verbosity=2)
