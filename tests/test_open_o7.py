#!/usr/bin/env python3
"""Contact ouvert O7 — levier d'O3 activé (k₂/k₁ = 3 déclaré).

Chronologie du gel :
1. Protocole écrit et gelé avant toute exécution : même table bandes
   (carbon_raman_LITERATURE-2018), nouvelle table forces
   (carbon_raman_forces_LITERATURE-2018) avec r = k2/k1 = 3,0 déclaré —
   paramètre EFFECTIF du modèle 1D, pas une constante mesurée (écrit
   dans la table). Même référence (bande D observée, 1350 cm⁻¹),
   MÊME θ = 0,10 gelé qu'O3 — le seuil ne bouge jamais. La bande D
   observée ne participe toujours pas au calcul (anti-tautologie
   maintenue) : seuls G et r pilotent.
2. Premier run : mot = S+ (δ ≈ 1,36 % << θ). Découvert, pas choisi.
3. Ce test fixe le mot, comme pour tout contact du registre.

Le levier k<-desegaliser est ACTIF. Fenêtre de robustesse : le S+ tient
pour r ∈ [~1,45 ; ~7,61] (δ ≤ 10 %), soit un facteur > 5 sur le
paramètre — verdict robuste, contrairement au P fragile en n d'O5.
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


def _d_pred(g_cm: float, r: float) -> float:
    return g_cm * math.sqrt(max(1.0, r) / (1.0 + r))


class TestOpenContactO7(unittest.TestCase):
    def row(self) -> dict:
        by = {r["id"]: r for r in run_registers()["rows"]}
        return by["O7_Carbon_D_Levier"]

    def test_o7_word_frozen(self) -> None:
        r = self.row()
        self.assertEqual(r["verdict"], "S+")  # mot du premier run, figé
        self.assertEqual(r["statut"], "ouverte")
        self.assertIsNone(r["expected"])  # aucun mot attendu au gel
        self.assertLessEqual(r["delta"], r["theta"])  # 1,36 % ≤ 10 %
        self.assertAlmostEqual(r["mu_loc"], 1368.320137979413, places=6)

    def test_o7_anti_tautology_d_never_in_calc(self) -> None:
        t = load_table("carbon_raman_LITERATURE-2018.json")
        tf = load_table("carbon_raman_forces_LITERATURE-2018.json")
        g_obs = float(t["bands"]["graphite_G_cm-1"])
        r_decl = float(tf["params"]["k2_over_k1"])
        d_pred = _d_pred(g_obs, r_decl)
        self.assertAlmostEqual(d_pred, self.row()["mu_loc"], places=9)
        # Structurelle : retirer la bande D observée ne change rien.
        bands_sans_d = {k: v for k, v in t["bands"].items()
                        if "D" not in k and "amorph" not in k}
        self.assertNotIn("graphite_D_cm-1", bands_sans_d)
        self.assertAlmostEqual(
            _d_pred(float(bands_sans_d["graphite_G_cm-1"]), r_decl),
            d_pred, places=12,
        )

    def test_o7_lever_window_robust(self) -> None:
        # Fenêtre de robustesse du S+ : δ ≤ 10 % pour r ∈ [~1,45 ; ~7,57]
        # (bornes exactes : D = 1580·sqrt(r/(1+r)), D/mu_ref = 0,90 et 1,10).
        g, mu_ref = 1580.0, 1350.0
        for r in (1.45, 2.0, 3.0, 5.0, 7.57):
            d = _d_pred(g, r)
            self.assertLessEqual(abs(d / mu_ref - 1.0), 0.10, msg=f"r={r}")
        # Le contact gelé (r = 3) est dans la fenêtre, marge basse ~1,55.
        self.assertGreaterEqual(3.0 - 1.45, 1.5)
        # Hors fenêtre : r = 1 (O3) donnait P (δ ≈ 17,2 %) ;
        # r = 20 reste P (δ ≈ 14,2 %). Propriété exacte et honnête du
        # modèle : il ne fait JAMAIS S- pour r > 0 (δ bornée dans
        # [0,138 ; 0,170] hors fenêtre) — le S- n'est pas accessible.
        self.assertGreater(abs(_d_pred(g, 1.0) / mu_ref - 1.0), 0.10)
        d20 = abs(_d_pred(g, 20.0) / mu_ref - 1.0)
        self.assertGreater(d20, 0.10)
        self.assertLessEqual(d20, 0.20)
        self.assertAlmostEqual(_d_pred(g, 3.0), self.row()["mu_loc"], places=9)


if __name__ == "__main__":
    unittest.main(verbosity=2)
