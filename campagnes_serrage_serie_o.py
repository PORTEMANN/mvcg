#!/usr/bin/env python3
"""Campagne SERRAGE-1 (série O) — serrage d'étalonnage des S+ à θ=0,1.

Protocole gelé : docs/SERRAGE-PROTOCOLE.md. La couleur n'est pas modifiée ;
θ* et les étages de serrage sont des mesures dérivées, consignées ici.

Sortie : tableau (contact, δ, θ*, étages, verdict de bascule) + trace
complète par contact. Déterministe : relit le registre figé, ne touche
à rien d'autre.
"""

from __future__ import annotations

import math
from typing import Any

from mvcg.metrics import _adc
from mvcg.registers import CONTACTS, run_contact
from mvcg.verdict_register import _thr_contact

PROTOCOL = "MVC-G-SERRAGE-1.0"
MAX_ETAGES = 60


def serrer_contact(contact_id: str) -> dict[str, Any]:
    """Échelle de serrage thr/2^k jusqu'au premier verdict ≠ S+.

    Trace complète conservée (seuil, verdict) — jamais tronquée.
    """
    c = next((x for x in CONTACTS if x.id == contact_id), None)
    if c is None:
        raise KeyError(contact_id)
    row = run_contact(c)
    gum = (row.get("extra") or {}).get("gum") or {}
    thr_home, calib = _thr_contact(float(c.theta), gum)
    delta = float(row["delta"])

    trace = []
    verdict_bascule = "S+"
    thr_bascule = None
    for k in range(MAX_ETAGES + 1):
        thr = thr_home / (2.0**k)
        v = _adc(delta, thr)
        trace.append({"k": k, "thr": thr, "verdict": v})
        if v != "S+":
            verdict_bascule = v
            thr_bascule = thr
            break

    etages = math.floor(math.log2(thr_home / delta)) if delta > 0 else MAX_ETAGES
    return {
        "protocol": PROTOCOL,
        "id": contact_id,
        "regime": calib,
        "delta": delta,
        "theta_home": float(c.theta),
        "thr_home": thr_home,
        "theta_etoile": delta,  # frontière exacte S+→P (monotonie de _adc)
        "etages": int(etages),
        "verdict_bascule": verdict_bascule,
        "thr_bascule": thr_bascule,
        "trace": trace,
        "warning": "mesure dérivée ; la couleur du registre n'est pas modifiée",
    }


def population_serie_o() -> list[str]:
    """S+ à θ=0,1 sans budget GUM (protocole gelé, population figée)."""
    ids = []
    for c in CONTACTS:
        if abs(float(c.theta) - 0.1) > 1e-12:
            continue
        row = run_contact(c)
        gum = (row.get("extra") or {}).get("gum") or {}
        if gum.get("uc"):
            continue
        if row["verdict"] == "S+":
            ids.append(c.id)
    return sorted(ids)


def run_serrage_serie_o() -> dict[str, Any]:
    pop = population_serie_o()
    resultats = [serrer_contact(i) for i in pop]
    return {
        "protocol": PROTOCOL,
        "population": pop,
        "n": len(resultats),
        "resultats": resultats,
        "warning": "pas de moyenne entre contacts ; chaque θ* est lu seul",
    }


if __name__ == "__main__":
    import json

    out = run_serrage_serie_o()
    print(json.dumps(out, indent=2, ensure_ascii=False))
