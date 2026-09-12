#!/usr/bin/env python3
"""Contact ouvert O3 — bande D du graphite par chaîne 1D à forces égales.

Chronologie du gel :
1. Protocole écrit et gelé avant toute exécution : table vintage
   (carbon_raman_LITERATURE-2018) ; règle déclarée — le graphite est
   une chaîne 1D diatomique de carbone, bande G = mode optique au
   centre de zone (ω² = 2(k1+k2)/m), bande D = bord de zone
   (ω² = 2·max(k1,k2)/m), transfert k2 := k1 (égalisation) donc
   D = G/√2 ; θ = 0,10 figé avant run (tolérance « entre labo » ×
   modèle 1D grossier) ; référence = bande D observée du graphite,
   1350 cm⁻¹. Anti-tautologie : la bande D observée ne participe
   jamais au calcul — seule G pilote la prédiction.
2. Premier run : mot = P (δ ≈ 17,24 %, zone 0,10 < δ ≤ 0,20).
   Découvert, pas choisi.
3. Ce test fixe le mot, comme pour tout contact du registre.

Le levier k<-desegaliser : D/G = sqrt(max(1,r)/(1+r)) avec r = k2/k1 —
minimal (1/√2) exactement à r = 1, monotone en s'éloignant de 1 dans
les deux sens, symétrique r ↔ 1/r. L'égalisation est donc le pire cas.
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


def _d_over_g(r: float) -> float:
    """Rapport D/G de la chaîne diatomique : sqrt(max(1,r)/(1+r))."""
    return math.sqrt(max(1.0, r) / (1.0 + r))


def _d_pred_from_g(g_cm: float, r: float) -> float:
    return g_cm * _d_over_g(r)


class TestOpenContactO3(unittest.TestCase):
    def row(self) -> dict:
        by = {r["id"]: r for r in run_registers()["rows"]}
        return by["O3_Carbon_D_Raman"]

    def test_o3_word_frozen(self) -> None:
        r = self.row()
        self.assertEqual(r["verdict"], "P")  # mot du premier run, figé
        self.assertEqual(r["statut"], "ouverte")
        self.assertIsNone(r["expected"])  # aucun mot attendu au gel
        self.assertGreater(r["delta"], r["theta"])  # 17,24 % > 10 %
        self.assertLessEqual(r["delta"], 2.0 * r["theta"])  # ... ≤ 20 %
        self.assertAlmostEqual(r["mu_loc"], 1117.228714274745, places=6)

    def test_o3_anti_tautology_d_never_in_calc(self) -> None:
        t = load_table("carbon_raman_LITERATURE-2018.json")
        g_obs = float(t["bands"]["graphite_G_cm-1"])
        d_pred = _d_pred_from_g(g_obs, 1.0)
        self.assertAlmostEqual(d_pred, self.row()["mu_loc"], places=9)
        # La bande cible D est à plus de 10 % (hors zone S+) :
        self.assertGreater(abs(d_pred / t["bands"]["graphite_D_cm-1"] - 1.0), 0.10)
        # Structurelle : retirer D (et l'amorphe) ne change rien.
        bands_sans_d = {k: v for k, v in t["bands"].items()
                        if "D" not in k and "amorph" not in k}
        self.assertNotIn("graphite_D_cm-1", bands_sans_d)
        self.assertAlmostEqual(
            _d_pred_from_g(float(bands_sans_d["graphite_G_cm-1"]), 1.0),
            d_pred, places=12,
        )

    def test_o3_lever_k_desegaliser(self) -> None:
        # r = k2/k1 ; D/G minimal à r = 1 (égalisation = pire cas),
        # monotone et symétrique de part et d'autre.
        g = 1580.0
        d_eq = _d_pred_from_g(g, 1.0)
        d_low = _d_pred_from_g(g, 0.5)
        d_high = _d_pred_from_g(g, 2.0)
        self.assertAlmostEqual(d_low, d_high, places=12)  # symétrie r <-> 1/r
        self.assertGreater(d_low, d_eq)
        self.assertGreater(d_high, d_eq)
        # Monotonie sur [1, inf) : s'éloigner de 1 rapproche D de G.
        self.assertLess(d_eq, _d_pred_from_g(g, 4.0))
        self.assertLess(_d_pred_from_g(g, 4.0), _d_pred_from_g(g, 9.0))
        self.assertAlmostEqual(_d_pred_from_g(g, 1.0), self.row()["mu_loc"], places=9)


if __name__ == "__main__":
    unittest.main(verbosity=2)
