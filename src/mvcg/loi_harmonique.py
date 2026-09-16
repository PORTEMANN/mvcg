#!/usr/bin/env python3
"""Chantier LOI-HARMONIQUE — premières pesées de la loi m = m_p.2^(n/12).

Protocole : docs/CHANTIER-LOI-HARMONIQUE-PROTOCOLE.md. La machine pèse
pour la première fois une loi interne au corpus noétique (et non des
tables externes) : ses instances particule par particule. Tables gelées
datées, zéro fetch. Emprunts CODATA-2018 / PDG-2024 écrits en source des
tables (grammaire PF1b — l'emprunt est un acte curatorial, pas une
correction en silence).
"""

from __future__ import annotations

import math
from typing import Any

from mvcg.tables import load_table


def sqf(n: int) -> int:
    """Noyau sans facteur carré : produit des facteurs premiers distincts."""
    res, m = 1, n
    p = 2
    while p * p <= m:
        if m % p == 0:
            res *= p
            while m % p == 0:
                m //= p
        p += 1
    return res * m


def lh_ko6_racines() -> tuple[float, dict[str, Any]]:
    """Loi KO-6 : les valeurs de sqf publiees par le corpus vs rad recompte.

    Le corpus publie (Géométrie Spectrale, 26/08/2026) : sqf(24)=6,
    sqf(63)=7, sqf(120)=30, sqf(36)=1, sqf(54)=6, avec la definition
    standard 'produit des diviseurs premiers distincts'. La machine
    recompute rad(n) pour chacun : rad(63) = 21 (pas 7), rad(36) = 6
    (pas 1) — deux des cinq valeurs publiees sont fausses, et
    l'exclusion d'E6 (sqf(36)=1) s'effondre. Les identites
    module-racines (24/63/120/36 vs D4/E7/E8/E6) restent exactes —
    information consignee en extra. mu_loc = ecart maximal |declare -
    recompute|.
    """
    t = load_table("lh_ko6_LITTERATURE-2026.json")
    p = t["params"]
    mods = {int(k): int(v) for k, v in p["modules"].items()}
    rac = {k: int(v) for k, v in p["racines"].items()}
    anu = {k: int(v) for k, v in p["anu_chimie_occulte"].items()}
    decl = {int(k): int(v) for k, v in p["sqf_declares_par_le_corpus"].items()}

    recomputes = {n: sqf(n) for n in decl}
    ecarts_sqf = {n: abs(decl[n] - recomputes[n]) for n in decl}
    identites = {
        "N24_vs_D4": mods[24] - rac["D4"],
        "N63_vs_E7": mods[63] - rac["E7_pos"],
        "N120_vs_E8": mods[120] - rac["E8_pos"],
        "N36_vs_E6": mods[36] - rac["E6_pos"],
        "He3_54_coquille": anu["He3_ANU"] - 9 * recomputes[54],
    }
    ecart = float(max(max(ecarts_sqf.values()),
                      max(abs(v) for v in identites.values())))
    return ecart, {
        "table": t["vintage"],
        "table_sha256": t["_sha256"],
        "sqf_declares": decl,
        "sqf_recomputes": recomputes,
        "ecarts_sqf": ecarts_sqf,
        "n_sqf_faux": sum(1 for v in ecarts_sqf.values() if v > 0),
        "identites_module_racines": identites,
        "E6_exclusion_tient": recomputes[36] == 1,
        "ref": t["value"],
        "note": "sqf publies vs rad recompte : 2 valeurs sur 5 fausses (63 et 36) ; identites module-racines exactes ; l'exclusion d'E6 par sqf(36)=1 s'effondre (rad(36)=6)",
    }


def lh_muon_quinte() -> tuple[float, dict[str, Any]]:
    """Masse du muon : la quinte (3/2) amplifiée par 1/alpha.

    m_loc = m_e x (3/2) / alpha (CODATA-2018 gelées) vs m_muon PDG-2024.
    La loi harmonique du corpus : le muon est l'électron résonnant à la
    quinte sur l'échelle 1/alpha.
    """
    t = load_table("lh_masses_LITTERATURE-2026.json")
    p = t["params"]
    m_e = float(p["m_e_MeV"])
    alpha = float(p["alpha"])
    m_pdg = float(p["m_muon_PDG_MeV"])
    m_loc = m_e * 1.5 / alpha
    return float(m_loc), {
        "table": t["vintage"],
        "table_sha256": t["_sha256"],
        "m_e_MeV": m_e,
        "alpha": alpha,
        "m_loc_MeV": m_loc,
        "ref_MeV": m_pdg,
        "ecart_pct": abs(m_loc - m_pdg) / m_pdg * 100.0,
        "note": "quinte 3/2 x 1/alpha ; revendication corpus ~99,4 %",
    }


def lh_z_diagonale() -> tuple[float, dict[str, Any]]:
    """Masse du boson Z : la projection diagonale m_p/alpha/sqrt(2).

    m_loc = m_p / alpha / sqrt(2) (CODATA-2018 gelées) vs m_Z PDG-2024.
    La loi harmonique du corpus : le Z est la tension maximale du proton
    (137 x m_p) projetée sur la diagonale d'un carré.
    """
    t = load_table("lh_masses_LITTERATURE-2026.json")
    p = t["params"]
    m_p = float(p["m_p_MeV"])
    alpha = float(p["alpha"])
    m_pdg = float(p["m_Z_PDG_MeV"])
    m_loc = m_p / alpha / math.sqrt(2.0)
    return float(m_loc), {
        "table": t["vintage"],
        "table_sha256": t["_sha256"],
        "m_p_MeV": m_p,
        "alpha": alpha,
        "m_loc_MeV": m_loc,
        "ref_MeV": m_pdg,
        "ecart_pct": abs(m_loc - m_pdg) / m_pdg * 100.0,
        "note": "m_p x (1/alpha) / sqrt(2) ; revendication corpus ~99,7 %",
    }


def lh_strange_quarte() -> tuple[float, dict[str, Any]]:
    """Masse du quark strange : la quarte 2 m_p/18 (instance G4).

    m_loc = 2 m_p / 18 (CODATA-2018 gelées) vs m_s PDG-2024 (valeur
    centrale 93 MeV, MSbar 2 GeV). La loi harmonique du corpus : le
    strange est deux fois la classe m_p/18. Attendu S- (~12 %) : c'est
    la frontiere de la loi, pas un accident.
    """
    t = load_table("lh_quarks_LITTERATURE-2026.json")
    p = t["params"]
    tm = load_table("lh_masses_LITTERATURE-2026.json")["params"]
    m_p = float(tm["m_p_MeV"])
    m_pdg = float(p["m_strange_PDG_MeV"])
    m_loc = 2.0 * m_p / 18.0
    return float(m_loc), {
        "table": t["vintage"],
        "table_sha256": t["_sha256"],
        "m_p_MeV": m_p,
        "m_loc_MeV": m_loc,
        "ref_MeV": m_pdg,
        "ref_unc_plus_MeV": float(p["m_strange_unc_plus_MeV"]),
        "ref_unc_minus_MeV": float(p["m_strange_unc_minus_MeV"]),
        "ecart_pct": abs(m_loc - m_pdg) / m_pdg * 100.0,
        "note": "quarte 2 m_p/18 ; revendication corpus ~112 % de m_s — la loi harmonique lache aux quarks moyens, la machine nomme la frontiere",
    }


def lh_bottom_g6() -> tuple[float, dict[str, Any]]:
    """Masse du quark bottom : la transposition G6 4 m_charm/2^(1/12).

    m_loc = 4 x (24 m_p/18) / 2^(1/12) (CODATA-2018 gelées) vs m_b
    PDG-2024 (valeur centrale 4180 MeV, MSbar m_b). La loi harmonique du
    corpus : le bottom est quatre fois le charm descendu d'un demi-ton.
    Attendu S- (~13 %) : frontiere de la loi cote quarks lourds.
    """
    t = load_table("lh_quarks_LITTERATURE-2026.json")
    p = t["params"]
    tm = load_table("lh_masses_LITTERATURE-2026.json")["params"]
    m_p = float(tm["m_p_MeV"])
    m_pdg = float(p["m_bottom_PDG_MeV"])
    m_charm_loc = 24.0 * m_p / 18.0
    m_loc = 4.0 * m_charm_loc / 2.0 ** (1.0 / 12.0)
    return float(m_loc), {
        "table": t["vintage"],
        "table_sha256": t["_sha256"],
        "m_p_MeV": m_p,
        "m_charm_loc_MeV": m_charm_loc,
        "m_loc_MeV": m_loc,
        "ref_MeV": m_pdg,
        "ecart_pct": abs(m_loc - m_pdg) / m_pdg * 100.0,
        "note": "G6 : 4 m_charm/2^(1/12) avec m_charm = 24 m_p/18 (G5 du meme article) ; revendication corpus « 5000/1,0593 ~ 4200 » — voir LH_Bottom_Arith pour la dette arithmetique interne",
    }


def lh_bottom_arith() -> tuple[float, dict[str, Any]]:
    """Dette arithmetique interne du corpus : « 5000/1,0593 ~ 4200 ».

    L'article (Géométrie Spectrale) affirme que 5000/1,0593 vaut environ
    4200 — c'est la valeur que sa formule G6 devrait donner. Recompute
    exact : 4720,098. mu_loc = recompute exact, mu_ref = valeur declaree
    (4200). Pendant de PF5 : la machine pese la coherence entre le
    resultat annonce et l'arithmetique du texte, pas la physique.
    """
    t = load_table("lh_quarks_LITTERATURE-2026.json")
    p = t["params"]
    num = float(p["bottom_arith_numerateur"])
    den = float(p["bottom_arith_diviseur"])
    declare = float(p["bottom_arith_declare"])
    rec = num / den
    return float(rec), {
        "table": t["vintage"],
        "table_sha256": t["_sha256"],
        "recompute_exact": rec,
        "declare": declare,
        "ecart": abs(rec - declare),
        "note": "5000/1,0593 = 4720,098 (pas ~4200) : l'arithmetique du texte est fausse de 520 unites — dette interne au corpus, type PF5",
    }


def lh_koide_q() -> tuple[float, dict[str, Any]]:
    """Rapport de Koide des leptons charges : Q = Somme(m)/(Somme(racine(m)))^2.

    Recompute depuis les masses gelées (CODATA-2018 m_e, PDG-2024 m_muon,
    m_tau) vs la revendication Q = 2/3 (loi empirique). Deux erreurs de
    préparation ont été attrapées avant gel de la formule (variantes sans
    racines / inversée) — leçon KO-6 appliquée : vérifier avant de geler,
    pas seulement après le run. Attendu S+ à ~1e-4 theta : le S+ le plus
    serré du registre.
    """
    t = load_table("lh_masses_LITTERATURE-2026.json")
    p = t["params"]
    m = [float(p["m_e_MeV"]), float(p["m_muon_PDG_MeV"]),
         float(p["m_tau_PDG_MeV"])]
    s_sqrt = sum(math.sqrt(x) for x in m)
    q = sum(m) / (s_sqrt ** 2)
    return float(q), {
        "table": t["vintage"],
        "table_sha256": t["_sha256"],
        "masses_MeV": m,
        "Q_recompute": q,
        "Q_ref": 2.0 / 3.0,
        "delta": abs(q - 2.0 / 3.0) / (2.0 / 3.0),
        "note": "loi empirique de Koide, pas une instance de la loi harmonique : le corpus la cite — la machine pèse sa tenue sur PDG-2024 gelé",
    }


def lh_zmax_modes() -> tuple[float, dict[str, Any]]:
    """Z_max et N_modes koïlon : recompute à alpha_hydro = 1e-3 gelé.

    Corps du corpus : Z_max ~ 179, N_modes ~ 120 (= racines E8), avec
    N_modes = 12.log2(1/alpha_hydro) et Z_max = (3/2).N_modes. Recompute :
    N_modes = 119,589, Z_max = 179,384. mu_loc = Z_max recompute,
    mu_ref = 179 declare. Attendu S+ arithmétique (l'écart « ~ » tient).
    """
    t = load_table("lh_zmax_LITTERATURE-2026.json")
    p = t["params"]
    alpha_h = float(p["alpha_hydro"])
    n_modes = 12.0 * math.log2(1.0 / alpha_h)
    zmax = 1.5 * n_modes
    return float(zmax), {
        "table": t["vintage"],
        "table_sha256": t["_sha256"],
        "alpha_hydro": alpha_h,
        "N_modes_recompute": n_modes,
        "N_modes_declare": float(p["N_modes_declare"]),
        "delta_N_modes": abs(n_modes - float(p["N_modes_declare"]))
        / float(p["N_modes_declare"]),
        "Z_max_recompute": zmax,
        "Z_max_declare": float(p["Z_max_declare_corps"]),
        "note": "le « ~ 179 » du corps tient au seuil theta (0,215 %) ; N_modes ~ 120 tient aussi (0,342 %) — extra ; alpha double-usage nommé en dette G12",
    }


def lh_addendum_corps() -> tuple[float, dict[str, Any]]:
    """Tension addendum/corps sur Z_max : 180 « recomputé exact » vs ~ 179.

    L'addendum (07/09/2026) publie « Z_max = 180 (recomputé exact) » à
    alpha_K = 2^-10 gelé ; le corps publie « Z_max ~ 179 » à alpha_hydro
    = 1e-3. Deux énoncés présentés comme des recomputes, écart 1.
    mu_loc = |180 - 179| = 1 U absolu, mu_ref = 0 (identités déclarées
    exactes) — grammaire KO-6. Explication candidate en extra (alpha
    différent) mais les deux énoncés se présentent comme « recomputé
    exact » : la dette est de présentation, type PF5.
    """
    t = load_table("lh_zmax_LITTERATURE-2026.json")
    p = t["params"]
    ecart = abs(float(p["Z_max_declare_addendum"])
                - float(p["Z_max_declare_corps"]))
    return float(ecart), {
        "table": t["vintage"],
        "table_sha256": t["_sha256"],
        "addendum": float(p["Z_max_declare_addendum"]),
        "corps": float(p["Z_max_declare_corps"]),
        "alpha_K_addendum": float(p["alpha_K_addendum"]),
        "alpha_hydro": float(p["alpha_hydro"]),
        "note": "explication candidate : alpha diffère (2^-10 vs 1e-3, Z_max = 180,0 vs 179,4) — mais les deux énoncés se disent « recomputé exact » : la dette est de présentation",
    }


def lh_up_g3() -> tuple[float, dict[str, Any]]:
    """Masse du quark up : la classe m_p/18 amortie par racine(alpha)/2.

    m_loc = (m_p/18).racine(alpha)/2 (CODATA-2018 gelées) vs m_u PDG-2024
    (valeur centrale 2,16 MeV, MSbar 2 GeV, +0,49/-0,26). Instance G3 de
    la loi harmonique. Attendu S+ (delta ~3,1 %) : la valeur centrale
    locale tombe dans la fourchette PDG (extra : position en sigma).
    """
    t = load_table("lh_quarks_LITTERATURE-2026.json")
    p = t["params"]
    tm = load_table("lh_masses_LITTERATURE-2026.json")["params"]
    m_p = float(tm["m_p_MeV"])
    alpha = float(tm["alpha"])
    m_pdg = float(p["m_up_PDG_MeV"])
    m_loc = (m_p / 18.0) * math.sqrt(alpha) / 2.0
    return float(m_loc), {
        "table": t["vintage"],
        "table_sha256": t["_sha256"],
        "m_p_MeV": m_p,
        "alpha": alpha,
        "m_loc_MeV": m_loc,
        "ref_MeV": m_pdg,
        "ref_unc_plus_MeV": float(p["m_up_unc_plus_MeV"]),
        "ref_unc_minus_MeV": float(p["m_up_unc_minus_MeV"]),
        "position_sigma_haut": (m_loc - m_pdg)
        / float(p["m_up_unc_plus_MeV"]),
        "ecart_pct": abs(m_loc - m_pdg) / m_pdg * 100.0,
        "note": "(m_p/18).racine(alpha)/2 ; la valeur locale est dans la fourchette PDG (+0,49/-0,26) — extra sigma haut",
    }


def lh_charm_g5() -> tuple[float, dict[str, Any]]:
    """Masse du quark charm : la classe 24 m_p/18 (instance G5).

    m_loc = 24 m_p/18 (CODATA-2018 gelées) vs m_c PDG-2024 (valeur
    centrale 1270 +/- 20 MeV, MSbar m_c). Attendu S+ (delta ~1,5 %) :
    le dernier S+ attendu du sextuor G1-G6.
    """
    t = load_table("lh_quarks_LITTERATURE-2026.json")
    p = t["params"]
    tm = load_table("lh_masses_LITTERATURE-2026.json")["params"]
    m_p = float(tm["m_p_MeV"])
    m_pdg = float(p["m_charm_PDG_MeV"])
    m_loc = 24.0 * m_p / 18.0
    return float(m_loc), {
        "table": t["vintage"],
        "table_sha256": t["_sha256"],
        "m_p_MeV": m_p,
        "m_loc_MeV": m_loc,
        "ref_MeV": m_pdg,
        "ref_unc_MeV": float(p["m_charm_unc_MeV"]),
        "position_sigma": abs(m_loc - m_pdg)
        / float(p["m_charm_unc_MeV"]),
        "ecart_pct": abs(m_loc - m_pdg) / m_pdg * 100.0,
        "note": "24 m_p/18 ; delta 1,49 %, la valeur locale est a 0,95 sigma du centre PDG",
    }


def lh_anu_gamme() -> tuple[float, dict[str, Any]]:
    """Gamme du Koilon : rapport geometrique moyen N(Z)/N(Z-1), Z = 11-30.

    Table n°2 ANU (1908) gelee : GM = exp(moyenne(ln r_Z)) avec
    r_Z = N(Z)/N(Z-1) sur 20 rapports, vs 2^(1/12) declare par le corpus
    (« converge vers 2^(1/12) dans la plage Z = 11-30 »). Le corpus
    annonce meme la valeur recomptee « 1,0607 » — la machine pese la
    declaration, pas le hasard.
    """
    t = load_table("lh_koilon_gamme_LITTERATURE-1908.json")
    p = t["params"]
    rows = {int(r[0]): (r[1], int(r[2])) for r in p["rows"]}
    z0, z1 = (int(x) for x in p["plage_c1"])
    ratios = {z: rows[z][1] / rows[z - 1][1] for z in range(z0, z1 + 1)}
    gm = math.exp(sum(math.log(r) for r in ratios.values())
                  / len(ratios))
    cible = 2.0 ** (1.0 / 12.0)
    return float(gm), {
        "table": t["vintage"],
        "table_sha256": t["_sha256"],
        "plage": [z0, z1],
        "n_rapports": len(ratios),
        "rapports": ratios,
        "GM_recompute": gm,
        "rapport_declare": cible,
        "delta": abs(gm - cible) / cible,
        "note": "le corpus annonce « converge vers 2^(1/12) » ET la valeur 1,0607 — recompute : 1,060 704, les deux declarations tiennent au seuil",
    }


def lh_alpha_double() -> tuple[float, dict[str, Any]]:
    """Dette G12 : deux constantes sous un meme symbole alpha.

    Le corpus utilise alpha = 1/137 (structure fine) et alpha = c_s/c =
    1e-3 (Koilon) dans le même texte, et la formule k(Z) = (3/2).
    exp(-ln Z/103 . alpha) reference alpha sans specifier laquelle.
    mu_loc = alpha_sf (1/137 declare), mu_ref = alpha_hydro (1e-3
    declare) : l'ecart relatif nomme la collision d'identification.
    Extras : ratio 7,30 et sensibilite de k(Z) aux deux lectures —
    le formulaire est aveugle a sa propre ambiguite (4,8e-4).
    """
    t = load_table("lh_alpha_LITTERATURE-2026.json")
    p = t["params"]
    a_sf = float(p["alpha_structure_fine_declare"])
    a_h = float(p["alpha_hydro_declare"])
    pref = float(p["k_prefacteur"])
    div = float(p["k_diviseur"])
    zev = float(p["k_Z_eval"])
    k_sf = pref * math.exp(-math.log(zev) / div * a_sf)
    k_h = pref * math.exp(-math.log(zev) / div * a_h)
    return float(a_sf), {
        "table": t["vintage"],
        "table_sha256": t["_sha256"],
        "alpha_sf": a_sf,
        "alpha_hydro": a_h,
        "ratio_sf_sur_hydro": a_sf / a_h,
        "delta_rel": abs(a_sf - a_h) / a_h,
        "k_Z_sf": k_sf,
        "k_Z_hydro": k_h,
        "k_sensibilite": abs(k_sf - k_h),
        "note": "un symbole, deux constantes : 1/137 vs 1e-3 — l'ecart relatif (630 %) est la dette ; k(Z) ne peut pas trancher (sensibilite 4,8e-4), la dette est dans la declaration pas dans l'instrument",
    }


def lh_anu_pont_rms() -> tuple[float, dict[str, Any]]:
    """Pont ANU <-> nucléides : RMS de la fenêtre vérifiable Z = 1-12.

    L'addendum (07/09/2026) déclare « écart-mètre RMS 1,42 % ». La table
    isotopique complète Z = 13-92 du corpus n'existe pas en local (l'audit E44 fourni porte sur la nucléation de l'enlacement, sans table isotopique) :
    la pesée porte sur la fenêtre vérifiable — 12 lignes du scan 1908,
    isotopes du corpus verbatim (B = 10B). mu_loc = RMS recompté des
    écarts relatifs (N/18 - m)/m, mu_ref = 1,42 % déclaré. Extras :
    RMS hors bore, écarts par élément, dette de table nommée.
    """
    t = load_table("lh_anu_pont_LITTERATURE-1908.json")
    p = t["params"]
    ecarts = {}
    for z, sym, n_anu, m in p["rows"]:
        n18 = n_anu / 18.0
        ecarts[sym] = (n18 - m) / m * 100.0
    rms = math.sqrt(sum(e * e for e in ecarts.values()) / len(ecarts))
    hb = {k: v for k, v in ecarts.items() if k != "B"}
    rms_hors_b = math.sqrt(sum(e * e for e in hb.values()) / len(hb))
    # transport en fraction (mu_ref = 0,0142) — les % restent en extras
    return float(rms / 100.0), {
        "table": t["vintage"],
        "table_sha256": t["_sha256"],
        "n_lignes": len(ecarts),
        "ecarts_pct": ecarts,
        "RMS_recompute_pct": rms,
        "RMS_hors_bore_pct": rms_hors_b,
        "rms_declare_pct": float(p["rms_declare_pct"]),
        "delta": abs(rms - float(p["rms_declare_pct"]))
        / float(p["rms_declare_pct"]),
        "note": "le bore (10B, choix du corpus dans sa propre table) porte +10,97 % et domine le RMS ; hors bore la fenêtre donne 1,225 % — cohérent avec la déclaration 1,42 % ; la déclaration globale reste non vérifiable (table Z = 13-92 absente, dette nommée)",
    }


def lh_g11_mass_shift() -> tuple[float, dict[str, Any]]:
    """G11 : déplacement de masse Δm/m = ε₀E²/8P_K (contact expérimental).

    Article « Géométrie spectrale et physique » (août 2026), formule (21),
    intrants gelés datés (table lh_g11_LITTERATURE-2026.json) : E = 1e15
    V/m déclaré, P_K = 8,5e21 Pa déclaré (estimation « ~ » sans budget —
    gelé tel que déclaré avec sa dette explicite, grammaire PF6). mu_loc =
    recompute strict de (21) : ε₀ (CODATA-2018, SI_VACUUM) E² / 8 P_K ;
    mu_ref = 6,5e-8 déclaré (eq. 26). Extras : dette arithmétique interne
    type PF5 — le corpus a calculé 4,4e15/(8 × 8,5e21) avec P_ext =
    ε₀E²/2 là où (21) exige ε₀E² (facteur 2) ; dette d'estimation —
    P_K déclaré ne suit pas de ses propres intrants déclarés (0,5 MeV,
    3,9e-13 m → 1,35e24 Pa, facteur ~159). La machine pèse la déclaration
    globale « 6,5e-8 dérivé de (21) », pas l'estimation P_K seule.
    """
    from mvcg.dictionaries import SI_VACUUM
    t = load_table("lh_g11_LITTERATURE-2026.json")
    p = t["params"]
    eps0 = SI_VACUUM["epsilon0"]
    E = float(p["E_declare_V_m"])
    pk = float(p["P_K_declare_Pa"])
    dmm_decl = float(p["dmm_declare"])
    mu = eps0 * E * E / (8.0 * pk)
    mev_j = float(p["me_c2_declare_MeV"]) * 1e6 * 1.602176634e-19
    lam = float(p["lambda_C_declare_m"])
    pk_recompute = mev_j / lam ** 3
    return float(mu), {
        "table": t["vintage"],
        "table_sha256": t["_sha256"],
        "epsilon0": eps0,
        "E_V_m": E,
        "P_K_Pa": pk,
        "dmm_declare": dmm_decl,
        "dmm_recompute": mu,
        "delta": abs(mu - dmm_decl) / dmm_decl,
        "P_ext_declare_Pa": float(p["P_ext_declare_Pa"]),
        "dmm_avec_P_ext": float(p["P_ext_declare_Pa"]) / (8.0 * pk),
        "P_K_recompute_Pa": pk_recompute,
        "P_K_ratio_recompute_sur_declare": pk_recompute / pk,
        "note": "le recompute strict de (21) donne 1,302e-4, pas 6,5e-8 : le corpus a mis P_ext = ε₀E²/2 au numérateur (facteur 2, dette type PF5) et P_K déclaré ne suit pas de ses propres intrants (0,5 MeV, 3,9e-13 m → 1,35e24 Pa, facteur ~159) ; la prédiction expérimentale est donc doublement non tenue sur sa propre arithmétique",
    }
