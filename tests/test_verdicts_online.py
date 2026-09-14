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
        self.assertEqual(idx["n"], 46)  # série en ligne au 2026-09-13 + Bertsch + KSS×2 + AMU WP25 (la paire complète) + H0 (chantier local) + H(z) bas-z DEMO (chantier local) + H(z) bas-z LITERATURE ×2 ancrages (chantier local 2026-09-13 soir)
        self.assertEqual(len(idx["fibres"]), 12)
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
        # Le complexe g-2 : les quatre contacts, la paire d'identifications
        # complète dans la même fibre — WP25 S+ à 0,6 U, WP20 S− à 3,7 U,
        # HVP P, HLbL S+. Deux mots opposés, aucun choisi.
        self.assertEqual(by[("1", "1e-11")]["counts"],
                         {"S+": 2, "P": 1, "S-": 1})
        self.assertIn("AMU_Delta_WP25", by[("1", "1e-11")]["ids"])
        self.assertIn("AMU_exp_minus_WP20", by[("1", "1e-11")]["ids"])
        self.assertIn("HVP_LO_lat_vs_ee", by[("1", "1e-11")]["ids"])
        self.assertIn("HLbL_lat_vs_pheno", by[("1", "1e-11")]["ids"])
        # Hyperfluidité : Landau rejoint la fibre des vitesses
        # (cousin de O5, condensat dilué côté BEC).
        self.assertEqual(by[("si", "m/s")]["counts"],
                         {"S+": 1, "P": 1, "S-": 0})
        self.assertIn("Landau_Vc_He4", by[("si", "m/s")]["ids"])
        self.assertIn("O5_BEC_Sound", by[("si", "m/s")]["ids"])
        # CKM apporte le seul P de la fibre sans dimension ; Bertsch y
        # apporte un S- de dette (mean-field vs QMC, pendant de P27), KSS
        # un S- de marge (8,8 planchers), KSS_QGP un S- qui dévoile la
        # non-saturation déclarée (borne inf 2 planchers vs plancher).
        self.assertEqual(by[("1", "1")]["counts"],
                         {"S+": 4, "P": 2, "S-": 9})
        self.assertIn("CKM_Row1_Unitarity", by[("1", "1")]["ids"])
        self.assertIn("H0_Ecart_Planck_SH0ES", by[("1", "1")]["ids"])
        self.assertIn("Bertsch_Xi_Unitary", by[("1", "1")]["ids"])
        self.assertIn("KSS_EtaS_He4", by[("1", "1")]["ids"])
        self.assertIn("KSS_EtaS_QGP", by[("1", "1")]["ids"])
        # Le contact H(z) bas-z ouvre la fibre des modules de distance :
        # extract DEMO (fiducial H0=70 déclaré), la fabrication Planck
        # manque les bins de 0,117 mag — dette au-delà de 2 theta.
        # 2026-09-13 soir : la paire LITERATURE (Pantheon+ ancrée
        # Planck 0,0695 / ancrée SH0ES 0,2314, deux S-) — même fibre,
        # deux ancrages déclarés, dettes écrites.
        self.assertEqual(by[("1", "mag")]["counts"],
                         {"S+": 0, "P": 0, "S-": 3})
        self.assertIn("H0_Hz_SNe_LOWZ_DEMO", by[("1", "mag")]["ids"])
        self.assertIn("H0_Hz_SNe_LOWZ_LIT_PLANCK", by[("1", "mag")]["ids"])
        self.assertIn("H0_Hz_SNe_LOWZ_LIT_SH0ES", by[("1", "mag")]["ids"])

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

    def test_g2_contacts_sweep(self) -> None:
        # Balayage de la fibre g-2. AMU WP20 : S- invariant. HVP et
        # HLbL : deux instruments, deux mots figés — le balayage
        # (θ seul) dit S- pour HVP et P pour HLbL, pendant que le
        # home (GUM k=2) dit P et S+ : exactement le suspense sur k
        # déclaré au gel.
        st = street_sweep("AMU_exp_minus_WP20")
        licites = [r for r in st["rows"] if not r["units_kill"]]
        self.assertEqual(len(licites), 4)
        self.assertEqual(st["home_verdict"], "S-")
        for r in licites:
            self.assertEqual(r["verdict"], "S-")
        for cid, home, sweep in (("HVP_LO_lat_vs_ee", "P", "S-"),
                                 ("HLbL_lat_vs_pheno", "S+", "P")):
            st = street_sweep(cid)
            licites = [r for r in st["rows"] if not r["units_kill"]]
            self.assertEqual(len(licites), 4, f"{cid}: units_kill inattendu")
            self.assertEqual(st["home_verdict"], home)
            for r in licites:
                self.assertEqual(r["verdict"], sweep)


if __name__ == "__main__":
    unittest.main(verbosity=2)
