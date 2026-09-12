#!/usr/bin/env python3
"""Lecture de tables gelées. Pas de fetch réseau."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
TABLES = ROOT / "data" / "tables"


def load_table(name: str) -> dict[str, Any]:
    path = TABLES / name
    if not path.exists():
        raise FileNotFoundError(f"table absente: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def h2plus_de() -> dict[str, Any]:
    p = TABLES / "h2plus_De_LITERATURE-2018.json"
    return load_table(p.name if p.exists() else "h2plus_De_DEMO-2026.json")


def h2o_dipole() -> dict[str, Any]:
    p = TABLES / "h2o_dipole_LITERATURE-2018.json"
    return load_table(p.name if p.exists() else "h2o_dipole_DEMO-2026.json")


def kato_h() -> dict[str, Any]:
    return load_table("kato_cusp_H_DEMO-2026.json")


def he_corr() -> dict[str, Any]:
    return load_table("he_corr_LITERATURE-2018.json")
