#!/usr/bin/env python3
"""Balayage de dictionnaires U — un levier packet, plusieurs mots.

μ_loc est gelé (répétition). Chaque paquet recalcule μ_ref quand la
formule le permet (Dirac, flux, Coulomb). Sinon le paquet est juste
accepté ou refusé par parse_units.
"""

from __future__ import annotations

from typing import Any

from mvcg.metrics import _delta, _verdict
from mvcg.rationalization import (
    PACKETS,
    UnitSystem,
    dirac_product,
    parse_units,
)

SI_VACUUM = {"epsilon0": 8.8541878128e-12, "mu0": 1.25663706212e-6}


def _unit_doc(packet: str) -> dict[str, Any]:
    doc: dict[str, Any] = {"packet": packet, "vintage": "sweep"}
    if packet == "si":
        doc.update(SI_VACUUM)
    return doc


def sweep_dirac(mu_loc: float = 2.0 * 3.141592653589793, theta: float = 1e-9, n: int = 1) -> dict[str, Any]:
    """eg mesuré en HL (2π) ; chaque U donne sa cible Dirac."""
    rows = []
    for packet in PACKETS:
        try:
            U = parse_units(_unit_doc(packet), dimension="e*g")
            if packet == "1":
                raise ValueError("paquet 1 : pas de cible Dirac")
            mu_ref = float(dirac_product(n, U))
            delta = _delta(mu_loc, mu_ref, "rel")
            verdict = _verdict(delta, theta)
            kill = None
        except (ValueError, TypeError, AssertionError) as exc:
            mu_ref, delta, verdict, kill = None, None, "S-", str(exc)
        rows.append(
            {
                "packet": packet,
                "mu_loc": mu_loc,
                "mu_ref": mu_ref,
                "theta": theta,
                "delta": delta,
                "verdict": verdict,
                "units_kill": kill,
            }
        )
    return {
        "protocol": "MVC-G-DICT-0.1",
        "s": "eg = cible Dirac(U)",
        "lever": "packet ← hl|gauss|si|1",
        "note": "μ_loc gelé ; seul U bouge",
        "rows": rows,
    }


def sweep_contact(
    mu_loc: float,
    mu_ref: float,
    dimension: str,
    theta: float,
    delta_kind: str = "rel",
    thr: float | None = None,
) -> dict[str, Any]:
    """μ_loc et μ_ref gelés : le paquet ne change le mot que s'il est illicite.

    thr : seuil de décision réel du contact (U si decide=U) pour un
    balayage À MÊME ÉTALONNAGE (chantier A2, 2026-09-14). Par défaut
    (None) : θ seul — comportement historique du street sweep, figé
    par les tests « deux instruments » (CKM, HVP, HLbL). Ne pas
    changer ce défaut : c'est un gel.
    """
    seuil = float(thr) if thr is not None else float(theta)
    rows = []
    for packet in PACKETS:
        try:
            parse_units(_unit_doc(packet), dimension=dimension)
            delta = _delta(mu_loc, mu_ref, delta_kind)
            verdict = _verdict(delta, seuil)
            kill = None
        except (ValueError, TypeError) as exc:
            delta, verdict, kill = None, "S-", str(exc)
        rows.append(
            {
                "packet": packet,
                "mu_loc": mu_loc,
                "mu_ref": mu_ref,
                "dimension": dimension,
                "delta": delta,
                "thr": seuil,
                "verdict": verdict,
                "units_kill": kill,
            }
        )
    return {
        "protocol": "MVC-G-DICT-0.1",
        "s": "μ figés, U variable",
        "lever": "packet",
        "rows": rows,
    }


def run_dictionaries() -> dict[str, Any]:
    return {
        "protocol": "MVC-G-DICT-0.1",
        "warning": "un S+ n'est vrai que pour le packet de sa ligne",
        "dirac_eg_2pi": sweep_dirac(),
        "raie_eV": sweep_contact(-13.605693122994, -13.605693122994, "eV", 1e-12, "rel"),
        "fermeture_omega": sweep_contact(0.0, 0.0, "1", 1e-3, "abs"),
    }
