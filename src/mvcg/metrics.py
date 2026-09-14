#!/usr/bin/env python3
"""Métrique de contact phénoménologique.

μ = (μ_loc, μ_ref, δ, θ, U, dimension)
S+ seulement si référence, unités et seuil sont là *avant* le verdict.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from typing import Any, Optional

import hashlib
from datetime import datetime, timezone

from mvcg.rationalization import UnitSystem, parse_units, units_payload

PROTOCOL_MET = "MET-LIB-1.5-MET"


def _canonical(obj: Any) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")


def _sha(obj: Any) -> str:
    return hashlib.sha256(_canonical(obj)).hexdigest()


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")


@dataclass
class ContactMetric:
    protocol: str
    frontier_id: str
    mu_loc: float
    mu_ref: float
    delta: float
    delta_kind: str  # abs | rel
    theta: float
    dimension: str
    units: dict
    units_sha256: str
    verdict: str  # S+ | P | S-
    measured_at: str
    metric_sha256: str


def _delta(mu_loc: float, mu_ref: float, kind: str) -> float:
    if kind == "abs":
        return abs(mu_loc - mu_ref)
    if kind == "rel":
        if mu_ref == 0:
            return math.inf if mu_loc != 0 else 0.0
        return abs(mu_loc / mu_ref - 1.0)
    raise ValueError("delta_kind ∈ {abs, rel}")


def _adc(delta: float, thr: float) -> str:
    """Convertisseur 3 niveaux : on tranche, on n'explique pas."""
    if not math.isfinite(delta):
        return "S-"
    if delta <= thr:
        return "S+"
    if delta <= 2.0 * thr:
        return "P"
    return "S-"


def marge_adc(delta: float, thr: float, mot: str) -> float:
    """Distance POSITIVE à la frontière où le mot de _adc basculerait.

    S+ : thr - δ (montée en P à δ = thr) ; P : min(δ - thr, 2 thr - δ)
    (frontière la plus proche, des deux côtés) ; S- : δ - 2 thr
    (redescente en P à δ = 2 thr). Campagne MARGE (2026-09-14) : la
    marge classe l'exposition d'un verdict, ce n'est pas une p-value.
    """
    if mot == "S+":
        return thr - delta
    if mot == "P":
        return min(delta - thr, 2.0 * thr - delta)
    return delta - 2.0 * thr


def _verdict(delta: float, theta: float, sigma: float | None = None) -> str:
    th = float(theta)
    if sigma is not None:
        # héritage max(θ, σ) — à ne plus étendre (voir DISCRET-CONTINU, capot C)
        th = max(th, float(sigma))
    return _adc(delta, th)


def build_metric(
    frontier_id: str,
    mu_loc: float,
    mu_ref: float,
    theta: float,
    U: UnitSystem,
    dimension: str,
    delta_kind: str = "rel",
) -> ContactMetric:
    if dimension.strip() == "":
        raise ValueError("dimension obligatoire (ex. 1, MeV, cm^-1, e*g)")
    if delta_kind == "rel" and dimension not in ("1", "dimensionless", "eg", "e*g"):
        # relatif licite aussi pour grandeurs dimensionnées (écart relatif)
        pass
    payload_u = units_payload(U)
    dlt = _delta(float(mu_loc), float(mu_ref), delta_kind)
    body = {
        "protocol": PROTOCOL_MET,
        "frontier_id": frontier_id,
        "mu_loc": float(mu_loc),
        "mu_ref": float(mu_ref),
        "delta": dlt,
        "delta_kind": delta_kind,
        "theta": float(theta),
        "dimension": dimension,
        "units": payload_u,
        "units_sha256": _sha(payload_u),
        "verdict": _verdict(dlt, float(theta)),
        "measured_at": _now(),
    }
    rec = ContactMetric(metric_sha256=_sha(body), **body)
    return rec


def audit_metric(rec: ContactMetric | dict[str, Any]) -> dict[str, Any]:
    doc = rec if isinstance(rec, dict) else asdict(rec)
    kills = []
    if doc.get("mu_ref") is None:
        kills.append("I-V6: mu_ref vide")
    if not doc.get("dimension"):
        kills.append("dimension vide")
    try:
        U = parse_units(doc["units"])
    except Exception as exc:  # noqa: BLE001
        kills.append(f"U illisible: {exc}")
        U = None
    if U is not None and U.packet == "si" and doc.get("dimension") in ("eg", "e*g"):
        if U.mu0 is None:
            kills.append("SI + Dirac : mu0 manquant")
    stored = doc.get("metric_sha256")
    body = {k: v for k, v in doc.items() if k != "metric_sha256"}
    if stored and stored != _sha(body):
        kills.append("metric_sha256 ≠ payload")
    if U is not None:
        u_sha = _sha(units_payload(U))
        if u_sha != doc.get("units_sha256"):
            kills.append("units_sha256 ≠ U")
    return {
        "kill": bool(kills),
        "reasons": kills,
        "verdict": doc.get("verdict"),
        "delta": doc.get("delta"),
    }
