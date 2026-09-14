#!/usr/bin/env python3
"""Extraction V2 — ancrage natif MU_SH0ES (2026-09-14).

Chantier local. Méthodologie déclarée AVANT run (doctrine V2) :
1. SOURCE : fichier de release Pantheon+SH0ES (pantheon_ref.dat, 1701
   light curves), colonne MU_SH0ES PUBLIÉE (estimateur propre de la
   collaboration, ancrage Céphéides natif) — PAS de transposition
   mBcorr + K_B. La Table 7 VizieR ne porte pas MU_SH0ES : la V2 se
   construit sur le fichier de release, déclaré.
2. DÉDOUBLONNAGE : même règle déclarée que V1 (nom normalisé minuscules,
   préfixes retirés, e minimal — ici e = MU_SH0ES_ERR_DIAG).
3. FENÊTRE zHD ∈ [0,01 ; 0,15), calibrateurs exclus (z < 0,01).
4. 8 bins équipopulaires, moyenne arithmétique déclarée (dette de
   compression identique à V1, non pondérée).
5. σ_bin = sqrt(moyenne(e²)/N), e = MU_SH0ES_ERR_DIAG (propriété de la
   source) ; θ = moyenne des σ_bin, gelé AVANT le run.
6. Dettes écrites : calibration commune des bins non réduite ; la
   colonne MU_SH0ES incorpore les ajustements propres de la
   collaboration (Ω_m, nuisance) — dette de forme +0,049 mag mesurée
   campagne 7, écrite dans la doctrine.
7. Validation croisée : comparaison des bins V2 à la transposition V1
   (SH0ES) — écart attendu ~0,00-0,05 mag (conventions communes).

Deux contacts miroirs de la paire V1, sur cette table unique :
  V2_PLANCK : courbe mu_pred(z ; 67,4, Ω gelés) vs bins natifs
  V2_SH0ES  : courbe mu_pred(z ; 73,04, Ω gelés) vs bins natifs
"""

from __future__ import annotations

import json
import math
import re
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent
OM, OL, C = 0.315, 0.685, 299792.458
ZMIN, ZMAX, NBINS = 0.01, 0.15, 8
G = np.linspace(1e-8, 1, 800)


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


def _norm(n: str) -> str:
    n = n.lower().strip()
    return re.sub(r"^(sn|asassn-|ps1-|atlas)", "", n)


rows = []
for ln in lines[1:]:
    f = ln.split()
    rows.append({
        "name": f[ix["CID"]], "z": float(f[ix["zHD"]]),
        "mu": float(f[ix["MU_SH0ES"]]),
        "e": float(f[ix["MU_SH0ES_ERR_DIAG"]]),
        "hf": int(f[ix["USED_IN_SH0ES_HF"]]),
    })
print(f"release brute : {len(rows)} light curves")

best: dict[str, dict] = {}
for r in rows:
    n = _norm(r["name"])
    if n not in best or r["e"] < best[n]["e"]:
        best[n] = r
rows = list(best.values())
print(f"après dédoublonnage (règle déclarée) : {len(rows)} SNe uniques")

sel = [r for r in rows if ZMIN <= r["z"] < ZMAX]
print(f"fenêtre zHD [{ZMIN}, {ZMAX}) : {len(sel)} SNe")
sel.sort(key=lambda r: r["z"])

edges = [sel[int(i * len(sel) / NBINS)]["z"] for i in range(NBINS)]
edges.append(sel[-1]["z"] + 1e-9)

bins = []
for b in range(NBINS):
    grp = [r for r in sel if edges[b] <= r["z"] < edges[b + 1]]
    zz = np.array([r["z"] for r in grp])
    mm = np.array([r["mu"] for r in grp])
    ee = np.array([r["e"] for r in grp])
    bins.append({
        "z_mean": round(float(np.mean(zz)), 6),
        "z_range": [round(float(zz.min()), 6), round(float(zz.max()), 6)],
        "N": len(grp),
        "mu_mean": round(float(np.mean(mm)), 6),
        "sigma_bin": round(float(np.sqrt(np.mean(ee ** 2) / len(grp))), 6),
        "rms_intra": round(float(np.std(mm, ddof=1)), 4),
    })

print(f"\n{'z_mean':>8} {'N':>4} {'mu_mean':>9} {'sig_bin':>8} "
      f"{'rms_intra':>9}")
for bb in bins:
    print(f"{bb['z_mean']:8.4f} {bb['N']:4d} {bb['mu_mean']:9.4f} "
          f"{bb['sigma_bin']:8.5f} {bb['rms_intra']:9.4f}")

sig_theta = round(float(np.mean([b["sigma_bin"] for b in bins])), 6)
z_mid = np.array([b["z_mean"] for b in bins])
mu_b = np.array([b["mu_mean"] for b in bins])
for nom, h0 in (("SH0ES", 73.04), ("Planck", 67.4)):
    r = mu_of(z_mid, h0) - mu_b
    rms = float(np.sqrt(np.mean(r ** 2)))
    print(f"\nrms résidus courbe {nom} ({h0}) : {rms:.5f} mag "
          f"(offset moyen {float(np.mean(r)):+.4f}) ; θ = {sig_theta:.5f}")

# validation croisée V1 (transposition SH0ES) vs V2 (natif)
t1 = json.loads((ROOT / "data/tables/hz_sne_LOWZ-LITERATURE-SH0ES.json")
                .read_text(encoding="utf-8"))
v1 = np.array([b[1] for b in t1["bins"]])
print(f"\nVALIDATION CROISÉE V1(SH0ES transposé) vs V2(natif) : "
      f"écart moyen {float(np.mean(v1 - mu_b)):+.4f} mag, "
      f"max {float(np.max(np.abs(v1 - mu_b))):.4f}")

table = {
    "id": "hz_sne_lowz_v2_mush0es",
    "vintage": "V2-MUSH0ES-PantheonPlus-release",
    "source": "Pantheon+ SH0ES data release (pantheon_ref.dat, 1701 LC), "
              "MU_SH0ES publié (ancrage Céphéides natif, pas de "
              "transposition), SNe Ia flux Hubble zHD ∈ [0.01, 0.15), "
              "dédoublonnées (règle : nom normalisé minuscules, préfixes "
              "retirés, MU_SH0ES_ERR_DIAG minimal), calibrateurs exclus",
    "doi_or_ref": "Scolnic et al. 2022, ApJ, 938, 113 ; Riess et al. 2022 "
                  "(SH0ES) ; Brout et al. 2022, ApJ, 938, 110 (Table 7 "
                  "pour mBcorr — MU_SH0ES absent de Table 7)",
    "species": "supernovae Ia (Pantheon+, flux Hubble bas-z)",
    "quantity": "module de distance publié MU_SH0ES binné bas-z, ancrage "
                "natif SH0ES",
    "dimension": "mag",
    "packet": "1",
    "bins": [[b["z_mean"], b["mu_mean"]] for b in bins],
    "sigma_mag": sig_theta,
    "params": {
        "Omega_m": OM, "Omega_L": OL, "c_km_s": C,
        "H0_courbe_PLANCK_km_s_Mpc": 67.4,
        "H0_courbe_SH0ES_km_s_Mpc": 73.04,
        "regle_bins": "8 bins equipopulaires, moyenne arithmetique "
                      "declaree (non ponderee, dette de compression)",
        "sigma_regle": "sqrt(moyenne(e^2)/N), e = MU_SH0ES_ERR_DIAG",
        "validation_croisee_V1": "ecart moyen vs transposition SH0ES V1 "
                                 "declare ci-dessus",
        "dettes": ("calibration commune des bins non reduite ; MU_SH0ES "
                   "incorpore les ajustements propres de la collaboration "
                   "(Omega_m, nuisance) : dette de forme +0.049 mag "
                   "mesuree campagne 7"),
    },
    "protocole": "docs/H0-HZ-SNE-V2-PROTOCOLE.md",
}
out = ROOT / "data/tables/hz_sne_LOWZ-V2-MUSH0ES.json"
out.write_text(json.dumps(table, ensure_ascii=False, indent=1),
               encoding="utf-8")
print(f"\n-> {out}")
