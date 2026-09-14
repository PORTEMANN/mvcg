#!/usr/bin/env python3
"""Chantier PRINCIPES — calculs des contacts PF1-PF4.

Protocole gelé : docs/CHANTIER-PRINCIPES-PROTOCOLE.md. Chaque runner
relit les tables gelées (affirmations datées des volets I-V) et les
constantes déclarées — jamais de fetch réseau, jamais de pointeur vers
l'archive. La machine pèse les revendications publiées, elle ne les
transcrit pas.
"""

from __future__ import annotations

import math
from typing import Any

from mvcg.tables import load_table


def pf1_rg_spread() -> tuple[float, dict[str, Any]]:
    """Dispersion relative minimale des 4 couplages au 1-loop.

    Entrées gelées : table pf1 (g(Mz), betas, b_noet). La machine
    n'intègre QUE le 1-loop (coefficients SM 2-boucles absents de la
    source) — c'est la revendication 1-loop qui est mesurée, l'article
    renvoyant lui-même au 2-boucles pour la coïncidence.
    """
    t_pf1 = load_table("pf1_rg_unification_LITTERATURE-2025.json")
    p = t_pf1["params"]
    mz = float(p["Mz_GeV"])
    g0 = [float(p["g1_Mz"]), float(p["g2_Mz"]), float(p["g3_Mz"]),
          float(p["g_noet_Mz"])]
    b = [float(p["b1"]), float(p["b2"]), float(p["b3"]), float(p["b_noet"])]

    def g_at(t: float) -> list[float]:
        return [
            math.sqrt(4.0 * math.pi / (4.0 * math.pi / gi**2 - bi * t / (2.0 * math.pi)))
            for gi, bi in zip(g0, b)
        ]

    best_spread = math.inf
    best_t = None
    t_claim = math.log(float(p["mu_U_claim_GeV"]) / mz)
    # calcule hors du balayage : t_claim (ln(2e16/Mz) ~ 33,02) n'est pas
    # un multiple de 0,1, le test d'egalite dans la grille le manquait
    g_claim = g_at(t_claim)
    g_at_claim = g_claim if all(
        math.isfinite(g) and g > 0 for g in g_claim
    ) else None
    for k in range(0, 361):
        t = k * 0.1
        gs = g_at(t)
        if any(not math.isfinite(g) or g <= 0 for g in gs):
            continue
        mean = sum(gs) / 4.0
        spread = (max(gs) - min(gs)) / mean
        if spread < best_spread:
            best_spread = spread
            best_t = t

    return float(best_spread), {
        "table": t_pf1["vintage"],
        "table_sha256": t_pf1["_sha256"],
        "loop": "1-loop",
        "best_t": best_t,
        "best_mu_GeV": mz * math.exp(best_t),
        "spread_rel": best_spread,
        "g_at_claim_scale": g_at_claim,
        "ref": t_pf1["value"],
        "note": "dispersion (max-min)/moyenne au meilleur t ; revendique 1 % (2-boucles)",
    }


def pf2_graviton_ev() -> tuple[float, dict[str, Any]]:
    """E = h.f du pic 25 THz, en eV (h gelé CODATA-2018)."""
    t_pf2 = load_table("pf2_graviton_25thz_LITTERATURE-2025.json")
    t_codata = load_table("codata2018_extract.json")
    h_Js = float(t_codata["constants"]["h_Js"])
    e_C = float(t_codata["constants"]["e_C"])
    f = float(t_pf2["params"]["f_claim_Hz"])
    ev = h_Js * f / e_C
    return float(ev), {
        "table": t_pf2["vintage"],
        "table_sha256": t_pf2["_sha256"],
        "f_Hz": f,
        "h_Js": h_Js,
        "E_eV": ev,
        "ref": t_pf2["value"],
        "note": "contact de coherence interne II x V",
    }


def pf3_tau5_recompute() -> tuple[float, dict[str, Any]]:
    """Recompute arithmétique du jeu illustratif : 10.exp(-beta.S5)."""
    t_pf3 = load_table("pf3_tau5_jeu_LITTERATURE-2025.json")
    p = t_pf3["params"]
    tau = float(p["base"]) * math.exp(-float(p["beta"]) * float(p["S5"]))
    return float(tau), {
        "table": t_pf3["vintage"],
        "table_sha256": t_pf3["_sha256"],
        "base": p["base"],
        "beta": p["beta"],
        "S5": p["S5"],
        "tau5": tau,
        "ref": t_pf3["value"],
        "note": "jeu illustratif declare comme tel par la source",
    }


def pf4_vide_log_ratio() -> tuple[float, dict[str, Any]]:
    """log10(rho_Planck / rho_Lambda) depuis les constantes déclarées.

    rho_Planck = c^7 / (hbar.G^2) ; rho_Lambda = Omega_Lambda . rho_crit . c^2
    avec rho_crit = 3 H0^2 / (8 pi G). Les deux en J/m^3.
    """
    t_pf4 = load_table("pf4_vide_catastrophe_LITTERATURE-2025.json")
    t_in = load_table("pf_vide_inputs_DECLARED-2026.json")
    t_codata = load_table("codata2018_extract.json")
    pin = t_in["params"]
    pc = t_codata["constants"]
    c = float(pc["c_ms"])
    hbar = float(pc["hbar_Js"])
    g = float(pin["G_SI"])
    h0 = float(pin["H0_km_s_Mpc"]) * 1e3 / float(pin["Mpc_m"])
    om = float(pin["OmegaLambda"])
    rho_planck = c**7 / (hbar * g**2)
    rho_crit = 3.0 * h0**2 / (8.0 * math.pi * g)
    rho_lambda = om * rho_crit * c**2
    log_ratio = math.log10(rho_planck / rho_lambda)
    return float(log_ratio), {
        "table": t_pf4["vintage"],
        "table_sha256": t_pf4["_sha256"],
        "rho_planck_J_m3": rho_planck,
        "rho_lambda_J_m3": rho_lambda,
        "log_ratio": log_ratio,
        "ref": t_pf4["value"],
        "note": "exposant recompute vs 122 revendique",
    }
