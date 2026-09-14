#!/usr/bin/env python3
"""Campagne 9 — chasse a l'exces : decomposition par survey.

Locale, non publiee (2026-09-14). DERIVE de campagne — aucun contact
cree, aucun gel touche (mots S-/S- inchanges). Suite de la campagne 8 :
l'excès de dispersion est reel (dette de forme negligible) — qui le
porte ?

Correspondance IDSURVEY officielle (README 4_DISTANCES_AND_COVAR du
depot PantheonPlusSH0ES/DataRelease, verifiee) :
  1 SDSS, 4 SNLS, 5 CSP, 10 DES, 15 PS1MD, 18 CNIa0.02,
  50 LOWZ/JRK07, 51 LOSS1, 56 SOUSA, 57 LOSS2, 61 CFA1, 62 CFA2,
  63 CFA3S, 64 CFA3K, 65 CFA4p2, 66 CFA4p3, 100 HST, 101 SNAP,
  106 CANDELS, 150 FOUND.

PROTOCOLE DECLARE :
1. OFFSETS PAR SURVEY : selection officielle HF (277 LC),
   rebin equipopule 8 bins (regle de la doctrine), H0* = 73.36
   (meilleur fit cote donnees, Omega gelee — campagne 7/8).
   Pour chaque survey : ecart moyen MU_SH0ES - mu_pred(z_i; H0*),
   erreur standard, significativite. H0* est re-fit dans ce script
   (grille identique) — doit reproduire 15.45.
2. JACKKNIFE LOSO (leave-one-survey-out) : pour chaque survey s,
   retrait de ses LC, memes frontieres de bins (comparabilite),
   moyennes de bins et covariance STAT+SYS reconstruites sur le
   reste, re-fit H0 (Omega gelee). Influence : delta_chi2 =
   chi2_min(complet) - chi2_min(-s) > 0  =>  le survey tirait
   Loin du meilleur ajustement (porteur d'exces). Ce sont des
   influences jackknife, PAS une decomposition additive de chi2
   (les bins sont correles) — declare.
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

SURVEYS = {
    1: "SDSS", 4: "SNLS", 5: "CSP", 10: "DES", 15: "PS1MD",
    18: "CNIa0.02", 50: "LOWZ/JRK07", 51: "LOSS1", 56: "SOUSA",
    57: "LOSS2", 61: "CFA1", 62: "CFA2", 63: "CFA3S", 64: "CFA3K",
    65: "CFA4p2", 66: "CFA4p3", 100: "HST", 101: "SNAP",
    106: "CANDELS", 150: "FOUND",
}


def mu_pred(z_arr: np.ndarray, h0: float) -> np.ndarray:
    g = np.linspace(1e-8, 1, 800)
    out = np.empty(len(z_arr))
    for i, z in enumerate(z_arr):
        integrand = 1.0 / np.sqrt(OM * (1.0 + z * g) ** 3 + OL)
        chi = z * np.trapezoid(integrand, g)
        out[i] = 5.0 * math.log10((1.0 + z) * chi * C / h0) + 25.0
    return out


# --- chargement .dat ---
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

# frontieres equipopulees sur la selection complete (regle doctrine)
z_all = np.array([dat[i]["z"] for i in idx_sel])
edges = [z_all[int(i * len(z_all) / NBINS)] for i in range(NBINS)]
edges.append(z_all[-1] + 1e-9)


def bin_obs(idx: list[int]) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """z_mid, mu moyen, et vecteur d'assignation par LC (classement
    dans l'ordre de idx)."""
    assign = np.empty(len(idx), dtype=int)
    for k, i in enumerate(idx):
        for b in range(NBINS):
            if edges[b] <= dat[i]["z"] < edges[b + 1]:
                assign[k] = b
                break
    z_mid = np.array([np.mean([dat[i]["z"] for k, i in enumerate(idx)
                               if assign[k] == b]) for b in range(NBINS)])
    mu_b = np.array([np.mean([dat[i]["mu"] for k, i in enumerate(idx)
                              if assign[k] == b]) for b in range(NBINS)])
    return z_mid, mu_b, assign


def c_binned(idx: list[int], assign: np.ndarray) -> np.ndarray:
    idx_arr = np.array(idx)
    sub = cov_full[np.ix_(idx_arr, idx_arr)]
    c_bins = np.zeros((NBINS, NBINS))
    cnt = np.zeros((NBINS, NBINS))
    for a in range(len(idx_arr)):
        for bp in range(len(idx_arr)):
            c_bins[assign[a], assign[bp]] += sub[a, bp]
            cnt[assign[a], assign[bp]] += 1
    return c_bins / cnt


def fit_h0(z_mid: np.ndarray, mu_b: np.ndarray, c_inv: np.ndarray,
           grid: np.ndarray) -> tuple[float, float]:
    best, cmin = None, 1e18
    for h in grid:
        r = mu_pred(z_mid, h) - mu_b
        c2 = float(r @ c_inv @ r)
        if c2 < cmin:
            best, cmin = h, c2
    return best, cmin


grid = np.linspace(60.0, 85.0, 501)
z_mid, mu_b, assign_full = bin_obs(idx_sel)
c_inv_full = np.linalg.inv(c_binned(idx_sel, assign_full))
h0_star, chi2_full = fit_h0(z_mid, mu_b, c_inv_full, grid)
print(f"refit interne : H0* = {h0_star:.3f}, chi2_min = {chi2_full:.3f} "
      f"(campagne 7 : 73.36 / 15.45)")

# ================= 1. OFFSETS PAR SURVEY ================================
print("\n=== 1. OFFSETS PAR SURVEY (MU_SH0ES - mu_pred(z; H0*), "
      f"H0* = {h0_star:.2f}) ===")
print(f"{'survey':>10} {'n_LC':>5} {'z_min':>7} {'z_max':>7} "
      f"{'offset':>8} {'SE':>7} {'signif':>7}")
rows = []
for sid in sorted({dat[i]["sid"] for i in idx_sel},
                  key=lambda s: -sum(1 for i in idx_sel
                                     if dat[i]["sid"] == s)):
    sub_idx = [i for i in idx_sel if dat[i]["sid"] == sid]
    d = np.array([dat[i]["mu"] - mu_pred(np.array([dat[i]["z"]]),
                                         h0_star)[0] for i in sub_idx])
    off, se = float(np.mean(d)), float(np.std(d) / math.sqrt(len(d)))
    rows.append((sid, len(sub_idx), off, se))
    zs = [dat[i]["z"] for i in sub_idx]
    sig = f"{off / se:+7.2f}" if se > 0 else "     na"
    print(f"{SURVEYS[sid]:>10} {len(sub_idx):5d} {min(zs):7.4f} "
          f"{max(zs):7.4f} {off:+8.4f} {se:7.4f} {sig}")

# ================= 2. JACKKNIFE LOSO ====================================
print("\n=== 2. JACKKNIFE LOSO (delta_chi2 = chi2(complet) - "
      "chi2(sans survey)) ===")
print(f"{'survey':>10} {'n_LC':>5} {'chi2(-s)':>9} {'d_chi2':>8} "
      f"{'H0*(-s)':>8}")
results = []
for sid, n_lc, off, se in rows:
    idx_m = [i for i in idx_sel if dat[i]["sid"] != sid]
    z_m, mu_m, assign_m = bin_obs(idx_m)
    c_inv_m = np.linalg.inv(c_binned(idx_m, assign_m))
    h0_m, c2_m = fit_h0(z_m, mu_m, c_inv_m, grid)
    results.append((sid, n_lc, c2_m, chi2_full - c2_m, h0_m))
    print(f"{SURVEYS[sid]:>10} {n_lc:5d} {c2_m:9.3f} "
          f"{chi2_full - c2_m:+8.3f} {h0_m:8.3f}")
tot = sum(r[3] for r in results)
print(f"\nsomme des influences jackknife : {tot:+.3f} "
      f"(NON additive avec chi2_min = {chi2_full:.3f} — bins correles, "
      f"declare)")

print("\nCAMPAGNE 9 TERMINEE — derive de campagne, aucun gel touche")
