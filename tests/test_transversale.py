#!/usr/bin/env python3
"""Verrous du chantier TRANSVERSALE (fouille transversale, 2026-09-16).

Contact 103 TR_Davies_TrioMesons : trio mésonique cité par le corpus
(« La Constante ALPHA de Structure fine », 2022, citant Paul Davies).
Les valeurs gelées ci-dessous sont les sorties du runner au moment du
gel — toute évolution du code qui les déplace fait échouer le test.
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from mvcg.registers import CONTACTS, run_contact  # noqa: E402
from mvcg.transversale import (  # noqa: E402
    tr_alpha_deltaanu,
    tr_alpha_proton_muon,
    tr_b11_liaison,
    tr_conv4_alcalins,
    tr_conv4_moyenne_ki,
    tr_conv4_seuil_z25,
    tr_electron_bilan_argile,
    tr_electron_h_assemblage,
    tr_electron_masse_uud,
    tr_electron_modele_lineaire,
    tr_davies_trio,
    tr_kzn_comparaison,
    tr_kzn_expq65,
    tr_kzn_fusion,
    tr_kzn_grille,
    tr_kzn_sensibilite,
    tr_mda_suite_stable,
    tr_pred23_edm,
    tr_sn132_liaison,
    tr_tov_sn195pt,
)


def _contact(cid: str) -> dict:
    c = next(x for x in CONTACTS if x.id == cid)
    return run_contact(c)


class TestDaviesTrio(unittest.TestCase):
    def test_mu_gelé(self):
        # mu_loc = écart relatif maximal des trois rapports mesurés
        # (PDG-2024) sur déclarés (alpha 137,036 gelée verbatim) —
        # le kaon est la pire ligne : 0,714 %.
        self.assertAlmostEqual(tr_davies_trio()[0],
                               0.0071407611826164175, delta=1e-15)
        _, x = tr_davies_trio()
        self.assertEqual(x["pire_ligne"], "kaon±")
        self.assertAlmostEqual(x["ecarts_relatifs"]["muon"],
                               0.0059073673470992905, delta=1e-15)
        self.assertAlmostEqual(x["ecarts_relatifs"]["pion±"],
                               0.003428150630794602, delta=1e-15)
        # variantes neutres : la tension nommée (corpus sans ±/0)
        self.assertAlmostEqual(x["neutres"]["pion0"]["delta"],
                               0.0362276755267551, delta=1e-15)
        self.assertAlmostEqual(x["neutres"]["K0"]["delta"],
                               0.0151664373929572, delta=1e-15)

    def test_attendu_splus_tenu(self):
        # attendu gelé S+ (le corpus dit « presque exactement ») ; le run
        # confirme : pire écart 0,714 % vs theta 1 % -> S+ à 0,71 theta.
        r = _contact("TR_Davies_TrioMesons")
        self.assertEqual(r["expected"], "S+")
        self.assertEqual(r["verdict"], "S+")
        self.assertFalse(r["b3_fail"])
        self.assertAlmostEqual(r["mu_loc"], 0.0071407611826164175,
                               delta=1e-15)
        self.assertIsNone(r["units_kill"])


class TestAlphaProtonMuon(unittest.TestCase):
    def test_mu_gelé(self):
        # mu_loc = écart relatif maximal des trois rapports mesurés
        # (PDG-2024) sur déclarés — la prémisse muon « 200 » est la
        # pire ligne : 3,384 %.
        self.assertAlmostEqual(tr_alpha_proton_muon()[0],
                               0.033841414938328374, delta=1e-15)
        _, x = tr_alpha_proton_muon()
        self.assertEqual(x["pire_ligne"], "muon/electron")
        self.assertAlmostEqual(x["ecarts_relatifs"]["proton/electron"],
                               0.020084818569588103, delta=1e-15)
        self.assertAlmostEqual(x["ecarts_relatifs"]["proton/muon"],
                               0.013306292599586822, delta=1e-15)
        # l'inférence interne du corpus (1800/200) est exacte
        self.assertEqual(x["inference_interne"], 9.0)

    def test_attendu_splus_non_tenu(self):
        # attendu gelé S+ (le corpus énonce 200, 1800 et « donc » 9
        # comme des faits) ; le run corrige : pire écart 3,38 % vs
        # theta 1 % -> S- à 3,38 theta — l'inférence « donc » est
        # arithmétiquement exacte, ce sont les prémisses rondes qui
        # portent l'écart et le transmettent à la conclusion (1,33 %).
        r = _contact("TR_Alpha_ProtonMuonNeuf")
        self.assertEqual(r["expected"], "S+")
        self.assertEqual(r["verdict"], "S-")
        self.assertTrue(r["b3_fail"])
        self.assertAlmostEqual(r["mu_loc"], 0.033841414938328374,
                               delta=1e-15)
        self.assertIsNone(r["units_kill"])


class TestB11Liaison(unittest.TestCase):
    def test_mu_gelé(self):
        # mu_loc = écart relatif de B/A NUBASE2020 (6,927732 MeV, excès
        # de masse Δ = 8667,708 keV ligne 011 0050, conversion u et
        # masses H/n CODATA-2018) sur déclaré 6,8 = 1,878 %.
        self.assertAlmostEqual(tr_b11_liaison()[0],
                               0.018784185943439002, delta=1e-15)
        _, x = tr_b11_liaison()
        self.assertAlmostEqual(x["BA_NUBASE2020_MeV"],
                               6.927732464415385, delta=1e-12)
        self.assertAlmostEqual(x["BA_declare_MeV"], 6.8, delta=1e-15)
        self.assertAlmostEqual(x["B_totale_MeV"],
                               76.20505710856924, delta=1e-12)

    def test_attendu_splus_tenu_justesse(self):
        # attendu gelé S+ ; le run tient de justesse : 1,878 % vs
        # theta 2 % = 0,94 theta — le calage deltashell laisse un
        # résidu visible pile sous le seuil.
        r = _contact("TR_KZN_B11_Liaison")
        self.assertEqual(r["expected"], "S+")
        self.assertEqual(r["verdict"], "S+")
        self.assertFalse(r["b3_fail"])
        self.assertAlmostEqual(r["mu_loc"], 0.018784185943439002,
                               delta=1e-15)
        self.assertIsNone(r["units_kill"])


class TestSn132Preference(unittest.TestCase):
    def test_mu_gelé(self):
        # mu_loc = écart relatif maximal des deux B/A NUBASE2020 sur
        # déclarés — la colonne 132Sn est la pire : 0,537 %.
        self.assertAlmostEqual(tr_sn132_liaison()[0],
                               0.005372251109505455, delta=1e-15)
        _, x = tr_sn132_liaison()
        self.assertEqual(x["pire_ligne"], "132Sn")
        self.assertAlmostEqual(x["lignes"]["132Sn"]["BA_NUBASE2020_MeV"],
                               8.354873090680154, delta=1e-12)
        self.assertAlmostEqual(x["lignes"]["133Sn"]["BA_NUBASE2020_MeV"],
                               8.310089218120146, delta=1e-12)
        # l'inégalité déclarée (« 132Sn favorisé ») est vraie côté
        # NUBASE2020 : le 133e neutron quitte la couche magique N=82.
        self.assertTrue(x["inegalite_NUBASE2020"])

    def test_attendu_splus_tenu(self):
        # attendu gelé S+ ; le run confirme : pire écart 0,537 % vs
        # theta 2 % = 0,27 theta — valeurs arrondies à deux chiffres.
        r = _contact("TR_KZN_Sn132_Preference")
        self.assertEqual(r["expected"], "S+")
        self.assertEqual(r["verdict"], "S+")
        self.assertFalse(r["b3_fail"])
        self.assertAlmostEqual(r["mu_loc"], 0.005372251109505455,
                               delta=1e-15)
        self.assertIsNone(r["units_kill"])


class TestKZNGrille(unittest.TestCase):
    def test_mu_gelé(self):
        # mu_loc = écart relatif RMS du modèle k(Z,N) transcrit vs
        # NUBASE2020 sur les 235 noyaux stables du domaine déclaré
        # (12 ≤ A ≤ 200, grille gelée, masses mesurées) — 12,36 %.
        self.assertAlmostEqual(tr_kzn_grille()[0],
                               0.12356358712158289, delta=1e-15)
        _, x = tr_kzn_grille()
        self.assertEqual(x["n_lignes"], 235)
        self.assertEqual(x["n_dans_2pct"], 3)
        self.assertAlmostEqual(x["max_relatif"],
                               0.2210438367430141, delta=1e-15)
        self.assertAlmostEqual(x["mediane_relatif"],
                               0.1094999098900542, delta=1e-15)
        # pire noyau : 12C, modèle 9,378 vs NUBASE 7,680 MeV
        self.assertEqual(x["pire_noyau"]["A"], 12)
        self.assertEqual(x["pire_noyau"]["Z"], 6)
        self.assertAlmostEqual(x["pire_noyau"]["ecart"],
                               0.2210438367430141, delta=1e-15)

    def test_regimes_ou_casse_le_calage(self):
        # découpage par bande du domaine déclaré (les mêmes que les
        # morceaux du modèle) : le calage casse aux deux extrémités,
        # tient le mieux en vallée.
        _, x = tr_kzn_grille()
        r = x["regimes"]
        self.assertEqual(r["A<20"]["n"], 8)
        self.assertEqual(r["20<=A<=100"]["n"], 98)
        self.assertEqual(r["A>100"]["n"], 129)
        self.assertAlmostEqual(r["A<20"]["rms_relatif"],
                               0.1434846556617462, delta=1e-12)
        self.assertAlmostEqual(r["20<=A<=100"]["rms_relatif"],
                               0.07073463654191978, delta=1e-12)
        self.assertAlmostEqual(r["A>100"]["rms_relatif"],
                               0.1507844022815636, delta=1e-12)
        self.assertLess(r["20<=A<=100"]["rms_relatif"],
                        r["A<20"]["rms_relatif"])
        self.assertLess(r["20<=A<=100"]["rms_relatif"],
                        r["A>100"]["rms_relatif"])

    def test_modele_ne_se_reproduit_pas_lui_meme(self):
        # extras : le modèle ne reproduit pas ses propres exemples
        # publiés par le corpus (même article).
        _, x = tr_kzn_grille()
        ex = x["exemples_corpus_recomputes"]
        self.assertAlmostEqual(ex["11B"]["modele"],
                               8.547572258645268, delta=1e-12)
        self.assertAlmostEqual(ex["11B"]["ecart"],
                               0.25699592038901, delta=1e-12)
        self.assertAlmostEqual(ex["132Sn"]["modele"],
                               9.462530996228681, delta=1e-12)
        self.assertAlmostEqual(ex["133Sn"]["modele"],
                               9.216803252057836, delta=1e-12)

    def test_attendu_splus_non_tenu(self):
        # attendu gelé S+ (le corpus présente le modèle comme donnant
        # les énergies de liaison sur son domaine) ; le run : RMS
        # 12,36 % vs theta 2 % -> S- a 6,18 theta — le prix en justesse
        # du facteur 10⁵ revendiqué.
        r = _contact("TR_KZN_Modele_Grille")
        self.assertEqual(r["expected"], "S+")
        self.assertEqual(r["verdict"], "S-")
        self.assertTrue(r["b3_fail"])
        self.assertAlmostEqual(r["mu_loc"], 0.12356358712158289,
                               delta=1e-15)
        self.assertIsNone(r["units_kill"])


class TestKZNFusion(unittest.TestCase):
    def test_mu_gelé(self):
        # mu_loc = écart relatif maximal des trois liaisons et de la
        # Q-value D-T recompute — la ligne D est la pire (1,12 %).
        self.assertAlmostEqual(tr_kzn_fusion()[0],
                               0.011166599398620747, delta=1e-15)
        _, x = tr_kzn_fusion()
        self.assertEqual(x["pire_ligne"], "D")
        self.assertAlmostEqual(x["liaisons"]["D"]["nubase"],
                               2.2245665186769656, delta=1e-12)
        self.assertAlmostEqual(x["liaisons"]["T"]["nubase"],
                               8.481796553861841, delta=1e-12)
        self.assertAlmostEqual(x["liaisons"]["4He"]["nubase"],
                               28.295662957354125, delta=1e-12)
        self.assertAlmostEqual(x["Q_DT"]["nubase"],
                               17.58929988481532, delta=1e-12)
        self.assertAlmostEqual(x["Q_DT"]["ecart"],
                               0.0006079610900387999, delta=1e-15)
        # D+D : deux canaux, dette nommée, hors mu_loc
        self.assertAlmostEqual(x["D+D_deux_canaux"]["3He+n"],
                               3.268908809999857, delta=1e-12)
        self.assertAlmostEqual(x["D+D_deux_canaux"]["T+p"],
                               4.032663825999407, delta=1e-12)

    def test_attendu_splus_tenu(self):
        # première fournée k(Z,N) verte : données standard citées
        # correctement (pire 1,12 % vs theta 2 %).
        r = _contact("TR_KZN_FusionDT_Liaisons")
        self.assertEqual(r["expected"], "S+")
        self.assertEqual(r["verdict"], "S+")
        self.assertFalse(r["b3_fail"])
        self.assertAlmostEqual(r["mu_loc"], 0.011166599398620747,
                               delta=1e-15)
        self.assertIsNone(r["units_kill"])


class TestKZNComparaison(unittest.TestCase):
    def test_mu_gelé(self):
        # mu_loc = écart relatif max des lignes à canal unique —
        # p+11B est la pire (0,208 %).
        self.assertAlmostEqual(tr_kzn_comparaison()[0],
                               0.0020768087938919377, delta=1e-15)
        _, x = tr_kzn_comparaison()
        self.assertEqual(x["pire_ligne"], "p+11B")
        self.assertAlmostEqual(x["comparaison"]["D+T"]["ecart"],
                               0.0006079610900387999, delta=1e-15)
        self.assertAlmostEqual(x["comparaison"]["p+11B"]["nubase"],
                               8.68193176349314, delta=1e-12)

    def test_attendu_splus_tenu(self):
        r = _contact("TR_KZN_TableComparaison")
        self.assertEqual(r["expected"], "S+")
        self.assertEqual(r["verdict"], "S+")
        self.assertFalse(r["b3_fail"])
        self.assertAlmostEqual(r["mu_loc"], 0.0020768087938919377,
                               delta=1e-15)
        self.assertIsNone(r["units_kill"])


class TestKZNExpQ65(unittest.TestCase):
    def test_mu_gelé(self):
        # étape 1 (rapport) tient à 0,025 % ; étape 2 (exponentielle)
        # casse à 11,90 % — dette arithmétique interne au corpus.
        self.assertAlmostEqual(tr_kzn_expq65()[0],
                               0.11901575042118973, delta=1e-15)
        _, x = tr_kzn_expq65()
        self.assertEqual(x["pire_etape"], "exponentielle")
        self.assertAlmostEqual(x["rapport_recompute"],
                               75.58139534883722, delta=1e-12)
        self.assertAlmostEqual(x["ecart_rapport"],
                               0.0002460932693488793, delta=1e-15)
        self.assertAlmostEqual(x["exponentielle_recompute"],
                               1.4976732242839775e-33, delta=1e-45)

    def test_attendu_splus_non_tenu(self):
        r = _contact("TR_KZN_ExpQ65")
        self.assertEqual(r["expected"], "S+")
        self.assertEqual(r["verdict"], "S-")
        self.assertTrue(r["b3_fail"])
        self.assertAlmostEqual(r["mu_loc"], 0.11901575042118973,
                               delta=1e-15)
        self.assertIsNone(r["units_kill"])


class TestKZNSensibilite(unittest.TestCase):
    def test_mu_gelé(self):
        # sensibilité déclarée 0,1 MeV/1 % vs modèle gelé 0,006 MeV/1 %
        # (terme de couches 4He = 0,3×S(2,2) = 0,6 MeV) — le delta
        # shell impliqué par la déclaration serait 10 MeV.
        self.assertAlmostEqual(tr_kzn_sensibilite()[0],
                               15.666666666666668, delta=1e-15)
        _, x = tr_kzn_sensibilite()
        self.assertAlmostEqual(x["sensibilite_recompute_MeV_par_pct"],
                               0.006, delta=1e-15)
        self.assertAlmostEqual(x["terme_couches_4He_MeV"],
                               0.6, delta=1e-15)
        self.assertAlmostEqual(x["delta_shell_implique_MeV"],
                               10.0, delta=1e-12)
        self.assertAlmostEqual(x["Q_final_recompute_MeV"],
                               17.612000000000002, delta=1e-12)
        self.assertAlmostEqual(x["Q_final_declare_MeV"], 17.8, delta=1e-12)

    def test_attendu_splus_non_tenu(self):
        r = _contact("TR_KZN_SensibiliteShell")
        self.assertEqual(r["expected"], "S+")
        self.assertEqual(r["verdict"], "S-")
        self.assertTrue(r["b3_fail"])
        self.assertAlmostEqual(r["mu_loc"], 15.666666666666668,
                               delta=1e-15)
        self.assertIsNone(r["units_kill"])


if __name__ == "__main__":
    unittest.main()


class TestConv4MoyenneKi(unittest.TestCase):
    def test_mu_gelé(self):
        # B2 : moyenne 1,0828 (écart 2,20 %) / fraction 92,22 %
        # (écart relatif 15,278 % vs 80 % déclaré) — mu = pire = fraction.
        self.assertAlmostEqual(tr_conv4_moyenne_ki()[0],
                               0.15277777777777768, delta=1e-15)
        _, x = tr_conv4_moyenne_ki()
        self.assertEqual(x["nb_ratios"], 90)
        self.assertAlmostEqual(x["moyenne_recompute"],
                               1.0828133165387523, delta=1e-15)
        self.assertAlmostEqual(x["ecart_moyenne"],
                               0.02203967491059977, delta=1e-15)
        self.assertAlmostEqual(x["fraction_recompute"],
                               0.9222222222222223, delta=1e-15)
        self.assertEqual([z for z, _ in x["positions_hors_bande"]],
                         [2, 3, 4, 5, 7, 19, 86])

    def test_attendu_splus_non_tenu(self):
        r = _contact("TR_CONV4_MoyenneKi")
        self.assertEqual(r["expected"], "S+")
        self.assertEqual(r["verdict"], "S-")
        self.assertTrue(r["b3_fail"])
        self.assertAlmostEqual(r["mu_loc"], 0.15277777777777768,
                               delta=1e-15)
        self.assertIsNone(r["units_kill"])


class TestConv4SeuilZ25(unittest.TestCase):
    def test_mu_gelé(self):
        # B3 : 1 violation (Rn, Z=86) sur 67 coefficients Z=26..92.
        self.assertAlmostEqual(tr_conv4_seuil_z25()[0],
                               0.015151515151515152, delta=1e-15)
        _, x = tr_conv4_seuil_z25()
        self.assertEqual(x["nb_ratios_fenetre"], 66)
        self.assertEqual(x["violations_hors_bande"], [(86, 0.9896)])
        self.assertAlmostEqual(x["amplitude_k_fenetre"][0], 0.9895833333333334,
                               delta=1e-15)

    def test_attendu_splus_tenu(self):
        r = _contact("TR_CONV4_SeuilZ25")
        self.assertEqual(r["expected"], "S+")
        self.assertEqual(r["verdict"], "S+")
        self.assertFalse(r["b3_fail"])
        self.assertAlmostEqual(r["mu_loc"], 0.015151515151515152,
                               delta=1e-15)
        self.assertIsNone(r["units_kill"])


class TestConv4Alcalins(unittest.TestCase):
    def test_mu_gelé(self):
        # B4 : K (Z=19) pire ligne, écart 9,381 % — courbure du groupe.
        self.assertAlmostEqual(tr_conv4_alcalins()[0],
                               0.09381085785000343, delta=1e-15)
        _, x = tr_conv4_alcalins()
        self.assertEqual(x["pire_ligne"], "K")
        self.assertEqual(len(x["lignes"]), 6)
        self.assertAlmostEqual(x["lignes"]["Li"]["ecart_relatif"],
                               0.0005122261168875042, delta=1e-15)

    def test_attendu_splus_non_tenu(self):
        r = _contact("TR_CONV4_Alcalins")
        self.assertEqual(r["expected"], "S+")
        self.assertEqual(r["verdict"], "S-")
        self.assertTrue(r["b3_fail"])
        self.assertAlmostEqual(r["mu_loc"], 0.09381085785000343,
                               delta=1e-15)
        self.assertIsNone(r["units_kill"])


class TestMDASuiteStable(unittest.TestCase):
    def test_mu_gelé(self):
        # B5 : pire lecture multiplicative au terme 1 (579 %),
        # additive 93,3 % au terme 10.
        self.assertAlmostEqual(tr_mda_suite_stable()[0],
                               5.792095810347826, delta=1e-15)
        _, x = tr_mda_suite_stable()
        self.assertAlmostEqual(x["modeles"]["additive"]["ecart_max"],
                               0.9329966966909419, delta=1e-15)
        self.assertAlmostEqual(x["modeles"]["multiplicative"]["ecart_max"],
                               5.792095810347826, delta=1e-15)
        self.assertAlmostEqual(
            x["sous_claim_rapport_moyen"]["moyenne_rapports_suite"],
            1.5450468259608514, delta=1e-15)

    def test_attendu_splus_non_tenu(self):
        r = _contact("TR_MDA_SuiteStable")
        self.assertEqual(r["expected"], "S+")
        self.assertEqual(r["verdict"], "S-")
        self.assertTrue(r["b3_fail"])
        self.assertAlmostEqual(r["mu_loc"], 5.792095810347826, delta=1e-15)
        self.assertIsNone(r["units_kill"])


class TestAlphaDeltaANU(unittest.TestCase):
    def test_mu_gelé(self):
        # B6 : pire écart relatif Sc 166,9 % ; 13 violations absolues
        # (11 points négatifs + Cu/Ga sous loi < 1).
        self.assertAlmostEqual(tr_alpha_deltaanu()[0],
                               1.6685654897798825, delta=1e-15)
        _, x = tr_alpha_deltaanu()
        self.assertEqual(x["pire_point"], "Sc")
        self.assertEqual(len(x["violations_absolues"]), 13)
        self.assertEqual(len(x["comparaison"]) - len(x["violations_absolues"]),
                         18)

    def test_attendu_splus_non_tenu(self):
        r = _contact("TR_ALPHA_DeltaANU")
        self.assertEqual(r["expected"], "S+")
        self.assertEqual(r["verdict"], "S-")
        self.assertTrue(r["b3_fail"])
        self.assertAlmostEqual(r["mu_loc"], 1.6685654897798825, delta=1e-15)
        self.assertIsNone(r["units_kill"])


class TestTOVSn195Pt(unittest.TestCase):
    def test_mu_gelé(self):
        # C1 : S_n(196Pt) recompute NUBASE2020 = 7921,9171 keV vs
        # 6,5 MeV déclaré (« Ex pour 195Pt=>196Pt, Sn=6,5 MeV »,
        # article TOV 2025-01-29) — écart 21,88 %.
        self.assertAlmostEqual(tr_tov_sn195pt()[0],
                               0.21875647692307676, delta=1e-15)
        _, x = tr_tov_sn195pt()
        self.assertAlmostEqual(x["Sn_NUBASE2020_MeV"], 7.9219171,
                               delta=1e-12)
        self.assertAlmostEqual(x["Sn_NUBASE2020_keV"], 7921.9171,
                               delta=1e-9)
        self.assertEqual(x["Sn_declare_MeV"], 6.5)
        self.assertLess(x["Sn_incertitude_keV"], 1.0)

    def test_attendu_splus_non_tenu(self):
        r = _contact("TR_TOV_Sn195Pt")
        self.assertEqual(r["expected"], "S+")
        self.assertEqual(r["verdict"], "S-")
        self.assertTrue(r["b3_fail"])
        self.assertAlmostEqual(r["mu_loc"], 0.21875647692307676,
                               delta=1e-15)
        self.assertIsNone(r["units_kill"])


class TestPRED23EDMNeutron(unittest.TestCase):
    def test_mu_gelé(self):
        # PRED-23 : retard de veille = 3,0/1,8 − 1 = 2/3 exact —
        # la borne du corpus coïncide avec Pendlebury 2015, la frontière
        # gelée est Abel 2020 (1,8×10⁻²⁶ e·cm, 90 % CL).
        self.assertAlmostEqual(tr_pred23_edm()[0],
                               0.6666666666666667, delta=1e-15)
        _, x = tr_pred23_edm()
        self.assertTrue(x["plafond_physiquement_vrai"])
        self.assertAlmostEqual(x["ancrage_2015_exact"], 0.0, delta=1e-15)
        self.assertAlmostEqual(x["borne_declaree_e_cm"], 3.0e-26)
        self.assertAlmostEqual(x["borne_litterature_2020_e_cm"], 1.8e-26)

    def test_attendu_splus_non_tenu(self):
        r = _contact("TR_PRED23_EDMNeutron")
        self.assertEqual(r["expected"], "S+")
        self.assertEqual(r["verdict"], "S-")
        self.assertTrue(r["b3_fail"])
        self.assertAlmostEqual(r["mu_loc"], 0.6666666666666667,
                               delta=1e-15)
        self.assertIsNone(r["units_kill"])


class TestElectronAssemblageH(unittest.TestCase):
    def test_mu_gelé(self):
        # E1 : charge nette unitaire de l'assemblage H+ déclaré
        # (10 ANU+ / 8 ANU−) = +2 e vs +1 e de l'ion H+ — écart 100 % ;
        # lecture ±e/2 : +1 ✓ (escape nommée, quantum indéclaré).
        self.assertAlmostEqual(tr_electron_h_assemblage()[0], 1.0,
                               delta=1e-15)
        _, x = tr_electron_h_assemblage()
        self.assertTrue(x["sommes_tiennent"])
        self.assertEqual(x["charge_nette_H_unitaire"], 0)
        self.assertEqual(x["charge_nette_Hplus_unitaire"], 2)
        self.assertAlmostEqual(x["charge_nette_Hplus_demi"], 1.0)
        self.assertAlmostEqual(x["mu_lecture_demi"], 0.0, delta=1e-15)

    def test_attendu_splus_non_tenu(self):
        r = _contact("TR_ELECTRON_AssemblageH")
        self.assertEqual(r["expected"], "S+")
        self.assertEqual(r["verdict"], "S-")
        self.assertTrue(r["b3_fail"])
        self.assertAlmostEqual(r["mu_loc"], 1.0, delta=1e-15)
        self.assertIsNone(r["units_kill"])


class TestElectronMasseUUD(unittest.TestCase):
    def test_mu_gelé(self):
        # E2 : m_uud = 9,4 MeV (Part. 3) vs 2×2,01 + 4,79 = 8,81 MeV
        # (Part. 1) — tension interne 6,70 %.
        self.assertAlmostEqual(tr_electron_masse_uud()[0],
                               0.06696935300794582, delta=1e-15)
        _, x = tr_electron_masse_uud()
        self.assertAlmostEqual(x["somme_Part1_MeV"], 8.81, delta=1e-12)
        self.assertEqual(x["m_uud_declare_MeV"], 9.4)

    def test_attendu_splus_non_tenu(self):
        r = _contact("TR_ELECTRON_MasseUUD")
        self.assertEqual(r["expected"], "S+")
        self.assertEqual(r["verdict"], "S-")
        self.assertTrue(r["b3_fail"])
        self.assertAlmostEqual(r["mu_loc"], 0.06696935300794582,
                               delta=1e-15)
        self.assertIsNone(r["units_kill"])


class TestElectronBilanArgile(unittest.TestCase):
    def test_mu_gelé(self):
        # E3 : « 4 + 3x(-2)/2 + 2 = -1 » recomptée telle qu'écrite =
        # +3 — écart 400 % ; lecture corrigée (dernier terme −2) : −1 ✓.
        self.assertAlmostEqual(tr_electron_bilan_argile()[0], 4.0,
                               delta=1e-15)
        _, x = tr_electron_bilan_argile()
        self.assertAlmostEqual(x["somme_ecrite_recompute"], 3.0)
        self.assertEqual(x["resultat_declare"], -1.0)
        self.assertAlmostEqual(x["somme_corrigee_lecture"], -1.0)

    def test_attendu_splus_non_tenu(self):
        r = _contact("TR_ELECTRON_BilanArgile")
        self.assertEqual(r["expected"], "S+")
        self.assertEqual(r["verdict"], "S-")
        self.assertTrue(r["b3_fail"])
        self.assertAlmostEqual(r["mu_loc"], 4.0, delta=1e-15)
        self.assertIsNone(r["units_kill"])


class TestElectronModeleLineaire(unittest.TestCase):
    def test_mu_gelé(self):
        # E4 : ANU = 46,9 Z − 151,2 vs les ancres du même article —
        # pire écart 679,4 % à Z=1 (−104,3 vs 18) ; ancres cohérentes
        # avec la table 1908 ; régime lourd (Z=82) 0,87 %.
        self.assertAlmostEqual(tr_electron_modele_lineaire()[0],
                               6.794444444444443, delta=1e-12)
        _, x = tr_electron_modele_lineaire()
        self.assertEqual(x["pire_ancre"], "H")
        self.assertTrue(all(x["ancres_coherentes_table_1908"].values()))
        self.assertAlmostEqual(
            x["regime_lourd_Z82"]["ecart_relatif"],
            0.008693319023343249, delta=1e-12)
        self.assertEqual(x["regime_lourd_Z82"]["U_table"], 3727.0)

    def test_attendu_splus_non_tenu(self):
        r = _contact("TR_ELECTRON_ModeleLineaire")
        self.assertEqual(r["expected"], "S+")
        self.assertEqual(r["verdict"], "S-")
        self.assertTrue(r["b3_fail"])
        self.assertAlmostEqual(r["mu_loc"], 6.794444444444443, delta=1e-12)
        self.assertIsNone(r["units_kill"])
