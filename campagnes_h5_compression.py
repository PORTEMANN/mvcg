#!/usr/bin/env python3
"""Campagne 5 — sensibilite a la dette de compression : bins ponderes.

Locale, non publiee (2026-09-13 soir). DÉRIVÉ de campagne — aucun
contact cree, aucun gel touche. Les contacts restent S-/S- sur les
tables non ponderees ; ici on mesure CE QUE LA DETTE ENGAGE.

Protocole declare :
1. MEME selection que l'extraction LITERATURE : table 7 Brout 2022,
   dedoublonnage normalise (e min), fenetre zHD [0.01, 0.15),
   8 bins equipopulaires (memes frontieres de z que la campagne
   non ponderee — la geometrie des bins ne bouge pas).
2. Binning PONDERE : mu_bin = somme(w*m)/somme(w), w = 1/e_mBcorr^2 ;
   sigma_bin = 1/racine(somme(w)). Pratique standard metrologique,
   diagonale seule : la covariance C_stat/C_syst reste une dette.
3. Transposition d'ancrage IDENTIQUE (meme K_B = 28.52698, meme
   methode) : seul le binning change.
4. Balayage du levier H0 sur les deux cartes ponderees, RÈGLE DE
   PESÉE IDENTIQUE (rms des residus) : la difference mesuree est
   l'effet du binning seul.
5. theta de campagne = sigma_bin ponderee (chaque carte porte son
   propre seuil, comme la doctrine l'exige).

ESTIMATION PRÉ-CAMPAGNE (avant run) : le pondere defavorise les SNe
bruyantes (bas-z a sigma_vpec grand, PS1MD/SDSS) -> bins plus
« FOUND-like » (survey le plus coherent, MAD 0.164) -> sigma_var
pourrait diminuer et les fenetres s'elargir ; ou le N effectif
reduit fait l'inverse. Suspense reel.
"""
from __future__ import annotations

import csv
import json
import math
import re
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))
from mvcg.tables import load_table  # noqa: E402

OM, OL, C = 0.315, 0.685, 299792.458
K_B = 28.52698  # convention mesuree campagne LITERATURE (inchangee)
ZMIN, ZMAX, NBINS = 0.01, 0.15, 8
ANCHORAGES = {"SH0ES": (73.04, 1.04), "Planck": (67.4, 0.5)}


def mot(delta: float, theta: float) -> str:
    if delta < theta:
        return "S+"
    if delta < 2.0 * theta:
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


def frontiere(f, a, b, target):
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
    return 0.5 * (a, b) if False else 0.5 * (a + b)


# --- selection identique a l'extraction LITERATURE ---
rows = list(csv.DictReader(open(ROOT / "pantheon_t7.csv",
                                newline="", encoding="utf-8")))


def norm(n: str) -> str:
    return re.sub(r"^(sn|asassn-|ps1-|atlas)", "", n.lower().strip())


best: dict[str, dict] = {}
for r in rows:
    k = norm(r["Name"])
    if k not in best or float(r["e_mBcorr"]) < float(best[k]["e_mBcorr"]):
        best[k] = r
sel = [(float(r["zHD"]), float(r["mBcorr"]), float(r["e_mBcorr"]))
       for r in best.values() if ZMIN <= float(r["zHD"]) < ZMAX]
sel.sort(key=lambda t: t[0])
edges = [sel[int(i * len(sel) / NBINS)][0] for i in range(NBINS)]
edges.append(sel[-1][0] + 1e-9)

# --- bins ponderes (memes frontieres) ---
wbins = []
for bidx in range(NBINS):
    grp = [t for t in sel if edges[bidx] <= t[0] < edges[bidx + 1]]
    zz = np.array([t[0] for t in grp])
    mm = np.array([t[1] for t in grp])
    ee = np.array([t[2] for t in grp])
    w = 1.0 / ee ** 2
    mu_w = float(np.sum(w * mm) / np.sum(w))
    sig_w = float(1.0 / math.sqrt(np.sum(w)))
    wbins.append({
        "z_median": round(float(np.median(zz)), 6), "N": len(grp),
        "mBcorr_wmean": round(mu_w, 6), "sigma_bin_w": round(sig_w, 6),
        "rms_intra": round(float(np.std(mm, ddof=1)), 4),
    })
sig_theta_w = round(float(np.mean([b["sigma_bin_w"] for b in wbins])), 6)
print(f"bins pondérés : theta_w = {sig_theta_w:.5f} mag "
      f"(non pondéré : 0.02756)")
print(f"{'z_med':>8} {'N':>4} {'sig_w':>9} {'rms_intra':>9}")
for b in wbins:
    print(f"{b['z_median']:8.4f} {b['N']:4d} {b['sigma_bin_w']:9.5f} "
          f"{b['rms_intra']:9.4f}")

# --- tables pondérées (dérivés de campagne, non gelées) ---
for nom, (h0a, ua) in ANCHORAGES.items():
    dmu = 5.0 * math.log10(h0a) - K_B
    table = {
        "id": f"hz_sne_lowz_literature_{nom.lower()}_weighted",
        "vintage": "DERIVE-CAMPAGNE-5-WEIGHTED (non gele)",
        "source": "Meme extraction LITERATURE, bins ponderes "
                  "w=1/e_mBcorr^2, memes frontieres ; derive de "
                  "sensibilite, PAS une table de contact",
        "doi_or_ref": "voir hz_sne_LOWZ-LITERATURE-{nom}.json",
        "species": "supernovae Ia (Pantheon+)",
        "quantity": "module de distance binned bas-z PONDERE, "
                    f"amplitude ancree {nom}",
        "dimension": "mag",
        "packet": "1",
        "bins": [[b["z_median"], round(b["mBcorr_wmean"] - dmu, 6)]
                 for b in wbins],
        "sigma_mag": sig_theta_w,
        "params": {"Omega_m": OM, "Omega_L": OL, "c_km_s": C,
                   "H0_ancrage_km_s_Mpc": h0a,
                   "K_B_convention": K_B,
                   "transposition": "identique a la carte non ponderee",
                   "regle_bins": "8 bins equipopulaires, moyenne "
                                 "ponderee w=1/e_mBcorr^2 declaree"},
        "dettes": {"D-compression-residuelle": "pondération diagonale "
                   "seule ; covariance C_stat/C_syst toujours ignoree"},
        "sha256_note": "derive de campagne ; ne geler aucun mot dessus",
    }
    out = ROOT / "data" / "tables" / \
        f"hz_sne_LOWZ-LITERATURE-{nom}-WEIGHTED.json"
    out.write_text(json.dumps(table, indent=2, ensure_ascii=False),
                   encoding="utf-8")
    print(f"\ntable ponderee {nom} -> {out.name}")

# --- balayage comparé ---
print("\n" + "=" * 66)
for nom, ancrage in (("Planck", 67.4), ("SH0ES", 73.04)):
    tw = load_table(f"hz_sne_LOWZ-LITERATURE-{nom}-WEIGHTED.json")
    tu = load_table(f"hz_sne_LOWZ-LITERATURE-{nom}.json")
    th = float(tw["sigma_mag"])
    print(f"CARTE {nom} PONDÉRÉE — theta_w = {th:.5f}, 2*theta = "
          f"{2 * th:.5f} (non pondéré : 0.02756 / 0.05512)")
    print(f"{'H0':>8} {'rms_w':>9} {'mot_w':>5} {'rms_nw':>9} {'mot':>4}")
    for h0v in (66.0, 67.4, 68.5, 69.0, 70.0, 71.5, 73.04, 74.8,
                76.0, 78.0):
        rw = rms(tw, h0v)
        ru = rms(tu, h0v)
        print(f"{h0v:8.2f} {rw:9.5f} {mot(rw, th):>5} {ru:9.5f} "
              f"{mot(ru, 0.02756):>4}")
    grid = np.linspace(60.0, 85.0, 2501)
    hstar_w, rmin_w = min(((h, rms(tw, h)) for h in grid),
                          key=lambda x: x[1])
    hstar_u, rmin_u = min(((h, rms(tu, h)) for h in grid),
                          key=lambda x: x[1])
    fg = frontiere(lambda h: rms(tw, h), 60.0, hstar_w, 2 * th)
    fd = frontiere(lambda h: rms(tw, h), hstar_w, 85.0, 2 * th)
    residus = []
    for z, mu_obs in tw["bins"]:
        g = np.linspace(1e-8, z, 2000)
        chi = np.trapezoid(1.0 / np.sqrt(OM * (1.0 + g) ** 3 + OL), g)
        dl = (1.0 + z) * chi * C / hstar_w
        residus.append(5.0 * math.log10(dl) + 25.0 - mu_obs)
    residus = np.array(residus)
    print(f"H0* : pondéré {hstar_w:.3f} / non pondéré {hstar_u:.3f} "
          f"({hstar_w - hstar_u:+.3f})")
    print(f"rms_min : pondé {rmin_w:.5f} ({rmin_w / th:.2f} th_w) / "
          f"non pondé {rmin_u:.5f} ({rmin_u / 0.02756:.2f} th)")
    print(f"sigma_var pondéré : {np.std(residus, ddof=1):.5f} "
          f"(non pondéré : 0.04895)")
    print(f"frontières P pondérées : [{fg:.3f} ; {fd:.3f}] vs "
          f"[{frontiere(lambda h: rms(tu, h), 60.0, hstar_u, 0.05512):.3f}"
          f" ; {frontiere(lambda h: rms(tu, h), hstar_u, 85.0, 0.05512):.3f}]")
print("=" * 66)
print("CAMPAGNE 5 TERMINEE — dérivé de campagne, aucun gel touché")
