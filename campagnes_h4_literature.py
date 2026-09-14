#!/usr/bin/env python3
"""Campagne 4 — frontière du levier H0 sur les cartes LITERATURE.

Locale, non publiée (2026-09-13 soir). Pendant exact de la campagne 3
(DEMO). Levier : H0 de la courbe prédite H(z) — jamais les bins,
jamais θ = 0,02756, jamais les Ω gelés. Frontières par bisection.

ESTIMATION PRÉ-CAMPAGNE (honnête, écrite avant le run) :
- les deux cartes sont des miroirs exacts : la VARIANCE des résidus
  est identique ; seul le décalage moyen diffère (+0,1745 mag) ;
- la carte Planck pose sa courbe à l'ancrage (H0 = 67,4) et obtient
  δ = 0,0695 : le bruit réalisé σ_var ≈ 0,065-0,070 y domine déjà ;
- or 2θ = 0,05512 < σ_var attendu -> S- attendu SUR TOUT LE BALAYAGE,
  aucune fenêtre P/S+ accessible au levier H0 seul. Suspense borné :
  σ_var réalisé vs 2θ. Si σ_var < 2θ, une fenêtre P étroite existerait
  autour de l'ancrage — le balayage tranche.
- H0* (minimum du rms) attendu ≈ l'ancrage, à ±0,5 (décalage de
  convention δ_conv entre les 8 bins et le diagramme complet).
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))

from mvcg.tables import load_table  # noqa: E402

OM, OL, C = 0.315, 0.685, 299792.458
THETA = 0.02756


def mot(delta: float) -> str:
    if delta < THETA:
        return "S+"
    if delta < 2.0 * THETA:
        return "P"
    return "S-"


def rms(t: dict, h0: float) -> float:
    p = t["params"]
    res = []
    for z, mu_obs in t["bins"]:
        g = np.linspace(1e-8, z, 2000)
        chi = np.trapezoid(1.0 / np.sqrt(OM * (1.0 + g) ** 3 + OL), g)
        dl = (1.0 + z) * chi * C / h0
        res.append((5.0 * math.log10(dl) + 25.0 - mu_obs) ** 2)
    return float(math.sqrt(sum(res) / len(res)))


def frontiere(f, a: float, b: float, target: float) -> float | None:
    fa, fb = f(a), f(b)
    if (fa - target) * (fb - target) > 0:
        return None
    for _ in range(80):
        m = 0.5 * (a + b)
        fm = f(m)
        if abs(fm - target) < 1e-15:
            return m
        if (fa - target) * (fm - target) < 0:
            b, fb = m, fm
        else:
            a, fa = m, fm
    return 0.5 * (a + b)


for nom, ancrage in (("Planck", 67.4), ("SH0ES", 73.04)):
    t = load_table(f"hz_sne_LOWZ-LITERATURE-{nom}.json")
    print("=" * 66)
    print(f"CARTE {nom} (ancrage {ancrage}) — theta = {THETA}, "
          f"2*theta = {2 * THETA:.5f}")
    print(f"{'H0 courbe':>9} {'rms':>9} {'rms/2theta':>10}  mot")
    for h0v in (60.0, 63.0, 65.0, 66.0, 67.4, 68.5, 70.0, 71.5,
                73.04, 74.5, 76.0, 78.0, 80.0, 83.0):
        r = rms(t, h0v)
        print(f"{h0v:9.2f} {r:9.5f} {r / (2 * THETA):10.3f}  {mot(r)}")

    grid = np.linspace(60.0, 85.0, 2501)
    vals = [(h, rms(t, h)) for h in grid]
    h_star, r_min = min(vals, key=lambda x: x[1])
    print(f"\nminimum : H0* = {h_star:.3f}, rms_min = {r_min:.5f} mag "
          f"({r_min / THETA:.2f} theta -> mot {mot(r_min)})")
    print(f"vs ancrage : decalage {h_star - ancrage:+.3f} km/s/Mpc")

    fg = frontiere(lambda h: rms(t, h), 60.0, h_star, 2 * THETA)
    fd = frontiere(lambda h: rms(t, h), h_star, 85.0, 2 * THETA)
    if fg is None and fd is None:
        print("frontiere S-/P : AUCUNE — le mot reste S- sur tout le "
              "balayage (sigma_var > 2*theta)")
    else:
        print(f"frontiere S-/P : H0 <= {fg:.3f} / H0 >= {fd:.3f}")
    fs = frontiere(lambda h: rms(t, h), 60.0, h_star, THETA)
    if fs is None:
        print("frontiere P/S+ : AUCUNE — rms_min > theta, le S+ est "
              "inaccessible au levier H0 seul")
    else:
        print(f"frontiere P/S+ : {fs:.3f}")

    # decomposition honnete : decalage moyen vs dispersion autour du min
    residus = []
    for z, mu_obs in t["bins"]:
        g = np.linspace(1e-8, z, 2000)
        chi = np.trapezoid(1.0 / np.sqrt(OM * (1.0 + g) ** 3 + OL), g)
        dl = (1.0 + z) * chi * C / h_star
        residus.append(5.0 * math.log10(dl) + 25.0 - mu_obs)
    residus = np.array(residus)
    print(f"decomposition au minimum : decalage moyen = "
          f"{np.mean(residus):+.5f} mag, sigma_var = "
          f"{np.std(residus, ddof=1):.5f} mag")
    print(f"verif miroir : rms(courbe a l'ancrage {ancrage}) = "
          f"{rms(t, ancrage):.5f}")

print("=" * 66)
print("CAMPAGNE 4 TERMINEE — aucun gel modifie, mots toujours figes")
