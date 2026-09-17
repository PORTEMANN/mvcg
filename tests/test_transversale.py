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
    tr_alpha_proton_muon,
    tr_b11_liaison,
    tr_davies_trio,
    tr_kzn_comparaison,
    tr_kzn_expq65,
    tr_kzn_fusion,
    tr_kzn_grille,
    tr_kzn_sensibilite,
    tr_sn132_liaison,
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
