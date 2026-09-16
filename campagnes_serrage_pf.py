#!/usr/bin/env python3
"""Campagne SERRAGE-PF — le corpus PRINCIPES sous balayage d'étalonnage.

Protocole : la machine apprend de ses propres verdicts. Chaque contact
PF est repesé sous une grille de θ d'étalonnage (la couleur du registre
n'est PAS modifiée — mesures dérivées, comme SERRAGE-1). Deux nombres
par contact : θ* = δ (frontière exacte S+↔P en régime θ) et le verdict
sous chaque θ de la grille. Les S+ fins (PF7, PF4, PF3, PF2) disent où
le vert se termine ; les S− larges disent où le rouge deviendrait
indifférent (θ = δ/2, frontière P↔S−).

Déterministe : relit le registre figé, aucun fetch.
"""

from __future__ import annotations

from typing import Any

from mvcg.metrics import _adc
from mvcg.registers import CONTACTS, run_contact
from mvcg.verdict_register import _thr_contact

PROTOCOL = "MVC-G-SERRAGE-PF-1.0"
THETA_GRID = [0.20, 0.10, 0.05, 0.02, 0.01, 0.005]


def population_pf() -> list[str]:
    """Les 9 contacts du corpus PRINCIPES (PF1–PF8 + PF1b), figés."""
    ids = []
    for c in CONTACTS:
        if c.id.startswith("PF") and (len(c.id) < 4 or c.id[2].isdigit()
                                      or c.id.startswith("PF1b")):
            ids.append(c.id)
    return sorted(ids)


def run_serrage_pf() -> dict[str, Any]:
    """Balayage θ du corpus PF — verdicts dérivés, couleur non modifiée."""
    resultats = []
    for cid in population_pf():
        c = next(x for x in CONTACTS if x.id == cid)
        row = run_contact(c)
        delta = float(row["delta"])
        gum = (row.get("extra") or {}).get("gum") or {}
        thr_home, calib = _thr_contact(float(c.theta), gum)
        verdict_home = row["verdict"]
        sweep = []
        for th in THETA_GRID:
            thr, _ = _thr_contact(th, gum)
            sweep.append({"theta": th, "verdict": _adc(delta, thr)})
        resultats.append({
            "id": cid,
            "delta": delta,
            "theta_home": float(c.theta),
            "verdict_home": verdict_home,
            "regime": calib,
            "theta_etoile": delta,        # frontière exacte S+↔P (régime θ)
            "theta_relachement": delta / 2.0,  # frontière P↔S−
            "marge": delta / float(c.theta),
            "sweep": sweep,
        })
    return {"protocol": PROTOCOL, "n": len(resultats),
            "theta_grid": THETA_GRID, "resultats": resultats,
            "warning": "mesures dérivées ; la couleur du registre n'est pas modifiée"}


if __name__ == "__main__":
    import json
    print(json.dumps(run_serrage_pf(), indent=2, ensure_ascii=False))
