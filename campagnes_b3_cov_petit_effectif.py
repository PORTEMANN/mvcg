#!/usr/bin/env python3
"""Famille B, campagne B3 — covariance a petit effectif : le haut-z
blanchit-il par surestimation de covariance ? (2026-09-14)

Locale, non publiee. DERIVE de campagne — aucun contact cree, aucun gel
touche. Suite de la campagne 10 : le split fixe z = 0,07 donnait
chi2/ndof = 0,45 (haut-z) vs 0,92 (bas-z) — le haut-z serait SOUS-
dispersé face a la covariance. Deux explications candidates :
  (a) la covariance binee surestime la dispersion a petit effectif
      (moyenne de paires de covariance sur peu de LC) ;
  (b) fluctuation / biais de fit (H0* ajuste sur les memes donnees).

PROTOCOLE DECLARE :
1. Sous-echantillon HF z >= 0,07 (campagne 10), rebinning equipopule
   a 8 bins, covariance STAT+SYS binee, fit H0 seul (Omega gelee) —
   reproduction du chi2/ndof observe.
2. Bootstrap parametrique : 2000 pseudo-jeux tires de
   N(mu_pred(z; H0*_haut), C_binned) ; re-fit H0 sur chaque tirage ;
   distribution du chi2_min/ndof sous le modele. Si le modele est
   juste, le chi2 observe doit etre une realisation ordinaire de cette
   distribution ; une p-value basse soutient (a).
3. Rappel honnete : le bootstrap teste la calibration INTERNE
   (modele + covariance figes) ; il ne peut pas dire si la covariance
   PUBLIEE est juste, seulement si l'ecart observe est compatible
   avec elle.

mu_pred exact en forme close (B1) : mu = 5 log10(K(z)) - 5 log10(H0)
+ 25 — le bootstrap 2000 x fit grille est donc immediat.
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
G = np.linspace(1e-8, 1, 800)
SEED = 20260914  # gel de campagne


def K_of_z(z_arr: np.ndarray) -> np.ndarray:
    out = np.empty(len(z_arr))
    for i, z in enumerate(z_arr):
        integ = 1.0 / np.sqrt(OM * (1.0 + z * G) ** 3 + OL)
        out[i] = (1.0 + z) * (z * np.trapezoid(integ, G)) * C
    return out


lines = (ROOT / "pantheon_ref.dat").read_text().splitlines()
hdr = lines[0].split()
ix = {h: i for i, h in enumerate(hdr)}
dat = []
for ln in lines[1:]:
    f = ln.split()
    dat.append({
        "sid": int(f[ix["IDSURVEY"]]), "z": float(f[ix["zHD"]]),
        "mu": float(f[ix["MU_SH0ES"]]), "hf": int(f[ix["USED_IN_SH0ES_HF"]]),
    })

idx_sel = [i for i, d in enumerate(dat) if d["hf"] == 1]
idx_haut = [i for i in idx_sel if dat[i]["z"] >= 0.07]
print(f"selection HF : {len(idx_sel)} LC ; haut-z (z >= 0,07) : "
      f"{len(idx_haut)} LC")

zh = np.array([dat[i]["z"] for i in idx_haut])
edges = [zh[int(i * len(zh) / NBINS)] for i in range(NBINS)]
edges.append(zh[-1] + 1e-9)
assign = np.empty(len(idx_haut), dtype=int)
for k, i in enumerate(idx_haut):
    for b in range(NBINS):
        if edges[b] <= dat[i]["z"] < edges[b + 1]:
            assign[k] = b
            break
z_mid = np.array([np.mean([dat[i]["z"] for k, i in enumerate(idx_haut)
                           if assign[k] == b]) for b in range(NBINS)])
mu_b = np.array([np.mean([dat[i]["mu"] for k, i in enumerate(idx_haut)
                          if assign[k] == b]) for b in range(NBINS)])
print("z_moyens des bins :", np.round(z_mid, 4))

print("chargement STAT+SYS.cov ...")
raw = np.loadtxt(ROOT / "pantheon_STAT+SYS.cov", skiprows=1)
cov_full = raw.reshape(1701, 1701)
del raw

idx_arr = np.array(idx_haut)
sub = cov_full[np.ix_(idx_arr, idx_arr)]
c_bins = np.zeros((NBINS, NBINS))
cnt = np.zeros((NBINS, NBINS))
for a in range(len(idx_arr)):
    for bp in range(len(idx_arr)):
        c_bins[assign[a], assign[bp]] += sub[a, bp]
        cnt[assign[a], assign[bp]] += 1
c_bins /= cnt
c_inv = np.linalg.inv(c_bins)

grid = np.linspace(60.0, 85.0, 2001)
K_h = K_of_z(z_mid)
mu_grid = 5.0 * np.log10(K_h[None, :]) \
    - 5.0 * np.log10(grid[:, None]) + 25.0


def fit_c2(mu_obs: np.ndarray) -> tuple[float, float]:
    r = mu_grid - mu_obs[None, :]
    c2 = np.einsum("hb,bc,hc->h", r, c_inv, r)
    h = int(np.argmin(c2))
    return float(grid[h]), float(c2[h])


h0_fit, c2_obs = fit_c2(mu_b)
ndof = NBINS - 1
print(f"\n=== 1. OBSERVE (reproduction campagne 10) ===")
print(f"H0* haut-z = {h0_fit:.3f} ; chi2 = {c2_obs:.3f} ; "
      f"chi2/ndof = {c2_obs / ndof:.3f} (campagne 10 : 0,45)")

print("\n=== 2. BOOTSTRAP PARAMETRIQUE (2000 tirages) ===")
rng = np.random.default_rng(SEED)
mu_model = mu_grid[int(np.argmin(np.abs(grid - h0_fit)))].copy()
L = np.linalg.cholesky(c_bins)
c2_boot = np.empty(2000)
h0_boot = np.empty(2000)
for s in range(2000):
    mu_s = mu_model + L @ rng.standard_normal(NBINS)
    h0_boot[s], c2_boot[s] = fit_c2(mu_s)
c2_boot /= ndof
p_obs = float(np.mean(c2_boot <= c2_obs / ndof))
print(f"E[chi2/ndof] sous le modele     : {c2_boot.mean():.3f} "
      f"(attendu ~ (ndof-1)/ndof = {(ndof - 1) / ndof:.3f} — biais de fit)")
print(f"ecart-type du chi2/ndof         : {c2_boot.std():.3f}")
print(f"quantiles 5% / 50% / 95%        : "
      f"{np.quantile(c2_boot, 0.05):.3f} / {np.quantile(c2_boot, 0.5):.3f}"
      f" / {np.quantile(c2_boot, 0.95):.3f}")
print(f"p(chi2/ndof <= observe = {c2_obs / ndof:.3f}) : {p_obs:.3f}")
print(f"E[H0* bootstrap] = {h0_boot.mean():.3f} "
      f"(decentrement attendu : le vrai H0 du tirage est {h0_fit:.3f})")

print("\n=== 3. LECTURE ===")
if p_obs < 0.05:
    print(f"p = {p_obs:.3f} < 5% : le chi2 observe est ANORMALEMENT BAS "
          "sous le modele covariance publiee -> soutient (a) : covariance "
          "surestimée a petit effectif OU erreurs publiees surestimées "
          "haut-z.")
else:
    print(f"p = {p_obs:.3f} : le chi2 observe est compatible avec le "
          "modele + covariance -> pas de preuve de surestimation ; "
          "l'ecart est une fluctuation (ndof faible).")

print("\nCAMPAGNE B3 TERMINEE — derive de campagne, aucun gel touche")
