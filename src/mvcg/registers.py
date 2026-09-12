#!/usr/bin/env python3
"""Trois registres = trois tiroirs de contacts, pas trois substances.

micro  — tables / formules (raie, Rydberg, masse)
meso   — partitions / profils (atlas, Dice, instrument)
macro  — bilans (H^2, Ω, vintage H0)
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable

import numpy as np

from mvcg.metrics import _delta, _verdict
from mvcg.rationalization import parse_units


REGISTERS = ("micro", "meso", "macro")


@dataclass
class Contact:
    id: str
    register: str
    orig: str
    packet: str
    dimension: str
    delta_kind: str
    theta: float
    mu_ref: float
    lever: str
    lever_off_note: str
    s_phrase: str
    note: str
    runner: str
    statut: str = "ouverte"
    expected: str | None = None
    campaign: str = ""


def _h1s_rydberg() -> tuple[float, dict]:
    from mvcg.tables import load_table

    c = load_table("codata2018_extract.json")["constants"]
    r_inf_ev = float(c["Rydberg_eV"])
    return -r_inf_ev, {"r_inf_ev": r_inf_ev, "n": 1, "vintage": "CODATA-2018"}


def _h1s_rydberg_vintage_off() -> tuple[float, dict]:
    """Levier vintage : R arrondi 13.6 eV."""
    return -13.6, {"r_inf_ev": 13.6, "lever": "vintage←13.6"}


def _dice(a: np.ndarray, b: np.ndarray) -> float:
    inter = float(np.sum(a == b))
    return 2.0 * inter / (a.size + b.size + 1e-15)


def _aal_dice_stable() -> tuple[float, dict]:
    """Partition synthétique : même atlas, lissage léger (proto, pas un cerveau)."""
    rng = np.random.default_rng(0)
    atlas = rng.integers(0, 8, size=(32, 32))
    # lissage = vote majoritaire 3x3
    pad = np.pad(atlas, 1, mode="edge")
    flat = np.lib.stride_tricks.sliding_window_view(pad, (3, 3))
    smooth = np.array([[np.bincount(flat[i, j].ravel()).argmax()
                        for j in range(32)] for i in range(32)])
    d = _dice(atlas, smooth)
    return d, {"n_labels": 8, "grid": 32, "lever_pending": "atlas←autre"}


def _p20_h2plus_lcao() -> tuple[float, dict]:
    from mvcg.h2plus import lcao_1s
    from mvcg.tables import h2plus_de

    t = h2plus_de()
    sol = lcao_1s(2.0)
    return float(sol["De_eV"]), {
        "table": t["vintage"],
        "mu_ref_table": t["value"],
        "ansatz": "LCAO 1s Lowe R=2",
        "S": sol["S"],
        "E": sol["E"],
    }


def _p21_h2o_point_charge() -> tuple[float, dict]:
    from mvcg.tables import h2o_dipole

    t = h2o_dipole()
    return float(t["ansatz_point_charge"]), {"table": t["vintage"], "ref": t["value"]}


def _p30_kato_gaussian() -> tuple[float, dict]:
    from mvcg.tables import kato_h

    t = kato_h()
    return float(t["ansatz_gaussian"]), {"table": t["vintage"], "ref": t["value"]}


def _p30_kato_exact() -> tuple[float, dict]:
    from mvcg.tables import kato_h

    t = kato_h()
    return float(t["value"]), {"table": t["vintage"], "ansatz": "1s exact"}


def _p27_he_hf() -> tuple[float, dict]:
    from mvcg.tables import he_corr

    t = he_corr()
    return 0.0, {"table": t["vintage"], "E_HF": t["E_HF_Ha"], "method": "HF"}


def _p27_he_table() -> tuple[float, dict]:
    from mvcg.tables import he_corr

    t = he_corr()
    return float(t["value"]), {"table": t["vintage"], "note": "tautologie table"}


def _p35_sigma_as_spike() -> tuple[float, dict]:
    """B3-FAIL déclaré : σ logistique n'est pas un spike. μ = 0 (overlap)."""
    return 0.0, {"model": "logistic_sigma", "target": "spike", "note": "réfuté"}


def _p20_h2plus_table_only() -> tuple[float, dict]:
    from mvcg.tables import h2plus_de

    t = h2plus_de()
    return float(t["value"]), {"table": t["vintage"], "note": "tautologie table=table"}


def _aal_dice_other_atlas() -> tuple[float, dict]:
    """Levier atlas←autre : permutation des labels + bruit de frontières."""
    rng = np.random.default_rng(0)
    atlas = rng.integers(0, 8, size=(32, 32))
    other = (atlas + 1) % 8
    other[rng.random(other.shape) < 0.15] = rng.integers(0, 8)
    d = _dice(atlas, other)
    return d, {"lever": "atlas←autre"}


def _friedmann_baryons_only() -> tuple[float, dict]:
    """1 - Ω_b  (bilan 'les connus suffisent', plat). vintage H0 déclaré, pas utilisé."""
    omega_b = 0.0493
    return 1.0 - omega_b, {"omega_b": omega_b, "H0_vintage": "Planck-2018", "flat": True}


def _friedmann_lcdm() -> tuple[float, dict]:
    """|1 - (Ω_m + Ω_Λ)|  — fermeture plate, millésime déclaré."""
    omega_m, omega_l = 0.315, 0.685
    return abs(1.0 - (omega_m + omega_l)), {
        "omega_m": omega_m, "omega_l": omega_l, "H0_vintage": "Planck-2018"
    }


def _friedmann_lcdm_shoes_H0() -> tuple[float, dict]:
    """Même Ω, autre vintage H0 — le levier ne doit PAS être une moyenne."""
    omega_m, omega_l = 0.315, 0.685
    return abs(1.0 - (omega_m + omega_l)), {
        "omega_m": omega_m, "omega_l": omega_l, "H0_vintage": "SH0ES",
        "note": "fermeture Ω indépendante de H0 ; H0 entrerait dans un autre μ",
    }


RUNNERS: dict[str, Callable[[], tuple[float, dict]]] = {
    "h1s_rydberg": _h1s_rydberg,
    "h1s_vintage": _h1s_rydberg_vintage_off,
    "aal_dice": _aal_dice_stable,
    "aal_other": _aal_dice_other_atlas,
    "frw_baryons": _friedmann_baryons_only,
    "frw_lcdm": _friedmann_lcdm,
    "frw_shoes": _friedmann_lcdm_shoes_H0,
    "p20_lcao": _p20_h2plus_lcao,
    "p20_table": _p20_h2plus_table_only,
    "p21_pc": _p21_h2o_point_charge,
    "p30_g": _p30_kato_gaussian,
    "p30_ex": _p30_kato_exact,
    "p35_sigma": _p35_sigma_as_spike,
    "p27_hf": _p27_he_hf,
    "p27_tab": _p27_he_table,
}

CONTACTS: list[Contact] = [
    Contact(
        "H1s_Rydberg", "micro", "pred", "si", "eV", "rel", 1e-12,
        -13.605693122994, "vintage←13.6", "voir H1s_Rydberg_13p6",
        "E_1s = -R_∞ (CODATA-2018 gelé)",
        "formule = constante déclarée ; pas un atome ontologique",
        "h1s_rydberg",
    ),
    Contact(
        "H1s_Rydberg_13p6", "micro", "pred", "si", "eV", "rel", 1e-12,
        -13.605693122994, "vintage←13.6 (actif)", "—",
        "même S, R arrondi",
        "levier vintage : doit casser un θ trop serré",
        "h1s_vintage",
    ),
    Contact(
        "P20_H2plus_LCAO", "micro", "pred", "si", "eV", "rel", 0.05,
        2.6508, "ansatz←table", "voir P20_H2plus_table",
        "De(H2+) LCAO 1s = table DEMO-2026",
        "ansatz pauvre vs constante déclarée ; pas un CCCBDB live",
        "p20_lcao",
    ),
    Contact(
        "P20_H2plus_table", "micro", "pred", "si", "eV", "rel", 1e-12,
        2.6508, "—", "—",
        "De(H2+) = table lue deux fois",
        "contrôle tautologique ; ne pas exporter comme P20",
        "p20_table",
        "ouverte", None, "P20",
    ),
    Contact(
        "P21_H2O_dipole", "micro", "pred", "si", "D", "rel", 0.05,
        1.8546, "ansatz←table", "—",
        "μ(H2O) charges ponctuelles = table DEMO-2026",
        "P21 rejoué en maquette",
        "p21_pc",
        "ouverte", "S-", "P21",
    ),
    Contact(
        "P30_Kato_gaussian", "micro", "pred", "1", "1", "abs", 0.05,
        -1.0, "ansatz←1s", "voir P30_Kato_1s",
        "(1/ψ)∂rψ|_0 = -Z  (gaussienne)",
        "P30 partiel d'origine : le continu lisse rate le cusp",
        "p30_g",
        "partielle", "S-", "P30",
    ),
    Contact(
        "P30_Kato_1s", "micro", "thm", "1", "1", "abs", 1e-12,
        -1.0, "—", "—",
        "(1/ψ)∂rψ|_0 = -1 pour 1s H exact",
        "identité de la 1s ; pas un solveur multi-corps",
        "p30_ex",
        "fermee", "S+", "P30",
    ),
    Contact(
        "P27_He_HF", "micro", "pred", "si", "Ha", "abs", 0.002,
        -0.042044, "methode←HF", "voir P27_He_table",
        "E_corr(He, HF) = table Hylleraas",
        "HF ne récupère aucune corrélation ; S− obligatoire",
        "p27_hf",
        "fermee", "S-", "P27",
    ),
    Contact(
        "P27_He_table", "micro", "pred", "si", "Ha", "abs", 1e-12,
        -0.042044, "—", "—",
        "E_corr(He) = table lue deux fois",
        "contrôle tautologique",
        "p27_tab",
        "ouverte", None, "P27",
    ),
    Contact(
        "P35_sigma_spike", "meso", "proto", "1", "1", "abs", 0.05,
        1.0, "modele←HH", "—",
        "σ logistique recouvre le spike",
        "B3-FAIL déclaré : overlap 0 vs 1",
        "p35_sigma",
        "fermee", "S-", "P35",
    ),
    Contact(
        "AAL_dice_lissage", "meso", "proto", "1", "1", "abs", 0.05,
        1.0, "atlas←autre", "voir AAL_dice_atlas",
        "Dice(atlas, atlas lissé 3×3) ≈ 1",
        "partition synthétique ; pas une carte cérébrale",
        "aal_dice",
    ),
    Contact(
        "AAL_dice_atlas", "meso", "proto", "1", "1", "abs", 0.05,
        1.0, "atlas←autre (actif)", "—",
        "Dice(atlas, autre atlas)",
        "levier atlas : prévision mot_change",
        "aal_other",
    ),
    Contact(
        "FRW_baryons", "macro", "pred", "1", "1", "abs", 0.05,
        0.0, "Ω_c←0 déjà", "ajouter Ω_c+Ω_Λ",
        "1-Ω_b = 0  (les connus ferment le bilan plat)",
        "H0 vintage Planck-2018 gelé ; S- attendu",
        "frw_baryons",
    ),
    Contact(
        "FRW_lcdm_Planck", "macro", "pred", "1", "1", "abs", 1e-3,
        0.0, "H0←SH0ES en contact séparé", "voir FRW_lcdm_SH0ES",
        "|1-(Ω_m+Ω_Λ)|=0  millésime Planck Ω",
        "fermeture plate ; H0 n'entre pas dans ce μ",
        "frw_lcdm",
    ),
    Contact(
        "FRW_lcdm_SH0ES", "macro", "pred", "1", "1", "abs", 1e-3,
        0.0, "H0 vintage SH0ES (même Ω)", "—",
        "même fermeture Ω, autre étiquette H0",
        "montre que CE μ ignore H0 — un vrai contact H0 serait H(z) vs donnée",
        "frw_shoes",
    ),
]


def run_contact(c: Contact) -> dict[str, Any]:
    mu_loc, extra = RUNNERS[c.runner]()
    delta = _delta(mu_loc, c.mu_ref, c.delta_kind)
    verdict = _verdict(delta, c.theta)
    units_kill = None
    try:
        U = parse_units(
            {"packet": c.packet, "vintage": "registre"},
            dimension=c.dimension,
        )
        packet = U.packet
    except (ValueError, TypeError, KeyError) as exc:
        U = None
        packet = c.packet
        units_kill = str(exc)
        verdict = "S-"
    return {
        "id": c.id,
        "register": c.register,
        "orig": c.orig,
        "s": c.s_phrase,
        "lever": c.lever,
        "mu_loc": mu_loc,
        "mu_ref": c.mu_ref,
        "theta": c.theta,
        "delta": delta,
        "verdict": verdict,
        "dimension": c.dimension,
        "packet": packet,
        "note": c.note,
        "extra": extra,
        "units_kill": units_kill,
        "statut": c.statut,
        "expected": c.expected,
        "campaign": c.campaign,
        "b3_fail": bool(c.expected and verdict != c.expected),
    }


def run_registers() -> dict[str, Any]:
    rows = [run_contact(c) for c in CONTACTS]
    by = {r: [x for x in rows if x["register"] == r] for r in REGISTERS}
    return {
        "protocol": "MVC-G-REGISTRES-0.1",
        "warning": "trois tiroirs, pas trois substances ; S+ ne s'exporte pas",
        "counts": {
            r: {
                "n": len(by[r]),
                "S+": sum(1 for x in by[r] if x["verdict"] == "S+"),
                "P": sum(1 for x in by[r] if x["verdict"] == "P"),
                "S-": sum(1 for x in by[r] if x["verdict"] == "S-"),
            }
            for r in REGISTERS
        },
        "rows": rows,
    }
