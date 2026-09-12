#!/usr/bin/env python3
"""Loi de Karplus ³J(HN,Hα) — coefficients gelés."""

from __future__ import annotations

import math
from typing import Any

from mvcg.tables import load_table


def peptide_doc() -> dict[str, Any]:
    return load_table("karplus_peptide_LITERATURE.json")


def j_hn_ha(phi_deg: float, doc: dict[str, Any] | None = None) -> float:
    t = doc or peptide_doc()
    theta = math.radians(float(phi_deg) - float(t["offset_deg"]))
    return float(t["A"]) * math.cos(theta) ** 2 + float(t["B"]) * math.cos(theta) + float(t["C"])
