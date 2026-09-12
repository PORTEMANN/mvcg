#!/usr/bin/env python3
"""Corridor P2 — discret dans le continu, sans récit.

E68 : le mot dépend de n sur un blanc (pas sur une bande).
E64 : fenêtre κ comme θ-intervalle, pas une cavité.
"""

from __future__ import annotations

from typing import Any

from mvcg.dynamics import DynParams, analyze


def e68_n_white(ns: tuple[int, ...] = (16, 32)) -> dict[str, Any]:
    rows = []
    for n in ns:
        r = analyze(
            DynParams(
                n=n,
                steps=20,
                dt=0.002,
                nu0=0.05,
                torsion=0.0,
                pressure_mode="spectral",
                dealias=True,
                ic="white",
                nu_mode="const",
                seed=0,
            )
        )
        rows.append({"n": n, "energy_ratio": r.energy_ratio, "div_rms": r.div_rms})
    spread = max(x["energy_ratio"] for x in rows) - min(x["energy_ratio"] for x in rows)
    return {
        "id": "E68_n_white",
        "s": "r(n) plat sur IC blanc visqueux",
        "lever": "n←2n",
        "prevision": "mot_change",
        "spread": spread,
        "verdict": "S-" if spread > 1e-4 else "S+",
        "rows": rows,
        "note": "non-universalité en n — équivalent corridor E68",
    }


def e68_n_band(ns: tuple[int, ...] = (16, 32)) -> dict[str, Any]:
    rows = []
    for n in ns:
        r = analyze(
            DynParams(
                n=n,
                steps=20,
                dt=0.002,
                nu0=0.05,
                torsion=0.0,
                pressure_mode="spectral",
                dealias=True,
                ic="band",
                nu_mode="const",
                seed=0,
            )
        )
        rows.append({"n": n, "energy_ratio": r.energy_ratio})
    spread = max(x["energy_ratio"] for x in rows) - min(x["energy_ratio"] for x in rows)
    return {
        "id": "E68_n_band",
        "s": "r(n) plat sur IC bande",
        "lever": "n←2n",
        "prevision": "mot_stable",
        "spread": spread,
        "verdict": "S+" if spread <= 1e-6 else "S-",
        "rows": rows,
    }


def e64_kappa_window(kappa: float, lo: float = 0.075, hi: float = 0.125) -> dict[str, Any]:
    """Fenêtre déclarée — P si κ ∈ ]lo,hi[, sinon S−. Pas une cavité ANU."""
    inside = lo < kappa < hi
    return {
        "id": "E64_kappa_window",
        "s": f"κ ∈ ]{lo},{hi}[",
        "mu_loc": kappa,
        "theta_lo": lo,
        "theta_hi": hi,
        "verdict": "P" if inside else "S-",
        "note": "intervalle gelé ; E68 dit que la fenêtre n'est pas universelle en n",
    }


def run_corridor() -> dict[str, Any]:
    white = e68_n_white()
    band = e68_n_band()
    win_in = e64_kappa_window(0.10)
    win_out = e64_kappa_window(0.40)
    return {
        "protocol": "MVC-G-CORRIDOR-0.1",
        "warning": "discret dans le continu — pas Hopf, pas ANU, pas E8",
        "rows": [white, band, win_in, win_out],
    }
