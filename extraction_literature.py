#!/usr/bin/env python3
"""Extraction LITERATURE bas-z depuis Pantheon+ (Brout et al. 2022, Table 7).

Chantier local, non publie. Methodologie declaree :
1. DEDOUBLONNAGE declare : la table 7 porte 1701 light curves pour
   1550 SNe uniques (151 SNe observees par plusieurs surveys). Regle :
   par nom, garder la mesure a e_mBcorr minimal. La cosmologie
   officielle gere les doublons par covariance ; notre extraction les
   dedouble et la declare.
2. Fenetre zHD ∈ [0.01, 0.15) : miroir de la table DEMO. Les
   calibrateurs Cepheides (tous z < 0.01, verifies) sont exclus.
3. Constante de convention K_B = moyenne(A(z) - mBcorr) sur le
   diagramme COMPLET dedouble, A(z) = 5*log10((1+z)*chi(z)*c) + 25
   a la forme gelee (Omega 0.315/0.685, loi du contact). K_B mesure
   la convention d'amplitude de la source — la combinaison
   M - 5*log10(H0) n'est PAS separable sans les Cepheides (dege-
   nescence documentee Brout et al. 2022 §2.3).
4. VALIDATION CROISEE : std(A - mBcorr) sur le diagramme complet vs
   rms BS21 = 0.171 mag publie (Brout et al. 2022, Table 2).
5. 8 bins equipopulaires, moyenne arithmetique declaree (cosmologie
   officielle ponderee : ecart = dette de compression).
6. sigma_bin = sqrt(moyenne(e_mBcorr^2)/N) : incertitudes declarees
   par la collaboration (propriete de la source).
7. Transposition d'ancrage EXACTE a Omega gelas identiques :
   mu_obs_ancre = mBcorr + 5*log10(H0_ancrage) - K_B
   -> la courbe de l'ancrage passe par les bins EN MOYENNE par
   construction de conversion d'unite, jamais par ajustement sur
   les bins (aucun parametre n'est fitte sur la courbe de fabrication).
"""
from __future__ import annotations

import csv
import json
import math
import re
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent
OM, OL, C = 0.315, 0.685, 299792.458
ZMIN, ZMAX, NBINS = 0.01, 0.15, 8
ANCHORAGES = {"SH0ES": (73.04, 1.04), "Planck": (67.4, 0.5)}

rows = []
with open(ROOT / "pantheon_t7.csv", newline="", encoding="utf-8") as fh:
    for r in csv.DictReader(fh):
        rows.append(r)
print(f"table 7 brute : {len(rows)} light curves")

# --- (1) dedoublonnage declare : garder e_mBcorr minimal par nom ---
def _norm(n: str) -> str:
    n = n.lower().strip()
    return re.sub(r"^(sn|asassn-|ps1-|atlas)", "", n)


best: dict[str, dict] = {}
for r in rows:
    n = _norm(r["Name"])
    if n not in best or float(r["e_mBcorr"]) < float(best[n]["e_mBcorr"]):
        best[n] = r
rows = list(best.values())
print(f"apres dedoublonnage (regle declaree) : {len(rows)} SNe uniques")

z_all = np.array([float(r["zHD"]) for r in rows])
m_all = np.array([float(r["mBcorr"]) for r in rows])

# --- (3) constante de convention + (4) validation croisee ---
g_all = np.linspace(1e-8, 2.3, 4000)
e_inv = 1.0 / np.sqrt(OM * (1.0 + g_all) ** 3 + OL)
chi_all = np.array([np.trapezoid(e_inv[:max(2, int(zi / 2.3 * 4000))],
                                 g_all[:max(2, int(zi / 2.3 * 4000))])
                    for zi in z_all])
a_z = 5.0 * np.log10((1.0 + z_all) * chi_all * C) + 25.0
b = a_z - m_all
k_b = float(np.mean(b))
rms_glue = float(np.std(b, ddof=1))
print(f"K_B (convention table 7, forme gelee) : {k_b:.5f} mag")
print(f"VALIDATION CROISEE : std(A - mBcorr) = {rms_glue:.4f} mag vs "
      f"rms BS21 publie = 0.171 mag (Brout 2022, Table 2)")
rms_ge01 = float(np.std(b[z_all >= 0.01], ddof=1))
print(f"  std a z >= 0.01 : {rms_ge01:.4f} mag vs publie ~0.15 mag "
      f"(Table 2, hors vitesses particulieres)")
print(f"  ecart residuel du aux Omega gelas (non ajustes) et aux "
      f"nuisances non re-ajustees : declare, pas corrige")

# --- (2) fenetre bas-z ---
sel = [(float(r["zHD"]), float(r["mBcorr"]), float(r["e_mBcorr"]))
       for r in rows if ZMIN <= float(r["zHD"]) < ZMAX]
print(f"fenetre zHD [{ZMIN}, {ZMAX}) : {len(sel)} SNe")

# --- (5) 8 bins equipopulaires ---
sel.sort(key=lambda t: t[0])
edges = [sel[int(i * len(sel) / NBINS)][0] for i in range(NBINS)]
edges.append(sel[-1][0] + 1e-9)
bins = []
for bidx in range(NBINS):
    grp = [t for t in sel if edges[bidx] <= t[0] < edges[bidx + 1]]
    zz = np.array([t[0] for t in grp])
    mm = np.array([t[1] for t in grp])
    ee = np.array([t[2] for t in grp])
    n = len(grp)
    bins.append({
        "z_median": round(float(np.median(zz)), 6), "N": n,
        "mBcorr_mean": round(float(np.mean(mm)), 6),
        "sigma_bin": round(float(np.sqrt(np.mean(ee ** 2) / n)), 6),
        "rms_intra": round(float(np.std(mm, ddof=1)), 4),
        "e_moy": round(float(np.sqrt(np.mean(ee ** 2))), 4),
        "z_range": [round(float(zz.min()), 6), round(float(zz.max()), 6)],
    })
print(f"\n{'z_med':>8} {'N':>4} {'e_moy':>7} {'sig_bin':>8} {'rms_intra':>9}")
for bb in bins:
    print(f"{bb['z_median']:8.4f} {bb['N']:4d} {bb['e_moy']:7.4f} "
          f"{bb['sigma_bin']:8.5f} {bb['rms_intra']:9.4f}")

sig_theta = round(float(np.mean([bb["sigma_bin"] for bb in bins])), 6)
delta_fp = 5.0 * math.log10(73.04 / 67.4)
print(f"\ntheta declare (moyenne sigma_bin) : {sig_theta:.5f} mag ; "
      f"2*theta = {2 * sig_theta:.5f}")
print(f"ecart amplitude 5*log10(73.04/67.4) = {delta_fp:.4f} mag")
print(f"rms attendu fabrication opposee : "
      f"{math.sqrt(sig_theta**2 + delta_fp**2):.4f} mag "
      f"-> S- sans suspense")
print(f"rms attendu fabrication de l'ancrage : bruit realise des bins "
      f"vs theta = {sig_theta:.5f} -> zone P au cheveu du S-/S+ "
      f"(suspense, comme la DEMO)")

# --- (7) les deux tables ---
for nom, (h0a, ua) in ANCHORAGES.items():
    dmu = 5.0 * math.log10(h0a) - k_b
    table = {
        "id": f"hz_sne_lowz_literature_{nom.lower()}",
        "vintage": "LITERATURE-PantheonPlus-B22",
        "source": "Pantheon+ : Table 7 de Brout et al. 2022 (ApJ 938:110, "
                  "magnitudes corrigees BBC, via VizieR J/ApJ/938/110), "
                  "SNe Ia flux Hubble zHD ∈ [0.01, 0.15), dedoublonnees "
                  "(regle : nom normalise minuscules, prefixes retires, "
                  "e_mBcorr minimal), calibrateurs "
                  "Cepheides exclus (tous z < 0.01)",
        "doi_or_ref": "Brout et al. 2022, ApJ, 938, 110 (Table 7 ; Table 2 "
                      ": rms BS21 = 0.171 mag global, ~0.15 mag a z >= "
                      "0.01) ; Scolnic et al. 2022, ApJ, 938, 113",
        "species": "supernovae Ia (Pantheon+, flux Hubble bas-z)",
        "quantity": "module de distance binned bas-z, amplitude ancree "
                    f"{nom} (H0 = {h0a} ± {ua} km/s/Mpc declare)",
        "dimension": "mag",
        "packet": "1",
        "bins": [[bb["z_median"], round(bb["mBcorr_mean"] - dmu, 6)]
                 for bb in bins],
        "sigma_mag": sig_theta,
        "params": {
            "Omega_m": OM, "Omega_L": OL, "c_km_s": C,
            "H0_ancrage_km_s_Mpc": h0a,
            "u_ancrage_km_s_Mpc": ua,
            "K_B_convention": round(k_b, 6),
            "K_B_methode": "moyenne(A(z) - mBcorr) sur le diagramme "
                           "complet dedouble, A a la forme gelee "
                           "(Omega gelas) ; la combinaison M - 5*log10(H0) "
                           "n'est pas separable sans Cepheides "
                           "(degenrescence Brout et al. 2022 §2.3)",
            "transposition": "mu_ancre = mBcorr + 5*log10(H0_ancrage) - "
                             "K_B ; exact a Omega gelas identiques ; la "
                             "courbe de l'ancrage passe par les bins EN "
                             "MOYENNE par conversion d'unite, jamais par "
                             "ajustement sur les bins",
            "validation_croisee": f"std(A - mBcorr) = {rms_glue:.4f} mag "
                                  f"vs rms BS21 publie 0.171 mag",
            "regle_bins": "8 bins equipopulaires sur zHD, moyenne "
                          "arithmetique declaree (non ponderee)",
            "sigma_bin": "sqrt(moyenne(e_mBcorr^2)/N) : incertitudes "
                         "declarees par la collaboration",
        },
        "dettes": {
            "D-nature": "donnee reelle binned ; compression d'evenements "
                        "individuels",
            "D-compression": "bins non ponderes (cosmologie officielle "
                             "ponderee) ; covariance C_stat/C_syst "
                             "ignoree : calibration commune NON reduite "
                             "en sqrt(N)",
            "D-ancrage": f"amplitude fixee a l'echelle {nom} par "
                         f"transposition exacte : la carte porte le choix "
                         f"d'ancrage",
            "D-independance": ("ancrage SH0ES : donnee et levier H0<-SH0ES "
                               "non independants (pendant Landau)"
                               if nom == "SH0ES" else
                               "ancrage Planck : transposition depuis la "
                               "convention de la table ; dette symetrique "
                               "au contact SH0ES"),
            "D-vitesses": "zHD corrige 2M++ ; sigma_vpec declaratif dans "
                          "e_mBcorr (dominant a bas z, ex. R22 n'utilise "
                          "le flux Hubble que pour z > 0.023)",
            "D-miroir": "les deux ancrages sont des miroirs exacts "
                        "(memes bins, transposition pure) : les contacts "
                        "portent une meme carte avec deux dettes "
                        "differentes, pas deux verdicts independants",
        },
        "sha256_note": "figer ce fichier ; changer params = autre D",
    }
    out = ROOT / "data" / "tables" / f"hz_sne_LOWZ-LITERATURE-{nom}.json"
    out.write_text(json.dumps(table, indent=2, ensure_ascii=False),
                   encoding="utf-8")
    print(f"\ntable {nom} -> {out.name}  (Δμ = {dmu:+.4f} ; "
          f"M implicite = {dmu:+.4f})")
    print(f"  bins mu : {[r[1] for r in table['bins']]}")
print("\nEXTRACTION TERMINEE — tables locales, non poussees")
