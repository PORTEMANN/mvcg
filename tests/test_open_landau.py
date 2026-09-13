#!/usr/bin/env python3
"""Contact ouvert hyperfluidité — la vitesse critique de Landau du ⁴He.

Chronologie du gel :
1. Protocole écrit et gelé avant toute exécution : v_c = min_p E(p)/p
   (Landau 1941) sur le spectre phonon-roton déclaré de la table
   (`he4_spectrum_LANDAU.json`) — scan fin + parabole locale, aucun
   point ajusté sur la référence. La référence v_c ≈ 58 m/s est un
   ordre de grandeur de littérature déclaré. Dette assumée : spectre
   et v_c ne sont pas physiquement indépendants (le min de E/p EST le
   roton) — le contact mesure la cohérence interne de la carte
   spectrale, pas une prédiction. θ = 0,10 rel gelé avant run.
   Estimation pré-run honnête : v_c ≈ 58,8 m/s au roton, δ ≈ 1,3 %
   → S+ attendu ; suspense faible, dette assumée.
2. Premier run : mot découvert : **S+**, δ = 1,34 %, mécanisme roton
   confirmé au point déclaré (k* = 1,920 Å⁻¹). Artefacts gelés
   offline (audits [HOLD] I-G1 / I-G2) : `examples/registre/LANDAU.*`.
3. Figé : mot dans ce test.
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from mvcg.landau import landau_vc, spectrum_doc  # noqa: E402
from mvcg.registers import run_registers  # noqa: E402
from mvcg.tables import load_table  # noqa: E402


class TestOpenContactLandau(unittest.TestCase):
    def row(self) -> dict:
        by = {r["id"]: r for r in run_registers()["rows"]}
        return by["Landau_Vc_He4"]

    def test_landau_word_frozen(self) -> None:
        r = self.row()
        self.assertEqual(r["verdict"], "S+")  # mot du premier run, figé
        self.assertEqual(r["statut"], "ouverte")
        self.assertIsNone(r["expected"])
        self.assertLessEqual(r["delta"], r["theta"])  # 1,34 % ≤ 10 %
        self.assertAlmostEqual(r["mu_loc"], 58.77813039835071, places=9)
        self.assertAlmostEqual(r["mu_ref"], 58.0, places=12)

    def test_landau_minimum_au_roton_declare(self) -> None:
        # Le calcul trouve le minimum au roton déclaré — c'est la
        # physique attendue (E/p y est minimal), et c'est aussi la
        # dette déclarée : spectre et v_c ne sont pas indépendants.
        r = self.row()
        self.assertEqual(r["extra"]["mechanism"], "roton")
        self.assertAlmostEqual(r["extra"]["k_star_ang^-1"],
                               1.9200342857142858, places=9)
        t = load_table("he4_spectrum_LANDAU.json")
        roton = [p for p in t["points"] if abs(p[0] - 1.92) < 1e-9][0]
        self.assertAlmostEqual(float(roton[1]), 8.62, places=12)
        # La pente phonon ne gagne pas : c = 238 m/s > v_c.
        self.assertGreater(float(t["phonon_speed_m_s"]), r["mu_loc"])

    def test_landau_anti_tautologie_points_intacts(self) -> None:
        # Le geste interdit serait de déplacer les points du spectre
        # (ou la référence) pour faire coïncider v_c. Le test verrouille
        # : la table déclarée est celle du run, et la loi Landau
        # recombinée depuis la table donne le μ du registre.
        t = spectrum_doc()
        sol = landau_vc(t["points"])
        self.assertAlmostEqual(sol["vc_m_s"], self.row()["mu_loc"],
                               places=9)
        self.assertAlmostEqual(float(t["vc_ref_m_s"]),
                               self.row()["mu_ref"], places=12)

    def test_landau_sweep_invariant(self) -> None:
        # Contact à θ seul (pas de GUM) : le balayage sous les quatre
        # paquets coïncide avec le mot home, comme la série O.
        from mvcg.verdict_register import street_sweep

        st = street_sweep("Landau_Vc_He4")
        licites = [r for r in st["rows"] if not r["units_kill"]]
        self.assertEqual(len(licites), 4)
        self.assertEqual(st["home_verdict"], "S+")
        for r in licites:
            self.assertEqual(r["verdict"], "S+")


if __name__ == "__main__":
    unittest.main(verbosity=2)
