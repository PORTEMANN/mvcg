#!/usr/bin/env python3
"""Chantier E44 — nucléation de l'enlacement : verrous figés.

La note d'audit E44 (31/07/2026) est un protocole pré-enregistré haché
SHA-256 avant calcul : la machine pèse ses déclarations gelées et leur
arithmétique interne, elle ne rejoue pas la simulation GP.
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from mvcg.e44 import (  # noqa: E402
    e44_lk_paire,
    e44_p3_filaments,
    e44_t0_lien,
)
from mvcg.registers import CONTACTS  # noqa: E402
from mvcg.registers import run_contact  # noqa: E402


def _contact(cid: str) -> dict:
    c = next(x for x in CONTACTS if x.id == cid)
    return run_contact(c)


class TestE44Calculs(unittest.TestCase):
    def test_mu_gelés(self):
        # déclarations verbatim de la note (2026-09-16)
        self.assertAlmostEqual(e44_t0_lien()[0], 0.994, delta=1e-15)
        self.assertAlmostEqual(e44_lk_paire()[0], 1.004, delta=1e-15)
        self.assertAlmostEqual(e44_p3_filaments()[0], 14.0, delta=1e-15)

    def test_t0_extras(self):
        _, x = e44_t0_lien()
        self.assertAlmostEqual(x["ecart_lien"], 0.006, delta=1e-15)
        self.assertAlmostEqual(x["ecart_temoin"], 0.007, delta=1e-15)

    def test_lk_robustesse_declaree(self):
        # trois estimations déclarées, les trois passent le seuil
        _, x = e44_lk_paire()
        self.assertEqual(x["n_passent_seuil"], 3)
        self.assertAlmostEqual(x["spread"], 0.074, delta=1e-15)
        self.assertEqual(len(x["estimations"]), 3)

    def test_p3_ecart_sigma(self):
        _, x = e44_p3_filaments()
        self.assertAlmostEqual(x["ecart_sigma"], 5.0, delta=1e-15)


class TestE44Contacts(unittest.TestCase):
    def test_verdicts_figés(self):
        attendus = {
            "E44_T0_LienHopf": ("S+", 0.994),
            "E44_Lk_PaireHopf": ("S+", 1.004),
            "E44_P3_Filaments": ("S-", 14.0),
        }
        for cid, (mot, mu) in attendus.items():
            r = _contact(cid)
            self.assertEqual(r["verdict"], mot, cid)
            self.assertEqual(r["expected"], mot, cid)
            self.assertAlmostEqual(r["mu_loc"], mu, delta=1e-15, msg=cid)
            self.assertFalse(r["b3_fail"], cid)
            self.assertIsNone(r["units_kill"], cid)

    def test_t0_lien_tenu(self):
        r = _contact("E44_T0_LienHopf")
        self.assertLess(r["delta"], 0.01)

    def test_p3_attendu_sminus_tenu(self):
        # le corpus statue la réfutation de sa propre prédiction P3 —
        # la machine confirme le mot sur les nombres gelés (5 σ).
        r = _contact("E44_P3_Filaments")
        self.assertEqual(r["expected"], "S-")
        self.assertEqual(r["verdict"], "S-")
        self.assertAlmostEqual(r["delta"], 2.5, delta=1e-15)


if __name__ == "__main__":
    unittest.main()
