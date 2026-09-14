#!/usr/bin/env python3
"""Export FAIR dérivé du registre — prototype local (principe 2, ligne directrice).

Chaque contact devient un JSON normalisé DÉRIVÉ du registre au moment de
l'exécution — jamais écrit à la main (épistémologie du casier : une carte
dérivée ne peut pas mentir par construction). Régénérer = mêmes octets :
aucun horodatage horloge, aucun état caché, les fichiers ne se font
jamais éditer — ils se régénèrent.

Principe 1 (pré-enregistrement externe) NON adopté : freeze_timestamp,
ots_proof et prereg_url sont null et le resteront tant qu'aucun
engagement externe vérifiable n'existe. L'export ne prétend pas à une
preuve que la machine ne possède pas.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from mvcg.casier import family_of
from mvcg.registers import CONTACTS, run_registers
from mvcg.tables import ROOT, TABLES, load_table

PROTOCOL = "MVC-G-FAIR-EXPORT-0.1"
BUILD = ROOT / "build" / "fair"


def _table_ref(name: str | None) -> dict[str, Any]:
    # Certains runners portent dans extra["table"] une étiquette de
    # vintage ("LITERATURE-2018"), pas un nom de fichier : on ne
    # prétend pas à une empreinte sans fichier réel.
    if not name:
        return {"name": None, "sha256": None}
    path = TABLES / name
    if not path.exists():
        return {"name": None, "sha256": None, "vintage_label": name}
    t = load_table(name)
    return {"name": name, "sha256": t["_sha256"]}


def contact_cards() -> list[dict[str, Any]]:
    """Une carte normalisée par contact, dérivée du registre."""
    by_id = {c.id: c for c in CONTACTS}
    cards = []
    for r in run_registers()["rows"]:
        c = by_id.get(r["id"])
        gum = r["extra"].get("gum") or {}
        cards.append(
            {
                "contact_id": r["id"],
                "family": family_of(r["id"]),
                "domain": getattr(c, "register", None),
                "statut": r["statut"],
                "s": r["s"],
                "mu_loc": r["mu_loc"],
                "mu_ref": r["mu_ref"],
                "theta": r["theta"],
                "delta": r["delta"],
                "delta_kind": getattr(c, "delta_kind", None),
                "verdict": r["verdict"],
                "packet": r["packet"],
                "dimension": r["dimension"],
                "lever": r["lever"],
                "table": _table_ref(r["extra"].get("table")),
                "runner_sha256": r["extra"].get("runner_sha256"),
                "gum": {
                    "decide": gum.get("decide"),
                    "k": gum.get("k"),
                    "uc": gum.get("uc"),
                    "U": gum.get("U"),
                },
                "freeze": {
                    "timestamp": None,
                    "ots_proof": None,
                    "prereg_url": None,
                    "note": (
                        "gel prouvé par les docs et les tests du dépôt ; "
                        "horodatage externe non branché (principe 1 non adopté)"
                    ),
                },
            }
        )
    return cards


def export_fair(out_dir: Path | None = None) -> dict[str, Any]:
    """Écrit build/fair/{index.json, contacts/*.json} ; retourne le résumé."""
    out = Path(out_dir) if out_dir is not None else BUILD
    cdir = out / "contacts"
    cdir.mkdir(parents=True, exist_ok=True)
    index = []
    for card in contact_cards():
        doc = {"protocol": PROTOCOL, **card}
        raw = (json.dumps(doc, indent=2, sort_keys=True) + "\n").encode("utf-8")
        name = f"{card['contact_id']}.json"
        (cdir / name).write_bytes(raw)
        index.append(
            {
                "contact_id": card["contact_id"],
                "verdict": card["verdict"],
                "file": f"contacts/{name}",
                "sha256": hashlib.sha256(raw).hexdigest(),
            }
        )
    idx_raw = (
        json.dumps(
            {
                "protocol": PROTOCOL,
                "warning": (
                    "export dérivé du registre ; jamais écrit à la main ; "
                    "régénération = mêmes octets ; principe 1 non adopté"
                ),
                "n": len(index),
                "contacts": index,
            },
            indent=2,
        )
        + "\n"
    ).encode("utf-8")
    (out / "index.json").write_bytes(idx_raw)
    return {
        "protocol": PROTOCOL,
        "n": len(index),
        "out": str(out),
        "index_sha256": hashlib.sha256(idx_raw).hexdigest(),
    }
