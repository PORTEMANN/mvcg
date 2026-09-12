#!/usr/bin/env python3
"""C5 instrument + dynamique candidate — hors tuyau d'entrée."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from mvcg.ash_instrument import AshParams, analyze  # noqa: E402
from mvcg.dynamics import DynParams, analyze as dyn_analyze  # noqa: E402
from mvcg.met_lib import MetLib15  # noqa: E402


class TestC5(unittest.TestCase):
    def test_gain_stable_tone(self) -> None:
        fs = 256.0
        t = np.arange(0.0, 2.0, 1.0 / fs)
        x = np.sin(2.0 * np.pi * 4.0 * t)
        rep = analyze(x, fs, AshParams(f0=1.0, n_oct=4, tau=0.1))
        self.assertTrue(rep.gain_stable)
        self.assertGreater(rep.R_c, 0.0)
        self.assertGreaterEqual(rep.delta_vs_periodogram, 0.0)

    def test_not_used_as_pipe(self) -> None:
        # freeze/measure ne lisent pas ASH
        import tempfile
        from pathlib import Path

        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        lib = MetLib15(Path(tmp.name), offline_ots=True)
        lib.freeze("F40", phys=0, orig="proto", kappa_hat="hors_domaine")
        lib.measure("F40", None)
        names = {p.name for p in Path(tmp.name).iterdir()}
        self.assertTrue("F40.bits.json" in names)
        self.assertFalse(any("ash" in n for n in names))


class TestDynamics(unittest.TestCase):
    def test_dealias_23_kills_high_k(self) -> None:
        raw = dyn_analyze(
            DynParams(
                n=32, steps=20, torsion=0.5, seed=2, nu0=0.05,
                pressure_mode="spectral", dealias=False, nu_local=True,
            )
        )
        cut = dyn_analyze(
            DynParams(
                n=32, steps=20, torsion=0.5, seed=2, nu0=0.05,
                pressure_mode="spectral", dealias=True, nu_local=True,
            )
        )
        self.assertLess(cut.high_k_frac, 1e-12)
        self.assertGreater(raw.high_k_frac, cut.high_k_frac)
        self.assertLess(cut.div_rms, 1e-10)

    def test_spectral_nu0_conserves(self) -> None:
        r = dyn_analyze(
            DynParams(
                n=32, steps=20, torsion=0.8, seed=1, nu0=0.0,
                pressure_mode="spectral", dealias=True,
            )
        )
        self.assertGreater(r.energy_ratio, 0.99)
        self.assertLess(r.div_rms, 1e-10)

    def test_poisson_kills_divergence(self) -> None:
        pres = dyn_analyze(DynParams(n=16, steps=20, torsion=0.8, seed=1, pressure_mode="prescribed"))
        poi = dyn_analyze(DynParams(n=16, steps=20, torsion=0.8, seed=1, pressure_mode="poisson"))
        self.assertLess(poi.div_rms, 0.2 * pres.div_rms)
        self.assertLess(poi.p_rms, 10.0)

    def test_runs_and_lever(self) -> None:
        on = dyn_analyze(DynParams(n=16, steps=20, torsion=0.8, seed=1, nu0=0.08))
        off = dyn_analyze(DynParams(n=16, steps=20, torsion=0.0, seed=1, nu0=0.08))
        self.assertTrue(np.isfinite(on.energy_end))
        self.assertTrue(off.lever_drop is False or off.torsion == 0.0)
        self.assertNotEqual(on.energy_ratio, off.energy_ratio)

    def test_t0_is_not_prefilter(self) -> None:
        from mvcg.met_lib import MetLib15
        import tempfile

        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        lib = MetLib15(Path(tmp.name), offline_ots=True)
        lib.freeze("F41", phys=1, orig="pred", kappa_hat="deficit")
        lib.measure("F41", 1)
        self.assertFalse((Path(tmp.name) / "F41.dyn.json").exists())


if __name__ == "__main__":
    unittest.main(verbosity=2)
