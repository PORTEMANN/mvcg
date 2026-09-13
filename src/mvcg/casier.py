#!/usr/bin/env python3
"""Casier de D — la carte des modes fonctionnels de la machine.

Un mode = un dossier D (règle, θ, table, fibre). Changer D, changer de
mode : le casier dit quels D existent et quels D ne sont encore que des
étiquettes. Les cartes « pesé » sont DÉRIVÉES du registre — jamais
déclarées : une étiquette ne ment pas, par construction. Les cartes
« sans μ » sont des modes possibles en attente d'extrait ; elles ne
pèsent rien et ne doivent rien afficher.
"""

from __future__ import annotations

from typing import Any

from mvcg.registers import run_registers

# Modes possibles, en attente d'extrait déclaré. « sans μ » = étiquette.
CANDIDATES: list[dict[str, Any]] = [
    {"id": "H0_Hz_SNe", "family": "cosmo", "s": "H(z) = donnee SNe",
     "note": "sans μ"},
    {"id": "HVP_CMD3_vs_KLOE", "family": "g-2", "s": "sigma_pipi CMD-3=KLOE",
     "note": "sans μ"},
    {"id": "QCD_fplus_K", "family": "QCD", "s": "f_+(0) A=B",
     "note": "sans μ"},
    {"id": "KNIGHT_K", "family": "NMR", "s": "K=K_table",
     "note": "sans μ"},
    {"id": "NMR_delta_ppm", "family": "NMR", "s": "delta=delta_table",
     "note": "sans μ"},
]

_FAMILY_RULES = [
    ("BEC", "BEC"), ("Carbon", "carbone/spectro"), ("TK_", "carbone/spectro"),
    ("CO2", "molécule/spectro"), ("PMMA", "polymère/spectro"),
    ("H2_Harmonique", "molécule/vibration"), ("H2O", "molécule"),
    ("Cu_Gamma", "solide"), ("Grille_H1s", "atome/grille"),
    ("H1s", "atome"), ("H2plus", "atome"), ("He_", "atome"),
    ("Kato", "atome"), ("FRW", "cosmo"), ("H0_", "cosmo"),
    ("AMU", "g-2"), ("dice", "imagerie"), ("DIRAC", "unités"),
    ("Dirac", "unités"), ("F22", "unités"), ("F30", "unités"),
    ("Karplus", "NMR"), ("CKM", "CKM"), ("HVP", "g-2"), ("HLbL", "g-2"),
    ("Landau", "hyperfluidité"), ("Bertsch", "hyperfluidité"),
]


def family_of(row_id: str) -> str:
    for key, fam in _FAMILY_RULES:
        if key in row_id:
            return fam
    return "divers"


def cards() -> list[dict[str, Any]]:
    """Cartes « pesé » dérivées du registre + candidats « sans μ »."""
    rows = run_registers()["rows"]
    weighed = [
        {
            "id": r["id"],
            "family": family_of(r["id"]),
            "s": r["s"],
            "note": "pesé",
            "verdict": r["verdict"],
            "campaign": r.get("campaign"),
        }
        for r in rows
    ]
    return weighed + [dict(c) for c in CANDIDATES]


def modules() -> list[str]:
    return [
        "casier",
        "registers",
        "dictionaries",
        "spectro_air",
        "hitran_extract",
        "h2plus",
        "verdict_register",
        "archive",
        "gum",
        "rationalization",
    ]


def index() -> dict[str, Any]:
    return {
        "protocol": "MVC-G-CASIER-0.2",
        "warning": "un D par carte ; pas de score SM ; sans μ = étiquette ; pesé dérivé du registre",
        "cards": cards(),
        "modules": modules(),
    }
