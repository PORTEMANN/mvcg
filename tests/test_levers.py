#!/usr/bin/env python3
from __future__ import annotations

import sys
import unittest
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from mvcg.ash_instrument import AshParams, analyze as ash  # noqa: E402
from mvcg.dynamics import DynParams, analyze as dyn  # noqa: E402


class TestMissingLevers(unittest.TestCase):
    def test_ash_renorm_off_breaks_relative_claim(self) -> None:
        t = np.arange(0.0, 2.0, 1.0 / 256.0)
        x = np.sin(2.0 * np.pi * 4.0 * t)
        on = ash(x, 256.0, AshParams(1.0, 4, tau=0.1, renorm=True))
        off = ash(x, 256.0, AshParams(1.0, 4, tau=0.1, renorm=False))
        self.assertTrue(on.gain_stable)
        self.assertFalse(off.gain_stable)
        self.assertGreater(off.gain_ratio, 0.5)

    def test_nu_const_vs_entropic_band(self) -> None:
        kw = dict(n=16, steps=20, dt=0.002, nu0=0.05, torsion=0.0, seed=0,
                  pressure_mode="spectral", dealias=True, ic="band")
        c = dyn(DynParams(**kw, nu_mode="const"))
        e = dyn(DynParams(**kw, nu_mode="entropic"))
        self.assertNotAlmostEqual(c.energy_ratio, e.energy_ratio, places=5)

    def test_band_r_independent_of_n(self) -> None:
        rs = []
        for n in (16, 32):
            r = dyn(DynParams(n=n, steps=20, dt=0.002, nu0=0.05, torsion=0.0,
                              pressure_mode="spectral", dealias=True, ic="band",
                              nu_mode="const"))
            rs.append(r.energy_ratio)
        self.assertAlmostEqual(rs[0], rs[1], places=8)

    def test_pjp_reduces_gyro_energy_leak_on_white(self) -> None:
        kw = dict(n=32, steps=20, dt=0.01, nu0=0.0, torsion=0.8, seed=1,
                  pressure_mode="spectral", dealias=True, ic="white")
        j = dyn(DynParams(**kw, generator="J"))
        p = dyn(DynParams(**kw, generator="PJP"))
        self.assertLessEqual(abs(p.energy_ratio - 1.0), abs(j.energy_ratio - 1.0) + 1e-12)


if __name__ == "__main__":
    unittest.main(verbosity=2)
