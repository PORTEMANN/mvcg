"""CAMPAGNE MARGE — prototype local (2026-09-14).

Chaque verdict du registre gagne son épaisseur : à combien de frontières
(θ et 2θ, ou U et 2U selon decide) se trouve le δ mesuré ?

La marge est exprimée en deux unités :
  - en θ (ou thr de décision) : universel, tous contacts ;
  - en σ (u_c GUM déclaré) : seulement là où un budget d'incertitude
    est gelé — c'est la vraie « épaisseur » face à une réanalyse qui
    remonterait l'incertitude déclarée.

Convention : marge positive = robuste (le mot tient), négative = déjà
passé (impossible par construction). Pour un P, distance à la frontière
la plus proche. Un S− au cheveu de 2θ a une marge mince : une réanalyse
déclarée peut le renvoyer en P sans rien changer au protocole.

Campagne dérivée, aucun contact nouveau, aucun gel touché.
"""

from __future__ import annotations

import json

from mvcg.metrics import marge_adc
from mvcg.registers import CONTACTS, run_contact


def main() -> None:
    rows = []
    for c in CONTACTS:
        r = run_contact(c)
        g = (r.get("extra") or {}).get("gum") or {}
        delta = float(r["delta"])
        theta = float(c.theta)
        decide = g.get("decide")
        uc = g.get("uc")
        U = g.get("U")
        thr = float(U) if (decide == "U" and U) else theta
        mot = r["verdict"]
        m_thr = marge_adc(delta, thr, mot)
        m_sig = (m_thr / uc) if (uc and uc > 0) else None
        rows.append({
            "id": c.id,
            "verdict": mot,
            "delta": delta,
            "theta": theta,
            "thr": thr,
            "decide": decide or "theta",
            "uc": uc,
            "marge_thr": m_thr,
            "marge_sigma": m_sig,
            "dimension": c.dimension,
            "packet": c.packet,
        })

    rows.sort(key=lambda r: r["marge_thr"])
    print(f"{'contact':34s} {'mot':3s} {'δ/θ':>9s} {'δ/thr':>8s} "
          f"{'marge(thr)':>11s} {'marge(σ)':>9s}")
    for r in rows:
        dth = r['delta'] / r['theta'] if r['theta'] else float('nan')
        dthr = r['delta'] / r['thr'] if r['thr'] else float('nan')
        ms = f"{r['marge_sigma']:8.2f}" if r['marge_sigma'] is not None else "      n/a"
        print(f"{r['id']:34s} {r['verdict']:3s} {dth:9.3f} {dthr:8.3f} "
              f"{r['marge_thr']:11.4g} {ms}")
    with open("marge_verdicts.json", "w", encoding="utf-8") as f:
        json.dump(rows, f, ensure_ascii=False, indent=1)
    print("\n-> marge_verdicts.json")


if __name__ == "__main__":
    main()
