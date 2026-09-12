#!/usr/bin/env python3
"""Budget GUM minimal — u_c et U, pas un institut."""

from __future__ import annotations

import math
from typing import Any

from mvcg.metrics import _adc


def u_a(s: float, n: int) -> float:
    if n < 2:
        raise ValueError("type A : N ≥ 2")
    return float(s) / math.sqrt(int(n))


def u_line(ln: dict[str, Any]) -> float:
    kind = str(ln.get("type", "B")).upper()
    if kind == "A":
        return u_a(float(ln["s"]), int(ln["N"]))
    return float(ln["u"])


def u_c(lines: list[dict[str, Any]]) -> float:
    acc = 0.0
    for ln in lines:
        c = float(ln.get("c", 1.0))
        acc += (c * u_line(ln)) ** 2
    return math.sqrt(acc)


def U(uc: float, k: float = 2.0) -> float:
    return float(k) * float(uc)


def uc_delta_rel(u_loc: float, u_ref: float, mu_loc: float, mu_ref: float) -> float:
    if mu_ref == 0:
        return math.inf
    t1 = u_loc / abs(mu_ref)
    t2 = abs(mu_loc) * u_ref / (mu_ref * mu_ref)
    return math.sqrt(t1 * t1 + t2 * t2)


def verdict_gum(delta: float, theta: float, uc: float, k: float, decide: str) -> str:
    if decide == "U":
        thr = U(uc, k)
    elif decide == "theta":
        thr = float(theta)
    else:
        raise ValueError("gum.decide ∈ {U, theta}")
    return _adc(delta, thr)


def apply_gum(delta: float, theta: float, gum: dict[str, Any] | None) -> dict[str, Any]:
    if not gum:
        from mvcg.metrics import _verdict

        return {"verdict": _verdict(delta, theta), "uc": None, "U": None, "decide": None}
    lines = list(gum.get("lines") or [])
    uc = u_c(lines) if lines else 0.0
    k = float(gum.get("k", 2.0))
    decide = str(gum.get("decide", "theta"))
    return {
        "verdict": verdict_gum(delta, theta, uc, k, decide),
        "uc": uc,
        "U": U(uc, k),
        "decide": decide,
        "k": k,
    }
