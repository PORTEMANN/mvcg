#!/usr/bin/env python3
"""Campagne 8 — fit conjoint (H0, Omega_m) : separation dette de forme
vs exces de dispersion, et test des verdicts gelés contre un
adversaire 2-parametres.

Locale, non publiee (2026-09-14). DERIVE de campagne — aucun contact
cree, aucun gel touche (mots S-/S- inchanges). Suite de la campagne 7.

PROTOCOLE DECLARE — deux analyses, toutes deux derivees, jamais cote
gel des contacts :
A. SEPARATION (cote donnees) : rebinning equipopule a 8 bins sur la
   selection officielle (regle de la doctrine), observable = MU_SH0ES
   moyen par bin, covariance = STAT+SYS binnee (meme construction que
   la campagne 7). Fit a 2 parametres (H0, Omega_m) de la forme
   LCDM a courbure nulle (Omega_Lambda = 1 - Omega_m).
   ndof = 8 - 2 = 6. Comparaison au fit a H0 seul (Omega gelee
   0,315) de la campagne 7 : la chute de chi2 mesure la DETTE DE
   FORME des Omega gelées ; le chi2/ndof residuel mesure l'EXCES DE
   DISPERSION reel.
B. ROBUSTESSE DES VERDICTS (cote cartes gelees) : grille C4-C6 a
   8 bins, les deux cartes, covariance C6 (selection 591, dedup
   e-min — bruit de reference de la campagne 6, choix conservateur
   pour le test). Fit (H0, Omega_m) libre : un adversaire a
   2 parametres peut-il rattraper ce que le gel S-/S- a condamne ?
   chi2_min, meilleur couple, et chi2 de l'ancre officielle pour
   comparaison. ndof = 6. Les contacts restent figes quoi qu'il
   arrive — c'est un test de leur marge, pas une remise en cause.
"""
from __future__ import annotations

import math
import re
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))
from mvcg.tables import load_table  # noqa: E402

C = 299792.458
NBINS = 8


def mu_pred_arr(z: np.ndarray, h0: np.ndarray, om: float) -> np.ndarray:
    """mu(z) LCDM courbure nulle ; h0 vecteur, om scalaire."""
    u = np.linspace(1e-8, 1, 800)
    chi = np.empty(len(z))
    for i, zi in enumerate(z):
        integrand = 1.0 / np.sqrt(om * (1.0 + zi * u) ** 3 + (1.0 - om))
        chi[i] = zi * np.trapezoid(integrand, u)
    logterm = np.log10((1.0 + z) * chi * C)
    return 5.0 * (logterm[:, None] - np.log10(h0)[None, :]) + 25.0


def fit2d(z: np.ndarray, mu: np.ndarray, c_inv: np.ndarray,
          h0_grid: np.ndarray, om_grid: np.ndarray):
    """chi2 sur la grille (om x h0), vectorise."""
    chi2_map = np.empty((len(om_grid), len(h0_grid)))
    for a, om in enumerate(om_grid):
        mu_a = mu_pred_arr(z, h0_grid, om)          # (nbins, nh0)
        r = mu_a - mu[:, None]
        chi2_map[a] = np.einsum("ik,jk,ij->k", r, r, c_inv)
    a_min, h_min = np.unravel_index(np.argmin(chi2_map), chi2_map.shape)
    return (float(om_grid[a_min]), float(h0_grid[h_min]),
            float(chi2_map[a_min, h_min]), chi2_map)


# --- chargement .dat officiel ---
lines = (ROOT / "pantheon_ref.dat").read_text().splitlines()
hdr = lines[0].split()
ix = {h: i for i, h in enumerate(hdr)}
dat = []
for ln in lines[1:]:
    f = ln.split()
    dat.append({
        "cid": f[ix["CID"]],
        "z": float(f[ix["zHD"]]),
        "e_diag": float(f[ix["m_b_corr_err_DIAG"]]),
        "mu_sh0es": float(f[ix["MU_SH0ES"]]),
        "calib": int(f[ix["IS_CALIBRATOR"]]),
        "hf": int(f[ix["USED_IN_SH0ES_HF"]]),
    })
print(f".dat officiel : {len(dat)} light curves")

print("chargement STAT+SYS.cov ...")
raw = np.loadtxt(ROOT / "pantheon_STAT+SYS.cov", skiprows=1)
cov_full = raw.reshape(1701, 1701)
del raw


def agregate(idx: list[int], assign_of: dict[int, int],
             bins: list[int]) -> np.ndarray:
    """C_bins par moyenne non ponderee, restreinte a `bins`."""
    idx_arr = np.array(idx)
    sub = cov_full[np.ix_(idx_arr, idx_arr)]
    nb = len(bins)
    c_bins = np.zeros((nb, nb))
    cnt = np.zeros((nb, nb))
    pos = np.array([bins.index(assign_of[i]) for i in idx])
    for a in range(len(idx_arr)):
        for bp in range(len(idx_arr)):
            c_bins[pos[a], pos[bp]] += sub[a, bp]
            cnt[pos[a], pos[bp]] += 1
    return c_bins / cnt


h0_grid = np.linspace(60.0, 85.0, 501)
om_grid = np.linspace(0.02, 0.65, 127)

# ================= ANALYSE A : separation (cote donnees) ================
idx_sel = [i for i, d in enumerate(dat) if d["hf"] == 1]
z_sel = np.array([dat[i]["z"] for i in idx_sel])
edges_o = [z_sel[int(i * len(z_sel) / NBINS)] for i in range(NBINS)]
edges_o.append(z_sel[-1] + 1e-9)
assign_o = {}
for i in idx_sel:
    for b in range(NBINS):
        if edges_o[b] <= dat[i]["z"] < edges_o[b + 1]:
            assign_o[i] = b
            break
mu_o = np.array([float(np.mean([dat[i]["mu_sh0es"] for i in idx_sel
                                if assign_o[i] == b]))
                 for b in range(NBINS)])
z_mid = np.array([float(np.mean([dat[i]["z"] for i in idx_sel
                                 if assign_o[i] == b]))
                  for b in range(NBINS)])
c_a = agregate(idx_sel, assign_o, list(range(NBINS)))
c_inv_a = np.linalg.inv(c_a)

om_s, h0_s, cmin_a, chi2_map_a = fit2d(z_mid, mu_o, c_inv_a,
                                       h0_grid, om_grid)
print("\n=== A. SEPARATION (cote donnees, rebin officiel 8 bins, "
      "STAT+SYS) ===")
print(f"fit 2 parametres : H0* = {h0_s:.3f}, Omega_m* = {om_s:.4f}")
print(f"chi2_min = {cmin_a:.3f}, ndof = 6 -> chi2/ndof = "
      f"{cmin_a / 6:.3f}")
i_om = int(np.argmin(np.abs(om_grid - 0.315)))
chi2_gel = chi2_map_a[i_om]
h0_f = float(h0_grid[int(np.argmin(chi2_gel))])
print(f"reference Omega gelee 0.315 : H0* = {h0_f:.3f}, "
      f"chi2_min = {chi2_gel.min():.3f} (campagne 7 : 73.36 / 15.45)")
print(f"chute de chi2 en libérant Omega_m : "
      f"{chi2_gel.min() - cmin_a:.3f} pour 1 parametre ajoute")
for nsig, dchi2 in ((1, 2.30), (2, 6.18)):
    region = chi2_map_a <= cmin_a + dchi2
    om_vals = om_grid[region.any(axis=1)]
    h0_vals = h0_grid[region.any(axis=0)]
    print(f"contour {nsig}sigma : Omega_m in [{om_vals.min():.3f}, "
          f"{om_vals.max():.3f}], H0 in [{h0_vals.min():.2f}, "
          f"{h0_vals.max():.2f}]")

# ================= ANALYSE B : robustesse des verdicts ==================
def norm(n: str) -> str:
    return re.sub(r"^(sn|asassn-|ps1-|atlas)", "", n.lower().strip())


# selection C6 (dedup e-min, fenetre [0.01, 0.15), non calibrateurs)
best: dict[str, int] = {}
for i, d in enumerate(dat):
    if 0.01 <= d["z"] < 0.15 and d["calib"] == 0:
        k = norm(d["cid"])
        if k not in best or d["e_diag"] < dat[best[k]]["e_diag"]:
            best[k] = i
sel_c6 = sorted(best.values())
sel_z = sorted(dat[i]["z"] for i in sel_c6)
edges = [sel_z[int(i * len(sel_z) / NBINS)] for i in range(NBINS)]
edges.append(sel_z[-1] + 1e-9)
assign_c6 = {}
for i in sel_c6:
    for b in range(NBINS):
        if edges[b] <= dat[i]["z"] < edges[b + 1]:
            assign_c6[i] = b
            break
c_b = agregate(sel_c6, assign_c6, list(range(NBINS)))
c_inv_b = np.linalg.inv(c_b)

print("\n=== B. ROBUSTESSE DES VERDICTS (cote cartes gelees, grille "
      "C4-C6 8 bins, bruit C6) ===")
for nom, ancre in (("Planck", 67.4), ("SH0ES", 73.04)):
    t = load_table(f"hz_sne_LOWZ-LITERATURE-{nom}.json")
    z_g = np.array([bb[0] for bb in t["bins"]])
    mu_g = np.array([bb[1] for bb in t["bins"]])
    om_b, h0_b, cmin_b, chi2_map_b = fit2d(z_g, mu_g, c_inv_b,
                                           h0_grid, om_grid)
    # chi2 de l'ancre officielle (H0 gele a la fabrication, Om 0.315)
    i_a = int(np.argmin(np.abs(om_grid - 0.315)))
    i_h = int(np.argmin(np.abs(h0_grid - ancre)))
    chi2_ancre = float(chi2_map_b[i_a, i_h])
    print(f"carte {nom} : meilleur couple H0* = {h0_b:.3f}, "
          f"Omega_m* = {om_b:.4f}")
    print(f"  chi2_min = {cmin_b:.3f}, ndof = 6 -> chi2/ndof = "
          f"{cmin_b / 6:.3f}")
    print(f"  chi2(ancre {ancre}, 0.315) = {chi2_ancre:.3f} -> "
          f"delta vs min = {chi2_ancre - cmin_b:.2f}")
    for nsig, dchi2 in ((1, 2.30), (2, 6.18)):
        region = chi2_map_b <= cmin_b + dchi2
        om_vals = om_grid[region.any(axis=1)]
        h0_vals = h0_grid[region.any(axis=0)]
        print(f"  contour {nsig}sigma : Omega_m [{om_vals.min():.3f}, "
              f"{om_vals.max():.3f}], H0 [{h0_vals.min():.2f}, "
              f"{h0_vals.max():.2f}]")

print("\nCAMPAGNE 8 TERMINEE — derive de campagne, aucun gel touche")
