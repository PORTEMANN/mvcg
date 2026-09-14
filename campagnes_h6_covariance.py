#!/usr/bin/env python3
"""Campagne 6 — covariance complète C_stat+syst appliquée aux 8 bins.

Locale, non publiee (2026-09-13 soir). DERIVE de campagne — aucun
contact cree, aucun gel touche (mots S-/S- inchanges sur les tables
non ponderees). Chiffrage de la dette de compression.

SOURCES (declarees) :
- Matrices : Pantheon+SH0ES_STATONLY.cov et STAT+SYS.cov, depot
  officiel github.com/PantheonPlusSH0ES/DataRelease
  (4_DISTANCES_AND_COVAR/), format : 1ere ligne N=1701 puis N^2
  lignes sequentielles. Ordre = ordre de Pantheon+SH0ES.dat.
- Le README du depot avertit noir sur blanc : m_b_corr_err_DIAG
  (nos e_mBcorr, donc notre theta declare) « DO NOT FIT COSMOLOGICAL
  PARAMETERS WITH THESE UNCERTAINTIES — YOU MUST USE THE FULL
  COVARIANCE ». La dette de compression est documentee par la source
  elle-meme.

PROTOCOLE DECLARE :
1. SELECTION CONSTANTE avec la campagne 4 : memes noms normalises,
   e_mBcorr minimal (dedoublonnage), fenetre zHD [0.01, 0.15),
   memes 8 frontieres de bins. Seule la propagation d'incertitude
   change : e_diag -> covariance complete.
   Limite declaree : la covariance des doublons ecartes et la
   covariance Cepheid ne sont pas portees (sous-matrice des indices
   retenus seulement) — effet covariance a selection fixee, pas
   refit complet de la selection officielle.
2. C_bins[b,b'] = moyenne des C_ij, i dans bin b, j dans bin b'
   (regle du contact non ponderee, appliquee a la covariance).
3. Mesures :
   a. sigma_diag(b) = racine(C_bins[b,b]) vs theta = 0.02756 ;
   b. correlations inter-bins (off-diag / racine(diag*diag)) ;
   c. CHI2 = r^T C_bins^{-1} r au centre H0*, ndof = 7 (1 parametre
      d'amplitude ajuste par H0*) — LE chiffrage de la dette ;
   d. H0* par Mahalanobis (min chi2) vs H0* rms (campagne 4) ;
   e. verification croisee : MU_SH0ES officiel (ancrage natif du
      .dat) vs notre transposition K_B — ecart d'amplitude.
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

OM, OL, C = 0.315, 0.685, 299792.458
ZMIN, ZMAX, NBINS = 0.01, 0.15, 8
THETA_NW = 0.02756  # theta declare campagne LITERATURE (non ponderee)


def norm(n: str) -> str:
    return re.sub(r"^(sn|asassn-|ps1-|atlas)", "", n.lower().strip())


def mu_pred(z: float, h0: float) -> float:
    g = np.linspace(1e-8, z, 2000)
    chi = np.trapezoid(1.0 / np.sqrt(OM * (1.0 + g) ** 3 + OL), g)
    return 5.0 * math.log10((1.0 + z) * chi * C / h0) + 25.0


# --- chargement .dat officiel (ordre = indices matrices) ---
lines = (ROOT / "pantheon_ref.dat").read_text().splitlines()
hdr = lines[0].split()
ix = {h: i for i, h in enumerate(hdr)}
dat = []
for ln in lines[1:]:
    f = ln.split()
    dat.append({
        "cid": f[ix["CID"]], "z": float(f[ix["zHD"]]),
        "e_diag": float(f[ix["m_b_corr_err_DIAG"]]),
        "mu_sh0es": float(f[ix["MU_SH0ES"]]),
        "calib": int(f[ix["IS_CALIBRATOR"]]),
    })
print(f".dat officiel : {len(dat)} light curves")

# coherence e_diag table7 vs .dat (ordre identique attendu)
t7 = list(__import__("csv").DictReader(
    open(ROOT / "pantheon_t7.csv", newline="", encoding="utf-8")))
diffs = [abs(float(t7[i]["e_mBcorr"]) - dat[i]["e_diag"])
         for i in range(0, 1701, 97)]
print(f"coherence e_mBcorr table7/.dat (ech. 18) : max {max(diffs):.2e}")

# --- selection identique campagne 4 (dedoublonnage e-min) ---
best: dict[str, int] = {}
for i, d in enumerate(dat):
    k = norm(d["cid"])
    if ZMIN <= d["z"] < ZMAX and d["calib"] == 0:
        if k not in best or d["e_diag"] < dat[best[k]]["e_diag"]:
            best[k] = i
idx_sel = sorted(best.values())
print(f"selection : {len(idx_sel)} SNe uniques (campagne 4 : 598)")

# --- frontieres de bins : memes regles (equipopulaire sur la selection) ---
sel_z = sorted(dat[i]["z"] for i in idx_sel)
edges = [sel_z[int(i * len(sel_z) / NBINS)] for i in range(NBINS)]
edges.append(sel_z[-1] + 1e-9)
assign = {}
for i in idx_sel:
    for b in range(NBINS):
        if edges[b] <= dat[i]["z"] < edges[b + 1]:
            assign[i] = b
            break

# --- chargement STAT+SYS (33 Mo) ---
print("chargement STAT+SYS.cov ...")
raw = np.loadtxt(ROOT / "pantheon_STAT+SYS.cov", skiprows=1)
cov_full = raw.reshape(1701, 1701)
print(f"matrice chargee : {cov_full.shape}")

# --- sous-matrice selectionnee, agrégée en 8 bins ---
idx_arr = np.array(idx_sel)
sub = cov_full[np.ix_(idx_arr, idx_arr)]
c_bins = np.zeros((NBINS, NBINS))
cnt = np.zeros((NBINS, NBINS))
for a_pos, i in enumerate(idx_sel):
    bi = assign[i]
    for b_pos, j in enumerate(idx_sel):
        c_bins[bi, assign[j]] += sub[a_pos, b_pos]
        cnt[bi, assign[j]] += 1
c_bins /= cnt

print(f"\n{'bin':>3} {'sigma_diag':>11} {'theta_nw':>9} {'gonflement':>10}")
sig_diag = np.sqrt(np.diag(c_bins))
for b in range(NBINS):
    print(f"{b:3d} {sig_diag[b]:11.5f} {THETA_NW:9.5f} "
          f"{sig_diag[b] / THETA_NW:10.3f}")
print(f"moyenne sigma_diag covarie : {np.mean(sig_diag):.5f} "
      f"vs theta declare {THETA_NW} (ratio "
      f"{np.mean(sig_diag) / THETA_NW:.2f})")

print("\ncorrelations inter-bins (off-diag / sqrt(diag*diag)) :")
for b in range(NBINS):
    row = []
    for bp in range(NBINS):
        r = c_bins[b, bp] / math.sqrt(c_bins[b, b] * c_bins[bp, bp])
        row.append(f"{r:+.3f}")
    print("  " + " ".join(row))

# --- chi2/ndof et H0* Mahalanobis (les deux cartes) ---
for nom, ancrage in (("Planck", 67.4), ("SH0ES", 73.04)):
    t = load_table(f"hz_sne_LOWZ-LITERATURE-{nom}.json")
    z_bins = np.array([bb[0] for bb in t["bins"]])
    mu_bins = np.array([bb[1] for bb in t["bins"]])
    # verification croisee MU_SH0ES officiel (carte SH0ES seulement)
    if nom == "SH0ES":
        # moyenne MU_SH0ES officielle par bin, ecart vs mu_bins
        ecarts = []
        for b in range(NBINS):
            mus = [dat[i]["mu_sh0es"] for i in idx_sel if assign[i] == b]
            ecarts.append(float(np.mean(mus)) - mu_bins[b])
        print(f"\nverif ancrage : ecart MU_SH0ES officiel - notre "
              f"transposition par bin : {[f'{e:+.4f}' for e in ecarts]}")
        print(f"  ecart moyen : {np.mean(ecarts):+.5f} mag")

    def residus(h0: float) -> np.ndarray:
        return np.array([mu_pred(z, h0) for z in z_bins]) - mu_bins

    def chi2(h0: float) -> float:
        r = residus(h0)
        return float(r @ np.linalg.solve(c_bins, r))

    grid = np.linspace(60.0, 85.0, 2501)
    hstar_c, cmin = min(((h, chi2(h)) for h in grid), key=lambda x: x[1])
    rms_hstar = float(np.sqrt(np.mean(residus(hstar_c) ** 2)))
    print(f"\nCARTE {nom} : chi2/ndof au centre Mahalanobis")
    print(f"  H0* (Mahalanobis) = {hstar_c:.3f} (rms : 69.04 / "
          f"{'74.82' if nom == 'SH0ES' else '69.04'})")
    print(f"  chi2_min = {cmin:.3f}, ndof = 7 -> chi2/ndof = "
          f"{cmin / 7:.3f}")
    print(f"  rms brut au H0* covarie : {rms_hstar:.5f} "
          f"(non covarie : 0.04579)")
    for h0v in (67.4, 70.0, 73.04):
        print(f"  chi2({h0v}) = {chi2(h0v):8.3f} "
              f"(rms {float(np.sqrt(np.mean(residus(h0v)**2))):.5f})")

print("\nCAMPAGNE 6 TERMINEE — derive de campagne, aucun gel touche")
