#!/usr/bin/env python3
"""Structures candidates — engrenages du noyau, pas une ontologie.

Chaque candidat expose (D, S, L, μ_ref, θ, U) puis un run() qui rend μ_loc.
Le noyau (gel, U, métrique, d) décide S+/P/S-.
"""

from __future__ import annotations

import math
from dataclasses import asdict, dataclass
from typing import Any, Callable

import numpy as np

from mvcg.ash_instrument import AshParams, analyze as ash_analyze
from mvcg.dynamics import DynParams, analyze as dyn_analyze
from mvcg.rationalization import UnitSystem, check_dirac_identity, dirac_product


@dataclass
class Candidate:
    id: str
    domain: str
    orig: str  # pred | thm | proto
    phys: int
    packet: str
    dimension: str
    delta_kind: str
    theta: float
    mu_ref: float
    lever: str
    note: str
    runner: str


def _dirac_hl() -> tuple[float, dict]:
    U = UnitSystem(packet="hl", vintage="convention")
    out = check_dirac_identity(e=1.0, g=2.0 * math.pi, n=1, U=U)
    return float(out["eg"]), {"expected": out["eg_expected"], "identity": out["identity"]}


def _dirac_wrong_packet() -> tuple[float, dict]:
    """eg Gauss lu comme référence HL — le dictionnaire doit échouer."""
    return 0.5, {"note": "n/2 Gauss présenté contre 2π HL"}


def _ash_gain() -> tuple[float, dict]:
    fs = 256.0
    t = np.arange(0.0, 2.0, 1.0 / fs)
    x = np.sin(2.0 * np.pi * 4.0 * t)
    rep = ash_analyze(x, fs, AshParams(f0=1.0, n_oct=4, tau=0.1))
    return float(rep.gain_ratio), {"gain_stable": rep.gain_stable, "R_top": rep.R_top}


def _spectral_conserve() -> tuple[float, dict]:
    r = dyn_analyze(
        DynParams(
            n=32, steps=20, nu0=0.0, torsion=0.8, seed=1,
            pressure_mode="spectral", dealias=True,
        )
    )
    return float(r.energy_ratio), {"div": r.div_rms, "high_k": r.high_k_frac}


def _spectral_gyro_energy() -> tuple[float, dict]:
    on = dyn_analyze(
        DynParams(n=32, steps=20, nu0=0.0, torsion=0.8, seed=1,
                  pressure_mode="spectral", dealias=True)
    )
    off = dyn_analyze(
        DynParams(n=32, steps=20, nu0=0.0, torsion=0.0, seed=1,
                  pressure_mode="spectral", dealias=True)
    )
    return abs(on.energy_ratio - off.energy_ratio), {
        "r_T": on.energy_ratio, "r_0": off.energy_ratio, "p_rms_T": on.p_rms
    }


def _poisson_num_dissipation() -> tuple[float, dict]:
    r = dyn_analyze(
        DynParams(n=32, steps=40, nu0=0.0, torsion=0.0, seed=0, pressure_mode="poisson")
    )
    return float(1.0 - r.energy_ratio), {"r": r.energy_ratio, "div": r.div_rms}


def _bps_profile_ratio() -> tuple[float, dict]:
    """Proxy C(ρ): masse relâchée / borne. Ici r spectral ν>0 vs ν=0 (pas un monopôle)."""
    bps = dyn_analyze(
        DynParams(n=32, steps=20, nu0=0.0, torsion=0.0, seed=1,
                  pressure_mode="spectral", dealias=True)
    )
    full = dyn_analyze(
        DynParams(n=32, steps=20, nu0=0.05, torsion=0.0, seed=1,
                  pressure_mode="spectral", dealias=True)
    )
    c = full.energy_end / (bps.energy_end + 1e-15)
    return float(c), {"E_nu0": bps.energy_end, "E_nu": full.energy_end}


RUNNERS: dict[str, Callable[[], tuple[float, dict]]] = {
    "dirac_hl": _dirac_hl,
    "dirac_wrong_packet": _dirac_wrong_packet,
    "ash_gain": _ash_gain,
    "spectral_conserve": _spectral_conserve,
    "spectral_gyro_energy": _spectral_gyro_energy,
    "poisson_num_dissipation": _poisson_num_dissipation,
    "bps_profile_ratio": _bps_profile_ratio,
}

CATALOG: list[Candidate] = [
    Candidate("dirac_hl", "physique", "thm", 1, "hl", "e*g", "rel", 1e-9, 2.0 * math.pi,
              "paquet HL déclaré", "identité Dirac en HL", "dirac_hl"),
    Candidate("dirac_wrong_packet", "physique", "thm", 1, "hl", "e*g", "rel", 1e-3, 2.0 * math.pi,
              "mauvais dictionnaire", "0.5 Gauss contre 2π HL", "dirac_wrong_packet"),
    Candidate("ash_gain", "instrument", "proto", 0, "hl", "1", "abs", 1e-8, 0.0,
              "gain ×2", "I-A3 profil relatif", "ash_gain"),
    Candidate("spectral_conserve", "dynamique", "thm", 0, "hl", "1", "rel", 1e-2, 1.0,
              "ν=0 spectral", "conservation d'énergie", "spectral_conserve"),
    Candidate("spectral_gyro_energy", "dynamique", "thm", 0, "hl", "1", "abs", 1e-4, 0.0,
              "T←0", "gyro ne travaille pas (spectral)", "spectral_gyro_energy"),
    Candidate("poisson_num_dissipation", "dynamique", "proto", 0, "hl", "1", "abs", 0.05, 0.0,
              "ν=0 5points", "ε_num du projecteur inconsistent", "poisson_num_dissipation"),
    Candidate("bps_profile_ratio", "dynamique", "proto", 0, "hl", "1", "rel", 0.5, 1.0,
              "ν←0", "ratio d'énergie vs cas sans dissipation — proxy pas un monopôle",
              "bps_profile_ratio"),
]


def run_candidate(c: Candidate) -> dict[str, Any]:
    mu_loc, extra = RUNNERS[c.runner]()
    return {
        "id": c.id,
        "domain": c.domain,
        "orig": c.orig,
        "phys": c.phys,
        "packet": c.packet,
        "dimension": c.dimension,
        "delta_kind": c.delta_kind,
        "theta": c.theta,
        "mu_ref": c.mu_ref,
        "mu_loc": mu_loc,
        "lever": c.lever,
        "note": c.note,
        "extra": extra,
    }
