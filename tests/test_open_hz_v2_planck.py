#!/usr/bin/env python3
"""Contact H0 bas-z V2, courbe Planck posée — Pantheon+ MU_SH0ES natif.

Chronologie du gel :
1. Protocole écrit avant toute exécution : H0-HZ-SNE-V2-PROTOCOLE.md —
   règle déclarée : mêmes 8 bins équipopulaires que V1 (fenêtre zHD
   [0,01 ; 0,15), 598 SNe, même règle de dispersion), amplitude
   MU_SH0ES telle que publiée dans la release Pantheon+ (ancrage natif,
   dette de forme +0,049 mag de la campagne 7 supprimée). Courbe posée
   par le contact : mu_pred(z ; H0_courbe déclaré 67,4, Omega gelés
   0,315/0,685), H0 lu dans la table (pas en dur). mu_loc = rms des
   résidus sur 8 bins, mu_ref = 0 ; theta = sigma bins déclarée =
   0,027737 mag, gelée AVANT le run. Interdit : ajuster bins,
   dispersion, Omega, theta ou le H0 de courbe après coup.
2. Estimation pré-run honnête : résidu moyen ~ +0,1766 mag quasi
   constant (miroir exact du contact V1 ancré SH0ES), delta ~ 0,178 >>
   2*theta = 0,055474 : S- attendu SANS suspense.
3. Premier run : mot découvert : **S-**, delta = 0,178285002738 mag.
   Conforme à l'estimation. La carte dit : poser la courbe Planck sur
   les distances natives SH0ES décale les bins de plus de 6 theta —
   la tension H0 se lit déjà dans les modules de distance bas-z, au-
   delà du bruit déclaré des bins.
4. Figé : mot et valeur à 12 décimales dans ce test.
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


def _rms(t: dict, h0: float) -> float:
    p = t["params"]
    om, ol, c = float(p["Omega_m"]), float(p["Omega_L"]), float(p["c_km_s"])
    res = []
    for z, mu_obs in t["bins"]:
        import numpy as np
        g = np.linspace(1e-8, z, 2000)
        chi = np.trapezoid(1.0 / np.sqrt(om * (1.0 + g) ** 3 + ol), g)
        dl = (1.0 + z) * chi * c / h0
        res.append((5.0 * math.log10(dl) + 25.0 - mu_obs) ** 2)
    return float(math.sqrt(sum(res) / len(res)))


class TestOpenContactHzV2Planck(unittest.TestCase):
    def row(self) -> dict:
        by = {r["id"]: r for r in run_registers()["rows"]}
        return by["H0_Hz_SNe_LOWZ_V2_PLANCK"]

    def test_hz_v2_planck_word_frozen(self) -> None:
        r = self.row()
        self.assertEqual(r["verdict"], "S-")  # mot du premier run, figé
        self.assertEqual(r["statut"], "ouverte")
        self.assertIsNone(r["expected"])
        self.assertGreater(r["delta"], 2.0 * r["theta"])  # 0,1783 > 0,0555
        self.assertAlmostEqual(r["mu_loc"], 0.17828500273805192, places=12)

    def test_hz_v2_planck_gum_carried_not_used(self) -> None:
        g = self.row()["extra"]["gum"]
        self.assertEqual(g["decide"], "theta")
        self.assertAlmostEqual(g["uc"], 0.027737, places=12)
        self.assertAlmostEqual(g["U"], 0.055474, places=12)

    def test_hz_v2_planck_reproducible_from_table(self) -> None:
        t = load_table("hz_sne_LOWZ-V2-MUSH0ES.json")
        h0 = float(t["params"]["H0_courbe_PLANCK_km_s_Mpc"])
        self.assertAlmostEqual(_rms(t, h0), self.row()["mu_loc"], places=12)
        self.assertEqual(len(t["bins"]), 8)
        self.assertAlmostEqual(float(t["sigma_mag"]), 0.027737, places=12)
        self.assertEqual(t["vintage"], "V2-MUSH0ES-PantheonPlus-release")


if __name__ == "__main__":
    unittest.main(verbosity=2)
