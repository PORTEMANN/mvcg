#!/usr/bin/env python3
"""Vitesse critique de Landau — minimisation de E(p)/p sur un spectre déclaré.

Critère de Landau (1941) : un superfluide reste sans dissipation tant
que la vitesse de l'écoulement est inférieure à

    v_c = min_p E(p) / p

Sur le spectre phonon-roton de ⁴He II, le minimum est atteint au
roton — c'est ce que le calcul vérifie à partir de la table déclarée,
sans ajuster aucun point sur la référence.

Pur standard : scan fin + interpolation quadratique locale.
"""

from __future__ import annotations

import math
from typing import Any

H_BAR = 1.054571817e-34  # J s (CODATA-2018)
K_B = 1.380649e-23       # J K^-1 (exact)
ANGSTROM = 1e-10         # m


def _E_over_p(k_ang: float, E_K: float) -> float:
    """E(p)/p en m/s pour k en Å^-1 et E/k_B en K."""
    if k_ang <= 0.0:
        return math.inf
    p = H_BAR * k_ang / ANGSTROM
    E = K_B * E_K
    return E / p


def landau_vc(points: list[list[float]], n_scan: int = 4000) -> dict[str, Any]:
    """v_c par scan + parabole locale sur les trois voisins du minimum.

    points : [[k_ang, E_K], ...] trié par k croissant, k > 0 ignoré à
    l'origine (E/p → pente phonon). Aucune contrainte sur la forme :
    la parabole n'est qu'un raffinement local, le min reste encadré
    par les points déclarés.
    """
    pts = sorted((float(k), float(E)) for k, E in points if float(k) > 0.0)
    if len(pts) < 3:
        raise ValueError("spectre : ≥ 3 points k > 0")
    k_min, k_max = pts[0][0], pts[-1][0]

    def interp(k: float) -> float:
        # interpolation linéaire entre voisins déclarés
        for (k0, e0), (k1, e1) in zip(pts, pts[1:]):
            if k0 <= k <= k1:
                if k1 == k0:
                    return e0
                return e0 + (e1 - e0) * (k - k0) / (k1 - k0)
        raise ValueError("hors spectre")

    best_k, best_v = None, math.inf
    for i in range(1, n_scan + 1):
        k = k_min + (k_max - k_min) * i / n_scan
        v = _E_over_p(k, interp(k))
        if v < best_v:
            best_k, best_v = k, v

    # parabole locale E(k) sur les voisins du minimum scanne
    dk = (k_max - k_min) / n_scan
    k_a, k_b, k_c = best_k - dk, best_k, best_k + dk
    e_a, e_b, e_c = interp(k_a), interp(k_b), interp(k_c)
    denom = (e_a - 2.0 * e_b + e_c)
    k_star = k_b if abs(denom) < 1e-18 else k_b - 0.5 * (e_a - e_c) * dk / denom
    if not (k_min <= k_star <= k_max):
        k_star = k_b
    v_c = _E_over_p(k_star, interp(k_star))

    return {
        "vc_m_s": v_c,
        "k_star_ang^-1": k_star,
        "E_star_K": interp(k_star),
        "mechanism": "roton" if k_star > 1.0 else "phonon",
    }


def spectrum_doc() -> dict[str, Any]:
    from mvcg.tables import load_table

    return load_table("he4_spectrum_LANDAU.json")
