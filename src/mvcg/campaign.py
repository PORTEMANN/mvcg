#!/usr/bin/env python3
"""Campagne : le noyau pose les engrenages sur les S candidates."""

from __future__ import annotations

from dataclasses import asdict
from pathlib import Path
from typing import Any

from mvcg.candidates import CATALOG, run_candidate
from mvcg.met_lib import MetLib15
from mvcg.metrics import _delta, _verdict, audit_metric


def rehearse_campaign(root: Path | None = None) -> dict[str, Any]:
    """Campagne locale : μ et mots, aucun gel, aucun OTS, aucun d."""
    rows = []
    for c in CATALOG:
        raw = run_candidate(c)
        delta = _delta(raw["mu_loc"], c.mu_ref, c.delta_kind)
        verdict = _verdict(delta, c.theta)
        d_map = {"S+": 0, "P": 1, "S-": 2}
        rows.append(
            {
                **raw,
                "verdict": verdict,
                "delta": delta,
                "d_reg": d_map.get(verdict, 2),
                "metric_kill": False,
                "committed": False,
            }
        )
    out = {
        "protocol": "MVC-G-REHEARSAL-0.1",
        "committed": False,
        "note": "répétition locale — hasher et publier seulement avec campaign --publish",
        "n": len(rows),
        "splus": sum(1 for r in rows if r["verdict"] == "S+"),
        "partial": sum(1 for r in rows if r["verdict"] == "P"),
        "sminus": sum(1 for r in rows if r["verdict"] == "S-"),
        "rows": rows,
    }
    if root is not None:
        Path(root).mkdir(parents=True, exist_ok=True)
        (Path(root) / "rehearsal.json").write_text(
            __import__("json").dumps(out, indent=2) + "\n", encoding="utf-8"
        )
    return out


def run_campaign(root: Path, offline_ots: bool = True, commit: bool = True) -> dict[str, Any]:
    if not commit:
        return rehearse_campaign(root)
    lib = MetLib15(Path(root), offline_ots=offline_ots)
    rows = []
    for c in CATALOG:
        raw = run_candidate(c)
        fid = c.id
        dossier = {
            "id": c.id,
            "s": getattr(c, "s_phrase", c.id),
            "packet": c.packet,
            "dimension": c.dimension,
            "theta": c.theta,
            "sigma": getattr(c, "sigma", None),
            "mu_ref": c.mu_ref,
            "lever": getattr(c, "lever", "—"),
            "delta_kind": c.delta_kind,
            "register": getattr(c, "domain", ""),
            "orig": c.orig,
        }
        lib.freeze(fid, phys=c.phys, orig=c.orig, kappa_hat="equilibre", dossier=dossier)
        lib.freeze_units(fid, {"packet": c.packet, "vintage": "campaign"})
        metric = lib.record_metric(
            fid, raw["mu_loc"], c.mu_ref, c.theta, c.dimension, c.delta_kind
        )
        d_map = {"S+": 0, "P": 1, "S-": 2}
        d = d_map.get(metric["verdict"], 2)
        lib.measure(fid, d)
        rows.append(
            {
                **raw,
                "verdict": metric["verdict"],
                "delta": metric["delta"],
                "d_reg": d,
                "metric_kill": audit_metric(metric)["kill"],
                "committed": True,
            }
        )
    out = {
        "protocol": "MVC-G-CAMPAIGN-0.1",
        "committed": True,
        "n": len(rows),
        "splus": sum(1 for r in rows if r["verdict"] == "S+"),
        "partial": sum(1 for r in rows if r["verdict"] == "P"),
        "sminus": sum(1 for r in rows if r["verdict"] == "S-"),
        "rows": rows,
    }
    Path(root).mkdir(parents=True, exist_ok=True)
    (Path(root) / "campaign.json").write_text(
        __import__("json").dumps(out, indent=2) + "\n", encoding="utf-8"
    )
    return out
