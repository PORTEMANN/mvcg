#!/usr/bin/env python3
"""Trois registres = trois tiroirs de contacts, pas trois substances.

micro  — tables / formules (raie, Rydberg, masse)
meso   — partitions / profils (atlas, Dice, instrument)
macro  — bilans (H^2, Ω, vintage H0)
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

import math

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


def _o7_carbon_d_lever() -> tuple[float, dict]:
    """Contact ouvert O7 — levier d'O3 activé (k₂/k₁ = 3 déclaré).

    Même modèle que O3 (chaîne 1D diatomique, G du graphite pilote la
    prédiction, la bande D observée ne participe JAMAIS au calcul),
    MÊME θ = 0,10 gelé. Le levier k<-desegaliser est activé : le
    rapport effectif r = k2/k1 = 3,0 est déclaré dans une table
    vintage dédiée (paramètre effectif du modèle 1D — pas une
    constante mesurée ; c'est écrit dans la table). D = G·√(r/(1+r)).
    Seul r a bougé : le seuil et la référence sont ceux d'O3.
    """
    import math

    from mvcg.tables import load_table

    t = load_table("carbon_raman_LITERATURE-2018.json")
    tf = load_table("carbon_raman_forces_LITERATURE-2018.json")
    bands = t["bands"]
    g_obs = float(bands["graphite_G_cm-1"])
    r = float(tf["params"]["k2_over_k1"])
    ratio = math.sqrt(max(1.0, r) / (1.0 + r))
    d_pred = g_obs * ratio
    return d_pred, {
        "table": "carbon_raman_LITERATURE-2018.json",
        "table_forces": "carbon_raman_forces_LITERATURE-2018.json",
        "vintage": t["vintage"],
        "method": "chaine 1D diatomique, levier k<-desegaliser (actif)",
        "rule": "D = G * sqrt(r/(1+r)), r = k2/k1 = 3",
        "k2_over_k1": r,
        "G_obs_cm-1": g_obs,
        "D_over_G": ratio,
        "ansatz": "parametre effectif inter/intra declare (non mesure)",
        "lever": "k<-desegaliser (actif)",
        "unit_raw": "cm^-1",
    }


def _o8_bec_tc() -> tuple[float, dict]:
    """Contact ouvert O8 — T_c d'un gaz de Bose (condensat idéal).

    Règle déclarée AVANT le premier run : gaz de Bose idéal dilué,
    T_c = (2 pi hbar^2 / m k_B) (n / 2,612)^{2/3}. Paramètres déclarés :
    masse 87Rb, densité n = 3e19 m^-3 (même nuage déclaré qu'O5).
    La T_c observée NE DOIT JAMAIS entrer dans le calcul. Suspense réel :
    les interactions déplacent T_c de quelques % à plus de 10 % selon
    les mesures.
    """
    import math

    from mvcg.tables import load_table

    hbar = 1.054571817e-34
    k_B = 1.380649e-23  # exact
    amu = 1.66053906660e-27
    t = load_table("bec_tc_LITERATURE-2018.json")
    p = t["params"]
    m = float(p["mass_87Rb_u"]) * amu
    n = float(p["n_cloud_m-3"])
    tc_k = (2.0 * math.pi * hbar**2 / (m * k_B)) * (n / 2.612) ** (2.0 / 3.0)
    tc_nk = tc_k * 1e9
    return tc_nk, {
        "table": "bec_tc_LITERATURE-2018.json",
        "vintage": t["vintage"],
        "method": "gaz de Bose ideal, transition en n^(2/3)",
        "rule": "Tc = (2 pi hbar^2 / m kB) (n/2.612)^(2/3)",
        "Tc_K": tc_k,
        "n_m-3": n,
        "ansatz": "condensat ideal, interactions negligees",
        "lever": "n<-densite-effective",
        "unit_raw": "nK",
    }


def _o9_h2o_pauling() -> tuple[float, dict]:
    """Contact ouvert O9 — moment dipolaire de H2O par électronégativités.

    Règle déclarée AVANT le premier run : charge partielle d'après
    l'échelle de Pauling, q = (chi_O - chi_H) / 2,25 (en e), géométrie
    déclarée (r_OH = 0,958 Å, angle 104,5°), mu = 2 q r cos(angle/2).
    Le moment observé NE DOIT JAMAIS entrer dans le calcul.
    """
    import math

    from mvcg.tables import load_table

    e_A_to_D = 4.80320427  # 1 e·Å en D, déclarée locale
    t = load_table("h2o_pauling_LITERATURE-2018.json")
    p = t["params"]
    q = (float(p["chi_O"]) - float(p["chi_H"])) / float(p["pauling_scale_eV"])
    r = float(p["r_OH_A"])
    ang = math.radians(float(p["angle_deg"]))
    mu_eA = 2.0 * q * r * math.cos(ang / 2.0)
    mu_d = mu_eA * e_A_to_D
    return mu_d, {
        "table": "h2o_pauling_LITERATURE-2018.json",
        "vintage": t["vintage"],
        "method": "charges partielles par electronegativite de Pauling",
        "rule": "q = dChi/2.25 ; mu = 2 q r cos(angle/2)",
        "q_e": q,
        "r_OH_A": r,
        "angle_deg": float(p["angle_deg"]),
        "ansatz": "ionicite d'echelle, polarisation negligee",
        "lever": "q<-polarisation",
        "unit_raw": "D",
    }


def _o10_carbonyl() -> tuple[float, dict]:
    """Contact ouvert O10 — bande carbonyle du PMMA par transfert de force.

    Règle déclarée AVANT le premier run : k(C=O ester) := k(C=O
    formaldehyde), extraite par le modele harmonique k = mu omega^2
    (mu identique : liaisons C=O de memes atomes) ; nu_ester =
    sqrt(k/mu)/(2 pi c). La bande PMMA observée NE DOIT JAMAIS entrer
    dans le calcul. Suspense minimal assumé au gel : le transfert entre
    liaisons de memes atomes est le cas le plus favorable du geste O2.
    """
    import math

    from mvcg.tables import load_table

    amu = 1.66053906660e-27
    c_cm = 2.99792458e10
    t = load_table("pmma_carbonyl_LITERATURE-2018.json")
    p = t["params"]
    nu_ch2o = float(p["nu_CH2O_cm-1"])
    m_c = 12.0 * amu
    m_o = 16.0 * amu
    mu = m_c * m_o / (m_c + m_o)
    omega = 2.0 * math.pi * c_cm * nu_ch2o
    k = mu * omega**2
    nu_ester = math.sqrt(k / mu) / (2.0 * math.pi * c_cm)
    return nu_ester, {
        "table": "pmma_carbonyl_LITERATURE-2018.json",
        "vintage": t["vintage"],
        "method": "transfert de constante de force CH2O -> ester",
        "rule": "k(C=O ester) := k(C=O CH2O)",
        "k_r_N_per_m": k,
        "nu_CH2O_cm-1": nu_ch2o,
        "ansatz": "liaisons de memes atomes : masse reduite identique",
        "lever": "k<-conjugaison",
        "unit_raw": "cm^-1",
    }


def _o11_bec_healing() -> tuple[float, dict]:
    """Contact ouvert O11 — longueur de guérison du condensat.

    Règle déclarée AVANT le premier run : Bogolioubov, xi =
    1/sqrt(8 pi n a_s). Paramètres déclarés : n = 3e19 m^-3,
    a_s = 100 a0 (même nuage qu'O5). La valeur observée NE DOIT JAMAIS
    entrer dans le calcul.
    """
    import math

    from mvcg.tables import load_table

    t = load_table("bec_healing_LITERATURE-2018.json")
    p = t["params"]
    n = float(p["n_cloud_m-3"])
    a_s = float(p["a_s_100a0_nm"]) * 1e-9
    xi_m = 1.0 / math.sqrt(8.0 * math.pi * n * a_s)
    xi_um = xi_m * 1e6
    return xi_um, {
        "table": "bec_healing_LITERATURE-2018.json",
        "vintage": t["vintage"],
        "method": "Bogolioubov, longueur de guerison",
        "rule": "xi = 1/sqrt(8 pi n a_s)",
        "xi_m": xi_m,
        "n_m-3": n,
        "a_s_m": a_s,
        "ansatz": "condensat homogene, interactions de contact",
        "lever": "n<-densite-effective",
        "unit_raw": "um",
    }


def _o12_cu_gamma() -> tuple[float, dict]:
    """Contact ouvert O12 — chaleur spécifique électronique du cuivre.

    Règle déclarée AVANT le premier run : modèle de Sommerfeld avec
    masse LIBRE, gamma = pi^2 k_B^2 n / (2 E_F), E_F = hbar^2
    (3 pi^2 n)^{2/3} / (2 m_e). La mesure du cuivre NE DOIT JAMAIS
    entrer dans le calcul. Estimation pré-run honnête : le modèle à
    masse libre sous-estime gamma (~27 % d'écart) — c'est le S-
    historique qui a révélé la masse effective. Levier :
    m <- masse effective (1,38 m_e dans les solides).
    """
    import math

    from mvcg.tables import load_table

    hbar = 1.054571817e-34
    k_B = 1.380649e-23
    m_e = 9.1093837015e-31  # kg, déclarée locale
    t = load_table("cu_gamma_LITERATURE-2018.json")
    p = t["params"]
    n = float(p["n_e_m-3"])
    e_f = hbar**2 * (3.0 * math.pi**2 * n) ** (2.0 / 3.0) / (2.0 * m_e)
    gamma = math.pi**2 * k_B**2 * n / (2.0 * e_f)
    return gamma, {
        "table": "cu_gamma_LITERATURE-2018.json",
        "vintage": t["vintage"],
        "method": "Sommerfeld, masse libre",
        "rule": "gamma = pi^2 kB^2 n / (2 E_F)",
        "E_F_J": e_f,
        "E_F_eV": e_f / 1.602176634e-19,
        "n_m-3": n,
        "ansatz": "gaz d'electrons libres, masse = m_e",
        "lever": "m<-masse-effective",
        "unit_raw": "J m^-3 K^-2",
    }


def _o13_co2_isotopologue() -> tuple[float, dict]:
    """Contact ouvert O13 — bande ν₃ du 13CO2 par la loi des masses.

    Règle déclarée AVANT le premier run : isotopologue plus lourd,
    fréquence réduite par la masse réduite, nu(13) = nu(12)·√(μ12/μ13),
    μ = m_C·m_O/(m_C+m_O), masses conventionnelles 12/16 et 13/16.
    La bande cible du 13CO2 (2273,7 cm⁻¹) NE DOIT JAMAIS entrer dans
    le calcul : seule la bande du 12CO2 pilote (règle isotopique).
    """
    import math

    from mvcg.tables import load_table

    t = load_table("co2_bands_LITERATURE-2018.json")
    bands = t["bands"]
    nu12 = float(bands["CO2_nu3_cm-1"])
    mu12 = 12.0 * 16.0 / (12.0 + 16.0)
    mu13 = 13.0 * 16.0 / (13.0 + 16.0)
    nu13 = nu12 * math.sqrt(mu12 / mu13)
    return nu13, {
        "table": "co2_bands_LITERATURE-2018.json",
        "vintage": t["vintage"],
        "method": "loi des masses (isotopologue), masse reduite",
        "rule": "nu(13CO2) = nu(12CO2) * sqrt(mu12/mu13)",
        "mu12_amu": mu12,
        "mu13_amu": mu13,
        "nu_12CO2_cm-1": nu12,
        "ansatz": "deplacement isotopique, constante de force inchangee",
        "lever": "k<-anharmonicite",
        "unit_raw": "cm^-1",
    }


def _o14_tk_window() -> tuple[float, dict]:
    """Contact ouvert O14 — loi de Tuinstra–Koenig DANS sa fenêtre.

    Pendant d'O4 : même loi, autre échantillon. Règle déclarée AVANT
    le premier run : I_D/I_G = C(λ)/L_a avec C = 4,4 nm (même constante
    empirique) et L_a = 10 nm (charbon graphitisé, cœur de la fenêtre
    de phase 1). Le rapport observé NE DOIT JAMAIS entrer dans le
    calcul. Avec O4, la loi devient une carte : échec à 3 nm, test à
    10 nm.
    """
    from mvcg.tables import load_table

    t = load_table("carbon_tk_window_LITERATURE-2018.json")
    p = t["params"]
    c_lambda = float(p["TK_C_lambda514_nm"])
    la = float(p["La_nm"])
    pred = c_lambda / la
    return pred, {
        "table": "carbon_tk_window_LITERATURE-2018.json",
        "vintage": t["vintage"],
        "method": "loi de Tuinstra-Koenig, phase 1 (fenetre)",
        "rule": "ID/IG = C(lambda)/La, La = 10 nm",
        "C_lambda514_nm": c_lambda,
        "La_nm": la,
        "ansatz": "activation du D proportionnelle aux bords de domaine",
        "lever": "La<-recalibrer",
        "unit_raw": "1",
    }


def _o15_h2_harmonic() -> tuple[float, dict]:
    """Contact ouvert O15 — constante harmonique du H2 par force déclarée.

    Règle déclarée AVANT le premier run : oscillateur harmonique,
    nu_harm = sqrt(k/mu)/(2 pi c), k = 510 N/m (constante de force de
    Morse au minimum, valeur usuelle déclarée), mu = m_H/2. Comparaison
    HONNÊTE : contre omega_e = 4401,2 cm⁻¹ (constante HARMONIQUE
    expérimentale), pas contre le fondamental anharmonique (4160).
    La cible omega_e NE DOIT JAMAIS entrer dans le calcul.
    """
    import math

    from mvcg.tables import load_table

    amu = 1.66053906660e-27
    c_cm = 2.99792458e10
    t = load_table("h2_vibration_LITERATURE-2018.json")
    p = t["params"]
    k = float(p["k_H2_N_per_m"])
    m_h = 1.007825 * amu
    mu = m_h / 2.0
    omega = math.sqrt(k / mu)
    nu_harm = omega / (2.0 * math.pi * c_cm)
    return nu_harm, {
        "table": "h2_vibration_LITERATURE-2018.json",
        "vintage": t["vintage"],
        "method": "oscillateur harmonique, k de Morse declaree",
        "rule": "nu_harm = sqrt(k/mu)/(2 pi c), mu = m_H/2",
        "k_N_per_m": k,
        "mu_amu": mu / amu,
        "ansatz": "harmonique pur ; l'anharmonicite est la dette attendue",
        "lever": "k<-morse",
        "unit_raw": "cm^-1",
    }


def _o16_cu_gamma_eff() -> tuple[float, dict]:
    """Contact ouvert O16 — levier d'O12 activé : masse effective.

    Règle déclarée AVANT le premier run : même modèle de Sommerfeld
    qu'O12, même densité, mais la masse déclarée est la masse
    effective de bande m* = 1,38 m_e (valeur des solides, Ashcroft-
    Mermin), JAMAIS dérivée de la référence (γ_ref/γ_modèle = 1,37
    serait circulaire : la référence entrerait dans le calcul).
    γ ∝ m : γ(m*) = γ(m_e libre, O12) × 1,38. La mesure du cuivre
    NE DOIT JAMAIS entrer dans le calcul. Estimation pré-run honnête :
    δ ≈ 1 % — suspense faible assumé au gel : c'est le pendant
    disciplinaire d'O7 (chaque échec a son levier activé, θ jamais
    déplacé).
    """
    import math

    from mvcg.tables import load_table

    hbar = 1.054571817e-34
    k_B = 1.380649e-23
    m_e = 9.1093837015e-31  # kg, déclarée locale
    m_star_over_me = 1.38  # déclarée (bande), pas calculée depuis gamma_ref
    t = load_table("cu_gamma_LITERATURE-2018.json")
    p = t["params"]
    n = float(p["n_e_m-3"])
    m_eff = m_star_over_me * m_e
    e_f = hbar**2 * (3.0 * math.pi**2 * n) ** (2.0 / 3.0) / (2.0 * m_eff)
    gamma = math.pi**2 * k_B**2 * n / (2.0 * e_f)
    return gamma, {
        "table": "cu_gamma_LITERATURE-2018.json",
        "vintage": t["vintage"],
        "method": "Sommerfeld, masse effective declaree (bande)",
        "rule": "gamma = pi^2 kB^2 n / (2 E_F), E_F a m* = 1.38 m_e",
        "E_F_J": e_f,
        "E_F_eV": e_f / 1.602176634e-19,
        "n_m-3": n,
        "m_star_over_me": m_star_over_me,
        "ansatz": "gaz d'electrons, masse de bande (levier d'O12 active)",
        "lever": "m<-masse-effective (active, 1.38 m_e)",
        "unit_raw": "J m^-3 K^-2",
    }


def _o17_h2_anharmonic() -> tuple[float, dict]:
    """Contact ouvert O17 — fondamental du H2 par Dunham ordre 1.

    Règle déclarée AVANT le premier run : nu_pred(1-0) = omega_e -
    2*omega_e x_e, extraits declares Huber & Herzberg (table
    h2_anharmonic_LITERATURE-2018.json). mu_ref = 4160.0 cm^-1, le
    fondamental declare repris de la note de la table h2_vibration
    (meme gel que O15) : la dette promise par O15. La reference NE DOIT
    JAMAIS entrer dans le calcul. La tare assumee : la reference est un
    arrondi au cm^-1 (u=0.5 declaree) — le contact pese la tare de
    declaration, pas la physique anharmonique (nu_pred ~ 4158.5 est la
    physique correcte). Estimation pre-run honnete : delta ~ 1.48 cm^-1,
    theta = u_delta ~ 0.5026 cm^-1 (convention GUM k=1, precedent
    Rydberg voie 2), ratio ~ 2.94 -> P au cheveu de la borne S- ;
    suspense reel annonce au gel, mot inconnu.
    """
    from mvcg.tables import load_table

    t = load_table("h2_anharmonic_LITERATURE-2018.json")
    p = t["params"]
    omega_e = float(p["omega_e_cm-1"])
    omega_ex_e = float(p["omega_ex_e_cm-1"])
    nu_pred = omega_e - 2.0 * omega_ex_e
    return nu_pred, {
        "table": "h2_anharmonic_LITERATURE-2018.json",
        "vintage": t["vintage"],
        "method": "developpement de Dunham ordre 1, constantes declarees",
        "rule": "nu(1-0) = omega_e - 2 omega_e x_e",
        "omega_e_cm-1": omega_e,
        "omega_ex_e_cm-1": omega_ex_e,
        "nu10_declared_cm-1": float(p["nu10_declared_cm-1"]),
        "ansatz": "Dunham ordre 1 ; dette assumee = arrondi de declaration du fondamental (u=0.5 declaree)",
        "lever": "—",
        "unit_raw": "cm^-1",
    }


def _o18_h2_tare_lecture() -> tuple[float, dict]:
    """Contact ouvert O18 — tare de lecture, pendant disciplinaire d'O17.

    Règle déclarée AVANT le premier run : MÊME transport Dunham que O17
    (nu_pred = omega_e - 2*omega_e x_e, mêmes extraits gelés), MÊME
    référence 4160, même delta attendu (~1.48 cm^-1). Une seule chose
    change, gelée avant run : la lecture de précision de la référence —
    u = 5/sqrt(3) = 2.886751345948129 (arrondi au dizaine, demi-largeur
    5) au lieu de l'over-read u = 0.5 d'O17. La référence NE DOIT JAMAIS
    entrer dans le calcul. Estimation pré-run honnête : delta ~ 1.48,
    theta = u_delta = 2.887201644037585 cm^-1, ratio ~ 0.5126 -> S+
    attendu SANS suspense (bande vérifiée contre _adc : S+ = [0, theta],
    P = [theta, 2 theta]). Le suspense n'est pas dans le mot : il est
    dans la démonstration — même physique, même écart, verdict opposé,
    parce que le verdict pèse des déclarations, pas des physiques.
    """
    from mvcg.tables import load_table

    t = load_table("h2_tare_lecture_LITERATURE-2018.json")
    p = t["params"]
    omega_e = float(p["omega_e_cm-1"])
    omega_ex_e = float(p["omega_ex_e_cm-1"])
    nu_pred = omega_e - 2.0 * omega_ex_e
    return nu_pred, {
        "table": "h2_tare_lecture_LITERATURE-2018.json",
        "vintage": t["vintage"],
        "method": "developpement de Dunham ordre 1, constantes declarees (memes gel qu'O17)",
        "rule": "nu(1-0) = omega_e - 2 omega_e x_e",
        "omega_e_cm-1": omega_e,
        "omega_ex_e_cm-1": omega_ex_e,
        "nu10_declared_cm-1": float(p["nu10_declared_cm-1"]),
        "ansatz": "lecture honnete de la reference arrondie (u = 5/sqrt(3)) ; pendant d'O17",
        "lever": "lecture<-honnête (pendant d'O17)",
        "unit_raw": "cm^-1",
    }


def _p31_lamb_dirac() -> tuple[float, dict]:
    """Contact ouvert P31 — Lamb : Dirac seul predit la degenerescence.

    Règle déclarée AVANT le premier run : Dirac (equation relativiste a
    un electron dans le champ Coulombien du proton) place 2S1/2 et 2P1/2
    degenerees : le deplacement de Lamb predit est 0. Score normalise
    (grammaire de P30_Kato_gaussian) : mu_loc = 0, mu_ref = 1 (la
    mesure, normalisee). La mesure brute NE DOIT JAMAIS entrer dans le
    calcul. Estimation pre-run honnete : delta = 1,0 -> S- a 20 theta,
    SANS suspense — la machine quantifie la dette historique qui a fait
    naitre la QED (Lamb-Retherford 1947).
    """
    from mvcg.tables import load_table

    t = load_table("lamb_shift_P31_LITERATURE-1981.json")
    return 0.0, {
        "table": "lamb_shift_P31_LITERATURE-1981.json",
        "vintage": t["vintage"],
        "method": "Dirac seul : degenerescence 2S1/2 = 2P1/2 (shift 0), score normalise",
        "rule": "mu_loc = 0 (degenere) vs 1 (mesure normalisee)",
        "ansatz": "Dirac 1928-1947, sans corrections radiatives",
        "lever": "—",
        "unit_raw": "1",
    }


def _p31_lamb_mohr() -> tuple[float, dict]:
    """Contact ouvert P31 — Lamb : calcul QED Mohr (annees 1970) vs mesure.

    Règle déclarée AVANT le premier run : mu_loc = 1057.864 MHz (calcul
    QED Mohr declare, u = 0.014), mu_ref = 1057.845 MHz (mesure
    Lundeen-Pipkin 1981 declaree, u = 0.009). La reference NE DOIT
    JAMAIS entrer dans le calcul. theta = u_delta =
    0.016643316977093238 MHz, decide=U, k=1 (convention GUM, precedents
    Rydberg voie 2 / O17 / O18). Estimation pre-run honnete : delta ~
    0.019 -> ratio ~ 1.14 -> P au cheveu de S+ annonce (bande P =
    [theta, 2 theta], verifiee contre _adc). Suspense reel, mot inconnu
    au gel : a l'epoque, mesure et calcul QED se disputaient a ~1 sigma.
    """
    from mvcg.tables import load_table

    t = load_table("lamb_shift_P31_LITERATURE-1981.json")
    p = t["params"]
    mu = float(p["mohr_theory_MHz"])
    return mu, {
        "table": "lamb_shift_P31_LITERATURE-1981.json",
        "vintage": t["vintage"],
        "method": "calcul QED Mohr (annees 1970), valeur declaree",
        "rule": "Lamb(QED Mohr) = Lamb(mesure Lundeen-Pipkin 1981)",
        "mohr_theory_MHz": mu,
        "lamb_measured_MHz": float(p["lamb_measured_MHz"]),
        "ansatz": "QED ordre alpha (Bethe 1947 et suivants), vintage annees 1970",
        "lever": "—",
        "unit_raw": "MHz",
    }


def _p31_lamb_erickson() -> tuple[float, dict]:
    """Contact ouvert P31 — Lamb : calcul QED Erickson (annees 1970) vs mesure.

    Règle déclarée AVANT le premier run : mu_loc = 1057.912 MHz (calcul
    QED Erickson declare, u = 0.011), mu_ref = 1057.845 MHz (mesure
    Lundeen-Pipkin 1981 declaree, u = 0.009). La reference NE DOIT
    JAMAIS entrer dans le calcul. theta = u_delta =
    0.014212670403551895 MHz, decide=U, k=1. Estimation pre-run honnete
    : delta ~ 0.067 -> ratio ~ 4.71 -> S- attendu, SANS suspense —
    Lundeen & Pipkin ecrivaient eux-memes « not in good agreement with
    theory » (PRL 46, 232, 1981). Deux calculs QED de la meme epoque,
    deux verdicts attendus differents : la machine pese des declarations,
    elle ne sacralise pas « la theorie ».
    """
    from mvcg.tables import load_table

    t = load_table("lamb_shift_P31_LITERATURE-1981.json")
    p = t["params"]
    mu = float(p["erickson_theory_MHz"])
    return mu, {
        "table": "lamb_shift_P31_LITERATURE-1981.json",
        "vintage": t["vintage"],
        "method": "calcul QED Erickson (annees 1970), valeur declaree",
        "rule": "Lamb(QED Erickson) = Lamb(mesure Lundeen-Pipkin 1981)",
        "erickson_theory_MHz": mu,
        "lamb_measured_MHz": float(p["lamb_measured_MHz"]),
        "ansatz": "QED ordre alpha, vintage annees 1970 (autre evaluation que Mohr)",
        "lever": "—",
        "unit_raw": "MHz",
    }


def _p32_lamb_modern() -> tuple[float, dict]:
    """Contact ouvert P32 — Lamb moderne : la dette se ferme (suite P31).

    Règle déclarée AVANT le premier run : mu_loc = 1057.842 MHz (calcul
    QED Pachucki 2001 declare, u = 0.004, pour rp = 0.862(12) fm
    declare — dependance ecrite, pas circularite), mu_ref = 1057.845 MHz
    (MEME temoin Lundeen-Pipkin 1981 que P31, gel commun, u = 0.009).
    La reference NE DOIT JAMAIS entrer dans le calcul. theta = u_delta =
    0.009848857801796104 MHz, decide=U, k=1. Estimation pre-run honnete :
    delta ~ 0.003 MHz -> ratio ~ 0.305 -> S+ attendu, suspense faible —
    le suspense est dans l'arc : le temoin qui valait P/S- contre les
    theories vintage (Mohr 1.14 theta, Erickson 4.71 theta) devient S+
    contre la theorie reevaluee. La QED a paye sa dette.
    """
    from mvcg.tables import load_table

    t = load_table("lamb_shift_P32_LITERATURE-2001.json")
    p = t["params"]
    mu = float(p["pachucki2001_theory_MHz"])
    return mu, {
        "table": "lamb_shift_P32_LITERATURE-2001.json",
        "vintage": t["vintage"],
        "method": "calcul QED Pachucki 2001 (reevaluation ordres superieurs), valeur declaree",
        "rule": "Lamb(QED Pachucki 2001) = Lamb(mesure témoin Lundeen-Pipkin 1981, gel commun P31)",
        "pachucki2001_theory_MHz": mu,
        "lamb_measured_MHz": float(p["lamb_measured_MHz"]),
        "proton_radius_fm": float(p["proton_radius_fm"]),
        "ansatz": "QED reevaluee 2001, dependance rp declaree",
        "lever": "—",
        "unit_raw": "MHz",
    }


def _karplus_helix() -> tuple[float, dict]:
    """Contact ouvert NMR-Karplus hélice — ³J par la loi de Karplus.

    Règle déclarée AVANT le premier run : ³J(φ) = A cos²(φ−60°) +
    B cos(φ−60°) + C, coefficients gelés de la table (Vuister-Bax
    déclarés), φ_helix = −60° de la table. La référence
    J_helix_typical = 4,0 Hz est un ORDRE DE GRANDEUR déclaré (« pas
    un PDB »), pas une mesure de référence — c'est la dette attendue
    du contact. Aucun ajustement des coefficients sur les références
    typiques. θ = 0,10 rel gelé avant run. Estimation pré-run
    honnête : J ≈ 4,11 vs 4,0 → ~2,7 % → S+ attendu ; la référence
    étant grossière, le suspense porte sur la dette, pas sur le mot.
    """
    from mvcg.karplus import j_hn_ha, peptide_doc

    t = peptide_doc()
    j = j_hn_ha(float(t["phi_helix_deg"]), t)
    return j, {
        "table": "karplus_peptide_LITERATURE.json",
        "vintage": t["vintage"],
        "method": "loi de Karplus, coefficients gelés",
        "rule": "3J = A cos^2(phi-60) + B cos(phi-60) + C",
        "phi_deg": float(t["phi_helix_deg"]),
        "A": float(t["A"]), "B": float(t["B"]), "C": float(t["C"]),
        "J_ref_Hz": float(t["J_helix_typical_Hz"]),
        "ansatz": "conformation hélice, coefficients peptide déclarés",
        "lever": "coefficients<-autre-parametrisation",
        "unit_raw": "Hz",
    }


def _karplus_sheet() -> tuple[float, dict]:
    """Contact ouvert NMR-Karplus brin — même loi, autre conformation.

    Règle déclarée AVANT le premier run : mêmes coefficients gelés,
    φ_sheet = −120°. La référence J_sheet_typical = 8,5 Hz est un
    ordre de grandeur déclaré. Avec la fibre hélice, la loi devient
    une carte : deux conformations, deux mots attendus différents —
    l'estimation pré-run dit ~16 %, c'est-à-dire la zone P [θ, 2θ] :
    suspense réel au bord de la zone S− (20 %). θ = 0,10 gelé avant
    run ; jamais recalibré sur la référence.
    """
    from mvcg.karplus import j_hn_ha, peptide_doc

    t = peptide_doc()
    j = j_hn_ha(float(t["phi_sheet_deg"]), t)
    return j, {
        "table": "karplus_peptide_LITERATURE.json",
        "vintage": t["vintage"],
        "method": "loi de Karplus, coefficients gelés",
        "rule": "3J = A cos^2(phi-60) + B cos(phi-60) + C",
        "phi_deg": float(t["phi_sheet_deg"]),
        "A": float(t["A"]), "B": float(t["B"]), "C": float(t["C"]),
        "J_ref_Hz": float(t["J_sheet_typical_Hz"]),
        "ansatz": "conformation brin, mêmes coefficients",
        "lever": "coefficients<-autre-parametrisation",
        "unit_raw": "Hz",
    }


def _karplus_helix_vogelibax2007() -> tuple[float, dict]:
    """Contact ouvert NMR-Karplus hélice, seconde voie Vogeli-Bax 2007.

    Règle déclarée AVANT le premier run (protocole
    NMR-KARPLUS-VOGELIBAX-CONTACT-OUVERT.md, gel 2026-09-14, campagne
    croisée) : ³J(φ) = 7,97 cos²(φ−60°) − 1,26 cos(φ−60°) + 0,63
    (Vogeli, Ying, Grishaev, Bax, JACS 2007, 129, 9377 — déclarés),
    φ_helix = −60° de la table, MU REFERENCE TYPIQUE 4,0 Hz commune
    à la paire VB (ordre de grandeur déclaré, pas un PDB — dette
    identique). θ = 0,10 rel, MÊME étalonnage que la paire VB (la
    comparaison des deux voies n'a de sens qu'à θ identique). La
    paramétrisation a été choisie pour sa canonicité et sa traçabilité,
    jamais pour un mot attendu. Estimation pré-run (CORRIGÉE : la valeur
    initiale 4,2525 était une erreur d'addition du rédacteur —
    1,9925+0,63+0,63 = 3,2525) : le run a découvert J = 3,2525 vs 4,0
    → 18,69 % → P à 1,87 θ (à 0,13 θ de la frontière S−) — l'estimation
    erronée est conservée en trace, le mot vrai est figé dans le test.
    """
    from mvcg.karplus import j_hn_ha, peptide_vogelibax2007_doc

    t = peptide_vogelibax2007_doc()
    j = j_hn_ha(float(t["phi_helix_deg"]), t)
    return j, {
        "table": "karplus_peptide_VOGELIBAX2007.json",
        "vintage": t["vintage"],
        "method": "loi de Karplus, coefficients Vogeli-Bax 2007 gelés",
        "rule": "3J = 7.97 cos^2(phi-60) - 1.26 cos(phi-60) + 0.63",
        "phi_deg": float(t["phi_helix_deg"]),
        "A": float(t["A"]), "B": float(t["B"]), "C": float(t["C"]),
        "J_ref_Hz": float(t["J_helix_typical_Hz"]),
        "ansatz": "conformation hélice, coefficients Vogeli-Bax 2007 (2e voie)",
        "lever": "coefficients<-Vuister-Bax-1993 (1re voie, contact separe)",
        "unit_raw": "Hz",
    }


def _karplus_sheet_vogelibax2007() -> tuple[float, dict]:
    """Contact ouvert NMR-Karplus brin, seconde voie Vogeli-Bax 2007.

    Règle déclarée AVANT le premier run : mêmes coefficients gelés,
    φ_sheet = −120°, référence typique 8,5 Hz commune à la paire VB.
    θ = 0,10 rel au même étalonnage. Estimation pré-run : J ≈ 9,86 vs
    8,5 → 16,0 % → P attendu à ~1,60 θ (zone P, à 0,40 θ de la
    frontière S−). La question de la campagne croisée : les deux voies
    changent-elles le mot par conformation ?
    """
    from mvcg.karplus import j_hn_ha, peptide_vogelibax2007_doc

    t = peptide_vogelibax2007_doc()
    j = j_hn_ha(float(t["phi_sheet_deg"]), t)
    return j, {
        "table": "karplus_peptide_VOGELIBAX2007.json",
        "vintage": t["vintage"],
        "method": "loi de Karplus, coefficients Vogeli-Bax 2007 gelés",
        "rule": "3J = 7.97 cos^2(phi-60) - 1.26 cos(phi-60) + 0.63",
        "phi_deg": float(t["phi_sheet_deg"]),
        "A": float(t["A"]), "B": float(t["B"]), "C": float(t["C"]),
        "J_ref_Hz": float(t["J_sheet_typical_Hz"]),
        "ansatz": "conformation brin, coefficients Vogeli-Bax 2007 (2e voie)",
        "lever": "coefficients<-Vuister-Bax-1993 (1re voie, contact separe)",
        "unit_raw": "Hz",
    }


def _ckm_row1() -> tuple[float, dict]:
    """Contact ouvert CKM — l'unitarité de la première ligne.

    Règle déclarée AVANT le premier run : la première ligne de la
    matrice CKM est unitaire de par la définition même du modèle —
    |Vud|²+|Vus|²+|Vub|² = 1. mu_loc = somme déclarée de la table
    (extrait PDG déclaré, pas un fetch pdgLive), mu_ref = 1.0
    (identité du modèle, jamais ajustée). θ : decide=U, k=2 sur
    u = 0,0007 déclarée → U = 0,0014 ; le contact porte θ = 0,0007.
    Estimation pré-run honnête : δ = 0,0016, soit 2,3 sigma —
    U < δ ≤ 2U → P attendu, au cheveu du S+ (δ/U = 1,14) : suspense
    réel. Levier : somme<-autres entrées (Vus d'autres désintégrations).
    """
    from mvcg.tables import load_table

    t = load_table("ckm_row1_LITERATURE.json")
    s = float(t["sum"])
    return s, {
        "table": "ckm_row1_LITERATURE.json",
        "vintage": t["vintage"],
        "method": "somme |Vud|^2+|Vus|^2+|Vub|^2, extrait declare",
        "rule": "somme = 1 (unitarite de la 1re ligne)",
        "u_sum": float(t["u"]),
        "unitarity_ref": float(t["unitarity"]),
        "ansatz": "3 generations, unitarite du modèle",
        "lever": "somme<-autres-entrees",
        "unit_raw": "1",
    }


def _amu_wp20() -> tuple[float, dict]:
    """Contact ouvert AMU-WP20 — l'écart porté, seconde identification.

    Règle déclarée AVANT le premier run : même objet, même étalonnage
    de la doctrine AMU (l'écart normalisé : θ = u_delta déclarée,
    decide=U, k=1 — l'étalonnage fait partie du protocole et se
    justifie par la nature de l'objet, jamais par le mot attendu).
    μ_loc = Δ déclaré de la table (exp − SM(WP20), identification
    dispersive e+e-), porté, pas reconstruit — la table ne porte pas
    a_exp seul. μ_ref = identité 0 (jamais ajustée). L'identification lattice est
    déclarée ici comme identification sœur (honnêteté O15 généralisée) :
    elle aura droit à son contact séparé si elle est montée.
    Estimation pré-run honnête : δ = 279, U = 76 → δ/U = 3,67 →
    S− attendu, net (le mot reste S− jusqu'à k = 3). Le contraste entre les deux identifications sera
    porté par le protocole, jamais choisi.
    """
    from mvcg.tables import load_table

    t = load_table("amu_wp20_LITERATURE.json")
    return float(t["delta_exp_minus_wp20"]), {
        "table": "amu_wp20_LITERATURE.json",
        "vintage": t["vintage"],
        "method": "écart déclaré, porté (pas calculé depuis a_exp seul)",
        "rule": "a_exp - a_SM(WP20) vs identité 0",
        "u_delta": float(t["u_delta"]),
        "ansatz": "SM complet, identification dispersive déclarée",
        "lever": "HVP←lattice (autre id, contact séparé : HVP_LO_lat_vs_ee)",
        "unit_raw": "1e-11",
    }


def _hvp_lo_lat_ee() -> tuple[float, dict]:
    """Contact ouvert HVP_LO — deux fabrications du même terme.

    Règle déclarée AVANT le premier run : μ_loc = |lat_WP25 − ee_WP20|,
    les deux valeurs de la table ; μ_ref = identité 0 (deux
    fabrications du même terme devraient coïncider). θ : decide=U,
    k=2 standard machine — l'objet est un écart entre deux
    fabrications, non un écart exp−théorie : l'étalonnage k=1 de la
    paire AMU ne s'applique pas ici (l'étalonnage se justifie par la
    nature de l'objet). R identité déclarée (indépendance assumée) ;
    CMD-3 hors moyenne ee déclaré. Estimation pré-run honnête :
    δ = 201, u_c = √(61²+40²) ≈ 72,9, U(k=2) = 145,8 → δ/U = 1,38 →
    P attendu AU CHEVEU du S− (à k=1 : δ/U = 2,76 → S−). Suspense
    réel sur k — déclaré ici, avant le run.
    """
    from mvcg.tables import load_table

    t = load_table("hvp_lo_LITERATURE.json")
    return abs(float(t["lat_wp25"]) - float(t["ee_wp20"])), {
        "table": "hvp_lo_LITERATURE.json",
        "vintage": t["vintage"],
        "method": "écart entre deux fabrications déclarées du même terme",
        "rule": "a_HVP_LO(WP25 lat) = a_HVP_LO(WP20 ee)",
        "lat": float(t["lat_wp25"]), "ee": float(t["ee_wp20"]),
        "u_lat": float(t["u_lat"]), "u_ee": float(t["u_ee"]),
        "ansatz": "un seul terme HVP LO ; les deux fabrications devraient coïncider",
        "lever": "ee←autre-moyenne (CMD-3 déjà hors, déclaré)",
        "unit_raw": "1e-11",
    }


def _hlbl_lat_pheno() -> tuple[float, dict]:
    """Contact ouvert HLbL — deux fabrications du même terme.

    Règle déclarée AVANT le premier run : μ_loc = |lat − pheno|,
    mêmes vintage WP25 déclarés ; μ_ref = identité 0. θ : decide=U,
    k=2 standard machine (même raison que HVP_LO). R identité
    déclarée. La note de la mouture 6 annonçait « k=2 → P » : erreur
    arithmétique corrigée dans la table (19,2 ≤ 25,2). Estimation
    pré-run honnête : δ = 19,2, u_c = √(9²+8,8²) ≈ 12,6, U(k=2) =
    25,2 → δ/U = 0,76 → S+ attendu (à k=1 : δ/U = 1,53 → P).
    Suspense déclaré — le mot appartient au k gelé, pas à l'envie.
    """
    from mvcg.tables import load_table

    t = load_table("hlbl_LITERATURE.json")
    return abs(float(t["lat"]) - float(t["pheno"])), {
        "table": "hlbl_LITERATURE.json",
        "vintage": t["vintage"],
        "method": "écart entre deux fabrications déclarées du même terme",
        "rule": "a_HLbL(lat WP25) = a_HLbL(pheno WP25)",
        "lat": float(t["lat"]), "pheno": float(t["pheno"]),
        "u_lat": float(t["u_lat"]), "u_pheno": float(t["u_pheno"]),
        "ansatz": "un seul terme HLbL ; les deux fabrications devraient coïncider",
        "lever": "lat←autre-ensemble (jamais pheno, jamais θ)",
        "unit_raw": "1e-11",
    }


def _h0_ecart() -> tuple[float, dict]:
    """Contact ouvert H0 — l'écart entre deux fabrications déclarées.

    Règle déclarée AVANT le premier run : la tension H0 est l'objet.
    mu_loc = |H0_SH0ES / H0_Planck - 1|, les deux valeurs de la table
    sont la règle elle-même (contrairement aux contacts O, où la
    référence est exclue du calcul — ici il n'y a pas de troisième
    référence cachée : l'identité, un seul H0, est mu_ref = 0).
    Interdit par la table : moyenner les deux fabrications. θ = 0,05
    abs gelé avant run. Estimation pré-run honnête : δ ≈ 8,4 % —
    dans la zone P [θ, 2θ], au bord de la zone S− à 10 % : suspense
    réel. GUM : deux lignes B (Planck, SH0ES), R identité déclarée.
    """
    from mvcg.tables import load_table

    t = load_table("h0_LITERATURE-2018.json")
    p = t["params"]
    h0_p = float(p["Planck2018_H0"])
    h0_s = float(p["SH0ES2022_H0"])
    mu = abs(h0_s / h0_p - 1.0)
    return mu, {
        "table": "h0_LITERATURE-2018.json",
        "vintage": t["vintage"],
        "method": "ecart relatif de deux fabrications declarees",
        "rule": "|H0_SH0ES/H0_Planck - 1| vs identite 0",
        "H0_Planck": h0_p,
        "H0_SH0ES": h0_s,
        "u_Planck": float(p["Planck2018_u"]),
        "u_SH0ES": float(p["SH0ES2022_u"]),
        "ansatz": "une seule constante de Hubble ; les deux f devraient coincider",
        "lever": "f<-Planck_ou_SH0ES",
        "unit_raw": "1",
    }


def _hz_sne_lowz() -> tuple[float, dict]:
    """Contact H0 bas-z — la courbe H(z) declaree vs les bins SNe.

    Règle déclarée AVANT le premier run : mu_loc = rms_i( mu_pred(z_i ;
    H(z) fabrication Planck declaree) - mu_obs,i ), mu_ref = 0 (la
    courbe passe par les bins). θ = 0,05 mag abs gelé avant run.
    Interdit : ajuster les bins sur la référence — la recette de
    génération DEMO est déclarée dans la table (seed gelé), rien ne
    peut être retouché après coup. Dette déclarée : l'extract est
    SYNTHÉTIQUE (DEMO-2026), fiducial H0 = 70 entre les deux
    fabrications — le contact valide le protocole sur une carte dont
    la réponse est connue par construction ; il ne dit rien de
    l'univers réel. La table LITERATURE (compilation publique
    vérifiée) reste à déclarer, par nous ou par un tiers.
    Estimation pré-run honnête : écart systématique Planck-vs-70
    ≈ +0,082 mag quasi constant à bas z ; δ attendu ≈ sqrt(0,082² +
    0,05²) ≈ 0,096 — zone P [θ, 2θ], à ~0,004 du bord S− : suspense
    maximal, le bruit des 8 bins décide.
    """
    from mvcg.tables import load_table

    t = load_table("hz_sne_LOWZ-DEMO-2026.json")
    p = t["params"]
    om = float(p["Omega_m"])
    ol = float(p["Omega_L"])
    h0 = float(p["H0_fabrication_km_s_Mpc"])
    c = float(p["c_km_s"])
    res2 = []
    for z, mu_obs in t["bins"]:
        g = np.linspace(1e-8, z, 2000)
        chi = np.trapezoid(1.0 / np.sqrt(om * (1.0 + g) ** 3 + ol), g)
        dl = (1.0 + z) * chi * c / h0  # Mpc
        res2.append((5.0 * np.log10(dl) + 25.0 - mu_obs) ** 2)
    mu = float(np.sqrt(np.mean(res2)))
    return mu, {
        "table": "hz_sne_LOWZ-DEMO-2026.json",
        "vintage": t["vintage"],
        "method": "rms des residus mu_pred(H(z) Planck declare) - mu_obs sur 8 bins bas-z",
        "rule": "rms residu = 0  (la courbe declaree passe par les bins)",
        "H0_fabrication": h0,
        "Omega_m": om,
        "fiducial_H0_declare": float(p["fiducial_H0_km_s_Mpc"]),
        "n_bins": len(t["bins"]),
        "sigma_mag": float(t["sigma_mag"]),
        "ansatz": "LCDM a Omega gelé ; le seul degre de liberte declare est H0 de la fabrication",
        "lever": "H0<-SH0ES_ou_autre",
        "unit_raw": "mag",
    }


def _hz_sne_literature(table_name: str, ancrage: str) -> tuple[float, dict]:
    """Contact ouvert H0 bas-z LITERATURE — Pantheon+ ancré {ancrage}.

    Règle déclarée AVANT le premier run (protocole
    H0-HZ-SNE-PROTOCOLE-LITERATURE.md, §5) : mu_loc = rms_i(
    mu_pred(z_i ; H(z) fabrication Planck déclarée 67,4, Omega gelés)
    - mu_obs,i ), mu_ref = 0 (la courbe passe par les bins). θ =
    sigma bins déclarée = 0,02756 mag, gelé AVANT le run dans la
    déclaration de table — jamais ajusté après coup. GUM : une ligne
    B (incertitudes déclarées e_mBcorr/√N), decide=theta.
    Extraction (extraction_literature.py, chantier local) : Table 7
    de Brout et al. 2022 (VizieR J/ApJ/938/110), 1701 light curves
    dédoublonnées par nom normalisé (1542 SNe uniques), fenêtre zHD
    [0,01 ; 0,15) = 598 SNe, 8 bins équipopulaires, moyenne
    arithmétique déclarée. Amplitude : transposition EXACTE à Omega
    gelés identiques, mu_ancre = mBcorr + 5*log10(H0_ancrage) - K_B,
    K_B = 28,52698 = convention de la table mesurée à la forme gelée
    (dégénérescence M-H0 : non séparable sans Céphéides, Brout 2022
    §2.3). Validation croisée : std(A - mBcorr) = 0,160 mag à z >= 0,01
    vs rms ~0,15 publié (Table 2, BS21). Dettes écrites dans la table :
    compression, ancrage, indépendance, vitesses, miroir.
    Estimation pré-run honnête :
    - ancrage Planck, courbe Planck posée : résidu = bruit réalisé
      des bins, δ attendu ~0,02–0,04 — zone P [θ, 2θ] au cheveu :
      SUSPENS RÉEL, le bruit réalisé décide.
    - ancrage SH0ES, courbe Planck posée : résidu moyen =
      +5*log10(73,04/67,4) = +0,1745 mag quasi constant (exact à
      Omega gelés identiques), δ ≈ sqrt(σ² + 0,1745²) ≈ 0,177
      >> 2θ = 0,0551 : S− attendu SANS suspense.
    """
    from mvcg.tables import load_table

    t = load_table(table_name)
    p = t["params"]
    om = float(p["Omega_m"])
    ol = float(p["Omega_L"])
    h0 = 67.4  # fabrication Planck déclarée, posée par le contact gelé
    c = float(p["c_km_s"])
    res2 = []
    for z, mu_obs in t["bins"]:
        g = np.linspace(1e-8, z, 2000)
        chi = np.trapezoid(1.0 / np.sqrt(om * (1.0 + g) ** 3 + ol), g)
        dl = (1.0 + z) * chi * c / h0  # Mpc
        res2.append((5.0 * np.log10(dl) + 25.0 - mu_obs) ** 2)
    mu = float(np.sqrt(np.mean(res2)))
    return mu, {
        "table": table_name,
        "vintage": t["vintage"],
        "method": "rms des residus mu_pred(H(z) Planck declare) - mu_obs "
                  "sur 8 bins bas-z Pantheon+ (Brout 2022 Table 7)",
        "rule": "rms residu = 0  (la courbe declaree passe par les bins)",
        "H0_fabrication": h0,
        "H0_ancrage": float(p["H0_ancrage_km_s_Mpc"]),
        "Omega_m": om,
        "n_bins": len(t["bins"]),
        "sigma_mag": float(t["sigma_mag"]),
        "ansatz": "LCDM a Omega gelé ; seul levier declare H0 de la "
                  "fabrication",
        "lever": "H0<-SH0ES_ou_autre",
        "unit_raw": "mag",
    }


def _hz_sne_lit_sh0es() -> tuple[float, dict]:
    return _hz_sne_literature("hz_sne_LOWZ-LITERATURE-SH0ES.json", "SH0ES")


def _hz_sne_lit_planck() -> tuple[float, dict]:
    return _hz_sne_literature("hz_sne_LOWZ-LITERATURE-Planck.json", "Planck")


def _hz_sne_v2(h0_courbe: float, courbe_nom: str) -> tuple[float, dict]:
    """Contact ouvert H0 bas-z V2 — Pantheon+ ancré MU_SH0ES natif.

    Règle déclarée AVANT le premier run (protocole
    H0-HZ-SNE-V2-PROTOCOLE.md) : mêmes bins que V1 (8 bins équipopulaires,
    fenêtre zHD [0,01 ; 0,15), 598 SNe, même règle de dispersion σ_bin),
    mais l'amplitude est MU_SH0ES telle que publiée dans la release
    Pantheon+ (ancrage natif, plus de transposition) — supprime la dette
    de forme (+0,049 mag, campagne 7). La courbe posée par le contact est
    mu_pred(z ; H0_courbe déclaré, Omega gelés 0,315/0,685) ; le H0 de
    courbe est passé explicitement par le wrapper (corrige le piège
    silencieux du runner V1 qui ignore son ancrage et lit 67,4 en dur).
    mu_loc = rms des résidus sur 8 bins, mu_ref = 0. θ = sigma bins
    déclarée = 0,027737 mag, gelée AVANT le run dans la table. GUM :
    une ligne B (incertitudes déclarées MU_SH0ES_ERR_DIAG/√N),
    decide=theta. V2 complète V1 sans la remplacer (les contacts V1
    restent gelés). Dettes écrites : calibration commune non réduite ;
    forme residuelle Omega gelés vs ajustements de la collaboration.
    Estimation pré-run honnête :
    - courbe Planck 67,4 posée : résidu moyen ≈ +0,1766 mag quasi
      constant (miroir de V1_SH0ES), δ ≈ 0,178 >> 2θ = 0,055474 :
      S- attendu SANS suspense.
    - courbe SH0ES 73,04 posée : résidu = bruit réalisé, rms ≈ 0,0249,
      δ/θ ≈ 0,897 < 1 : S+ attendu AU CHEVEU, le bruit réalisé décide.
    """
    from mvcg.tables import load_table

    t = load_table("hz_sne_LOWZ-V2-MUSH0ES.json")
    p = t["params"]
    om = float(p["Omega_m"])
    ol = float(p["Omega_L"])
    c = float(p["c_km_s"])
    res2 = []
    for z, mu_obs in t["bins"]:
        g = np.linspace(1e-8, z, 2000)
        chi = np.trapezoid(1.0 / np.sqrt(om * (1.0 + g) ** 3 + ol), g)
        dl = (1.0 + z) * chi * c / h0_courbe  # Mpc
        res2.append((5.0 * np.log10(dl) + 25.0 - mu_obs) ** 2)
    mu = float(np.sqrt(np.mean(res2)))
    return mu, {
        "table": "hz_sne_LOWZ-V2-MUSH0ES.json",
        "vintage": t["vintage"],
        "method": "rms des residus mu_pred(H(z) courbe declaree) - "
                  "mu_obs SNe sur 8 bins bas-z Pantheon+ MU_SH0ES natif",
        "rule": "rms residu = 0  (la courbe declaree passe par les bins)",
        "H0_courbe": h0_courbe,
        "H0_courbe_nom": courbe_nom,
        "Omega_m": om,
        "n_bins": len(t["bins"]),
        "sigma_mag": float(t["sigma_mag"]),
        "ansatz": "LCDM a Omega gelé ; seul levier declare H0 de la courbe",
        "lever": "H0<-courbe_PLANCK_ou_SH0ES",
        "unit_raw": "mag",
    }


def _hz_sne_v2_params() -> dict:
    from mvcg.tables import load_table

    return load_table("hz_sne_LOWZ-V2-MUSH0ES.json")["params"]


def _hz_sne_v2_planck() -> tuple[float, dict]:
    p = _hz_sne_v2_params()
    return _hz_sne_v2(float(p["H0_courbe_PLANCK_km_s_Mpc"]), "PLANCK")


def _hz_sne_v2_sh0es() -> tuple[float, dict]:
    p = _hz_sne_v2_params()
    return _hz_sne_v2(float(p["H0_courbe_SH0ES_km_s_Mpc"]), "SH0ES")


def _co_rot_table() -> dict:
    from mvcg.tables import load_table

    return load_table("co_rot_NIST-HH.json")


def _co_rot_abinitio() -> tuple[float, dict]:
    """Contact SPEC CO rotationnel — rotor rigide a l'equilibre.

    Règle déclarée AVANT le premier run (protocole SPEC-CO-ROT-
    PROTOCOLE.md, gel 2026-09-14) : mu_loc = |B_e,calc - B0,obs| en
    Hz, B_e,calc = hbar/(4 pi mu r_e^2), mu en kg (NIST JPCRD 53),
    r_e déclaré Huber & Herzberg 1979 ; mu_ref = B0 mesuré NIST.
    theta = 3000 Hz = u(B0) déclarée NIST, gelée avant run. GUM :
    une ligne B (u(B0) déclarée), decide=theta, k=2. Table vintage :
    NIST JPCRD 53 + HH1979 via RIOS (API interrogée 2026-09-14).
    Estimation pré-run honnête : delta ~ 265 MHz ~ alpha_e/2 (zéro
    vibratoire : B0 = B_e - alpha_e/2), delta/theta ~ 9e4 -> S- attendu
    SANS suspense — leçon : le rotor rigide à l'équilibre ne prédit
    pas le niveau v=0 ; l'écart s'appelle alpha_e (S- de dette, dans
    l'esprit O1 grille -> O6). Dettes : vintage HH arrondi 6 chiffres ;
    mu en masse standard (isotopes dominants).
    """
    p = _co_rot_table()["params"]
    hbar = float(p["hbar_SI"])
    u_kg = float(p["u_kg"])
    mu = float(p["mu_u"]) * u_kg
    re = float(p["re_A"]) * 1e-10
    b_e = hbar / (4.0 * np.pi * mu * re**2)  # Hz
    b0 = float(p["B0_MHz"]) * 1e6  # Hz
    delta = abs(b_e - b0)
    return delta, {
        "table": "co_rot_NIST-HH.json",
        "vintage": _co_rot_table()["vintage"],
        "method": "B_e calcule (hbar/4 pi mu r_e^2, mu NIST, r_e HH) "
                  "compare a B0 mesure NIST",
        "rule": "|B_e,calc - B0,obs| = 0  (rotor rigide a l'equilibre = niveau v=0)",
        "B_e_calc_Hz": float(b_e),
        "B0_obs_Hz": float(b0),
        "alpha_e_attendu_Hz": 0.0175 * float(p["cm-1_to_MHz"]) * 1e6 / 2.0,
        "unit_raw": "Hz",
    }


def _co_rot_dunham() -> tuple[float, dict]:
    """Contact SPEC CO rotationnel — coherence interne du catalogue.

    Règle déclarée AVANT le premier run (protocole SPEC-CO-ROT-
    PROTOCOLE.md, gel 2026-09-14) : mu_loc = |nu_pred - nu_obs| en
    Hz, nu_pred = 2*B0 - 4*D0 (B0, D0 déclarés NIST) ; mu_ref =
    nu(1-0) NIST. theta = 10000 Hz = u(nu) déclarée NIST, gelée avant
    run. GUM : une ligne B (u(nu) déclarée), decide=theta, k=2.
    Estimation pré-run honnête : nu_pred = 115271,20372 MHz,
    delta ~ 280 Hz, delta/theta ~ 0,03 -> S+ attendu SANS suspense :
    le catalogue est interne cohérent à ~3e-6 de son budget déclaré.
    Dette écrite : circularité — B0, D0 et nu d'un même ajustement ;
    ce contact calibre le transport de table, pas une prédiction
    indépendante (contrairement au contact ab initio).
    """
    p = _co_rot_table()["params"]
    nu_pred = (2.0 * float(p["B0_MHz"]) - 4.0 * float(p["D0_kHz"]) / 1000.0)
    nu_obs = float(p["nu_10_MHz"])
    delta = abs(nu_pred - nu_obs) * 1e6  # Hz
    return delta, {
        "table": "co_rot_NIST-HH.json",
        "vintage": _co_rot_table()["vintage"],
        "method": "nu_pred = 2*B0 - 4*D0 (NIST) compare a nu(1-0) NIST",
        "rule": "2*B0 - 4*D0 = nu(1-0)  (coherence interne du catalogue)",
        "nu_pred_MHz": float(nu_pred),
        "nu_obs_MHz": float(nu_obs),
        "unit_raw": "Hz",
    }


def _co13_rot_mu_rule() -> tuple[float, dict]:
    """Contact SPEC CO isotopologue — règle de la masse réduite.

    Règle déclarée AVANT le premier run (protocole SPEC-CO-ROT-
    PROTOCOLE.md §3, gel 2026-09-14) : mu_loc = |B0_pred - B0'(mesure)|
    en Hz, B0_pred = B0(12CO) * mu/mu' (règle de la masse réduite
    appliquée telle quelle au niveau v=0) ; mu, mu', B0, B0' déclarés
    NIST JPCRD 53. mu_ref = B0' mesuré. theta = 12000 Hz = u(B0')
    déclarée NIST, gelée avant run. GUM : une ligne B (u(B0') déclarée),
    decide=theta, k=2.
    Estimation pré-run honnête : B0_pred ~ 55 096,7 MHz, delta ~ 4,3 MHz,
    delta/theta ~ 360 -> S- attendu SANS suspense. La règle s'applique
    rigoureusement à B_e, pas à B0 : l'écart nomme la correction
    isotopique de la vibration-rotation (alpha_e non purement en 1/mu)
    + effets au-delà de Born-Oppenheimer. Le suspense porte sur la
    taille de l'écart, pas sur le mot. Dettes : mu'/B0' de la même
    table NIST (validation croisée interne) ; alpha_e' non extrait.
    """
    p = _co_rot_table()["params"]
    b_pred = float(p["B0_MHz"]) * float(p["mu_u"]) / float(p["mu13_u"])
    b_obs = float(p["B0_13_MHz"])
    delta = abs(b_pred - b_obs) * 1e6  # Hz
    return delta, {
        "table": "co_rot_NIST-HH.json",
        "vintage": _co_rot_table()["vintage"],
        "method": "B0'(13CO) predite par la regle de la masse reduite "
                  "B0*mu/mu' comparee a B0' NIST",
        "rule": "B0 * mu/mu' = B0'(mesure)  (regle de la masse reduite "
                "au niveau v=0)",
        "B0_pred_MHz": float(b_pred),
        "B0_obs_13_MHz": float(b_obs),
        "unit_raw": "Hz",
    }


def _co_rot_kratzer() -> tuple[float, dict]:
    """Contact SPEC CO — relation de Kratzer (prediction croisee).

    Règle déclarée AVANT le premier run (protocole SPEC-CO-ROT-
    PROTOCOLE.md §4, gel 2026-09-14) : mu_loc = |D_e,calc - D0,obs|
    en Hz, D_e = 4*B_e^3/omega_e^2 (relation de Kratzer pour
    l'oscillateur de Morse). Entrees déclarées B_e et omega_e (Huber &
    Herzberg 1979 via RIOS, indépendants de l'ajustement NIST de D0) ;
    mu_ref = D0 mesuré NIST JPCRD 53. theta = 70 Hz = u(D0) déclarée
    NIST, gelée avant run. GUM : une ligne B (u(D0) déclarée),
    decide=theta, k=2.
    Estimation pré-run honnête : D_e,calc ~ 6,120e-6 cm-1 ~ 183,6 kHz ;
    delta ~ 70-80 Hz ; delta/theta ~ 1,0-1,1 — zone P [theta, 2theta]
    au cheveu : SUSPENSE MAXIMAL, le mot est réellement inconnu (P, S+
    et S- accessibles selon les arrondis H&H). Pendant du S- 13CO :
    la regle mu echoue a 412 theta ; la relation anharmonique teste
    si la physique tient au niveau 1e-4. Dettes : D_e (equilibre)
    pesé contre D0 (v=0), ecart vibrationnel ~0,2 Hz << theta ;
    arrondis H&H 6 chiffres propagent l'ecart attendu ; Kratzer exact
    pour Morse seulement.
    """
    p = _co_rot_table()["params"]
    be = float(p["Be_cm-1"])
    we = float(p["omega_e_cm-1"])
    d_e_cm = 4.0 * be**3 / we**2
    d_calc = d_e_cm * float(p["cm-1_to_MHz"]) * 1e6  # Hz
    d_obs = float(p["D0_kHz"]) * 1e3  # Hz
    delta = abs(d_calc - d_obs)
    return delta, {
        "table": "co_rot_NIST-HH.json",
        "vintage": _co_rot_table()["vintage"],
        "method": "D_e = 4*B_e^3/omega_e^2 (Kratzer, entrees H&H) "
                  "compare a D0 mesure NIST",
        "rule": "4*B_e^3/omega_e^2 = D0  (relation de Kratzer)",
        "D_e_calc_Hz": float(d_calc),
        "D0_obs_Hz": float(d_obs),
        "unit_raw": "Hz",
    }


def _co_rot_alpha_e() -> tuple[float, dict]:
    """Contact SPEC CO — levier alpha_e du rotor rigide ab initio.

    Règle déclarée AVANT le premier run (protocole SPEC-CO-ROT-
    PROTOCOLE.md §5, gel 2026-09-14) : mu_loc = |B0,calc - B0,obs| en
    Hz, B0,calc = B_e,calc - alpha_e/2 (même calcul ab initio que le
    contact 1, correction vibration-rotation soustraite, alpha_e/2
    déclaré H&H 1979) ; mu_ref = B0 mesuré NIST. theta = 3000 Hz =
    u(B0) NIST, gelée avant run. GUM : une ligne B (u(B0) déclarée),
    decide=theta, k=2.
    Estimation pré-run honnête : le contact 1 a mesuré B_e,calc - B0 =
    262394407 Hz, ecart a alpha_e/2 attendu = 76007 Hz ; delta ~ 76 kHz,
    delta/theta ~ 25 -> S- attendu SANS suspense. Le levier réduit
    l'ecart d'un facteur ~3500 : alpha_e nomme la physique manquante ;
    le résidu nomme la dette de vintage (H&H 1979, alpha_e 3 chiffres,
    ajustement 1976) qui ne rejoint pas le NIST 2013. Leçon attendue
    cohérente avec le P de Kratzer : geste + levier justes, table
    détentrice de la dette. Suspense faible sur le mot, fort sur la
    taille du résidu (dérive vintage H&H -> NIST).
    """
    p = _co_rot_table()["params"]
    hbar = float(p["hbar_SI"])
    u_kg = float(p["u_kg"])
    mu = float(p["mu_u"]) * u_kg
    re = float(p["re_A"]) * 1e-10
    b_e = hbar / (4.0 * np.pi * mu * re**2)  # Hz
    alpha_half = float(p["alpha_e_cm-1"]) / 2.0 * float(p["cm-1_to_MHz"]) * 1e6
    b0_calc = b_e - alpha_half
    b0 = float(p["B0_MHz"]) * 1e6
    delta = abs(b0_calc - b0)
    return delta, {
        "table": "co_rot_NIST-HH.json",
        "vintage": _co_rot_table()["vintage"],
        "method": "B0,calc = B_e,calc - alpha_e/2 (ab initio + correction "
                  "H&H) compare a B0 mesure NIST",
        "rule": "B_e - alpha_e/2 = B0  (rotor rigide + vibration-rotation)",
        "B0_calc_Hz": float(b0_calc),
        "B_e_calc_Hz": float(b_e),
        "alpha_e_half_Hz": float(alpha_half),
        "B0_obs_Hz": float(b0),
        "unit_raw": "Hz",
    }


def _amu_delta() -> tuple[float, dict]:
    """Contact ouvert AMU — l'écart g-2 porté, en unités de son incertitude.

    Règle déclarée AVANT le premier run : mu_loc = delta déclaré
    (a_exp - a_SM lattice WP25) = 38e-11, porté par la table — ce
    n'est pas un calcul depuis a_SM et a_exp séparément (la table ne
    porte pas a_exp seul). La référence est l'identité (le SM complet
    prédit delta = 0). θ = 63 abs gelé avant run = u_delta déclarée :
    le seuil EST l'incertitude de l'écart. GUM : decide=U, k=1 —
    un S+ ici veut dire « l'écart tient dans une incertitude », pas
    « le SM est confirmé ». Autre identification (HVP e+e-) déclarée
    dans la note, jamais choisie après coup (honnêteté O15).
    Estimation pré-run : 38 ≤ 63 → S+ attendu, à 0,6 theta — suspense
    faible : contact de calibre de la tension, pas de suspense.
    """
    from mvcg.tables import load_table

    t = load_table("amu_LITERATURE-2018.json")
    p = t["params"]
    delta = float(p["delta_exp_minus_wp25"])
    return delta, {
        "table": "amu_LITERATURE-2018.json",
        "vintage": t["vintage"],
        "method": "ecart declare, porte (pas calcule depuis a_SM seul)",
        "rule": "a_exp - a_SM(WP25) vs identite 0",
        "a_sm_wp25": float(p["a_sm_wp25"]),
        "u_sm_wp25": float(p["u_sm_wp25"]),
        "u_delta": float(p["u_delta_wp25"]),
        "ansatz": "SM complet ; toute identification HVP declaree a droit au sien",
        "lever": "HVP<-e+e- (autre id, contact separe)",
        "unit_raw": "1e-11",
    }


def _rydberg_voie2() -> tuple[float, dict]:
    """Contact ouvert Rydberg voie 2 — R∞ depuis alpha et me*c^2.

    Règle déclarée AVANT le premier run (protocole
    RYDBERG-VOIE2-CONTACT-OUVERT.md, gel 2026-09-14, campagne
    croisee) : mu_loc = R_∞ en eV CALCULE : R_∞ = alpha^2 me*c^2 / (2e),
    alpha = 7.2973525693(11)e-3 et me*c^2 = 8.1871057769(25)e-14 J
    (CODATA 2018, incertitudes declarees dans la table), e exacte (SI).
    mu_ref = Rydberg_eV declare du meme tableau. GUM : decide=U, k=1,
    theta = u_delta = 5.838364428925748e-9 eV (quadrature de
    l'incertitude propagee — 2*u_alpha/alpha et u_me/me dominant,
    u_rel ~ 4.3e-10 — et de l'incertitude declaree de la reference,
    portee par la table). DETTE DE CIRCULARITE DECLAREE : alpha,
    me*c^2 et Rydberg_eV participent du MEME ajustement CODATA-2018 —
    ce contact mesure la coherence interne du catalogue, exactement
    comme SPEC_CO_Rot_Dunham ; il ne mesure pas une prediction
    independante. Suspense annonce nul au gel (estimation S+ a ~0.02 U)
    : c'est un contact de certification de la fibre eV, pas de suspense.
    """
    from mvcg.tables import load_table

    t = load_table("codata2018_rydberg_voie2.json")
    c = t["constants"]
    alpha = float(c["alpha"])
    me_c2 = float(c["me_c2_J"])
    e = float(c["e_C"])
    e_calc = alpha**2 * me_c2 / (2.0 * e)
    return e_calc, {
        "table": "codata2018_rydberg_voie2.json",
        "vintage": t["vintage"],
        "method": "R_∞ = alpha^2 me*c^2 / (2e), constantes declarees",
        "rule": "R_∞ calculee vs Rydberg_eV declare, identite attendue",
        "alpha": alpha,
        "me_c2_J": me_c2,
        "rydberg_ref_eV": float(c["rydberg_eV"]),
        "u_delta_eV": float(c["u_delta_ecart_eV"]),
        "ansatz": "coherence interne CODATA-2018 (circularite declaree, pendant du Dunham)",
        "lever": "spectro<-H1s_Rydberg (1re voie, contact separe)",
        "unit_raw": "eV",
    }


def _hvp_pipi_cmd3() -> tuple[float, dict]:
    """Contact ouvert HVP pi pi — CMD-3 vs moyenne pre-CMD-3, l'ecart porte.

    Règle déclarée AVANT le premier run (protocole
    HVP-PIPI-CMD3-CONTACT-OUVERT.md, gel 2026-09-14, campagne
    croisee) : mu_loc = ecart tel que publie dans le PRL CMD-3 :
    a_mu^had,LO(2pi, CMD-3) = 5260(42) vs moyenne des mesures
    precedentes = 5060(34) (1e-11) -> delta = 200, PORTE, pas calcule
    depuis les sections efficaces. La reference est l'identite (deux
    fabrications du meme objet). theta = u_delta = sqrt(42^2+34^2)
    = 54.037 (1e-11), independance assumée (meme convention que la
    table hvp_lo). GUM : decide=U, k=1 — l'etalonnage de la doctrine
    AMU. Identification multiple declaree : la moyenne pre-CMD-3 est
    KLOE-dominee ; un contact KLOE seul exigerait une valeur KLOE sur
    la fenetre exacte CMD-3, non publiee — identifiee, jamais choisie
    apres coup. Dette de fenetre declaree (CMD-3 exclusif 0.327-1.2
    GeV + moyenne au-dela). Estimation pre-run : 200 > 54 -> S-
    attendu a ~3.7 theta — suspense faible, contact de calibre.
    """
    from mvcg.tables import load_table

    t = load_table("hvp_pipi_cmd3_LITERATURE.json")
    p = t["params"]
    delta = float(p["delta_cmd3_minus_premoy"])
    return delta, {
        "table": "hvp_pipi_cmd3_LITERATURE.json",
        "vintage": t["vintage"],
        "method": "ecart publie par CMD-3, porte (pas calcule depuis sigma)",
        "rule": "a(2pi, CMD-3) - a(2pi, moyenne pre-CMD-3) vs identite 0",
        "a_cmd3": float(p["a_cmd3"]),
        "u_cmd3": float(p["u_cmd3"]),
        "a_premoy": float(p["a_premoy"]),
        "u_premoy": float(p["u_premoy"]),
        "u_delta": float(p["u_delta"]),
        "ansatz": "deux fabrications exp du meme terme ; la moyenne est KLOE-dominee (declare)",
        "lever": "KLOE<-seul (autre id, fenetre exacte non publiee)",
        "unit_raw": "1e-11",
    }


def _landau_vc_he4() -> tuple[float, dict]:
    """Contact ouvert hyperfluidité — la vitesse critique de Landau du ⁴He.

    Règle déclarée AVANT le premier run : v_c = min_p E(p)/p (Landau
    1941) calculée sur le spectre phonon-roton déclaré de la table
    (`he4_spectrum_LANDAU.json`) — scan fin + parabole locale, aucun
    point ajusté sur la référence. La référence v_c ≈ 58 m/s est un
    ordre de grandeur de littérature déclaré. Dette assumée et écrite
    : spectre et v_c ne sont pas physiquement indépendants (le min de
    E/p EST le roton) — ce contact mesure la cohérence interne de la
    carte spectrale déclarée, pas une prédiction ; la dette est
    déclarée au lieu d'être cachée. θ = 0,10 rel gelé avant run.
    Estimation pré-run honnête : v_c ≈ 58,8 m/s au roton (k ≈ 1,92 Å⁻¹),
    δ ≈ 1,3 % → S+ attendu ; suspense faible, dette assumée. Levier :
    spectre←autre-mesure (jamais la référence, jamais θ).
    """
    from mvcg.landau import landau_vc, spectrum_doc

    t = spectrum_doc()
    sol = landau_vc(t["points"])
    return float(sol["vc_m_s"]), {
        "table": "he4_spectrum_LANDAU.json",
        "vintage": t["vintage"],
        "method": "Landau 1941, min E(p)/p sur spectre déclaré",
        "rule": "v_c = min_p E(p)/p (critère de Landau)",
        "k_star_ang^-1": float(sol["k_star_ang^-1"]),
        "E_star_K": float(sol["E_star_K"]),
        "mechanism": sol["mechanism"],
        "vc_ref_m_s": float(t["vc_ref_m_s"]),
        "phonon_speed_m_s": float(t["phonon_speed_m_s"]),
        "ansatz": "superfluidité = spectre d'énergie déclaré ; le min porte le mécanisme",
        "lever": "spectre<-autre-mesure",
        "unit_raw": "m/s",
    }


def _kss_eta_s_qgp() -> tuple[float, dict]:
    """Contact ouvert hyperfluidité — le QGP sature-t-il le plancher KSS ?

    Règle déclarée AVANT le premier run : c'est le premier contact du
    tiroir dont le mot tranche une question ouverte — la saturation de
    la borne KSS par le plasma quarks-gluons, fluide déclaré le plus
    proche du plancher. La fabrication est la borne INFÉRIEURE de
    l'extraction la plus citée (η/s ≈ (2-3) unités KSS, Luzum &
    Romatschke, repris dans arXiv:1108.0734) lue dans la table
    (`eta_s_qgp_LITERATURE.json`) — la déclaration la plus favorable
    au suspense. La référence est le plancher (1). Dette assumée et
    écrite : les extractions ne coïncident pas, la fourchette large
    (0,6-2,5 planchers) chevauche le plancher ; un mot S− dira «
    non-saturation établie pour la déclaration choisie », jamais « KSS
    violée ». Le geste interdit : descendre la borne inf sous 2
    planchers en invoquant la fourchette large pour rapprocher μ_loc
    du plancher. θ = 0,10 rel gelé avant run. Levier : η/s←autre-
    extraction (jamais la référence, jamais θ). Estimation pré-run
    honnête : δ = 100 % → S− attendu probable ; suspense limité mais
    réel — c'est le dévoilement qui compte, pas la surprise.
    """
    from mvcg.tables import load_table

    t = load_table("eta_s_qgp_LITERATURE.json")
    return float(t["eta_s_over_kss_min_declared"]), {
        "table": "eta_s_qgp_LITERATURE.json",
        "vintage": t["vintage"],
        "method": "borne inferieure de l'extraction la plus citee (Luzum & Romatschke)",
        "rule": "eta/s >= hbar/(4 pi k_B) (KSS 2005) ; le QGP sature-t-il le plancher ?",
        "fluid": t["fluid"],
        "kss_bound": t["kss_bound"],
        "range_broad_planck_units": t["range_broad_planck_units"],
        "ansatz": "le mot tranche la saturation pour la declaration choisie, pas KSS elle-meme",
        "lever": "eta/s<-autre-extraction",
        "unit_raw": "1",
    }


def _kss_eta_s_he4() -> tuple[float, dict]:
    """Contact ouvert hyperfluidité — la marge η/s du ⁴He au plancher KSS.

    Règle déclarée AVANT le premier run : la conjecture Kovtun-Son-
    Starinets (2005), η/s ≥ ℏ/(4πk_B), est une BORNE — démontrée en
    holographie, avec des contre-exemples théoriques en théorie
    effective, jamais violée expérimentalement. Ce contact pèse la
    marge, pas la validité : la fabrication est la borne inférieure
    expérimentale déclarée du ⁴He liquide (η/s ≥ 8,8 planchers,
    évaluation Schafer & Teaney 2009 reprise dans Kagamihara et al.
    2019) lue dans la table (`eta_s_kss_LITERATURE.json`), la référence
    est le plancher lui-même (1 en unités du plancher). Le geste
    interdit est double et écrit : déplacer 8,8 vers le plancher, ou
    lire un mot S− comme une réfutation de KSS — un fluide au-dessus
    de la borne la satisfait. θ = 0,10 rel gelé avant run. Levier :
    η/s←autre-mesure (jamais la référence, jamais θ). Estimation
    pré-run honnête : 8,8 vs 1 → δ = 780 % → S− net attendu ; suspense
    structurellement nul — c'est un contact de marge, comme Bertsch est
    un contact de dette.
    """
    from mvcg.tables import load_table

    t = load_table("eta_s_kss_LITERATURE.json")
    return float(t["eta_s_over_kss_min_exp"]), {
        "table": "eta_s_kss_LITERATURE.json",
        "vintage": t["vintage"],
        "method": "borne inferieure experimentale declaree (Schafer & Teaney 2009)",
        "rule": "eta/s >= hbar/(4 pi k_B) (KSS 2005) ; marge du 4He declaree au-dessus du plancher",
        "fluid": t["fluid"],
        "kss_bound": t["kss_bound"],
        "ansatz": "la borne n'est pas une identite ; le mot mesure la marge, pas la validite",
        "lever": "eta/s<-autre-mesure",
        "unit_raw": "1",
    }


def _bertsch_xi() -> tuple[float, dict]:
    """Contact ouvert hyperfluidité — le paramètre de Bertsch ξ à l'unitarité.

    Règle déclarée AVANT le premier run : ξ = (5/3)·E/(Nε_F) en ansatz
    BCS mean-field à T = 0 (Leggett 1980), équations gap + nombre
    résolues par quadrature avec corrections de queue analytiques
    (`bertsch.py`). Aucun point ajusté sur la référence. La référence
    ξ ≈ 0,370 est le consensus expérience/QMC déclaré de la table
    (`xi_unitary_LITERATURE.json`). Dette assumée et écrite : l'ansatz
    mean-field ne récupère pas la corrélation forte de l'unitarité —
    pendant exact de P27 (He Hartree-Fock) ; la dette est déclarée au
    lieu d'être cachée. θ = 0,10 abs gelé avant run.
    Estimation pré-run honnête : ξ_MF = 0,5905 (littérature mean-field),
    δ = |0,5905−0,370|/0,370 ≈ 60 % → S− attendu net (δ > 2θ) ; suspense
    quasi nul — ce contact calibre l'erreur structurelle du mean-field,
    comme P27. Levier : ξ←autre-ansatz (jamais la référence, jamais θ).
    """
    from mvcg.bertsch import bertsch_xi

    sol = bertsch_xi()
    return float(sol["xi"]), {
        "table": "xi_unitary_LITERATURE.json",
        "vintage": "litterature-declaree",
        "method": "BCS mean-field T=0 (Leggett 1980), gap+nombre, queues analytiques",
        "rule": "xi = (5/3) E/(N eps_F) mean-field a l'unite",
        "mu_over_ef": float(sol["mu_over_ef"]),
        "delta_over_ef": float(sol["delta_over_ef"]),
        "xi_ref": 0.370,
        "ansatz": "superfluidite = ansatz BCS mean-field ; la correlation forte de l'unite est la dette",
        "lever": "xi<-autre-ansatz",
        "unit_raw": "1",
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


def _l4_gap_universel() -> tuple[float, dict]:
    """Contact L4 — gap universel ω(k1) insensible a l'inertie (vague fine).

    Protocole L4-GYROCORPS-CONTACTS.md (gelé avant run) : lecture croisée
    fine/fine ω(k1, m=12) vs ω(k1, m=5), meme protocole AMP=0.15. La
    reference NE DOIT JAMAIS entrer dans le calcul : mu = lecture table.
    """
    from mvcg.tables import load_table

    t = load_table("l4_gyrocorps_LITERATURE-HP2027.json")
    p = t["params"]
    return float(p["w1_m12_fine"]), {
        "table": "l4_gyrocorps_LITERATURE-HP2027.json",
        "vintage": t["vintage"],
        "method": "lecture croisée fine/fine du gap k1 (m=12 vs m=5)",
        "rule": "gap universel : omega(k1) identique pour toute masse m",
        "mu_ref": float(p["w1_m5_fine"]),
        "unit_raw": "1 (unités internes GP)",
    }


def _l4_branche_k2() -> tuple[float, dict]:
    """Contact L4 — branche gelée ω²=ω₀²+β²k⁴ évaluée à k₂ (régime fin).

    Protocole gelé : transposabilité de la branche P1-P2 (calibrée AMP=0.3)
    au régime fin AMP=0.15 — la dette ouverte du corpus (dépendance en
    amplitude) devient un écart chiffré. mu = branche(k2) depuis les params
    gelés de la table, jamais la mesure.
    """
    from mvcg.tables import load_table

    t = load_table("l4_gyrocorps_LITERATURE-HP2027.json")
    p = t["params"]
    w0, beta, k2 = float(p["omega0"]), float(p["beta"]), float(p["k2"])
    w_pred = math.sqrt(w0**2 + beta**2 * k2**4)
    return w_pred, {
        "table": "l4_gyrocorps_LITERATURE-HP2027.json",
        "vintage": t["vintage"],
        "method": "branche gappée P1-P2 gelée évaluée à k2",
        "rule": "omega^2(k) = omega0^2 + beta^2 k^4",
        "omega0": w0, "beta": beta, "k2": k2,
        "mu_ref": float(p["w2_m8_fine"]),
        "ansatz": "arrondis P1-P2 (u propagée, pas rétro-ajustée) ; dette assumée = transposition de régime AMP 0.3 -> 0.15",
        "unit_raw": "1 (unités internes GP)",
    }


def _l4_fenetre_branche() -> tuple[float, dict]:
    """Contact L4 — la branche gelée prédit-elle la fenêtre inertielle D₃ ?

    Protocole gelé : D3_pred = branche(k3)/vide(k3), la contrainte 1 de P4
    (deux nombres liés) pesée indirectement — si la branche gelée avant
    l'addendum prédit la fenêtre reformulée, le pont tient à ce niveau.
    """
    from mvcg.tables import load_table

    t = load_table("l4_gyrocorps_LITERATURE-HP2027.json")
    p = t["params"]
    w0, beta = float(p["omega0"]), float(p["beta"])
    k3, vide3 = float(p["k3"]), float(p["vide_k3"])
    w3 = math.sqrt(w0**2 + beta**2 * k3**4)
    d3 = w3 / vide3
    return d3, {
        "table": "l4_gyrocorps_LITERATURE-HP2027.json",
        "vintage": t["vintage"],
        "method": "branche gappée rapportée à la ligne vide calibrée à k3",
        "rule": "D3_pred = omega_branche(k3) / omega_vide(k3)",
        "omega_branche_k3": w3, "vide_k3": vide3,
        "mu_ref": float(p["D3_m8_addendum"]),
        "ansatz": "u(D_pred) en propagation relative (branche + ligne vide) ; u(D_obs)=0.5 déclarée (pic dominant, dédoublement m=10 exclu)",
        "unit_raw": "1 (rapport de fréquences)",
    }


def _l4_kappa_eff() -> tuple[float, dict]:
    """Contact L4 volet 2 — κ_eff implicite de la pente par Kelvin nu.

    Protocole L4-DEUX-NOMBRES-LIES.md (gelé avant run) : si la pente de la
    branche est d'origine Kelvin (forme nue ω_K = (κ/4π)k², convention
    « paramètres nus » du corpus), la circulation implicite est κ_eff = 4πβ.
    mu = κ_eff depuis β gelé de la table ; la référence κ=2π NE DOIT JAMAIS
    entrer dans le calcul.
    """
    from mvcg.tables import load_table

    t = load_table("l4_gyrocorps_LITERATURE-HP2027.json")
    p = t["params"]
    beta = float(p["beta"])
    return 4.0 * math.pi * beta, {
        "table": "l4_gyrocorps_LITERATURE-HP2027.json",
        "vintage": t["vintage"],
        "method": "circulation implicite d'une pente Kelvin : kappa_eff = 4 pi beta",
        "rule": "omega_K = (kappa/4pi) k^2, forme nue (paramètres nus), sans logarithme",
        "beta": beta,
        "mu_ref": 2.0 * math.pi,
        "ansatz": "dette de forme écrite : la variante log (k3, xi=0.3) donnerait kappa_eff x12,9 au lieu de x22,4 — sensibilité consignée au gel, verdict invariant",
        "unit_raw": "1 (unités internes GP)",
    }


def _l4_kelvin_gap() -> tuple[float, dict]:
    """Contact L4 volet 2 — la circulation pure ne produit pas de gap.

    Protocole gelé : ω_K → 0 quand k → 0 ; pred ω_K(k1) = (κ/4π)k1² gelé vs
    le gap universel 0.62. mu depuis κ et k1 gelés uniquement.
    """
    from mvcg.tables import load_table

    t = load_table("l4_gyrocorps_LITERATURE-HP2027.json")
    p = t["params"]
    kappa = 2.0 * math.pi
    k1 = float(p["k1"])
    return (kappa / 4.0 / math.pi) * k1**2, {
        "table": "l4_gyrocorps_LITERATURE-HP2027.json",
        "vintage": t["vintage"],
        "method": "loi de Kelvin nue évaluée à k1 — aucun terme de gap",
        "rule": "omega_K(k) = (kappa/4pi) k^2 ; omega_K -> 0 quand k -> 0",
        "kappa": kappa, "k1": k1,
        "mu_ref": 0.62,
        "ansatz": "le gap est une dette de structure, pas de circulation (P4 : ni corde ni gap nu) — chiffré ici",
        "unit_raw": "1 (unités internes GP)",
    }


def _corr_stabilite_energie() -> tuple[float, dict]:
    """Contact CORR — optimum de stabilité (E63) vs minimum d'énergie (E65).

    Protocole CORRIDOR-CROISE-CONTACTS.md (gelé avant run) : les deux
    facettes d'une même structure présentées unies par le corridor — la
    machine pèse leur décalage. mu = lecture E63, la référence E65 NE DOIT
    JAMAIS entrer dans le calcul.
    """
    from mvcg.tables import load_table

    t = load_table("corridor_cages_LITERATURE-E2026.json")
    p = t["params"]
    return float(p["e63_n_opt_marge"]), {
        "table": "corridor_cages_LITERATURE-E2026.json",
        "vintage": t["vintage"],
        "method": "lecture de l'optimum de marge E63 (kappa=0,05, t=90)",
        "rule": "l'optimum de stabilité minimise l'énergie par anneau",
        "mu_ref": float(p["e65_n_min_energie"]),
        "ansatz": "dette nommée : les facettes se découplent (E68 qualitative) — publié ici en verdict",
        "unit_raw": "1 (nombre de cages)",
    }


def _corr_fenetre_point() -> tuple[float, dict]:
    """Contact CORR — le point E61 (kappa=0,05) vs le bord bas E64-A.

    Protocole gelé : le point tient à t=90, la fenêtre est mesurée à t=180 —
    tare de temps de vol déclarée, la machine mesure l'écart à face value.
    mu = kappa E61 gelé par protocole ; la référence NE DOIT JAMAIS entrer
    dans le calcul.
    """
    from mvcg.tables import load_table

    t = load_table("corridor_cages_LITERATURE-E2026.json")
    p = t["params"]
    return float(p["e61_kappa"]), {
        "table": "corridor_cages_LITERATURE-E2026.json",
        "vintage": t["vintage"],
        "method": "lecture du point E61 (SUCCÈS à t=90)",
        "rule": "le point est compatible avec la fenêtre à face value",
        "mu_ref": float(p["e64a_bord_bas"]),
        "ansatz": "tare de temps de vol déclarée (90 vs 180) : deux horizons, pas une contradiction — l'écart est chiffré, la dette écrite",
        "unit_raw": "1 (kappa, unités internes)",
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
    "o7_carbon_d_lever": _o7_carbon_d_lever,
    "o8_bec_tc": _o8_bec_tc,
    "o9_h2o_pauling": _o9_h2o_pauling,
    "o10_carbonyl": _o10_carbonyl,
    "o11_bec_healing": _o11_bec_healing,
    "o12_cu_gamma": _o12_cu_gamma,
    "o13_co2_isotopologue": _o13_co2_isotopologue,
    "o14_tk_window": _o14_tk_window,
    "o15_h2_harmonic": _o15_h2_harmonic,
    "o16_cu_gamma_eff": _o16_cu_gamma_eff,
    "o17_h2_anharmonic": _o17_h2_anharmonic,
    "o18_h2_tare_lecture": _o18_h2_tare_lecture,
    "p31_lamb_dirac": _p31_lamb_dirac,
    "p31_lamb_mohr": _p31_lamb_mohr,
    "p31_lamb_erickson": _p31_lamb_erickson,
    "p32_lamb_modern": _p32_lamb_modern,
    "l4_gap_universel": _l4_gap_universel,
    "l4_branche_k2": _l4_branche_k2,
    "l4_fenetre_branche": _l4_fenetre_branche,
    "l4_kappa_eff": _l4_kappa_eff,
    "l4_kelvin_gap": _l4_kelvin_gap,
    "corr_stabilite_energie": _corr_stabilite_energie,
    "corr_fenetre_point": _corr_fenetre_point,
    "h0_ecart": _h0_ecart,
    "hz_sne_lowz": _hz_sne_lowz,
    "hz_sne_lit_sh0es": _hz_sne_lit_sh0es,
    "hz_sne_lit_planck": _hz_sne_lit_planck,
    "hz_sne_v2_planck": _hz_sne_v2_planck,
    "hz_sne_v2_sh0es": _hz_sne_v2_sh0es,
    "co_rot_abinitio": _co_rot_abinitio,
    "co_rot_dunham": _co_rot_dunham,
    "co13_rot_mu_rule": _co13_rot_mu_rule,
    "co_rot_kratzer": _co_rot_kratzer,
    "co_rot_alpha_e": _co_rot_alpha_e,
    "karplus_helix": _karplus_helix,
    "karplus_sheet": _karplus_sheet,
    "karplus_helix_vogelibax2007": _karplus_helix_vogelibax2007,
    "karplus_sheet_vogelibax2007": _karplus_sheet_vogelibax2007,
    "rydberg_voie2": _rydberg_voie2,
    "ckm_row1": _ckm_row1,
    "amu_wp20": _amu_wp20,
    "hvp_lo_lat_ee": _hvp_lo_lat_ee,
    "hlbl_lat_pheno": _hlbl_lat_pheno,
    "amu_wp25": _amu_delta,
    "hvp_pipi_cmd3": _hvp_pipi_cmd3,
    "landau_vc_he4": _landau_vc_he4,
    "bertsch_xi": _bertsch_xi,
    "kss_eta_s_he4": _kss_eta_s_he4,
    "kss_eta_s_qgp": _kss_eta_s_qgp,
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
        "H1s_Rydberg_Voie2", "micro", "pred", "si", "eV", "abs",
        5.838364428925748e-9,
        13.605693122994, "spectro<-H1s_Rydberg (1re voie)", "voir H1s_Rydberg",
        "R_∞ calculee (alpha^2 me*c^2 / 2e) = Rydberg_eV declare (coherence CODATA-2018)",
        "contact ouvert campagne croisee : seconde voie vers R_∞, decide=U k=1, theta=u_delta=5.838e-9 eV (propagation alpha x2 et me*c^2) ; dette de circularite declaree — meme ajustement CODATA, pendant du Dunham ; S+ annonce a ~0.02 U, suspense nul : certification de la fibre eV, pas de suspense",
        "rydberg_voie2",
        "ouverte", None, "",
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
    Contact(
        "O7_Carbon_D_Levier", "micro", "pred", "1", "cm^-1", "rel", 0.10,
        1350.0, "k<-desegaliser (actif)", "—",
        "bande D(graphite) = G * sqrt(r/(1+r)), r=3 (levier d'O3 active) = bande D observee",
        "contact ouvert O7 : levier d'O3 active, theta=0.10 INCHANGE (seuil gelé d'O3) ; mot inconnu au gel",
        "o7_carbon_d_lever",
        "ouverte", None, "O7",
    ),
    Contact(
        "O8_BEC_Tc", "micro", "pred", "si", "nK", "rel", 0.10,
        170.0, "n<-densite-effective", "—",
        "Tc(gaz de Bose ideal, 87Rb, n=3e19) = temperature critique observee",
        "contact ouvert O8 : gaz ideal declare, mot inconnu au gel ; theta=0.10 fige avant run (Tc inter-labo ~10 %)",
        "o8_bec_tc",
        "ouverte", None, "O8",
    ),
    Contact(
        "O9_H2O_Pauling", "micro", "pred", "si", "D", "rel", 0.10,
        1.8546, "q<-polarisation", "—",
        "mu(H2O) charges d'electronegativite Pauling = moment dipolaire observe",
        "contact ouvert O9 : echelle Pauling declaree, mot inconnu au gel ; theta=0.10 fige avant run",
        "o9_h2o_pauling",
        "ouverte", None, "O9",
    ),
    Contact(
        "O10_PMMA_Carbonyl", "micro", "pred", "1", "cm^-1", "rel", 0.10,
        1735.0, "k<-conjugaison", "—",
        "nu(C=O ester PMMA) par transfert de force depuis CH2O = bande observee",
        "contact ouvert O10 : transfert memes atomes, suspense minimal assume au gel ; theta=0.10 fige avant run",
        "o10_carbonyl",
        "ouverte", None, "O10",
    ),
    Contact(
        "O11_BEC_Healing", "micro", "pred", "si", "um", "rel", 0.10,
        0.55, "n<-densite-effective", "—",
        "xi(guerison, 87Rb) = 1/sqrt(8 pi n a_s) = taille observee",
        "contact ouvert O11 : Bogolioubov declare, mot inconnu au gel ; theta=0.10 fige avant run",
        "o11_bec_healing",
        "ouverte", None, "O11",
    ),
    Contact(
        "O12_Cu_Gamma", "micro", "pred", "si", "J m^-3 K^-2", "rel", 0.10,
        96.6, "m<-masse-effective", "—",
        "gamma(Cu, Sommerfeld masse libre) = chaleur specifique electronique mesuree",
        "contact ouvert O12 : masse libre declaree, mot inconnu au gel ; theta=0.10 fige avant run",
        "o12_cu_gamma",
        "ouverte", None, "O12",
    ),
    Contact(
        "O13_CO2_Isotopologue", "micro", "pred", "1", "cm^-1", "rel", 0.10,
        2273.7, "k<-anharmonicite", "—",
        "nu3(13CO2) par loi des masses depuis nu3(12CO2) = bande isotopologue observee",
        "contact ouvert O13 : isotopie declaree, mot inconnu au gel ; theta=0.10 fige avant run",
        "o13_co2_isotopologue",
        "ouverte", None, "O13",
    ),
    Contact(
        "O14_TK_Fenetre", "micro", "pred", "1", "1", "rel", 0.10,
        0.45, "La<-recalibrer", "—",
        "ID/IG(charbon graphitise, La=10nm) = C(514nm)/La = rapport observe",
        "contact ouvert O14 : TK dans sa fenetre (pendant d'O4), mot inconnu au gel ; theta=0.10 fige avant run",
        "o14_tk_window",
        "ouverte", None, "O14",
    ),
    Contact(
        "O15_H2_Harmonique", "micro", "pred", "1", "cm^-1", "rel", 0.10,
        4401.2, "k<-morse", "—",
        "omega_e(H2) par oscillateur harmonique a k=510 N/m declaree",
        "contact ouvert O15 : harmonique pur declare (comparaison vs omega_e, pas vs le fondamental), mot inconnu au gel",
        "o15_h2_harmonic",
        "ouverte", None, "O15",
    ),
    Contact(
        "O16_Cu_Gamma_Eff", "micro", "pred", "si", "J m^-3 K^-2", "rel", 0.10,
        96.6, "m<-masse-effective (active)", "—",
        "gamma(Cu, Sommerfeld masse effective 1.38 m_e declaree) = chaleur specifique electronique mesuree",
        "contact ouvert O16 : levier d'O12 active (pendant disciplinaire d'O7), m* declaree jamais derivee de la reference ; theta=0.10 fige avant run",
        "o16_cu_gamma_eff",
        "ouverte", None, "O16",
    ),
    Contact(
        "O17_H2_Anharmonique", "micro", "pred", "1", "cm^-1", "abs",
        0.5025932749251625,
        4160.0, "—", "—",
        "nu(1-0) H2 par Dunham ordre 1 (omega_e, omega_e x_e declarees) = fondamental declare 4160 (arrondi, u=0.5)",
        "contact ouvert O17 : dette d'O15 levee ; tare assumee = arrondi de declaration du fondamental (u=0.5 declaree), theta = u_delta = 0.5025932749251625 cm^-1, decide=U k=1 (convention GUM, precedent Rydberg voie 2), gele avant run ; estimation pre-run honnete : delta ~ 1.48 cm^-1, ratio ~ 2.94 -> P au cheveu de la borne S- annonce ; suspense reel, mot inconnu au gel",
        "o17_h2_anharmonic",
        "ouverte", None, "O17",
    ),
    Contact(
        "O18_H2_Tare_Lecture", "micro", "pred", "1", "cm^-1", "abs",
        2.887201644037585,
        4160.0, "lecture<-honnête (pendant d'O17)", "—",
        "nu(1-0) H2 par Dunham ordre 1 (memes extraits qu'O17) = fondamental declare 4160 relu a u = 5/sqrt(3)",
        "contact ouvert O18 : pendant disciplinaire d'O17 — meme transport, meme reference, meme delta ; seule la lecture de precision change (u = 2.8868 honnete vs 0.5 over-read), theta = u_delta = 2.887201644037585 cm^-1, decide=U k=1, gele avant run ; estimation pre-run : delta ~ 1.48, ratio ~ 0.5126, S+ attendu sans suspense (bande verifiee contre _adc) ; le verdict pese des declarations, pas des physiques",
        "o18_h2_tare_lecture",
        "ouverte", None, "O18",
    ),
    Contact(
        "P31_Lamb_Dirac", "micro", "pred", "1", "1", "abs", 0.05,
        1.0, "—", "—",
        "degenerescence 2S1/2 = 2P1/2 predite par Dirac seul (shift normalise 0) vs deplacement de Lamb mesure (normalise 1)",
        "contact ouvert P31 : dette historique — Dirac seul manque le Lamb shift de 100 % de l'effet ; grammaire P30_Kato_gaussian (score normalise, theta=0.05 fige avant run) ; S- attendu sans suspense : la machine quantifie la dette qui a fait naitre la QED (Lamb-Retherford 1947)",
        "p31_lamb_dirac",
        "ouverte", None, "P31",
    ),
    Contact(
        "P31_Lamb_Mohr", "micro", "pred", "si", "MHz", "abs",
        0.016643316977093238,
        1057.845, "—", "—",
        "Lamb(QED Mohr, annees 1970) = Lamb(mesure Lundeen-Pipkin 1981)",
        "contact ouvert P31 : theta = u_delta = 0.016643316977093238 MHz, decide=U k=1, gele avant run ; estimation pre-run honnete : delta ~ 0.019, ratio ~ 1.14, P au cheveu de S+ annonce (bande [theta, 2 theta] verifiee contre _adc) ; suspense reel, mot inconnu au gel ; vintages distincts declares (mesure posterieure aux calculs)",
        "p31_lamb_mohr",
        "ouverte", None, "P31",
    ),
    Contact(
        "P31_Lamb_Erickson", "micro", "pred", "si", "MHz", "abs",
        0.014212670403551895,
        1057.845, "—", "—",
        "Lamb(QED Erickson, annees 1970) = Lamb(mesure Lundeen-Pipkin 1981)",
        "contact ouvert P31 : theta = u_delta = 0.014212670403551895 MHz, decide=U k=1, gele avant run ; estimation pre-run honnete : delta ~ 0.067, ratio ~ 4.71, S- attendu sans suspense (Lundeen-Pipkin 1981 : « not in good agreement with theory ») ; meme mesure, autre calcul QED de la meme epoque : la machine tranche la ou les physiciens debattaient",
        "p31_lamb_erickson",
        "ouverte", None, "P31",
    ),
    Contact(
        "P32_Lamb_Modern", "micro", "pred", "si", "MHz", "abs",
        0.009848857801796104,
        1057.845, "—", "—",
        "Lamb(QED Pachucki 2001, reevaluation) = Lamb(mesure témoin Lundeen-Pipkin 1981, gel commun P31)",
        "contact ouvert P32 : la dette se ferme — meme temoin que P31 (Mohr P a 1,14 theta, Erickson S- a 4,71 theta) contre la theorie reevaluee ; theta = u_delta = 0.009848857801796104 MHz, decide=U k=1, gele avant run ; estimation pre-run : delta ~ 0.003 MHz, ratio ~ 0.305, S+ attendu suspense faible — le suspense est dans l'arc (la QED a paye sa dette), pas dans le mot ; dependance rp = 0.862(12) fm declaree dans la table",
        "p32_lamb_modern",
        "ouverte", None, "P32",
    ),
    Contact(
        "O19_CO2_nu3_Fine", "micro", "pred", "1", "cm^-1", "abs",
        0.1414213562373095,
        2349.3, "—", "—",
        "nu3(CO2) VFF a k transferee de CO = bande IR observee (12CO2)",
        "contact affiné O19 (REFINED-P-CONTACTS.md, gelé avant run) : D-bump de O2_CO2_nu3 — meme runner o2_co2_nu3, meme sha256, seules les déclarations d'incertitude changent ; comparaison posée en cm^-1 (abs) ; theta = u_delta = 0.1414213562373095 cm^-1 (u(VFF)=0.1, u(obs)=0.1), decide=U k=1 ; est. pre-run : delta ~ 340.085, ratio ~ 2405 -> S- attendu SANS suspense : le P grossier d'O2 cachait une dette de modèle 1D (k transférée de CO ne porte pas le paquet nu3)",
        "o2_co2_nu3",
        "ouverte", None, "O19",
    ),
    Contact(
        "O20_Carbon_D_Raman_Fine", "micro", "pred", "1", "cm^-1", "abs",
        5.0124844139408555,
        1350.0, "—", "—",
        "bande D(graphite) = bande G / sqrt(2) (chaine 1D k2=k1) = bande D observee",
        "contact affiné O20 (REFINED-P-CONTACTS.md, gelé avant run) : D-bump de O3_Carbon_D_Raman — meme runner o3_carbon_d_raman, meme sha256 ; comparaison en cm^-1 (abs) ; theta = u_delta = 5.0124844139408555 cm^-1 (u(G)=0.5 -> 0.3536, u(D_obs)=5.0), decide=U k=1 ; est. pre-run : delta ~ 232.771, ratio ~ 46.4 -> S- attendu SANS suspense : dette de la chaine 1D égale (bande D = double résonance + défauts, pas k2=k1)",
        "o3_carbon_d_raman",
        "ouverte", None, "O20",
    ),
    Contact(
        "SPEC_CO_Rot_Kratzer_Fine", "meso", "pred", "si", "Hz", "abs",
        5.0990195135927845,
        0.0, "B_e_omega_e<-autre-table-anharmonicite", "voir SPEC_CO_Rot_Kratzer",
        "4*B_e^3/omega_e^2 (Kratzer, entrees H&H) = D0 (mesure NIST)  (distorsion centrifuge ab initio)",
        "contact affiné SPEC (REFINED-P-CONTACTS.md, gelé avant run) : D-bump de SPEC_CO_Rot_Kratzer — meme runner co_rot_kratzer, meme sha256 ; theta = u_delta = 5.0990195135927845 Hz (u(De_pred H&H)=1.0 bornes prudentes déclarées, u(D0_obs)=5.0), decide=U k=1 ; est. pre-run : delta ~ 97.551, ratio ~ 19.1 -> S- attendu SANS suspense : le P au cheveu du grossier (theta=70 Hz, ratio 1,39) fondait sur une u(D0) trop étroite ; dette nommée vibrationnelle (Kratzer = équilibre, D0 = v=0)",
        "co_rot_kratzer",
        "ouverte", None, "SPEC",
    ),
    Contact(
        "P31_Lamb_Mohr_K2", "micro", "pred", "si", "MHz", "abs",
        0.016643316977093238,
        1057.845, "—", "—",
        "Lamb(QED Mohr, annees 1970) = Lamb(mesure Lundeen-Pipkin 1981)",
        "contact affiné P31 (REFINED-P-CONTACTS.md, gelé avant run) : couverture k=2 sur P31_Lamb_Mohr — meme runner p31_lamb_mohr, meme sha256, memes lignes GUM (mohr 0.014, lundeen_pipkin 0.009), uc inchangé ; decide=U k=2, U = 0.033286633954186476 MHz ; est. pre-run : delta ~ 0.019, ratio delta/U ~ 0.571 -> S+ attendu ; trace écrite : le mot dépend de la couverture (à k=1 le même écart est P à 1,14 uc) ; la dette vintage est à ~1 sigma, compatible au seuil 95 %",
        "p31_lamb_mohr",
        "ouverte", None, "P31",
    ),
    Contact(
        "L4_Gap_Universel", "meso", "pred", "1", "1", "abs",
        0.0282842712474619,
        0.630, "—", "—",
        "gap universel : omega(k1, m=12, vague fine) = omega(k1, m=5, vague fine)  (insensibilite a l'inertie du milieu)",
        "chantier L4 (L4-GYROCORPS-CONTACTS.md, gelé avant run) : transposition du corpus hors-programme gap gyroscopique (notes P1-P4 + addendum, vintage HP distinct declare, aucune retro-injection) ; theta = u_delta = 0.0282842712474619 (u=0,02 declaree de part et d'autre, dispersion corpus), decide=U k=1 ; est. pre-run : delta = 0,010, ratio 0,354 -> S+ attendu, suspense faible : la propriete la plus robuste du corpus confirmee en pesee croisee fine/fine",
        "l4_gap_universel",
        "ouverte", None, "L4",
    ),
    Contact(
        "L4_Branche_k2_RegimeFin", "meso", "pred", "1", "1", "abs",
        0.02138372495786989,
        0.58, "—", "—",
        "branche gappee P1-P2 (omega0=0.45, beta=11.2, geles) evaluee a k2 au regime fin = omega(k2, m=8, AMP=0.15, addendum)",
        "chantier L4 (L4-GYROCORPS-CONTACTS.md, gelé avant run) : la dette ouverte du corpus (dependance en amplitude, AMP 0.3 -> 0.15) devient un ecart chiffre ; theta = u_delta = 0.02138372495786989 (u(branch)=0,007567 par propagation des arrondis omega0/beta, u(obs)=0,02 declaree), decide=U k=1 ; est. pre-run : delta ~ 1,205, ratio ~ 56 -> S- attendu SANS suspense : la retractation de l'addendum P3 pesee — la branche ne se transpose pas a k2 en regime fin",
        "l4_branche_k2",
        "ouverte", None, "L4",
    ),
    Contact(
        "L4_Fenetre_Branche", "meso", "pred", "1", "1", "abs",
        0.5815053896029518,
        6.9, "—", "—",
        "D3_pred = branche gappee(k3) / ligne vide calibree(k3) = D3(m=8) addendum  (fenetre inertielle, contrainte 1 de P4 pesée indirectement)",
        "chantier L4 (L4-GYROCORPS-CONTACTS.md, gelé avant run) : si la branche gelée avant l'addendum predit la fenetre reformulee, le pont 'deux nombres lies' tient a ce niveau ; theta = u_delta = 0.5815053896029518 (u(D_pred)=0,2969 propagation relative branche+ligne vide, u(D_obs)=0,5 declaree, pic dominant, dedoublement m=10 exclu), decide=U k=1 ; est. pre-run : delta ~ 0,696, ratio ~ 1,20 -> P annonce AU CHEVEU, suspense maximal",
        "l4_fenetre_branche",
        "ouverte", None, "L4",
    ),
    Contact(
        "L4_Kappa_Eff", "meso", "pred", "1", "1", "abs",
        0.6283185307179586,
        6.283185307179586, "—", "—",
        "circulation implicite d'une pente d'origine Kelvin (kappa_eff = 4 pi beta, forme nue) = circulation declaree du banc (kappa = 2 pi)",
        "chantier L4 volet 2 (L4-DEUX-NOMBRES-LIES.md, gelé avant run) : la moitié PENTE du lien 'deux nombres lies' pesée directement ; theta = u(4 pi beta) = 0.6283185307179586 (u(beta)=0,05 propagée, ligne unique), decide=U k=1 ; est. pre-run : mu_loc ~ 140,743, delta ~ 134,460, ratio ~ 214 -> S- attendu SANS suspense : la pente exige une circulation x22,4 — la demultiplication du corpus restatee comme dette de circulation ; sensibilité declaree (forme log favorable : x12,9, verdict invariant)",
        "l4_kappa_eff",
        "ouverte", None, "L4",
    ),
    Contact(
        "L4_Kelvin_Gap", "meso", "pred", "1", "1", "abs",
        0.02,
        0.62, "—", "—",
        "gap produit par une circulation pure (omega_K(k1) = (kappa/4pi) k1^2, aucun terme de gap) = gap universel mesure 0.62",
        "chantier L4 volet 2 (L4-DEUX-NOMBRES-LIES.md, gelé avant run) : la moitié GAP du lien pesée directement — la circulation seule ne produit pas de gap (omega_K -> 0 quand k -> 0) ; theta = u = 0.02 (lecture declaree du gap, ligne unique), decide=U k=1 ; est. pre-run : mu_loc ~ 0,01928, delta ~ 0,60072, ratio ~ 30 -> S- attendu SANS suspense : le gap est une dette de structure, pas de circulation (P4 : ni corde ni gap nu — chiffre ici)",
        "l4_kelvin_gap",
        "ouverte", None, "L4",
    ),
    Contact(
        "CORR_Stabilite_Energie", "meso", "pred", "1", "1", "abs",
        1.4142135623730951,
        18.0, "—", "—",
        "optimum de stabilite E63 (n=14, marge max) = minimum d'energie par anneau E65 (n=18)  (les deux facettes d'une meme structure)",
        "chantier CORR corridor croise (CORRIDOR-CROISE-CONTACTS.md, gelé avant run) : tension inter-campagnes du corridor jamais chiffree comme telle ; theta = u_delta = 1.4142135623730951 (u(n)=1 déclaree de part et d'autre, comptage entier sans interpolation), decide=U k=1 ; est. pre-run : delta = 4, ratio 2,83 -> S- attendu SANS suspense : les facettes se decouplent (E68 l'avait refute qualitativement), la machine le publie en verdict",
        "corr_stabilite_energie",
        "ouverte", None, "CORR",
    ),
    Contact(
        "CORR_Fenetre_Point", "meso", "pred", "1", "1", "abs",
        0.007216878364870325,
        0.075, "—", "—",
        "point E61 (kappa=0,05 tient a t=90) compatible avec la fenetre E64-A (bord bas 0,075, t=180) a face value",
        "chantier CORR corridor croise (CORRIDOR-CROISE-CONTACTS.md, gelé avant run) : theta = u = 0.007216878364870325 (bracket rectangulaire du bord bas, demi-largeur 0,0125/sqrt(3), ligne unique), decide=U k=1 ; est. pre-run : delta = 0,025, ratio 3,46 -> S- attendu, suspense modere : le point est hors fenetre a face value ; dette nommee = tare de temps de vol (90 vs 180, deux horizons pas une contradiction) — l'ecart est chiffre",
        "corr_fenetre_point",
        "ouverte", None, "CORR",
    ),
    Contact(
        "H0_Ecart_Planck_SH0ES", "macro", "pred", "1", "1", "abs", 0.05,
        0.0, "f<-Planck_ou_SH0ES", "—",
        "|H0_SH0ES/H0_Planck - 1| = 0  (une seule constante de Hubble)",
        "contact ouvert H0 : tension de deux fabrications declarees, ne pas moyenner ; mot inconnu au gel ; theta=0.05 fige avant run",
        "h0_ecart",
        "ouverte", None, "H0",
    ),
    Contact(
        "H0_Hz_SNe_LOWZ_DEMO", "macro", "pred", "1", "mag", "abs", 0.05,
        0.0, "H0<-SH0ES_ou_autre", "voir H0_Ecart_Planck_SH0ES",
        "rms(mu_pred(H(z) Planck declare) - mu_obs SNe) = 0  (la courbe passe par les bins)",
        "contact H0 bas-z : extract DEMO synthétique (fiducial H0=70 declare, seed gele) — validation de protocole, rien sur l'univers reel ; table LITERATURE a declarer ; theta=0.05 mag fige avant run ; est. pre-run delta~0.096, au bord S- — suspense maximal",
        "hz_sne_lowz",
        "ouverte", None, "H0",
    ),
    Contact(
        "H0_Hz_SNe_LOWZ_LIT_SH0ES", "macro", "pred", "1", "mag", "abs", 0.02756,
        0.0, "H0<-SH0ES_ou_autre", "voir H0_Hz_SNe_LOWZ_DEMO",
        "rms(mu_pred(H(z) Planck declare) - mu_obs SNe Pantheon+ ancres SH0ES) = 0  (la courbe passe par les bins)",
        "contact H0 bas-z LITERATURE : Pantheon+ Brout 2022 Table 7, 8 bins bas-z, amplitude ancree SH0ES 73,04 (transposition exacte, dette d'independance) ; theta=0.02756 = sigma bins declare, gele avant run ; est. pre-run : courbe Planck decalee de +0.1745 mag -> S- attendu sans suspense",
        "hz_sne_lit_sh0es",
        "ouverte", None, "H0",
    ),
    Contact(
        "H0_Hz_SNe_LOWZ_LIT_PLANCK", "macro", "pred", "1", "mag", "abs", 0.02756,
        0.0, "H0<-SH0ES_ou_autre", "voir H0_Hz_SNe_LOWZ_DEMO",
        "rms(mu_pred(H(z) Planck declare) - mu_obs SNe Pantheon+ ancres Planck) = 0  (la courbe passe par les bins)",
        "contact H0 bas-z LITERATURE : memes bins ancres Planck 67,4 (miroir exact, dette d'ancrage) ; theta=0.02756 gele avant run ; est. pre-run : courbe Planck = ancrage, residu = bruit realise des bins -> P au cheveu, suspense reel",
        "hz_sne_lit_planck",
        "ouverte", None, "H0",
    ),
    Contact(
        "H0_Hz_SNe_LOWZ_V2_PLANCK", "macro", "pred", "1", "mag", "abs", 0.027737,
        0.0, "H0<-courbe_PLANCK_ou_SH0ES", "voir H0_Hz_SNe_LOWZ_LIT_PLANCK",
        "rms(mu_pred(H(z) courbe Planck 67,4 posee) - mu_obs SNe Pantheon+ MU_SH0ES natif) = 0  (la courbe passe par les bins)",
        "contact H0 bas-z V2 : memes 8 bins, amplitude MU_SH0ES native (dette de forme +0,049 supprimee, campagne 7) ; courbe Planck posee par le contact, H0 lu dans la table ; theta=0.027737 gele avant run ; est. pre-run : decalage ~+0,1766 mag quasi constant -> S- attendu sans suspense (miroir de V1_SH0ES) ; V2 complete V1 sans la remplacer",
        "hz_sne_v2_planck",
        "ouverte", None, "H0",
    ),
    Contact(
        "H0_Hz_SNe_LOWZ_V2_SH0ES", "macro", "pred", "1", "mag", "abs", 0.027737,
        0.0, "H0<-courbe_PLANCK_ou_SH0ES", "voir H0_Hz_SNe_LOWZ_LIT_SH0ES",
        "rms(mu_pred(H(z) courbe SH0ES 73,04 posee) - mu_obs SNe Pantheon+ MU_SH0ES natif) = 0  (la courbe passe par les bins)",
        "contact H0 bas-z V2 : courbe SH0ES posee sur amplitude native SH0ES ; theta=0.027737 gele avant run ; est. pre-run : residu = bruit realise des bins, delta/theta ~0,897 -> S+ attendu AU CHEVEU, le bruit realise decide ; suspense reel",
        "hz_sne_v2_sh0es",
        "ouverte", None, "H0",
    ),
    Contact(
        "SPEC_CO_Rot_AbInitio", "meso", "pred", "si", "Hz", "abs", 3000.0,
        0.0, "r_e<-autre-mesure-geometrie", "—",
        "|B_e calcule (hbar/4 pi mu r_e^2) - B0 mesure NIST| = 0  (rotor rigide a l'equilibre = niveau v=0)",
        "contact SPEC rotationnel 2026-09-14 : CO X1Sigma+, r_e H&H 1979, mu NIST JPCRD 53 ; theta=3000 Hz = u(B0) gele avant run ; est. pre-run : delta ~ 265 MHz ~ alpha_e/2 (zero vibratoire), S- attendu SANS suspense — lecon : le rotor rigide a l'equilibre ne predit pas le niveau v=0 ; protocole SPEC-CO-ROT-PROTOCOLE.md",
        "co_rot_abinitio",
        "ouverte", None, "SPEC",
    ),
    Contact(
        "SPEC_CO_Rot_Dunham", "meso", "pred", "si", "Hz", "abs", 10000.0,
        0.0, "B0_D0<-autre-ajustement", "voir SPEC_CO_Rot_AbInitio",
        "2*B0 - 4*D0 (NIST) = nu(1-0) NIST  (coherence interne du catalogue)",
        "contact SPEC rotationnel 2026-09-14 : transport de table 2B0-4D0 vs nu mesure ; theta=10000 Hz = u(nu) gele avant run ; est. pre-run : delta ~ 280 Hz, delta/theta ~ 0,03 -> S+ attendu SANS suspense ; dette circularite ecrite (meme ajustement) — calibre le transport, pas une prediction independante",
        "co_rot_dunham",
        "ouverte", None, "SPEC",
    ),
    Contact(
        "SPEC_CO13_Rot_MuRule", "meso", "pred", "si", "Hz", "abs", 12000.0,
        0.0, "mu_prime<-autre-isotopologue", "voir SPEC_CO_Rot_Dunham",
        "B0(12CO) * mu/mu' = B0'(13CO, mesure NIST)  (regle de la masse reduite au niveau v=0)",
        "contact SPEC isotopologue 2026-09-14 (protocole §3, declare avant run) : regle mu/mu' appliquee telle quelle a B0 ; theta=12000 Hz = u(B0') gele avant run ; est. pre-run : delta ~ 4,3 MHz, delta/theta ~ 360 -> S- attendu SANS suspense ; l'ecart nomme la correction isotopique vibration-rotation (alpha_e non purement 1/mu) + au-dela de Born-Oppenheimer ; le suspense porte sur la taille de l'ecart, pas sur le mot",
        "co13_rot_mu_rule",
        "ouverte", None, "SPEC",
    ),
    Contact(
        "SPEC_CO_Rot_Kratzer", "meso", "pred", "si", "Hz", "abs", 70.0,
        0.0, "B_e_omega_e<-autre-table-anharmonicite", "voir SPEC_CO13_Rot_MuRule",
        "4*B_e^3/omega_e^2 (Kratzer, entrees H&H) = D0 (mesure NIST)  (distorsion centrifuge ab initio)",
        "contact SPEC Kratzer 2026-09-14 (protocole §4, declare avant run) : prediction croisee — B_e et omega_e H&H independants de l'ajustement NIST de D0 ; theta=70 Hz = u(D0) gele avant run ; est. pre-run : delta ~ 70-80 Hz, delta/theta ~ 1,0-1,1 -> zone P AU CHEVEU, SUSPENSE MAXIMAL (P, S+ et S- accessibles selon les arrondis H&H) ; dettes : D_e vs D0 (ecart vibrationnel ~0,2 Hz), vintage H&H, Kratzer=Morse",
        "co_rot_kratzer",
        "ouverte", None, "SPEC",
    ),
    Contact(
        "SPEC_CO_Rot_AlphaE", "meso", "pred", "si", "Hz", "abs", 3000.0,
        0.0, "alpha_e<-table-rotation-vibration-recente", "voir SPEC_CO_Rot_AbInitio",
        "B_e,calc - alpha_e/2 = B0 (mesure NIST)  (rotor rigide + correction vibration-rotation)",
        "levier SPEC 2026-09-14 (protocole §5, declare avant run) : le levier d'AbInitio — meme calcul moins alpha_e/2 H&H ; theta=3000 Hz gele avant run ; est. pre-run : le contact 1 a mesure un residu de 76007 Hz apres soustraction de alpha_e/2 attendu, delta/theta ~ 25 -> S- attendu SANS suspense ; le levier reduit l'ecart d'un facteur ~3500, le residu nomme la dette de vintage H&H 1979 vs NIST 2013 ; coherent avec le P de Kratzer",
        "co_rot_alpha_e",
        "ouverte", None, "SPEC",
    ),
    Contact(
        "NMR_Karplus_Helix", "micro", "pred", "si", "Hz", "rel", 0.10,
        4.0, "coefficients<-autre-parametrisation", "—",
        "3J(HN,Ha) helice par loi de Karplus (coefficients gelés) = ordre de grandeur typique declare",
        "contact ouvert NMR : reference typique 'pas un PDB' declaree, dette attendue ; theta=0.10 fige avant run",
        "karplus_helix",
        "ouverte", None, "NMR",
    ),
    Contact(
        "NMR_Karplus_Sheet", "micro", "pred", "si", "Hz", "rel", 0.10,
        8.5, "coefficients<-autre-parametrisation", "—",
        "3J(HN,Ha) brin par même loi de Karplus = ordre de grandeur typique declare",
        "contact ouvert NMR : meme loi, autre conformation (carte) ; estimation pre-run zone P, suspense reel au bord S-",
        "karplus_sheet",
        "ouverte", None, "NMR",
    ),
    Contact(
        "NMR_Karplus_Helix_VogeliBax2007", "micro", "pred", "si", "Hz", "rel", 0.10,
        4.0, "coefficients<-Vuister-Bax-1993 (1re voie)", "voir NMR_Karplus_Helix",
        "3J(HN,Ha) helice par loi de Karplus Vogeli-Bax 2007 (coefficients gelés) = même référence typique declare",
        "contact ouvert campagne croisee : 2e voie canonique (JACS 2007, 129, 9377), même phi et même référence que la paire VB, theta=0.10 identique ; parametrisation choisie pour sa canonicite, jamais pour un mot attendu",
        "karplus_helix_vogelibax2007",
        "ouverte", None, "NMR",
    ),
    Contact(
        "NMR_Karplus_Sheet_VogeliBax2007", "micro", "pred", "si", "Hz", "rel", 0.10,
        8.5, "coefficients<-Vuister-Bax-1993 (1re voie)", "voir NMR_Karplus_Sheet",
        "3J(HN,Ha) brin par loi de Karplus Vogeli-Bax 2007 (coefficients gelés) = même référence typique declare",
        "contact ouvert campagne croisee : même loi 2e voie, autre conformation ; question — les deux voies changent-elles le mot ? theta=0.10 identique à la paire VB",
        "karplus_sheet_vogelibax2007",
        "ouverte", None, "NMR",
    ),
    Contact(
        "CKM_Row1_Unitarity", "micro", "pred", "1", "1", "abs", 0.0007,
        1.0, "somme<-autres-entrees", "—",
        "|Vud|^2+|Vus|^2+|Vub|^2 = 1 (unitarite de la 1re ligne)",
        "contact ouvert CKM : somme declaree PDG, decide=U k=2 ; suspense reel δ/U=1.14 au cheveu du S+",
        "ckm_row1",
        "ouverte", None, "CKM",
    ),
    Contact(
        "AMU_exp_minus_WP20", "macro", "pred", "1", "1e-11", "abs", 76.0,
        0.0, "HVP<-lattice (autre id)", "identification lattice : contact separe si monte",
        "a_exp - a_SM(WP20) = 0  (identification dispersive declaree)",
        "contact ouvert g-2 : etalonnage ecart normalise (theta=76=u_delta, decide=U k=1), identification dispersive declaree ; mot attendu S- net (d/U=3,67), robuste jusqu'a k=3",
        "amu_wp20",
        "ouverte", None, "g-2",
    ),
    Contact(
        "HVP_LO_lat_vs_ee", "macro", "pred", "1", "1e-11", "abs", 72.9,
        0.0, "ee<-autre-moyenne", "voir AMU_exp_minus_WP20",
        "a_HVP_LO(WP25 lat) = a_HVP_LO(WP20 ee)",
        "contact ouvert g-2 : deux fabrications du meme terme, decide=U k=2 ; P attendu AU CHEVEU du S- (d/U=1,38 ; S- a k=1) — suspense declare",
        "hvp_lo_lat_ee",
        "ouverte", None, "g-2",
    ),
    Contact(
        "HLbL_lat_vs_pheno", "macro", "pred", "1", "1e-11", "abs", 12.6,
        0.0, "lat<-autre-ensemble", "voir HVP_LO_lat_vs_ee",
        "a_HLbL(lat WP25) = a_HLbL(pheno WP25)",
        "contact ouvert g-2 : deux fabrications du meme terme, decide=U k=2 ; S+ attendu (d/U=0,76 ; P a k=1) — suspense declare ; note mouture 6 « k=2 -> P » corrigee",
        "hlbl_lat_pheno",
        "ouverte", None, "g-2",
    ),
    Contact(
        "AMU_Delta_WP25", "macro", "pred", "1", "1e-11", "abs", 63.0,
        0.0, "HVP<-e+e- (autre id)", "voir AMU_exp_minus_WP20",
        "a_exp - a_SM(WP25) = 0  (SM complet, identification lattice declaree)",
        "contact ouvert AMU : ecart porte en unites de son incertitude, autre identification declaree jamais choisie apres coup ; theta=63=u_delta fige avant run ; S+ a 0,6 U, pendant de WP20 (S- a 3,7 U) — la paire d'identifications est complete",
        "amu_wp25",
        "ouverte", None, "AMU",
    ),
    Contact(
        "HVP_Pipi_CMD3_vs_PreAvg", "macro", "pred", "1", "1e-11", "abs",
        54.037024344425184,
        0.0, "KLOE<-seul (autre id)", "voir AMU_Delta_WP25",
        "a(2pi, CMD-3) - a(2pi, moyenne pre-CMD-3) = 0  (deux fabrications exp du meme terme)",
        "contact ouvert campagne croisee : ecart porte tel que publie par le PRL CMD-3, theta=54.037=u_delta quadrature (independance assumée), decide=U k=1 ; moyenne pre-CMD-3 KLOE-dominee (identification declaree, jamais choisie apres coup), dette de fenetre ecrite ; S- attendu a 3.7 U — contact de calibre, pas de suspense",
        "hvp_pipi_cmd3",
        "ouverte", None, "g-2",
    ),
    Contact(
        "Landau_Vc_He4", "micro", "pred", "si", "m/s", "rel", 0.10,
        58.0, "spectre<-autre-mesure", "—",
        "v_c = min_p E(p)/p (Landau 1941) sur spectre phonon-roton declare",
        "contact ouvert hyperfluidite : cohérence interne de la carte spectrale, dette quasi-tautologie declaree au gel ; theta=0.10 fige avant run",
        "landau_vc_he4",
        "ouverte", None, "hyperfluidite",
    ),
    Contact(
        "Bertsch_Xi_Unitary", "micro", "pred", "1", "1", "abs", 0.10,
        0.370, "xi<-autre-ansatz", "—",
        "xi = (5/3) E/(N eps_F) BCS mean-field (Leggett 1980) a l'unite",
        "contact ouvert hyperfluidite : dette mean-field declaree (ansatz pauvre = pendant exact de P27 He HF) ; theta=0.10 fige avant run ; S- attendu net",
        "bertsch_xi",
        "ouverte", None, "hyperfluidite",
    ),
    Contact(
        "KSS_EtaS_He4", "micro", "pred", "1", "1", "rel", 0.10,
        1.0, "eta/s<-autre-mesure", "—",
        "eta/s >= hbar/(4 pi k_B) (KSS 2005) ; marge du 4He declaree au-dessus du plancher",
        "contact ouvert hyperfluidite : la borne n'est PAS une identite — le mot mesure la marge (8,8 planchers), pas la validite de KSS ; theta=0.10 fige avant run ; S- attendu net",
        "kss_eta_s_he4",
        "ouverte", None, "hyperfluidite",
    ),
    Contact(
        "KSS_EtaS_QGP", "micro", "pred", "1", "1", "rel", 0.10,
        1.0, "eta/s<-autre-extraction", "—",
        "eta/s >= hbar/(4 pi k_B) (KSS 2005) ; le QGP sature-t-il le plancher ?",
        "contact ouvert hyperfluidite : premier mot qui tranche une question ouverte (saturation KSS) — borne inf declaree (2 planchers) vs plancher ; S- = non-saturation etablie, jamais 'KSS violee' ; theta=0.10 fige avant run",
        "kss_eta_s_qgp",
        "ouverte", None, "hyperfluidite",
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
_GUM["CKM_Row1_Unitarity"] = {
    "decide": "U",
    "k": 2,
    "lines": [{"name": "sum_PDG", "type": "B", "u": 0.0007}],
}
_GUM["H0_Ecart_Planck_SH0ES"] = {
    "decide": "theta",
    "k": 2,
    "lines": [
        {"name": "Planck", "type": "B", "u": 0.5 / 67.4, "c": 1},
        {"name": "SH0ES", "type": "B", "u": 1.04 / 67.4, "c": 1},
    ],
    "R": [[1.0, 0.0], [0.0, 1.0]],
}
_GUM["H0_Hz_SNe_LOWZ_DEMO"] = {
    "decide": "theta",
    "k": 2,
    "lines": [{"name": "bins_SNe", "type": "B", "u": 0.05, "note": "mag, dispersion declaree des bins (DEMO)"}],
}
_GUM["H0_Hz_SNe_LOWZ_LIT_SH0ES"] = {
    "decide": "theta",
    "k": 2,
    "lines": [{"name": "bins_SNe_Pantheon", "type": "B", "u": 0.02756,
               "note": "mag, incertitudes declarees e_mBcorr/rac(N), "
                       "calibration commune NON reduite (dette)"}],
}
_GUM["H0_Hz_SNe_LOWZ_LIT_PLANCK"] = {
    "decide": "theta",
    "k": 2,
    "lines": [{"name": "bins_SNe_Pantheon", "type": "B", "u": 0.02756,
               "note": "mag, incertitudes declarees e_mBcorr/rac(N), "
                       "calibration commune NON reduite (dette)"}],
}
_GUM["H0_Hz_SNe_LOWZ_V2_PLANCK"] = {
    "decide": "theta",
    "k": 2,
    "lines": [{"name": "bins_SNe_Pantheon", "type": "B", "u": 0.027737,
               "note": "mag, incertitudes declarees MU_SH0ES_ERR_DIAG/rac(N), "
                       "calibration commune NON reduite (dette)"}],
}
_GUM["H0_Hz_SNe_LOWZ_V2_SH0ES"] = {
    "decide": "theta",
    "k": 2,
    "lines": [{"name": "bins_SNe_Pantheon", "type": "B", "u": 0.027737,
               "note": "mag, incertitudes declarees MU_SH0ES_ERR_DIAG/rac(N), "
                       "calibration commune NON reduite (dette)"}],
}
_GUM["SPEC_CO_Rot_AbInitio"] = {
    "decide": "theta",
    "k": 2,
    "lines": [{"name": "B0_NIST", "type": "B", "u": 3000.0,
               "note": "Hz, u(B0) declaree NIST JPCRD 53"}],
}
_GUM["SPEC_CO_Rot_Dunham"] = {
    "decide": "theta",
    "k": 2,
    "lines": [{"name": "nu_NIST", "type": "B", "u": 10000.0,
               "note": "Hz, u(nu 1-0) declaree NIST JPCRD 53, "
                       "circularite B0/D0/nu ecrite (dette)"}],
}
_GUM["SPEC_CO13_Rot_MuRule"] = {
    "decide": "theta",
    "k": 2,
    "lines": [{"name": "B0p_NIST", "type": "B", "u": 12000.0,
               "note": "Hz, u(B0' 13CO) declaree NIST JPCRD 53, "
                       "meme table (validation croisee interne, dette)"}],
}
_GUM["SPEC_CO_Rot_Kratzer"] = {
    "decide": "theta",
    "k": 2,
    "lines": [{"name": "D0_NIST", "type": "B", "u": 70.0,
               "note": "Hz, u(D0) declaree NIST JPCRD 53 ; entrees H&H "
                       "arrondies 6 chiffres, suspense au cheveu (dette)"}],
}
_GUM["SPEC_CO_Rot_AlphaE"] = {
    "decide": "theta",
    "k": 2,
    "lines": [{"name": "B0_NIST", "type": "B", "u": 3000.0,
               "note": "Hz, u(B0) declaree NIST JPCRD 53 ; alpha_e H&H "
                       "3 chiffres (1976), residu = dette de vintage"}],
}
_GUM["AMU_exp_minus_WP20"] = {
    "decide": "U",
    "k": 1,
    "lines": [{"name": "delta_WP20", "type": "B", "u": 76.0}],
}
_GUM["AMU_Delta_WP25"] = {
    "decide": "U",
    "k": 1,
    "lines": [{"name": "delta_WP25", "type": "B", "u": 63.0}],
}
_GUM["HVP_Pipi_CMD3_vs_PreAvg"] = {
    "decide": "U",
    "k": 1,
    "lines": [
        {"name": "CMD3_2pi", "type": "B", "u": 42.0},
        {"name": "premoy_2pi", "type": "B", "u": 34.0},
    ],
    "R": [[1.0, 0.0], [0.0, 1.0]],
}
_GUM["H1s_Rydberg_Voie2"] = {
    "decide": "U",
    "k": 1,
    "lines": [
        {"name": "R_inf_calc", "type": "B", "u": 5.838306535712686e-9},
        {"name": "R_inf_declaree", "type": "B", "u": 2.6e-11},
    ],
    "R": [[1.0, 0.0], [0.0, 1.0]],
}
_GUM["HVP_LO_lat_vs_ee"] = {
    "decide": "U",
    "k": 2,
    "lines": [
        {"name": "lat_WP25", "type": "B", "u": 61.0},
        {"name": "ee_WP20", "type": "B", "u": 40.0},
    ],
    "R": [[1.0, 0.0], [0.0, 1.0]],
}
_GUM["HLbL_lat_vs_pheno"] = {
    "decide": "U",
    "k": 2,
    "lines": [
        {"name": "lat", "type": "B", "u": 9.0},
        {"name": "pheno", "type": "B", "u": 8.8},
    ],
    "R": [[1.0, 0.0], [0.0, 1.0]],
}
_GUM["O17_H2_Anharmonique"] = {
    "decide": "U",
    "k": 1,
    "lines": [
        {"name": "nu_pred_Dunham", "type": "B", "u": 0.050990195135927854},
        {"name": "nu10_declaree", "type": "B", "u": 0.5},
    ],
    "R": [[1.0, 0.0], [0.0, 1.0]],
}
_GUM["O18_H2_Tare_Lecture"] = {
    "decide": "U",
    "k": 1,
    "lines": [
        {"name": "nu_pred_Dunham", "type": "B", "u": 0.050990195135927854},
        {"name": "nu10_relue_honnete", "type": "B", "u": 2.886751345948129},
    ],
    "R": [[1.0, 0.0], [0.0, 1.0]],
}
_GUM["P31_Lamb_Mohr"] = {
    "decide": "U",
    "k": 1,
    "lines": [
        {"name": "mohr_QED", "type": "B", "u": 0.014},
        {"name": "lundeen_pipkin", "type": "B", "u": 0.009},
    ],
    "R": [[1.0, 0.0], [0.0, 1.0]],
}
_GUM["P31_Lamb_Erickson"] = {
    "decide": "U",
    "k": 1,
    "lines": [
        {"name": "erickson_QED", "type": "B", "u": 0.011},
        {"name": "lundeen_pipkin", "type": "B", "u": 0.009},
    ],
    "R": [[1.0, 0.0], [0.0, 1.0]],
}
_GUM["P32_Lamb_Modern"] = {
    "decide": "U",
    "k": 1,
    "lines": [
        {"name": "pachucki2001_QED", "type": "B", "u": 0.004},
        {"name": "lundeen_pipkin_temoin", "type": "B", "u": 0.009},
    ],
    "R": [[1.0, 0.0], [0.0, 1.0]],
}
_GUM["O19_CO2_nu3_Fine"] = {
    "decide": "U",
    "k": 1,
    "lines": [
        {"name": "nu_pred_VFF", "type": "B", "u": 0.1,
         "note": "cm^-1, u déclarée (VFF 1D grossier, k transférée de CO)"},
        {"name": "nu3_obs", "type": "B", "u": 0.1,
         "note": "cm^-1, u déclarée (dispersion bande rotation-vibration sous le paquet nu3)"},
    ],
    "R": [[1.0, 0.0], [0.0, 1.0]],
}
_GUM["O20_Carbon_D_Raman_Fine"] = {
    "decide": "U",
    "k": 1,
    "lines": [
        {"name": "D_pred", "type": "B", "u": 0.3535533905932738,
         "note": "cm^-1, u(G)=0.5 déclarée / sqrt(2) (transfert chaîne 1D)"},
        {"name": "D_obs", "type": "B", "u": 5.0,
         "note": "cm^-1, u déclarée (bande de défaut, dispersion inter-échantillons)"},
    ],
    "R": [[1.0, 0.0], [0.0, 1.0]],
}
_GUM["SPEC_CO_Rot_Kratzer_Fine"] = {
    "decide": "U",
    "k": 1,
    "lines": [
        {"name": "De_pred_HH", "type": "B", "u": 1.0,
         "note": "Hz, bornes prudentes déclarées sur entrées H&H arrondies (PAS NIST)"},
        {"name": "D0_obs", "type": "B", "u": 5.0,
         "note": "Hz, u déclarée (dispersion mesure D0)"},
    ],
    "R": [[1.0, 0.0], [0.0, 1.0]],
}
_GUM["P31_Lamb_Mohr_K2"] = {
    "decide": "U",
    "k": 2,
    "lines": [
        {"name": "mohr_QED", "type": "B", "u": 0.014},
        {"name": "lundeen_pipkin", "type": "B", "u": 0.009},
    ],
    "R": [[1.0, 0.0], [0.0, 1.0]],
}
_GUM["L4_Gap_Universel"] = {
    "decide": "U",
    "k": 1,
    "lines": [
        {"name": "w1_m12_fine", "type": "B", "u": 0.02,
         "note": "unités internes GP, u déclarée (dispersion corpus vague fine)"},
        {"name": "w1_m5_fine", "type": "B", "u": 0.02,
         "note": "unités internes GP, u déclarée (dispersion corpus vague fine)"},
    ],
    "R": [[1.0, 0.0], [0.0, 1.0]],
}
_GUM["L4_Branche_k2_RegimeFin"] = {
    "decide": "U",
    "k": 1,
    "lines": [
        {"name": "branche_k2", "type": "B", "u": 0.007567277784899113,
         "note": "propagation des arrondis gelés omega0 (0.005) et beta (0.05), P1-P2"},
        {"name": "w2_m8_fine", "type": "B", "u": 0.02,
         "note": "unités internes GP, u de lecture déclarée (addendum)"},
    ],
    "R": [[1.0, 0.0], [0.0, 1.0]],
}
_GUM["L4_Fenetre_Branche"] = {
    "decide": "U",
    "k": 1,
    "lines": [
        {"name": "D3_pred", "type": "B", "u": 0.29689816122246504,
         "note": "propagation relative : branche k3 (0.01724) + ligne vide k3 (0.02/0.515)"},
        {"name": "D3_m8_addendum", "type": "B", "u": 0.5,
         "note": "u déclarée (pic dominant par bande FFT, dédoublement m=10 exclu)"},
    ],
    "R": [[1.0, 0.0], [0.0, 1.0]],
}
_GUM["L4_Kappa_Eff"] = {
    "decide": "U",
    "k": 1,
    "lines": [
        {"name": "kappa_eff_implicite", "type": "B", "u": 0.6283185307179586,
         "note": "propagation de u(beta)=0,05 par kappa_eff = 4 pi beta ; kappa=2pi exact (constante de protocole)"},
    ],
}
_GUM["L4_Kelvin_Gap"] = {
    "decide": "U",
    "k": 1,
    "lines": [
        {"name": "gap_obs", "type": "B", "u": 0.02,
         "note": "unités internes GP, lecture déclarée du gap universel ; kappa et k1 gelés exacts"},
    ],
}
_GUM["CORR_Stabilite_Energie"] = {
    "decide": "U",
    "k": 1,
    "lines": [
        {"name": "n_opt_E63", "type": "B", "u": 1.0,
         "note": "comptage entier de cages, pas d'interpolation publiée (déclaration)"},
        {"name": "n_min_E65", "type": "B", "u": 1.0,
         "note": "comptage entier de cages, pas d'interpolation publiée (déclaration)"},
    ],
    "R": [[1.0, 0.0], [0.0, 1.0]],
}
_GUM["CORR_Fenetre_Point"] = {
    "decide": "U",
    "k": 1,
    "lines": [
        {"name": "bord_bas_E64A", "type": "B", "u": 0.007216878364870325,
         "note": "bracket rectangulaire (0,075 ; 0,1), demi-largeur 0,0125/sqrt(3) ; kappa_E61 gelé exact par protocole"},
    ],
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
    from mvcg.archive import source_sha
    from mvcg.runner import execute

    mu_loc, extra = execute(RUNNERS[c.runner], chain=c.chain)
    extra = {**extra, "runner_sha256": source_sha(RUNNERS[c.runner])}
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


def run_registers(archive: Path | None = None) -> dict[str, Any]:
    rows = [run_contact(c) for c in CONTACTS]
    if archive is not None:
        from mvcg.archive import append_traces

        append_traces(rows, Path(archive))
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
