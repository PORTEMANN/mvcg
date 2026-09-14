#!/usr/bin/env python3
"""Campagne 10 — split d'echantillon en z : le bas-z et le haut-z
preferent-ils le meme H0 ? (micro-tension interne).

Locale, non publiee (2026-09-14). DERIVE de campagne — aucun contact
cree, aucun gel touche (mots S-/S- inchanges). Suite de la campagne 9 :
l'offset PS1MD (+2.0 sigma, s'etendant a z = 0.148) invite a tester
une derive de POSITION avec z, pas seulement de la dispersion.

PROTOCOLE DECLARE :
1. Selection officielle HF (277 LC), deux coupures :
   a. coupure a la mediane (regle equipopulee de la doctrine) ;
   b. coupure fixe z = 0.07 (physique : separe l'echantillon local
      FOUND/CSP/LOSS/CFA de l'echantillon etendu SDSS/PS1MD).
2. Chaque sous-echantillon : rebinning equipopule a 8 bins
   (regle de la doctrine), observable = MU_SH0ES moyen par bin,
   covariance STAT+SYS binee, fit H0 seul (Omega gelee 0.315),
   ndof = 7. Erreur par intervalle delta chi2 = 1 sur grille.
3. Test de coherence : chi2(fit unique, 8 bins) vs
   chi2_bas + chi2_haut (fits separes, 1 parametre de plus).
   Une amelioration marquee signalerait une incompatibilite de
   position entre les moities (derive avec z).
4. Zoom : offsets PS1MD et SDSS restreints au haut-z (z >= 0.07) —
   l'offset de la campagne 9 est-il un phenomene haut-z ?
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))

OM, OL, C = 0.315, 0.685, 299792.458
NBINS = 8


def mu_pred(z_arr: np.ndarray, h0: float) -> np.ndarray:
    g = np.linspace(1e-8, 1, 800)
    out = np.empty(len(z_arr))
    for i, z in enumerate(z_arr):
        integrand = 1.0 / np.sqrt(OM * (1.0 + z * g) ** 3 + OL)
        chi = z * np.trapezoid(integrand, g)
        out[i] = 5.0 * math.log10((1.0 + z) * chi * C / h0) + 25.0
    return out


# --- chargement ---
lines = (ROOT / "pantheon_ref.dat").read_text().splitlines()
hdr = lines[0].split()
ix = {h: i for i, h in enumerate(hdr)}
dat = []
for ln in lines[1:]:
    f = ln.split()
    dat.append({
        "sid": int(f[ix["IDSURVEY"]]),
        "z": float(f[ix["zHD"]]),
        "mu": float(f[ix["MU_SH0ES"]]),
        "hf": int(f[ix["USED_IN_SH0ES_HF"]]),
    })
idx_sel = [i for i, d in enumerate(dat) if d["hf"] == 1]
print(f"selection officielle HF : {len(idx_sel)} LC")

print("chargement STAT+SYS.cov ...")
raw = np.loadtxt(ROOT / "pantheon_STAT+SYS.cov", skiprows=1)
cov_full = raw.reshape(1701, 1701)
del raw

GRID = np.linspace(60.0, 85.0, 2501)


def analyse(idx: list[int], label: str):
    """Rebin equipopule 8 bins + fit H0. Retourne resultats."""
    z_a = np.array([dat[i]["z"] for i in idx])
    edges = [z_a[int(i * len(z_a) / NBINS)] for i in range(NBINS)]
    edges.append(z_a[-1] + 1e-9)
    assign = np.empty(len(idx), dtype=int)
    for k, i in enumerate(idx):
        for b in range(NBINS):
            if edges[b] <= dat[i]["z"] < edges[b + 1]:
                assign[k] = b
                break
    n_par_bin = [int(np.sum(assign == b)) for b in range(NBINS)]
    z_mid = np.array([np.mean([dat[i]["z"] for k, i in enumerate(idx)
                               if assign[k] == b]) for b in range(NBINS)])
    mu_b = np.array([np.mean([dat[i]["mu"] for k, i in enumerate(idx)
                              if assign[k] == b]) for b in range(NBINS)])
    idx_arr = np.array(idx)
    sub = cov_full[np.ix_(idx_arr, idx_arr)]
    c_bins = np.zeros((NBINS, NBINS))
    cnt = np.zeros((NBINS, NBINS))
    for a in range(len(idx_arr)):
        for bp in range(len(idx_arr)):
            c_bins[assign[a], assign[bp]] += sub[a, bp]
            cnt[assign[a], assign[bp]] += 1
    c_inv = np.linalg.inv(c_bins / cnt)
    chi2 = np.empty(len(GRID))
    for k, h in enumerate(GRID):
        r = mu_pred(z_mid, h) - mu_b
        chi2[k] = r @ c_inv @ r
    kmin = int(np.argmin(chi2))
    cmin = float(chi2[kmin])
    # erreur par delta chi2 = 1
    klo = kmin
    while klo > 0 and chi2[klo] < cmin + 1.0:
        klo -= 1
    khi = kmin
    while khi < len(GRID) - 1 and chi2[khi] < cmin + 1.0:
        khi += 1
    err = (GRID[khi] - GRID[klo]) / 2.0
    print(f"[{label}] n = {len(idx)}, z in [{z_a.min():.4f}, "
          f"{z_a.max():.4f}], min/bin = {min(n_par_bin)}")
    print(f"  H0* = {GRID[kmin]:.3f} +/- {err:.3f}, "
          f"chi2_min = {cmin:.3f}, chi2/ndof = {cmin / 7:.3f}")
    return float(GRID[kmin]), err, cmin


print("\n=== 1. COUPURE A LA MEDIANE (regle equipopulee) ===")
z_sel = np.array([dat[i]["z"] for i in idx_sel])
z_med = float(np.median(z_sel))
lo = [i for i in idx_sel if dat[i]["z"] < z_med]
hi = [i for i in idx_sel if dat[i]["z"] >= z_med]
print(f"medianes : z_med = {z_med:.4f} -> {len(lo)} / {len(hi)} LC")
h0_lo, e_lo, c_lo = analyse(lo, "bas-z median")
h0_hi, e_hi, c_hi = analyse(hi, "haut-z median")

print("\n=== 2. COUPURE FIXE z = 0.07 ===")
lo7 = [i for i in idx_sel if dat[i]["z"] < 0.07]
hi7 = [i for i in idx_sel if dat[i]["z"] >= 0.07]
print(f"z < 0.07 : {len(lo7)} LC | z >= 0.07 : {len(hi7)} LC")
h0_lo7, e_lo7, c_lo7 = analyse(lo7, "bas-z 0.07")
h0_hi7, e_hi7, c_hi7 = analyse(hi7, "haut-z 0.07")

print("\n=== 3. COHERENCE : fit unique vs fits separes ===")
h0_f, e_f, c_f = analyse(idx_sel, "complet")
print(f"median : chi2 sep = {c_lo + c_hi:.3f} vs unique = {c_f:.3f} "
      f"-> delta = {c_f - (c_lo + c_hi):+.3f} pour 1 parametre en moins")
print(f"z=0.07 : chi2 sep = {c_lo7 + c_hi7:.3f} vs unique = {c_f:.3f} "
      f"-> delta = {c_f - (c_lo7 + c_hi7):+.3f}")
print(f"delta H0 median : {h0_hi - h0_lo:+.3f} +/- "
      f"{math.sqrt(e_lo ** 2 + e_hi ** 2):.3f}")
print(f"delta H0 z=0.07 : {h0_hi7 - h0_lo7:+.3f} +/- "
      f"{math.sqrt(e_lo7 ** 2 + e_hi7 ** 2):.3f}")

print("\n=== 4. ZOOM HAUT-Z : offsets PS1MD / SDSS a z >= 0.07 ===")
h0_star = h0_f
for sid, nom in ((15, "PS1MD"), (1, "SDSS")):
    for zcut, lab in ((0.07, "haut-z"), (0.0, "tout-z")):
        sub_idx = [i for i in idx_sel if dat[i]["sid"] == sid
                   and dat[i]["z"] >= zcut]
        if not sub_idx:
            continue
        d = np.array([dat[i]["mu"] - mu_pred(np.array([dat[i]["z"]]),
                                             h0_star)[0]
                      for i in sub_idx])
        se = float(np.std(d) / math.sqrt(len(d)))
        print(f"  {nom} {lab} (n = {len(sub_idx)}) : "
              f"{float(np.mean(d)):+.4f} +/- {se:.4f} mag")

print("\nCAMPAGNE 10 TERMINEE — derive de campagne, aucun gel touche")
