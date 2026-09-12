#!/usr/bin/env python3
"""Classement des verdicts par fibre — appliqué à la série en ligne.

Méthode (portée de la mouture github5, verdict_register.py) : indexer
les verdicts par (packet, dimension), balayer chaque contact sous les
quatre paquets d'unités. Interdit : η comme μ, export d'un mot vers
une autre fibre, moyennage des couleurs.

Ce test fige le classement de la série en ligne au moment de l'application
(2026-09-12) : 16 contacts ouverts, invariance complète sous balayage.
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from mvcg.registers import run_registers  # noqa: E402
from mvcg.verdict_register import index_verdicts, street_sweep  # noqa: E402


class TestVerdictsOnline(unittest.TestCase):
    def test_fiber_classification_frozen(self) -> None:
        idx = index_verdicts()
        self.assertEqual(idx["n"], 34)  # série en ligne au 2026-09-12
        self.assertEqual(len(idx["fibres"]), 10)
        by = {(f["packet"], f["dimension"]): f for f in idx["fibres"]}
        # Les trois fibres phares de la série O :
        self.assertEqual(by[("1", "cm^-1")]["counts"],
                         {"S+": 4, "P": 2, "S-": 0})
        self.assertEqual(by[("si", "eV")]["counts"],
                         {"S+": 3, "P": 0, "S-": 3})
        self.assertEqual(by[("si", "J m^-3 K^-2")]["counts"],
                         {"S+": 1, "P": 0, "S-": 1})
        # La paire NMR : même loi de Karplus, deux conformations —
        # la loi devient une carte (hélice S+, brin P).
        self.assertEqual(by[("si", "Hz")]["counts"],
                         {"S+": 1, "P": 1, "S-": 0})
        self.assertIn("NMR_Karplus_Helix", by[("si", "Hz")]["ids"])
        self.assertIn("NMR_Karplus_Sheet", by[("si", "Hz")]["ids"])
        # CKM apporte le seul P de la fibre sans dimension.
        self.assertEqual(by[("1", "1")]["counts"],
                         {"S+": 4, "P": 1, "S-": 6})
        self.assertIn("CKM_Row1_Unitarity", by[("1", "1")]["ids"])

    def test_all_16_open_contacts_sweep_invariant(self) -> None:
        rows = run_registers()["rows"]
        o_ids = [r["id"] for r in rows
                 if r["id"].startswith("O") and r["statut"] == "ouverte"]
        self.assertEqual(len(o_ids), 16)
        for cid in o_ids:
            st = street_sweep(cid)
            licites = [r for r in st["rows"] if not r["units_kill"]]
            self.assertEqual(len(licites), 4, f"{cid}: units_kill inattendu")
            for r in licites:
                self.assertEqual(r["verdict"], st["home_verdict"],
                                 f"{cid}: mot {r['verdict']} en packet "
                                 f"{r['packet']} != home {st['home_verdict']}")

    def test_words_are_not_unit_artifacts(self) -> None:
        # Le point du classement : un S+ découvert en packet « 1 »
        # (cm⁻¹) reste S+ sous hl/gauss/si — δ rel est invariant, le
        # dictionnaire d'unités ne fabrique aucun mot.
        st = street_sweep("O13_CO2_Isotopologue")
        self.assertEqual(st["home_packet"], "1")
        for r in st["rows"]:
            self.assertEqual(r["verdict"], "S+")
            self.assertAlmostEqual(r["delta"], 0.010285795843806511,
                                   places=12)

    def test_nmr_contacts_sweep_invariant(self) -> None:
        # La paire Karplus se balaie comme la série O : un mot par
        # couleur, identique au mot home (θ = 0,10 rel).
        for cid, mot in (("NMR_Karplus_Helix", "S+"),
                         ("NMR_Karplus_Sheet", "P")):
            st = street_sweep(cid)
            licites = [r for r in st["rows"] if not r["units_kill"]]
            self.assertEqual(len(licites), 4, f"{cid}: units_kill inattendu")
            self.assertEqual(st["home_verdict"], mot)
            for r in licites:
                self.assertEqual(r["verdict"], mot)

    def test_ckm_two_instruments_two_frozen_words(self) -> None:
        # CKM est le premier contact où le mot home (GUM, decide=U,
        # k=2 → U = 0,0014) diffère du mot balayage (θ seul = 0,0007).
        # Les deux instruments sont figés, séparément — le balayage
        # ne « corrige » pas le home, il mesure autre chose. C'est
        # exactement la dette annoncée au gel : δ = 0,0016 dépasse
        # 2θ sans dépasser 2U.
        st = street_sweep("CKM_Row1_Unitarity")
        licites = [r for r in st["rows"] if not r["units_kill"]]
        self.assertEqual(len(licites), 4, "CKM: units_kill inattendu")
        self.assertEqual(st["home_verdict"], "P")
        for r in licites:
            self.assertEqual(r["verdict"], "S-")
            # Dimension « 1 » : δ partagé par les quatre paquets, mot
            # S- partout sous θ seul.
            self.assertAlmostEqual(r["delta"], 0.0016000000000000458,
                                   places=12)


if __name__ == "__main__":
    unittest.main(verbosity=2)
