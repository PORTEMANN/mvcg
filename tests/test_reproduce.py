#!/usr/bin/env python3
"""Prototype reproduce.py — la réplication enveloppe le test figé.

Propriétés figées :
- le mot « obtenu » vient du registre live, jamais d'un fichier
  exporté (pas de circularité avec fair_export) ;
- le mot « attendu » vient de l'assertion du test figé
  (convention test_open_*.py), pas d'une déclaration à la main ;
- les contacts du chantier H0 se répliquent : attendu == obtenu, OK.
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from mvcg.registers import run_registers  # noqa: E402
from mvcg.reproduce import expected_word, freezing_files, live_row, reproduce  # noqa: E402


class TestReproduce(unittest.TestCase):
    def test_obtained_is_live_register_not_export(self) -> None:
        # L'obtenu = recalcul du registre. Vérifié sur deux contacts
        # aux mots opposés, sans lire aucun fichier d'export.
        rows = {r["id"]: r for r in run_registers()["rows"]}
        for cid in ("H0_Ecart_Planck_SH0ES", "H0_Hz_SNe_LOWZ_DEMO"):
            got = live_row(cid)
            self.assertEqual(got["verdict"], rows[cid]["verdict"])
            self.assertEqual(got["delta"], rows[cid]["delta"])

    def test_expected_comes_from_frozen_assertion(self) -> None:
        # L'attendu = assertion figée du test dédié, jamais la
        # première assertion du fichier : test_pred_words_frozen fige
        # DEUX contacts — le mot du voisin ne doit jamais être pris.
        files = freezing_files("H0_Hz_SNe_LOWZ_DEMO")
        self.assertTrue(any(p.name == "test_open_hz_sne_lowz.py" for p in files))
        self.assertEqual(expected_word("H0_Hz_SNe_LOWZ_DEMO", files), "S-")
        files_p = freezing_files("H0_Ecart_Planck_SH0ES")
        self.assertEqual(expected_word("H0_Ecart_Planck_SH0ES", files_p), "P")
        # Le même fichier, deux contacts : chacun retrouve SON mot.
        fz = freezing_files("FRW_lcdm_SH0ES")
        self.assertEqual(expected_word("FRW_lcdm_SH0ES", fz), "S+")
        self.assertEqual(expected_word("AAL_dice_lissage", fz), "S-")

    def test_no_neighbor_word_in_classification_file(self) -> None:
        # Anti-régression du faux ami (audit 2026-09-13) : les mots
        # g-2 vivent dans test_open_g2.py, mais l'id y est dans un
        # helper et le fichier porte trois mots — le reproducteur
        # doit dire « non isolable » (None), JAMAIS prendre le mot
        # d'une boucle du fichier de classification.
        files = freezing_files("HVP_LO_lat_vs_ee")
        self.assertIn("test_verdicts_online.py", [p.name for p in files])
        self.assertIsNone(expected_word("HVP_LO_lat_vs_ee", files))
        files_h = freezing_files("HLbL_lat_vs_pheno")
        self.assertIsNone(expected_word("HLbL_lat_vs_pheno", files_h))

    def test_h0_contacts_replicate_ok(self) -> None:
        # Vraie réplication (sous-processus) sur le chantier H0 :
        # attendu == obtenu, tests figés verts.
        for cid, word in (
            ("H0_Ecart_Planck_SH0ES", "P"),
            ("H0_Hz_SNe_LOWZ_DEMO", "S-"),
        ):
            out = reproduce(cid)
            self.assertEqual(out["status"], "OK")
            self.assertEqual(out["expected"], word)
            self.assertEqual(out["obtained"]["verdict"], word)


if __name__ == "__main__":
    unittest.main(verbosity=2)
