#!/usr/bin/env python3
"""Contact ouvert O5 — vitesse du son d'un condensat de Bose (Bogolioubov).

Chronologie du gel :
1. Protocole écrit et gelé avant toute exécution : table vintage
   (bec_sound_LITERATURE-2018) ; règle déclarée — c = sqrt(g n / m),
   g = 4 pi hbar^2 a_s / m (régime dilué, T = 0) ; θ = 0,05 figé avant
   run (accord inter-labo vitesse du son + incertitude de densité du
   nuage inhomogène) ; référence = vitesse observée 1,1 mm/s. Le
   paramètre le moins contraint (densité n = 3e19 m^-3) est documenté
   AVANT le run — c'est là que vit le levier. Anti-tautologie : la
   vitesse observée ne participe jamais au calcul.
2. Premier run : mot = P (δ ≈ 6,17 %, θ = 5 %). Découvert, pas choisi.
3. Ce test fixe le mot, comme pour tout contact du registre.

Le levier n<-profil : c ∝ sqrt(n) — monotone ; le S+ est fragile en
densité (+3 % suffisent), ce qui est la physique attendue du contact.
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

HBAR = 1.054571817e-34  # J s (h exact / 2 pi)
AMU = 1.66053906660e-27  # kg, déclarée locale


def _c_sound(m_u: float, a_s_nm: float, n_m3: float) -> float:
    m = m_u * AMU
    a_s = a_s_nm * 1e-9
    return math.sqrt(4.0 * math.pi * HBAR**2 * a_s * n_m3 / m**2)


class TestOpenContactO5(unittest.TestCase):
    def row(self) -> dict:
        by = {r["id"]: r for r in run_registers()["rows"]}
        return by["O5_BEC_Sound"]

    def test_o5_word_frozen(self) -> None:
        r = self.row()
        self.assertEqual(r["verdict"], "P")  # mot du premier run, figé
        self.assertEqual(r["statut"], "ouverte")
        self.assertIsNone(r["expected"])  # aucun mot attendu au gel
        self.assertGreater(r["delta"], r["theta"])  # 6,17 % > 5 %
        self.assertLessEqual(r["delta"], 2.0 * r["theta"])  # ... ≤ 10 %
        self.assertAlmostEqual(r["mu_loc"], 0.0010321135921727029, places=12)

    def test_o5_anti_tautology_c_obs_never_in_calc(self) -> None:
        t = load_table("bec_sound_LITERATURE-2018.json")
        p = t["params"]
        c = _c_sound(float(p["mass_87Rb_u"]), float(p["a_s_100a0_nm"]),
                     float(p["n_cloud_m-3"]))
        self.assertAlmostEqual(c, self.row()["mu_loc"], places=15)
        # La vitesse observée est à plus de 5 % (hors zone S+) :
        self.assertGreater(abs(c / p["c_observed_m_s"] - 1.0), 0.05)
        # Structurelle : retirer la vitesse observée ne change rien.
        params_sans_obs = {k: v for k, v in p.items() if k != "c_observed_m_s"}
        self.assertNotIn("c_observed_m_s", params_sans_obs)
        self.assertAlmostEqual(
            _c_sound(float(params_sans_obs["mass_87Rb_u"]),
                     float(params_sans_obs["a_s_100a0_nm"]),
                     float(params_sans_obs["n_cloud_m-3"])),
            c, places=15,
        )

    def test_o5_lever_n_profil(self) -> None:
        # c ∝ sqrt(n) : monotone croissante, concave.
        args = (86.909187, 5.291772)
        self.assertLess(_c_sound(*args, 2.5e19), _c_sound(*args, 3.0e19))
        self.assertLess(_c_sound(*args, 3.0e19), _c_sound(*args, 3.5e19))
        # Demi-incrément : c(n*4) = 2 c(n) — échelle sqrt exacte.
        self.assertAlmostEqual(_c_sound(*args, 1.2e20),
                               2.0 * _c_sound(*args, 3.0e19), places=15)
        # Point de bascule vers S+ documenté : c = 1,048 mm/s (δ = 5 %)
        c_ref = 0.0011
        n_sp = 3e19 * (0.95 * c_ref / _c_sound(*args, 3.0e19)) ** 2
        self.assertAlmostEqual(_c_sound(*args, n_sp), 0.95 * c_ref, places=15)
        self.assertGreater(n_sp, 3.0e19)  # il faut densifier ~3 %
        self.assertAlmostEqual(_c_sound(*args, 3.0e19),
                               self.row()["mu_loc"], places=15)


if __name__ == "__main__":
    unittest.main(verbosity=2)
