#!/usr/bin/env python3
"""Loi de Karplus ³J(HN,Hα) — coefficients gelés."""

from __future__ import annotations

import math
from typing import Any

from mvcg.tables import load_table


def peptide_doc() -> dict[str, Any]:
    return load_table("karplus_peptide_LITERATURE.json")


def peptide_vogelibax2007_doc() -> dict[str, Any]:
    """Seconde voie de la campagne croisée : mêmes phi, mêmes références,
    coefficients Vogeli-Bax 2007 déclarés (gel 2026-09-14, voir
    docs/NMR-KARPLUS-VOGELIBAX-CONTACT-OUVERT.md)."""
    return load_table("karplus_peptide_VOGELIBAX2007.json")


def j_hn_ha(phi_deg: float, doc: dict[str, Any] | None = None) -> float:
    t = doc or peptide_doc()
    theta = math.radians(float(phi_deg) - float(t["offset_deg"]))
    return float(t["A"]) * math.cos(theta) ** 2 + float(t["B"]) * math.cos(theta) + float(t["C"])
