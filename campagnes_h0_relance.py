#!/usr/bin/env python3
"""Relance des campagnes H0 (locale, non publiée) — 2026-09-13 soir.

C1 street sweep : mot P indépendant du paquet d'unité (hl/gauss/si/1).
C2 frontière du levier tension : balayage sigma déclarés, frontières
   exactes du changement de mot (SH0ES glisse, Planck fixe et vice versa).
C3 frontière du contact bas-z (NOUVELLE) : levier H0 de la courbe H(z),
   où le mot S−/P/S+ bascule quand on déplace la fabrication.

Aucun gel modifié : les mots restent figés (P / S−), theta = 0,05 gelé.
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))

from mvcg.registers import run_registers  # noqa: E402
from mvcg.tables import load_table  # noqa: E402

THETA = 0.05
THETA_REL = 0.05  # tension : theta absolu sur ecart relatif


def mot(delta: float, theta: float) -> str:
    if delta < theta:
        return "S+"
    if delta < 2.0 * theta:
        return "P"
    return "S-"


# ---------------------------------------------------------------- C0 : gel
print("=" * 68)
print("C0 — re-verification des mots geles apres restauration des fichiers")
rows = {r["id"]: r for r in run_registers()["rows"]}
r_t = rows["H0_Ecart_Planck_SH0ES"]
r_z = rows["H0_Hz_SNe_LOWZ_DEMO"]
print(f"tension : mot={r_t['verdict']}  delta={r_t['delta']:.12f}  "
      f"(attendu P / 0.08367952522255195)")
print(f"bas-z   : mot={r_z['verdict']}  delta={r_z['delta']:.12f}  "
      f"(attendu S- / 0.11727000773640141)")
assert r_t["verdict"] == "P" and abs(r_t["delta"] - 0.08367952522255195) < 1e-12
assert r_z["verdict"] == "S-" and abs(r_z["delta"] - 0.11727000773640141) < 1e-12
print("OK — les deux mots geles sont intacts")

# ------------------------------------------------------------- C1 : sweep
print("=" * 68)
print("C1 — street sweep : le mot sous chaque paquet de la rue")
t = load_table("h0_LITERATURE-2018.json")
p = t["params"]
hp, hs = float(p["Planck2018_H0"]), float(p["SH0ES2022_H0"])
# km/s/Mpc ; /s ; m/s/Mpc : l'ecart relatif est adimensionne, invariant
paquets = {
    "km/s/Mpc": (1.0, 1.0),
    "/s": (1 / 3.0856775814913673e19, 1 / 3.0856775814913673e19),
    "m/s/Mpc": (1000.0, 1000.0),
    "1 (domicile)": (1.0, 1.0),
}
for nom, (kp, ksp) in paquets.items():
    delta = abs((hs * ksp) / (hp * kp) - 1.0)
    print(f"  paquet {nom:14s} : delta={delta:.6f}  mot={mot(delta, THETA_REL)}")
    assert mot(delta, THETA_REL) == "P"
print("OK — mot independant du paquet, aucun paquet illicite")

# ------------------------------------------------------ C2 : frontières
print("=" * 68)
print("C2 — frontiere du levier tension (sigma declares)")
u_s, u_p = 1.04, 0.5


def ecart(hp: float, hs: float) -> float:
    return abs(hs / hp - 1.0)


print("SH0ES glisse (Planck 67,4 fixe) :")
for k in (-3, -2, -1, 0, 1, 2):
    s = hs + k * u_s
    d = ecart(hp, s)
    print(f"  {k:+d} sigma : S={s:6.2f}  delta={d * 100:7.3f} %  mot={mot(d, THETA_REL)}")
print("Planck glisse (SH0ES 73,04 fixe) :")
for k in (-2, -1, 0, 4, 5):
    pv = hp + k * u_p
    d = ecart(pv, hs)
    print(f"  {k:+d} sigma : P={pv:6.2f}  delta={d * 100:7.3f} %  mot={mot(d, THETA_REL)}")

# frontières exactes par bisection
def frontiere(f, a: float, b: float, target: float) -> float:
    for _ in range(80):
        m = 0.5 * (a + b)
        if abs(f(m) - target) < 1e-15:
            return m
        if (f(a) - target) * (f(m) - target) < 0:
            b = m
        else:
            a = m
    return 0.5 * (a + b)


s_plus_lim = frontiere(lambda s: ecart(hp, s), hs - 5 * u_s, hs, THETA_REL)
s_moins_lim = frontiere(lambda s: ecart(hp, s), hs, hs + 3 * u_s, 2 * THETA_REL)
p_plus_lim = frontiere(lambda pv: ecart(pv, hs), hp, hp + 6 * u_p, THETA_REL)
p_moins_lim = frontiere(lambda pv: ecart(pv, hs), hp - 3 * u_p, hp, 2 * THETA_REL)
print(f"  frontiere exacte : S+ si S <= {s_plus_lim:.4f} ({(s_plus_lim - hs) / u_s:+.2f} sigma S)")
print(f"                     S- si S >= {s_moins_lim:.4f} ({(s_moins_lim - hs) / u_s:+.2f} sigma S)")
print(f"  frontiere exacte : S+ si P >= {p_plus_lim:.4f} ({(p_plus_lim - hp) / u_p:+.2f} sigma P)")
print(f"                     S- si P <= {p_moins_lim:.4f} ({(p_moins_lim - hp) / u_p:+.2f} sigma P)")

# ------------------------------------------- C3 : frontière contact bas-z
print("=" * 68)
print("C3 — frontiere du contact bas-z : levier H0 de la courbe H(z)")
tz = load_table("hz_sne_LOWZ-DEMO-2026.json")
pz = tz["params"]
om, ol, c = float(pz["Omega_m"]), float(pz["Omega_L"]), float(pz["c_km_s"])


def rms(h0: float) -> float:
    res = []
    for z, mu_obs in tz["bins"]:
        g = np.linspace(1e-8, z, 2000)
        chi = np.trapezoid(1.0 / np.sqrt(om * (1.0 + g) ** 3 + ol), g)
        dl = (1.0 + z) * chi * c / h0
        res.append((5.0 * math.log10(dl) + 25.0 - mu_obs) ** 2)
    return float(np.sqrt(np.mean(res)))


print("balayage H0 de la courbe (bins et theta geles, jamais touches) :")
for h0v in (65.0, 66.0, 67.4, 68.5, 69.5, 70.0, 70.5, 71.0, 71.5,
            72.5, 73.04, 74.0, 75.0, 76.0):
    r = rms(h0v)
    print(f"  H0={h0v:6.2f} : rms={r:.6f} mag  delta/theta={r / THETA:6.3f}  mot={mot(r, THETA)}")

h0_min = frontiere(rms, 70.0, 72.0, 0.0)  # minimum du rms par bisection sur pente
# rms n'est pas monotone : on balaye finement pour localiser le min
grid = np.linspace(68.0, 74.0, 601)
vals = [(h, rms(h)) for h in grid]
h_star, r_min = min(vals, key=lambda t: t[1])
print(f"minimum du rms : H0*={h_star:.3f}, rms_min={r_min:.6f} mag "
      f"(theta={THETA} -> mot={mot(r_min, THETA)}, marge S+ : {r_min - THETA:+.6f})")

# frontieres : delta = 2 theta (S- <-> P) de chaque cote, delta = theta (P <-> S+)
gauche_p = frontiere(rms, 67.4, h_star, 2 * THETA)
droite_p = frontiere(rms, h_star, 74.0, 2 * THETA)
print(f"frontiere S-/P : H0 <= {gauche_p:.4f} (S-) , H0 >= {droite_p:.4f} (S-)")
try:
    g_splus = frontiere(rms, gauche_p, h_star, THETA)
    d_splus = frontiere(rms, h_star, droite_p, THETA)
    print(f"frontiere P/S+ : H0 dans [{g_splus:.4f}, {d_splus:.4f}] (P) "
          f"-> S+ au-dela")
except Exception as e:  # noqa: BLE001
    print("frontiere P/S+ :", e)
print(f"acces au S+ : rms_min={r_min:.6f} vs theta={THETA} -> "
      f"{'S+ INACCESSIBLE a 8 bins' if r_min > THETA else 'S+ accessible'}")

print("=" * 68)
print("CAMPAGNES TERMINEES — aucun gel modifie, mots toujours figes")
