#!/usr/bin/env python3
from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from mvcg.spectro_air import (  # noqa: E402
    N_AIR_STP,
    air_from_vacuum,
    pont_air,
    vacuum_from_air,
)


class TestSpectroAir(unittest.TestCase):
    def test_roundtrip(self) -> None:
        vac = 2349.1
        air = air_from_vacuum(vac)
        self.assertAlmostEqual(vacuum_from_air(air), vac, places=9)
        self.assertGreater(air, vac)

    def test_pont(self) -> None:
        p = pont_air()
        self.assertEqual(p["tau"], "spectro-air")
        self.assertAlmostEqual(p["k"] * N_AIR_STP, 1.0, places=12)
        # Δrel air vs vide ~ 2.7e-4 << θ labo 0.05
        self.assertAlmostEqual(N_AIR_STP - 1.0, 2.72e-4, places=6)


if __name__ == "__main__":
    unittest.main(verbosity=2)
