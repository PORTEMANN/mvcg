#!/usr/bin/env python3
"""Capot A — exécution d'un runner.

Contrat : fn() -> (μ, extra). extra hors δ.
La chaîne (capot B) est optionnelle et *après* le runner.
La tare reste dans le runner (sinon double zéro).
"""

from __future__ import annotations

from typing import Any, Callable

from mvcg.chain import apply_chain, compose

RunnerFn = Callable[[], tuple[float, dict[str, Any]]]


def execute(
    fn: RunnerFn,
    chain: list[dict[str, Any]] | None = None,
) -> tuple[float, dict[str, Any]]:
    mu, extra = fn()
    extra = dict(extra or {})
    extra["mu_raw"] = float(mu)
    if chain:
        out = compose(chain)
        extra["chain"] = out
        if out.get("kill"):
            extra["chain_kill"] = out["kill"]
            return float(mu), extra
        mu = apply_chain(float(mu), chain)
    extra["mu_loc"] = float(mu)
    return float(mu), extra
