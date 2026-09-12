#!/usr/bin/env python3
from __future__ import annotations

import sys
import unittest
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from mvcg.spectral3d import (  # noqa: E402
    DynParams3,
    analyze3,
    box_high_mask,
    dealias_23_nd,
    high_k_frac_nd,
    spec_div_nd,
    spec_project_nd,
)


class TestDealias3D(unittest.TestCase):
    def test_box_kills_all_axes(self) -> None:
        n = 12
        rng = np.random.default_rng(0)
        f = rng.standard_normal((n, n, n))
        g = dealias_23_nd(f)
        self.assertLess(high_k_frac_nd(g), 1e-12)
        mask = box_high_mask((n, n, n))
        self.assertTrue(mask.any())
        # un mode coin (haut, haut, haut) est dans le masque
        self.assertTrue(mask[n // 2, n // 2, n // 2] or mask[n // 2, 0, 0])

    def test_project_div_free(self) -> None:
        rng = np.random.default_rng(1)
        comps = [rng.standard_normal((8, 8, 8)) for _ in range(3)]
        comps = [dealias_23_nd(c) for c in comps]
        out, _ = spec_project_nd(comps)
        div = spec_div_nd(out)
        self.assertLess(float(np.sqrt((div**2).mean())), 1e-10)

    def test_nu0_conserves(self) -> None:
        r = analyze3(DynParams3(n=8, steps=8, nu0=0.0, torsion=0.5, dealias=True, seed=0))
        self.assertGreater(r.energy_ratio, 0.99)
        self.assertLess(r.div_rms, 1e-10)
        self.assertLess(r.high_k_frac, 1e-12)

    def test_without_dealias_keeps_high_k(self) -> None:
        raw = analyze3(DynParams3(n=8, steps=4, nu0=0.05, torsion=0.4, dealias=False, nu_local=True, seed=2))
        cut = analyze3(DynParams3(n=8, steps=4, nu0=0.05, torsion=0.4, dealias=True, nu_local=True, seed=2))
        self.assertLess(cut.high_k_frac, 1e-12)
        self.assertGreater(raw.high_k_frac, cut.high_k_frac)


if __name__ == "__main__":
    unittest.main(verbosity=2)
