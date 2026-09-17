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


if __name__ == "__main__":
    unittest.main()
