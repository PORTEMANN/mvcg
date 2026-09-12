#!/usr/bin/env python3
"""Métrique de contact + rationalisation HL / Gauss / SI."""

from __future__ import annotations

import math
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from mvcg.met_lib import MetLib15  # noqa: E402
from mvcg.metrics import audit_metric, build_metric  # noqa: E402
from mvcg.rationalization import (  # noqa: E402
    UnitSystem,
    charge_from_hl,
    charge_to_hl,
    check_dirac_identity,
    dirac_product,
    flux_quantum,
)


class TestRationalization(unittest.TestCase):
    def test_hl_gauss_charge_roundtrip(self) -> None:
        qg = 1.0
        qhl = charge_to_hl(qg, "hl") if False else charge_to_hl(qg, "gauss")
        self.assertAlmostEqual(charge_from_hl(qhl, "gauss"), qg)

    def test_dirac_dictionary(self) -> None:
        hl = UnitSystem(packet="hl", vintage="test")
        ga = UnitSystem(packet="gauss", vintage="test")
        self.assertAlmostEqual(dirac_product(1, hl), 2 * math.pi)
        self.assertAlmostEqual(dirac_product(1, ga), 0.5)
        # e_HL g_HL = 4π e_G g_G
        self.assertAlmostEqual(dirac_product(1, hl), 4 * math.pi * dirac_product(1, ga))

    def test_dirac_identity_hl(self) -> None:
        U = UnitSystem(packet="hl", vintage="test")
        out = check_dirac_identity(e=1.0, g=2 * math.pi, n=1, U=U)
        self.assertTrue(out["identity"])
        self.assertAlmostEqual(out["delta_rel"], 0.0)

    def test_flux_dictionary(self) -> None:
        hl = UnitSystem(packet="hl", vintage="test")
        ga = UnitSystem(packet="gauss", vintage="test")
        self.assertAlmostEqual(flux_quantum(1.0, hl), 2 * math.pi)
        self.assertAlmostEqual(flux_quantum(1.0, ga), 4 * math.pi)
        self.assertAlmostEqual(flux_quantum(1.0, ga) / flux_quantum(1.0, hl), 2.0)

    def test_si_requires_mu0(self) -> None:
        from mvcg.rationalization import parse_units

        parse_units({"packet": "si", "vintage": "test"}, dimension="eV")
        with self.assertRaises(ValueError):
            parse_units({"packet": "si", "vintage": "test"}, dimension="e*g")

    def test_parse_units_packets(self) -> None:
        from mvcg.rationalization import parse_units

        self.assertEqual(parse_units({"packet": "1"}).packet, "1")
        self.assertEqual(parse_units({"packet": "dimensionless"}).packet, "1")
        with self.assertRaises(ValueError):
            parse_units({"packet": "imperial"})
        with self.assertRaises(ValueError):
            parse_units({})


class TestContactMetric(unittest.TestCase):
    def test_splus_relative(self) -> None:
        U = UnitSystem(packet="hl", vintage="test")
        rec = build_metric("F-dirac", 2 * math.pi, 2 * math.pi, 1e-9, U, "e*g", "rel")
        self.assertEqual(rec.verdict, "S+")
        self.assertFalse(audit_metric(rec)["kill"])

    def test_sminus_far(self) -> None:
        U = UnitSystem(packet="hl", vintage="test")
        rec = build_metric("F-x", 10.0, 1.0, 0.05, U, "MeV", "rel")
        self.assertEqual(rec.verdict, "S-")

    def test_partial_band(self) -> None:
        U = UnitSystem(packet="hl", vintage="test")
        rec = build_metric("F-p", 1.08, 1.0, 0.05, U, "1", "rel")
        self.assertEqual(rec.verdict, "P")


class TestRegistryHook(unittest.TestCase):
    def test_units_then_metric(self) -> None:
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        lib = MetLib15(Path(tmp.name), offline_ots=True)
        lib.freeze("F30", phys=1, orig="thm", kappa_hat="equilibre")
        lib.freeze_units("F30", {"packet": "hl", "vintage": "convention"})
        met = lib.record_metric("F30", 2 * math.pi, dirac_product(1, UnitSystem("hl", "convention")), 1e-12, "e*g", "rel")
        self.assertEqual(met["verdict"], "S+")
        lib.measure("F30", 0)
        cost = json_cost(Path(tmp.name) / "F30.cost.json")
        self.assertIn("units_sha256", cost["inputs_sha256"])
        self.assertIn("metric_sha256", cost["inputs_sha256"])


def json_cost(path: Path) -> dict:
    import json

    return json.loads(path.read_text())


if __name__ == "__main__":
    unittest.main(verbosity=2)
