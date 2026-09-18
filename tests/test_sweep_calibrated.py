#!/usr/bin/env python3
"""Balayage calibré (chantier A2) — l'invariance d'unités à même
étalonnage, figée d'abord sur les 46 contacts, étendue à 48 (V2, 2026-09-14).

Contexte : `street_sweep` historique juge au θ seul et conserve, par
gel, les « deux instruments » de CKM / HVP / HLbL (tests dédiés dans
test_verdicts_online.py — ne pas y toucher). La campagne A2 a montré
que ces divergences sont la comparaison de deux seuils, pas un effet
d'unités. `street_sweep_calibrated` rejoue le balayage au seuil gelé
du contact (U si decide=U, θ sinon) : là, et seulement là, le mot doit
être identique sous les quatre paquets pour CHAQUE contact du registre.

Propriétés figées :
- 46/46 au gel A2, puis 48/48 après V2 : mot calibré identique au mot
  home sous les 4 paquets ;
- zéro units_kill : aucun paquet n'est illicite pour une dimension
  portée par le registre ;
- CKM porte thr = U = 0,0014 (étalonnage U déclaré, k = 2) — la
  valeur qui séparait les deux instruments.
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from mvcg.registers import CONTACTS  # noqa: E402
from mvcg.verdict_register import street_sweep_calibrated  # noqa: E402


class TestSweepCalibrated(unittest.TestCase):
    def test_all_contacts_invariant_at_same_calibration(self) -> None:
        self.assertEqual(len(CONTACTS), 122)  # 56 + chantier PRINCIPES x4 (PF1 RG 1-loop S- attendu, PF2 croisement 25 THz, PF3 jeu tau5, PF4 vide 122,95, 2026-09-14) + PF1b RG 2-boucles (le calcul designe par le volet IV : best spread 0,337 vs coincidence 1 %, S- a 654 theta — le 2-boucles ne ferme pas la dette de PF1, coefficients SM empruntes MV1983 geles datés, 2026-09-15) + chantier PSY-RMN x2 (PF5 coherence de l'unite psy S- a 9,0 theta, PF6 prediction RMN recomputablee S- a 8,4e35 theta, 2026-09-14) + chantier H(z) F4 x2 (PF7 arithmetique du tableau des plans S+ a 0,046 theta, PF8 tension equation/revendication S- a 331 theta, 2026-09-14) + Rydberg voie 2 (campagne croisee, 2026-09-14) + O17 H2 anharmonique (tare de declaration, 2026-09-14) + O18 H2 tare de lecture (pendant d'O17, 2026-09-14) + P31 Lamb x3 (Dirac dette historique / Mohr P au cheveu / Erickson S-, chantier atome, 2026-09-14) + P32 Lamb moderne (la dette se ferme : QED reevaluee S+ sur le temoin commun, 2026-09-14) + les quatre P affines (D-bump REFINED-P-CONTACTS.md : O19 CO2 Fine, O20 carbone D Fine, SPEC Kratzer Fine, P31 Mohr_K2 — runner et sha256 strictement partagés avec l'original, 2026-09-14) + chantier L4 gyrocorpus x5 (transposition corpus hors-programme gap gyroscopique, table LITERATURE-HP2027, 2026-09-14 : volet 1 x3 + volet 2 deux nombres lies x2) + chantier CORR corridor croise x2 (tensions inter-campagnes du corridor E, table LITERATURE-E2026, 2026-09-14) + chantier LOI-HARMONIQUE x3 (LH_KO6_Racines S- a 14 U — deux sqf publies fausses, LH_Muon_Quinte S+ 0,059 theta, LH_Z_Diagonale S+ 0,030 theta, 2026-09-15) + chantier LOI-HARMONIQUE 2e fournee G4/G6 x3 (LH_Strange_Quarte P 1,21 theta, LH_Bottom_G6 P 1,30 theta, LH_Bottom_Arith P 1,24 theta — attendus S- gelés non tenus, la frontiere de la loi est grise pas rouge, 2026-09-15) + chantier LOI-HARMONIQUE 3e fournee G7/G9/G10 x3 (LH_Koide_Q S+ 9,2e-5 theta — le plus serre du registre, LH_Zmax_Modes S+ 0,022 theta, LH_Addendum_Corps S- 1 U — attendus tous tenus, 2026-09-15) + chantier LOI-HARMONIQUE 4e fournee G3/G5 x2 (LH_Up_G3 S+ 0,307 theta, LH_Charm_G5 S+ 0,149 theta — clôture du sextuor G1-G6, attendus tenus, 2026-09-15) + chantier LOI-HARMONIQUE 5e fournee C1/G12 x2 (LH_Anu_Gamme S+ 0,117 theta — gamme koilon 2^(1/12) tient sur la table ANU 1908, LH_Alpha_DoubleUsage S- 63 theta — dette d'identification alpha, 2026-09-15) + chantier LOI-HARMONIQUE 6e fournee C3 x1 (LH_Anu_Pont_RMS S- 13,8 theta — attendu S+ non tenu : RMS 3,376 % sur la fenêtre vérifiable Z=1-12, le bore 10B du corpus porte l'écart, hors bore 1,225 % cohérent avec le 1,42 % déclaré — dette table Z=13-92 nommée, 2026-09-16) + chantier TRANSVERSALE x1 (TR_Davies_TrioMesons S+ 0,71 theta — trio mésonique cité par « La Constante ALPHA » 2022 citant Davies, pire écart 0,714 % vs theta 1 % gelé « presque exactement », 2026-09-16) + chantier TRANSVERSALE B2-B6 x5 (B2 conv4 moyenne ki S- 0,15 theta attendu S+ non tenu, B3 conv4 seuil Z25 S+ 0,76 theta TENU — seul tenu des 5, B4 alcalins S- 4,7 theta, B5 MDA suite stable S- 290 theta, B6 deltaANU S- 83 theta — tables Occult Chemistry 1908 double transcription gelee + EI alcalins 2018 + graphe deltaANU Plotnikov 2022, dettes nommees : calibration bande B3, double lecture B5, coherence interne B6, 2026-09-17 soir + chantier TRANSVERSALE C1 (TR_TOV_Sn195Pt S- a 10,9 theta — S_n(196Pt) NUBASE2020 7921,9 keV vs 6,5 MeV declare article TOV 2025-01-29, la valeur sert d'intrant a l'exemple exp(-6,5/0,086) de « Linéarisation » — trou de TR_KZN_ExpQ65 bouche, 2026-09-18 + chantier TRANSVERSALE PRED-23 (TR_PRED23_EDMNeutron S- a 6,7 theta — pesee de type plafond sur une veille, mu_loc = retard de veille = 3,0/1,8 - 1 = 66,7 %, la borne du corpus coincide EXACTEMENT avec Pendlebury 2015 et la frontiere est Abel 2020 — la borne est vraie physiquement, la veille « en cours » figee d'avant 2020, ouvre la fibre (si, e.cm), 2026-09-18 + chantier ÉLECTRON x4 (E1 assemblage H/H+ S- a 50 theta — charge nette unitaire +2 e vs +1 e de l'ion, quantum de charge de l'ANU indéclaré, lecture ±e/2 escape nommée ; E2 masse uud S- a 3,35 theta — 9,4 MeV Part.3 vs 8,81 MeV Part.1, dette de datation ; E3 bilan argile S- a 200 theta — equation « 4 + 3x(-2)/2 + 2 = -1 » fausse telle qu'ecrite (+3), coquille de signe, bilan physique juste ; E4 modele lineaire S- a 340 theta — ANU = 46,9Z − 151,2 ne reproduit aucune de ses 6 ancres, regime lourd 0,87 % nommé, document source des claims deja peses LH_Anu_Gamme/B2 et B6, 2026-09-18)
        for c in CONTACTS:
            st = street_sweep_calibrated(c.id)
            licites = [r for r in st["rows"] if not r["units_kill"]]
            self.assertEqual(len(licites), 4,
                             f"{c.id}: units_kill inattendu en balayage calibré")
            for r in licites:
                self.assertEqual(r["verdict"], st["home_verdict"],
                                 f"{c.id}: mot {r['verdict']} en packet "
                                 f"{r['packet']} != home {st['home_verdict']} "
                                 "à même étalonnage")
                self.assertAlmostEqual(r["thr"], st["thr"], places=15)

    def test_ckm_calibrated_carries_u_threshold(self) -> None:
        # Le seuil qui séparait les deux instruments : U = 0,0014
        # (decide=U, k=2). À même étalonnage, chaque paquet rejoint
        # le mot home — on compare au registre live, sans écrire le
        # mot ici (garde anti-tautologie de reproduce : jamais de mot
        # voisin dans un fichier de classification).
        st = street_sweep_calibrated("CKM_Row1_Unitarity")
        self.assertEqual(st["calibration"], "U")
        self.assertAlmostEqual(st["thr"], 0.0014, places=12)
        for r in st["rows"]:
            self.assertEqual(r["verdict"], st["home_verdict"])
            self.assertAlmostEqual(r["delta"], 0.0016000000000000458,
                                   places=12)

    def test_g2_calibrated_restores_home_words(self) -> None:
        # HVP et HLbL : à même étalonnage, le balayage rejoint le mot
        # home — les divergences historiques n'étaient que le changement
        # de seuil, jamais un effet d'unités. Mots comparés au live,
        # jamais écrits ici (même garde anti-tautologie).
        for cid in ("HVP_LO_lat_vs_ee", "HLbL_lat_vs_pheno"):
            st = street_sweep_calibrated(cid)
            self.assertEqual(st["calibration"], "U")
            for r in st["rows"]:
                self.assertEqual(r["verdict"], st["home_verdict"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
