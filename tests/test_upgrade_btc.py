#!/usr/bin/env python3
"""Upgrade OTS + vérif Blockstream — F22 encore pending est un succès de protocole."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

try:
    import opentimestamps  # noqa: F401
except ImportError:
    opentimestamps = None

from mvcg.ots_anchor import upgrade_and_verify, _http_body, _http_json  # noqa: E402


@unittest.skipIf(opentimestamps is None, "opentimestamps absent")
class TestUpgradeBtc(unittest.TestCase):
    def test_f22_still_pending(self) -> None:
        dest = ROOT / "examples" / "registre"
        if not (dest / "F22.bits.ots").exists():
            self.skipTest("F22.bits.ots absent")
        out = upgrade_and_verify(dest, "F22")
        self.assertEqual(out["upgrade"]["pending_seen"], 3)
        self.assertEqual(out["upgrade"]["bitcoin_attestations"], 0)
        self.assertTrue(out["verify"]["kill"])
        self.assertEqual(out["status"], "pending")

    def test_blockstream_header_path(self) -> None:
        height = 966551
        block_hash = _http_body(f"https://blockstream.info/api/block-height/{height}").strip()
        header = _http_json(f"https://blockstream.info/api/block/{block_hash}")
        self.assertEqual(header.get("height"), height)
        self.assertEqual(len(header.get("merkle_root", "")), 64)


if __name__ == "__main__":
    unittest.main(verbosity=2)
