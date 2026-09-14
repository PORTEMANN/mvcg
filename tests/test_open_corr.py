"""Chantier CORR — le corridor croisé (protocole CORRIDOR-CROISE-CONTACTS.md,
gelé avant run).

Le corridor_E est déjà une machine de verdicts sœur ; ce chantier y applique
la grammaire croisée S+/P/S− + GUM sur deux tensions inter-campagnes que le
corridor n'a jamais chiffrées comme telles : le décalage optimum de
stabilité (E63, n=14) vs minimum d'énergie (E65, n=18), et le point E61
(κ=0,05, t=90) vs le bord bas de la fenêtre E64-A (0,075, t=180).
"""

import unittest

from mvcg.registers import CONTACTS, run_contact
from mvcg.tables import load_table

CORR_WORDS = {
    "CORR_Stabilite_Energie": "S-",
    "CORR_Fenetre_Point": "S-",
}


class TestCorridorCroise(unittest.TestCase):
    def test_mots_decouverts_conformes_au_protocole_gele(self):
        for cid, mot in CORR_WORDS.items():
            with self.subTest(contact=cid):
                c = next(x for x in CONTACTS if x.id == cid)
                self.assertEqual(run_contact(c)["verdict"], mot)

    def test_transport_pur_reference_jamais_dans_le_calcul(self):
        t = load_table("corridor_cages_LITERATURE-E2026.json")
        p = t["params"]
        attendus = {
            "CORR_Stabilite_Energie": float(p["e63_n_opt_marge"]),
            "CORR_Fenetre_Point": float(p["e61_kappa"]),
        }
        refs = {
            "CORR_Stabilite_Energie": float(p["e65_n_min_energie"]),
            "CORR_Fenetre_Point": float(p["e64a_bord_bas"]),
        }
        for cid, mu in attendus.items():
            with self.subTest(contact=cid):
                r = run_contact(next(x for x in CONTACTS if x.id == cid))
                self.assertEqual(r["mu_loc"], mu)
                self.assertEqual(r["mu_ref"], refs[cid])
                self.assertNotEqual(r["mu_loc"], r["mu_ref"])

    def test_tensions_chiffrees(self):
        # les deux écarts annoncés au gel — la machine mesure en unités de
        # seuil ce que le corridor n'avait chiffré nulle part.
        r1 = run_contact(next(x for x in CONTACTS if x.id == "CORR_Stabilite_Energie"))
        r2 = run_contact(next(x for x in CONTACTS if x.id == "CORR_Fenetre_Point"))
        self.assertAlmostEqual(r1["delta"], 4.0)
        self.assertAlmostEqual(r1["delta"] / r1["extra"]["gum"]["U"], 2.8284271247461903)
        self.assertAlmostEqual(r2["delta"], 0.025)
        self.assertAlmostEqual(r2["delta"] / r2["extra"]["gum"]["U"], 3.4641016151377544)

    def test_dettes_nommees_pas_masquees(self):
        # les dettes sont écrites dans les notes des runners, pas résorbées
        # par des u gonflées : u(n)=1 déclarée (comptage entier), u(bord)
        # = bracket rectangulaire — aucune ne dépend de la valeur mesurée.
        r1 = run_contact(next(x for x in CONTACTS if x.id == "CORR_Stabilite_Energie"))
        r2 = run_contact(next(x for x in CONTACTS if x.id == "CORR_Fenetre_Point"))
        self.assertIn("découplent", r1["note"] + r1["extra"].get("ansatz", ""))
        self.assertIn("temps de vol", r2["note"] + r2["extra"].get("ansatz", ""))


if __name__ == "__main__":
    unittest.main()
