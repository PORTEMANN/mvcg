"""Couche de position (chantier SERRAGE) — verrous de la carte principale."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT))

from mvcg.carte import _position_zone  # noqa: E402
from mvcg.registers import run_registers  # noqa: E402


def _row(contact_id: str) -> dict:
    rows = run_registers()["rows"]
    return next(r for r in rows if r["id"] == contact_id)


class TestPositionZone(unittest.TestCase):
    """Positions figées (campagnes SERRAGE 1-3, 2026-09-14)."""

    def test_positions_connues(self):
        attendus = {
            "O10_PMMA_Carbonyl": 1.0,        # S+ profond (3+ octaves)
            "O11_BEC_Healing": 0.052,        # S+ de surface (0 étage)
            "O2_CO2_nu3": 0.534,             # P : pos_bande
            "Bertsch_Xi_Unitary": 0.071,     # S- chaud : pos_rouge/2
            "H1s_Rydberg": 1.0,              # delta = 0 : plein
        }
        for cid, p in attendus.items():
            self.assertAlmostEqual(_position_zone(_row(cid)), p, places=3)

    def test_bornes_0_1(self):
        for r in run_registers()["rows"]:
            p = _position_zone(r)
            self.assertGreaterEqual(p, 0.0)
            self.assertLessEqual(p, 1.0)

    def test_coherence_campagne_2(self):
        """P nus : la position de carte EST la pos_bande de la campagne."""
        from campagnes_detente_serie_o import run_detente_serie_o

        out = run_detente_serie_o()
        for r in out["resultats"]:
            self.assertAlmostEqual(_position_zone(_row(r["id"])), r["pos_bande"])

    def test_coherence_campagne_3(self):
        """S− de la fenêtre : la position de carte EST pos_rouge/2."""
        from campagnes_remontee_bord import run_remontee_bord

        out = run_remontee_bord()
        for r in out["resultats"]:
            self.assertAlmostEqual(
                _position_zone(_row(r["id"])), r["pos_rouge"] / 2.0
            )


if __name__ == "__main__":
    unittest.main()
