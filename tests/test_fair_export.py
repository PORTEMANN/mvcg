#!/usr/bin/env python3
"""Prototype export FAIR — un export dérivé ne ment pas, ne vieillit pas.

Propriétés figées :
- dérivé : les cartes coïncident avec le registre (id, μ, θ, mot) ;
- déterministe : régénérer = mêmes octets (aucun horodatage horloge) ;
- honnête sur le principe 1 : freeze/ots/prereg null tant qu'aucun
  engagement externe n'existe — l'export ne prétend pas à une preuve
  absente ;
- interopérable : chaque fichier est du JSON valide, contact_id = nom
  du fichier, empreinte de table = empreinte réelle du fichier gelé.
"""

from __future__ import annotations

import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from mvcg.fair_export import PROTOCOL, contact_cards, export_fair  # noqa: E402
from mvcg.registers import run_registers  # noqa: E402
from mvcg.tables import load_table  # noqa: E402


def _tree(d: Path) -> dict[str, bytes]:
    return {str(p.relative_to(d)): p.read_bytes() for p in sorted(d.rglob("*")) if p.is_file()}


class TestFairExport(unittest.TestCase):
    def test_derived_from_register(self) -> None:
        rows = {r["id"]: r for r in run_registers()["rows"]}
        cards = contact_cards()
        self.assertEqual(len(cards), len(rows))
        for c in cards:
            r = rows[c["contact_id"]]
            self.assertEqual(c["mu_loc"], r["mu_loc"])
            self.assertEqual(c["mu_ref"], r["mu_ref"])
            self.assertEqual(c["theta"], r["theta"])
            self.assertEqual(c["delta"], r["delta"])
            self.assertEqual(c["verdict"], r["verdict"])

    def test_regeneration_same_bytes(self) -> None:
        # Régénérer = mêmes octets : un export dérivé ne vieillit pas
        # et ne peut pas être « édité à la main » sans se faire
        # écraser par la prochaine régénération.
        with tempfile.TemporaryDirectory() as a, tempfile.TemporaryDirectory() as b:
            export_fair(Path(a))
            export_fair(Path(b))
            self.assertEqual(_tree(Path(a)), _tree(Path(b)))

    def test_principle1_not_claimed(self) -> None:
        # Principe 1 non adopté : pas d'horodatage externe prétendu.
        for c in contact_cards():
            f = c["freeze"]
            self.assertIsNone(f["timestamp"])
            self.assertIsNone(f["ots_proof"])
            self.assertIsNone(f["prereg_url"])
            self.assertIn("non branché", f["note"])

    def test_interoperable_and_honest_hash(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp)
            summary = export_fair(out)
            idx = json.loads((out / "index.json").read_text(encoding="utf-8"))
            self.assertEqual(idx["protocol"], PROTOCOL)
            self.assertEqual(idx["n"], summary["n"])
            for entry in idx["contacts"]:
                doc = json.loads((out / entry["file"]).read_text(encoding="utf-8"))
                self.assertEqual(doc["contact_id"], Path(entry["file"]).stem)
                self.assertEqual(
                    hashlib.sha256((out / entry["file"]).read_bytes()).hexdigest(),
                    entry["sha256"],
                )
                if doc["table"]["name"] is not None:
                    t = load_table(doc["table"]["name"])
                    self.assertEqual(doc["table"]["sha256"], t["_sha256"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
