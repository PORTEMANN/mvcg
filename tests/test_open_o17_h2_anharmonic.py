#!/usr/bin/env python3
"""Contact ouvert O17 — fondamental du H2 par Dunham ordre 1.

Chronologie du gel :
1. Protocole ecrit et gele avant toute execution (doc
   O17-H2-ANHARMONIQUE-CONTACT-OUVERT.md) : mu_loc = nu_pred(1-0) =
   omega_e - 2*omega_e x_e, extraits declares Huber & Herzberg (table
   h2_anharmonic_LITERATURE-2018.json : omega_e = 4401.2 +- 0.05,
   omega_e x_e = 121.34 +- 0.005). mu_ref = 4160.0 cm^-1, fondamental
   declare repris de la note de la table h2_vibration (meme gel que O15
   — la dette promise par O15). theta = u_delta = 0.5025932749251625
   cm^-1, decide=U, k=1 (convention GUM, precedent Rydberg voie 2).
   DETTE ASSUMEE : la reference est un arrondi (u = 0.5 declaree) — le
   contact pese la tare de declaration, pas la physique anharmonique
   (nu_pred ~ 4158.5 est la physique correcte).
   Erreur de gel conservee et corrigee dans le doc (trace) : la bande P
   est [theta, 2 theta] (regle _adc), non [theta, 3 theta] — l'estimation
   pre-run corrigee etait donc S- attendu, mot inconnu au gel.
2. Premier run : mot = S- (delta = 1.480000000000473 cm^-1,
   a 2.944727 theta — au cheveu de la borne P 2 theta = 1.0051865).
   Decouvert, pas choisi.
3. Ce test fixe le mot, comme pour tout contact du registre.
"""

from __future__ import annotations

import math
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from mvcg.gum import u_c  # noqa: E402
from mvcg.registers import run_registers  # noqa: E402
from mvcg.tables import load_table  # noqa: E402


class TestOpenContactO17H2Anharmonic(unittest.TestCase):
    def row(self) -> dict:
        by = {r["id"]: r for r in run_registers()["rows"]}
        return by["O17_H2_Anharmonique"]

    def test_o17_word_frozen(self) -> None:
        r = self.row()
        self.assertEqual(r["verdict"], "S-")  # mot du premier run, fige
        self.assertEqual(r["statut"], "ouverte")
        self.assertIsNone(r["expected"])
        # delta dans la bande S- : au-dela de 2*theta (borne P), trace
        # du ratio au cheveu consignee.
        self.assertGreater(r["delta"], 2.0 * r["theta"])
        self.assertAlmostEqual(r["delta"], 1.480000000000473, places=9)
        self.assertAlmostEqual(r["mu_loc"], 4158.5199999999995, places=9)
        self.assertAlmostEqual(r["mu_ref"], 4160.0, places=12)
        self.assertAlmostEqual(r["delta"] / r["theta"], 2.944727026482495,
                               places=9)

    def test_o17_calculee_depuis_la_table(self) -> None:
        # mu_loc est le transport Dunham calcule depuis les constantes
        # DECLAREES de la table — geste interdit : corriger une constante
        # pour rapprocher la reference (autre D).
        t = load_table("h2_anharmonic_LITERATURE-2018.json")
        p = t["params"]
        attendu = (float(p["omega_e_cm-1"])
                   - 2.0 * float(p["omega_ex_e_cm-1"]))
        self.assertAlmostEqual(self.row()["mu_loc"], attendu, places=9)
        self.assertAlmostEqual(float(p["nu10_declared_cm-1"]),
                               self.row()["mu_ref"], places=12)

    def test_o17_gum_decide_U_k1(self) -> None:
        # Le seuil EST l'incertitude propagee : decide=U, k=1 declares.
        g = self.row()["extra"]["gum"]
        self.assertEqual(g["decide"], "U")
        self.assertEqual(g["k"], 1.0)
        self.assertAlmostEqual(g["U"], 0.5025932749251625, places=12)
        # Les lignes B portees recombinent au seuil declare :
        lines = [{"name": "nu_pred_Dunham", "type": "B",
                  "u": 0.050990195135927854},
                 {"name": "nu10_declaree", "type": "B", "u": 0.5}]
        self.assertAlmostEqual(u_c(lines), 0.5025932749251625, places=12)
        # La tare depasse U a k=1 et k=2, passerait a k=3 — le S- est
        # un vrai signal de tare, pas un artefact de couverture.
        self.assertGreater(self.row()["delta"], 2.0 * g["uc"])
        self.assertLess(self.row()["delta"], 3.0 * g["uc"])

    def test_tare_assumee_declaree_dans_la_table(self) -> None:
        # Verrou : la dette de la reference arrondie est ecrite dans la
        # table — retirer la note serait une falsification du gel.
        t = load_table("h2_anharmonic_LITERATURE-2018.json")
        self.assertIn("arrondi", t["params"]["note"])
        self.assertIn("tare", t["params"]["note"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
