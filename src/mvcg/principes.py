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


def pf5_psy_energie() -> tuple[float, dict[str, Any]]:
    """Recompute de l'exemple psy : E = N_psy * hbar_N / delta_t.

    Coherence interne du volet I : l'equation-image donne
    hbar_N = 1,054e-34 J.s, l'exemple-texte 5,25e-31 J pour 500 psy
    sur 1 s (coherent avec 1,054e-33). La machine pese l'ecart
    structurel d'un facteur 10 entre image et texte, pas la physique.
    """
    t5 = load_table("pf5_psy_unite_LITTERATURE-2025.json")
    p = t5["params"]
    e = float(p["N_psy_exemple"]) * float(p["hbar_N_Js"]) / float(p["delta_t_s"])
    return float(e), {
        "table": t5["vintage"],
        "table_sha256": t5["_sha256"],
        "hbar_N_Js": float(p["hbar_N_Js"]),
        "N_psy": float(p["N_psy_exemple"]),
        "delta_t_s": float(p["delta_t_s"]),
        "E_recompute_J": e,
        "hbar_N_implicite_du_texte_Js": (
            float(p["E_annoncee_J"]) * float(p["delta_t_s"]) / float(p["N_psy_exemple"])
        ),
        "ref": t5["value"],
        "note": "E recomputee avec la constante de l'equation-image vs energie annoncee du texte",
    }


def pf6_rmn_deltab() -> tuple[float, dict[str, Any]]:
    """Delta(B) RMN recompute depuis la formule transcrite (image-61).

    dB = (m_e c / (g e)) * (c_éth k / sqrt(a^2 + b^2)) avec c_éth = c_N
    = 1e9 c (volet III) sous l'identification declaree dans le protocole
    gele CHANTIER-PSY-RMN-PROTOCOLE.md. m_e et e gelés DECLARED-2026.
    """
    t6 = load_table("pf6_rmn_deltab_LITTERATURE-2025.json")
    tc = load_table("pf6_ceth_LITTERATURE-2025.json")
    tk = load_table("pf6_constants_DECLARED-2026.json")
    tcodata = load_table("codata2018_extract.json")
    p = t6["params"]
    c = float(tcodata["constants"]["c_ms"])
    me = float(tk["params"]["me_kg"])
    e = float(tk["params"]["e_C"])
    a = float(p["a_m"])
    b = float(p["b_over_a"]) * a
    k = float(p["k"])
    g = float(p["g_Lande"])
    geo = math.sqrt(a * a + b * b)
    ceth = float(tc["params"]["c_N_over_c"]) * c
    pref = me * c / (g * e)
    dB = pref * (ceth * k / geo)
    ceth_requis = float(t6["value"]) * g * e * geo / (me * c * k)
    dB_si_ceth_c = pref * (c * k / geo)
    return float(dB), {
        "table": t6["vintage"],
        "table_sha256": t6["_sha256"],
        "a_m": a,
        "b_m": b,
        "k": k,
        "g_Lande": g,
        "geo_m": geo,
        "ceth_m_s": ceth,
        "DeltaB_T": dB,
        "ceth_requis_m_s": ceth_requis,
        "DeltaB_si_ceth_eq_c_T": dB_si_ceth_c,
        "ref": t6["value"],
        "note": "prediction RMN recomputee sous l'identification declaree c_éth = c_N = 1e9 c",
    }


def pf7_f4_recompute() -> tuple[float, dict[str, Any]]:
    """F4 recompte depuis beta_4 et S_4 publies : F4 = e^{-beta_4 S_4}.

    Coherence arithmetique du jeu numerique illustratif du volet V
    (tableaux image-30/31), comme PF3 — la machine verifie l'arithmetique
    publiee, pas la physique des plans.
    """
    t7 = load_table("pf7_plans_tableau_LITTERATURE-2025.json")
    p = t7["params"]
    beta4 = float(p["beta_4"])
    s4 = float(p["S_4_tableau"])
    f4 = math.exp(-beta4 * s4)
    f4_depuis_N = math.exp(-beta4 * math.log(float(p["N_4"])))
    f_publies = {k: float(v) for k, v in p["F_publies"].items()}
    beta = {k: float(v) for k, v in p["beta"].items()}
    svals = {k: float(v) for k, v in p["S"].items()}
    recomputes = {
        k: math.exp(-beta[k] * svals[k]) for k in beta
    }
    deltas_vs_publies = {
        k: abs(recomputes[k] - f_publies[k]) / f_publies[k] for k in beta
    }
    return float(f4), {
        "table": t7["vintage"],
        "table_sha256": t7["_sha256"],
        "beta_4": beta4,
        "S_4": s4,
        "F4_recompute": f4,
        "F4_depuis_N": f4_depuis_N,
        "F_recomputes_tous_plans": recomputes,
        "delta_max_vs_publies": max(deltas_vs_publies.values()),
        "ref": t7["value"],
        "note": "F4 recompte depuis le tableau publie vs 0,035 publie",
    }


def pf8_hz_filtrage_ecart() -> tuple[float, dict[str, Any]]:
    """Ecart max |H_filtree - H_LCDM|/H_LCDM sur z in [0, z_max].

    Equation image-29 prise telle que publiee (F_U non chiffre dans le
    corpus -> lecture neutre F_U = 1 gelee dans le protocole) ; la borne
    revendiquee du texte (<2 %) est la reference. H0 se cancele dans le
    rapport des H.
    """
    t8 = load_table("pf7_hz_filtrage_LITTERATURE-2025.json")
    tin = load_table("pf7_hz_inputs_DECLARED-2026.json")
    p = tin["params"]
    om = float(p["Omega_m"])
    ol = float(p["Omega_lambda"])
    orr = float(p["Omega_r"])
    f1 = float(p["F1"])
    f4 = float(p["F4"])
    z_max = float(p["z_max"])
    # F_U = 1 (lecture gelee, protocole) ; Omega_k = 0
    def h2_lcdm(z: float) -> float:
        return om * (1.0 + z) ** 3 + orr * (1.0 + z) ** 4 + ol

    def h2_filtre(z: float) -> float:
        return f4 * om * (1.0 + z) ** 3 + f1 * orr * (1.0 + z) ** 4 + ol

    n = 420  # pas 0,005 sur [0, 2,1] — grille figee
    ecart_max = -1.0
    z_argmax = None
    ecart_z0 = None
    for i in range(n + 1):
        z = z_max * i / n
        e = abs(math.sqrt(h2_filtre(z) / h2_lcdm(z)) - 1.0)
        if i == 0:
            ecart_z0 = e
        if e > ecart_max:
            ecart_max = e
            z_argmax = z
    return float(ecart_max), {
        "table": t8["vintage"],
        "table_sha256": t8["_sha256"],
        "Omega_m": om,
        "Omega_lambda": ol,
        "F4": f4,
        "F1": f1,
        "z_max": z_max,
        "ecart_max": ecart_max,
        "z_argmax": z_argmax,
        "ecart_z0": ecart_z0,
        "H2_filtre_sur_H02_z0": h2_filtre(0.0),
        "note": "borne <2 % revendiquee vs ecart publie par l'equation meme ; normalisation H(0)=H0 non tenue (F_U non declare)",
    }


def pf1b_rg_spread_2loop() -> tuple[float, dict[str, Any]]:
    """Dispersion relative minimale des 4 couplages au 2-boucles.

    Meme transport que pf1_rg_spread (meme grille t in [0, 36] pas 0,1,
    meme spread (max-min)/moyenne), meme entrees 1-loop gelees ; seuls
    les coefficients 2-boucles changent : matrice b_ij SM empruntee a
    Machacek & Vaughn 1983 (gelee datée dans pf1b_rg_2loop), coefficient
    diagonal noetique b_njn = +10 declare par la source. Integration RK4
    de dX_i/dt = -(1/2pi)[b_i + sum_j b_ij/X_j], X = 4pi/g^2 ; termes
    croises noet x SM non declares -> 0 (lecture neutre gelee).
    """
    t1b = load_table("pf1b_rg_2loop_LITTERATURE-2026.json")
    p = t1b["params"]
    mz = float(p["Mz_GeV"])
    g0 = [float(p["g1_Mz"]), float(p["g2_Mz"]), float(p["g3_Mz"]),
          float(p["g_noet_Mz"])]
    b = [float(p["b1"]), float(p["b2"]), float(p["b3"]), float(p["b_noet"])]
    bij = [[float(v) for v in row] for row in p["b_ij_SM"]]
    bnjn = float(p["b_njn_declared"])
    x0 = [4.0 * math.pi / g**2 for g in g0]

    def dx(x: list[float]) -> list[float]:
        out = []
        for i in range(3):
            s = sum(bij[i][j] * (4.0 * math.pi / x[j]) / (16.0 * math.pi**2)
                    for j in range(3))
            out.append(-(1.0 / (2.0 * math.pi)) * (b[i] + s))
        g2n = 4.0 * math.pi / x[3]
        out.append(-(1.0 / (2.0 * math.pi))
                   * (b[3] + bnjn * g2n / (16.0 * math.pi**2)))
        return out

    h_rk = 0.02  # pas interne fige

    def rk4(x: list[float], t: float) -> list[float]:
        for _ in range(int(round(t / h_rk))):
            k1 = dx(x)
            k2 = dx([xi + h_rk * k / 2.0 for xi, k in zip(x, k1)])
            k3 = dx([xi + h_rk * k / 2.0 for xi, k in zip(x, k2)])
            k4 = dx([xi + h_rk * k for xi, k in zip(x, k3)])
            x = [xi + h_rk * (a + 2.0 * c + 2.0 * d + e) / 6.0
                 for xi, a, c, d, e in zip(x, k1, k2, k3, k4)]
        return x

    def spread_of(x: list[float]) -> float:
        g = [math.sqrt(4.0 * math.pi / xi) for xi in x]
        m = sum(g) / 4.0
        return (max(g) - min(g)) / m

    t_claim = math.log(float(p["mu_U_claim_GeV"]) / mz)
    x_claim = rk4(x0.copy(), t_claim)
    g_claim = [math.sqrt(4.0 * math.pi / xi) for xi in x_claim]
    spread_claim = spread_of(x_claim)

    best_spread = math.inf
    best_t = None
    x = x0.copy()
    t = 0.0
    while t <= 36.0 + 1e-9:
        s = spread_of(x)
        if s < best_spread:
            best_spread = s
            best_t = round(t, 1)
        if t < 36.0:
            x = rk4(x, 0.1)
        t = round(t + 0.1, 10)

    return float(best_spread), {
        "table": t1b["vintage"],
        "table_sha256": t1b["_sha256"],
        "loop": "2-loop",
        "best_t": best_t,
        "best_mu_GeV": mz * math.exp(best_t),
        "spread_rel": best_spread,
        "spread_at_claim_scale": spread_claim,
        "g_at_claim_scale": g_claim,
        "g_noet_at_claim": g_claim[3],
        "g_U_claim": float(p["g_U_claim"]),
        "ref": t1b["value"],
        "note": "dispersion (max-min)/moyenne au 2-boucles, meilleur t ; coefficients SM empruntes MV1983 geles, b_njn declare ; le 2-boucles ne ferme pas la dette 1-loop de PF1",
    }
