#!/usr/bin/env python3
"""Dealiasing 2/3 en boîte et pas spectral 3D.

Masque ℓ^∞ : |k_i| > n_i/3 sur chaque axe (diagonales comprises).
Gyro : T = (0,0,T) ⇒ T×v = (-T vy, T vx, 0) — même convention que le 2D.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

import numpy as np


def kgrid_nd(shape: tuple[int, ...]) -> list[np.ndarray]:
    axes = [np.fft.fftfreq(n) * n for n in shape]
    return list(np.meshgrid(*axes, indexing="ij"))


def box_high_mask(shape: tuple[int, ...], frac: float = 1.0 / 3.0) -> np.ndarray:
    ks = kgrid_nd(shape)
    mask = np.zeros(shape, dtype=bool)
    for k, n in zip(ks, shape):
        mask |= np.abs(k) > n * frac
    return mask


def dealias_23_nd(f: np.ndarray) -> np.ndarray:
    fh = np.fft.fftn(f)
    fh[box_high_mask(f.shape)] = 0.0
    return np.fft.ifftn(fh).real


def high_k_frac_nd(*comps: np.ndarray) -> float:
    shape = comps[0].shape
    mask = box_high_mask(shape)
    eh = et = 0.0
    for c in comps:
        p = np.abs(np.fft.fftn(c)) ** 2
        et += float(p.sum())
        eh += float(p[mask].sum())
    return eh / (et + 1e-15)


def _ksq(shape: tuple[int, ...]) -> np.ndarray:
    ks = kgrid_nd(shape)
    return sum(k**2 for k in ks)


def spec_lap_nd(f: np.ndarray) -> np.ndarray:
    return np.fft.ifftn(-_ksq(f.shape) * np.fft.fftn(f)).real


def spec_grad_nd(f: np.ndarray) -> list[np.ndarray]:
    fh = np.fft.fftn(f)
    return [np.fft.ifftn(1j * k * fh).real for k in kgrid_nd(f.shape)]


def spec_div_nd(comps: list[np.ndarray]) -> np.ndarray:
    acc = np.zeros(comps[0].shape, dtype=float)
    for i, c in enumerate(comps):
        acc = acc + spec_grad_nd(c)[i]
    return acc


def spec_project_nd(comps: list[np.ndarray]) -> tuple[list[np.ndarray], np.ndarray]:
    shape = comps[0].shape
    rh = np.fft.fftn(spec_div_nd(comps))
    lap = -_ksq(shape)
    lap.flat[0] = 1.0
    ph = rh / lap
    ph.flat[0] = 0.0
    pressure = np.fft.ifftn(ph).real
    grads = spec_grad_nd(pressure)
    return [c - g for c, g in zip(comps, grads)], pressure


@dataclass
class DynParams3:
    n: int = 16
    steps: int = 12
    dt: float = 0.002
    nu0: float = 0.0
    torsion: float = 0.0
    seed: int = 0
    dealias: bool = True
    nu_local: bool = False


@dataclass
class DynReport3:
    params: dict
    energy_0: float
    energy_end: float
    energy_ratio: float
    div_rms: float
    high_k_frac: float
    dealias: bool


def _fields3(p: DynParams3) -> list[np.ndarray]:
    rng = np.random.default_rng(p.seed)
    return [0.1 * rng.standard_normal((p.n, p.n, p.n)) for _ in range(3)]


def _rhs3(comps: list[np.ndarray], p: DynParams3) -> list[np.ndarray]:
    vx, vy, vz = comps
    if p.dealias:
        vx, vy, vz = dealias_23_nd(vx), dealias_23_nd(vy), dealias_23_nd(vz)
    if p.nu_local:
        s = 0.5 * (vx**2 + vy**2 + vz**2)
        if p.dealias:
            s = dealias_23_nd(s)
        nu = p.nu0 * np.exp(-np.abs(s))
        if p.dealias:
            nu = dealias_23_nd(nu)
        visc = [nu * spec_lap_nd(c) for c in (vx, vy, vz)]
        if p.dealias:
            visc = [dealias_23_nd(w) for w in visc]
    else:
        s = 0.5 * float((vx**2 + vy**2 + vz**2).mean())
        nu = p.nu0 * float(np.exp(-abs(s)))
        visc = [nu * spec_lap_nd(c) for c in (vx, vy, vz)]
    # T × v  with T = (0,0,T)
    gyro = [-p.torsion * vy, p.torsion * vx, np.zeros_like(vx)]
    if p.dealias:
        gyro = [dealias_23_nd(g) for g in gyro]
    return [g + vi for g, vi in zip(gyro, visc)]


def analyze3(p: DynParams3) -> DynReport3:
    comps = _fields3(p)
    if p.dealias:
        comps = [dealias_23_nd(c) for c in comps]
    comps, _ = spec_project_nd(comps)
    e0 = 0.5 * float(sum(float((c**2).mean()) for c in comps))
    for _ in range(p.steps):
        rhs = _rhs3(comps, p)
        comps = [c + p.dt * f for c, f in zip(comps, rhs)]
        comps, _ = spec_project_nd(comps)
    e1 = 0.5 * float(sum(float((c**2).mean()) for c in comps))
    div = float(np.sqrt((spec_div_nd(comps) ** 2).mean()))
    return DynReport3(
        params=asdict(p),
        energy_0=e0,
        energy_end=e1,
        energy_ratio=e1 / (e0 + 1e-15),
        div_rms=div,
        high_k_frac=high_k_frac_nd(*comps),
        dealias=p.dealias,
    )


def report_dict(rep: DynReport3) -> dict[str, Any]:
    return asdict(rep)
