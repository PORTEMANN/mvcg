#!/usr/bin/env python3
"""Campagne SERRAGE-2 (détente) — serrage ascendant des P à θ=0,1.

Protocole gelé : docs/SERRAGE-PROTOCOLE.md (section Campagne 2, ajoutée
2026-09-14 après le feu vert). Symétrique de la campagne 1 : au lieu de
diviser le seuil par 2 jusqu'à casser le S+, on le multiplie par 2
jusqu'à remonter le P en S+. Mesures consignées : k* de détente et
position dans la bande `pos = log2(δ/θ_home)` — c'est elle qui discrime,
car tous les P de la population basculent au premier palier.

La couleur du registre n'est pas modifiée : mesures dérivées uniquement.
"""

from __future__ import annotations

import math
from typing import Any

from mvcg.metrics import _adc
from mvcg.registers import CONTACTS, run_contact
from mvcg.verdict_register import _thr_contact

PROTOCOL = "MVC-G-SERRAGE-2.0"
MAX_ETAGES = 60


def detendre_contact(contact_id: str) -> dict[str, Any]:
    """Échelle de détente thr*2^k jusqu'au premier verdict S+.

    Trace complète conservée (seuil, verdict) — jamais tronquée.
    """
    c = next((x for x in CONTACTS if x.id == contact_id), None)
    if c is None:
        raise KeyError(contact_id)
    row = run_contact(c)
    gum = (row.get("extra") or {}).get("gum") or {}
    thr_home, calib = _thr_contact(float(c.theta), gum)
    delta = float(row["delta"])
    if row["verdict"] != "P":
        raise ValueError(f"{contact_id} n'est pas un P (serrage/détente)")

    trace = []
    k_bascule = None
    for k in range(MAX_ETAGES + 1):
        thr = thr_home * (2.0**k)
        v = _adc(delta, thr)
        trace.append({"k": k, "thr": thr, "verdict": v})
        if v == "S+":
            k_bascule = k
            break

    return {
        "protocol": PROTOCOL,
        "id": contact_id,
        "regime": calib,
        "delta": delta,
        "theta_home": float(c.theta),
        "thr_home": thr_home,
        "pos_bande": math.log2(delta / thr_home),  # 0 = frontière S+, 1 = S-
        "etages_detente": k_bascule,
        "trace": trace,
        "warning": "mesure dérivée ; la couleur du registre n'est pas modifiée",
    }


def population_p_sans_gum() -> list[str]:
    """P à θ=0,1 sans budget GUM (protocole gelé, population figée)."""
    ids = []
    for c in CONTACTS:
        if abs(float(c.theta) - 0.1) > 1e-12:
            continue
        row = run_contact(c)
        gum = (row.get("extra") or {}).get("gum") or {}
        if gum.get("uc"):
            continue
        if row["verdict"] == "P":
            ids.append(c.id)
    return sorted(ids)


def run_detente_serie_o() -> dict[str, Any]:
    pop = population_p_sans_gum()
    resultats = [detendre_contact(i) for i in pop]
    return {
        "protocol": PROTOCOL,
        "population": pop,
        "n": len(resultats),
        "resultats": resultats,
        "warning": "pas de moyenne entre contacts ; chaque position est lue seule",
    }


if __name__ == "__main__":
    import json

    out = run_detente_serie_o()
    print(json.dumps(out, indent=2, ensure_ascii=False))
