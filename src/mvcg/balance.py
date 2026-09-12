#!/usr/bin/env python3
"""Tare et calibres — analogie de la balance.

tare    : ce qu'on soustrait avant δ (plateau vide, H séparé, E_HF).
caliber : jeu de poids étalon pour θ, pas un levier pour forcer S+.
"""

from __future__ import annotations

from typing import Any

# Calibres déclarés — choisir *avant* le run, geler dans D.
CALIBERS: dict[str, dict[str, Any]] = {
    "fin": {"theta_rel": 1e-12, "theta_abs": 1e-12, "note": "identité / constante"},
    "labo": {"theta_rel": 0.05, "theta_abs": 0.002, "note": "ansatz vs table"},
    "grossier": {"theta_rel": 0.20, "theta_abs": 0.05, "note": "ordre de grandeur"},
}


def after_tare(raw: float, tare: float) -> float:
    """μ sur le plateau une fois la tare ôtée."""
    return float(raw) - float(tare)


def caliber_theta(name: str, kind: str) -> float:
    if name not in CALIBERS:
        raise ValueError(f"caliber ∈ {tuple(CALIBERS)}, reçu {name!r}")
    key = "theta_rel" if kind == "rel" else "theta_abs"
    return float(CALIBERS[name][key])
