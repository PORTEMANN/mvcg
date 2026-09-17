#!/usr/bin/env python3
"""Chantier TRANSVERSALE — pesées croisées issues de la fouille transversale.

Protocole : docs/PROSPECTIVE-FOUILLE-TRANSVERSALE.md (2026-09-16). La
machine pèse des déclarations chiffrées du corpus repérées hors des
chantiers déjà ouverts (LOI-HARMONIQUE, PRINCIPES, E44) : vieux articles
(2022), séries éparses, index de l'écosystème. Tables gelées datées,
zéro fetch. Emprunts CODATA-2018 / PDG-2024 écrits en source des tables
(grammaire PF1b — l'emprunt est un acte curatorial, pas une correction
en silence).
"""

from __future__ import annotations

from typing import Any

from mvcg.tables import load_table


def tr_davies_trio() -> tuple[float, dict[str, Any]]:
    """Trio mésonique de Paul Davies (article « La Constante ALPHA », 2022).

    Déclaration gelée : « les masses du muon, du pion et du kaon valent
    presque exactement 3/2 x 1/alpha, 2 x 1/alpha et 7 x 1/alpha fois la
    masse de l'electron ». mu_loc = écart relatif maximal des trois
    rapports mesurés (PDG-2024 gelé) sur déclarés (alpha 137,036 gelée
    verbatim), theta abs gelé 0,01 = calibration déclarée de « presque
    exactement ». Extras : écarts par ligne, tensions des variantes
    neutres (le corpus ne tranche pas ±/0 — dette nommée), voisinage
    déclaré avec LH_Muon_Quinte (même loi, source CTFT 2026).
    """
    t = load_table("tr_davies_trio_LITTERATURE-2022.json")
    p = t["params"]
    alpha_inv = float(p["alpha_inv_declaree"])
    m_e = float(p["m_e_MeV"])
    deltas: dict[str, float] = {}
    ratios: dict[str, float] = {}
    declares: dict[str, float] = {}
    for nom, coeff, m_mes in p["rows_chargees"]:
        decl = float(coeff) * alpha_inv
        mes = float(m_mes) / m_e
        declares[nom] = decl
        ratios[nom] = mes
        deltas[nom] = abs(mes / decl - 1.0)
    mu_loc = float(max(deltas.values()))
    neutres = {}
    for nom, m_n in p["m_neutres_MeV"].items():
        coeff = 2.0 if nom == "pion0" else 7.0
        decl = coeff * alpha_inv
        mes = float(m_n) / m_e
        neutres[nom] = {"declare": decl, "mesure": mes, "delta": abs(mes / decl - 1.0)}
    return mu_loc, {
        "table": t["vintage"],
        "table_sha256": t["_sha256"],
        "alpha_inv_declaree": alpha_inv,
        "ecarts_relatifs": deltas,
        "rapports_declares": declares,
        "rapports_mesures": ratios,
        "pire_ligne": max(deltas, key=deltas.get),
        "neutres": neutres,
        "note": "le trio chargé tient à 0,34-0,71 % (pire : kaon) — « presque exactement » vérifié au theta 1 % gelé ; les variantes neutres cassent (pion0 3,6 %, K0 1,5 %) : le corpus ne tranche pas ±/0, dette nommée arbitrée par la variante chargée, la seule qui tienne ; la ligne muon échole à LH_Muon_Quinte (CTFT, S+ 0,059 theta) — l'information nouvelle ici est la structure de trio et la tension des neutres ; alpha CODATA-2018 (137,035999084) déplace les déclarés de ~7e-9 relatif, sans effet sur les verdicts",
    }


def tr_b11_liaison() -> tuple[float, dict[str, Any]]:
    """« Pour 11B on a Elie/A = 6,8 MeV » (article k(Z,N), 2025).

    Déclaration semi-empirique : modèle deltashell « ajusté pour Z=5 »
    (calibration nommée dans le texte, dette nommée — pas ab initio).
    mu_loc = écart relatif de B/A NUBASE2020 gelé sur déclaré, theta abs
    gelé 0,02 = tolérance de déclaration à deux chiffres significatifs
    (6,8 arrondit 6,93 à 2 % près). Extras : B totale, écart, rappel que
    l'incertitude NUBASE (12 eV sur Δ) est sans effet au ppm près.
    """
    t = load_table("tr_b11_liaison_LITTERATURE-2025.json")
    p = t["params"]
    u = float(p["u_MeV"])
    m_h = float(p["m_H_u"]) * u
    m_n = float(p["m_n_u"]) * u
    A = int(p["A"])
    Z = int(p["Z"])
    N = int(p["N"])
    M = A * u + float(p["exces_masse_MeV"])
    B = Z * m_h + N * m_n - M
    ba = B / A
    decl = float(p["BA_declare_MeV"])
    return abs(ba / decl - 1.0), {
        "table": t["vintage"],
        "table_sha256": t["_sha256"],
        "BA_NUBASE2020_MeV": ba,
        "B_totale_MeV": B,
        "BA_declare_MeV": decl,
        "ecart_relatif": abs(ba / decl - 1.0),
        "note": "B/A(11B) = 6,927732 MeV (NUBASE2020 gelé) vs 6,8 déclaré (« deltashell ajusté pour Z=5 ») : écart 1,878 % — le « ajusté » est nommé par le corpus, la machine pèse le résidu du calage ; theta 2 % gelé = tolérance de déclaration semi-empirique à un chiffre significatif près (6,8 arrondit 6,93 à 2 % près) ; incertitude NUBASE sur Δ (12 eV) sans effet au ppm près",
    }


def tr_sn132_liaison() -> tuple[float, dict[str, Any]]:
    """« 132Sn favorisé car 8,40 > 8,35 » (article k(Z,N), 2025).

    Déclaration à deux colonnes : deux énergies de liaison par nucléon
    déclarées (8,40 et 8,35 MeV) plus une inégalité (132Sn > 133Sn).
    mu_loc = écart relatif maximal des deux B/A NUBASE2020 gelés sur
    déclarés, theta abs gelé 0,02 (même calibration que B11, même
    article). Extras : l'inégalité déclarée vérifiée côté NUBASE2020
    (le neutron de 133Sn part de la couche magique N=82), écart par
    colonne.
    """
    t = load_table("tr_sn132_liaison_LITTERATURE-2025.json")
    p = t["params"]
    u = float(p["u_MeV"])
    m_h = float(p["m_H_u"]) * u
    m_n = float(p["m_n_u"]) * u
    resultats: dict[str, dict[str, float]] = {}
    for nom, A, Z, d_meV, _d_kev, decl in p["rows"]:
        A = int(A)
        Z = int(Z)
        N = A - Z
        M = A * u + float(d_meV)
        ba = (Z * m_h + N * m_n - M) / A
        resultats[nom] = {
            "BA_NUBASE2020_MeV": ba,
            "BA_declare_MeV": float(decl),
            "ecart_relatif": abs(ba / float(decl) - 1.0),
        }
    mu_loc = float(max(r["ecart_relatif"] for r in resultats.values()))
    return mu_loc, {
        "table": t["vintage"],
        "table_sha256": t["_sha256"],
        "lignes": resultats,
        "inegalite_declaree": "B/A(132Sn) > B/A(133Sn)",
        "inegalite_NUBASE2020": resultats["132Sn"]["BA_NUBASE2020_MeV"] > resultats["133Sn"]["BA_NUBASE2020_MeV"],
        "pire_ligne": max(resultats, key=lambda k: resultats[k]["ecart_relatif"]),
        "note": "B/A(132Sn) = 8,354873 MeV vs 8,40 déclaré (écart 0,537 %) et B/A(133Sn) = 8,310089 MeV vs 8,35 déclé (0,478 %) ; l'inégalité « 132Sn favorisé » est vraie côté NUBASE2020 : le 133e neutron quitte la couche magique N=82 et est moins lié de 45 keV/nucléon — la physique déclarée (magie neutronique) tient, les valeurs arrondies à 2 chiffres tiennent à 0,54 % près ; même modèle deltashell ajusté que le contact B11 (article unique, calibration theta 2 % partagée)",
    }


def tr_alpha_proton_muon() -> tuple[float, dict[str, Any]]:
    """« 1800 fois, donc 9 fois » (article « La Constante ALPHA », 2022).

    Trois déclarations enchaînées : m_mu/m_e = 200, m_p/m_e = 1800, et
    « donc » m_p/m_mu = 9. mu_loc = écart relatif maximal des trois
    rapports mesurés (PDG-2024 gelé) sur déclarés, theta abs gelé 0,01
    (même calibration que TR_Davies_TrioMesons — article unique).
    Extras : écart par ligne, l'inférence interne 1800/200 = 9 (exacte —
    l'erreur des prémisses se transmet à la conclusion), le rappel que
    les nombres ronds de vulgarisation ne déclarent pas de tolérance
    (dette nommée).
    """
    t = load_table("tr_proton_muon_LITTERATURE-2022.json")
    p = t["params"]
    mesures = {
        "muon/electron": float(p["m_mu_MeV"]) / float(p["m_e_MeV"]),
        "proton/electron": float(p["m_p_MeV"]) / float(p["m_e_MeV"]),
        "proton/muon": float(p["m_p_MeV"]) / float(p["m_mu_MeV"]),
    }
    deltas: dict[str, float] = {}
    declares: dict[str, float] = {}
    for nom, decl in p["declarations"]:
        declares[nom] = float(decl)
        deltas[nom] = abs(mesures[nom] / float(decl) - 1.0)
    mu_loc = float(max(deltas.values()))
    return mu_loc, {
        "table": t["vintage"],
        "table_sha256": t["_sha256"],
        "ecarts_relatifs": deltas,
        "rapports_declares": declares,
        "rapports_mesures": mesures,
        "pire_ligne": max(deltas, key=deltas.get),
        "inference_interne": declares["proton/electron"] / declares["muon/electron"],
        "note": "l'inférence du corpus (1800/200 = 9) est arithmétiquement exacte — l'erreur ne vient pas du « donc » mais des prémisses rondes : le muon à 206,768 mesuré viole le « 200 » à 3,38 % (pire ligne), le proton « 1800 » à 2,01 %, et la conclusion « 9 » hérite de 1,33 % ; nombres ronds de vulgarisation sans tolérance déclarée (dette nommée) pesés au theta 1 % de cohérence avec le trio de Davies, même article",
    }
