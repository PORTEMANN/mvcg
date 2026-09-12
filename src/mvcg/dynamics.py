#!/usr/bin/env python3
"""Dynamique candidate (forme MDU), pas un préfiltre.

    ∂v/∂t = -∇P + v ∧ T + ν(S) Δv

Torsion T scalaire (2D) : v∧T = (-T vy, T vx).
ν(S) = ν0 * exp(-S), S = énergie cinétique moyenne (proxy entropique local).
Aucun appel depuis freeze/measure : S candidate, levier T=0.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

import numpy as np


@dataclass
class DynParams:
    n: int = 32
    steps: int = 40
    dt: float = 0.01
    nu0: float = 0.05
    torsion: float = 0.0
    pressure_amp: float = 0.1
    seed: int = 0
    pressure_mode: str = "prescribed"  # prescribed | poisson | spectral
    dealias: bool = False
    dealias_mode: str = "2/3"  # 2/3 | 3/2
    nu_local: bool = False
    nu_mode: str = "entropic"  # entropic | const
    ic: str = "white"  # white | band
    generator: str = "J"  # J | PJP


@dataclass
class DynReport:
    params: dict
    energy_0: float
    energy_end: float
    energy_ratio: float
    div_rms: float
    p_rms: float
    torsion: float
    lever_T0_energy_ratio: float
    lever_drop: bool
    pressure_mode: str
    dealias: bool
    high_k_frac: float


def _kgrid(n: int) -> tuple[np.ndarray, np.ndarray]:
    k = np.fft.fftfreq(n) * n
    return np.meshgrid(k, k)


def dealias_23(f: np.ndarray) -> np.ndarray:
    """Règle 2/3 d'Orszag : annule |kx| ou |ky| > n/3."""
    n = f.shape[0]
    kx, ky = _kgrid(n)
    cut = n / 3.0
    fh = np.fft.fft2(f)
    fh[(np.abs(kx) > cut) | (np.abs(ky) > cut)] = 0.0
    return np.fft.ifft2(fh).real


def _high_k_frac(vx: np.ndarray, vy: np.ndarray) -> float:
    n = vx.shape[0]
    kx, ky = _kgrid(n)
    cut = n / 3.0
    eh = 0.0
    et = 0.0
    for comp in (vx, vy):
        p = np.abs(np.fft.fft2(comp)) ** 2
        et += float(p.sum())
        eh += float(p[(np.abs(kx) > cut) | (np.abs(ky) > cut)].sum())
    return eh / (et + 1e-15)


def _spec_grad(f: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    kx, ky = _kgrid(f.shape[0])
    fh = np.fft.fft2(f)
    return np.fft.ifft2(1j * kx * fh).real, np.fft.ifft2(1j * ky * fh).real


def _spec_lap(f: np.ndarray) -> np.ndarray:
    kx, ky = _kgrid(f.shape[0])
    return np.fft.ifft2(-(kx**2 + ky**2) * np.fft.fft2(f)).real


def _spec_div(vx: np.ndarray, vy: np.ndarray) -> np.ndarray:
    dx, _ = _spec_grad(vx)
    _, dy = _spec_grad(vy)
    return dx + dy


def _zero_nyquist(fh: np.ndarray) -> np.ndarray:
    """Mode k=n/2 (grille paire) : on l'annule, P n'est pas idempotent sinon."""
    n = fh.shape[-1]
    if n % 2 == 0:
        fh = fh.copy()
        fh[..., n // 2] = 0.0
        fh[n // 2, ...] = 0.0
    return fh


def _spec_project(vx: np.ndarray, vy: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    kx, ky = _kgrid(vx.shape[0])
    vx = np.fft.ifft2(_zero_nyquist(np.fft.fft2(vx))).real
    vy = np.fft.ifft2(_zero_nyquist(np.fft.fft2(vy))).real
    rh = np.fft.fft2(_spec_div(vx, vy))
    lap = -(kx**2 + ky**2)
    lap[0, 0] = 1.0
    ph = rh / lap
    ph[0, 0] = 0.0
    pressure = np.fft.ifft2(ph).real
    dpx, dpy = _spec_grad(pressure)
    return vx - dpx, vy - dpy, pressure


def _laplacian(f: np.ndarray) -> np.ndarray:
    return (
        np.roll(f, 1, 0)
        + np.roll(f, -1, 0)
        + np.roll(f, 1, 1)
        + np.roll(f, -1, 1)
        - 4.0 * f
    )


def _div(vx: np.ndarray, vy: np.ndarray) -> np.ndarray:
    dvx_dx = 0.5 * (np.roll(vx, -1, 1) - np.roll(vx, 1, 1))
    dvy_dy = 0.5 * (np.roll(vy, -1, 0) - np.roll(vy, 1, 0))
    return dvx_dx + dvy_dy


def _poisson_periodic(rhs: np.ndarray) -> np.ndarray:
    """∇²P = rhs sur tore, moyenne nulle. FFT."""
    n = rhs.shape[0]
    rhs = rhs - rhs.mean()
    spec = np.fft.fft2(rhs)
    ky = 2.0 * np.pi * np.fft.fftfreq(n)
    kx = 2.0 * np.pi * np.fft.fftfreq(n)
    kx, ky = np.meshgrid(kx, ky)
    # laplacien 5 points (même stencil que _laplacian) : nul seulement en k=0
    lap = 2.0 * np.cos(kx) + 2.0 * np.cos(ky) - 4.0
    lap[0, 0] = 1.0
    spec = spec / lap
    spec[0, 0] = 0.0
    return np.fft.ifft2(spec).real


def _project(vx: np.ndarray, vy: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """v ← v - ∇P, ∇²P = ∇·v  (projection Helmholtz périodique)."""
    pressure = _poisson_periodic(_div(vx, vy))
    dpx, dpy = _grad(pressure)
    return vx - dpx, vy - dpy, pressure


def _grad(p: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    dx = 0.5 * (np.roll(p, -1, 1) - np.roll(p, 1, 1))
    dy = 0.5 * (np.roll(p, -1, 0) - np.roll(p, 1, 0))
    return dx, dy


def _fields(p: DynParams) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    n = p.n
    x = np.linspace(0.0, 2.0 * np.pi, n, endpoint=False)
    xx, yy = np.meshgrid(x, x)
    pressure = p.pressure_amp * np.cos(xx) * np.cos(yy)
    if p.ic == "band":
        vx = 0.2 * np.sin(xx) + 0.1 * np.sin(xx + yy)
        vy = 0.2 * np.cos(yy) + 0.1 * np.cos(xx + yy)
        return vx, vy, pressure
    rng = np.random.default_rng(p.seed)
    vx = 0.1 * rng.standard_normal((n, n))
    vy = 0.1 * rng.standard_normal((n, n))
    return vx, vy, pressure


def _spectral_rhs(vx: np.ndarray, vy: np.ndarray, p: DynParams) -> tuple[np.ndarray, np.ndarray]:
    """Produits dans l'espace physique après 2/3 ou padding 3/2."""
    mode = p.dealias_mode if p.dealias else "none"
    if mode == "2/3":
        vx_p, vy_p = dealias_23(vx), dealias_23(vy)
    else:
        vx_p, vy_p = vx, vy
    if p.nu_local:
        if mode == "3/2":
            from mvcg.padding import pad_product
            s_field = 0.5 * (pad_product(vx_p, vx_p) + pad_product(vy_p, vy_p))
            nu_f = p.nu0 * np.exp(-np.abs(s_field))
            viscx = pad_product(nu_f, _spec_lap(vx_p))
            viscy = pad_product(nu_f, _spec_lap(vy_p))
        else:
            s_field = 0.5 * (vx_p**2 + vy_p**2)
            if mode == "2/3":
                s_field = dealias_23(s_field)
            nu_f = p.nu0 * np.exp(-np.abs(s_field))
            if mode == "2/3":
                nu_f = dealias_23(nu_f)
            viscx, viscy = nu_f * _spec_lap(vx_p), nu_f * _spec_lap(vy_p)
            if mode == "2/3":
                viscx, viscy = dealias_23(viscx), dealias_23(viscy)
    else:
        s_mean = 0.5 * float((vx_p**2 + vy_p**2).mean())
        nu = p.nu0 if p.nu_mode == "const" else p.nu0 * math_exp(s_mean)
        viscx, viscy = nu * _spec_lap(vx_p), nu * _spec_lap(vy_p)
    gyrox, gyroy = -p.torsion * vy_p, p.torsion * vx_p
    if p.generator == "PJP" and p.pressure_mode == "spectral":
        gyrox, gyroy, _ = _spec_project(gyrox, gyroy)
    if mode == "2/3":
        gyrox, gyroy = dealias_23(gyrox), dealias_23(gyroy)
    return gyrox + viscx, gyroy + viscy


def step(
    vx: np.ndarray, vy: np.ndarray, pressure: np.ndarray, p: DynParams
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    if p.pressure_mode == "spectral":
        fx, fy = _spectral_rhs(vx, vy, p)
        vx_s, vy_s = vx + p.dt * fx, vy + p.dt * fy
        return _spec_project(vx_s, vy_s)
    s_ent = 0.5 * float((vx**2 + vy**2).mean())
    nu = p.nu0 if p.nu_mode == "const" else p.nu0 * math_exp(-s_ent)
    if p.pressure_mode == "poisson":
        vx_s = vx + p.dt * (-p.torsion * vy + nu * _laplacian(vx))
        vy_s = vy + p.dt * (p.torsion * vx + nu * _laplacian(vy))
        vx_n, vy_n, pressure = _project(vx_s, vy_s)
        return vx_n, vy_n, pressure
    dpx, dpy = _grad(pressure)
    dvx = -dpx - p.torsion * vy + nu * _laplacian(vx)
    dvy = -dpy + p.torsion * vx + nu * _laplacian(vy)
    return vx + p.dt * dvx, vy + p.dt * dvy, pressure


def math_exp(x: float) -> float:
    return float(np.exp(-abs(x)))


def run(p: DynParams) -> tuple[np.ndarray, np.ndarray, np.ndarray, list[float]]:
    vx, vy, pressure = _fields(p)
    if p.pressure_mode == "poisson":
        vx, vy, pressure = _project(vx, vy)
    if p.pressure_mode == "spectral":
        if p.dealias and p.dealias_mode == "2/3":
            vx, vy = dealias_23(vx), dealias_23(vy)
        vx, vy, pressure = _spec_project(vx, vy)
    energy = []
    for _ in range(p.steps):
        energy.append(float(0.5 * (vx**2 + vy**2).mean()))
        vx, vy, pressure = step(vx, vy, pressure, p)
    energy.append(float(0.5 * (vx**2 + vy**2).mean()))
    return vx, vy, pressure, energy


def analyze(p: DynParams) -> DynReport:
    vx, vy, pressure, energy = run(p)
    if p.pressure_mode == "spectral":
        div_rms = float(np.sqrt((_spec_div(vx, vy) ** 2).mean()))
    else:
        div_rms = float(np.sqrt((_div(vx, vy) ** 2).mean()))
    p_rms = float(np.sqrt((pressure**2).mean()))
    high_k = _high_k_frac(vx, vy)

    lever = DynParams(**{**asdict(p), "torsion": 0.0})
    _, _, _, e0 = run(lever)
    ratio = energy[-1] / (energy[0] + 1e-15)
    ratio_t0 = e0[-1] / (e0[0] + 1e-15)
    lever_drop = abs(ratio - ratio_t0) > 1e-6

    return DynReport(
        params=asdict(p),
        energy_0=energy[0],
        energy_end=energy[-1],
        energy_ratio=ratio,
        div_rms=div_rms,
        p_rms=p_rms,
        torsion=p.torsion,
        lever_T0_energy_ratio=ratio_t0,
        lever_drop=lever_drop,
        pressure_mode=p.pressure_mode,
        dealias=p.dealias,
        high_k_frac=high_k,
    )


def report_dict(rep: DynReport) -> dict[str, Any]:
    return asdict(rep)
