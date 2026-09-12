#!/usr/bin/env python3
"""Contact ouvert CKM — l'unitarité de la première ligne.

Chronologie du gel :
1. Protocole écrit et gelé avant toute exécution : règle déclarée —
   la première ligne de la matrice CKM est unitaire de par la
   définition du modèle à trois générations : |Vud|²+|Vus|²+|Vub|² =
   1. mu_loc = somme déclarée de la table (extrait PDG déclaré, pas
   un fetch pdgLive), mu_ref = 1.0 (identité du modèle, jamais
   ajustée pour absorber l'écart). Seuil : decide=U, k=2 sur
   u = 0,0007 déclarée → U = 0,0014 ; le contact porte θ = 0,0007.
   Estimation pré-run honnête : δ = 0,0016 soit 2,3 sigma —
   U < δ ≤ 2U → P attendu au cheveu du S+ (δ/U = 1,14) : suspense
   réel. Levier : somme←autres entrées (Vus d'autres désintégrations),
   jamais θ ni l'identité.
2. Premier run : mot = P (δ = 0,0016, U = 0,0014). Découvert, pas
   choisi. Artefacts gelés offline (audits [HOLD]) :
   `examples/registre/CKM.*`.
3. Figé : mot dans ce test.
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from mvcg.gum import u_c, U as gum_U  # noqa: E402
from mvcg.registers import run_registers  # noqa: E402
from mvcg.tables import load_table  # noqa: E402


class TestOpenContactCKM(unittest.TestCase):
    def row(self) -> dict:
        by = {r["id"]: r for r in run_registers()["rows"]}
        return by["CKM_Row1_Unitarity"]

    def test_ckm_word_frozen(self) -> None:
        r = self.row()
        self.assertEqual(r["verdict"], "P")  # mot du premier run, figé
        self.assertEqual(r["statut"], "ouverte")
        self.assertIsNone(r["expected"])
        g = r["extra"]["gum"]
        self.assertGreater(r["delta"], g["U"])  # 0,0016 > 0,0014
        self.assertLess(r["delta"], 2.0 * g["U"])  # 0,0016 < 0,0028
        self.assertAlmostEqual(r["mu_loc"], 0.9984, places=12)

    def test_ckm_anti_tautology_identite_jamais_ajustee(self) -> None:
        # mu_ref = 1.0 est l'identité du modèle : le geste interdit
        # serait de déplacer mu_ref (ou de gonfler u) pour absorber
        # le déficit d'unitarité. Le test vérifie que la référence
        # est exactement 1 et que u est celle déclarée de la table.
        t = load_table("ckm_row1_LITERATURE.json")
        self.assertEqual(float(t["unitarity"]), 1.0)
        self.assertEqual(self.row()["mu_ref"], 1.0)
        self.assertAlmostEqual(float(t["sum"]), self.row()["mu_loc"],
                               places=12)
        self.assertAlmostEqual(float(t["u"]), 0.0007, places=12)
        g = self.row()["extra"]["gum"]
        # La ligne B portée (reconstruite localement, comme AMU)
        # recombine au seuil déclaré : u = 0,0007, U(k=2) = 0,0014.
        lines = [{"name": "sum_PDG", "type": "B", "u": 0.0007}]
        self.assertAlmostEqual(u_c(lines), 0.0007, places=12)
        self.assertAlmostEqual(g["U"], gum_U(0.0007, 2), places=12)
        self.assertAlmostEqual(g["uc"], 0.0007, places=12)

    def test_ckm_suspense_au_cheveu(self) -> None:
        # Le mot P est tenu d'un cheveu : δ/U = 1,14. Une réanalyse
        # qui déplacerait la somme de ~0,0003 changerait le mot — le
        # registre le dit, et c'est exactement ce que le levier
        # « somme←autres entrées » annonce.
        g = self.row()["extra"]["gum"]
        ratio = self.row()["delta"] / g["U"]
        self.assertGreater(ratio, 1.0)
        self.assertLess(ratio, 1.3)
        # Le seuil reste U(k=2) quelle que soit la theta colonne :
        self.assertEqual(g["decide"], "U")
        self.assertEqual(g["k"], 2.0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
