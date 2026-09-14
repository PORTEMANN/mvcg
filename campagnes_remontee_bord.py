#!/usr/bin/env python3
"""Campagne SERRAGE-3 (remontée) — les S− de bord de bande, δ/thr ∈ [2,4).

Protocole gelé : docs/SERRAGE-PROTOCOLE.md (section Campagne 3 + correction
de direction, ajoutées 2026-09-14). Dernière arête non cartographiée :
un S− proche de la bande peut être un rouge franc ou un quasi-P. On
DÉTEND le seuil (thr×2^k) jusqu'à la remontée en P — la position du rouge
se lit en octaves au-dessus de la frontière.

Correction conservée en trace : la première version de cette campagne
serrait le seuil VERS LE BAS ; un S− ne peut jamais remonter ainsi
(monotonie de `_adc`). La direction correcte est la détente.

Population : contacts NUS (sans budget GUM, règle des campagnes 1-2),
verdict S−, 2 ≤ δ/thr_home < 4 — sur tout le registre, toute θ.
La couleur du registre n'est pas modifiée : mesures dérivées uniquement.
"""

from __future__ import annotations

import math
from typing import Any

from mvcg.metrics import _adc
from mvcg.registers import CONTACTS, run_contact
from mvcg.verdict_register import _thr_contact

PROTOCOL = "MVC-G-SERRAGE-3.1"  # 3.0 = direction erronée, conservée en trace
MAX_ETAGES = 60


def remonter_contact(contact_id: str) -> dict[str, Any]:
    """Échelle de détente thr*2^k jusqu'au premier verdict ≠ S−.

    Trace complète conservée (seuil, verdict) — jamais tronquée.
    """
    c = next((x for x in CONTACTS if x.id == contact_id), None)
    if c is None:
        raise KeyError(contact_id)
    row = run_contact(c)
    gum = (row.get("extra") or {}).get("gum") or {}
    thr_home, calib = _thr_contact(float(c.theta), gum)
    delta = float(row["delta"])
    if row["verdict"] != "S-":
        raise ValueError(f"{contact_id} n'est pas un S- (remontée)")

    trace = []
    verdict_remontee = "S-"
    for k in range(MAX_ETAGES + 1):
        thr = thr_home * (2.0**k)
        v = _adc(delta, thr)
        trace.append({"k": k, "thr": thr, "verdict": v})
        if v != "S-":
            verdict_remontee = v
            break

    # frontière exacte S- -> P : thr = delta / 2 (monotonie de _adc).
    # pos_rouge = log2(delta / (2 thr_home)) in [0, 1) sur la fenêtre :
    # 0 = collé au P, 1 = bord haut (delta = 4 thr_home).
    return {
        "protocol": PROTOCOL,
        "id": contact_id,
        "regime": calib,
        "delta": delta,
        "theta_home": float(c.theta),
        "thr_home": thr_home,
        "frontiere_remontee": delta / 2.0,  # seuil exact de remontée en P
        "pos_rouge": math.log2(delta / (2.0 * thr_home)),
        "etages_remontee": trace[-1]["k"],
        "verdict_remontee": verdict_remontee,
        "trace": trace,
        "warning": "mesure dérivée ; la couleur du registre n'est pas modifiée",
    }


def population_s_moins_bord() -> list[str]:
    """S− nus avec 2 ≤ δ/thr_home < 4 (protocole gelé, population figée)."""
    ids = []
    for c in CONTACTS:
        row = run_contact(c)
        gum = (row.get("extra") or {}).get("gum") or {}
        if gum.get("uc"):
            continue
        thr, _ = _thr_contact(float(c.theta), gum)
        d = float(row["delta"])
        if row["verdict"] == "S-" and thr > 0 and 2.0 <= d / thr < 4.0:
            ids.append(c.id)
    return sorted(ids)


def run_remontee_bord() -> dict[str, Any]:
    pop = population_s_moins_bord()
    resultats = [remonter_contact(i) for i in pop]
    return {
        "protocol": PROTOCOL,
        "population": pop,
        "n": len(resultats),
        "resultats": resultats,
        "warning": "pas de moyenne entre contacts ; chaque position est lue seule",
    }


if __name__ == "__main__":
    import json

    out = run_remontee_bord()
    print(json.dumps(out, indent=2, ensure_ascii=False))
