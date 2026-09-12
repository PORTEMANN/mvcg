#!/usr/bin/env python3
from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from mvcg.hitran_extract import line_nu  # noqa: E402
from mvcg.spectro_air import vacuum_from_air  # noqa: E402


class TestHitranExtract(unittest.TestCase):
    def test_vacuum_line(self) -> None:
        nu, extra = line_nu("nu3_origin")
        self.assertAlmostEqual(nu, 2349.143)
        self.assertEqual(extra["medium"], "vacuum")
        self.assertEqual(len(extra["sha"]), 64)

    def test_nu2_origin(self) -> None:
        nu, extra = line_nu("nu2_origin")
        self.assertAlmostEqual(nu, 667.380)
        self.assertEqual(extra["medium"], "vacuum")

    def test_medium_declared_not_fetched(self) -> None:
        # Les positions sont un extrait déclaré : pas de fetch
        # HITRAN. Le pont air/vide reste un pont déclaré (capot B) :
        # la table dit vide, le pont ne change pas la ligne.
        nu, extra = line_nu("nu3_origin")
        self.assertEqual(extra["medium"], "vacuum")
        self.assertAlmostEqual(vacuum_from_air(nu), nu / 1.000272,
                               places=9)

    def test_unknown_tag(self) -> None:
        with self.assertRaises(KeyError):
            line_nu("bande_inventee")


if __name__ == "__main__":
    unittest.main(verbosity=2)
