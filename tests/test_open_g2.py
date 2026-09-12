#!/usr/bin/env python3
"""Complexe g-2 — trois contacts ouverts, les trois couleurs.

Chronologie du gel (commune, écrite avant tout run) :
1. Protocoles déclarés avant exécution : AMU_exp_minus_WP20 prend
   l'étalonnage de la doctrine AMU (écart normalisé : θ = u_delta,
   decide=U, k=1) ; l'identification lattice est déclarée comme
   identification sœur (honnêteté O15) — contact séparé si montée.
   HVP_LO et
   HLbL sont des écarts entre deux fabrications d'un même terme :
   decide=U, k=2 standard machine (l'étalonnage se justifie par la
   nature de l'objet, jamais par le mot). Estimations pré-run
   honnêtes : WP20 S− net (δ/U = 3,67) ; HVP P au cheveu du S−
   (δ/U = 1,38 ; S− à k=1) ; HLbL S+ (δ/U = 0,76 ; P à k=1).
2. Premiers runs : mots découverts = estimations tenues :
   S−, P, S+ — la panoplie complète. La doctrine G2-CONTACT-OUVERT.md
   porte la question des identifications et le périmètre publié.
   Artefacts gelés offline (audits [HOLD] I-G1 / I-G2) :
   `examples/registre/{AMU20,HVP,HLBL}.*`.
3. Figé : mots dans ce test.
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


class TestOpenContactAMUWP20(unittest.TestCase):
    def row(self) -> dict:
        by = {r["id"]: r for r in run_registers()["rows"]}
        return by["AMU_exp_minus_WP20"]

    def test_wp20_word_frozen(self) -> None:
        r = self.row()
        self.assertEqual(r["verdict"], "S-")  # mot du premier run, figé
        self.assertEqual(r["statut"], "ouverte")
        self.assertIsNone(r["expected"])
        g = r["extra"]["gum"]
        self.assertGreater(r["delta"], 2.0 * g["U"])  # 279 > 152
        self.assertAlmostEqual(r["mu_loc"], 279.0, places=12)

    def test_wp20_anti_tautologie_identite_et_porte(self) -> None:
        # μ_ref = 0 identité, jamais ajustée ; l'écart est porté par
        # la table, pas reconstruit depuis a_exp (table sans a_exp).
        t = load_table("amu_wp20_LITERATURE.json")
        self.assertNotIn("a_exp", t)
        self.assertEqual(self.row()["mu_ref"], 0.0)
        self.assertAlmostEqual(float(t["delta_exp_minus_wp20"]),
                               self.row()["mu_loc"], places=12)
        g = self.row()["extra"]["gum"]
        lines = [{"name": "delta_WP20", "type": "B", "u": 76.0}]
        self.assertAlmostEqual(u_c(lines), 76.0, places=12)
        self.assertAlmostEqual(g["U"], gum_U(76.0, 1), places=12)
        # Même étalonnage que WP25 : θ = u_delta, k = 1.
        self.assertEqual(g["decide"], "U")
        self.assertEqual(g["k"], 1.0)
        self.assertEqual(self.row()["theta"], 76.0)

    def test_wp20_robustesse_jusqu_a_k3(self) -> None:
        # S− net : le mot tient pour k = 1, 2, 3 — pas une affaire de
        # couverture. (À k = 3 : U = 228 < 279/2 ? non : 279 > 456 ?
        # le seuil 2U à k=3 est 456 → S- tient.)
        g = self.row()["extra"]["gum"]
        self.assertGreater(self.row()["delta"], 3.0 * g["uc"])


class TestOpenContactHVPLO(unittest.TestCase):
    def row(self) -> dict:
        by = {r["id"]: r for r in run_registers()["rows"]}
        return by["HVP_LO_lat_vs_ee"]

    def test_hvp_word_frozen(self) -> None:
        r = self.row()
        self.assertEqual(r["verdict"], "P")  # mot du premier run, figé
        self.assertEqual(r["statut"], "ouverte")
        self.assertIsNone(r["expected"])
        g = r["extra"]["gum"]
        self.assertGreater(r["delta"], g["U"])  # 201 > 145,8
        self.assertLess(r["delta"], 2.0 * g["U"])  # 201 < 291,6
        self.assertAlmostEqual(r["mu_loc"], 201.0, places=12)

    def test_hvp_gum_correle_recombine(self) -> None:
        # Deux lignes B, R identité déclarée (indépendance assumée) ;
        # u_c recombine au seuil déclaré.
        g = self.row()["extra"]["gum"]
        self.assertEqual(g["decide"], "U")
        self.assertEqual(g["k"], 2.0)
        self.assertEqual(g["R"], [[1.0, 0.0], [0.0, 1.0]])  # R identité déclarée
        lines = [{"name": "lat_WP25", "type": "B", "u": 61.0},
                 {"name": "ee_WP20", "type": "B", "u": 40.0}]
        self.assertAlmostEqual(u_c(lines), 72.94518489934754, places=9)
        self.assertAlmostEqual(g["U"], 2.0 * 72.94518489934754, places=9)

    def test_hvp_suspense_cheveu_du_smoins(self) -> None:
        # Le P est tenu au cheveu du S− : à k=1, δ/u_c = 2,76 → S-.
        # Le suspense est déclaré au gel, le mot appartient au k=2.
        g = self.row()["extra"]["gum"]
        ratio = self.row()["delta"] / g["U"]
        self.assertGreater(ratio, 1.0)
        self.assertLess(ratio, 1.5)
        self.assertGreater(self.row()["delta"], 2.0 * g["uc"])


class TestOpenContactHLbL(unittest.TestCase):
    def row(self) -> dict:
        by = {r["id"]: r for r in run_registers()["rows"]}
        return by["HLbL_lat_vs_pheno"]

    def test_hlbl_word_frozen(self) -> None:
        r = self.row()
        self.assertEqual(r["verdict"], "S+")  # mot du premier run, figé
        self.assertEqual(r["statut"], "ouverte")
        self.assertIsNone(r["expected"])
        g = r["extra"]["gum"]
        self.assertLessEqual(r["delta"], g["U"])  # 19,2 ≤ 25,2
        self.assertAlmostEqual(r["mu_loc"], 19.2, places=12)

    def test_hlbl_gum_correle_recombine(self) -> None:
        g = self.row()["extra"]["gum"]
        self.assertEqual(g["decide"], "U")
        self.assertEqual(g["k"], 2.0)
        self.assertEqual(g["R"], [[1.0, 0.0], [0.0, 1.0]])  # R identité déclarée
        lines = [{"name": "lat", "type": "B", "u": 9.0},
                 {"name": "pheno", "type": "B", "u": 8.8}]
        self.assertAlmostEqual(u_c(lines), 12.58729518204765, places=9)
        self.assertAlmostEqual(g["U"], 2.0 * 12.58729518204765, places=9)

    def test_hlbl_suspense_cheveu_du_p(self) -> None:
        # À k=1 : δ/u_c = 1,53 → P. Le S+ tient du k=2 déclaré —
        # et la note de la mouture 6 (« k=2 → P ») est l'erreur
        # arithmétique corrigée dans la table re-déclarée.
        g = self.row()["extra"]["gum"]
        self.assertGreater(self.row()["delta"], g["uc"])  # 19,2 > 12,6
        self.assertGreater(self.row()["delta"] / g["uc"], 1.5)


if __name__ == "__main__":
    unittest.main(verbosity=2)
