#!/usr/bin/env python3
"""Contact ouvert O18 — tare de lecture, pendant disciplinaire d'O17.

Chronologie du gel :
1. Protocole ecrit et gele avant toute execution (doc
   O18-H2-TARE-LECTURE-CONTACT-OUVERT.md) : MÊME transport Dunham qu'O17
   (nu_pred = omega_e - 2*omega_e x_e, mêmes extraits gelés), MÊME
   reference 4160, même delta attendu (~1.48 cm^-1). Seule chose change,
   gelee avant run : la lecture de precision de la reference — u =
   5/sqrt(3) = 2.886751345948129 (arrondi au dizaine, demi-largeur 5)
   au lieu de l'over-read u = 0.5 d'O17. theta = u_delta =
   2.887201644037585 cm^-1, decide=U, k=1.
   Amendement visible : la formule 5/sqrt(12) ecrite dans la trace d'O17
   est FAUSSE (demi-largeur 5 -> u = a/sqrt(3)) — corrigee ici et dans
   le doc d'O17, jamais effacee.
   Estimation pre-run honnete : delta ~ 1.48, ratio ~ 0.5126 -> S+ attendu
   SANS suspense (bande verifiee contre _adc : S+ = [0, theta],
   P = [theta, 2 theta]). Le suspense est dans la demonstration : même
   physique, même écart, verdict opposé — le verdict pèse des
   déclarations, pas des physiques.
2. Premier run : mot = S+ (delta = 1.480000000000473 cm^-1,
   à 0.512607 theta). Decouvert, pas choisi.
3. Ce test fixe le mot, comme pour tout contact du registre.
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


class TestOpenContactO18H2TareLecture(unittest.TestCase):
    def row(self) -> dict:
        by = {r["id"]: r for r in run_registers()["rows"]}
        return by["O18_H2_Tare_Lecture"]

    def test_o18_word_frozen(self) -> None:
        r = self.row()
        self.assertEqual(r["verdict"], "S+")  # mot du premier run, fige
        self.assertEqual(r["statut"], "ouverte")
        self.assertIsNone(r["expected"])
        self.assertLessEqual(r["delta"], r["theta"])
        self.assertAlmostEqual(r["delta"], 1.480000000000473, places=9)
        # Même transport qu'O17 : mu_loc identique au bit près.
        self.assertAlmostEqual(r["mu_loc"], 4158.5199999999995, places=9)
        self.assertAlmostEqual(r["mu_ref"], 4160.0, places=12)
        self.assertAlmostEqual(r["delta"] / r["theta"], 0.5126070785727243,
                               places=9)

    def test_o18_meme_transport_que_o17(self) -> None:
        # La démonstration repose sur l'identité du transport : mu_loc
        # d'O18 == mu_loc d'O17 à la table près. Geste interdit :
        # modifier un paramètre pour éloigner/rapprocher un verdict.
        by = {r["id"]: r for r in run_registers()["rows"]}
        self.assertAlmostEqual(by["O18_H2_Tare_Lecture"]["mu_loc"],
                               by["O17_H2_Anharmonique"]["mu_loc"],
                               places=9)
        # ... et le delta est identique : seule la lecture de la
        # référence diffère entre les deux contacts.
        self.assertAlmostEqual(by["O18_H2_Tare_Lecture"]["delta"],
                               by["O17_H2_Anharmonique"]["delta"],
                               places=9)
        self.assertGreater(by["O17_H2_Anharmonique"]["delta"],
                           2.0 * by["O17_H2_Anharmonique"]["theta"])
        self.assertLessEqual(by["O18_H2_Tare_Lecture"]["delta"],
                             by["O18_H2_Tare_Lecture"]["theta"])

    def test_o18_gum_decide_U_k1(self) -> None:
        g = self.row()["extra"]["gum"]
        self.assertEqual(g["decide"], "U")
        self.assertEqual(g["k"], 1.0)
        self.assertAlmostEqual(g["U"], 2.887201644037585, places=9)
        lines = [{"name": "nu_pred_Dunham", "type": "B",
                  "u": 0.050990195135927854},
                 {"name": "nu10_relue_honnete", "type": "B",
                  "u": 2.886751345948129}]
        self.assertAlmostEqual(u_c(lines), 2.887201644037585, places=9)

    def test_lecture_honnete_declaree_dans_la_table(self) -> None:
        # Verrou : la relecture honnête (5/sqrt(3)) et l'amendement de
        # formule sont écrits dans la table — retirer la note serait
        # une falsification du gel.
        t = load_table("h2_tare_lecture_LITERATURE-2018.json")
        self.assertAlmostEqual(float(t["params"]["u_nu10_cm-1"]),
                               2.886751345948129, places=9)
        self.assertIn("amendement", t["params"]["note"].lower())


if __name__ == "__main__":
    unittest.main(verbosity=2)
