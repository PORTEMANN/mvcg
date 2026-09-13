#!/usr/bin/env python3
"""Contact ouvert hyperfluidité — la marge η/s du ⁴He au plancher KSS.

Chronologie du gel :
1. Protocole écrit avant toute exécution : la conjecture Kovtun-Son-
   Starinets (2005), η/s ≥ ℏ/(4πk_B), est une BORNE — démontrée en
   holographie, avec des contre-exemples théoriques en théorie
   effective, jamais violée expérimentalement. La fabrication est la
   borne inférieure expérimentale déclarée du ⁴He liquide (η/s ≥ 8,8
   planchers, Schafer & Teaney 2009, reprise dans Kagamihara et al.
   2019) lue dans la table (`eta_s_kss_LITERATURE.json`), la référence
   est le plancher (1). Le geste interdit est double et écrit :
   déplacer 8,8 vers le plancher, ou lire S− comme une réfutation de
   KSS. θ = 0,10 rel gelé avant run. Estimation pré-run honnête :
   δ = 780 % → S− net attendu ; suspense structurellement nul —
   contact de marge, comme Bertsch est un contact de dette.
2. Premier run : mot découvert : **S−**, δ = 7,8 = 780 % > 2θ = 0,20.
   Artefacts gelés offline (audits [HOLD] I-G1 / I-G2) :
   `examples/registre/KSS.*`.
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


class TestOpenContactKSS(unittest.TestCase):
    def row(self) -> dict:
        by = {r["id"]: r for r in run_registers()["rows"]}
        return by["KSS_EtaS_He4"]

    def test_kss_word_frozen(self) -> None:
        r = self.row()
        self.assertEqual(r["verdict"], "S-")  # mot du premier run, figé
        self.assertEqual(r["statut"], "ouverte")
        self.assertIsNone(r["expected"])
        self.assertGreater(r["delta"], 2 * r["theta"])  # 7,8 > 0,20
        self.assertAlmostEqual(r["mu_loc"], 8.8, places=12)
        self.assertAlmostEqual(r["mu_ref"], 1.0, places=12)
        # Le mot mesure la MARGE, pas la validité de KSS : un fluide
        # au-dessus de la borne la satisfait — la règle gelée le dit.
        self.assertIn("PAS une identite", r["note"])
        self.assertIn("marge", r["extra"]["rule"])

    def test_kss_anti_tautologie_table_intacte(self) -> None:
        # Le geste interdit serait de rapprocher 8,8 du plancher pour
        # fabriquer une « saturation ». Le test verrouille : la table
        # déclarée est celle du run, et la recombinaison depuis la
        # table donne le μ du registre.
        t = load_table("eta_s_kss_LITERATURE.json")
        self.assertAlmostEqual(float(t["eta_s_over_kss_min_exp"]),
                               self.row()["mu_loc"], places=12)
        self.assertEqual(t["fluid"], "4He liquide")
        self.assertEqual(t["kss_bound"], "hbar/(4*pi*k_B)")
        # La référence est le plancher (1 en unités du plancher),
        # jamais la valeur de la table : la comparaison est table vs
        # borne, pas table vs elle-même.
        self.assertAlmostEqual(self.row()["mu_ref"], 1.0, places=12)

    def test_kss_sweep_invariant(self) -> None:
        # Contact à θ seul (pas de GUM) : le balayage sous les quatre
        # paquets coïncide avec le mot home, comme la série O.
        from mvcg.verdict_register import street_sweep

        st = street_sweep("KSS_EtaS_He4")
        licites = [r for r in st["rows"] if not r["units_kill"]]
        self.assertEqual(len(licites), 4)
        self.assertEqual(st["home_verdict"], "S-")
        for r in licites:
            self.assertEqual(r["verdict"], "S-")


if __name__ == "__main__":
    unittest.main(verbosity=2)
