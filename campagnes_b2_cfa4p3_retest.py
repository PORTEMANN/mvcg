#!/usr/bin/env python3
"""Famille B, campagne B2 — retest de la paire CFA4p3 (2026-09-14).

Locale, non publiee. DERIVE de campagne — aucun contact cree, aucun gel
touche. Suite de la campagne 9 : la paire CFA4p3 pesait +0,084 mag a
n = 2 (SE non interpretable). Les donnees locales montrent que CFA4p3
compte 12 LC au total mais seulement 2 dans la selection HF : 2010ag
(FITPROB = 2,3e-12 — ajustement de courbe de lumiere pathologique) et
2010dt (FITPROB = 0,086 — marginal). Hypothese declaree : l'offset de
la paire est porte par 2010ag.

PROTOCOLE DECLARE :
1. Tableau des 12 LC CFA4p3 : z, statut HF, FITPROB, erreur diag,
   residu individuel mu - mu_pred(z; H0*), H0* = 73,36 re-fit interne.
2. Decomposition de l'offset HF : 2010ag seul, 2010dt seul, paire.
3. Offset des 10 LC non-HF et des 12 (DIAGNOSTIC HORS SELECTION —
   declare, aucun mot n'en depend).
4. Lecture : le +0,084 mag de la campagne 9 tient-il en un LC dont le
   FITPROB est 2,3e-12 ?
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
H0_STAR = 73.36  # campagnes 7/8/9 : meilleur fit donnees, Omega gelee


def K_of_z(z_arr: np.ndarray) -> np.ndarray:
    out = np.empty(len(z_arr))
    for i, z in enumerate(z_arr):
        integ = 1.0 / np.sqrt(OM * (1.0 + z * G) ** 3 + OL)
        out[i] = (1.0 + z) * (z * np.trapezoid(integ, G)) * C
    return out


def mu_of(z_arr: np.ndarray, h0: float) -> np.ndarray:
    return 5.0 * np.log10(K_of_z(z_arr)) - 5.0 * math.log10(h0) + 25.0


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
        "embc": float(f[ix["m_b_corr_err_DIAG"]]),
        "cid": f[ix["CID"]],
    })

cfa = [i for i, d in enumerate(dat) if d["sid"] == 66]
print(f"CFA4p3 : {len(cfa)} LC au total, "
      f"{sum(dat[i]['hf'] for i in cfa)} dans la selection HF\n")
print(f"{'CID':10s} {'z':>7s} {'HF':>3s} {'FITPROB':>10s} {'e_mbc':>6s} "
      f"{'residu':>8s}")
res = {}
for i in sorted(cfa, key=lambda k: dat[k]["z"]):
    d = dat[i]
    r = d["mu"] - mu_of(np.array([d["z"]]), H0_STAR)[0]
    res[i] = r
    print(f"{d['cid']:10s} {d['z']:7.4f} {d['hf']:3d} {d['fitprob']:10.3g} "
          f"{d['embc']:6.3f} {r:+8.4f}")

hf = [i for i in cfa if dat[i]["hf"] == 1]
nohf = [i for i in cfa if dat[i]["hf"] == 0]


def offset(idx: list[int], label: str) -> None:
    d = np.array([res[i] for i in idx])
    se = float(np.std(d) / math.sqrt(len(d)))
    print(f"{label:36s} n={len(idx):2d} offset={d.mean():+.4f} "
          f"SE={se:.4f}")


print("\n=== 1. DECOMPOSITION DE LA PAIRE HF ===")
offset(hf, "paire HF (campagne 9 : +0,084)")
for i in hf:
    offset([i], f"  {dat[i]['cid']} seul (FITPROB {dat[i]['fitprob']:.2g})")

print("\n=== 2. DIAGNOSTIC HORS SELECTION (10 LC non-HF) ===")
offset(nohf, "10 LC non-HF")
offset(cfa, "12 LC toutes")

print("\n=== 3. LECTURE ===")
ag = [i for i in hf if dat[i]['cid'] == '2010ag'][0]
dt = [i for i in hf if dat[i]['cid'] == '2010dt'][0]
print(f"2010ag residu {res[ag]:+.4f} (FITPROB 2,3e-12) ; "
      f"2010dt residu {res[dt]:+.4f} (FITPROB 0,086)")
print(f"la paire = moyenne : {(res[ag] + res[dt]) / 2:+.4f}")
print("hypothese verifiee si 2010ag seul ~= offset de la paire")

print("\nCAMPAGNE B2 TERMINEE — derive de campagne, aucun gel touche")
