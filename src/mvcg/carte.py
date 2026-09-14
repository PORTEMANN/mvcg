#!/usr/bin/env python3
"""Carte des verdicts — la mémoire de la machine, dérivée, jamais dessinée.

Deux vues, toutes deux générées depuis le registre au moment de
l'exécution (épistémologie du casier : une carte dérivée ne ment pas).

`principale` — les deux coordonnées natives de la machine :
    x = θ gelé (l'étalonnage du contact, abs ou rel),
    y = δ/θ (la tension mesurée, en unités de seuil).
Les bandes horizontales δ/θ = 1 et δ/θ = 2 SONT la règle de verdict :
la zone sous 1 est celle du S+, entre 1 et 2 celle du P, au-dessus de
2 celle du S−. Un point proche d'une bande = un verdict au tranchant ;
un point loin = un mot sans suspense. Forme = domaine (micro/meso/macro),
couleur = mot réel.

`identite` — la carte de profil : 44 cases colorisées par verdict,
groupées par famille. Pour un regard étranger, pas pour un opérateur.

Couche d'épaisseur (campagne MARGE, 2026-09-14) : partout où un
budget GUM est gelé, la marge en σ (distance à la frontière de
bascule, `marge_adc`) est encodée — taille des pastilles sur la carte
principale, case pâlie vers le blanc sur la carte d'identité. Les
contacts sans budget GUM gardent taille/opacité neutres : la couche
ne montre que ce qui est déclaré, jamais une épaisseur inventée.

Couche de position (chantier SERRAGE, campagnes 1-3, 2026-09-14) :
l'opacité des pastilles encode la position dans la zone de verdict —
pâle = collé à la frontière (verdict fragile), plein = profond dans la
zone (verdict franc). Dérivée du même δ que les campagnes, sans les
réimporter :
    S+ : p = min(1, log2(θ/δ)/3)      (3 octaves de marge saturent)
    P  : p = clip(log2(δ/θ), 0, 1)    (pos_bande, campagne 2)
    S− : p = min(1, max(0, log2(δ/2θ))/2)
                                      (pos_rouge linéarisé, campagne 3)
Même sémantique de pâleur que la carte d'identité. La couleur du mot
reste pleine dans le SVG (l'opacité est un attribut séparé) : le test
de dérivation par comptage des couleurs est inchangé.

Limite déclarée : un point ne montre pas sa fibre (unités) — la fibre
est dans le classement figé, pas dans cette carte.
"""

from __future__ import annotations

import math
from pathlib import Path
from typing import Any

from mvcg.casier import family_of
from mvcg.metrics import marge_adc
from mvcg.registers import run_registers
from mvcg.tables import ROOT
from mvcg.verdict_register import _thr_contact

OUT = ROOT / "docs"

# Matplotlib écrit un horodatage dc:date dans le SVG — une carte
# dérivée ne vieillit pas : on le neutralise pour que régénérer =
# mêmes octets (propriété figée par le test).
def _strip_dc_date(path: Path) -> None:
    import re

    raw = path.read_text(encoding="utf-8")
    raw = re.sub(r"<dc:date>.*?</dc:date>\s*", "", raw)
    path.write_text(raw, encoding="utf-8")

COLORS = {"S+": "#2e8b57", "P": "#d4a017", "S-": "#b22222"}
MARKERS = {"micro": "o", "meso": "^", "macro": "s"}

# Contacts annotés sur la carte principale : les deux H0 (chantier du
# jour) et la paire WP25/WP20 (doctrine de la paire).
ANNOTATE = {
    "H0_Ecart_Planck_SH0ES",
    "H0_Hz_SNe_LOWZ_DEMO",
    "AMU_Delta_WP25",
    "AMU_exp_minus_WP20",
    "KSS_EtaS_QGP",
    "Landau_Vc_He4",
}


def _rows() -> list[dict[str, Any]]:
    return run_registers()["rows"]


def _marge_sigma(r: dict[str, Any]) -> float | None:
    """Marge du verdict en σ (u_c GUM gelé), ou None sans budget déclaré.

    Le seuil de décision est celui du contact (_thr_contact, partagé
    avec le sweep calibré) — une seule définition d'étalonnage.
    """
    g = ((r.get("extra") or {}).get("gum")) or {}
    uc = g.get("uc")
    if not uc or uc <= 0:
        return None
    thr, _ = _thr_contact(float(r["theta"]), g)
    return marge_adc(float(r["delta"]), thr, r["verdict"]) / float(uc)


def _position_zone(r: dict[str, Any]) -> float:
    """Position dans la zone de verdict, p ∈ [0,1] — couche SERRAGE.

    0 = collé à la frontière (verdict fragile), 1 = profond (franc).
    Dérivée du δ du registre ; les campagnes 1-3 en sont la mesure
    détaillée, cette fonction en est l'encodage cartographique.
    """
    delta, theta = float(r["delta"]), float(r["theta"])
    if theta <= 0:
        return 1.0
    v = r["verdict"]
    if v == "S+":
        if delta <= 0:
            return 1.0
        return max(0.0, min(1.0, math.log2(theta / delta) / 3.0))
    if v == "P":
        return max(0.0, min(1.0, math.log2(delta / theta)))
    return max(0.0, min(1.0, math.log2(delta / (2.0 * theta)) / 2.0))


def _taille_pastille(marge_sig: float | None) -> float:
    """Carte principale : 30 + 70·log10(1+marge)/1, borné à 100.

    Pastille fine = verdict mince ; neutre (52) sans budget GUM.
    """
    if marge_sig is None:
        return 52.0
    return 30.0 + 70.0 * min(1.0, math.log10(1.0 + marge_sig))


def _case_palee(couleur: str, marge_sig: float | None) -> str:
    """Carte identité : la case est pâlie vers le blanc quand le verdict
    est mince — alpha = 0,30 + 0,70·min(1, marge/2). Couleur pleine
    sans budget GUM. Blend explicite en hex (pas de rgba) pour rester
    dérivé et déterministe."""
    if marge_sig is None:
        return couleur
    alpha = 0.30 + 0.70 * min(1.0, marge_sig / 2.0)
    rv, gv, bv = (int(couleur[i : i + 2], 16) for i in (1, 3, 5))
    return "#{:02x}{:02x}{:02x}".format(
        round(alpha * rv + (1.0 - alpha) * 255),
        round(alpha * gv + (1.0 - alpha) * 255),
        round(alpha * bv + (1.0 - alpha) * 255),
    )


def carte_principale(path: Path) -> dict[str, Any]:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    matplotlib.rcParams["svg.hashsalt"] = "mvcg-carte"
    rows = _rows()
    fig, ax = plt.subplots(figsize=(9, 6))

    # Zones de la règle de verdict (log en y : bandes = lignes).
    ax.axhline(1.0, color="#666666", lw=0.8, ls="--")
    ax.axhline(2.0, color="#666666", lw=0.8, ls="--")
    ax.fill_between([1e-5, 1e3], 0.05, 1.0, color="#2e8b57", alpha=0.06)
    ax.fill_between([1e-5, 1e3], 1.0, 2.0, color="#d4a017", alpha=0.08)
    ax.fill_between([1e-5, 1e3], 2.0, 5e2, color="#b22222", alpha=0.06)
    ax.text(1.6e-5, 0.55, "zone S+", color="#2e8b57", fontsize=8)
    ax.text(1.6e-5, 1.35, "zone P", color="#8a6d0b", fontsize=8)
    ax.text(1.6e-5, 2.6, "zone S-", color="#b22222", fontsize=8)

    for r in rows:
        x, y = r["theta"], r["delta"] / r["theta"]
        ax.scatter(
            x, y,
            marker=MARKERS.get(r["register"], "o"),
            c=COLORS[r["verdict"]],
            alpha=0.35 + 0.65 * _position_zone(r),
            s=_taille_pastille(_marge_sigma(r)), zorder=3,
            edgecolors="white", linewidths=0.6,
        )
    for r in rows:
        if r["id"] in ANNOTATE:
            x, y = r["theta"], r["delta"] / r["theta"]
            label = r["id"].replace("_", " ")
            ax.annotate(
                label, (x, y), textcoords="offset points", xytext=(7, 5),
                fontsize=7, color="#333333",
            )

    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("θ gelé (l'étalonnage du contact — abs et rel mélangés, log)")
    ax.set_ylabel("δ/θ (la tension, en unités de seuil — log)")
    ax.set_title(
        f"MVC-G — {len(rows)} verdicts : chaque point est une pesée, les bandes sont la règle\n"
        "○ micro  △ meso  □ macro — vert S+  ambre P  rouge S− — "
        "pastille fine = verdict mince (marge en σ, budget GUM) — "
        "pastille pâle = collé à la frontière (position dans la zone)"
    )
    ax.set_xlim(1e-5, 1e3)
    ax.set_ylim(0.05, 5e2)
    ax.grid(True, which="both", lw=0.2, color="#cccccc", alpha=0.5)
    fig.tight_layout()
    fmt = Path(path).suffix.lstrip(".") or "svg"
    fig.savefig(path, format=fmt, bbox_inches="tight")
    plt.close(fig)
    if fmt == "svg":
        _strip_dc_date(Path(path))
    return {"carte": "principale", "out": str(path), "n": len(rows)}


def carte_identite(path: Path) -> dict[str, Any]:
    """La carte de profil : cases colorisées par verdict, groupées par famille."""
    rows = _rows()
    fams: dict[str, list[dict[str, Any]]] = {}
    for r in rows:
        fams.setdefault(family_of(r["id"]), []).append(r)

    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    matplotlib.rcParams["svg.hashsalt"] = "mvcg-carte-identite"
    cell = 0.32
    gap_fam = 0.75
    width = max(7.0, sum(len(v) * cell + gap_fam for v in fams.values()))
    fig, ax = plt.subplots(figsize=(width, 1.9))
    x = 0.0
    for fam in sorted(fams):
        for r in fams[fam]:
            ax.add_patch(plt.Rectangle((x, 0.3), cell * 0.9, cell * 0.9,
                                       color=_case_palee(COLORS[r["verdict"]],
                                                         _marge_sigma(r))))
            x += cell
        ax.text(x - len(fams[fam]) * cell / 2, 0.12, fam,
                ha="right", rotation=25, fontsize=7, color="#444444")
        x += gap_fam
    ax.set_xlim(-0.1, x)
    ax.set_ylim(-0.15, 0.75)
    ax.axis("off")
    ax.set_title(
        f"MVC-G — {len(rows)} verdicts : vert S+ · ambre P · rouge S− — "
        "case pâle = verdict mince (< 2σ de sa frontière, budget GUM)",
        fontsize=10,
    )
    fmt = Path(path).suffix.lstrip(".") or "svg"
    fig.savefig(path, format=fmt, bbox_inches="tight")
    plt.close(fig)
    if fmt == "svg":
        _strip_dc_date(Path(path))
    return {"carte": "identite", "out": str(path), "n": len(rows)}


def main_carte(kind: str, out: Path | None = None) -> dict[str, Any]:
    if kind == "principale":
        return carte_principale(Path(out) if out else OUT / "carte-verdicts.svg")
    if kind == "identite":
        return carte_identite(Path(out) if out else OUT / "carte-identite.svg")
    raise ValueError(f"carte inconnue: {kind} (principale|identite)")
