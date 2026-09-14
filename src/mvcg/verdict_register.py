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


def _thr_contact(theta: float, gum: dict[str, Any] | None) -> tuple[float, str]:
    """Seuil de décision réel du contact : U si decide=U, θ sinon.

    Même règle que la couche épaisseur des cartes (carte.py) — une
    seule définition d'étalonnage partout où on la rejoue.
    """
    g = gum or {}
    if g.get("decide") == "U" and g.get("U"):
        return float(g["U"]), "U"
    return float(theta), "theta"


def street_sweep_calibrated(contact_id: str) -> dict[str, Any]:
    """Même rue, MÊME ÉTALONNAGE : le balayage re-décide au seuil gelé
    du contact (U si decide=U, θ sinon).

    Chantier A2 (2026-09-14) : la « divergence home/balayage » de CKM,
    HVP et HLbL n'était pas un effet d'unités mais la comparaison de
    deux seuils (street_sweep historique juge au θ seul — gel figé par
    les tests « deux instruments »). Ici les quatre paquets sont jugés
    au seuil du contact : l'invariance d'unités seule est mesurée.
    Les deux balayages sont complémentaires, pas concurrents :
    street_sweep compare les étalonnages, celui-ci compare les unités.
    """
    c = next((x for x in CONTACTS if x.id == contact_id), None)
    if c is None:
        raise KeyError(contact_id)
    row = run_contact(c)
    thr, calib = _thr_contact(float(c.theta), (row.get("extra") or {}).get("gum"))
    swept = sweep_contact(
        float(row["mu_loc"]),
        float(row["mu_ref"]),
        str(c.dimension),
        float(c.theta),
        c.delta_kind,
        thr=thr,
    )
    for r in swept["rows"]:
        r["color"] = COLORS.get(r["packet"], r["packet"])
        r["id"] = contact_id
    return {
        "protocol": "MVC-G-STREET-CAL-0.1",
        "id": contact_id,
        "s": c.s_phrase,
        "dimension": c.dimension,
        "mu_loc": row["mu_loc"],
        "mu_ref": row["mu_ref"],
        "home_packet": c.packet,
        "home_verdict": row["verdict"],
        "calibration": calib,
        "thr": thr,
        "warning": "à même étalonnage ; un mot par couleur ; ne pas moyenner",
        "rows": swept["rows"],
    }
