"""CAMPAGNE A2 — stress de précision sur les divergences home/balayage.

Contexte (coloration par unité, 2026-09-14) : le street sweep des 46
contacts sous les 4 paquets HL/Gauss/SI/1 donne des mots identiques
partout SAUF CKM, HVP_LO et HLbL. Hypothèse à tester : effet numérique
(arrondi flottant dans la conversion de paquet) vs effet protocolaire.

Trois vérifications :
1. MECANISME — `verdict_register.street_sweep` ne ré-exécute pas le
   runner sous d'autres unités : il reprend (mu_loc, mu_ref) du run
   maison et re-décide avec `_verdict(delta, theta)` SANS la couche GUM.
   Pour un contact `decide="U"`, le seuil maison est U = k·u_c et le
   seuil sweep est θ. Divergence attendue ⟺ decide=U ∧ U ≠ θ ∧ δ dans
   la bande entre les deux régimes de seuil.
2. RE-DECISION — `_adc(delta_home, theta)` reproduit exactement le mot
   sweep pour les 3 contacts (preuve que le sweep ne voit que θ).
3. STRESS NUMERIQUE — recombinaison des budgets GUM en précision
   `decimal` (30 chiffres) vs float64 : l'écart relatif doit être
   ~1e-16, c'est-à-dire des ordres de grandeur SOUS la marge la plus
   mince (CKM : 0,29σ ≈ 4e-4 relatif). Conclusion : l'invariance
   numérique tient ; la divergence est protocolaire, pas numérique.

Campagne dérivée : aucun contact nouveau, aucun gel touché.
"""

from __future__ import annotations

import json
from decimal import Decimal, getcontext

from mvcg.metrics import _adc, marge_adc
from mvcg.registers import CONTACTS, run_contact
from mvcg.verdict_register import street_sweep

getcontext().prec = 30


def uc_decimal(lines: list[dict], R: list[list[float]] | None) -> Decimal:
    """Recombinaison haute précision du budget (forme de gum.u_c)."""
    us = [Decimal(str(l["u"])) for l in lines]
    if not R:
        s = sum(u * u for u in us)
        return s.sqrt()
    # corrélation déclarée : u_c = sqrt(u' R u) — même contrat que gum.u_c
    n = len(us)
    s = Decimal(0)
    for i in range(n):
        for j in range(n):
            s += us[i] * us[j] * Decimal(str(R[i][j]))
    return s.sqrt()


def main() -> None:
    print("=== 1+2. MECANISME : decide=U, U/θ, re-décision ===")
    mecanisme = []
    for c in CONTACTS:
        if not c.gum:
            continue
        r = run_contact(c)
        g = r["extra"]["gum"]
        if g.get("decide") != "U":
            continue
        sw = {row["packet"]: row["verdict"] for row in street_sweep(c.id)["rows"]}
        diverge = len(set(sw.values()) | {r["verdict"]}) > 1
        redecide = _adc(float(r["delta"]), float(c.theta))
        attendu = diverge and abs(g["U"] / c.theta - 1.0) > 1e-9
        ok = (redecide == sw[c.packet]) if not diverge else (redecide in set(sw.values()))
        mecanisme.append({
            "id": c.id, "U_sur_theta": g["U"] / c.theta, "home": r["verdict"],
            "sweep": sw[c.packet], "diverge": diverge, "redecide_theta": redecide,
            "regle_confirmee": bool(ok and (diverge == attendu or not diverge)),
        })
        print(f"{c.id:28s} U/θ={g['U']/c.theta:8.4f} home={r['verdict']:2s} "
              f"sweep={sw[c.packet]:2s} diverge={diverge!s:5s} "
              f"redecide(δ,θ)={redecide:2s} regle={ok}")

    print("\n=== 3. STRESS NUMERIQUE (decimal 30 chiffres vs float64) ===")
    stress = []
    for cid in ["CKM_Row1_Unitarity", "HVP_LO_lat_vs_ee", "HLbL_lat_vs_pheno"]:
        c = next(x for x in CONTACTS if x.id == cid)
        r = run_contact(c)
        g = r["extra"]["gum"]
        uc_dec = uc_decimal(c.gum["lines"], c.gum.get("R"))
        uc_f64 = Decimal(str(g["uc"]))
        ecart_rel = abs(uc_dec - uc_f64) / uc_dec
        marge_sigma = marge_adc(float(r["delta"]), g["U"], r["verdict"]) / g["uc"]
        marge_frac_thr = marge_sigma * g["uc"] / g["U"]
        stress.append({
            "id": cid, "uc_decimal": str(uc_dec), "uc_float64": str(uc_f64),
            "ecart_relatif": float(ecart_rel), "marge_sigma": marge_sigma,
            "marge_fraction_de_thr": float(marge_frac_thr),
        })
        print(f"{cid:28s} ecart relatif uc = {float(ecart_rel):.3e} "
              f"(marge la plus mince du contact : {marge_sigma:.2f}σ "
              f"= {float(marge_frac_thr):.1%} du seuil)")

    with open("a2_stress_precision.json", "w", encoding="utf-8") as f:
        json.dump({"mecanisme": mecanisme, "stress": stress}, f,
                  ensure_ascii=False, indent=1)
    print("\n-> a2_stress_precision.json")


if __name__ == "__main__":
    main()
