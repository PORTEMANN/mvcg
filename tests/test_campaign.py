#!/usr/bin/env python3
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from mvcg.campaign import run_campaign  # noqa: E402


class TestCampaign(unittest.TestCase):
    def test_gears_mesh(self) -> None:
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        out = run_campaign(Path(tmp.name), offline_ots=True)
        ids = {r["id"]: r for r in out["rows"]}
        self.assertEqual(ids["dirac_hl"]["verdict"], "S+")
        self.assertEqual(ids["dirac_wrong_packet"]["verdict"], "S-")
        self.assertEqual(ids["ash_gain"]["verdict"], "S+")
        self.assertEqual(ids["spectral_conserve"]["verdict"], "S+")
        self.assertEqual(ids["spectral_gyro_energy"]["verdict"], "S+")
        self.assertEqual(ids["poisson_num_dissipation"]["verdict"], "S-")
        self.assertTrue((Path(tmp.name) / "campaign.json").exists())
        self.assertGreaterEqual(out["splus"], 4)
        self.assertGreaterEqual(out["sminus"], 2)

    def test_rehearsal_writes_no_bits(self) -> None:
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        root = Path(tmp.name)
        from mvcg.campaign import rehearse_campaign

        out = rehearse_campaign(root)
        self.assertFalse(out["committed"])
        self.assertTrue((root / "rehearsal.json").exists())
        self.assertFalse(any(root.glob("*.bits.json")))
        self.assertFalse(any(root.glob("*.cost.json")))
        self.assertFalse((root / "campaign.json").exists())


if __name__ == "__main__":
    unittest.main(verbosity=2)
