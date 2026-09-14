#!/usr/bin/env python3
"""Campagne 11 — test VPEC : l'exces bas-z vient-il des vitesses
particulieres residuelles ?

Locale, non publiee (2026-09-14). DERIVE de campagne — aucun contact
cree, aucun gel touche (mots S-/S- inchanges). Suite de la campagne 10 :
l'excès de dispersion est concentre sous z ~ 0.07 — le regime des
vitesses particulieres. Le .dat porte VPEC et VPECERR par SN, et zHD
est deja « with CMB and VPEC corrections » (README officiel, verifie).

DIAGNOSTIC DECLARE (niveau LC, pas de chi2 binne — simplification
declaree) :
residu  d_i = MU_SH0ES_i - mu_pred(zHD_i ; H0*)      H0* = 73.36
predicteur x_i = VPEC_i / (c * zHD_i)   [effet attendu en mag :
d = (5/ln10) * vpec/(c z) si la correction etait ABSENTE]
Pentes de reference : b = 0 correction parfaite ; b = 5/ln10 = 2.171
correction absente. Regression lineaire ponderee (w = 1/e_diag^2) +
correlation de Pearson. Sous-echantillon bas-z (z < 0.07) en focus.
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
B_NOCORR = 5.0 / math.log(10.0)


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
        "z": float(f[ix["zHD"]]),
        "mu": float(f[ix["MU_SH0ES"]]),
        "e_diag": float(f[ix["m_b_corr_err_DIAG"]]),
        "vpec": float(f[ix["VPEC"]]),
        "vpecerr": float(f[ix["VPECERR"]]),
        "hf": int(f[ix["USED_IN_SH0ES_HF"]]),
    })
idx_sel = [i for i, d in enumerate(dat) if d["hf"] == 1]
print(f"selection officielle HF : {len(idx_sel)} LC "
      f"(verifie : aucune sentinelle VPEC, toutes valeurs reelles "
      f"[-447, +max] km/s, VPECERR = 250 km/s plat)")

H0_STAR = 73.36  # fit complet cote donnees, campagnes 7-10 (reproduit ici)

d = np.array([dat[i]["mu"] - mu_pred(np.array([dat[i]["z"]]), H0_STAR)[0]
              for i in idx_sel])
x = np.array([dat[i]["vpec"] / (C * dat[i]["z"]) for i in idx_sel])
z = np.array([dat[i]["z"] for i in idx_sel])
w = np.array([1.0 / dat[i]["e_diag"] ** 2 for i in idx_sel])
print(f"|VPEC| : mediane {np.median(np.abs(x)):.4f}, "
      f"max {np.max(np.abs(x)):.4f} mag-equivalent")
print(f"residus d : rms {np.sqrt(np.mean(d ** 2)):.4f} mag")


def regression(mask: np.ndarray, label: str):
    dd, xx, ww = d[mask], x[mask], w[mask]
    n = len(dd)
    # moindres carres ponderes classiques, variance residuelle reechelonnee
    S = ww.sum()
    xm = (ww * xx).sum() / S
    dm = (ww * dd).sum() / S
    Sxx = (ww * (xx - xm) ** 2).sum()
    Sxd = (ww * (xx - xm) * (dd - dm)).sum()
    b = Sxd / Sxx
    a = dm - b * xm
    chi2r = (ww * (dd - a - b * xx) ** 2).sum() / (n - 2)
    se_b = math.sqrt(chi2r / Sxx)
    se_a = math.sqrt(chi2r * (1.0 / S + xm ** 2 / Sxx))
    r = Sxd / math.sqrt(Sxx * (ww * (dd - dm) ** 2).sum())
    t = b / se_b if se_b > 0 else float("nan")
    print(f"[{label}] n = {n}")
    print(f"  pente b = {b:+.4f} +/- {se_b:.4f} mag par unite x "
          f"(refs : 0 correction parfaite, {B_NOCORR:.3f} absente)")
    print(f"  offset a = {a:+.4f} +/- {se_a:.4f} mag, "
          f"r (Pearson pondere) = {r:+.3f}")
    print(f"  b / SE = {t:+.2f} — correction parfaite a "
          f"{abs(b) / se_b:.2f} sigma")
    return b, se_b, r


print("\n=== plein echantillon HF ===")
regression(np.ones(len(d), dtype=bool), "tout-z")
print("\n=== bas-z (z < 0.07) — zone de l'exces ===")
regression(z < 0.07, "bas-z 0.07")
print("\n=== tres bas-z (z < 0.0372, mediane C10) ===")
regression(z < 0.0372, "tres bas-z")
print("\n=== haut-z (z >= 0.07) — controle ===")
regression(z >= 0.07, "haut-z 0.07")

print("\nCAMPAGNE 11 TERMINEE — derive de campagne, aucun gel touche")
