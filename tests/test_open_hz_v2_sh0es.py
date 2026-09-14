#!/usr/bin/env python3
"""Contact H0 bas-z V2, courbe SH0ES posée — Pantheon+ MU_SH0ES natif.

Chronologie du gel :
1. Protocole écrit avant toute exécution : H0-HZ-SNE-V2-PROTOCOLE.md —
   mêmes 8 bins, amplitude MU_SH0ES native (ancrage natif, dette de
   forme supprimée). Courbe posée par le contact : mu_pred(z ; H0_courbe
   déclaré 73,04, Omega gelés 0,315/0,685), H0 lu dans la table. mu_loc
   = rms des résidus sur 8 bins, mu_ref = 0 ; theta = 0,027737 mag
   gelée AVANT le run. Interdit : ajuster quoi que ce soit après coup.
2. Estimation pré-run honnête : résidu = bruit réalisé des bins autour
   de la courbe de leur propre fabrication, rms ~ 0,0249, delta/theta
   ~ 0,897 < 1 : S+ attendu AU CHEVEU — le bruit réalisé décide.
3. Premier run : mot découvert : **S+**, delta = 0,024876389328 mag
   (delta/theta = 0,8969). Conforme à l'estimation, au cheveu près.
   La carte dit : les distances natives SH0ES passent par la courbe
   SH0ES à hauteur du bruit déclaré des bins — calibration interne
   cohérente, exactement ce qu'attend une fabrication qui s'auto-
   étalonne. Le suspense portait sur le bruit réalisé ; il est tombé
   juste sous theta.
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


class TestOpenContactHzV2Sh0es(unittest.TestCase):
    def row(self) -> dict:
        by = {r["id"]: r for r in run_registers()["rows"]}
        return by["H0_Hz_SNe_LOWZ_V2_SH0ES"]

    def test_hz_v2_sh0es_word_frozen(self) -> None:
        r = self.row()
        self.assertEqual(r["verdict"], "S+")  # mot du premier run, figé
        self.assertEqual(r["statut"], "ouverte")
        self.assertIsNone(r["expected"])
        self.assertLessEqual(r["delta"], r["theta"])  # 0,0249 <= 0,0277
        self.assertAlmostEqual(r["delta"] / r["theta"], 0.8968666160007644,
                               places=12)
        self.assertAlmostEqual(r["mu_loc"], 0.024876389328013206, places=12)

    def test_hz_v2_sh0es_gum_carried_not_used(self) -> None:
        g = self.row()["extra"]["gum"]
        self.assertEqual(g["decide"], "theta")
        self.assertAlmostEqual(g["uc"], 0.027737, places=12)
        self.assertAlmostEqual(g["U"], 0.055474, places=12)

    def test_hz_v2_sh0es_reproducible_from_table(self) -> None:
        t = load_table("hz_sne_LOWZ-V2-MUSH0ES.json")
        h0 = float(t["params"]["H0_courbe_SH0ES_km_s_Mpc"])
        self.assertAlmostEqual(_rms(t, h0), self.row()["mu_loc"], places=12)
        self.assertEqual(len(t["bins"]), 8)
        self.assertAlmostEqual(float(t["sigma_mag"]), 0.027737, places=12)
        self.assertEqual(t["vintage"], "V2-MUSH0ES-PantheonPlus-release")


if __name__ == "__main__":
    unittest.main(verbosity=2)
