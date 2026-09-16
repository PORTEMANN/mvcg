#!/usr/bin/env python3
"""Chantier E44 — nucléation de l'enlacement : pesée des déclarations.

Note d'audit E44 (31/07/2026, protocole pré-enregistré C12.1, haché
SHA-256 avant calcul) : la machine ne rejoue pas la simulation GP — elle
pèse les déclarations gelées de la note et leur arithmétique interne,
comme PF7 pèse l'arithmétique du tableau publié. Table gelée datée :
e44_LITTERATURE-2026.json (transcription verbatim, copie de travail de
la note dans le workspace).
"""

from __future__ import annotations

from typing import Any

from mvcg.tables import load_table


def e44_t0_lien() -> tuple[float, dict[str, Any]]:
    """Validation T0 du détecteur d'enlacement (déclarée par la note).

    Lien de Hopf contrôlé : Lk = +0,994 déclaré (attendu ±1) ; témoin
    non lié : Lk = +0,007 déclaré (attendu 0). mu_loc = Lk du lien
    déclaré, mu_ref = 1 (attendu). Extras : écart du lien, écart du
    témoin — le détecteur se valide à 0,6 % et 0,7 % près déclarés.
    """
    t = load_table("e44_LITTERATURE-2026.json")
    p = t["params"]
    lk = float(p["lk_t0_lien"])
    temoin = float(p["lk_t0_temoin"])
    attendu = float(p["lk_t0_attendu"])
    return float(lk), {
        "table": t["vintage"],
        "table_sha256": t["_sha256"],
        "lk_lien": lk,
        "lk_attendu": attendu,
        "ecart_lien": abs(lk - attendu),
        "lk_temoin": temoin,
        "ecart_temoin": abs(temoin - float(p["lk_t0_temoin_attendu"])),
        "note": "validation T0 déclarée : lien Lk = 0,994 vs attendu ±1 (écart 0,6 %), témoin non lié Lk = 0,007 vs attendu 0 — le détecteur se valide avant tout calcul sur les runs",
    }


def e44_lk_paire() -> tuple[float, dict[str, Any]]:
    """L'événement central : la paire de Hopf du run A/440103 (t = 12).

    Trois estimations indépendantes du nombre de Gauss déclarées :
    −1,041 (image minimale), −0,967 (brut), −1,004 (appariement
    alternatif) ; seuil de détection |Lk| ≥ 0,5. mu_loc = |moyenne des
    trois estimations| = 1,004, mu_ref = 1 (lien de Hopf unitaire).
    Extras : spread des trois estimations (0,074), les trois passent le
    seuil déclaré — la robustesse déclarée « à trois estimations » se
    vérifie sur les nombres gelés.
    """
    t = load_table("e44_LITTERATURE-2026.json")
    p = t["params"]
    ests = [float(p["lk_image_minimale"]), float(p["lk_brut"]),
            float(p["lk_appariement_alt"])]
    moy = sum(ests) / len(ests)
    spread = max(ests) - min(ests)
    seuil = float(p["lk_seuil_detection"])
    return float(abs(moy)), {
        "table": t["vintage"],
        "table_sha256": t["_sha256"],
        "estimations": ests,
        "moyenne": moy,
        "mu_loc_abs": abs(moy),
        "spread": spread,
        "seuil_detection": seuil,
        "n_passent_seuil": sum(1 for e in ests if abs(e) >= seuil),
        "distance_minimale_mailles": float(p["distance_minimale_mailles"]),
        "note": "trois estimations déclarées dont la moyenne vaut −1,004 (écart 0,4 % du lien unitaire), spread 0,074, les trois passent le seuil |Lk| ≥ 0,5 déclaré — la robustesse annoncée tient sur les nombres gelés ; distance minimale 3,16 mailles déclarée (pas de contact numérique)",
    }


def e44_p3_filaments() -> tuple[float, dict[str, Any]]:
    """P3 réfutée : la médiane des filaments axiaux vs la prédiction.

    Prédiction pré-enregistrée : filaments axiaux 4 ± 2 (circulation
    imposée) ; résultat déclaré : médiane 14, étendue 9–19 (ensemble B).
    mu_loc = médiane déclarée 14, mu_ref = prédiction déclarée 4 —
    l'écart porté tel que déclaré, en σ de la prédiction : (14 − 4)/2 =
    5 σ. Le corpus statue « réfutée » : attendu S− tenu.
    """
    t = load_table("e44_LITTERATURE-2026.json")
    p = t["params"]
    med = float(p["p3_mediane"])
    pred = float(p["p3_prediction"])
    sig = float(p["p3_sigma_prediction"])
    return float(med), {
        "table": t["vintage"],
        "table_sha256": t["_sha256"],
        "mediane": med,
        "etendue": list(p["p3_etendue"]),
        "prediction": pred,
        "sigma_prediction": sig,
        "ecart_sigma": (med - pred) / sig,
        "note": "médiane déclarée 14 (étendue 9–19) vs prédiction pré-enregistrée 4 ± 2 : écart 5 σ — la note statue « réfutée » et la machine confirme le mot sur les nombres gelés (l'ordre d'Abrikosov ne se cristallise pas à cette échelle)",
    }
