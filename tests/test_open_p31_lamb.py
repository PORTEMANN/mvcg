#!/usr/bin/env python3
"""Contact ouvert P31 — le couplet Lamb (Dirac / Mohr / Erickson).

Chronologie du gel :
1. Protocole ecrit et gele avant toute execution (doc
   P31-LAMB-CONTACT-OUVERT.md) : le deplacement de Lamb 2S1/2-2P1/2 de
   l'hydrogene. Trois declarations figées (table
   lamb_shift_P31_LITERATURE-1981.json, sources citees) :
   - Dirac seul : degenerescence (shift 0), dette historique
     (Lamb-Retherford 1947 -> naissance de la QED) ;
   - calcul QED Mohr (annees 1970) : 1057.864 +- 0.014 MHz ;
   - calcul QED Erickson (annees 1970) : 1057.912 +- 0.011 MHz ;
   - mesure Lundeen-Pipkin 1981 : 1057.845 +- 0.009 MHz (reference).
   Vintages distincts declares : la mesure est POSTERIEURE aux calculs,
   aucune constante n'est derivee de la reference.
   P31_Lamb_Dirac : grammaire du score normalise de P30_Kato_gaussian
   (dimension 1, abs, theta = 0.05 fige). Estimation : S- a 20 theta,
   sans suspense.
   P31_Lamb_Mohr : theta = u_delta = 0.016643316977093238 MHz,
   decide=U k=1. Estimation : delta ~ 0.019, ratio ~ 1.14 -> P au
   cheveu de S+ annonce (bande [theta, 2 theta] verifiee contre _adc),
   suspense reel, mot inconnu au gel.
   P31_Lamb_Erickson : theta = u_delta = 0.014212670403551895 MHz,
   decide=U k=1. Estimation : delta ~ 0.067, ratio ~ 4.71 -> S- attendu
   sans suspense (Lundeen-Pipkin 1981 : « not in good agreement with
   theory »).
2. Premier run : Dirac S- (20,0 theta), Mohr P (1,1416 theta),
   Erickson S- (4,7141 theta) — pile les trois estimations. Decouverts,
   pas choisis : meme mesure, deux calculs QED de la meme epoque, deux
   verdicts differents — la machine pese des declarations.
3. Ce test fixe les mots, comme pour tout contact du registre.
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from mvcg.gum import u_c  # noqa: E402
from mvcg.registers import run_registers  # noqa: E402
from mvcg.tables import load_table  # noqa: E402


class TestOpenContactP31Lamb(unittest.TestCase):
    def rows(self) -> dict:
        return {r["id"]: r for r in run_registers()["rows"]}

    def test_p31_words_frozen(self) -> None:
        by = self.rows()
        self.assertEqual(by["P31_Lamb_Dirac"]["verdict"], "S-")
        self.assertEqual(by["P31_Lamb_Mohr"]["verdict"], "P")
        self.assertEqual(by["P31_Lamb_Erickson"]["verdict"], "S-")
        for cid in ("P31_Lamb_Dirac", "P31_Lamb_Mohr", "P31_Lamb_Erickson"):
            self.assertEqual(by[cid]["statut"], "ouverte")
            self.assertIsNone(by[cid]["expected"])
            self.assertEqual(by[cid]["campaign"], "P31")

    def test_p31_dirac_debt(self) -> None:
        # Dirac seul : degenerescence — la dette historique pesee, mot
        # normalise (grammaire P30_Kato_gaussian).
        r = self.rows()["P31_Lamb_Dirac"]
        self.assertEqual(r["mu_loc"], 0.0)
        self.assertEqual(r["mu_ref"], 1.0)
        self.assertAlmostEqual(r["delta"], 1.0, places=12)
        self.assertAlmostEqual(r["delta"] / r["theta"], 20.0, places=9)

    def test_p31_mohr_au_cheveu(self) -> None:
        # Mohr : P a 1.1416 theta — au cheveu de la frontiere S+ (theta).
        r = self.rows()["P31_Lamb_Mohr"]
        self.assertGreater(r["delta"], r["theta"])
        self.assertLessEqual(r["delta"], 2.0 * r["theta"])
        self.assertAlmostEqual(r["mu_loc"], 1057.864, places=9)
        self.assertAlmostEqual(r["mu_ref"], 1057.845, places=9)
        self.assertAlmostEqual(r["delta"], 0.019000000000005457, places=9)
        self.assertAlmostEqual(r["delta"] / r["theta"],
                               1.1415993594399363, places=9)
        g = r["extra"]["gum"]
        self.assertEqual(g["decide"], "U")
        self.assertEqual(g["k"], 1.0)
        lines = [{"name": "mohr_QED", "type": "B", "u": 0.014},
                 {"name": "lundeen_pipkin", "type": "B", "u": 0.009}]
        self.assertAlmostEqual(u_c(lines), 0.016643316977093238, places=12)

    def test_p31_erickson_s_minus(self) -> None:
        # Erickson : S- a 4.7141 theta — « not in good agreement with
        # theory » (PRL 46, 232), pese par la machine.
        r = self.rows()["P31_Lamb_Erickson"]
        self.assertGreater(r["delta"], 2.0 * r["theta"])
        self.assertAlmostEqual(r["mu_loc"], 1057.912, places=9)
        self.assertAlmostEqual(r["mu_ref"], 1057.845, places=9)
        self.assertAlmostEqual(r["delta"], 0.06700000000000728, places=9)
        self.assertAlmostEqual(r["delta"] / r["theta"],
                               4.714103549693467, places=9)
        g = r["extra"]["gum"]
        self.assertEqual(g["decide"], "U")
        lines = [{"name": "erickson_QED", "type": "B", "u": 0.011},
                 {"name": "lundeen_pipkin", "type": "B", "u": 0.009}]
        self.assertAlmostEqual(u_c(lines), 0.014212670403551895, places=12)

    def test_p31_vintages_distincts_declares(self) -> None:
        # Verrou : la posteriorite de la mesure et le desaccord des deux
        # calculs QED sont ecrits dans la table — retirer la note serait
        # une falsification du gel.
        t = load_table("lamb_shift_P31_LITERATURE-1981.json")
        note = t["params"]["note"]
        self.assertIn("POSTERIEURE", note)
        self.assertIn("debat", note.lower())


if __name__ == "__main__":
    unittest.main(verbosity=2)
