#!/usr/bin/env python3
"""Archive append-only des traces de contact.

Une ligne = un run, pas un apprentissage.
N'entre dans G1 que si vous la passez à freeze vous-même.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from mvcg.met_lib import sha256_file, sha256_obj


def source_sha(fn) -> str:
    import inspect

    return sha256_file(Path(inspect.getfile(fn)))


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def trace_from_row(row: dict[str, Any]) -> dict[str, Any]:
    body = {
        "id": row.get("id"),
        "register": row.get("register"),
        "verdict": row.get("verdict"),
        "delta": row.get("delta"),
        "theta": row.get("theta"),
        "mu_loc": row.get("mu_loc"),
        "mu_ref": row.get("mu_ref"),
        "dimension": row.get("dimension"),
        "packet": row.get("packet"),
        "statut": row.get("statut"),
        "expected": row.get("expected"),
        "campaign": row.get("campaign"),
        "table_sha": (row.get("extra") or {}).get("sha"),
        "runner_sha256": (row.get("extra") or {}).get("runner_sha256"),
    }
    return {
        "at": _now(),
        "trace_sha256": sha256_obj(body),
        **body,
    }


def append_traces(rows: list[dict[str, Any]], path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as fh:
        for row in rows:
            fh.write(json.dumps(trace_from_row(row), ensure_ascii=True) + "\n")
    return path


def read_traces(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    out = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            out.append(json.loads(line))
    return out
