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
        self.assertEqual(idx["n"], 122)  # série en ligne au 2026-09-13 + chantier PRINCIPES x4 (PF1 RG 1-loop S- a 655,8 theta — delta 32,79, la coincidence 1 % n'est pas tenue au 1-loop pur, l'article renvoie au 2-boucles ; PF2 croisement 25 THz S+ a 0,34 theta ; PF3 jeu tau5 S+ a 0,11 theta ; PF4 vide 122,95 S+ a 0,08 theta, 2026-09-14) + chantier PSY-RMN x2 (PF5 : coherence interne du volet I, unite psy — l'equation-image donne hbar_N = 1,054e-34 J.s, l'exemple-texte 5,25e-31 J pour 500 psy sur 1 s (coherent avec 1,054e-33) : S- a 9,0 theta ; PF6 : prediction RMN des ANU recompute sous l'identification declaree c_éth = c_N = 1e9 c — 4,19e32 T vs 0,5 mT revendique : S- a 8,4e35 theta, 2026-09-14) + Bertsch + KSS×2 + AMU WP25 (la paire complète) + H0 (chantier local) + H(z) bas-z DEMO (chantier local) + H(z) bas-z LITERATURE ×2 ancrages (chantier local 2026-09-13 soir) + H(z) bas-z V2 ×2 courbes (MU_SH0ES natif, 2026-09-14) + SPEC CO rotationnel ×2 (ab initio / Dunham, 2026-09-14) + SPEC CO isotopologue (regle mu, 2026-09-14) + SPEC CO Kratzer (prediction croisee, P au cheveu, 2026-09-14) + SPEC CO levier alpha_e (residu vintage, 2026-09-14) + HVP pi pi CMD-3 vs pre-moyenne (campagne croisee, exp-vs-exp, 2026-09-14) + Karplus Vogeli-Bax 2007 ×2 (campagne croisee, seconde voie, 2026-09-14) + Rydberg voie 2 (R_∞ depuis alpha et me*c^2, certification CODATA, 2026-09-14) + O17 H2 anharmonique (Dunham ordre 1 vs fondamental declare arrondi, S- a 2,94 theta — tare de declaration pesee, 2026-09-14) + O18 H2 tare de lecture (meme transport, reference relue a u = 5/sqrt(3), S+ a 0,51 theta — le verdict pese des declarations pas des physiques, 2026-09-14) + P31 Lamb x3 (chantier atome : Dirac S- dette historique 20 theta, Mohr P au cheveu 1,14 theta, Erickson S- 4,71 theta — meme mesure, deux calculs QED de la meme epoque, deux verdicts, 2026-09-14) + P32 Lamb moderne (la dette se ferme : QED Pachucki 2001 reevaluee vs le MEME temoin Lundeen-Pipkin, S+ a 0,30 theta — l'arc P31 se clot, 2026-09-14) + les quatre P affines (D-bump REFINED-P-CONTACTS.md, gelé avant run, 2026-09-14 : O19 CO2 nu3 Fine S- a 2405 U, O20 carbone D Fine S- a 46,4 U, SPEC Kratzer Fine S- a 19,1 U — trois dettes de modele nommees que le P grossier cachait — et P31 Mohr_K2 S+ a 0,57 U : le mot dépend de la couverture, a k=1 le meme ecart est P) + chantier L4 gyrocorpus x5 (transposition du corpus hors-programme gap gyroscopique, table LITERATURE-HP2027, vintage distinct declare, 2026-09-14 : volet 1 — gap universel S+ a 0,35 U, branche P1-P2 au regime fin AMP 0.15 a k2 S- a 56 U (retractation de l'addendum P3 pesee), fenetre inertielle D3 par la branche rapportee a la ligne vide P AU CHEVEU a 1,20 U (pont tenu indirectement) ; volet 2 DEUX NOMBRES LIES — kappa_eff implicite de la pente par Kelvin nu S- a 214 U (dette de circulation x22,4, sensibilite log x12,9 consignee), gap par circulation pure S- a 30 U (le gap est une dette de structure, pas de circulation)) + chantier CORR corridor croise x2 (tensions inter-campagnes du corridor E, table LITERATURE-E2026, 2026-09-14 : optimum de stabilite E63 n=14 vs minimum d'energie E65 n=18 S- a 2,83 U (facettes decouplees, E68 qualitative publiee en verdict) ; point E61 kappa=0,05 vs bord bas fenetre E64-A 0,075 S- a 3,46 U (tare de temps de vol 90 vs 180 nommee)) + chantier TRANSVERSALE B2-B6 x5 (B2 conv4 moyenne ki S- 0,15 theta, B3 conv4 seuil Z25 S+ 0,76 theta TENU, B4 alcalins S- 4,7 theta, B5 MDA suite stable S- 290 theta, B6 deltaANU S- 83 theta — tables gelées Occult Chemistry 1908 / EI 2018 / deltaANU 2022, 2026-09-17 soir + chantier TRANSVERSALE C1 (TR_TOV_Sn195Pt S- a 10,9 theta — S_n(196Pt) recompute NUBASE2020 7921,9 keV vs 6,5 MeV declare, article TOV 2025-01-29, 2026-09-18 + chantier TRANSVERSALE PRED-23 (TR_PRED23_EDMNeutron S- a 6,7 theta — plafond EDM neutron 3e-26 e·cm vs Abel 2020 1,8e-26, veille figee 2015, 2026-09-18 + chantier ÉLECTRON x4 (E1 assemblage H/H+ S- 50 theta, E2 masse uud S- 3,35 theta, E3 bilan argile S- 200 theta, E4 modele lineaire S- 340 theta — série decembre 2020, 4 S-, 2026-09-18)
        self.assertEqual(len(idx["fibres"]), 18)  # 12 + (si, MHz) ouverte par le couplet Lamb P31 (2026-09-14) + (si, 1) ouverte par le chantier PRINCIPES (PF4 S+ / PF1 S-, 2026-09-14) + (si, J) et (si, T) ouvertes par le chantier PSY-RMN (PF5 et PF6, deux S- de dette interne au corpus, 2026-09-14) + (si, MeV) ouverte par le chantier LOI-HARMONIQUE (LH_Muon_Quinte et LH_Z_Diagonale, deux S+ θ, 2026-09-15)
        by = {(f["packet"], f["dimension"]): f for f in idx["fibres"]}
        # Les trois fibres phares de la série O :
        # 2026-09-14 : Rydberg voie 2 rejoint la fibre — R_∞ calculee
        # depuis alpha et me*c^2 (CODATA 2018 declares), S+ a 0,017 U :
        # certification pesee de la coherence interne du catalogue
        # (circularite declaree, pendant du Dunham) ; la fibre eV a sa
        # case de reference pour les contacts qui la citent.
        # 2026-09-14 : chantier PRINCIPES — PF2 (E = h.f du pic 25 THz
        # = 0,1034 eV, coherence interne II x V, S+ a 0,34 theta) rejoint
        # la fibre eV : la case de reference des contacts d'energie a
        # maintenant un cousin de transposition de corpus.
        self.assertEqual(by[("si", "eV")]["counts"],
                         {"S+": 5, "P": 0, "S-": 3})
        self.assertIn("H1s_Rydberg_Voie2", by[("si", "eV")]["ids"])
        self.assertIn("PF2_Graviton_25THz", by[("si", "eV")]["ids"])
        # 2026-09-18 : chantier TRANSVERSALE PRED-23 — la pesée de
        # plafond EDM neutron ouvre la fibre (si, e·cm) : un seul
        # contact, S− à 6,7 θ (veille figée à Pendlebury 2015).
        self.assertEqual(by[("si", "e.cm")]["counts"],
                         {"S+": 0, "P": 0, "S-": 1})
        self.assertIn("TR_PRED23_EDMNeutron", by[("si", "e.cm")]["ids"])
        self.assertEqual(by[("1", "cm^-1")]["counts"],
                         {"S+": 5, "P": 2, "S-": 3})
        # 2026-09-14 : affinage « les quatre P » — O19 (CO2 nu3 VFF fine,
        # D-bump d'O2) et O20 (carbone D fine, D-bump d'O3) : les deux P
        # grossiers de la fibre passent S- a 2405 U et 46,4 U — le theta
        # tol.-labo cachait une dette de modele 1D, l'affinage la nomme.
        # Transport strictement identique (meme runner, meme sha256) :
        # seules les declarations d'incertitude ont change.
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
        self.assertIn("O19_CO2_nu3_Fine", by[("1", "cm^-1")]["ids"])
        self.assertIn("O20_Carbon_D_Raman_Fine", by[("1", "cm^-1")]["ids"])
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
                         {"S+": 2, "P": 4, "S-": 4})
        # 2026-09-14 : Kratzer Fine (D-bump, u(D0) 70 Hz -> u_delta déclarée
        # 5,10 Hz) — le P au cheveu du grossier (1,394 theta) passe S- a
        # 19,1 U : l'u(D0) NIST trop étroite fondait le suspense, la dette
        # nommée est vibrationnelle (Kratzer = équilibre, D0 = v=0).
        self.assertIn("NMR_Karplus_Helix", by[("si", "Hz")]["ids"])
        self.assertIn("NMR_Karplus_Sheet", by[("si", "Hz")]["ids"])
        self.assertIn("NMR_Karplus_Helix_VogeliBax2007", by[("si", "Hz")]["ids"])
        self.assertIn("NMR_Karplus_Sheet_VogeliBax2007", by[("si", "Hz")]["ids"])
        self.assertIn("SPEC_CO_Rot_AbInitio", by[("si", "Hz")]["ids"])
        self.assertIn("SPEC_CO_Rot_Dunham", by[("si", "Hz")]["ids"])
        self.assertIn("SPEC_CO13_Rot_MuRule", by[("si", "Hz")]["ids"])
        self.assertIn("SPEC_CO_Rot_Kratzer", by[("si", "Hz")]["ids"])
        self.assertIn("SPEC_CO_Rot_AlphaE", by[("si", "Hz")]["ids"])
        self.assertIn("SPEC_CO_Rot_Kratzer_Fine", by[("si", "Hz")]["ids"])
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
        # 2026-09-14 : chantier PRINCIPES — PF3 (recompute arithmetique
        # du jeu illustratif 10.exp(-0,023.22,67) = 5,9368 vs ~6,0
        # annonce, S+ a 0,11 theta) rejoint la fibre sans dimension :
        # la machine verifie l'arithmetique que la source declare comme
        # jeu, pas la physique.
        # 2026-09-14 : chantier H(z) F4 (volet V) — PF7 (F4 = e^{-beta S}
        # recompte depuis le tableau publie, 0,03484 vs 0,035, S+ a 0,046
        # theta, la machine verifie l'arithmetique du jeu comme PF3) et
        # PF8 (ecart H_filtree vs LCDM = 16,6 % a z=0 montant a 68,3 % a
        # z=2,1 sous l'equation publiee, S- a 331 theta, la revendication
        # <2 % n'est pas tenue, F_U non chiffre -> lecture neutre gelee)
        # rejoignent la fibre sans dimension.
        # 2026-09-15 : chantier LOI-HARMONIQUE — la machine pèse pour la
        # première fois une loi interne au corpus : LH_KO6_Racines
        # (S- a 14 U — deux valeurs de sqf publiees fausses sous la
        # definition standard du corpus, rad(63)=21 pas 7, rad(36)=6
        # pas 1, l'exclusion d'E6 s'effondre ; identites module-racines
        # exactes en extra) rejoint la fibre sans dimension.
        # 2026-09-15 (soir) : chantier LOI-HARMONIQUE 2e fournée G4/G6 —
        # LH_Bottom_Arith (P à 1,24 θ, « 5000/1,0593 ~ 4200 » recompté
        # 4 720,098 — dette arithmétique interne au corpus, pendant PF5)
        # rejoint la fibre sans dimension en P.
        # 2026-09-15 (nuit) : chantier LOI-HARMONIQUE 3e fournée G7/G9/G10
        # — LH_Zmax_Modes (S+ à 0,022 θ, le « ~ 179 » du corps tient au
        # seuil) et LH_Addendum_Corps (S- à 1 U, tension 180 « recomputé
        # exact » vs 179 — dette de déclaration type PF5) rejoignent la
        # fibre sans dimension.
        # 2026-09-15 (nuit) : chantier LOI-HARMONIQUE 5e fournée C1/G12 —
        # LH_Anu_Gamme (S+ à 0,117 θ, la gamme koïlon 2^(1/12) tient sur
        # la table ANU 1908 — les deux déclarations du corpus tiennent)
        # et LH_Alpha_DoubleUsage (S- à 63 θ, dette d'identification :
        # deux constantes sous un même symbole α, 630 % d'écart —
        # pendant PF6) rejoignent la fibre sans dimension.
        # 2026-09-17 (soir) : chantier TRANSVERSALE B2-B6 x5 — la fouille
        # transversale poursuit sur les contacts B de la prospective :
        # TR_CONV4_MoyenneKi (S- à 0,15 θ, attendu S+ non tenu : 92,22 %
        # des ANU dans la bande déclarée 80 %, moyenne 1,0828 vs 2^(1/12),
        # écart 2,20 %) + TR_CONV4_SeuilZ25 (S+ à 0,76 θ TENU — 1/66 seul
        # dépassement, Rn Z=86 k=0,990, bande [1;1,2] calibrée sur le
        # claim 80 %, dette nommée) + TR_CONV4_Alcalins (S- à 4,7 θ, K
        # Z=19 seul dépassement, Li tient à 0,048 %) + TR_MDA_SuiteStable
        # (S- à 290 θ, lecture multiplicative du premier terme vs
        # déclaration additive à 93,3 % au terme 10 — double lecture
        # gelée, équation-image perdue) + TR_ALPHA_DeltaANU (S- à 83 θ,
        # cohérence interne loi vs graphe Plotnikov 2022 — Sc 167 %, Li
        # 150 %, jamais pesé contre une vérité externe, dette nommée).
        self.assertEqual(by[("1", "1")]["counts"],
                         {"S+": 15, "P": 5, "S-": 32})
        self.assertIn("PF3_Tau5_Jeu", by[("1", "1")]["ids"])
        self.assertIn("PF7_F4_Recompute", by[("1", "1")]["ids"])
        self.assertIn("PF8_Hz_Filtrage_Ecart", by[("1", "1")]["ids"])
        self.assertIn("LH_KO6_Racines", by[("1", "1")]["ids"])
        self.assertIn("LH_Bottom_Arith", by[("1", "1")]["ids"])
        self.assertIn("LH_Zmax_Modes", by[("1", "1")]["ids"])
        self.assertIn("LH_Addendum_Corps", by[("1", "1")]["ids"])
        self.assertIn("LH_Anu_Gamme", by[("1", "1")]["ids"])
        self.assertIn("LH_Alpha_DoubleUsage", by[("1", "1")]["ids"])
        self.assertIn("LH_Anu_Pont_RMS", by[("1", "1")]["ids"])
        self.assertIn("LH_G11_MassShift", by[("1", "1")]["ids"])
        self.assertIn("LH_Fexp_Corridor", by[("1", "1")]["ids"])
        # 2026-09-16 (soir) : chantier TRANSVERSALE — fouille transversale
        # (articles 2022, index de l'écosystème) : TR_Davies_TrioMesons
        # (S+ a 0,71 theta, trio mésonique cité par « La Constante ALPHA »
        # 2022 citant Davies : muon/pion/kaon = 3/2, 2, 7 x 1/alpha x m_e,
        # pire écart 0,714 % vs theta 1 % gelé = « presque exactement » —
        # variante chargée gelée, neutres pion0 3,6 % et K0 1,5 % nommés,
        # ligne muon échole à LH_Muon_Quinte).
        # 2026-09-17 : chantier TRANSVERSALE 2e contact —
        # TR_Alpha_ProtonMuonNeuf (S- a 3,38 theta, attendu S+ non tenu :
        # « le muon vaut 200 fois… le proton 1800 fois… donc 9 fois » —
        # prémisse muon 3,38 %, proton 2,01 %, conclusion 1,33 % ;
        # l'inférence 1800/200 = 9 est exacte, l'erreur des prémisses
        # rondes se transmet à la conclusion) : la fibre sans dimension
        # passe {S+ 12, P 5, S- 23}.
        self.assertIn("TR_Davies_TrioMesons", by[("1", "1")]["ids"])
        self.assertIn("TR_Alpha_ProtonMuonNeuf", by[("1", "1")]["ids"])
        self.assertIn("TR_KZN_B11_Liaison", by[("1", "1")]["ids"])
        self.assertIn("TR_KZN_Sn132_Preference", by[("1", "1")]["ids"])
        self.assertIn("TR_KZN_ExpQ65", by[("1", "1")]["ids"])
        self.assertIn("E44_T0_LienHopf", by[("1", "1")]["ids"])
        self.assertIn("E44_Lk_PaireHopf", by[("1", "1")]["ids"])
        self.assertIn("E44_P3_Filaments", by[("1", "1")]["ids"])
        # 2026-09-17 (soir) : chantier TRANSVERSALE B2-B6 — les 5 contacts
        # rejoignent la fibre sans dimension (4 S- dont 1 attendu-S+ non
        # tenu, 1 S+ tenu) : voir commentaire du bloc counts ci-dessus.
        self.assertIn("TR_CONV4_MoyenneKi", by[("1", "1")]["ids"])
        self.assertIn("TR_CONV4_SeuilZ25", by[("1", "1")]["ids"])
        self.assertIn("TR_CONV4_Alcalins", by[("1", "1")]["ids"])
        self.assertIn("TR_MDA_SuiteStable", by[("1", "1")]["ids"])
        self.assertIn("TR_ALPHA_DeltaANU", by[("1", "1")]["ids"])
        self.assertIn("TR_TOV_Sn195Pt", by[("1", "1")]["ids"])
        self.assertIn("TR_ELECTRON_AssemblageH", by[("1", "1")]["ids"])
        self.assertIn("TR_ELECTRON_BilanArgile", by[("1", "1")]["ids"])
        self.assertIn("TR_ELECTRON_ModeleLineaire", by[("1", "1")]["ids"])
        # 2026-09-16 (nuit) : chantier LOI-HARMONIQUE 8e fournée —
        # LH_Fexp_Corridor (P à 1,78 theta, attendu S+ non tenu :
        # corridor des corrections harmoniques declare ±3 % vs deviation
        # max recompute 8,33 % depuis les colonnes voisines de la table
        # du corpus — 5 violations du plancher 0,973 dont le charm
        # lui-meme, aucune ligne ne coincide avec son F imprime, « down
        # 1,028 » et bottom absents) : la fibre sans dimension passe
        # {S+ 11, P 5, S- 22}.
        # 2026-09-16 (journee) : chantier E44 — nucléation de
        # l'enlacement, pesée des déclarations de la note d'audit E44
        # (31/07/2026, protocole pré-enregistré haché SHA-256) : la
        # machine ne rejoue pas la simulation GP, elle pèse ses
        # déclarations gelées et leur arithmétique interne —
        # E44_T0_LienHopf (S+ a 0,06 theta, détecteur validé déclaré
        # 0,994 vs attendu 1) et E44_Lk_PaireHopf (S+ a 0,04 theta,
        # moyenne |Lk| = 1,004 des trois estimations, robustesse au
        # seuil 0,5 tenue) rejoignent la fibre ; E44_P3_Filaments
        # (S- a 25 theta, médiane déclarée 14 vs prédiction 4 ± 2 —
        # écart 5 sigma, le corpus statue la réfutation lui-même et la
        # machine confirme le mot) : la fibre sans dimension passe
        # {S+ 11, P 4, S- 22}.
        # 2026-09-16 : chantier LOI-HARMONIQUE 6e fournée C3 —
        # LH_Anu_Pont_RMS (S- a 13,8 theta, RMS recompote 3,376 % vs
        # 1,42 % declares ; hors bore 10B la fenetre verifiable Z=1-12
        # donne 1,225 % — c'est l'isotope 10B choisi par le corpus qui
        # casse la fenetre ; dette table Z=13-92 nommee).
        # 2026-09-16 (matin) : chantier LOI-HARMONIQUE 7e fournée G11 —
        # LH_G11_MassShift (S- a 20 022 theta, recompute strict de (21)
        # = 1,302e-4 vs 6,5e-8 declare : numerateur P_ext au lieu de
        # eps0.E^2, facteur 2, et P_K declare ne suit pas de ses propres
        # intrants, facteur ~159 — la prediction experimentale du corpus
        # est doublement non tenue sur sa propre arithmetique, cap
        # prospectif mecanique).
        # 2026-09-15 : chantier LOI-HARMONIQUE — ouverture de la fibre
        # (si, MeV) : LH_Muon_Quinte (S+ a 0,059 theta, quinte 3/2 x
        # 1/alpha) et LH_Z_Diagonale (S+ a 0,030 theta, m_p/alpha/
        # sqrt(2)) — les deux instances les plus solides de la loi
        # harmonique, entrées CODATA-2018 et PDG-2024 gelées datées.
        # 2026-09-15 (soir) : chantier LOI-HARMONIQUE 2e fournée G4/G6 —
        # LH_Strange_Quarte (P à 1,21 θ) et LH_Bottom_G6 (P à 1,30 θ)
        # rejoignent la fibre MeV en P : les attendus S- gelés ne sont
        # pas tenus, la frontière de la loi harmonique côté quarks est
        # grise (bande P 1–2 θ), pas rouge.
        # 2026-09-15 (nuit) : 4e fournée G3/G5 — LH_Up_G3 (S+ à 0,307 θ,
        # dans la fourchette PDG) et LH_Charm_G5 (S+ à 0,149 θ, 0,95 σ)
        # rejoignent la fibre MeV : clôture du sextuor G1-G6.
        self.assertEqual(by[("si", "MeV")]["counts"],
                         {"S+": 6, "P": 2, "S-": 3})
        self.assertIn("LH_Muon_Quinte", by[("si", "MeV")]["ids"])
        self.assertIn("LH_Z_Diagonale", by[("si", "MeV")]["ids"])
        self.assertIn("LH_Strange_Quarte", by[("si", "MeV")]["ids"])
        self.assertIn("LH_Bottom_G6", by[("si", "MeV")]["ids"])
        self.assertIn("LH_Up_G3", by[("si", "MeV")]["ids"])
        self.assertIn("LH_Charm_G5", by[("si", "MeV")]["ids"])
        # 2026-09-17 : chantier TRANSVERSALE / B1 — TR_KZN_Modele_Grille
        # (S- a 6,18 theta : RMS 12,36 % du modele k(Z,N) transcrit vs
        # NUBASE2020 sur 235 noyaux stables du domaine declare, le premier
        # S- de la fibre MeV — attendu S+ non tenu, prix en justesse du
        # facteur 1e5 revendique) rejoint la fibre MeV.
        self.assertIn("TR_KZN_Modele_Grille", by[("si", "MeV")]["ids"])
        self.assertIn("TR_ELECTRON_MasseUUD", by[("si", "MeV")]["ids"])
        # 2026-09-17 (soir) : 2e fournee k(Z,N) — les deux premiers S+
        # de la famille (TR_KZN_FusionDT_Liaisons 0,56 theta, donnees
        # standard D/T/4He citees correctement ; TR_KZN_TableComparaison
        # 0,10 theta, D+D a deux canaux non declares nommee hors mu_loc)
        # et le S- de sensibilite (TR_KZN_SensibiliteShell, 783 theta :
        # 0,1 MeV/% declare vs 0,006 recompute du modele gele) ;
        # TR_KZN_ExpQ65 (S- 5,95 theta, dette arithmetique exp(-75,6))
        # rejoint la fibre sans dimension.
        self.assertIn("TR_KZN_FusionDT_Liaisons", by[("si", "MeV")]["ids"])
        self.assertIn("TR_KZN_TableComparaison", by[("si", "MeV")]["ids"])
        self.assertIn("TR_KZN_SensibiliteShell", by[("si", "MeV")]["ids"])
        # 2026-09-14 : chantier PRINCIPES — ouverture de la fibre (si, 1) :
        # PF4 (log10(rho_Planck/rho_Lambda) recompute = 122,945 vs 122
        # revendique, S+ a 0,08 theta) et PF1 (dispersion 1-loop minimale
        # des 4 couplages = 0,338, la coincidence a 1 % n'est pas tenue
        # au 1-loop pur, S- a 655,8 theta — l'article IV renvoie lui-meme
        # au 2-boucles, c'est une information pas un accident).
        # 2026-09-15 : chantier PF1b — PF1b (meme transport au 2-boucles,
        # coefficients SM empruntes Machacek-Vaughn 1983 geles datés,
        # b_njn = +10 declare : best spread 0,337, S- a 654 theta —
        # le calcul que la source designe ne ferme pas la dette) rejoint
        # la fibre : le couplet PF1/PF1b pese un ordre de calcul et son
        # ordre superieur sur la meme revendication.
        self.assertEqual(by[("si", "1")]["counts"],
                         {"S+": 2, "P": 0, "S-": 2})
        self.assertIn("PF4_Vide_Catastrophe", by[("si", "1")]["ids"])
        self.assertIn("PF1_RG_Unification", by[("si", "1")]["ids"])
        self.assertIn("PF1b_RG_Unification_2Loop", by[("si", "1")]["ids"])
        # 2026-09-15 (nuit) : chantier LOI-HARMONIQUE 3e fournée —
        # LH_Koide_Q (S+ à 9,2e-5 θ, le plus serré du registre : la loi
        # empirique de Koide tient sur PDG-2024 gelé) rejoint la fibre.
        self.assertIn("LH_Koide_Q", by[("si", "1")]["ids"])
        # 2026-09-14 : chantier PSY-RMN — ouverture des fibres (si, J) et
        # (si, T) : PF5 (unite psy, coherence interne volet I — ecart
        # structurel d'un facteur 10 entre l'equation-image et l'exemple-
        # texte, S- a 9,0 theta) et PF6 (prediction RMN des ANU recompute
        # sous l'identification declaree c_éth = c_N = 1e9 c : 4,19e32 T
        # vs 0,5 mT, S- a 8,4e35 theta). Deux S- de dette interne au
        # corpus : les formules etaient publiees en images, la machine les
        # a transcrites (tables gelees, protocole PSY-RMN) puis pesees.
        self.assertEqual(by[("si", "J")]["counts"],
                         {"S+": 0, "P": 0, "S-": 1})
        self.assertIn("PF5_Psy_Energie", by[("si", "J")]["ids"])
        self.assertEqual(by[("si", "T")]["counts"],
                         {"S+": 0, "P": 0, "S-": 1})
        self.assertIn("PF6_RMN_DeltaB", by[("si", "T")]["ids"])
        # 2026-09-14 : chantier CORR corridor croisé — deux tensions
        # inter-campagnes du corridor chiffrées pour la première fois :
        # optimum de stabilité E63 (n=14) vs minimum d'énergie E65 (n=18)
        # S- à 2,83 U (facettes découplées, verdict publié) ; point E61
        # (κ=0,05, t=90) vs bord bas de fenêtre E64-A (0,075, t=180)
        # S- à 3,46 U (tare de temps de vol nommée).
        self.assertIn("CORR_Stabilite_Energie", by[("1", "1")]["ids"])
        self.assertIn("CORR_Fenetre_Point", by[("1", "1")]["ids"])
        self.assertIn("L4_Gap_Universel", by[("1", "1")]["ids"])
        self.assertIn("L4_Branche_k2_RegimeFin", by[("1", "1")]["ids"])
        self.assertIn("L4_Fenetre_Branche", by[("1", "1")]["ids"])
        self.assertIn("L4_Kappa_Eff", by[("1", "1")]["ids"])
        self.assertIn("L4_Kelvin_Gap", by[("1", "1")]["ids"])
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
                         {"S+": 2, "P": 1, "S-": 1})
        # 2026-09-14 : Mohr_K2 — meme transport, memes lignes GUM, couverture
        # k=2 (contact de couverture, pendant de la tare de lecture O18) :
        # le P a 1,14 uc de Mohr passe S+ a 0,57 U. Le mot dépend du niveau
        # de couverture déclaré — trace écrite, pas de correction en silence.
        self.assertIn("P31_Lamb_Mohr", by[("si", "MHz")]["ids"])
        self.assertIn("P31_Lamb_Erickson", by[("si", "MHz")]["ids"])
        self.assertIn("P31_Lamb_Mohr_K2", by[("si", "MHz")]["ids"])
        # 2026-09-14 : P32_Lamb_Modern ferme l'arc — QED reevaluee
        # (Pachucki 2001) vs le MEME temoin Lundeen-Pipkin : S+ a 0,3046
        # theta. Le temoin qui valait P (Mohr) et S- (Erickson) contre
        # les theories vintage devient S+ contre la theorie reevaluee.
        self.assertIn("P32_Lamb_Modern", by[("si", "MHz")]["ids"])
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
        # 2026-09-14 (affinage « les quatre P ») : 18 -> 20 (O19 CO2 nu3
        # Fine et O20 carbone D Fine, D-bumps d'O2/O3 — invariance de
        # balayage conservée par les versions abs, vérifiée par la boucle).
        self.assertEqual(len(o_ids), 20)
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
