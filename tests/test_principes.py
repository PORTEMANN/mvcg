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


class TestPrincipesContacts(unittest.TestCase):
    """Mots figes du chantier (premier run 2026-09-14)."""

    def test_verdicts_figés(self):
        attendus = {
            "PF1_RG_Unification": ("S-", 0.337925, 1e-5),
            "PF2_Graviton_25THz": ("S+", 0.103392, 1e-6),
            "PF3_Tau5_Jeu": ("S+", 5.93683, 1e-5),
            "PF4_Vide_Catastrophe": ("S+", 122.945, 1e-3),
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


if __name__ == "__main__":
    unittest.main()
