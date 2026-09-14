#!/usr/bin/env python3
"""Contact H0 bas-z LITERATURE ancré SH0ES — Pantheon+ (Brout 2022).

Chronologie du gel :
1. Protocole écrit avant toute exécution : H0-HZ-SNE-PROTOCOLE-
   LITERATURE.md (§5) — règle gelée du contact DEMO réutilisée telle
   quelle : mu_loc = rms des residus mu_pred(z_i ; H(z) fabrication
   Planck déclarée 67,4, Omega gelés) - mu_obs,i ; mu_ref = 0 ;
   theta = sigma bins déclarée = 0,02756 mag, gelée AVANT le run.
   Interdit : ajuster bins, dispersion, Omega ou theta.
2. Extraction déclarée (extraction_literature.py) : Table 7 de Brout
   et al. 2022 (VizieR J/ApJ/938/110), 1701 light curves dédoublonnées
   par nom normalisé (1542 SNe), fenêtre zHD [0,01 ; 0,15) = 598 SNe,
   8 bins équipopulaires à moyenne arithmétique déclarée, amplitude
   ancrée SH0ES (H0 = 73,04) par transposition EXACTE
   (mu = mBcorr + 5*log10(H0_A) - K_B, K_B = 28,52698 mesuré à la
   forme gelée). Dette d'indépendance : donnée et levier H0<-SH0ES
   non indépendants (pendant Landau). Dette de miroir : carte exacte-
   ment symétrique au contact ancré Planck, mêmes bins, deux dettes.
3. Estimation pré-run honnête : résidu moyen = +5*log10(73,04/67,4)
   = +0,1745 mag quasi constant (exact à Omega gelés identiques) ;
   delta ≈ sqrt(sigma² + 0,1745²) >> 2*theta = 0,0551 : S- attendu
   SANS suspense.
4. Premier run : mot découvert : **S-**, delta = 0,2314 mag —
   estimation confirmée. La courbe Planck manque les bins ancrés
   SH0ES de 0,231 mag en rms : la tension H0 relue par les SNe
   binnées, dans la carte de l'échelle locale.
5. Figé : mot et valeur à 12 décimales dans ce test.
"""

from __future__ import annotations

import math
import sys
import unittest
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from mvcg.registers import run_registers  # noqa: E402
from mvcg.tables import load_table  # noqa: E402


def _rms(t: dict) -> float:
    p = t["params"]
    om, ol, c = float(p["Omega_m"]), float(p["Omega_L"]), float(p["c_km_s"])
    res = []
    for z, mu_obs in t["bins"]:
        g = np.linspace(1e-8, z, 2000)
        chi = np.trapezoid(1.0 / np.sqrt(om * (1.0 + g) ** 3 + ol), g)
        dl = (1.0 + z) * chi * c / 67.4
        res.append((5.0 * math.log10(dl) + 25.0 - mu_obs) ** 2)
    return float(math.sqrt(sum(res) / len(res)))


class TestOpenContactHzLitSh0es(unittest.TestCase):
    def row(self) -> dict:
        by = {r["id"]: r for r in run_registers()["rows"]}
        return by["H0_Hz_SNe_LOWZ_LIT_SH0ES"]

    def test_hz_lit_sh0es_word_frozen(self) -> None:
        r = self.row()
        self.assertEqual(r["verdict"], "S-")  # mot du premier run, figé
        self.assertEqual(r["statut"], "ouverte")
        self.assertIsNone(r["expected"])
        self.assertGreater(r["delta"], 2.0 * r["theta"])  # 0,231 > 0,055
        self.assertAlmostEqual(r["mu_loc"], 0.23136304438473587, places=12)

    def test_hz_lit_sh0es_gum_carried_not_used(self) -> None:
        g = self.row()["extra"]["gum"]
        self.assertEqual(g["decide"], "theta")
        self.assertAlmostEqual(g["uc"], 0.02756, places=12)
        self.assertAlmostEqual(g["U"], 0.05512, places=12)

    def test_hz_lit_sh0es_reproducible_from_table(self) -> None:
        t = load_table("hz_sne_LOWZ-LITERATURE-SH0ES.json")
        self.assertAlmostEqual(_rms(t), self.row()["mu_loc"], places=12)
        self.assertEqual(len(t["bins"]), 8)

    def test_hz_lit_miroir_exact_avec_planck(self) -> None:
        # Transposition exacte à Omega gelés identiques : mu_obs
        # décroît avec H0 d'ancrage (d_L ∝ 1/H0), donc mp - ms =
        # +5*log10(73,04/67,4) = +0,1745 mag sur chaque bin. Le gel
        # du miroir est une propriété de la déclaration, pas un
        # résultat.
        tp = load_table("hz_sne_LOWZ-LITERATURE-Planck.json")
        ts = load_table("hz_sne_LOWZ-LITERATURE-SH0ES.json")
        shift = 5.0 * math.log10(73.04 / 67.4)
        for (zp, mp), (zs, ms) in zip(tp["bins"], ts["bins"]):
            self.assertAlmostEqual(zp, zs, places=12)
            # tables arrondies à 6 décimales : le miroir tient à 1e-5
            # mag (exact en réel, par construction de la transposition)
            self.assertAlmostEqual(mp - ms, shift, places=5)


if __name__ == "__main__":
    unittest.main(verbosity=2)
