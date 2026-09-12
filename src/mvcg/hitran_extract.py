#!/usr/bin/env python3
"""Extrait HITRAN déclaré. Pas de fetch hitran.org."""

from __future__ import annotations

from typing import Any

from mvcg.tables import load_table


def co2_hitran() -> dict[str, Any]:
    return load_table("co2_hitran_EXTRACT.json")


def line_nu(tag: str) -> tuple[float, dict[str, Any]]:
    doc = co2_hitran()
    for ln in doc["lines"]:
        if ln["tag"] == tag:
            return float(ln["nu_cm-1"]), {
                "table": doc["vintage"],
                "sha": doc.get("_sha256"),
                "medium": doc["medium"],
                "tag": tag,
            }
    raise KeyError(tag)
