#!/usr/bin/env python3
"""Contacts ouverts NMR — la loi de Karplus pesée sur deux conformations.

Chronologie du gel (commune aux deux cartes) :
1. Protocole écrit et gelé avant toute exécution : règle déclarée —
   ³J(φ) = A cos²(φ−60°) + B cos(φ−60°) + C, coefficients gelés de la
   table (Vuister-Bax déclarés, jamais ajustés sur les références) ;
   φ_helix = −60°, φ_sheet = −120° de la table. Les références
   J_typical (4,0 / 8,5 Hz) sont des ORDRES DE GRANDEUR déclarés
   (« pas un PDB ») — c'est la dette attendue. θ = 0,10 rel gelé
   avant run. Estimations pré-run honnêtes : hélice ~2,7 % (S+
   attendu) ; brin ~16 % (zone P, suspense réel au bord S− à 20 %).
2. Premiers runs : hélice = S+ (δ = 2,69 %) ; brin = P (δ = 16,12 %).
   Découverts, pas choisis. Artefacts gelés offline (audits [HOLD]) :
   `examples/registre/KARPLUS_{H,S}.*`.
3. Figés : mots dans ce test.
"""

from __future__ import annotations

import math
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from mvcg.karplus import j_hn_ha, peptide_doc  # noqa: E402
from mvcg.registers import run_registers  # noqa: E402


def _j(phi_deg: float, a: float, b: float, c: float, off: float) -> float:
    theta = math.radians(phi_deg - off)
    return a * math.cos(theta) ** 2 + b * math.cos(theta) + c


class TestOpenContactNMR(unittest.TestCase):
    def row(self, cid: str) -> dict:
        by = {r["id"]: r for r in run_registers()["rows"]}
        return by[cid]

    def test_nmr_words_frozen(self) -> None:
        h = self.row("NMR_Karplus_Helix")
        s = self.row("NMR_Karplus_Sheet")
        self.assertEqual(h["verdict"], "S+")  # mot du premier run, figé
        self.assertEqual(s["verdict"], "P")
        self.assertAlmostEqual(h["mu_loc"], 4.107499999999998, places=9)
        self.assertAlmostEqual(s["mu_loc"], 9.87, places=9)
        self.assertLess(h["delta"], h["theta"])
        self.assertGreater(s["delta"], s["theta"])  # 16,1 % > 10 %
        self.assertLess(s["delta"], 2.0 * s["theta"])  # 16,1 % < 20 %

    def test_nmr_law_is_a_map(self) -> None:
        # Même loi, deux conformations : la paire fait ce qu'O4/O14 a
        # fait pour Tuinstra-Koenig — une carte avec un domaine de
        # validité. Le hélice tient dans sa référence grossière, le
        # brin ne tient pas : la loi n'est pas universelle, elle est
        # locale dans le plan des conformations.
        t = peptide_doc()
        a, b, c, off = (float(t[k]) for k in ("A", "B", "C", "offset_deg"))
        self.assertAlmostEqual(
            _j(float(t["phi_helix_deg"]), a, b, c, off),
            self.row("NMR_Karplus_Helix")["mu_loc"], places=12)
        self.assertAlmostEqual(
            _j(float(t["phi_sheet_deg"]), a, b, c, off),
            self.row("NMR_Karplus_Sheet")["mu_loc"], places=12)
        # Mêmes coefficients sur les deux cartes (une seule loi) :
        self.assertEqual(self.row("NMR_Karplus_Helix")["extra"]["A"],
                         self.row("NMR_Karplus_Sheet")["extra"]["A"])

    def test_nmr_anti_tautology_pas_d_ajustement(self) -> None:
        # Les coefficients gelés sont ceux de la table ; le geste
        # interdit serait de recalibrer A, B, C pour coller aux
        # références typiques. Le test vérifie que les coefficients
        # utilisés sont les coefficients déclarés — pas un fit.
        t = peptide_doc()
        h = self.row("NMR_Karplus_Helix")
        self.assertAlmostEqual(h["extra"]["A"], float(t["A"]), places=12)
        self.assertAlmostEqual(h["extra"]["B"], float(t["B"]), places=12)
        self.assertAlmostEqual(h["extra"]["C"], float(t["C"]), places=12)
        # Et la fonction publique donne le même nombre que le runner :
        self.assertAlmostEqual(j_hn_ha(float(t["phi_helix_deg"])),
                               h["mu_loc"], places=12)


if __name__ == "__main__":
    unittest.main(verbosity=2)
