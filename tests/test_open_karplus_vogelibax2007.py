#!/usr/bin/env python3
"""Contacts ouverts NMR-Karplus Vogeli-Bax 2007 — la seconde voie.

Chronologie du gel :
1. Protocole ecrit et gele avant toute execution (doc
   NMR-KARPLUS-VOGELIBAX-CONTACT-OUVERT.md, campagne croisee) :
   3J(HN,Ha) = 7.97 cos^2(phi-60) - 1.26 cos(phi-60) + 0.63
   (Vogeli, Ying, Grishaev, Bax, JACS 2007, 129, 9377), memes phi
   declares que la paire VB et MEME reference typique (4.0 / 8.5 Hz,
   ordre de grandeur « pas un PDB », dette identique). theta = 0.10 rel
   au MEME etalonnage que la paire VB. La parametrisation a ete choisie
   pour sa canonicite et sa tracabilite, jamais pour un mot attendu.
   Estimation pre-run (CORRIGEE : l'estimation initiale helice 4,2525
   etait une erreur d'addition du redacteur — 1,9925+0,63+0,63 =
   3,2525) : le run a decouvert helice P a 1,87 theta (a 0,13 theta de
   la frontiere S-), brin P a 1,60 theta. L'estimation erronnee est
   conservee en trace dans la doc et la docstring, le mot vrai est
   fige ici.
2. Premier run : helice P (delta = 0,186875 = 18,69 %), brin P
   (delta = 0,16 = 16,0 %). Decouverts, pas choisis.
3. Ce test fixe les mots, comme pour tout contact du registre.

Le resultat de la campagne croisee : sur la MEME conformation helice,
la 1re voie (Vuister-Bax 1993) disait S+ a 0,27 theta et la 2e voie
(Vogeli-Bax 2007) dit P a 1,87 theta — la loi de Karplus n'est pas
robuste au choix des coefficients a theta = 0,10 de la reference
typique. Le contact mesure la sensibilite de la loi a sa
parametrisation, pas la physique du peptide.
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from mvcg.registers import run_registers  # noqa: E402
from mvcg.tables import load_table  # noqa: E402


class TestOpenContactKarplusVogeliBax2007(unittest.TestCase):
    def row(self, cid: str) -> dict:
        by = {r["id"]: r for r in run_registers()["rows"]}
        return by[cid]

    def test_helix_word_frozen(self) -> None:
        r = self.row("NMR_Karplus_Helix_VogeliBax2007")
        self.assertEqual(r["verdict"], "P")  # mot du premier run, fige
        self.assertEqual(r["statut"], "ouverte")
        self.assertIsNone(r["expected"])
        self.assertLess(r["theta"], r["delta"])  # 0.10 < 0.186875
        self.assertLess(r["delta"], 2 * r["theta"])  # zone P
        self.assertAlmostEqual(r["mu_loc"], 3.2525, places=12)
        self.assertAlmostEqual(r["delta"], 0.186875, places=12)
        self.assertAlmostEqual(r["delta"] / r["theta"], 1.86875, places=12)

    def test_sheet_word_frozen(self) -> None:
        r = self.row("NMR_Karplus_Sheet_VogeliBax2007")
        self.assertEqual(r["verdict"], "P")  # mot du premier run, fige
        self.assertEqual(r["statut"], "ouverte")
        self.assertIsNone(r["expected"])
        self.assertLess(r["theta"], r["delta"])  # 0.10 < 0.16
        self.assertLess(r["delta"], 2 * r["theta"])  # zone P
        self.assertAlmostEqual(r["mu_loc"], 9.86, places=12)
        self.assertAlmostEqual(r["delta"], 0.16, places=12)

    def test_meme_reference_que_la_paire_vb(self) -> None:
        # La seconde voie ne change que les coefficients : geometrie
        # et reference typique sont portees par la table, verrou
        # anti-re-calibrage — recalibrer la reference pour rapprocher
        # le mot serait le geste interdit.
        t = load_table("karplus_peptide_VOGELIBAX2007.json")
        self.assertEqual(float(t["phi_helix_deg"]), -60.0)
        self.assertEqual(float(t["phi_sheet_deg"]), -120.0)
        self.assertEqual(float(t["J_helix_typical_Hz"]), 4.0)
        self.assertEqual(float(t["J_sheet_typical_Hz"]), 8.5)
        self.assertAlmostEqual(float(t["A"]), 7.97, places=12)
        self.assertAlmostEqual(float(t["B"]), -1.26, places=12)
        self.assertAlmostEqual(float(t["C"]), 0.63, places=12)

    def test_les_deux_voies_divergent_helice(self) -> None:
        # La question de la campagne croisee, verrouillee : meme
        # conformation helice, deux parametrisations canoniques, deux
        # mots differents (S+ a 0,27 theta contre P a 1,87 theta).
        vb = self.row("NMR_Karplus_Helix")
        vb2 = self.row("NMR_Karplus_Helix_VogeliBax2007")
        self.assertEqual(vb["verdict"], "S+")
        self.assertEqual(vb2["verdict"], "P")
        ecart = abs(vb["mu_loc"] - vb2["mu_loc"])
        self.assertAlmostEqual(ecart, 4.1075 - 3.2525, places=12)
        self.assertGreater(ecart, 0.8)  # ~0.86 Hz entre les deux lois


if __name__ == "__main__":
    unittest.main(verbosity=2)
