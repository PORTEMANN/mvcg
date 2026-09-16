#!/usr/bin/env python3
"""Chantier LOI-HARMONIQUE — verrous figés (protocole gelé avant run).

Premier chantier pesant une loi interne au corpus noétique. Le run a
corrigé l'attendu du contact KO-6 : le corpus publie deux valeurs de
sqf fausses sous sa propre définition — dette interne, type PF5.
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from mvcg.loi_harmonique import (  # noqa: E402
    lh_addendum_corps,
    lh_alpha_double,
    lh_anu_gamme,
    lh_anu_pont_rms,
    lh_bottom_arith,
    lh_bottom_g6,
    lh_charm_g5,
    lh_fexp_corridor,
    lh_g11_mass_shift,
    lh_ko6_racines,
    lh_koide_q,
    lh_muon_quinte,
    lh_strange_quarte,
    lh_up_g3,
    lh_z_diagonale,
    lh_zmax_modes,
)
from mvcg.registers import run_contact  # noqa: E402
from mvcg.registers import CONTACTS  # noqa: E402


def _contact(cid: str) -> dict:
    c = next(x for x in CONTACTS if x.id == cid)
    return run_contact(c)


class TestLoiHarmoniqueCalculs(unittest.TestCase):
    def test_mu_gelés(self):
        self.assertAlmostEqual(lh_muon_quinte()[0], 105.03787746595427,
                               delta=1e-10)
        self.assertAlmostEqual(lh_z_diagonale()[0], 90917.70609072277,
                               delta=1e-8)
        self.assertEqual(lh_ko6_racines()[0], 14.0)

    def test_mu_gelés_g4_g6(self):
        # 2e fournée : frontière de la loi côté quarks (2026-09-15)
        self.assertAlmostEqual(lh_strange_quarte()[0], 104.25245424,
                               delta=1e-8)
        self.assertAlmostEqual(lh_bottom_g6()[0], 4723.2582523756655,
                               delta=1e-8)
        self.assertAlmostEqual(lh_bottom_arith()[0], 4720.098178042103,
                               delta=1e-8)

    def test_mu_gelés_g7_g9_g10(self):
        # 3e fournée (2026-09-15 nuit) : Koide, Z_max, tension addendum
        self.assertAlmostEqual(lh_koide_q()[0], 0.6666605114773855,
                               delta=1e-12)
        self.assertAlmostEqual(lh_zmax_modes()[0], 179.38411712391758,
                               delta=1e-8)
        self.assertEqual(lh_addendum_corps()[0], 1.0)

    def test_mu_gelés_g3_g5(self):
        # 4e fournée (2026-09-15 nuit) : clôture du sextuor G1-G6
        self.assertAlmostEqual(lh_up_g3()[0], 2.2264295684587667,
                               delta=1e-12)
        self.assertAlmostEqual(lh_charm_g5()[0], 1251.02945088,
                               delta=1e-8)

    def test_mu_gelés_c1_g12(self):
        # 5e fournée (2026-09-15 nuit) : gamme ANU, alpha double usage
        self.assertAlmostEqual(lh_anu_gamme()[0], 1.060703905809855,
                               delta=1e-12)
        self.assertAlmostEqual(lh_alpha_double()[0],
                               0.0072992700729927005, delta=1e-15)

    def test_mu_gelés_g11(self):
        # 7e fournée (2026-09-16) : déplacement de masse G11 — transport
        # strict de (21) depuis les intrants gelés (E = 1e15 V/m,
        # P_K = 8,5e21 Pa déclaré, ε₀ CODATA-2018)
        self.assertAlmostEqual(lh_g11_mass_shift()[0],
                               0.00013020864430588237, delta=1e-18)
        _, x = lh_g11_mass_shift()
        self.assertAlmostEqual(
            x["P_K_ratio_recompute_sur_declare"], 158.879422028256,
            delta=1e-9)

    def test_mu_gelés_c3(self):
        # 6e fournée (2026-09-16) : pont ANU — transport en fraction
        # (mu_ref = 0,0142), les % restent en extras
        self.assertAlmostEqual(lh_anu_pont_rms()[0], 0.03376492986006094,
                               delta=1e-14)

    def test_mu_gelés_fexp(self):
        # 8e fournée (2026-09-16) : corridor des corrections
        # harmoniques — deviation max recomputee depuis les colonnes
        # voisines de la table du corpus (up : 8,333 %)
        self.assertAlmostEqual(lh_fexp_corridor()[0],
                               0.08333333333333326, delta=1e-15)
        _, x = lh_fexp_corridor()
        self.assertEqual(x["pire_ligne"], "u")
        self.assertEqual(x["n_violations_plancher"], 5)

    def test_ko6_deux_sqf_faux(self):
        _, x = lh_ko6_racines()
        self.assertEqual(x["n_sqf_faux"], 2)
        self.assertEqual(x["sqf_recomputes"][63], 21)   # corpus publie 7
        self.assertEqual(x["sqf_recomputes"][36], 6)    # corpus publie 1
        # les identités module-racines restent exactes (information)
        for v in x["identites_module_racines"].values():
            self.assertEqual(v, 0)
        # l'exclusion d'E6 par sqf(36)=1 ne tient pas
        self.assertFalse(x["E6_exclusion_tient"])


class TestLoiHarmoniqueContacts(unittest.TestCase):
    def test_verdicts_figés(self):
        attendus = {
            "LH_KO6_Racines": ("S-", 14.0),
            "LH_Muon_Quinte": ("S+", 105.03787746595427),
            "LH_Z_Diagonale": ("S+", 90917.70609072277),
        }
        for cid, (mot, mu) in attendus.items():
            r = _contact(cid)
            self.assertEqual(r["verdict"], mot, cid)
            self.assertAlmostEqual(r["mu_loc"], mu, delta=1e-8, msg=cid)
            self.assertIsNone(r["units_kill"], cid)

    def test_verdicts_figés_g4_g6(self):
        # 2e fournée (2026-09-15) : les trois attendus S- gelés ne sont
        # PAS tenus — la bande P s'étend de 1 à 2 theta, et les écarts
        # (12,1 % / 13,0 % / 12,4 %) y tombent tous trois. Le run corrige
        # la prospective : la frontière de la loi est grise, pas rouge.
        attendus = {
            "LH_Strange_Quarte": ("P", 104.25245424),
            "LH_Bottom_G6": ("P", 4723.2582523756655),
            "LH_Bottom_Arith": ("P", 4720.098178042103),
        }
        for cid, (mot, mu) in attendus.items():
            r = _contact(cid)
            self.assertEqual(r["verdict"], mot, cid)
            self.assertAlmostEqual(r["mu_loc"], mu, delta=1e-8, msg=cid)
            self.assertIsNone(r["units_kill"], cid)

    def test_g4_g6_attendus_sminus_non_tenus(self):
        # attendus gelés S- (prospective : delta > theta) ; le run
        # corrige : delta/theta = 1,21 / 1,30 / 1,24 -> zone P. La
        # machine nomme une frontière grise, pas un rejet franche.
        for cid in ("LH_Strange_Quarte", "LH_Bottom_G6",
                    "LH_Bottom_Arith"):
            r = _contact(cid)
            self.assertEqual(r["expected"], "S-", cid)
            self.assertEqual(r["verdict"], "P", cid)
            self.assertTrue(r["b3_fail"], cid)

    def test_verdicts_figés_g7_g9_g10(self):
        # 3e fournée (2026-09-15 nuit) : les trois attendus sont TENUS.
        attendus = {
            "LH_Koide_Q": ("S+", 0.6666605114773855),
            "LH_Zmax_Modes": ("S+", 179.38411712391758),
            "LH_Addendum_Corps": ("S-", 1.0),
        }
        for cid, (mot, mu) in attendus.items():
            r = _contact(cid)
            self.assertEqual(r["verdict"], mot, cid)
            self.assertAlmostEqual(r["mu_loc"], mu, delta=1e-8, msg=cid)
            self.assertIsNone(r["units_kill"], cid)

    def test_g7_splus_le_plus_serré(self):
        # Koide : écart 9,2e-6 -> 9,2e-5 theta, le S+ le plus serré du
        # registre ; la loi empirique tient sur PDG-2024 gelé.
        r = _contact("LH_Koide_Q")
        self.assertEqual(r["expected"], "S+")
        self.assertEqual(r["verdict"], "S+")
        self.assertFalse(r["b3_fail"])
        self.assertLess(r["delta"], 1e-5)

    def test_g9_g10_couplet_zmax(self):
        # Le couplet Z_max : le « ~ 179 » du corps tient (S+) et la
        # tension addendum/corps (180 « recomputé exact » vs 179) est
        # nommée S- à 1 U — les deux énoncés se disent « recomputé ».
        r9 = _contact("LH_Zmax_Modes")
        self.assertEqual(r9["expected"], "S+")
        self.assertEqual(r9["verdict"], "S+")
        r10 = _contact("LH_Addendum_Corps")
        self.assertEqual(r10["expected"], "S-")
        self.assertEqual(r10["verdict"], "S-")

    def test_verdicts_figés_g3_g5(self):
        # 4e fournée (2026-09-15 nuit) : clôture du sextuor — les deux
        # attendus S+ sont tenus ; le up tombe dans la fourchette PDG.
        attendus = {
            "LH_Up_G3": ("S+", 2.2264295684587667),
            "LH_Charm_G5": ("S+", 1251.02945088),
        }
        for cid, (mot, mu) in attendus.items():
            r = _contact(cid)
            self.assertEqual(r["verdict"], mot, cid)
            self.assertAlmostEqual(r["mu_loc"], mu, delta=1e-8, msg=cid)
            self.assertIsNone(r["units_kill"], cid)

    def test_g3_g5_attendus_tenus(self):
        for cid in ("LH_Up_G3", "LH_Charm_G5"):
            r = _contact(cid)
            self.assertEqual(r["expected"], "S+", cid)
            self.assertEqual(r["verdict"], "S+", cid)
            self.assertFalse(r["b3_fail"], cid)

    def test_verdicts_figés_c1_g12(self):
        # 5e fournée (2026-09-15 nuit) : versant chimie occulte — les
        # deux attendus sont TENUS (gamme ANU S+, alpha double usage S-).
        attendus = {
            "LH_Anu_Gamme": ("S+", 1.060703905809855),
            "LH_Alpha_DoubleUsage": ("S-", 0.0072992700729927005),
        }
        for cid, (mot, mu) in attendus.items():
            r = _contact(cid)
            self.assertEqual(r["verdict"], mot, cid)
            self.assertAlmostEqual(r["mu_loc"], mu, delta=1e-12, msg=cid)
            self.assertIsNone(r["units_kill"], cid)

    def test_c1_g12_attendus_tenus(self):
        # C1 : le corpus annonce « converge vers 2^(1/12) » et la valeur
        # recomptee 1,0607 — les deux tiennent (delta 0,117 %).
        r_c1 = _contact("LH_Anu_Gamme")
        self.assertEqual(r_c1["expected"], "S+")
        self.assertEqual(r_c1["verdict"], "S+")
        self.assertFalse(r_c1["b3_fail"])
        self.assertLess(r_c1["delta"], 0.01)
        # G12 : dette d'identification nommée, k(Z) aveugle en extra.
        r_g12 = _contact("LH_Alpha_DoubleUsage")
        self.assertEqual(r_g12["expected"], "S-")
        self.assertEqual(r_g12["verdict"], "S-")
        self.assertFalse(r_g12["b3_fail"])
        self.assertGreater(r_g12["delta"], 1.0)

    def test_c3_attendu_splus_non_tenu(self):
        # C3 : l'addendum déclare RMS 1,42 % global ; sur la fenêtre
        # vérifiable Z = 1-12 (scan gelé, isotopes du corpus, B = 10B)
        # le RMS recompté vaut 3,376 % — le run corrige : S- à 13,8 θ.
        # Extra : hors bore la fenêtre donne 1,225 % (cohérent) — c'est
        # le bore 10B, choix du corpus dans sa propre table, qui porte
        # l'écart ; la déclaration globale reste non vérifiable (table
        # Z = 13-92 absente, dette nommée).
        r = _contact("LH_Anu_Pont_RMS")
        self.assertEqual(r["expected"], "S+")
        self.assertEqual(r["verdict"], "S-")
        self.assertTrue(r["b3_fail"])
        self.assertAlmostEqual(r["mu_loc"], 0.03376492986006094,
                               delta=1e-14)
        self.assertIsNone(r["units_kill"])

    def test_fexp_attendu_splus_non_tenu(self):
        # attendu gelé S+ (le corpus déclare la robustesse du corridor
        # ±3 %) ; le run corrige : deviation max recompute 8,33 % vs
        # 3 % déclaré -> P à 1,78 theta — la déclaration des corrections
        # harmoniques tient au mieux en zone grise.
        r = _contact("LH_Fexp_Corridor")
        self.assertEqual(r["expected"], "S+")
        self.assertEqual(r["verdict"], "P")
        self.assertTrue(r["b3_fail"])
        self.assertAlmostEqual(r["mu_loc"], 0.08333333333333326,
                               delta=1e-15)
        self.assertIsNone(r["units_kill"])

    def test_g11_attendu_splus_non_tenu(self):
        # G11 : le corpus présente 6,5e-8 comme dérivé de (21) ; le run
        # corrige : recompute strict = 1,302e-4 — le corpus a mis P_ext
        # = ε₀E²/2 au numérateur (facteur 2, dette type PF5) et P_K
        # déclaré ne suit pas de ses propres intrants (facteur ~159) :
        # S- à 20 022 θ, la prédiction expérimentale est doublement non
        # tenue sur sa propre arithmétique.
        r = _contact("LH_G11_MassShift")
        self.assertEqual(r["expected"], "S+")
        self.assertEqual(r["verdict"], "S-")
        self.assertTrue(r["b3_fail"])
        self.assertGreater(r["delta"], 1000.0)
        self.assertIsNone(r["units_kill"])

    def test_ko6_attendu_splus_non_tenu(self):
        # attendu gelé S+ (declarations exactes) ; le run corrige : S-
        r = _contact("LH_KO6_Racines")
        self.assertEqual(r["expected"], "S+")
        self.assertEqual(r["verdict"], "S-")
        self.assertTrue(r["b3_fail"])

    def test_muon_z_attendus_tenus(self):
        for cid in ("LH_Muon_Quinte", "LH_Z_Diagonale"):
            r = _contact(cid)
            self.assertEqual(r["expected"], "S+", cid)
            self.assertEqual(r["verdict"], "S+", cid)


if __name__ == "__main__":
    unittest.main()
