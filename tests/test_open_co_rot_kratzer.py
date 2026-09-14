#!/usr/bin/env python3
"""Contact SPEC CO — relation de Kratzer (prédiction croisée).

Chronologie du gel :
1. Protocole écrit avant toute exécution : SPEC-CO-ROT-PROTOCOLE.md
   §4 (gel 2026-09-14) — mu_loc = |D_e,calc − D0,obs| en Hz,
   D_e = 4·B_e³/ω_e² (oscillateur de Morse). Entrées déclarées B_e et
   ω_e (Huber & Herzberg 1979 via RIOS — indépendants de l'ajustement
   NIST de D₀) ; mu_ref = D₀ mesuré NIST JPCRD 53. theta = 70 Hz =
   u(D₀) déclarée NIST, gelée avant run. GUM : une ligne B,
   decide=theta, k=2.
2. Estimation pré-run honnête : delta ~ 70-80 Hz, delta/theta ~ 1,0-1,1
   — zone P [theta, 2theta] au cheveu : SUSPENSE MAXIMAL, le mot
   réellement inconnu (P, S+ et S- accessibles selon les arrondis H&H).
3. Premier run : mot découvert : **P**, delta = 97,551447 Hz
   (1,394 theta) — conforme à l'estimation (zone P au cheveu). La
   carte dit : la prédiction croisée ab initio de la distorsion
   centrifuge tient au cheveu mais pas dans le budget — la relation de
   Kratzer plus les constantes H&H 1979 ne reproduisent pas D0 au
   niveau de son incertitude moderne (70 Hz), sans échec franc. Le P
   nomme exactement le statut de la physique anharmonique gelée :
   "tenu mais pas exact" a la precision NIST. Pendant du S- 13CO :
   la regle mu a une limite nommée, la relation de Kratzer tient
   au cheveu.
4. Figé : mot et valeur à 12 décimales dans ce test.
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from mvcg.registers import run_registers  # noqa: E402
from mvcg.tables import load_table  # noqa: E402


class TestOpenContactCoRotKratzer(unittest.TestCase):
    def row(self) -> dict:
        by = {r["id"]: r for r in run_registers()["rows"]}
        return by["SPEC_CO_Rot_Kratzer"]

    def test_co_rot_kratzer_word_frozen(self) -> None:
        r = self.row()
        self.assertEqual(r["verdict"], "P")  # mot du premier run, figé
        self.assertEqual(r["statut"], "ouverte")
        self.assertIsNone(r["expected"])
        self.assertGreater(r["delta"], r["theta"])  # 97,6 > 70
        self.assertLessEqual(r["delta"], 2.0 * r["theta"])  # <= 140
        self.assertAlmostEqual(r["delta"] / r["theta"], 1.393592105834146,
                               places=12)
        self.assertAlmostEqual(r["mu_loc"], 97.55144740839023, places=12)

    def test_co_rot_kratzer_gum_carried_not_used(self) -> None:
        g = self.row()["extra"]["gum"]
        self.assertEqual(g["decide"], "theta")
        self.assertAlmostEqual(g["uc"], 70.0, places=12)
        self.assertAlmostEqual(g["U"], 140.0, places=12)

    def test_co_rot_kratzer_reproducible_from_table(self) -> None:
        t = load_table("co_rot_NIST-HH.json")
        p = t["params"]
        d_e = 4.0 * float(p["Be_cm-1"]) ** 3 / float(p["omega_e_cm-1"]) ** 2
        d_calc = d_e * float(p["cm-1_to_MHz"]) * 1e6
        self.assertAlmostEqual(abs(d_calc - float(p["D0_kHz"]) * 1e3),
                               self.row()["mu_loc"], places=6)
        self.assertIn("NIST-JPCRD53", t["vintage"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
