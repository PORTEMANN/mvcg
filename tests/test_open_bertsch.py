#!/usr/bin/env python3
"""Contact ouvert hyperfluidité — le paramètre de Bertsch ξ à l'unitarité.

Chronologie du gel :
1. Protocole écrit et gelé avant toute exécution : ξ = (5/3)·E/(Nε_F)
   en ansatz BCS mean-field à T = 0 (Leggett 1980), équations gap +
   nombre résolues par quadrature avec corrections de queue
   analytiques (`bertsch.py`), aucun point ajusté sur la référence.
   La référence ξ ≈ 0,370 est le consensus expérience/QMC déclaré de
   la table (`xi_unitary_LITERATURE.json`). Dette assumée : l'ansatz
   mean-field ne récupère pas la corrélation forte de l'unitarité —
   pendant exact de P27 (He Hartree-Fock). θ = 0,10 abs gelé avant run.
   Estimation pré-run honnête : ξ_MF = 0,5905, δ ≈ 60 % → S− attendu
   net ; suspense quasi nul — contact de calibre de l'erreur mean-field.
2. Premier run : mot découvert : **S−**, δ = 0,2206 abs > 2θ = 0,20,
   μ/ε_F = 0,5906 et Δ/ε_F = 0,6864 conformes à la littérature
   mean-field. Artefacts gelés offline (audits [HOLD] I-G1 / I-G2) :
   `examples/registre/BERTSCH.*`.
3. Figé : mot dans ce test.
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from mvcg.bertsch import bertsch_xi  # noqa: E402
from mvcg.registers import run_registers  # noqa: E402
from mvcg.tables import load_table  # noqa: E402


class TestOpenContactBertsch(unittest.TestCase):
    def row(self) -> dict:
        by = {r["id"]: r for r in run_registers()["rows"]}
        return by["Bertsch_Xi_Unitary"]

    def test_bertsch_word_frozen(self) -> None:
        r = self.row()
        self.assertEqual(r["verdict"], "S-")  # mot du premier run, figé
        self.assertEqual(r["statut"], "ouverte")
        self.assertIsNone(r["expected"])
        self.assertGreater(r["delta"], 2 * r["theta"])  # 0,221 > 0,20
        self.assertAlmostEqual(r["mu_loc"], 0.5906055451215995, places=9)
        self.assertAlmostEqual(r["mu_ref"], 0.370, places=12)

    def test_bertsch_solveur_vs_litterature(self) -> None:
        # Le solveur mean-field reproduit le triplet de littérature :
        # x = μ/ε_F = 0,5906, y = Δ/ε_F = 0,6864, ξ = 0,5905.
        sol = bertsch_xi()
        self.assertAlmostEqual(sol["mu_over_ef"], 0.5906, places=3)
        self.assertAlmostEqual(sol["delta_over_ef"], 0.6864, places=3)
        self.assertAlmostEqual(sol["xi"], 0.5905, places=3)

    def test_bertsch_anti_tautologie_recombinaison(self) -> None:
        # Le geste interdit serait d'ajuster le solveur sur la référence
        # ξ ≈ 0,370. Le test verrouille : la table déclarée est celle du
        # run, et le solveur recombiné donne le μ du registre.
        t = load_table("xi_unitary_LITERATURE.json")
        self.assertAlmostEqual(float(t["xi_exp"]), self.row()["mu_ref"],
                               places=12)
        self.assertAlmostEqual(bertsch_xi()["xi"], self.row()["mu_loc"],
                               places=9)

    def test_bertsch_sweep_invariant(self) -> None:
        # Contact à θ seul (pas de GUM) : le balayage sous les quatre
        # paquets coïncide avec le mot home, comme la série O.
        from mvcg.verdict_register import street_sweep

        st = street_sweep("Bertsch_Xi_Unitary")
        licites = [r for r in st["rows"] if not r["units_kill"]]
        self.assertEqual(len(licites), 4)
        self.assertEqual(st["home_verdict"], "S-")
        for r in licites:
            self.assertEqual(r["verdict"], "S-")


if __name__ == "__main__":
    unittest.main(verbosity=2)
