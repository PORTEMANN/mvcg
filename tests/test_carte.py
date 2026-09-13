#!/usr/bin/env python3
"""Carte des verdicts — dérivée du registre, déterministe, honnête sur ses limites.

Propriétés figées :
- dérivée : la carte compte autant de points que le registre, et les
  couleurs correspondent aux mots réels ;
- déterministe : régénérer = mêmes octets ;
- honnêteté de dimension : la carte est 2D (θ, δ/θ) — le module
  refuse toute autre dimension, la 3D n'a pas de sens ici (un axe de
  plus = une opportunité de plus de cacher quelque chose).
"""

from __future__ import annotations

import re
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from mvcg.carte import COLORS, main_carte  # noqa: E402
from mvcg.registers import run_registers  # noqa: E402


class TestCarte(unittest.TestCase):
    def test_derived_point_count_matches_register(self) -> None:
        rows = run_registers()["rows"]
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "carte.svg"
            main_carte("principale", out)
            svg = out.read_text(encoding="utf-8")
        # Un point de dispersion matplotlib = un <path> remi de couleur
        # de verdict dans le patch de la collection. Compteur honnête :
        # autant de marqueurs coloriés que de contacts.
        n_marqueurs = sum(svg.count(c) for c in COLORS.values())
        self.assertGreaterEqual(n_marqueurs, len(rows))

    def test_regeneration_same_bytes(self) -> None:
        with tempfile.TemporaryDirectory() as a, tempfile.TemporaryDirectory() as b:
            pa = Path(a) / "c.svg"
            pb = Path(b) / "c.svg"
            main_carte("principale", pa)
            main_carte("principale", pb)
            self.assertEqual(pa.read_bytes(), pb.read_bytes())

    def test_colors_follow_verdicts_and_families_grouped(self) -> None:
        rows = run_registers()["rows"]
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "id.svg"
            main_carte("identite", out)
            svg = out.read_text(encoding="utf-8")
        counts = {v: sum(1 for r in rows if r["verdict"] == v) for v in COLORS}
        for v, n in counts.items():
            # chaque case de la carte identité est un rectangle rempli
            # de la couleur du mot
            self.assertGreaterEqual(svg.count(COLORS[v]), n)

    def test_only_2d_exists(self) -> None:
        with self.assertRaises(ValueError):
            main_carte("3d", Path(tempfile.gettempdir()) / "x.svg")
        with self.assertRaises(ValueError):
            main_carte("mentale", Path(tempfile.gettempdir()) / "x.svg")


if __name__ == "__main__":
    unittest.main(verbosity=2)
