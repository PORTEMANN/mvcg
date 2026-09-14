#!/usr/bin/env python3
"""Balayage calibré (chantier A2) — l'invariance d'unités à même
étalonnage, figée d'abord sur les 46 contacts, étendue à 48 (V2, 2026-09-14).

Contexte : `street_sweep` historique juge au θ seul et conserve, par
gel, les « deux instruments » de CKM / HVP / HLbL (tests dédiés dans
test_verdicts_online.py — ne pas y toucher). La campagne A2 a montré
que ces divergences sont la comparaison de deux seuils, pas un effet
d'unités. `street_sweep_calibrated` rejoue le balayage au seuil gelé
du contact (U si decide=U, θ sinon) : là, et seulement là, le mot doit
être identique sous les quatre paquets pour CHAQUE contact du registre.

Propriétés figées :
- 46/46 au gel A2, puis 48/48 après V2 : mot calibré identique au mot
  home sous les 4 paquets ;
- zéro units_kill : aucun paquet n'est illicite pour une dimension
  portée par le registre ;
- CKM porte thr = U = 0,0014 (étalonnage U déclaré, k = 2) — la
  valeur qui séparait les deux instruments.
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from mvcg.registers import CONTACTS  # noqa: E402
from mvcg.verdict_register import street_sweep_calibrated  # noqa: E402


class TestSweepCalibrated(unittest.TestCase):
    def test_all_contacts_invariant_at_same_calibration(self) -> None:
        self.assertEqual(len(CONTACTS), 63)  # 56 + Rydberg voie 2 (campagne croisee, 2026-09-14) + O17 H2 anharmonique (tare de declaration, 2026-09-14) + O18 H2 tare de lecture (pendant d'O17, 2026-09-14) + P31 Lamb x3 (Dirac dette historique / Mohr P au cheveu / Erickson S-, chantier atome, 2026-09-14) + P32 Lamb moderne (la dette se ferme : QED reevaluee S+ sur le temoin commun, 2026-09-14)
        for c in CONTACTS:
            st = street_sweep_calibrated(c.id)
            licites = [r for r in st["rows"] if not r["units_kill"]]
            self.assertEqual(len(licites), 4,
                             f"{c.id}: units_kill inattendu en balayage calibré")
            for r in licites:
                self.assertEqual(r["verdict"], st["home_verdict"],
                                 f"{c.id}: mot {r['verdict']} en packet "
                                 f"{r['packet']} != home {st['home_verdict']} "
                                 "à même étalonnage")
                self.assertAlmostEqual(r["thr"], st["thr"], places=15)

    def test_ckm_calibrated_carries_u_threshold(self) -> None:
        # Le seuil qui séparait les deux instruments : U = 0,0014
        # (decide=U, k=2). À même étalonnage, chaque paquet rejoint
        # le mot home — on compare au registre live, sans écrire le
        # mot ici (garde anti-tautologie de reproduce : jamais de mot
        # voisin dans un fichier de classification).
        st = street_sweep_calibrated("CKM_Row1_Unitarity")
        self.assertEqual(st["calibration"], "U")
        self.assertAlmostEqual(st["thr"], 0.0014, places=12)
        for r in st["rows"]:
            self.assertEqual(r["verdict"], st["home_verdict"])
            self.assertAlmostEqual(r["delta"], 0.0016000000000000458,
                                   places=12)

    def test_g2_calibrated_restores_home_words(self) -> None:
        # HVP et HLbL : à même étalonnage, le balayage rejoint le mot
        # home — les divergences historiques n'étaient que le changement
        # de seuil, jamais un effet d'unités. Mots comparés au live,
        # jamais écrits ici (même garde anti-tautologie).
        for cid in ("HVP_LO_lat_vs_ee", "HLbL_lat_vs_pheno"):
            st = street_sweep_calibrated(cid)
            self.assertEqual(st["calibration"], "U")
            for r in st["rows"]:
                self.assertEqual(r["verdict"], st["home_verdict"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
