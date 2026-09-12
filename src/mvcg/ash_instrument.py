#!/usr/bin/env python3
"""C5 — instrument d'acquisition (ASH détaché).

Pas un tuyau d'entrée. Pas une ontologie.
Paramètres de domaine (f0, N_oct, tau) ∈ D.
Compare une énergie de bandes chromatiques à un périodogramme.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Optional

import numpy as np


@dataclass
class AshParams:
    f0: float
    n_oct: int
    bins_per_oct: int = 12
    tau: float = 0.1  # fraction de bande (domaine, pas théorème)
    renorm: bool = True  # I-A3 relatif si True ; abs si False


@dataclass
class AshReport:
    params: dict
    R_c: float
    R_top: float
    R_dyn: float
    E: list
    baseline_band_energy: float
    delta_vs_periodogram: float
    gain_stable: bool
    gain_ratio: float


def chromatic_grid(p: AshParams) -> np.ndarray:
    n = p.n_oct * p.bins_per_oct
    return p.f0 * (2.0 ** (np.arange(n) / p.bins_per_oct))


def _rfft_power(x: np.ndarray, fs: float) -> tuple[np.ndarray, np.ndarray]:
    x = np.asarray(x, dtype=float)
    x = x - x.mean()
    spec = np.fft.rfft(x)
    freqs = np.fft.rfftfreq(x.size, d=1.0 / fs)
    power = (spec.real**2 + spec.imag**2) / max(x.size, 1)
    return freqs, power


def band_energies(x: np.ndarray, fs: float, p: AshParams) -> np.ndarray:
    freqs, power = _rfft_power(x, fs)
    grid = chromatic_grid(p)
    e = np.zeros(grid.size)
    for i, f in enumerate(grid):
        lo, hi = f * (1.0 - p.tau), f * (1.0 + p.tau)
        mask = (freqs >= lo) & (freqs <= hi)
        e[i] = float(power[mask].sum()) if mask.any() else 0.0
    return e


def analyze(x: np.ndarray, fs: float, p: AshParams, gain: float = 2.0) -> AshReport:
    e = band_energies(x, fs, p)
    total = float(e.sum()) + 1e-15
    R_c = float(e.sum())
    peak = int(np.argmax(e)) if e.size else 0
    R_top = float(e[peak] / total)
    # variation relative d'énergie entre moitié basse / haute de la grille
    mid = max(e.size // 2, 1)
    low, high = float(e[:mid].sum()), float(e[mid:].sum())
    R_dyn = abs(high - low) / total

    freqs, power = _rfft_power(x, fs)
    baseline = float(power.sum())
    delta = abs(R_c - baseline) / (baseline + 1e-15)

    e_g = band_energies(np.asarray(x, dtype=float) * gain, fs, p)
    p0 = e / (e.sum() + 1e-15)
    p1 = e_g / (e_g.sum() + 1e-15)
    gain_ratio_rel = float(np.max(np.abs(p0 - p1)))
    gain_ratio_abs = float(np.max(np.abs(e_g - e)) / (float(e.sum()) + 1e-15))
    if p.renorm:
        gain_ratio = gain_ratio_rel
    else:
        gain_ratio = gain_ratio_abs
    gain_stable = gain_ratio < 1e-9

    return AshReport(
        params=asdict(p),
        R_c=R_c,
        R_top=R_top,
        R_dyn=R_dyn,
        E=e.tolist(),
        baseline_band_energy=baseline,
        delta_vs_periodogram=delta,
        gain_stable=gain_stable,
        gain_ratio=gain_ratio,
    )


def report_dict(rep: AshReport) -> dict[str, Any]:
    return asdict(rep)
