#!/usr/bin/env python3
"""Contact H0 bas-z LITERATURE ancré Planck — Pantheon+ (Brout 2022).

Chronologie du gel :
1. Protocole écrit avant toute exécution : H0-HZ-SNE-PROTOCOLE-
   LITERATURE.md (§5) — règle gelée du contact DEMO réutilisée telle
   quelle : mu_loc = rms des résidus mu_pred(z_i ; H(z) fabrication
   Planck déclarée 67,4, Omega gelés) - mu_obs,i ; mu_ref = 0 ;
   theta = sigma bins déclarée = 0,02756 mag, gelée AVANT le run.
   Interdit : ajuster bins, dispersion, Omega ou theta.
2. Extraction déclarée (extraction_literature.py) : Table 7 de Brout
   et al. 2022 (VizieR J/ApJ/938/110), 1701 light curves dédoublonnées
   par nom normalisé (1542 SNe), fenêtre zHD [0,01 ; 0,15) = 598 SNe,
   8 bins équipopulaires à moyenne arithmétique déclarée, amplitude
   ancrée Planck par transposition EXACTE (mu = mBcorr + 5*log10(H0_A)
   - K_B, K_B = 28,52698 mesuré à la forme gelée). Validation croisée :
   std(A - mBcorr) = 0,160 mag à z >= 0,01 vs rms ~0,15 publié.
   Dettes écrites dans la table : compression, ancrage, indépendance
   (miroir du contact SH0ES), vitesses, miroir.
3. Estimation pré-run honnête : courbe Planck = ancrage, résidu =
   bruit réalisé des bins, delta attendu ~0,02-0,04 — zone P [theta,
   2theta] au cheveu ; suspense réel, le bruit réalisé décide.
4. Premier run : mot découvert : **S-**, delta = 0,0695 mag. Le bruit
   réalisé des 8 bins (hétérogénéité surveys, vitesses particulières
   résiduelles, écarts de forme Omega gelés vs données) dépasse 2*theta
   = 0,0551 : l'estimation P était fausse du côté du bruit, comme
   annoncé possible. La carte dit : les bins Pantheon+ ancrés Planck
   ne passent pas par la courbe Planck à hauteur du bruit déclaré.
5. Figé : mot et valeur à 12 décimales dans ce test.
"""

from __future__ import annotations

import math
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from mvcg.registers import run_registers  # noqa: E402
from mvcg.tables import load_table  # noqa: E402


def _rms(t: dict) -> float:
    p = t["params"]
    om, ol, c = float(p["Omega_m"]), float(p["Omega_L"]), float(p["c_km_s"])
    res = []
    for z, mu_obs in t["bins"]:
        import numpy as np
        g = np.linspace(1e-8, z, 2000)
        chi = np.trapezoid(1.0 / np.sqrt(om * (1.0 + g) ** 3 + ol), g)
        dl = (1.0 + z) * chi * c / 67.4
        res.append((5.0 * math.log10(dl) + 25.0 - mu_obs) ** 2)
    return float(math.sqrt(sum(res) / len(res)))


class TestOpenContactHzLitPlanck(unittest.TestCase):
    def row(self) -> dict:
        by = {r["id"]: r for r in run_registers()["rows"]}
        return by["H0_Hz_SNe_LOWZ_LIT_PLANCK"]

    def test_hz_lit_planck_word_frozen(self) -> None:
        r = self.row()
        self.assertEqual(r["verdict"], "S-")  # mot du premier run, figé
        self.assertEqual(r["statut"], "ouverte")
        self.assertIsNone(r["expected"])
        self.assertGreater(r["delta"], 2.0 * r["theta"])  # 0,0695 > 0,0551
        self.assertAlmostEqual(r["mu_loc"], 0.06949833902331774, places=12)

    def test_hz_lit_planck_gum_carried_not_used(self) -> None:
        g = self.row()["extra"]["gum"]
        self.assertEqual(g["decide"], "theta")
        self.assertAlmostEqual(g["uc"], 0.02756, places=12)
        self.assertAlmostEqual(g["U"], 0.05512, places=12)

    def test_hz_lit_planck_reproducible_from_table(self) -> None:
        t = load_table("hz_sne_LOWZ-LITERATURE-Planck.json")
        self.assertAlmostEqual(_rms(t), self.row()["mu_loc"], places=12)
        self.assertEqual(len(t["bins"]), 8)
        self.assertAlmostEqual(float(t["sigma_mag"]), 0.02756, places=12)


if __name__ == "__main__":
    unittest.main(verbosity=2)
