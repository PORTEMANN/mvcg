#!/usr/bin/env python3
"""Rationalisation des champs : Gauss, Heaviside–Lorentz, SI.

Ce module ne découvre aucune constante. Il convertit les dictionnaires.
q_HL = sqrt(4π) q_G. Dirac : eg = 2πn (HL) = n/2 (Gauss).
"""

from __future__ import annotations

import math
from dataclasses import asdict, dataclass
from typing import Any, Literal, Optional

Packet = Literal["hl", "gauss", "si", "1"]
PACKETS = ("hl", "gauss", "si", "1")
EM_DIMENSIONS = frozenset({"eg", "e*g", "C", "A", "V", "T", "Wb", "F", "H"})
PI = math.pi
FOUR_PI = 4.0 * math.pi
SQRT_FOUR_PI = math.sqrt(FOUR_PI)


@dataclass(frozen=True)
class UnitSystem:
    packet: str
    vintage: str
    hbar: float = 1.0
    c: float = 1.0
    epsilon0: Optional[float] = None
    mu0: Optional[float] = None
    note: str = ""

    def __post_init__(self) -> None:
        if self.packet not in PACKETS:
            raise ValueError(f"packet ∈ {PACKETS}")
        object.__setattr__(self, "packet", self.packet)


def parse_units(doc: dict[str, Any], dimension: str = "") -> UnitSystem:
    """Lit un dictionnaire U. packet obligatoire. SI+EM exige ε0, μ0."""
    if not isinstance(doc, dict):
        raise TypeError("U doit être un objet {packet, vintage, ...}")
    if "packet" not in doc or doc["packet"] in (None, ""):
        raise ValueError("packet obligatoire (hl|gauss|si|1)")
    raw = str(doc["packet"]).strip().lower()
    if raw in ("1", "dimensionless", "un"):
        raw = "1"
    if raw not in PACKETS:
        raise ValueError(f"packet ∈ {PACKETS}, reçu {doc['packet']!r}")
    dim = str(dimension or doc.get("dimension") or "").strip()
    eps = None if doc.get("epsilon0") is None else float(doc["epsilon0"])
    mu = None if doc.get("mu0") is None else float(doc["mu0"])
    if raw == "si" and dim in EM_DIMENSIONS and eps == 1.0 and (mu is None or mu == 1.0):
        raise ValueError("si + epsilon0=1 : usurpation HL — reclasser packet=hl")
    if raw == "si" and dim in EM_DIMENSIONS and (eps is None or mu is None):
        raise ValueError("SI + dimension EM exige epsilon0 et mu0 dans U")
    return UnitSystem(
        packet=raw,
        vintage=str(doc.get("vintage", "unspecified")),
        hbar=float(doc.get("hbar", 1.0)),
        c=float(doc.get("c", 1.0)),
        epsilon0=eps,
        mu0=mu,
        note=str(doc.get("note", "")),
    )


def charge_to_hl(q: float, src: Packet) -> float:
    if src == "hl":
        return q
    if src == "gauss":
        return q * SQRT_FOUR_PI
    raise ValueError("conversion SI → HL : passer par e_SI et ε0, pas un simple facteur")


def charge_from_hl(q_hl: float, dst: Packet) -> float:
    if dst == "hl":
        return q_hl
    if dst == "gauss":
        return q_hl / SQRT_FOUR_PI
    raise ValueError("conversion HL → SI : non unitaire, exiger ε0")


def dirac_product(n: int, U: UnitSystem) -> float:
    """Valeur attendue de e·g pour la charge magnétique minimale × n."""
    if n < 0:
        n = -n
    if U.packet == "hl":
        return 2.0 * PI * n * U.hbar
    if U.packet == "gauss":
        return 0.5 * n * U.hbar * U.c
    # SI : eg = 2π n ħ / (μ0 c)   (une écriture usuelle cohérente avec μ0)
    assert U.mu0 is not None
    return (2.0 * PI * n * U.hbar) / (U.mu0 * U.c)


def flux_quantum(e: float, U: UnitSystem) -> float:
    """Quantum de flux Φ(n=1) vu à l'infini d'un monopôle."""
    if U.packet == "hl":
        return 2.0 * PI / e
    if U.packet == "gauss":
        return FOUR_PI / e
    assert U.epsilon0 is not None
    return 2.0 * PI * U.epsilon0 * U.hbar * U.c / e  # forme à déclarer dans D si utilisée


def coulomb_prefactor(U: UnitSystem) -> float:
    """Préfacteur de V = k q1 q2 / r."""
    if U.packet == "hl":
        return 1.0 / FOUR_PI
    if U.packet == "gauss":
        return 1.0
    assert U.epsilon0 is not None
    return 1.0 / (FOUR_PI * U.epsilon0)


def maxwell_div_e_prefactor(U: UnitSystem) -> float:
    """Coefficient tel que ∇·E = α ρ  (statique, sans 4π caché ailleurs)."""
    if U.packet == "hl":
        return 1.0
    if U.packet == "gauss":
        return FOUR_PI
    assert U.epsilon0 is not None
    return 1.0 / U.epsilon0


def check_dirac_identity(e: float, g: float, n: int, U: UnitSystem) -> dict[str, Any]:
    expected = dirac_product(n, U)
    got = e * g
    if expected == 0:
        rel = math.inf
    else:
        rel = abs(got / expected - 1.0)
    return {
        "packet": U.packet,
        "n": n,
        "eg": got,
        "eg_expected": expected,
        "delta_rel": rel,
        "identity": rel == 0.0 or rel < 1e-12,
    }


def units_payload(U: UnitSystem) -> dict[str, Any]:
    return asdict(U)
