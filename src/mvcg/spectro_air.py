#!/usr/bin/env python3
"""Indice de l'air — pont ν̃_air ↔ ν̃_vide.

Convention : ν̃_air = n ν̃_vide,  ν̃_vide = ν̃_air / n.
n gelé (STP déclaré). Pas un fetch météo.
HITRAN / tables zip : vide sauf mention contraire.
"""

from __future__ import annotations

from typing import Any

# Air sec, 15 °C, 1013.25 hPa, visible — ordre Edlén, vintage déclaré.
N_AIR_STP = 1.000272
VINTAGE = "AIR-n-DECLARE-STP-15C"


def n_air(vintage: str = VINTAGE) -> float:
    if vintage != VINTAGE:
        raise ValueError(f"n_air : vintage inconnu {vintage}")
    return N_AIR_STP


def vacuum_from_air(nubar_air: float, n: float | None = None) -> float:
    return float(nubar_air) / float(n if n is not None else N_AIR_STP)


def air_from_vacuum(nubar_vac: float, n: float | None = None) -> float:
    return float(nubar_vac) * float(n if n is not None else N_AIR_STP)


def pont_air(n: float | None = None) -> dict[str, Any]:
    nn = float(n if n is not None else N_AIR_STP)
    return {
        "tau": "spectro-air",
        "src": "cm-1-air",
        "dst": "cm-1-vac",
        "k": 1.0 / nn,
        "n_air": nn,
        "vintage": VINTAGE,
        "note": "ν̃_vac = ν̃_air / n",
    }
