"""Chantier PRINCIPES (PF1-PF4) — verrous figés (protocole gelé avant run).

Protocole : docs/CHANTIER-PRINCIPES-PROTOCOLE.md. Les valeurs chiffrées
ci-dessous sont celles du premier run (2026-09-14) ; elles figent les
contacts, comme pour tout contact du registre.
"""

from __future__ import annotations

import math
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from mvcg.principes import (  # noqa: E402
    pf1_rg_spread,
    pf2_graviton_ev,
    pf3_tau5_recompute,
    pf4_vide_log_ratio,
    pf5_psy_energie,
    pf6_rmn_deltab,
)
from mvcg.registers import CONTACTS, run_contact  # noqa: E402


def _contact(contact_id: str) -> dict:
    return run_contact(next(c for c in CONTACTS if c.id == contact_id))


class TestPrincipesCalculs(unittest.TestCase):
    def test_pf2_25thz_en_ev(self):
        mu, extra = pf2_graviton_ev()
        self.assertAlmostEqual(mu, 0.103392, places=6)
        self.assertAlmostEqual(extra["E_eV"], mu)

    def test_pf3_tau5_recompute(self):
        mu, extra = pf3_tau5_recompute()
        self.assertAlmostEqual(mu, 10.0 * math.exp(-0.023 * 22.67), places=9)
        self.assertAlmostEqual(mu, 5.93683, places=5)

    def test_pf4_vide_log_ratio(self):
        mu, extra = pf4_vide_log_ratio()
        self.assertAlmostEqual(mu, 122.945, places=3)
        self.assertAlmostEqual(
            extra["rho_planck_J_m3"], 4.633e113, delta=1e111
        )
        self.assertAlmostEqual(
            extra["rho_lambda_J_m3"], 5.252e-10, delta=1e-12
        )

    def test_pf1_spread_1loop(self):
        mu, extra = pf1_rg_spread()
        # la dispersion 1-loop minimale est ~34 %, loin des 1 % revendiques
        self.assertGreater(mu, 0.20)
        self.assertAlmostEqual(mu, 0.337925, places=6)
        self.assertEqual(extra["loop"], "1-loop")
        # les quatre couplages a l'echelle revendiquee ne coincident pas
        g = extra["g_at_claim_scale"]
        self.assertIsNotNone(g)
        self.assertGreater((max(g) - min(g)) / (sum(g) / 4.0), 0.20)

    def test_pf5_psy_energie(self):
        mu, extra = pf5_psy_energie()
        # 500 psy * 1,054e-34 / 1 s = 5,27e-32 J, loin des 5,25e-31 annonces
        self.assertAlmostEqual(mu, 5.27e-32, delta=1e-35)
        self.assertAlmostEqual(
            extra["hbar_N_implicite_du_texte_Js"], 1.05e-33, delta=1e-37
        )

    def test_pf6_rmn_deltab(self):
        mu, extra = pf6_rmn_deltab()
        # recompute sous c_éth = 1e9 c : ~4,19e32 T, loin des 5e-4 T
        self.assertAlmostEqual(mu, 4.186266511885707e32, delta=1e28)
        # c_éth requis pour tenir la revendication : ~3,58e-19 m/s
        self.assertAlmostEqual(
            extra["ceth_requis_m_s"], 3.5806661753238235e-19, delta=1e-23
        )
        # memoire : si c_éth = c, ΔB = ~4,19e23 T
        self.assertAlmostEqual(
            extra["DeltaB_si_ceth_eq_c_T"], 4.186266511885707e23, delta=1e19
        )


class TestPrincipesContacts(unittest.TestCase):
    """Mots figes du chantier (premier run 2026-09-14)."""

    def test_verdicts_figés(self):
        attendus = {
            "PF1_RG_Unification": ("S-", 0.337925, 1e-5),
            "PF2_Graviton_25THz": ("S+", 0.103392, 1e-6),
            "PF3_Tau5_Jeu": ("S+", 5.93683, 1e-5),
            "PF4_Vide_Catastrophe": ("S+", 122.945, 1e-3),
            "PF5_Psy_Energie": ("S-", 5.27e-32, 1e-35),
            "PF6_RMN_DeltaB": ("S-", 4.186266511885707e32, 1e28),
            # 2026-09-14 : chantier H(z) F4 (volet V) — PF7 arithmetique
            # du tableau des plans (S+ a 0,046 theta) et PF8 tension
            # equation publiee / revendication <2 % (S- a 331 theta)
            "PF7_F4_Recompute": ("S+", 0.034839621186663984, 1e-12),
            "PF8_Hz_Filtrage_Ecart": ("S-", 0.6827231514910878, 1e-12),
            # 2026-09-15 : chantier PF1b — le 2-boucles que le volet IV
            # designe lui-meme (coefficients SM empruntes MV1983 geles,
            # b_njn = +10 declare) : best spread 0,337 vs 0,01, S- a
            # 654 theta — le 2-boucles ne ferme pas la dette de PF1
            "PF1b_RG_Unification_2Loop": ("S-", 0.33704355972780004, 1e-12),
        }
        for cid, (mot, mu, tol) in attendus.items():
            r = _contact(cid)
            self.assertEqual(r["verdict"], mot, cid)
            self.assertAlmostEqual(r["mu_loc"], mu, delta=tol, msg=cid)
            self.assertIsNone(r["units_kill"], cid)

    def test_pf1_expected_s_moins_tenu(self):
        r = _contact("PF1_RG_Unification")
        self.assertEqual(r["expected"], "S-")
        self.assertFalse(r["b3_fail"])

    def test_pf5_pf6_attendus_s_moins_tenus(self):
        # chantier PSY-RMN : deux S- attendus (dettes internes au corpus),
        # les deux sont tenus par le run
        for cid in ("PF5_Psy_Energie", "PF6_RMN_DeltaB"):
            r = _contact(cid)
            self.assertEqual(r["expected"], "S-", cid)
            self.assertEqual(r["verdict"], "S-", cid)

    def test_pf7_pf8_attendus_tenus(self):
        # chantier H(z) F4 : S+ attendu sur l'arithmetique du tableau,
        # S- attendu sur la tension equation/revendication
        for cid, mot in (("PF7_F4_Recompute", "S+"),
                         ("PF8_Hz_Filtrage_Ecart", "S-")):
            r = _contact(cid)
            self.assertEqual(r["expected"], mot, cid)
            self.assertEqual(r["verdict"], mot, cid)

    def test_pf1b_attendu_tenu(self):
        # chantier PF1b : le 2-boucles designe par le volet IV ne ferme
        # pas la dette de PF1 — S- attendu, S- obtenu
        r = _contact("PF1b_RG_Unification_2Loop")
        self.assertEqual(r["expected"], "S-")
        self.assertEqual(r["verdict"], "S-")


if __name__ == "__main__":
    unittest.main()
