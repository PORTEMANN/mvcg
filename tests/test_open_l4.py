"""Chantier L4 — le gyrocorpus (protocole L4-GYROCORPS-CONTACTS.md, gelé avant run).

Transposition comparée du corpus hors-programme « gap gyroscopique comme
observable de L4 » (notes P1–P4 + addendum) : la loi arithmétique du corpus
a été ajustée par les dernières campagnes (addendum P3 : rétractation du
maximum à k₂, fenêtre inertielle reformulée). La machine en pèse trois
nombres — le gap universel, la transposabilité de la branche au régime fin,
et la prédiction de la fenêtre par la branche (contrainte 1 du pont pesée
indirectement).
"""

import math
import unittest

from mvcg.registers import CONTACTS, run_contact
from mvcg.tables import load_table

L4_WORDS = {
    "L4_Gap_Universel": "S+",
    "L4_Branche_k2_RegimeFin": "S-",
    "L4_Fenetre_Branche": "P",
    "L4_Kappa_Eff": "S-",
    "L4_Kelvin_Gap": "S-",
}


class TestL4Gyrocorps(unittest.TestCase):
    def test_mots_decouverts_conformes_au_protocole_gele(self):
        for cid, mot in L4_WORDS.items():
            with self.subTest(contact=cid):
                c = next(x for x in CONTACTS if x.id == cid)
                self.assertEqual(run_contact(c)["verdict"], mot)

    def test_transport_pur_reference_jamais_dans_le_calcul(self):
        # mu_loc vient de la table + de la branche gelée seulement ; la
        # référence (mu_ref) ne doit jamais entrer dans le transport.
        t = load_table("l4_gyrocorps_LITERATURE-HP2027.json")
        p = t["params"]
        k1, k2, k3 = float(p["k1"]), float(p["k2"]), float(p["k3"])
        w0, beta = float(p["omega0"]), float(p["beta"])
        attendus = {
            "L4_Gap_Universel": float(p["w1_m12_fine"]),
            "L4_Branche_k2_RegimeFin": math.sqrt(w0**2 + beta**2 * k2**4),
            "L4_Fenetre_Branche": math.sqrt(w0**2 + beta**2 * k3**4) / float(p["vide_k3"]),
            "L4_Kappa_Eff": 4.0 * math.pi * beta,
            "L4_Kelvin_Gap": 0.5 * k1**2,
        }
        for cid, mu in attendus.items():
            with self.subTest(contact=cid):
                r = run_contact(next(x for x in CONTACTS if x.id == cid))
                self.assertAlmostEqual(r["mu_loc"], mu, places=12)
                self.assertNotEqual(r["mu_loc"], r["mu_ref"])

    def test_ratios_pre_run_gelés(self):
        # les trois ratios annoncés au gel — la machine ne découvre pas
        # autre chose que ce qu'elle annonçait (suspense tenu ou nommé).
        ratios = {
            "L4_Gap_Universel": (0.010, 0.35355339059327406),
            "L4_Branche_k2_RegimeFin": (1.2048398843919652, 56.34377952231124),
            "L4_Fenetre_Branche": (0.6963572720020315, 1.1975078553915033),
        }
        for cid, (delta, ratio) in ratios.items():
            with self.subTest(contact=cid):
                r = run_contact(next(x for x in CONTACTS if x.id == cid))
                self.assertAlmostEqual(r["delta"], delta, places=9)
                U = r["extra"]["gum"]["U"]
                self.assertAlmostEqual(r["delta"] / U, ratio, places=9)

    def test_lien_direct_moitie_par_moitie(self):
        # volet 2 (L4-DEUX-NOMBRES-LIES.md, gelé avant run) : le lien
        # Kelvin nu est réfuté sur chaque moitié, dettes chiffrées —
        # pente : kappa_eff x22,4 la circulation declaree (214 uc) ;
        # gap : circulation pure sans terme de gap, ecart 30 uc.
        r_k = run_contact(next(x for x in CONTACTS if x.id == "L4_Kappa_Eff"))
        r_g = run_contact(next(x for x in CONTACTS if x.id == "L4_Kelvin_Gap"))
        self.assertEqual(r_k["verdict"], "S-")
        self.assertEqual(r_g["verdict"], "S-")
        self.assertAlmostEqual(r_k["delta"] / r_k["extra"]["gum"]["U"], 214.0, places=6)
        self.assertAlmostEqual(r_g["delta"] / r_g["extra"]["gum"]["U"], 30.036171445206115, places=6)
        # sensibilité declaree au gel : la forme log favorable (x12,9)
        # laisse le verdict S- invariant — consignee, pas utilisee.
        k3, beta = float(load_table("l4_gyrocorps_LITERATURE-HP2027.json")["params"]["k3"]), 11.2
        xi = 0.3
        kappa_eff_log = 4.0 * math.pi * beta / math.log(1.0 / (k3 * xi))
        self.assertGreater(kappa_eff_log / (2.0 * math.pi), 12.0)

    def test_lecon_d_ensemble(self):
        # l'arc L4 gelé avant run : la structure du gap tient en régime fin
        # (S+), la pente ne s'y transpose pas (S- — dette amplitude nommée),
        # mais la branche rapportée à la ligne vide prédit la fenêtre
        # reformulée à ~1,2 uc (P au cheveu — le pont tient indirectement).
        mots = {cid: run_contact(next(x for x in CONTACTS if x.id == cid))["verdict"]
                for cid in L4_WORDS}
        self.assertEqual(mots["L4_Gap_Universel"], "S+")
        self.assertEqual(mots["L4_Branche_k2_RegimeFin"], "S-")
        self.assertEqual(mots["L4_Fenetre_Branche"], "P")


if __name__ == "__main__":
    unittest.main()
