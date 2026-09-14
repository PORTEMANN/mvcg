"""Contacts affinés « les quatre P » (REFINED-P-CONTACTS.md, gelé avant run).

D-bump : les versions affinées partagent le runner ET le sha256 de leur
contact d'origine — seules les déclarations d'incertitude changent.
L'anti-fraude est le test d'identité bit-à-bit du transport.
"""

import unittest

from mvcg.registers import CONTACTS, run_contact

REFINED = {
    "O19_CO2_nu3_Fine": ("O2_CO2_nu3", "S-"),
    "O20_Carbon_D_Raman_Fine": ("O3_Carbon_D_Raman", "S-"),
    "SPEC_CO_Rot_Kratzer_Fine": ("SPEC_CO_Rot_Kratzer", "S-"),
    "P31_Lamb_Mohr_K2": ("P31_Lamb_Mohr", "S+"),
}


class TestRefinedPContacts(unittest.TestCase):
    def test_mots_decouverts_conformes_au_protocole_gele(self):
        for cid, (_, mot) in REFINED.items():
            with self.subTest(contact=cid):
                c = next(x for x in CONTACTS if x.id == cid)
                self.assertEqual(run_contact(c)["verdict"], mot)

    def test_transport_identique_bit_a_bit(self):
        # D-bump honnête : mu_loc et runner_sha256 strictement égaux à l'original
        for cid, (orig, _) in REFINED.items():
            with self.subTest(contact=cid, original=orig):
                r = run_contact(next(x for x in CONTACTS if x.id == cid))
                ro = run_contact(next(x for x in CONTACTS if x.id == orig))
                self.assertEqual(r["mu_loc"], ro["mu_loc"])
                self.assertEqual(
                    r["extra"].get("runner_sha256"),
                    ro["extra"].get("runner_sha256"),
                )

    def test_mohr_k2_dependance_a_la_couverture(self):
        # la leçon du contact : le mot dépend du niveau de couverture —
        # même écart, k=1 -> P (1,14 uc), k=2 -> S+ (0,57 U)
        r2 = run_contact(next(x for x in CONTACTS if x.id == "P31_Lamb_Mohr_K2"))
        r1 = run_contact(next(x for x in CONTACTS if x.id == "P31_Lamb_Mohr"))
        g2, g1 = r2["extra"]["gum"], r1["extra"]["gum"]
        self.assertEqual(r2["delta"], r1["delta"])  # même transport
        self.assertEqual(g2["uc"], g1["uc"])  # mêmes lignes
        self.assertEqual(g2["k"], 2)
        self.assertEqual(g1["k"], 1)
        self.assertAlmostEqual(g2["U"], 2.0 * g1["U"])
        self.assertEqual(r1["verdict"], "P")
        self.assertEqual(r2["verdict"], "S+")

    def test_affinage_revele_dettes_sans_casser_les_originaux(self):
        # les contacts grossiers restent publiés et inchangés : mémoire = somme
        for cid, (orig, _) in REFINED.items():
            with self.subTest(original=orig):
                ro = run_contact(next(x for x in CONTACTS if x.id == orig))
                self.assertIn(ro["verdict"], ("P", "S+", "S-"))
        # les trois dettes nommées passent de P (grossier) à S- (affiné)
        for cid in (
            "O19_CO2_nu3_Fine",
            "O20_Carbon_D_Raman_Fine",
            "SPEC_CO_Rot_Kratzer_Fine",
        ):
            with self.subTest(contact=cid):
                r = run_contact(next(x for x in CONTACTS if x.id == cid))
                self.assertEqual(r["verdict"], "S-")


if __name__ == "__main__":
    unittest.main()
