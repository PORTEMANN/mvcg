#!/usr/bin/env python3
"""Famille B, campagne B1 — zoom PS1MD (2026-09-14).

Locale, non publiee. DERIVE de campagne — aucun contact cree, aucun gel
touche (mots S-/S- inchanges). Suite de la campagne 9 : PS1MD est le
seul offset positif significatif (+0,028 mag, 2 sigma), uniforme en z.
20 LC PS1MD dans la selection HF (sur 269 au total) : la structure
interne est explorale.

PROTOCOLE DECLARE :
1. Reproduire l'offset PS1MD HF de la campagne 9 (mu - mu_pred(z; H0*),
   H0* = 73,36 re-fit interne, Omega gelee 0,315, selection HF).
2. Decoupes internes des 20 LC : mediane en z, FITPROB, HOST_LOGMASS,
   x1, c — l'offset est-il porte par une moitie ?
3. Leave-one-out intra-PS1MD : 20 offsets rettes — quelques LC
   portent-elles le signal ?
4. Diagnostic HORS selection : les 249 PS1MD non-HF ont aussi un
   MU_SH0ES publie — leur offset est-il du meme signe ? (declare :
   hors selection officielle, aucun mot n'en depend).
5. Rappel LOSO campagne 9 : H0* sans PS1MD.

mu_pred est exact en forme close : mu = 5 log10(K(z)) - 5 log10(H0)
+ 25, K(z) = (1+z) chi(z) c — verifie contre mu_pred historique.
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


def K_of_z(z_arr: np.ndarray) -> np.ndarray:
    """K(z) = (1+z) chi(z) c — l'integrale ne depend pas de H0."""
    out = np.empty(len(z_arr))
    for i, z in enumerate(z_arr):
        integ = 1.0 / np.sqrt(OM * (1.0 + z * G) ** 3 + OL)
        out[i] = (1.0 + z) * (z * np.trapezoid(integ, G)) * C
    return out


def mu_of(z_arr: np.ndarray, h0: float) -> np.ndarray:
    return 5.0 * np.log10(K_of_z(z_arr)) - 5.0 * math.log10(h0) + 25.0


def mu_pred_hist(z_arr: np.ndarray, h0: float) -> np.ndarray:
    """Forme historique (campagne 9) — pour verification croisee."""
    out = np.empty(len(z_arr))
    for i, z in enumerate(z_arr):
        integ = 1.0 / np.sqrt(OM * (1.0 + z * G) ** 3 + OL)
        chi = z * np.trapezoid(integ, G)
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
        "sid": int(f[ix["IDSURVEY"]]), "z": float(f[ix["zHD"]]),
        "mu": float(f[ix["MU_SH0ES"]]), "hf": int(f[ix["USED_IN_SH0ES_HF"]]),
        "fitprob": float(f[ix["FITPROB"]]),
        "logmass": float(f[ix["HOST_LOGMASS"]]),
        "x1": float(f[ix["x1"]]), "c": float(f[ix["c"]]),
        "cid": f[ix["CID"]],
    })

# verification croisee forme close vs historique
zt = np.array([0.02, 0.07, 0.15])
assert np.allclose(mu_of(zt, 73.36), mu_pred_hist(zt, 73.36), atol=1e-12)

idx_sel = [i for i, d in enumerate(dat) if d["hf"] == 1]
z_all = np.array([dat[i]["z"] for i in idx_sel])
edges = [z_all[int(i * len(z_all) / NBINS)] for i in range(NBINS)]
edges.append(z_all[-1] + 1e-9)


def bin_obs(idx: list[int]) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
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


print("chargement STAT+SYS.cov ...")
raw = np.loadtxt(ROOT / "pantheon_STAT+SYS.cov", skiprows=1)
cov_full = raw.reshape(1701, 1701)
del raw


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


grid = np.linspace(60.0, 85.0, 501)
K_full = K_of_z(bin_obs(idx_sel)[0])


def fit_h0_fast(mu_b: np.ndarray, c_inv: np.ndarray) -> tuple[float, float]:
    mu_grid = 5.0 * np.log10(K_full[None, :]) \
        - 5.0 * np.log10(grid[:, None]) + 25.0
    r = mu_grid - mu_b[None, :]
    c2 = np.einsum("hb,bc,hc->h", r, c_inv, r)
    h = int(np.argmin(c2))
    return float(grid[h]), float(c2[h])


z_mid, mu_b, _ = bin_obs(idx_sel)
c_inv_full = np.linalg.inv(c_binned(idx_sel, _))
h0_star, chi2_full = fit_h0_fast(mu_b, c_inv_full)
print(f"refit interne : H0* = {h0_star:.3f}, chi2_min = {chi2_full:.3f} "
      f"(campagne 7/9 : 73.36 / 15.45)")

ps1 = [i for i in idx_sel if dat[i]["sid"] == 15]
print(f"\nPS1MD dans HF : {len(ps1)} LC (sur 269 au total)")


def offset_of(idx: list[int], label: str) -> None:
    z = np.array([dat[i]["z"] for i in idx])
    d = np.array([dat[i]["mu"] for i in idx]) - mu_of(z, h0_star)
    se = float(np.std(d) / math.sqrt(len(d)))
    print(f"{label:34s} n={len(idx):3d} offset={d.mean():+.4f} "
          f"SE={se:.4f} signif={d.mean() / se:+.2f} sigma")


print("\n=== 1. OFFSET PS1MD HF (reproduction campagne 9) ===")
offset_of(ps1, "PS1MD HF (20 LC)")

print("\n=== 2. DECOMPES INTERNES (medianes) ===")
for key in ("z", "fitprob", "logmass", "x1", "c"):
    vals = sorted(dat[i][key] for i in ps1)
    med = vals[len(vals) // 2]
    lo = [i for i in ps1 if dat[i][key] <= med]
    hi = [i for i in ps1 if dat[i][key] > med]
    offset_of(lo, f"  {key} <= {med:.3f}")
    offset_of(hi, f"  {key} >  {med:.3f}")

print("\n=== 3. LEAVE-ONE-OUT INTRA-PS1MD (offset sans chaque LC) ===")
resid = {i: dat[i]["mu"] - mu_of(np.array([dat[i]["z"]]), h0_star)[0]
         for i in ps1}
base = float(np.mean([resid[i] for i in ps1]))
print(f"offset complet : {base:+.4f}")
for i in sorted(ps1, key=lambda k: -abs(resid[k]))[:8]:
    rest = [resid[k] for k in ps1 if k != i]
    print(f"  sans {dat[i]['cid']:10s} (resid {resid[i]:+.4f}) "
          f"-> offset {np.mean(rest):+.4f}")

print("\n=== 4. DIAGNOSTIC HORS SELECTION (249 PS1MD non-HF) ===")
ps1_x = [i for i, d in enumerate(dat) if d["sid"] == 15 and d["hf"] == 0]
offset_of(ps1_x, "PS1MD hors HF (249 LC)")
offset_of(ps1 + ps1_x, "PS1MD toutes (269 LC)")

print("\n=== 5. RAPPEL LOSO (campagne 9) : H0* sans PS1MD ===")
idx_m = [i for i in idx_sel if dat[i]["sid"] != 15]
z_m, mu_m, a_m = bin_obs(idx_m)
h0_m, _ = fit_h0_fast(mu_m, np.linalg.inv(c_binned(idx_m, a_m)))
print(f"H0* sans PS1MD : {h0_m:.3f} (complet : {h0_star:.3f})")

print("\nCAMPAGNE B1 TERMINEE — derive de campagne, aucun gel touche")
