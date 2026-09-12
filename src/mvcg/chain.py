#!/usr/bin/env python3
"""Chaîne de ponts 1-cellules + 2-cellule egal."""

from __future__ import annotations

from typing import Any


def compose(steps: list[dict[str, Any]]) -> dict[str, Any]:
    if not steps:
        return {"k": 1.0, "tau": None, "src": None, "dst": None, "kill": None}
    tau = steps[0].get("tau")
    src = steps[0].get("src")
    k = 1.0
    prev_dst = src
    for i, st in enumerate(steps):
        if st.get("tau") != tau:
            return {"k": None, "kill": f"tau rupture à l'étape {i}"}
        if st.get("src") != prev_dst:
            return {"k": None, "kill": f"src≠dst précédent à l'étape {i}"}
        k *= float(st["k"])
        prev_dst = st.get("dst")
    return {"k": k, "tau": tau, "src": src, "dst": prev_dst, "kill": None}


def egal(path_g: list[dict[str, Any]], path_d: list[dict[str, Any]], declared: bool) -> dict[str, Any]:
    g, d = compose(path_g), compose(path_d)
    if g["kill"] or d["kill"]:
        return {"egal": False, "kill": g["kill"] or d["kill"], "k_g": g["k"], "k_d": d["k"]}
    same_ends = g["src"] == d["src"] and g["dst"] == d["dst"] and g["tau"] == d["tau"]
    if not same_ends:
        return {
            "egal": False,
            "kill": "chemins non parallèles (src/dst/tau)",
            "k_g": g["k"],
            "k_d": d["k"],
        }
    close = g["k"] is not None and d["k"] is not None and abs(g["k"] - d["k"]) <= 1e-12 * max(1.0, abs(g["k"]))
    if declared and not close:
        return {"egal": False, "kill": "egal:true mais k_g ≠ k_d", "k_g": g["k"], "k_d": d["k"]}
    if (not declared) and close:
        return {"egal": True, "kill": None, "k_g": g["k"], "k_d": d["k"], "note": "nombres égaux, declaration false"}
    return {"egal": bool(declared and close), "kill": None, "k_g": g["k"], "k_d": d["k"]}


def apply_chain(x: float, steps: list[dict[str, Any]]) -> float:
    out = compose(steps)
    if out["kill"] or out["k"] is None:
        raise ValueError(out["kill"])
    return float(x) * float(out["k"])
