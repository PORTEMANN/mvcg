#!/usr/bin/env python3
"""Contact ouvert O6 — E_1s(H) par la grille raffinée (levier d'O1 activé).

Chronologie du gel :
1. Protocole écrit et gelé avant toute exécution : même table
   (codata2018_extract.json, R∞ CODATA-2018), même chaîne Ha→eV,
   MÊME θ = 1e-3 gelé qu'O1 — le seuil ne bouge jamais. Le levier
   grille←raffiner est activé : n = 1600 au lieu de 200, r_max = 25
   inchangé. L'erreur à n = 1600 n'était pas connue : seul son ordre
   (O(h²), h ÷ 8) était prédit.
2. Premier run : mot = S+ (δ ≈ 6,1e-5 << θ). Découvert, pas choisi.
3. Ce test fixe le mot, comme pour tout contact du registre.

Le levier grille<-raffiner est ici ACTIF : le contact entier est la
vérification que la direction déclarée à O1 tient son seuil.
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from mvcg.h2plus import HA_TO_EV  # noqa: E402
from mvcg.registers import _fd_h1s_ha, run_registers  # noqa: E402


class TestOpenContactO6(unittest.TestCase):
    def row(self) -> dict:
        by = {r["id"]: r for r in run_registers()["rows"]}
        return by["O6_Grille_H1s_Raffine"]

    def test_o6_word_frozen(self) -> None:
        r = self.row()
        self.assertEqual(r["verdict"], "S+")  # mot du premier run, figé
        self.assertEqual(r["statut"], "ouverte")
        self.assertIsNone(r["expected"])  # aucun mot attendu au gel
        self.assertLessEqual(r["delta"], r["theta"])  # 6,1e-5 ≤ 1e-3
        self.assertAlmostEqual(r["mu_loc"], -13.604863835526125, places=9)

    def test_o6_provenance_chain(self) -> None:
        r = self.row()
        self.assertAlmostEqual(r["extra"]["mu_raw"] * HA_TO_EV, r["mu_loc"], places=9)
        self.assertAlmostEqual(r["extra"]["chain"]["k"], HA_TO_EV, places=9)
        self.assertIsNone(r["chain_kill"])

    def test_o6_lever_refinement_holds(self) -> None:
        # Le levier est ACTIF : n=1600 tient le θ=1e-3 gelé quand
        # n=200 le manquait (même mu_ref, même θ, ordre 2 vérifié).
        r = self.row()
        d_coarse = abs(_fd_h1s_ha(200, 25.0) / -0.5 - 1.0)  # erreur rel.
        d_fine = abs(_fd_h1s_ha(1600, 25.0) / -0.5 - 1.0)
        self.assertGreater(d_coarse, r["theta"])  # O1 : S-
        self.assertLessEqual(d_fine, r["theta"])  # O6 : S+
        # ordre 2 : raffiner ×8 (h ÷ 8) divise l'erreur par ~64
        self.assertLess(d_fine, d_coarse / 50.0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
