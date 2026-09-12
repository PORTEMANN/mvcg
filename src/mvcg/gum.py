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


def _check_R_sdp(R: list[list[float]], n: int) -> None:
    """R matrice de corrélation : structure + SDP, pur standard.

    Pour n ≤ 2 la SDP se vérifie en forme close (λ_min ≥ 0). Au-delà,
    la validation structurelle (symétrie, diag 1, |ρ| ≤ 1) ne suffit
    pas à garantir la SDP : on refuse plutôt que de prétendre.
    """
    if len(R) != n or any(len(row) != n for row in R):
        raise ValueError("R n×n")
    for i in range(n):
        if abs(R[i][i] - 1.0) > 1e-9:
            raise ValueError("diag(R)=1")
        for j in range(n):
            if abs(R[i][j] - R[j][i]) > 1e-9:
                raise ValueError("R non symétrique")
            if abs(R[i][j]) > 1.0 + 1e-9:
                raise ValueError("|ρ|>1")
    if n > 2:
        raise ValueError("SDP hors n≤2 non vérifiée sans dépendance")
    if n == 2:
        det = R[0][0] * R[1][1] - R[0][1] * R[1][0]
        if det < -1e-12:
            raise ValueError("R non SDP (det<0)")


def u_c(lines: list[dict[str, Any]], R: list[list[float]] | None = None) -> float:
    uivec = [u_line(ln) * float(ln.get("c", 1.0)) for ln in lines]
    n = len(uivec)
    if not n:
        return 0.0
    if R is None:
        return math.sqrt(sum(u * u for u in uivec))
    _check_R_sdp(R, n)
    acc = 0.0
    for i in range(n):
        for j in range(n):
            acc += uivec[i] * R[i][j] * uivec[j]
    if acc < -1e-18:
        raise ValueError("u_c^2 < 0")
    return math.sqrt(max(acc, 0.0))


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
    R = gum.get("R")
    uc = u_c(lines, R) if lines else 0.0
    k = float(gum.get("k", 2.0))
    decide = str(gum.get("decide", "theta"))
    return {
        "verdict": verdict_gum(delta, theta, uc, k, decide),
        "uc": uc,
        "U": U(uc, k),
        "decide": decide,
        "k": k,
        "R": R,
    }
