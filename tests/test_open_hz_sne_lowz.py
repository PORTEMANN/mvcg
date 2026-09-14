#!/usr/bin/env python3
"""Contact H0 bas-z — la courbe H(z) déclarée contre les bins SNe.

Chronologie du gel :
1. Protocole écrit et gelé avant toute exécution : règle déclarée —
   mu_loc = rms_i( mu_pred(z_i ; H(z) fabrication Planck déclarée,
   Omega gelés) - mu_obs,i ), mu_ref = 0 (la courbe passe par les
   bins). θ = 0,05 mag abs gelé avant run ; GUM : une ligne B
   (dispersion des bins), decide=theta — le budget est porté, pas
   utilisé. Extract = DEMO-2026 SYNTHÉTIQUE : 8 bins bas-z, fiducial
   H0 = 70 entre les deux fabrications, seed numpy 20260913 gelé ;
   rien ne peut être retouché après coup. Dette écrite dans la
   table : cette carte valide le protocole, elle ne dit rien de
   l'univers réel ; la table LITERATURE reste à déclarer.
   Estimation pré-run honnête : δ ≈ 0,096 — zone P au bord S−,
   le bruit des 8 bins décide. Suspense maximal.
2. Premier run : mot découvert : **S-**, δ = 0,1173 mag (le bruit
   réalisé a renforcé l'écart systématique Planck-vs-70).
3. Figé : mot dans ce test.
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


def _rms(t: dict, h0: float) -> float:
    p = t["params"]
    om, ol, c = float(p["Omega_m"]), float(p["Omega_L"]), float(p["c_km_s"])
    res = []
    for z, mu_obs in t["bins"]:
        g = np.linspace(1e-8, z, 2000)
        chi = np.trapezoid(1.0 / np.sqrt(om * (1.0 + g) ** 3 + ol), g)
        dl = (1.0 + z) * chi * c / h0
        res.append((5.0 * math.log10(dl) + 25.0 - mu_obs) ** 2)
    return float(np.sqrt(np.mean(res)))


class TestOpenContactHzSneLowz(unittest.TestCase):
    def row(self) -> dict:
        by = {r["id"]: r for r in run_registers()["rows"]}
        return by["H0_Hz_SNe_LOWZ_DEMO"]

    def test_hz_word_frozen(self) -> None:
        r = self.row()
        self.assertEqual(r["verdict"], "S-")  # mot du premier run, figé
        self.assertEqual(r["statut"], "ouverte")
        self.assertIsNone(r["expected"])
        self.assertGreater(r["delta"], 2.0 * r["theta"])  # 0,117 > 0,10
        self.assertAlmostEqual(r["mu_loc"], 0.11727000773640141, places=12)

    def test_hz_sensitivity_data_not_tuned(self) -> None:
        # La carte encode bien la réponse par construction : au
        # fiducial déclaré (H0=70), le rms retombe à ~sigma des bins
        # (0,0506 — P au cheveu du S+, car theta gelé = dispersion
        # déclarée : un S+ exigerait plus de bins). Le S- de la
        # fabrication Planck est plus du double : il mesure l'écart
        # de la fabrication, pas un runner brouillé. Et les bins ne
        # sont pas ajustés sur la référence : les déplacer déplace mu.
        t = load_table("hz_sne_LOWZ-DEMO-2026.json")
        self.assertAlmostEqual(_rms(t, 70.0), 0.050646590812412004, places=12)
        self.assertLess(_rms(t, 70.0), 0.5 * _rms(t, 67.4))
        self.assertAlmostEqual(_rms(t, 67.4), self.row()["mu_loc"], places=12)
        shifted = [[z, m + 0.5] for z, m in t["bins"]]
        t2 = {**t, "bins": shifted}
        self.assertGreater(abs(_rms(t2, 67.4) - self.row()["mu_loc"]), 0.1)

    def test_hz_gum_carried_not_used(self) -> None:
        # Budget porté : decide=theta — U = 2 theta exactement, le
        # seuil reste le theta gelé.
        g = self.row()["extra"]["gum"]
        self.assertEqual(g["decide"], "theta")
        self.assertAlmostEqual(g["uc"], 0.05, places=12)
        self.assertAlmostEqual(g["U"], 0.1, places=12)


if __name__ == "__main__":
    unittest.main(verbosity=2)
