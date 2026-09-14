"""CAMPAGNE A3 — 5e paquet : unités naturelles (ℏ = c = k_B = 1).

La question du catalogue (A3) : l'invariance des verdicts tient-elle
hors HL/Gauss/SI/1 ? Deux vérifications :

1. LICCITÉ — chaque dimension du registre s'exprime en unités
   naturelles (puissances de l'eV). NAT_MAP ci-dessous est déclarée
   dans le script, pas gelée : c'est une sonde d'exploration.
2. MOTS — à μ gelés, le δ est identique quel que soit le paquet ; la
   re-décision au seuil calibré du contact doit donc rendre le mot
   home pour les 46 contacts. L'invariance n'est pas une propriété
   empirique de la machine : elle est architecturale (le paquet n'est
   jamais dans l'arithmétique, seulement dans la garde de dimension).

Subtilité EM consignée : en unités naturelles, le Debye devient
e·eV⁻¹ — la convention EM n'est pas supprimée, elle est déplacée
(la charge devient √4πα). NAT_MAP le note, ne le résout pas.

Sans toucher au cœur : PACKETS reste ("hl", "gauss", "si", "1") —
les gels « 4 paquets » des tests sont intacts. La sonde naturelle est
un UnitSystem existant (packet="hl", hbar=1, c=1, vintage déclaré) :
les unités naturelles sont un membre déclaré de la famille HL, pas un
cinquième paquet à enregistrer.

Campagne dérivée : aucun contact nouveau, aucun gel touché.
"""

from __future__ import annotations

import json

from mvcg.metrics import _adc, _delta
from mvcg.registers import CONTACTS, run_contact
from mvcg.rationalization import UnitSystem
from mvcg.verdict_register import _thr_contact

# Sonde d'unités naturelles : ℏ = c = 1 (k_B absorbé par définition des
# températures en énergie). Constructeur existant, vintage déclaré.
NAT_PROBE = UnitSystem(
    packet="hl",
    vintage="nat-A3-2026-09-14",
    hbar=1.0,
    c=1.0,
    note="unités naturelles ℏ=c=1 ; k_B absorbé (T en énergie)",
)

# Déclaration d'exploration (non gelée) : dimension → (expression en
# eV, convention). "e" = charge conservée comme unité (α en facteur).
NAT_MAP: dict[str, tuple[str, str]] = {
    "eV": ("eV", "l'énergie est la dimension native"),
    "Ha": ("eV (× 27,2114)", "Hartree = énergie atomique, convertie par e"),
    "cm^-1": ("eV (× hc)", "nombre d'onde → énergie via hc gelé"),
    "D": ("e·eV⁻¹", "dipôle = charge × longueur ; convention EM déplacée, pas supprimée"),
    "Hz": ("eV (× h)", "fréquence → énergie via h"),
    "m/s": ("1", "vitesse = 1/c : sans dimension en unités naturelles"),
    "nK": ("eV (× k_B)", "température → énergie via k_B"),
    "um": ("eV⁻¹", "longueur = 1/énergie"),
    "J m^-3 K^-2": ("eV⁴", "γ = densité d'énergie / T² → eV⁴"),
    "mag": ("1", "le magnitude est un rapport logarithmique : sans dimension"),
    "1": ("1", "sans dimension"),
    "1e-11": ("1", "sans dimension (échelle g-2, unité Δa_μ)"),
}


def main() -> None:
    rows = []
    for c in CONTACTS:
        r = run_contact(c)
        mapped = c.dimension in NAT_MAP
        if not mapped:
            rows.append({"id": c.id, "dimension": c.dimension,
                         "nat_licite": False, "mot_identique": None})
            continue
        delta = _delta(float(r["mu_loc"]), float(r["mu_ref"]), c.delta_kind)
        g = (r.get("extra") or {}).get("gum")
        thr, _ = _thr_contact(float(c.theta), g)
        mot = _adc(delta, thr)
        rows.append({
            "id": c.id,
            "dimension": c.dimension,
            "nat_licite": True,
            "nat_expression": NAT_MAP[c.dimension][0],
            "mot_home": r["verdict"],
            "mot_nat": mot,
            "mot_identique": mot == r["verdict"],
        })

    n = len(rows)
    licites = sum(1 for r in rows if r["nat_licite"])
    identiques = sum(1 for r in rows if r["mot_identique"])
    dims = {r["dimension"] for r in rows}
    print(f"contacts balayés        : {n}")
    print(f"licites en unités nat.  : {licites}/{n}")
    print(f"mots identiques au home : {identiques}/{n}")
    print(f"dimensions couvertes    : {len(dims)} "
          f"({', '.join(sorted(dims))})")
    non_licites = [r["id"] for r in rows if not r["nat_licite"]]
    if non_licites:
        print("NON licites :", non_licites)
    differents = [r["id"] for r in rows if r["mot_identique"] is False]
    if differents:
        print("mots DIFFERENTS :", differents)

    out = {
        "protocole": "MVC-G-A3-NAT-0.1",
        "probe": {"packet": NAT_PROBE.packet, "vintage": NAT_PROBE.vintage,
                  "hbar": NAT_PROBE.hbar, "c": NAT_PROBE.c,
                  "note": NAT_PROBE.note},
        "nat_map": {k: {"expr": v[0], "convention": v[1]}
                    for k, v in NAT_MAP.items()},
        "n": n, "licites": licites, "mots_identiques": identiques,
        "rows": rows,
        "lecture": ("invariance architecturale : le paquet n'entre jamais "
                    "dans l'arithmétique (μ gelés), seulement dans la garde "
                    "de dimension ; A2 a montré l'arithmétique propre à "
                    "5.6e-17, A3 montre la garde généralisable au 5e système"),
    }
    with open("a3_unites_naturelles.json", "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("\n-> a3_unites_naturelles.json")


if __name__ == "__main__":
    main()
