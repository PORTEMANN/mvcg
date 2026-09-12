#!/usr/bin/env python3
"""Manifeste D scientifique — entre dans le hash G1."""

from __future__ import annotations

import json
from typing import Any

REQUIRED = ("id", "s", "packet", "dimension", "theta", "mu_ref", "lever", "delta_kind")


def canonical_d(doc: dict[str, Any]) -> dict[str, Any]:
    missing = [k for k in REQUIRED if k not in doc]
    if missing:
        raise ValueError(f"D incomplet: {missing}")
    return {
        "id": str(doc["id"]),
        "s": str(doc["s"]),
        "packet": str(doc["packet"]),
        "dimension": str(doc["dimension"]),
        "theta": float(doc["theta"]),
        "sigma": None if doc.get("sigma") is None else float(doc["sigma"]),
        "mu_ref": float(doc["mu_ref"]),
        "lever": str(doc["lever"]),
        "delta_kind": str(doc["delta_kind"]),
        "register": str(doc.get("register", "")),
        "orig": str(doc.get("orig", "")),
        "table": doc.get("table"),
        "chain": doc.get("chain"),
        "gum": doc.get("gum"),
        "tare": doc.get("tare"),
        "caliber": doc.get("caliber"),
    }
