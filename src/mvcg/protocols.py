#!/usr/bin/env python3
"""Import d'un protocole JSON gelé (lecture seule, pas le corpus GitHub)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from mvcg.dossier import canonical_d

ROOT = Path(__file__).resolve().parents[2]
PROTO = ROOT / "data" / "protocols"

REQUIRED = ("id", "s", "packet", "dimension", "theta", "delta_kind", "lever", "campaign")


def load_protocol(name: str) -> dict[str, Any]:
    path = PROTO / name
    if not path.exists():
        raise FileNotFoundError(path)
    doc = json.loads(path.read_text(encoding="utf-8"))
    miss = [k for k in REQUIRED if k not in doc]
    if miss:
        raise ValueError(f"protocole incomplet: {miss}")
    return doc


def protocol_to_d(doc: dict[str, Any], mu_ref: float) -> dict[str, Any]:
    return canonical_d(
        {
            "id": doc["id"],
            "s": doc["s"],
            "packet": doc["packet"],
            "dimension": doc["dimension"],
            "theta": doc["theta"],
            "sigma": doc.get("sigma"),
            "mu_ref": mu_ref,
            "lever": doc["lever"],
            "delta_kind": doc["delta_kind"],
            "register": doc.get("register", "micro"),
            "orig": doc.get("orig", "pred"),
            "table": doc.get("table"),
        }
    )
