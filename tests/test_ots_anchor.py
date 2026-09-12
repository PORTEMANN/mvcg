#!/usr/bin/env python3
"""Ancre OTS — live si le réseau répond, sinon skip."""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

try:
    import opentimestamps  # noqa: F401
except ImportError:
    opentimestamps = None

from mvcg.met_lib import MetLib15  # noqa: E402
from mvcg.ots_anchor import audit_anchor  # noqa: E402


@unittest.skipIf(opentimestamps is None, "opentimestamps absent")
class TestOtsAnchor(unittest.TestCase):
    def test_live_stamp_and_measure(self) -> None:
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        lib = MetLib15(Path(tmp.name), offline_ots=False)
        try:
            rec = lib.freeze("F22", phys=1, orig="pred", kappa_hat="equilibre")
        except RuntimeError as exc:
            raise unittest.SkipTest(f"calendriers OTS injoignables: {exc}") from exc
        meta = json.loads((Path(tmp.name) / "F22.ots.json").read_text())
        self.assertEqual(meta["bits_sha256"], rec.bits_sha256)
        self.assertGreaterEqual(meta["receipts_ok"], 1)
        self.assertTrue((Path(tmp.name) / "F22.bits.ots").exists())
        self.assertIsNotNone(meta.get("frozen_at_ots"))
        ots = audit_anchor(Path(tmp.name), "F22", rec.bits_sha256)
        self.assertFalse(ots["kill"], ots)
        lib.measure("F22", 0)
        g1 = lib.audit_g1("F22")
        self.assertFalse(g1.kill, g1.reason)

    def test_measure_without_anchor_refused(self) -> None:
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        offline = MetLib15(Path(tmp.name), offline_ots=True)
        offline.freeze("F23", phys=0, orig="proto", kappa_hat="deficit")
        online = MetLib15(Path(tmp.name), offline_ots=False)
        with self.assertRaises(RuntimeError):
            online.measure("F23", 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
