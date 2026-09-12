#!/usr/bin/env python3
"""Le casier compare les modes (D) sans jamais mentir sur les pesées.

Cartes « pesé » dérivées du registre : une carte qui affirmerait un mot
absent du registre ferait échouer ce test. Candidats « sans μ » : des
étiquettes qui ne pèsent rien — et ne doivent rien afficher.
"""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from mvcg.casier import cards, index  # noqa: E402
from mvcg.registers import run_registers  # noqa: E402


class TestCasier(unittest.TestCase):
    def test_no_score_and_principle(self) -> None:
        idx = index()
        self.assertIn("pas de score SM", idx["warning"])
        self.assertIn("sans μ = étiquette", idx["warning"])
        self.assertIn("dérivé du registre", idx["warning"])

    def test_weighed_cards_match_register(self) -> None:
        # Aucune étiquette ne ment : chaque carte « pesé » est une ligne
        # réelle du registre, avec le mot réel de cette ligne.
        rows = {r["id"]: r for r in run_registers()["rows"]}
        weighed = [c for c in cards() if c["note"] == "pesé"]
        self.assertEqual(len(weighed), len(rows))
        for c in weighed:
            self.assertIn(c["id"], rows)
            self.assertEqual(c["verdict"], rows[c["id"]]["verdict"])

    def test_candidates_weigh_nothing(self) -> None:
        # Un candidat « sans μ » ne doit pas exister dans le registre :
        # s'il y entre, il devient une carte pesée (dérivée), pas un
        # candidat déclaré.
        ids = {r["id"] for r in run_registers()["rows"]}
        for c in cards():
            if c["note"] == "sans μ":
                self.assertNotIn(c["id"], ids)
                self.assertNotIn("verdict", c)

    def test_modes_are_comparable(self) -> None:
        # La raison d'être du casier : comparer les modes entre eux.
        # Même machine, D différents — les familles couvrent plusieurs
        # matières et les mots couvrent les trois couleurs.
        cs = cards()
        families = {c["family"] for c in cs}
        self.assertGreaterEqual(len(families), 5)
        mots = {c["verdict"] for c in cs if c["note"] == "pesé"}
        self.assertEqual(mots, {"S+", "P", "S-"})


if __name__ == "__main__":
    unittest.main(verbosity=2)
