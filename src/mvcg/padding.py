#!/usr/bin/env python3
"""Padding 3/2 (produit quadratique sans alias sur les N modes).

Lift Fourier N → M=3N/2, produit physique, descente.
N pair requis. Le mode Nyquist N/2 n'est pas recopié (mis à 0).
"""

from __future__ import annotations

from itertools import product

import numpy as np


def _fine_n(n: int, factor: float = 1.5) -> int:
    if n % 2:
        raise ValueError(f"padding 3/2 exige N pair, reçu {n}")
    m = int(round(factor * n))
    if m % 2:
        m += 1
    return m


def _copy_low_modes(src: np.ndarray, dst: np.ndarray) -> None:
    """Copie |k_i| < n_coarse/2, n_coarse = min(n_src, n_dst)."""
    n = min(src.shape[0], dst.shape[0])
    h = n // 2
    sl = (slice(0, h), slice(-h, None))
    ndim = src.ndim
    for choice in product((0, 1), repeat=ndim):
        idx = tuple(sl[c] for c in choice)
        dst[idx] = src[idx]


def lift_spectrum(fh: np.ndarray, m: int) -> np.ndarray:
    out = np.zeros((m,) * fh.ndim, dtype=complex)
    _copy_low_modes(fh, out)
    return out


def restrict_spectrum(gh: np.ndarray, n: int) -> np.ndarray:
    out = np.zeros((n,) * gh.ndim, dtype=complex)
    _copy_low_modes(gh, out)
    return out


def to_fine(u: np.ndarray, m: int | None = None) -> np.ndarray:
    n = u.shape[0]
    if m is None:
        m = _fine_n(n)
    scale = (m / n) ** u.ndim
    return np.fft.ifftn(lift_spectrum(np.fft.fftn(u), m)).real * scale


def from_fine(u_fine: np.ndarray, n: int) -> np.ndarray:
    m = u_fine.shape[0]
    scale = (m / n) ** u_fine.ndim
    return np.fft.ifftn(restrict_spectrum(np.fft.fftn(u_fine) / scale, n)).real


def pad_product(*fields: np.ndarray, factor: float = 1.5) -> np.ndarray:
    """Produit ponctuel désaliasé par padding 3/2 (degré = nombre de champs)."""
    if not fields:
        raise ValueError("pad_product: au moins un champ")
    n = fields[0].shape[0]
    m = _fine_n(n, factor)
    acc = np.ones((m,) * fields[0].ndim, dtype=float)
    for f in fields:
        if f.shape != fields[0].shape:
            raise ValueError("champs de formes distinctes")
        acc = acc * to_fine(f, m)
    return from_fine(acc, n)
