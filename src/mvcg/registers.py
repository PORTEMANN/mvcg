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
    "karplus_helix": _karplus_helix,
    "karplus_sheet": _karplus_sheet,
    "ckm_row1": _ckm_row1,
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
        "CKM_Row1_Unitarity", "micro", "pred", "1", "1", "abs", 0.0007,
        1.0, "somme<-autres-entrees", "—",
        "|Vud|^2+|Vus|^2+|Vub|^2 = 1 (unitarite de la 1re ligne)",
        "contact ouvert CKM : somme declaree PDG, decide=U k=2 ; suspense reel δ/U=1.14 au cheveu du S+",
        "ckm_row1",
        "ouverte", None, "CKM",
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
