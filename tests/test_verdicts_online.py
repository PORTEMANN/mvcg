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
        self.assertEqual(idx["n"], 62)  # série en ligne au 2026-09-13 + Bertsch + KSS×2 + AMU WP25 (la paire complète) + H0 (chantier local) + H(z) bas-z DEMO (chantier local) + H(z) bas-z LITERATURE ×2 ancrages (chantier local 2026-09-13 soir) + H(z) bas-z V2 ×2 courbes (MU_SH0ES natif, 2026-09-14) + SPEC CO rotationnel ×2 (ab initio / Dunham, 2026-09-14) + SPEC CO isotopologue (regle mu, 2026-09-14) + SPEC CO Kratzer (prediction croisee, P au cheveu, 2026-09-14) + SPEC CO levier alpha_e (residu vintage, 2026-09-14) + HVP pi pi CMD-3 vs pre-moyenne (campagne croisee, exp-vs-exp, 2026-09-14) + Karplus Vogeli-Bax 2007 ×2 (campagne croisee, seconde voie, 2026-09-14) + Rydberg voie 2 (R_∞ depuis alpha et me*c^2, certification CODATA, 2026-09-14) + O17 H2 anharmonique (Dunham ordre 1 vs fondamental declare arrondi, S- a 2,94 theta — tare de declaration pesee, 2026-09-14) + O18 H2 tare de lecture (meme transport, reference relue a u = 5/sqrt(3), S+ a 0,51 theta — le verdict pese des declarations pas des physiques, 2026-09-14) + P31 Lamb x3 (chantier atome : Dirac S- dette historique 20 theta, Mohr P au cheveu 1,14 theta, Erickson S- 4,71 theta — meme mesure, deux calculs QED de la meme epoque, deux verdicts, 2026-09-14)
        self.assertEqual(len(idx["fibres"]), 13)  # 12 + (si, MHz) ouverte par le couplet Lamb P31 (2026-09-14)
        by = {(f["packet"], f["dimension"]): f for f in idx["fibres"]}
        # Les trois fibres phares de la série O :
        # 2026-09-14 : Rydberg voie 2 rejoint la fibre — R_∞ calculee
        # depuis alpha et me*c^2 (CODATA 2018 declares), S+ a 0,017 U :
        # certification pesee de la coherence interne du catalogue
        # (circularite declaree, pendant du Dunham) ; la fibre eV a sa
        # case de reference pour les contacts qui la citent.
        self.assertEqual(by[("si", "eV")]["counts"],
                         {"S+": 4, "P": 0, "S-": 3})
        self.assertIn("H1s_Rydberg_Voie2", by[("si", "eV")]["ids"])
        self.assertEqual(by[("1", "cm^-1")]["counts"],
                         {"S+": 5, "P": 2, "S-": 1})
        # 2026-09-14 : O17 ouvre le S- de la fibre — Dunham ordre 1 vs
        # fondamental declare arrondi : la tare d'over-read de l'arrondi
        # "4160" (lu a u=0,5) est detectee a 2,94 sigma (verdict S- a
        # 2,9447 theta, au-dela de la borne P 2 theta). Erreur de bande
        # P au protocole conservee et corrigee en trace visible.
        # 2026-09-14 : O18, pendant disciplinaire — meme transport, meme
        # reference relue honnetement (u = 5/sqrt(3)) : S+ a 0,5126
        # theta. Meme delta 1,48 cm^-1, verdict oppose : la machine
        # pese des declarations, pas des physiques. Amendement de
        # formule visible (5/sqrt(12) -> 5/sqrt(3), trace d'O17).
        self.assertIn("O17_H2_Anharmonique", by[("1", "cm^-1")]["ids"])
        self.assertIn("O18_H2_Tare_Lecture", by[("1", "cm^-1")]["ids"])
        self.assertEqual(by[("si", "J m^-3 K^-2")]["counts"],
                         {"S+": 1, "P": 0, "S-": 1})
        # La paire NMR : même loi de Karplus, deux conformations —
        # la loi devient une carte (hélice S+, brin P).
        # 2026-09-14 : la fibre (si, Hz) s'ouvre au rotationnel — paire
        # SPEC CO : ab initio S- à 87465 theta (l'écart s'appelle
        # alpha_e), Dunham S+ à 0,028 theta (cohérence interne du
        # catalogue NIST, dette de circularité écrite) ; isotopologue
        # 13CO : regle de la masse reduite S- à 412 theta (a la
        # precision NIST la regle mu seule ne suffit pas au niveau v=0) ;
        # Kratzer : prediction croisee P au cheveu a 1,394 theta
        # (l'anharmonicite tient mais pas dans le budget NIST) ; levier
        # alpha_e : residu vintage S- a 25 theta (le levier reduit
        # l'ecart d'un facteur ~3500, la table H&H est la dette) ;
        # 2026-09-14 apres-midi : paire Karplus Vogeli-Bax 2007 — la
        # seconde voie de la campagne croisee (memes phi, meme
        # reference typique, memes theta) : helice P a 1,87 theta (a
        # 0,13 theta de la frontiere S-) contre S+ a 0,27 theta pour
        # Vuister-Bax — les deux voies canoniques divergent, la loi
        # n'est pas robuste a sa parametrisation a cet etalonnage ;
        # brin P a 1,60 theta.
        self.assertEqual(by[("si", "Hz")]["counts"],
                         {"S+": 2, "P": 4, "S-": 3})
        self.assertIn("NMR_Karplus_Helix", by[("si", "Hz")]["ids"])
        self.assertIn("NMR_Karplus_Sheet", by[("si", "Hz")]["ids"])
        self.assertIn("NMR_Karplus_Helix_VogeliBax2007", by[("si", "Hz")]["ids"])
        self.assertIn("NMR_Karplus_Sheet_VogeliBax2007", by[("si", "Hz")]["ids"])
        self.assertIn("SPEC_CO_Rot_AbInitio", by[("si", "Hz")]["ids"])
        self.assertIn("SPEC_CO_Rot_Dunham", by[("si", "Hz")]["ids"])
        self.assertIn("SPEC_CO13_Rot_MuRule", by[("si", "Hz")]["ids"])
        self.assertIn("SPEC_CO_Rot_Kratzer", by[("si", "Hz")]["ids"])
        self.assertIn("SPEC_CO_Rot_AlphaE", by[("si", "Hz")]["ids"])
        # Le complexe g-2 : les cinq contacts, la paire d'identifications
        # complète dans la même fibre — WP25 S+ à 0,6 U, WP20 S− à 3,7 U,
        # HVP P, HLbL S+. 2026-09-14 : HVP pi pi CMD-3 vs pre-moyenne
        # rejoint la fibre — premier contact exp-vs-exp de la machine
        # (deux fabrications experimentales du meme terme, ecart porte
        # tel que publie par le PRL CMD-3, S- a 3.7 U, moyenne
        # KLOE-dominee declaree). Deux mots opposes, aucun choisi.
        self.assertEqual(by[("1", "1e-11")]["counts"],
                         {"S+": 2, "P": 1, "S-": 2})
        self.assertIn("AMU_Delta_WP25", by[("1", "1e-11")]["ids"])
        self.assertIn("AMU_exp_minus_WP20", by[("1", "1e-11")]["ids"])
        self.assertIn("HVP_LO_lat_vs_ee", by[("1", "1e-11")]["ids"])
        self.assertIn("HLbL_lat_vs_pheno", by[("1", "1e-11")]["ids"])
        self.assertIn("HVP_Pipi_CMD3_vs_PreAvg", by[("1", "1e-11")]["ids"])
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
                         {"S+": 4, "P": 2, "S-": 10})
        self.assertIn("CKM_Row1_Unitarity", by[("1", "1")]["ids"])
        self.assertIn("H0_Ecart_Planck_SH0ES", by[("1", "1")]["ids"])
        self.assertIn("Bertsch_Xi_Unitary", by[("1", "1")]["ids"])
        self.assertIn("KSS_EtaS_He4", by[("1", "1")]["ids"])
        self.assertIn("KSS_EtaS_QGP", by[("1", "1")]["ids"])
        # 2026-09-14 : P31_Lamb_Dirac — la dette historique de Dirac seul
        # (degenerescence 2S1/2 = 2P1/2 vs Lamb shift mesure) : S- a 20
        # theta, score normalise, grammaire P30_Kato_gaussian.
        self.assertIn("P31_Lamb_Dirac", by[("1", "1")]["ids"])
        # 2026-09-14 : la fibre (si, MHz) s'ouvre sur le couplet Lamb —
        # Mohr P a 1,1416 theta (au cheveu de la frontiere S+) contre
        # Erickson S- a 4,7141 theta : meme mesure Lundeen-Pipkin 1981,
        # deux calculs QED de la meme epoque qui se disputaient 0,048
        # MHz — la machine tranche ou les physiciens debattaient.
        self.assertEqual(by[("si", "MHz")]["counts"],
                         {"S+": 0, "P": 1, "S-": 1})
        self.assertIn("P31_Lamb_Mohr", by[("si", "MHz")]["ids"])
        self.assertIn("P31_Lamb_Erickson", by[("si", "MHz")]["ids"])
        # Le contact H(z) bas-z ouvre la fibre des modules de distance :
        # extract DEMO (fiducial H0=70 déclaré), la fabrication Planck
        # manque les bins de 0,117 mag — dette au-delà de 2 theta.
        # 2026-09-13 soir : la paire LITERATURE (Pantheon+ ancrée
        # Planck 0,0695 / ancrée SH0ES 0,2314, deux S-) — même fibre,
        # deux ancrages déclarés, dettes écrites.
        # 2026-09-14 : la paire V2 (amplitude MU_SH0ES native, dette de
        # forme supprimée) — courbe Planck posée : S- à 6,4 theta (miroir
        # de V1_SH0ES) ; courbe SH0ES posée : S+ à 0,897 theta — le
        # premier S+ de la fibre, au cheveu.
        self.assertEqual(by[("1", "mag")]["counts"],
                         {"S+": 1, "P": 0, "S-": 4})
        self.assertIn("H0_Hz_SNe_LOWZ_DEMO", by[("1", "mag")]["ids"])
        self.assertIn("H0_Hz_SNe_LOWZ_LIT_PLANCK", by[("1", "mag")]["ids"])
        self.assertIn("H0_Hz_SNe_LOWZ_LIT_SH0ES", by[("1", "mag")]["ids"])
        self.assertIn("H0_Hz_SNe_LOWZ_V2_PLANCK", by[("1", "mag")]["ids"])
        self.assertIn("H0_Hz_SNe_LOWZ_V2_SH0ES", by[("1", "mag")]["ids"])

    def test_all_16_open_contacts_sweep_invariant(self) -> None:
        rows = run_registers()["rows"]
        o_ids = [r["id"] for r in rows
                 if r["id"].startswith("O") and r["statut"] == "ouverte"]
        # 2026-09-14 : 16 -> 17 contacts ouverts de la série O (O17 H2
        # anharmonique rejoint la série ; invariance de balayage conservée).
        # 2026-09-14 (soir) : 17 -> 18 (O18 H2 tare de lecture, pendant
        # disciplinaire d'O17).
        self.assertEqual(len(o_ids), 18)
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
