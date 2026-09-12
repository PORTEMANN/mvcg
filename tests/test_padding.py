#!/usr/bin/env python3
from __future__ import annotations

import sys
import unittest
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from mvcg.dynamics import DynParams, analyze as dyn_analyze  # noqa: E402
from mvcg.padding import from_fine, pad_product, to_fine  # noqa: E402


class TestPadding32(unittest.TestCase):
    def test_sin_squared(self) -> None:
        n = 16
        x = np.linspace(0, 2 * np.pi, n, endpoint=False)
        s = np.sin(x)
        self.assertLess(
            float(np.max(np.abs(pad_product(s, s) - (0.5 - 0.5 * np.cos(2 * x))))),
            1e-12,
        )

    def test_kills_alias_sin6(self) -> None:
        n = 16
        x = np.linspace(0, 2 * np.pi, n, endpoint=False)
        s = np.sin(6 * x)
        self.assertLess(float(np.max(np.abs(pad_product(s, s) - 0.5))), 1e-12)
        self.assertGreater(float(np.max(np.abs(s * s - 0.5))), 0.4)

    def test_roundtrip(self) -> None:
        n = 16
        x = np.linspace(0, 2 * np.pi, n, endpoint=False)
        s = np.sin(x) + 0.3 * np.cos(2 * x)
        self.assertLess(float(np.max(np.abs(from_fine(to_fine(s), n) - s))), 1e-12)

    def test_spectral_32_conserves(self) -> None:
        r = dyn_analyze(
            DynParams(
                n=16, steps=8, dt=0.002, nu0=0.0, torsion=0.0, seed=1,
                pressure_mode="spectral", dealias=True, dealias_mode="3/2",
            )
        )
        self.assertGreater(r.energy_ratio, 0.99)
        self.assertLess(r.div_rms, 1e-10)

    def test_pad_differs_when_aliased(self) -> None:
        on = dyn_analyze(
            DynParams(
                n=16, steps=6, dt=0.002, nu0=0.05, torsion=0.0, seed=2,
                pressure_mode="spectral", dealias=True, dealias_mode="3/2",
                nu_local=True,
            )
        )
        off = dyn_analyze(
            DynParams(
                n=16, steps=6, dt=0.002, nu0=0.05, torsion=0.0, seed=2,
                pressure_mode="spectral", dealias=True, dealias_mode="2/3",
                nu_local=True,
            )
        )
        self.assertNotAlmostEqual(on.energy_ratio, off.energy_ratio, places=3)


if __name__ == "__main__":
    unittest.main(verbosity=2)
