#!/usr/bin/env python3
"""Contact ouvert HVP pi pi — CMD-3 vs moyenne pre-CMD-3, l'ecart porte.

Chronologie du gel :
1. Protocole ecrit et gele avant toute execution (doc
   HVP-PIPI-CMD3-CONTACT-OUVERT.md, campagne croisee) : mu_loc = ecart
   tel que publie dans le PRL CMD-3 : a_mu^had,LO(2pi, CMD-3) = 5260(42)
   vs moyenne des mesures precedentes = 5060(34) (1e-11) -> delta = 200,
   PORTE, pas calcule depuis les sections efficaces. La reference est
   l'identite (deux fabrications du meme objet). theta = u_delta =
   sqrt(42^2+34^2) = 54.037 (1e-11), independance assumée (meme
   convention que la table hvp_lo). GUM : decide=U, k=1 — l'etalonnage
   de la doctrine AMU. Identification multiple declaree : la moyenne
   pre-CMD-3 est KLOE-dominee ; un contact KLOE seul exigerait une
   valeur KLOE sur la fenetre exacte CMD-3, non publiee — identifiee,
   jamais choisie apres coup. Dette de fenetre declaree. Estimation
   pre-run : 200 > 54 -> S- attendu a ~3.7 theta — suspense faible :
   contact de calibre, pas de suspense.
2. Premier run : mot = S- (delta = 200.0, a 3.70 theta). Decouvert,
   pas choisi.
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


class TestOpenContactHVPpipiCMD3(unittest.TestCase):
    def row(self) -> dict:
        by = {r["id"]: r for r in run_registers()["rows"]}
        return by["HVP_Pipi_CMD3_vs_PreAvg"]

    def test_hvp_pipi_word_frozen(self) -> None:
        r = self.row()
        self.assertEqual(r["verdict"], "S-")  # mot du premier run, fige
        self.assertEqual(r["statut"], "ouverte")
        self.assertIsNone(r["expected"])
        self.assertGreater(r["delta"], r["theta"])  # 200 > 54
        self.assertAlmostEqual(r["mu_loc"], 200.0, places=12)
        self.assertAlmostEqual(r["delta"] / r["theta"], 3.7011660509880264,
                               places=12)

    def test_hvp_pipi_delta_porte_pas_calcule(self) -> None:
        # mu_loc est la valeur declaree de la table, portee telle
        # quelle : ce n'est pas une re-integration des sections
        # efficaces CMD-3 / KLOE. Le geste interdit serait de
        # recombiner les sections efficaces — la table ne porte que
        # les integrales publiees, le calcul est impossible : porte,
        # pas derive.
        t = load_table("hvp_pipi_cmd3_LITERATURE.json")
        p = t["params"]
        self.assertEqual(float(p["delta_cmd3_minus_premoy"]),
                         self.row()["mu_loc"])
        self.assertNotIn("sigma_points", p)  # pas de reintegration possible
        self.assertEqual(float(p["u_delta"]), self.row()["theta"])
        self.assertAlmostEqual(float(p["a_cmd3"]) - float(p["a_premoy"]),
                               self.row()["mu_loc"], places=12)

    def test_hvp_pipi_gum_decide_U_k1(self) -> None:
        # Le seuil EST l'incertitude de l'ecart : decide=U, k=1
        # declares. Robustesse, pas choix : le mot ne change pas quand
        # k varie dans la plage usuelle — un S- a 3.7 U n'est pas une
        # affaire de couverture.
        g = self.row()["extra"]["gum"]
        self.assertEqual(g["decide"], "U")
        self.assertEqual(g["k"], 1.0)
        self.assertAlmostEqual(g["U"], 54.037024344425184, places=12)
        for k in (1.0, 2.0, 3.0):
            self.assertGreaterEqual(self.row()["delta"], k * g["uc"])
        # La ligne B portee recombine au seuil declare :
        lines = [{"name": "CMD3_2pi", "type": "B", "u": 42.0},
                 {"name": "premoy_2pi", "type": "B", "u": 34.0}]
        self.assertAlmostEqual(u_c(lines), 54.037024344425184, places=12)

    def test_hvp_pipi_identification_multiple_declaree(self) -> None:
        # La moyenne pre-CMD-3 est KLOE-dominee : l'identification est
        # ecrite dans la note du runner et du contact — jamais choisie
        # apres coup (honnêtete O15/AMU). Le contact ne porte pas de
        # valeur KLOE seule : c'est une propriete de la table, verrou.
        r = self.row()
        self.assertIn("KLOE", r["extra"]["ansatz"])
        t = load_table("hvp_pipi_cmd3_LITERATURE.json")
        p = t["params"]
        self.assertNotIn("a_kloe_seul", p)


if __name__ == "__main__":
    unittest.main(verbosity=2)
