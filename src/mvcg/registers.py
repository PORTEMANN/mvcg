#!/usr/bin/env python3
"""Trois registres = trois tiroirs de contacts, pas trois substances.

micro  — tables / formules (raie, Rydberg, masse)
meso   — partitions / profils (atlas, Dice, instrument)
macro  — bilans (H^2, Ω, vintage H0)
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable

import numpy as np

from mvcg.metrics import _delta, _verdict
from mvcg.rationalization import parse_units


REGISTERS = ("micro", "meso", "macro")


@dataclass
class Contact:
    id: str
    register: str
    orig: str
    packet: str
    dimension: str
    delta_kind: str
    theta: float
    mu_ref: float
    lever: str
    lever_off_note: str
    s_phrase: str
    note: str
    runner: str
    statut: str = "ouverte"
    expected: str | None = None
    campaign: str = ""
    gum: dict | None = None
    caliber: str = ""
    tare_note: str = ""
    chain: list | None = None


def _h1s_rydberg() -> tuple[float, dict]:
    from mvcg.tables import load_table

    c = load_table("codata2018_extract.json")["constants"]
    r_inf_ev = float(c["Rydberg_eV"])
    return -r_inf_ev, {"r_inf_ev": r_inf_ev, "n": 1, "vintage": "CODATA-2018"}


def _h1s_rydberg_vintage_off() -> tuple[float, dict]:
    """Levier vintage : R arrondi 13.6 eV."""
    return -13.6, {"r_inf_ev": 13.6, "lever": "vintage←13.6"}


def _dice(a: np.ndarray, b: np.ndarray) -> float:
    inter = float(np.sum(a == b))
    return 2.0 * inter / (a.size + b.size + 1e-15)


def _aal_dice_stable() -> tuple[float, dict]:
    """Partition synthétique : même atlas, lissage léger (proto, pas un cerveau)."""
    rng = np.random.default_rng(0)
    atlas = rng.integers(0, 8, size=(32, 32))
    # lissage = vote majoritaire 3x3
    pad = np.pad(atlas, 1, mode="edge")
    flat = np.lib.stride_tricks.sliding_window_view(pad, (3, 3))
    smooth = np.array([[np.bincount(flat[i, j].ravel()).argmax()
                        for j in range(32)] for i in range(32)])
    d = _dice(atlas, smooth)
    return d, {"n_labels": 8, "grid": 32, "lever_pending": "atlas←autre"}


def _p20_h2plus_lcao() -> tuple[float, dict]:
    from mvcg.h2plus import lcao_1s
    from mvcg.tables import h2plus_de

    t = h2plus_de()
    sol = lcao_1s(2.0)
    return float(sol["De_Ha"]), {
        "table": t["vintage"],
        "mu_ref_table": t["value"],
        "ansatz": "LCAO 1s Lowe R=2",
        "S": sol["S"],
        "E": sol["E"],
        "tare_Ha": sol["tare_Ha"],
        "caliber": "labo",
        "unit_raw": "Ha",
    }


def _p21_h2o_point_charge() -> tuple[float, dict]:
    from mvcg.tables import h2o_dipole

    t = h2o_dipole()
    return float(t["ansatz_point_charge"]), {"table": t["vintage"], "ref": t["value"]}


def _p30_kato_gaussian() -> tuple[float, dict]:
    from mvcg.tables import kato_h

    t = kato_h()
    return float(t["ansatz_gaussian"]), {"table": t["vintage"], "ref": t["value"]}


def _p30_kato_exact() -> tuple[float, dict]:
    from mvcg.tables import kato_h

    t = kato_h()
    return float(t["value"]), {"table": t["vintage"], "ansatz": "1s exact"}


def _p27_he_hf() -> tuple[float, dict]:
    from mvcg.balance import after_tare
    from mvcg.tables import he_corr

    t = he_corr()
    raw = float(t["E_HF_Ha"])
    tare = float(t["E_HF_Ha"])
    return after_tare(raw, tare), {
        "table": t["vintage"],
        "E_HF": t["E_HF_Ha"],
        "method": "HF",
        "tare_Ha": tare,
        "tare_note": "plateau vide = déterminant HF",
        "caliber": "labo",
    }


def _p27_he_table() -> tuple[float, dict]:
    from mvcg.tables import he_corr

    t = he_corr()
    return float(t["value"]), {"table": t["vintage"], "note": "tautologie table"}


def _fd_h1s_ha(n: int, r_max: float) -> float:
    """E_1s(H) en Ha par différences finies 2e ordre, Dirichlet aux deux bords."""
    import numpy as np

    h = r_max / (n + 1)
    r = np.arange(1, n + 1) * h
    V = -1.0 / r
    main = 1.0 / (h * h) + V
    off = -1.0 / (2.0 * h * h)
    H = (
        np.diag(main)
        + np.diag(np.full(n - 1, off), 1)
        + np.diag(np.full(n - 1, off), -1)
    )
    return float(np.linalg.eigvalsh(H)[0])


def _o1_grid_h1s() -> tuple[float, dict]:
    """Contact ouvert O1 — E_1s(H) par différences finies sur grille déclarée.

    Paramètres choisis avant le premier run : n=200, r_max=25 a0,
    différences finies 2e ordre, conditions de Dirichlet. L'erreur de
    discrétisation n'est PAS connue d'avance : c'est la pesée qui la dit.
    """
    from mvcg.tables import load_table

    n, r_max = 200, 25.0
    e1_ha = _fd_h1s_ha(n, r_max)
    t = load_table("codata2018_extract.json")
    return e1_ha, {
        "table": "codata2018_extract.json",
        "vintage": t["vintage"],
        "method": "differences finies 2e ordre, Dirichlet",
        "n": n,
        "r_max": r_max,
        "h": r_max / (n + 1),
        "ansatz": "grille uniforme (la grille est l'ansatz)",
        "lever": "grille<-raffiner",
        "unit_raw": "Ha",
    }


def _o2_co2_nu3() -> tuple[float, dict]:
    """Contact ouvert O2 — ν₃(CO₂) par transfert de constante de force.

    Règle déclarée AVANT le premier run : k_r(C=O du CO₂) := k(CO),
    extraite de la bande CO de la table par le modèle diatomique
    harmonique (k = μω², μ = m_C·m_O/(m_C+m_O)). Puis
    ν₃^harm = sqrt(2k_r/m_O)/(2πc). La bande ν₃ du CO₂ NE DOIT JAMAIS
    entrer dans le calcul : c'est l'anti-tautologie du contact.
    """
    import math

    from mvcg.tables import load_table

    amu = 1.66053906660e-27  # kg, déclarée locale
    c_cm = 2.99792458e10  # cm/s, exact
    m_C = 12.0 * amu  # masses conventionnelles déclarées
    m_O = 16.0 * amu
    mu_co = m_C * m_O / (m_C + m_O)
    t = load_table("co2_bands_LITERATURE-2018.json")
    bands = t["bands"]
    nu_co = float(bands["CO_nu01_cm-1"])
    omega_co = 2.0 * math.pi * c_cm * nu_co
    k = mu_co * omega_co**2
    nu3 = math.sqrt(2.0 * k / m_O) / (2.0 * math.pi * c_cm)
    return nu3, {
        "table": "co2_bands_LITERATURE-2018.json",
        "vintage": t["vintage"],
        "method": "VFF 1D harmonique, k_r transferee de CO",
        "rule": "k_r(C=O CO2) := k(CO)",
        "k_r_N_per_m": k,
        "nu_tilde_CO_cm-1": nu_co,
        "mu_CO_amu": mu_co / amu,
        "m_O_amu": 16.0,
        "ansatz": "transfert de constante de force (diatomique -> triatomique)",
        "lever": "k<-autre-liaison",
        "unit_raw": "cm^-1",
    }


def _o3_carbon_d_raman() -> tuple[float, dict]:
    """Contact ouvert O3 — bande D du graphite par chaîne 1D à forces égales.

    Règle déclarée AVANT le premier run : le graphite est une chaîne 1D
    diatomique de carbone (maille A-B, constantes k1 intra / k2 inter) ;
    la bande G = mode optique au centre de zone (ω² = 2(k1+k2)/m), la
    bande D = bord de zone (ω² = 2·max(k1,k2)/m, modes dégénérés).
    Transfert déclaré : k2 := k1 (égalisation) — le rapport vaut alors
    D/G = 1/√2. La bande D observée NE DOIT JAMAIS entrer dans le
    calcul : anti-tautologie du contact (seule G pilote la prédiction).
    D est le mode activé par le désordre : c'est lui qui distingue
    graphite (interdit, faible) et amorphe (permis) — le contact dit
    quelque chose sur cette frontière.
    """
    from mvcg.tables import load_table

    t = load_table("carbon_raman_LITERATURE-2018.json")
    bands = t["bands"]
    g_obs = float(bands["graphite_G_cm-1"])
    ratio = 1.0 / (2.0 ** 0.5)  # D/G à k2 = k1 : sqrt(max/(k1+k2))
    d_pred = g_obs * ratio
    return d_pred, {
        "table": "carbon_raman_LITERATURE-2018.json",
        "vintage": t["vintage"],
        "method": "chaine 1D diatomique, egalisation k2 := k1",
        "rule": "D = G / sqrt(2)",
        "k2_over_k1": 1.0,
        "G_obs_cm-1": g_obs,
        "D_over_G": ratio,
        "ansatz": "chaine diatomique 1D a constantes de force egales",
        "lever": "k<-desegaliser",
        "unit_raw": "cm^-1",
    }


def _o4_tk_id_ig() -> tuple[float, dict]:
    """Contact ouvert O4 — I_D/I_G par la loi de Tuinstra–Koenig.

    Règle déclarée AVANT le premier run : en phase 1 (domaines
    cristallins de quelques nm), I_D/I_G = C(λ)/L_a — chaque domaine
    contribue au D par ses bords et au G par son aire. C(λ = 514 nm)
    = 4,4 nm (constante empirique de la table), L_a = 3,0 nm (taille
    de domaine déclarée de l'échantillon suie/nanographite, dans la
    fenêtre de validité). Le rapport I_D/I_G observé NE DOIT JAMAIS
    entrer dans le calcul : anti-tautologie du contact (seuls C et L_a
    pilotent la prédiction).
    """
    from mvcg.tables import load_table

    t = load_table("carbon_disorder_LITERATURE-2018.json")
    p = t["params"]
    c_lambda = float(p["TK_C_lambda514_nm"])
    la = float(p["La_observed_nm"])
    pred = c_lambda / la
    return pred, {
        "table": "carbon_disorder_LITERATURE-2018.json",
        "vintage": t["vintage"],
        "method": "loi de Tuinstra-Koenig, phase 1",
        "rule": "ID/IG = C(lambda)/La",
        "C_lambda514_nm": c_lambda,
        "La_nm": la,
        "ansatz": "activation du D proportionnelle aux bords de domaine",
        "lever": "La<-recalibrer",
        "unit_raw": "1",
    }


def _o5_bec_sound() -> tuple[float, dict]:
    """Contact ouvert O5 — vitesse du son d'un condensat de Bose.

    Règle déclarée AVANT le premier run : régime de Bogolioubov pour un
    gaz dilué, c = sqrt(g n / m) avec g = 4 pi hbar^2 a_s / m, soit
    c = (hbar/m) sqrt(4 pi a_s n). Paramètres déclarés : masse du 87Rb,
    longueur de diffusion a_s = 100 a0, densité caractéristique du
    nuage n = 3e19 m^-3 (paramètre le moins contraint d'un nuage
    inhomogène — c'est là que vit le levier, documenté avant le run).
    La vitesse observée NE DOIT JAMAIS entrer dans le calcul :
    anti-tautologie du contact.
    """
    import math

    from mvcg.tables import load_table

    hbar = 1.054571817e-34  # J s (h exact / 2 pi)
    amu = 1.66053906660e-27  # kg, déclarée locale
    t = load_table("bec_sound_LITERATURE-2018.json")
    p = t["params"]
    m = float(p["mass_87Rb_u"]) * amu
    a_s = float(p["a_s_100a0_nm"]) * 1e-9
    n = float(p["n_cloud_m-3"])
    g = 4.0 * math.pi * hbar**2 * a_s / m
    c = math.sqrt(g * n / m)
    return c, {
        "table": "bec_sound_LITERATURE-2018.json",
        "vintage": t["vintage"],
        "method": "Bogolioubov dilue, c = sqrt(g n / m)",
        "rule": "c = (hbar/m) sqrt(4 pi a_s n)",
        "g_J_m3": g,
        "a_s_m": a_s,
        "n_m-3": n,
        "m_kg": m,
        "ansatz": "condensat homogene, interactions de contact, T = 0",
        "lever": "n<-profil",
        "unit_raw": "m/s",
    }


def _o6_grid_h1s_refined() -> tuple[float, dict]:
    """Contact ouvert O6 — E_1s(H) par la grille raffinée (levier d'O1).

    Même protocole qu'O1, même table (R∞ CODATA-2018), même chaîne
    Ha→eV, MÊME θ = 1e-3 gelé : le levier grille←raffiner est activé
    (n = 1600 au lieu de 200, r_max inchangé). L'erreur de
    discrétisation à n = 1600 n'est pas connue d'avance : seul son
    ordre (O(h²), h ÷ 8) est prédit. C'est le run qui dit le mot.
    """
    from mvcg.tables import load_table

    n, r_max = 1600, 25.0
    e1_ha = _fd_h1s_ha(n, r_max)
    t = load_table("codata2018_extract.json")
    return e1_ha, {
        "table": "codata2018_extract.json",
        "vintage": t["vintage"],
        "method": "differences finies 2e ordre, Dirichlet (grille raffinee)",
        "n": n,
        "r_max": r_max,
        "h": r_max / (n + 1),
        "ansatz": "grille uniforme raffinee (le levier d'O1, active)",
        "lever": "grille<-raffiner (actif)",
        "unit_raw": "Ha",
    }


def _p35_sigma_as_spike() -> tuple[float, dict]:
    """B3-FAIL déclaré : σ logistique n'est pas un spike. μ = 0 (overlap)."""
    return 0.0, {"model": "logistic_sigma", "target": "spike", "note": "réfuté"}


def _p20_h2plus_table_only() -> tuple[float, dict]:
    from mvcg.tables import h2plus_de

    t = h2plus_de()
    return float(t["value"]), {"table": t["vintage"], "note": "tautologie table=table"}


def _aal_dice_other_atlas() -> tuple[float, dict]:
    """Levier atlas←autre : permutation des labels + bruit de frontières."""
    rng = np.random.default_rng(0)
    atlas = rng.integers(0, 8, size=(32, 32))
    other = (atlas + 1) % 8
    other[rng.random(other.shape) < 0.15] = rng.integers(0, 8)
    d = _dice(atlas, other)
    return d, {"lever": "atlas←autre"}


def _friedmann_baryons_only() -> tuple[float, dict]:
    """1 - Ω_b  (bilan 'les connus suffisent', plat). vintage H0 déclaré, pas utilisé."""
    omega_b = 0.0493
    return 1.0 - omega_b, {"omega_b": omega_b, "H0_vintage": "Planck-2018", "flat": True}


def _friedmann_lcdm() -> tuple[float, dict]:
    """|1 - (Ω_m + Ω_Λ)|  — fermeture plate, millésime déclaré."""
    omega_m, omega_l = 0.315, 0.685
    return abs(1.0 - (omega_m + omega_l)), {
        "omega_m": omega_m, "omega_l": omega_l, "H0_vintage": "Planck-2018"
    }


def _friedmann_lcdm_shoes_H0() -> tuple[float, dict]:
    """Même Ω, autre vintage H0 — le levier ne doit PAS être une moyenne."""
    omega_m, omega_l = 0.315, 0.685
    return abs(1.0 - (omega_m + omega_l)), {
        "omega_m": omega_m, "omega_l": omega_l, "H0_vintage": "SH0ES",
        "note": "fermeture Ω indépendante de H0 ; H0 entrerait dans un autre μ",
    }


RUNNERS: dict[str, Callable[[], tuple[float, dict]]] = {
    "h1s_rydberg": _h1s_rydberg,
    "h1s_vintage": _h1s_rydberg_vintage_off,
    "aal_dice": _aal_dice_stable,
    "aal_other": _aal_dice_other_atlas,
    "frw_baryons": _friedmann_baryons_only,
    "frw_lcdm": _friedmann_lcdm,
    "frw_shoes": _friedmann_lcdm_shoes_H0,
    "p20_lcao": _p20_h2plus_lcao,
    "p20_table": _p20_h2plus_table_only,
    "p21_pc": _p21_h2o_point_charge,
    "p30_g": _p30_kato_gaussian,
    "p30_ex": _p30_kato_exact,
    "p35_sigma": _p35_sigma_as_spike,
    "p27_hf": _p27_he_hf,
    "p27_tab": _p27_he_table,
    "o1_grid_h1s": _o1_grid_h1s,
    "o2_co2_nu3": _o2_co2_nu3,
    "o3_carbon_d_raman": _o3_carbon_d_raman,
    "o4_tk_id_ig": _o4_tk_id_ig,
    "o5_bec_sound": _o5_bec_sound,
    "o6_grid_h1s_refined": _o6_grid_h1s_refined,
}

CONTACTS: list[Contact] = [
    Contact(
        "H1s_Rydberg", "micro", "pred", "si", "eV", "rel", 1e-12,
        -13.605693122994, "vintage←13.6", "voir H1s_Rydberg_13p6",
        "E_1s = -R_∞ (CODATA-2018 gelé)",
        "formule = constante déclarée ; pas un atome ontologique",
        "h1s_rydberg",
    ),
    Contact(
        "H1s_Rydberg_13p6", "micro", "pred", "si", "eV", "rel", 1e-12,
        -13.605693122994, "vintage←13.6 (actif)", "—",
        "même S, R arrondi",
        "levier vintage : doit casser un θ trop serré",
        "h1s_vintage",
    ),
    Contact(
        "P20_H2plus_LCAO", "micro", "pred", "si", "eV", "rel", 0.05,
        2.6508, "ansatz←table", "voir P20_H2plus_table",
        "De(H2+) LCAO 1s = table DEMO-2026",
        "ansatz pauvre vs constante déclarée ; pas un CCCBDB live",
        "p20_lcao",
    ),
    Contact(
        "P20_H2plus_table", "micro", "pred", "si", "eV", "rel", 1e-12,
        2.6508, "—", "—",
        "De(H2+) = table lue deux fois",
        "contrôle tautologique ; ne pas exporter comme P20",
        "p20_table",
        "ouverte", None, "P20",
    ),
    Contact(
        "P21_H2O_dipole", "micro", "pred", "si", "D", "rel", 0.05,
        1.8546, "ansatz←table", "—",
        "μ(H2O) charges ponctuelles = table DEMO-2026",
        "P21 rejoué en maquette",
        "p21_pc",
        "ouverte", "S-", "P21",
    ),
    Contact(
        "P30_Kato_gaussian", "micro", "pred", "1", "1", "abs", 0.05,
        -1.0, "ansatz←1s", "voir P30_Kato_1s",
        "(1/ψ)∂rψ|_0 = -Z  (gaussienne)",
        "P30 partiel d'origine : le continu lisse rate le cusp",
        "p30_g",
        "partielle", "S-", "P30",
    ),
    Contact(
        "P30_Kato_1s", "micro", "thm", "1", "1", "abs", 1e-12,
        -1.0, "—", "—",
        "(1/ψ)∂rψ|_0 = -1 pour 1s H exact",
        "identité de la 1s ; pas un solveur multi-corps",
        "p30_ex",
        "fermee", "S+", "P30",
    ),
    Contact(
        "P27_He_HF", "micro", "pred", "si", "Ha", "abs", 0.002,
        -0.042044, "methode←HF", "voir P27_He_table",
        "E_corr(He, HF) = table Hylleraas",
        "HF ne récupère aucune corrélation ; S− obligatoire",
        "p27_hf",
        "fermee", "S-", "P27",
    ),
    Contact(
        "P27_He_table", "micro", "pred", "si", "Ha", "abs", 1e-12,
        -0.042044, "—", "—",
        "E_corr(He) = table lue deux fois",
        "contrôle tautologique",
        "p27_tab",
        "ouverte", None, "P27",
    ),
    Contact(
        "P35_sigma_spike", "meso", "proto", "1", "1", "abs", 0.05,
        1.0, "modele←HH", "—",
        "σ logistique recouvre le spike",
        "B3-FAIL déclaré : overlap 0 vs 1",
        "p35_sigma",
        "fermee", "S-", "P35",
    ),
    Contact(
        "AAL_dice_lissage", "meso", "proto", "1", "1", "abs", 0.05,
        1.0, "atlas←autre", "voir AAL_dice_atlas",
        "Dice(atlas, atlas lissé 3×3) ≈ 1",
        "partition synthétique ; pas une carte cérébrale",
        "aal_dice",
    ),
    Contact(
        "AAL_dice_atlas", "meso", "proto", "1", "1", "abs", 0.05,
        1.0, "atlas←autre (actif)", "—",
        "Dice(atlas, autre atlas)",
        "levier atlas : prévision mot_change",
        "aal_other",
    ),
    Contact(
        "FRW_baryons", "macro", "pred", "1", "1", "abs", 0.05,
        0.0, "Ω_c←0 déjà", "ajouter Ω_c+Ω_Λ",
        "1-Ω_b = 0  (les connus ferment le bilan plat)",
        "H0 vintage Planck-2018 gelé ; S- attendu",
        "frw_baryons",
    ),
    Contact(
        "FRW_lcdm_Planck", "macro", "pred", "1", "1", "abs", 1e-3,
        0.0, "H0←SH0ES en contact séparé", "voir FRW_lcdm_SH0ES",
        "|1-(Ω_m+Ω_Λ)|=0  millésime Planck Ω",
        "fermeture plate ; H0 n'entre pas dans ce μ",
        "frw_lcdm",
    ),
    Contact(
        "FRW_lcdm_SH0ES", "macro", "pred", "1", "1", "abs", 1e-3,
        0.0, "H0 vintage SH0ES (même Ω)", "—",
        "même fermeture Ω, autre étiquette H0",
        "montre que CE μ ignore H0 — un vrai contact H0 serait H(z) vs donnée",
        "frw_shoes",
    ),
    Contact(
        "O1_Grille_H1s", "micro", "pred", "si", "eV", "rel", 1e-3,
        -13.605693122994, "grille←raffiner", "—",
        "E_1s(H) par différences finies (n=200, r_max=25) = R_∞ CODATA-2018",
        "contact ouvert O1 : le mot n'était pas connu avant le gel du protocole",
        "o1_grid_h1s",
        "ouverte", None, "O1",
    ),
    Contact(
        "O2_CO2_nu3", "micro", "pred", "1", "cm^-1", "rel", 0.10,
        2349.3, "k<-autre-liaison", "—",
        "nu3(CO2) VFF a k transferee de CO = bande IR observee (12CO2)",
        "contact ouvert O2 : transfert declare, mot inconnu au gel ; theta=0.10 fige avant run (labo + modele 1D grossier)",
        "o2_co2_nu3",
        "ouverte", None, "O2",
    ),
    Contact(
        "O3_Carbon_D_Raman", "micro", "pred", "1", "cm^-1", "rel", 0.10,
        1350.0, "k<-desegaliser", "—",
        "bande D(graphite) = bande G / sqrt(2) (chaine 1D k2=k1) = bande D observee",
        "contact ouvert O3 : egalisation declaree, mot inconnu au gel ; theta=0.10 fige avant run (tol. labo + modele 1D grossier)",
        "o3_carbon_d_raman",
        "ouverte", None, "O3",
    ),
    Contact(
        "O4_TK_ID_IG", "micro", "pred", "1", "1", "rel", 0.10,
        1.2, "La<-recalibrer", "—",
        "ID/IG(suie, La=3nm) = C(514nm)/La = rapport Raman observe",
        "contact ouvert O4 : loi Tuinstra-Koenig declaree, mot inconnu au gel ; theta=0.10 fige avant run (rapport d'intensites inter-labo)",
        "o4_tk_id_ig",
        "ouverte", None, "O4",
    ),
    Contact(
        "O5_BEC_Sound", "micro", "pred", "si", "m/s", "rel", 0.05,
        0.0011, "n<-profil", "—",
        "c(son, 87Rb) = sqrt(4 pi hbar^2 a_s n / m^2) = vitesse du son observee",
        "contact ouvert O5 : Bogolioubov declare, mot inconnu au gel ; theta=0.05 fige avant run (accord inter-labo + incertitude de densite du nuage)",
        "o5_bec_sound",
        "ouverte", None, "O5",
    ),
    Contact(
        "O6_Grille_H1s_Raffine", "micro", "pred", "si", "eV", "rel", 1e-3,
        -13.605693122994, "grille<-raffiner (actif)", "—",
        "E_1s(H) par differences finies (n=1600, r_max=25) = R_inf CODATA-2018",
        "contact ouvert O6 : le levier d'O1 active, theta=1e-3 INCHANGE (seuil gelé d'O1) ; mot inconnu au gel",
        "o6_grid_h1s_refined",
        "ouverte", None, "O6",
    ),
]

# GUM — lignes B de table seulement. Pas d'u_B « erreur de modèle ».
_GUM = {c.id: None for c in CONTACTS}
_GUM["H1s_Rydberg"] = {
    "decide": "U",
    "k": 2,
    "lines": [{"name": "Rinf_CODATA2018", "type": "B", "u": 1.9e-12, "note": "u_rel R_∞"}],
}
_GUM["P27_He_HF"] = {
    "decide": "U",
    "k": 2,
    "lines": [{"name": "Ecorr_table", "type": "B", "u": 1e-6, "note": "Ha, table Hylleraas"}],
}
_GUM["P20_H2plus_LCAO"] = {
    "decide": "theta",
    "k": 2,
    "lines": [{"name": "De_table", "type": "B", "u": 0.0005, "note": "eV table ; pas l'erreur LCAO"}],
}
for _c in CONTACTS:
    if _GUM.get(_c.id):
        _c.gum = _GUM[_c.id]

from mvcg.h2plus import HA_TO_EV

for _c in CONTACTS:
    if _c.id in ("P20_H2plus_LCAO", "O1_Grille_H1s", "O6_Grille_H1s_Raffine"):
        _c.chain = [{
            "tau": "energy",
            "src": "Ha",
            "dst": "eV",
            "k": HA_TO_EV,
        }]


def run_contact(c: Contact) -> dict[str, Any]:
    from mvcg.runner import execute

    mu_loc, extra = execute(RUNNERS[c.runner], chain=c.chain)
    delta = _delta(mu_loc, c.mu_ref, c.delta_kind)
    if c.gum:
        from mvcg.gum import apply_gum

        g = apply_gum(delta, c.theta, c.gum)
        verdict = g["verdict"]
        extra = {**extra, "gum": g}
    else:
        verdict = _verdict(delta, c.theta)
    units_kill = None
    try:
        U = parse_units(
            {"packet": c.packet, "vintage": "registre"},
            dimension=c.dimension,
        )
        packet = U.packet
    except (ValueError, TypeError, KeyError) as exc:
        U = None
        packet = c.packet
        units_kill = str(exc)
        verdict = "S-"
    chain_kill = extra.get("chain_kill")
    if chain_kill:
        # μ est en unités brutes : le mot serait calculé sur la mauvaise fibre.
        if not units_kill:
            units_kill = f"chain: {chain_kill}"
        verdict = "S-"
    return {
        "id": c.id,
        "register": c.register,
        "orig": c.orig,
        "s": c.s_phrase,
        "lever": c.lever,
        "mu_loc": mu_loc,
        "mu_ref": c.mu_ref,
        "theta": c.theta,
        "delta": delta,
        "verdict": verdict,
        "dimension": c.dimension,
        "packet": packet,
        "note": c.note,
        "extra": extra,
        "caliber": extra.get("caliber") or c.caliber,
        "tare": extra.get("tare_Ha") or extra.get("tare"),
        "units_kill": units_kill,
        "chain_kill": chain_kill,
        "statut": c.statut,
        "expected": c.expected,
        "campaign": c.campaign,
        "b3_fail": bool(c.expected and verdict != c.expected),
    }


def run_registers() -> dict[str, Any]:
    rows = [run_contact(c) for c in CONTACTS]
    by = {r: [x for x in rows if x["register"] == r] for r in REGISTERS}
    return {
        "protocol": "MVC-G-REGISTRES-0.1",
        "warning": "trois tiroirs, pas trois substances ; S+ ne s'exporte pas",
        "counts": {
            r: {
                "n": len(by[r]),
                "S+": sum(1 for x in by[r] if x["verdict"] == "S+"),
                "P": sum(1 for x in by[r] if x["verdict"] == "P"),
                "S-": sum(1 for x in by[r] if x["verdict"] == "S-"),
            }
            for r in REGISTERS
        },
        "rows": rows,
    }
