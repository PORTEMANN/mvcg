#!/usr/bin/env python3
from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from mvcg.registers import run_registers  # noqa: E402


class TestRegisters(unittest.TestCase):
    def test_three_drawers(self) -> None:
        out = run_registers()
        by = {r["id"]: r for r in out["rows"]}
        self.assertEqual(by["H1s_Rydberg"]["verdict"], "S+")
        self.assertEqual(by["H1s_Rydberg_13p6"]["verdict"], "S-")
        self.assertEqual(by["FRW_baryons"]["verdict"], "S-")
        self.assertEqual(by["FRW_lcdm_Planck"]["verdict"], "S+")
        self.assertEqual(by["AAL_dice_atlas"]["verdict"], "S-")
        self.assertEqual(set(out["counts"]), {"micro", "meso", "macro"})


if __name__ == "__main__":
    unittest.main(verbosity=2)
