#!/usr/bin/env python3
"""Contact ouvert hyperfluidité — le QGP sature-t-il le plancher KSS ?

Chronologie du gel :
1. Protocole écrit avant toute exécution : premier contact du tiroir
   dont le mot tranche une question ouverte — la saturation de la borne
   KSS par le plasma quarks-gluons, fluide déclaré le plus proche du
   plancher. Fabrication : la borne INFÉRIEURE de l'extraction la plus
   citée (η/s ≈ (2-3) unités KSS, Luzum & Romatschke, repris dans
   arXiv:1108.0734), la déclaration la plus favorable au suspense ;
   référence : le plancher (1). Dette assumée : les extractions ne
   coïncident pas, la fourchette large (0,6-2,5 planchers) chevauche
   le plancher ; un mot S− dira « non-saturation établie pour la
   déclaration choisie », jamais « KSS violée ». Le geste interdit :
   descendre la borne inf sous 2 planchers en invoquant la fourchette
   large. θ = 0,10 rel gelé avant run. Suspense limité mais réel.
2. Premier run : mot découvert : **S−**, δ = 1,0 = 100 % > 2θ = 0,20.
   Le suspense se dévoile : même la borne inf déclarée est à 2
   planchers — la saturation KSS par le QGP n'est PAS établie à
   θ = 0,10 près. Artefacts gelés offline (audits [HOLD] I-G1 / I-G2) :
   `examples/registre/QGP.*`.
3. Figé : mot dans ce test.
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from mvcg.registers import run_registers  # noqa: E402
from mvcg.tables import load_table  # noqa: E402


class TestOpenContactQGP(unittest.TestCase):
    def row(self) -> dict:
        by = {r["id"]: r for r in run_registers()["rows"]}
        return by["KSS_EtaS_QGP"]

    def test_qgp_word_frozen(self) -> None:
        r = self.row()
        self.assertEqual(r["verdict"], "S-")  # mot du premier run, figé
        self.assertEqual(r["statut"], "ouverte")
        self.assertIsNone(r["expected"])
        self.assertGreater(r["delta"], 2 * r["theta"])  # 1,0 > 0,20
        self.assertAlmostEqual(r["mu_loc"], 2.0, places=12)
        self.assertAlmostEqual(r["mu_ref"], 1.0, places=12)
        # Le mot tranche la saturation, pas KSS : la note gelée le dit.
        self.assertIn("saturation", r["note"])
        self.assertIn("jamais 'KSS violee'", r["note"])

    def test_qgp_anti_tautologie_borne_intacte(self) -> None:
        # Le geste interdit serait de descendre la borne inf sous 2
        # planchers en invoquant la fourchette large pour rapprocher
        # mu_loc du plancher. Le test verrouille : la table déclarée
        # est celle du run, la borne inf est 2,0, et la référence est
        # le plancher (1) — pas une valeur de la fourchette large.
        t = load_table("eta_s_qgp_LITERATURE.json")
        self.assertAlmostEqual(float(t["eta_s_over_kss_min_declared"]),
                               self.row()["mu_loc"], places=12)
        self.assertEqual(t["fluid"], "QGP (plasma quarks-gluons, RHIC/LHC)")
        # La fourchette large est déclarée dans la table (dette
        # assumée) mais n'est PAS la valeur pesée : le geste interdit
        # serait de peser 0,6 (borne large basse) pour chercher un P.
        lo, hi = t["range_broad_planck_units"]
        self.assertLess(float(lo), 1.2)  # la fourchette chevauche le plancher
        self.assertGreater(float(hi), 1.2)
        self.assertGreaterEqual(self.row()["mu_loc"], 2.0)

    def test_qgp_sweep_invariant(self) -> None:
        # Contact à θ seul (pas de GUM) : le balayage sous les quatre
        # paquets coïncide avec le mot home, comme la série O.
        from mvcg.verdict_register import street_sweep

        st = street_sweep("KSS_EtaS_QGP")
        licites = [r for r in st["rows"] if not r["units_kill"]]
        self.assertEqual(len(licites), 4)
        self.assertEqual(st["home_verdict"], "S-")
        for r in licites:
            self.assertEqual(r["verdict"], "S-")


if __name__ == "__main__":
    unittest.main(verbosity=2)
