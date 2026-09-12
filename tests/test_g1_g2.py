#!/usr/bin/env python3
"""Tueurs I-G1 et I-G2 — jeux qui doivent HOLD ou KILL."""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from mvcg.met_lib import MetLib15, sha256_obj  # noqa: E402


class TestG1G2(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.lib = MetLib15(Path(self.tmp.name), offline_ots=True)

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def test_happy_path_holds(self) -> None:
        self.lib.freeze("F21", phys=1, orig="pred", kappa_hat="equilibre")
        self.lib.measure("F21", 0)
        g1, g2 = self.lib.audit_g1("F21"), self.lib.audit_g2("F21")
        self.assertFalse(g1.kill, g1.reason)
        self.assertFalse(g2.kill, g2.reason)
        self.assertIn("bits_sha256", json.loads((self.lib.root / "F21.cost.json").read_text())["inputs_sha256"])

    def test_measure_without_bits_refused(self) -> None:
        with self.assertRaises(RuntimeError):
            self.lib.measure("F0", 1)

    def test_regels_refused(self) -> None:
        self.lib.freeze("F7", phys=0, orig="proto", kappa_hat="deficit")
        with self.assertRaises(RuntimeError):
            self.lib.freeze("F7", phys=1, orig="pred", kappa_hat="equilibre")

    def test_patch_after_d_kills_g2_and_does_not_write(self) -> None:
        self.lib.freeze("F19", phys=1, orig="pred", kappa_hat="deficit")
        self.lib.measure("F19", 3)
        before = json.loads((self.lib.root / "F19.bits.json").read_text())
        audit = self.lib.try_patch_bits("F19", b_orig="thm", b_phys=0)
        self.assertTrue(audit.kill)
        after = json.loads((self.lib.root / "F19.bits.json").read_text())
        self.assertEqual(before, after)
        g2 = self.lib.audit_g2("F19")
        self.assertFalse(g2.kill, "écriture refusée : I-G2 sur l'état HOLD")
        self.assertEqual(g2.details.get("incidents_refuses"), 1)

    def test_tamper_bits_file_kills_g2(self) -> None:
        self.lib.freeze("F5", phys=1, orig="pred", kappa_hat="non_contraint")
        self.lib.measure("F5", "inf")
        path = self.lib.root / "F5.bits.json"
        doc = json.loads(path.read_text())
        doc["b_orig"] = "thm"
        path.write_text(json.dumps(doc, indent=2) + "\n")
        self.assertTrue(self.lib.audit_g2("F5").kill)
        self.assertTrue(self.lib.audit_g1("F5").kill)

    def test_cost_missing_bits_hash_kills_g1(self) -> None:
        self.lib.freeze("F3", phys=1, orig="pred", kappa_hat="deficit")
        self.lib.measure("F3", 1)
        cost_path = self.lib.root / "F3.cost.json"
        cost = json.loads(cost_path.read_text())
        cost["inputs_sha256"]["bits_sha256"] = "0" * 64
        cost_path.write_text(json.dumps(cost, indent=2) + "\n")
        self.assertTrue(self.lib.audit_g1("F3").kill)

    def test_void_blocks_remeasure_and_patch_does_not_rewrite(self) -> None:
        self.lib.freeze("F18", phys=0, orig="proto", kappa_hat="hors_domaine")
        self.lib.measure("F18", None)
        self.lib.void("F18", "hygiene, pas un equilibre")
        with self.assertRaises(RuntimeError):
            self.lib.measure("F18", 0)
        bits_before = json.loads((self.lib.root / "F18.bits.json").read_text())
        audit = self.lib.try_patch_bits("F18", b_orig="pred", kappa_hat="equilibre")
        self.assertFalse(audit.kill)
        bits_after = json.loads((self.lib.root / "F18.bits.json").read_text())
        self.assertEqual(bits_before, bits_after)

    def test_clock_inversion_refused(self) -> None:
        self.lib.freeze("F9", phys=0, orig="proto", kappa_hat="deficit", frozen_at="2026-09-11T20:00:00.000000Z")
        with self.assertRaises(RuntimeError):
            self.lib.measure("F9", 1, measured_at="2026-09-11T19:00:00.000000Z")

    def test_bits_hash_covers_payload_only(self) -> None:
        rec = self.lib.freeze("F14", phys=0, orig="thm", kappa_hat="equilibre")
        payload = {
            "protocol": rec.protocol,
            "frontier_id": rec.frontier_id,
            "b_phys": rec.b_phys,
            "b_orig": rec.b_orig,
            "kappa_hat": rec.kappa_hat,
            "frozen_at": rec.frozen_at,
        }
        self.assertEqual(rec.bits_sha256, sha256_obj(payload))


if __name__ == "__main__":
    unittest.main(verbosity=2)
