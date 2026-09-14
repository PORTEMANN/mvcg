#!/usr/bin/env python3
"""Campagne 7 — refit a la selection officielle SH0ES (USED_IN_SH0ES_HF).

Locale, non publiee (2026-09-14). DERIVE de campagne — aucun contact
cree, aucun gel touche (mots S-/S- inchanges). Suite naturelle de la
campagne 6 : le refit complet a la selection officielle, doublons
portes par la covariance (plus de dedoublonnage e-min).

PROTOCOLE DECLARE :
1. SELECTION OFFICIELLE depuis le .dat : USED_IN_SH0ES_HF = 1
   (277 light curves, 238 noms uniques — la selection de l'analyse H0
   SH0ES 2022, Brout et al.), z dans [0,02343 ; 0,14898] : la coupure
   de vitesse particuliere z > 0,0233 y est deja appliquee. AUCUN
   dedoublonnage : les noms a light curves multiples sont portes avec
   leurs blocs de covariance, comme le fait l'analyse officielle.
   Les calibrateurs (IS_CALIBRATOR = 1, 77 LC / 43 noms, z <= 0,0168)
   ne sont PAS binnes : ce sont les ancres de l'echelle Cepheide, le
   fit d'echelle complet est hors doctrine de la forme gelee.
2. BINS : les 8 frontieres equipopulees des campagnes 4-6 servent de
   grille de comparaison. Les bins 0 et 1 y sont VIDES (le z_min
   officiel 0,02343 tombe dans le bin 2) : le chi2 est calcule sur
   les 6 bins peuples (ndof = 5). Controle de robustesse : rebinning
   equipopule a 8 bins sur la selection officielle (regle de binning
   de la doctrine appliquee a la nouvelle selection).
3. C_bins[b,b'] = moyenne des C_ij sur les LC membres (regle non
   ponderee du contact gelee, appliquee a la covariance), sur
   STAT+SYS complet et en STATONLY (part systematique a selection
   officielle).
4. Mesures : sigma_diag, correlations, chi2/ndof au centre,
   H0* Mahalanobis (les deux cartes), confrontes aux campagnes 4/6 ;
   verification d'ancrage MU_SH0ES officiel par bin ; comparaison
   des moyennes de bins C6 (dedup, 591) vs C7 (277 LC officielles).
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


def mu_pred(z: float, h0: float) -> float:
    g = np.linspace(1e-8, z, 2000)
    chi = np.trapezoid(1.0 / np.sqrt(OM * (1.0 + g) ** 3 + OL), g)
    return 5.0 * math.log10((1.0 + z) * chi * C / h0) + 25.0


def norm(n: str) -> str:
    return re.sub(r"^(sn|asassn-|ps1-|atlas)", "", n.lower().strip())


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
        "mb": float(f[ix["m_b_corr"]]),
        "e_diag": float(f[ix["m_b_corr_err_DIAG"]]),
        "mu_sh0es": float(f[ix["MU_SH0ES"]]),
        "calib": int(f[ix["IS_CALIBRATOR"]]),
        "hf": int(f[ix["USED_IN_SH0ES_HF"]]),
    })
print(f".dat officiel : {len(dat)} light curves")

# --- selection OFFICIELLE : pas de dedoublonnage ---
idx_sel = [i for i, d in enumerate(dat) if d["hf"] == 1]
z_hf = [dat[i]["z"] for i in idx_sel]
n_dup = len(idx_sel) - len({dat[i]["cid"] for i in idx_sel})
print(f"selection officielle HF : {len(idx_sel)} LC, "
      f"{len(idx_sel) - n_dup} noms uniques, {n_dup} LC doublons portes")
print(f"z HF : min {min(z_hf):.5f} (coupure vitesse particuliere SH0ES), "
      f"max {max(z_hf):.5f}")

cal = [d for d in dat if d["calib"] == 1]
print(f"calibrateurs : {len(cal)} LC / {len({d['cid'] for d in cal})} noms, "
      f"z max {max(d['z'] for d in cal):.5f} — ancres Cepheide, non binnes")

# --- frontieres IDENTIQUES campagnes 4-6 (regle equipopulee, sel. C6) ---
best: dict[str, int] = {}
for i, d in enumerate(dat):
    if ZMIN <= d["z"] < ZMAX and d["calib"] == 0:
        k = norm(d["cid"])
        if k not in best or d["e_diag"] < dat[best[k]]["e_diag"]:
            best[k] = i
sel_c6 = sorted(best.values())
sel_z = sorted(dat[i]["z"] for i in sel_c6)
edges = [sel_z[int(i * len(sel_z) / NBINS)] for i in range(NBINS)]
edges.append(sel_z[-1] + 1e-9)

assign = {}
for i in idx_sel:
    for b in range(NBINS):
        if edges[b] <= dat[i]["z"] < edges[b + 1]:
            assign[i] = b
            break
n_par_bin = [sum(1 for i in idx_sel if assign.get(i) == b)
             for b in range(NBINS)]
print(f"LC par bin (grille C4-C6) : {n_par_bin}")
pop = [b for b in range(NBINS) if n_par_bin[b] > 0]
print(f"bins peupls : {pop} — bins vides : "
      f"{[b for b in range(NBINS) if b not in pop]} (declare : le z_min "
      f"officiel tombe au-dela de leurs frontieres)")

# --- chargement des deux matrices ---
print("chargement STAT+SYS.cov et STATONLY.cov ...")
raw_sys = np.loadtxt(ROOT / "pantheon_STAT+SYS.cov", skiprows=1)
cov_sys = raw_sys.reshape(1701, 1701)
del raw_sys
raw_stat = np.loadtxt(ROOT / "pantheon_STATONLY.cov", skiprows=1)
cov_stat = raw_stat.reshape(1701, 1701)
del raw_stat


def agregate(cov_full: np.ndarray, bins: list[int],
             assign_of: dict[int, int]) -> np.ndarray:
    """C_bins par moyenne non ponderee des C_ij, restreinte a `bins`."""
    idx_arr = np.array([i for i in idx_sel if assign_of[i] in bins])
    sub = cov_full[np.ix_(idx_arr, idx_arr)]
    nb = len(bins)
    c_bins = np.zeros((nb, nb))
    cnt = np.zeros((nb, nb))
    pos_of = {}
    for a_pos, i in enumerate(idx_arr):
        pos_of[a_pos] = bins.index(assign_of[i])
    for a_pos in range(len(idx_arr)):
        bi = pos_of[a_pos]
        for b_pos in range(len(idx_arr)):
            c_bins[bi, pos_of[b_pos]] += sub[a_pos, b_pos]
            cnt[bi, pos_of[b_pos]] += 1
    return c_bins / cnt


c_sys = agregate(cov_sys, pop, assign)
c_stat = agregate(cov_stat, pop, assign)
nb_pop = len(pop)

print(f"\n{'bin':>3} {'n_LC':>5} {'sigma_STAT':>11} {'sigma_SYS':>10} "
      f"{'theta_nw':>9} {'ratio_SYS':>9}")
for pb, b in enumerate(pop):
    s_stat, s_sys = math.sqrt(c_stat[pb, pb]), math.sqrt(c_sys[pb, pb])
    print(f"{b:3d} {n_par_bin[b]:5d} {s_stat:11.5f} {s_sys:10.5f} "
          f"{THETA_NW:9.5f} {s_sys / THETA_NW:9.2f}")
m_sys = float(np.mean(np.sqrt(np.diag(c_sys))))
m_stat = float(np.mean(np.sqrt(np.diag(c_stat))))
print(f"moyennes sigma : STATONLY {m_stat:.5f}, STAT+SYS {m_sys:.5f} "
      f"(theta declare {THETA_NW}, ratio {m_sys / THETA_NW:.2f})")

print("\ncorrelations inter-bins peuples (STAT+SYS) :")
for pb in range(nb_pop):
    row = []
    for qb in range(nb_pop):
        r = c_sys[pb, qb] / math.sqrt(c_sys[pb, pb] * c_sys[qb, qb])
        row.append(f"{r:+.3f}")
    print("  " + " ".join(row))

ndof = nb_pop - 1

# --- confrontation : MU_SH0ES officiel (module de distance des donnees)
# vs cartes gelees, sur les bins peupls (les deux cartes) ---
print("\nverif ancrage (bins peupls) : MU_SH0ES officiel moyen par bin "
      "- mu des cartes gelees")
mu_data = {b: float(np.mean([dat[i]["mu_sh0es"] for i in idx_sel
                             if assign[i] == b])) for b in pop}
for nom in ("Planck", "SH0ES"):
    t = load_table(f"hz_sne_LOWZ-LITERATURE-{nom}.json")
    mu_g = np.array([bb[1] for bb in t["bins"]])
    ecarts = [mu_data[b] - mu_g[b] for b in pop]
    print(f"  carte {nom} : ecarts {[f'{e:+.4f}' for e in ecarts]} — "
          f"moyen {np.mean(ecarts):+.5f} mag")


def campagne(z_bins, mu_bins, cb, ndof_):
    def residus(h0: float) -> np.ndarray:
        return np.array([mu_pred(z, h0) for z in z_bins]) - mu_bins

    def chi2(h0: float) -> float:
        r = residus(h0)
        return float(r @ np.linalg.solve(cb, r))

    grid = np.linspace(60.0, 85.0, 2501)
    hstar, cmin = min(((h, chi2(h)) for h in grid), key=lambda x: x[1])
    return hstar, cmin, chi2


# --- chi2 / H0* Mahalanobis sur la grille C4-C6 (6 bins peuples) ---
for nom, h0_rms in (("Planck", 69.04), ("SH0ES", 74.82)):
    t = load_table(f"hz_sne_LOWZ-LITERATURE-{nom}.json")
    z_all = np.array([bb[0] for bb in t["bins"]])
    mu_all = np.array([bb[1] for bb in t["bins"]])
    z_b, mu_b = z_all[pop], mu_all[pop]
    print(f"\nCARTE {nom} (grille C4-C6, {nb_pop} bins peuples, "
          f"ndof = {ndof})")
    print(f"  H0* rms campagne 4 (8 bins) : {h0_rms}")
    for label, cb in (("STATONLY", c_stat), ("STAT+SYS", c_sys)):
        hstar, cmin, chi2 = campagne(z_b, mu_b, cb, ndof)
        print(f"  [{label}] H0* = {hstar:.3f}  chi2_min = {cmin:.3f}  "
              f"chi2/ndof = {cmin / ndof:.3f}")
        for h0v in (67.4, 73.04):
            print(f"    chi2({h0v}) = {chi2(h0v):8.3f}")

# --- controle de robustesse : rebinning equipopule sur la selection ---
print("\nCONTROLE ROBUSTESSE — 8 bins equipopules sur la selection "
      "officielle (regle de la doctrine)")
z_sel = np.array([dat[i]["z"] for i in idx_sel])
edges_o = [z_sel[int(i * len(z_sel) / NBINS)] for i in range(NBINS)]
edges_o.append(z_sel[-1] + 1e-9)
assign_o = {}
for i in idx_sel:
    for b in range(NBINS):
        if edges_o[b] <= dat[i]["z"] < edges_o[b + 1]:
            assign_o[i] = b
            break
c_sys_o = agregate(cov_sys, list(range(NBINS)), assign_o)
z_mid_o = np.array([float(np.mean([dat[i]["z"] for i in idx_sel
                                   if assign_o[i] == b]))
                    for b in range(NBINS)])
# du COTE DONNEES : mu = moyenne de MU_SH0ES officiel par bin
mu_o = np.array([float(np.mean([dat[i]["mu_sh0es"] for i in idx_sel
                                if assign_o[i] == b]))
                 for b in range(NBINS)])
hstar, cmin, _ = campagne(z_mid_o, mu_o, c_sys_o, NBINS - 1)
resid = np.array([mu_pred(z, hstar) for z in z_mid_o])
print(f"  [cote donnees, forme gelee libre en H0] H0* = {hstar:.3f}, "
      f"chi2/ndof = {cmin / (NBINS - 1):.3f}, rms brut = "
      f"{float(np.sqrt(np.mean((resid - mu_o) ** 2))):.5f}")

print("\nCAMPAGNE 7 TERMINEE — derive de campagne, aucun gel touche")
