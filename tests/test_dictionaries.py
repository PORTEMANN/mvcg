#!/usr/bin/env python3
from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from mvcg.dictionaries import sweep_dirac  # noqa: E402


class TestDictionaries(unittest.TestCase):
    def test_dirac_hl_holds_gauss_kills(self) -> None:
        rows = {r["packet"]: r for r in sweep_dirac()["rows"]}
        self.assertEqual(rows["hl"]["verdict"], "S+")
        self.assertEqual(rows["gauss"]["verdict"], "S-")
        self.assertEqual(rows["1"]["verdict"], "S-")
        self.assertIsNotNone(rows["1"]["units_kill"])
        self.assertEqual(rows["si"]["verdict"], "S-")


if __name__ == "__main__":
    unittest.main(verbosity=2)
