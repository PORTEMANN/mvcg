#!/usr/bin/env python3
"""Registre des verdicts — index par fibre.

Mode d'emploi : filtrer (packet, dimension), compter.
Interdit : η_S+ comme μ, export d'un mot vers une autre fibre.
"""

from __future__ import annotations

from collections import defaultdict
from typing import Any

from mvcg.dictionaries import sweep_contact
from mvcg.registers import CONTACTS, run_contact, run_registers

COLORS = {"hl": "hl", "gauss": "gauss", "si": "si", "1": "1"}


def fiber_key(row: dict[str, Any]) -> tuple[str, str]:
    return (str(row.get("packet") or ""), str(row.get("dimension") or ""))


def index_verdicts(
    rows: list[dict[str, Any]] | None = None,
    packet: str | None = None,
    dimension: str | None = None,
) -> dict[str, Any]:
    if rows is None:
        rows = run_registers()["rows"]
    selected = []
    for r in rows:
        if packet is not None and r.get("packet") != packet:
            continue
        if dimension is not None and r.get("dimension") != dimension:
            continue
        selected.append(r)
    by: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for r in selected:
        by[fiber_key(r)].append(r)

    fibres = []
    for (pkt, dim), rs in sorted(by.items()):
        c = {"S+": 0, "P": 0, "S-": 0}
        for r in rs:
            v = r.get("verdict")
            if v in c:
                c[v] += 1
        fibres.append(
            {
                "packet": pkt,
                "dimension": dim,
                "color": COLORS.get(pkt, pkt),
                "n": len(rs),
                "counts": c,
                "ids": [r["id"] for r in rs],
                "mots": {r["id"]: r["verdict"] for r in rs},
            }
        )
    return {
        "protocol": "MVC-G-VERDICT-REG-0.1",
        "warning": "comptage par fibre ; un S+ n'est pas une entrée d'une autre fibre",
        "filter": {"packet": packet, "dimension": dimension},
        "n": len(selected),
        "fibres": fibres,
    }


def mode_unites(packet: str, dimension: str | None = None) -> dict[str, Any]:
    """Mode d'utilisation : un dictionnaire U à la fois."""
    return index_verdicts(packet=packet, dimension=dimension)


def lcao_unit_street() -> dict[str, Any]:
    """P20 Lowe : même De, trois fibres d'affichage. Table convertie par k gelé."""
    from mvcg.h2plus import EV_TO_CM1, HA_TO_EV, lcao_1s
    from mvcg.metrics import _delta, _verdict
    from mvcg.tables import h2plus_de

    sol = lcao_1s(2.0)
    t = h2plus_de()
    ref_ev = float(t["value"])
    theta = 0.05
    plates = [
        ("Ha", sol["De_Ha"], ref_ev / HA_TO_EV, "si"),
        ("eV", sol["De_eV"], ref_ev, "si"),
        ("cm-1", sol["De_cm-1"], ref_ev * EV_TO_CM1, "si"),
    ]
    rows = []
    for dim, mu, ref, pkt in plates:
        dlt = _delta(mu, ref, "rel")
        rows.append(
            {
                "id": "P20_H2plus_LCAO",
                "packet": pkt,
                "dimension": dim,
                "color": dim,
                "mu_loc": mu,
                "mu_ref": ref,
                "delta": dlt,
                "theta": theta,
                "verdict": _verdict(dlt, theta),
            }
        )
    mots = {r["dimension"]: r["verdict"] for r in rows}
    return {
        "protocol": "MVC-G-STREET-LCAO-0.1",
        "s": "De(H2+) Lowe vs table, fibre d'affichage variable",
        "k_Ha_eV": HA_TO_EV,
        "k_eV_cm-1": EV_TO_CM1,
        "table_sha": t.get("_sha256"),
        "warning": "trois couleurs ; un seul ansatz ; ne pas moyenner",
        "rows": rows,
        "mots": mots,
    }


def street_sweep(contact_id: str) -> dict[str, Any]:
    """Même rue (id, μ) sous chaque paquet. Un mot par couleur, pas de fusion."""
    c = next((x for x in CONTACTS if x.id == contact_id), None)
    if c is None:
        raise KeyError(contact_id)
    row = run_contact(c)
    swept = sweep_contact(
        float(row["mu_loc"]),
        float(row["mu_ref"]),
        str(c.dimension),
        float(c.theta),
        c.delta_kind,
    )
    for r in swept["rows"]:
        r["color"] = COLORS.get(r["packet"], r["packet"])
        r["id"] = contact_id
    return {
        "protocol": "MVC-G-STREET-0.1",
        "id": contact_id,
        "s": c.s_phrase,
        "dimension": c.dimension,
        "mu_loc": row["mu_loc"],
        "mu_ref": row["mu_ref"],
        "home_packet": c.packet,
        "home_verdict": row["verdict"],
        "warning": "comparer les lignes ; ne pas moyenner les mots",
        "rows": swept["rows"],
    }
