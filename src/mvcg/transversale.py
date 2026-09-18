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

import math
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


def tr_kzn_grille() -> tuple[float, dict[str, Any]]:
    """Pesée systémique du modèle k(Z,N) vs NUBASE2020 (chantier B1).

    Le corpus revendique un gain computationnel jusqu'à 10⁵ vs DFT ; la
    machine mesure le prix en justesse : le modèle transcrit (formule
    complète + paramètres recalibrés gelés depuis l'image « Equations et
    calibrage ») est évalué sur les 235 noyaux stables du domaine déclaré
    (12 ≤ A ≤ 200, grille NUBASE2020 gelée). mu_loc = écart relatif RMS
    modèle-vs-NUBASE sur la grille, theta abs gelé 0,02 = même
    calibration « déclaration à deux chiffres » que TR_KZN_B11_Liaison
    et TR_KZN_Sn132_Preference (article unique, exemples chiffrés à
    2-3 chiffres). Extras : écart max, médiane, pire noyau, nombre de
    lignes dans ±2 θ, les deux exemples déclarés du corpus recomputés
    par son propre modèle (6,8 et 8,40/8,35 — le modèle ne se reproduit
    pas lui-même), la sensibilité pairing (le signe ± non déclaré).
    """
    tm = load_table("tr_kzn_modele_LITTERATURE-2025.json")
    tg = load_table("tr_kzn_grille_NUBASE2020.json")
    pm = tm["params"]
    pg = tg["params"]
    u = float(pg["u_MeV"])
    m_h = float(pg["m_H_u"]) * u
    m_n = float(pg["m_n_u"]) * u
    magics = [int(m) for m in pm["magics"]]
    s2 = float(pm["sigma2_couches"])

    def couches(z: int, n: int) -> float:
        return sum(math.exp(-(z - m) ** 2 / s2) for m in magics) + sum(
            math.exp(-(n - m) ** 2 / s2) for m in magics
        )

    def el_modele(z: int, n: int) -> float:
        a = z + n
        ac = float(pm["aC_MeV"]["Z<20"]) if z < 20 else float(pm["aC_MeV"]["Z>=20"])
        if a < 20:
            a_s = float(pm["aS_MeV"]["A<20"])
        elif a <= 100:
            a_s = float(pm["aS_MeV"]["20<=A<=100"])
        else:
            a_s = float(pm["aS_MeV"]["A>100"])
        k = (
            -ac * z**2 / a ** (4.0 / 3.0)
            - float(pm["aA_MeV"]) * ((n - z) / a) ** 2
            - a_s * a ** (-1.0 / 3.0)
            + float(pm["a_shell_MeV"]) * couches(z, n)
        )
        d_pair = float(pm["aP_MeV"]) / math.sqrt(a) if (z % 2 == 0 and n % 2 == 0) else 0.0
        return float(pm["pente"]) * k + float(pm["offset"]) + d_pair

    ecarts: list[float] = []
    pire = {"ecart": 0.0}
    n_dans_2pct = 0
    bandes: dict[str, list[float]] = {"A<20": [], "20<=A<=100": [], "A>100": []}
    for row in tg["grille"]:
        a, z, n = int(row["A"]), int(row["Z"]), int(row["N"])
        m = a * u + float(row["mex_keV"]) / 1000.0
        ba_nubase = (z * m_h + n * m_n - m) / a
        ba_modele = el_modele(z, n)
        e = ba_modele / ba_nubase - 1.0
        ecarts.append(e)
        bandes["A<20" if a < 20 else ("20<=A<=100" if a <= 100 else "A>100")].append(e)
        if abs(e) > abs(pire["ecart"]):
            pire = {"A": a, "Z": z, "N": n, "ecart": e,
                    "BA_modele": ba_modele, "BA_nubase": ba_nubase}
        if abs(e) <= 0.02:
            n_dans_2pct += 1
    rms = math.sqrt(sum(e**2 for e in ecarts) / len(ecarts))
    mediane = sorted(abs(e) for e in ecarts)[len(ecarts) // 2]
    # les deux exemples chiffrés du corpus recomputés par son propre modèle
    ex_corpus = {}
    for nom, z, n, decl in [("11B", 5, 6, 6.8), ("132Sn", 50, 82, 8.40), ("133Sn", 50, 83, 8.35)]:
        mod = el_modele(z, n)
        ex_corpus[nom] = {"modele": mod, "declare": decl, "ecart": abs(mod / decl - 1.0)}
    return float(rms), {
        "table_modele": tm["vintage"],
        "table_grille": tg["vintage"],
        "table_sha256": tm["_sha256"],
        "rms_relatif": rms,
        "max_relatif": max(abs(e) for e in ecarts),
        "mediane_relatif": mediane,
        "n_lignes": len(ecarts),
        "n_dans_2pct": n_dans_2pct,
        "pire_noyau": pire,
        "regimes": {
            nom: {
                "n": len(es),
                "rms_relatif": math.sqrt(sum(e**2 for e in es) / len(es)) if es else 0.0,
                "max_relatif": max((abs(e) for e in es), default=0.0),
            }
            for nom, es in bandes.items()
        },
        "exemples_corpus_recomputes": ex_corpus,
        "note": "le modèle linéarisé tel que transcrit donne un RMS de ~12 % sur son propre domaine déclaré (235 noyaux stables 12≤A≤200) — seulement quelques lignes tombent dans ±2 % ; le pire écart est en A=12-20 (surface/coupage mal calés à petite A) ; le modèle ne reproduit pas ses propres exemples publiés (6,8 vs 8,55 pour 11B ; 8,40/8,35 vs ~9,2-9,5 pour Sn) : la linéarisation globale aplatit la courbe B/A et la surestime presque partout au-dessus de A~30, la sous-estime à petite A — prix en justesse du facteur 10⁵ revendiqué ; dette pairing (signe ± non déclaré) : A pairs-pairs gelé +aP/√A, sinon 0",
    }


def _fusion_base() -> tuple[dict[str, Any], dict[str, Any]]:
    """Socle commun : liaisons D/T/⁴He, Q_DT et table comparaison gelées."""
    t = load_table("tr_kzn_fusion_LITTERATURE-2025.json")
    p = t["params"]
    u = float(p["u_MeV"])
    m_h = float(p["m_H_u"]) * u
    m_n = float(p["m_n_u"]) * u

    def b_liaison(a: int, z: int, mex_kev: float) -> float:
        return z * m_h + (a - z) * m_n - (a * u + mex_kev / 1000.0)

    liaisons = {}
    for nom, a, z, mex, decl in p["liaisons_declarees_MeV"]:
        b = b_liaison(int(a), int(z), float(mex))
        liaisons[nom] = {"nubase": b, "declare": float(decl), "ecart": abs(b / float(decl) - 1.0)}
    q_dt = liaisons["4He"]["nubase"] - liaisons["D"]["nubase"] - liaisons["T"]["nubase"]
    q_dt_ecart = abs(q_dt / float(p["Q_DT_declare_MeV"]) - 1.0)
    q_pb = 3.0 * liaisons["4He"]["nubase"] - b_liaison(11, 5, float(p["mex_annexes_keV"]["11B"]))
    q_dd_n = b_liaison(3, 2, float(p["mex_annexes_keV"]["3He"])) + b_liaison(1, 0, float(p["mex_annexes_keV"]["n"])) - 2.0 * liaisons["D"]["nubase"]
    q_dd_p = liaisons["T"]["nubase"] + b_liaison(1, 1, float(p["mex_annexes_keV"]["1H"])) - 2.0 * liaisons["D"]["nubase"]
    comparaison = {
        "D+T": {"nubase": q_dt, "declare": 17.6, "ecart": q_dt_ecart},
        "p+11B": {"nubase": q_pb, "declare": 8.7, "ecart": abs(q_pb / 8.7 - 1.0)},
    }
    return t, {
        "liaisons": liaisons,
        "q_dt": q_dt,
        "q_dt_ecart": q_dt_ecart,
        "comparaison": comparaison,
        "q_dd_n": q_dd_n,
        "q_dd_p": q_dd_p,
    }


def tr_kzn_fusion() -> tuple[float, dict[str, Any]]:
    """Énergies de liaison D/T/⁴He + Q-value D-T (image, 2025).

    Déclarations de l'image « Énergies de liaison » pesées sur NUBASE2020
    gelé. mu_loc = écart relatif maximal des trois liaisons et de la
    Q-value recompute, theta abs gelé 0,02 (calibration famille
    article). Première fournée k(Z,N) où le corpus tient — liaisons
    standard citées correctement (pire : D à 1,12 %, arrondi de
    vulgarisation). La table comparaison est le contact jumeau
    TR_KZN_TableComparaison ; la ligne D+D y est nommée (deux canaux
    non déclarés, dette) mais hors mu_loc ici aussi.
    """
    t, d = _fusion_base()
    p = t["params"]
    mu_loc = float(max(max(v["ecart"] for v in d["liaisons"].values()), d["q_dt_ecart"]))
    return mu_loc, {
        "table": t["vintage"],
        "table_sha256": t["_sha256"],
        "liaisons": d["liaisons"],
        "Q_DT": {"nubase": d["q_dt"], "declare": float(p["Q_DT_declare_MeV"]), "ecart": d["q_dt_ecart"]},
        "D+D_deux_canaux": {"3He+n": d["q_dd_n"], "T+p": d["q_dd_p"], "declare": 3.6,
                            "note": "deux canaux ouverts, corpus sans canal déclaré — dette nommée, hors mu_loc"},
        "pire_ligne": max(list(d["liaisons"].keys()) + ["Q_DT"],
                          key=lambda k: (d["liaisons"] | {"Q_DT": {"ecart": d["q_dt_ecart"]}})[k]["ecart"]),
        "note": "les liaisons D (2,2246 vs 2,2 déclaré), T (8,4818 vs 8,5), 4He (28,2957 vs 28,3) et la Q-value D-T (17,589 vs 17,6) tiennent à 1,2 % près (pire : D à 1,12 %, arrondi de vulgarisation à deux chiffres) ; première fournée du chantier où le corpus cite correctement des données standard",
    }


def tr_kzn_comparaison() -> tuple[float, dict[str, Any]]:
    """Table « Comparaison des Réactions » (image, 2025).

    Deux lignes sans ambiguïté de canal (D+T 17,6 ; p+11B 8,7) pesées
    sur NUBASE2020 gelé — mu_loc = écart relatif maximal. La ligne D+D
    « ~3,6 » a deux canaux ouverts (3He+n à 3,269 ; T+p à 4,033 MeV)
    que le corpus ne déclare pas : dette nommée, nommée en extra,
    EXCLUE du mu_loc (la machine ne devine pas le canal). theta abs
    gelé 0,02 (calibration famille article).
    """
    t, d = _fusion_base()
    mu_loc = float(max(v["ecart"] for v in d["comparaison"].values()))
    return mu_loc, {
        "table": t["vintage"],
        "table_sha256": t["_sha256"],
        "comparaison": d["comparaison"],
        "D+D_deux_canaux": {"3He+n": d["q_dd_n"], "T+p": d["q_dd_p"], "declare": 3.6,
                            "note": "« ~3,6 » est entre les deux canaux NUBASE (3,269 et 4,033) sans trancher — dette nommée, hors mu_loc"},
        "pire_ligne": max(d["comparaison"], key=lambda k: d["comparaison"][k]["ecart"]),
        "note": "D+T 17,589 vs 17,6 déclaré (0,061 %) et p+11B 8,682 vs 8,7 déclaré (0,208 %) tiennent ; seul D+D « ~3,6 » est indécidable sans canal déclaré — les deux canaux NUBASE encadrent la déclaration (3,269 et 4,033), la machine nomme la dette au lieu de choisir à la place du corpus",
    }


def tr_kzn_expq65() -> tuple[float, dict[str, Any]]:
    """« exp(−6,5/0,086) ≈ exp(−75,6) ≈ 1,7×10⁻³³ » (2025).

    Chaîne arithmétique déclarée en deux étapes. L'étape 1 tient
    (75,581 arrondi à 75,6) ; l'étape 2 casse : exp(−75,581) =
    1,498×10⁻³3 ≠ 1,7×10⁻³3 (écart ~11,9 %). mu_loc = écart relatif de
    l'exponentielle déclarée vs recomptée, theta abs gelé 0,02
    (calibration famille article). Dette arithmétique interne au
    corpus, pendant de PF5/LH_Bottom_Arith — la machine vérifie le
    calcul déclaré, pas la physique (kT = 0,086 MeV pris tel que gelé).
    """
    t = load_table("tr_kzn_expq65_LITTERATURE-2025.json")
    p = t["params"]
    q = float(p["Q_MeV"])
    kt = float(p["kT_MeV"])
    rapport = q / kt
    expo = math.exp(-rapport)
    decl_rapport = float(p["etapes_declarees"][0][1])
    decl_expo = float(p["etapes_declarees"][1][1])
    e_rapport = abs(rapport / decl_rapport - 1.0)
    mu_loc = abs(expo / decl_expo - 1.0)
    return float(mu_loc), {
        "table": t["vintage"],
        "table_sha256": t["_sha256"],
        "rapport_recompute": rapport,
        "rapport_declare": decl_rapport,
        "ecart_rapport": e_rapport,
        "exponentielle_recompute": expo,
        "exponentielle_declaree": decl_expo,
        "pire_etape": "exponentielle" if mu_loc > e_rapport else "rapport",
        "note": "l'étape 1 tient (6,5/0,086 = 75,581 → « 75,6 » arrondi, écart 0,025 %) ; l'étape 2 casse : exp(−75,581) = 1,498×10⁻³3, déclaré « 1,7×10⁻³3 » — écart 11,9 %, dette arithmétique interne au corpus (le taux neutronique est sous-estimé d'un facteur ~1,14 par la faute de calcul, non par physique) ; même grammaire que PF3/PF7 : la machine vérifie l'arithmétique que la source déclare",
    }


def tr_kzn_sensibilite() -> tuple[float, dict[str, Any]]:
    """« 1 % dans deltashell modifie Q de 0,1 MeV » (2025).

    Déclaration de sensibilité : +1 % du terme de couches de 4He → 0,1
    MeV sur Q(D-T) ; +2 % → Q passe 17,6 à 17,8 (cohérent en interne).
    Le modèle gelé de la même page donne terme de couches 4He =
    a_shell·S(2,2) = 0,3×2 = 0,6 MeV → 1 % = 0,006 MeV. mu_loc = écart
    relatif de la sensibilité déclarée vs recomptée, theta abs gelé
    0,02. Dette nommée : l'identification deltashell = a_shell·S est la
    lecture naturelle du texte unique mais non écrite explicitement ;
    la sensibilité déclarée impliquerait un terme de 10 MeV, incompatible
    avec le modèle transcrit de la même page.
    """
    t = load_table("tr_kzn_sensibilite_LITTERATURE-2025.json")
    p = t["params"]
    sens_decl = float(p["sensibilite_declaree_MeV_par_pct"])
    terme = float(p["a_shell_MeV"]) * float(p["S_4He"])
    sens_recomp = terme * 0.01
    mu_loc = abs(sens_decl / sens_recomp - 1.0)
    q_final_recomp = float(p["Q_initial_declare_MeV"]) + float(p["variation_declaree_pct"]) * sens_recomp
    return float(mu_loc), {
        "table": t["vintage"],
        "table_sha256": t["_sha256"],
        "sensibilite_declaree_MeV_par_pct": sens_decl,
        "sensibilite_recompute_MeV_par_pct": sens_recomp,
        "terme_couches_4He_MeV": terme,
        "delta_shell_implique_MeV": sens_decl / 0.01,
        "Q_final_recompute_MeV": q_final_recomp,
        "Q_final_declare_MeV": float(p["Q_final_declare_MeV"]),
        "note": "la déclaration est cohérente en interne (2×0,1 = 0,2 → 17,6 à 17,8) mais pas avec le modèle gelé de la même page : terme de couches 4He = 0,3×S(2,2) = 0,6 MeV → 1 % = 0,006 MeV, facteur ~16,7 sous la déclaration ; la sensibilité annoncée impliquerait deltashell(4He) = 10 MeV — dette interne au corpus entre le modèle transcrit et l'exemple chiffré de sensibilité (ou identification deltashell différente non écrite, dette nommée)",
    }


def _ratios_anu() -> tuple[list[tuple[int, float]], dict[str, Any]]:
    """Chaîne de ratios k(Z) = N(Z)/N(Z-1) depuis la table ANU complète gelée."""
    t = load_table("tr_anu_complet_LITTERATURE-1908.json")
    rows = t["params"]["rows"]
    ratios = [(b[0], b[3] / a[3]) for a, b in zip(rows, rows[1:])]
    return ratios, {"table": t["vintage"], "table_sha256": t["_sha256"]}


def tr_conv4_moyenne_ki() -> tuple[float, dict[str, Any]]:
    """« La moyenne des coefficients noologiques est égale à 2^(1/12) » et
    « 80 % des nucléides ont un coefficient entre 1 et 1,2 » (Convergences IV).

    Déclarations doubles de la même page (2025-01-19), coefficient
    noologique k(i) = N(Z_i)/N(Z_i-1) défini par le corpus lui-même
    (« rapport entre le nombre d'ANU d'un nucléide divisé par le nombre
    d'ANU du nucléide qui le précède »). Pesée sur la table complète gelée
    Z=1-92 (88 valeurs, Tc absent — la chaîne saute Z=43, dette nommée).
    mu_loc = pire des deux écarts relatifs (moyenne, fraction) vs déclarés,
    theta abs gelé 0,02 (calibration famille CONV4, déclarations chiffrées
    à 2-3 significations). Dette de la fouille bouclée : la « table Z=13-92 »
    (audit E44) est gelée (double transcription carte Crookes + Occult
    Chemistry Gutenberg #16058).
    """
    ratios, meta = _ratios_anu()
    cible = 2.0 ** (1.0 / 12.0)
    moy = sum(k for _, k in ratios) / len(ratios)
    moy_sans_sauts = sum(k for z, k in ratios if z > 5) / len([1 for z, _ in ratios if z > 5])
    dans = [z for z, k in ratios if 1.0 <= k <= 1.2]
    fraction = len(dans) / len(ratios)
    hors = [(z, round(k, 4)) for z, k in ratios if not (1.0 <= k <= 1.2)]
    r59 = [(z, k) for z, k in ratios if z <= 59]
    f59 = len([1 for z, k in r59 if 1.0 <= k <= 1.2]) / len(r59)
    m59 = sum(k for _, k in r59) / len(r59)
    e_moy = abs(moy / cible - 1.0)
    e_frac = abs(fraction / 0.80 - 1.0)
    mu_loc = float(max(e_moy, e_frac))
    return mu_loc, {
        **meta,
        "cible_2_pow_1_12": cible,
        "nb_ratios": len(ratios),
        "moyenne_recompute": moy,
        "moyenne_declaree": cible,
        "ecart_moyenne": e_moy,
        "moyenne_Z_gt5_recompute": moy_sans_sauts,
        "ecart_moyenne_Z_gt5": abs(moy_sans_sauts / cible - 1.0),
        "fraction_recompute": fraction,
        "fraction_declaree": 0.80,
        "ecart_fraction": e_frac,
        "positions_hors_bande": hors,
        "fenetre_Z_le_59": {"fraction": f59, "ecart_moyenne": abs(m59 / cible - 1.0)},
        "pire_claim": "fraction_80pct" if e_frac > e_moy else "moyenne_2pow1_12",
        "note": "les deux claims tombent : fraction mesurée 92,2 % (déclarée 80 %, écart relatif 15,3 % — le corpus sous-vend sa propre table) et moyenne 1,0828 vs 2^(1/12) = 1,0595 (écart 2,20 %, juste au-dessus du theta 2 % — les quatre sauts H→He→Li→Be→B (4,0 ; 1,764 ; 1,291 ; 1,220) empoisonnent la moyenne ; sans eux 1,0370, écart 2,12 % de l'autre côté) ; 7 positions hors bande : Z=2,3,4,5,7 (sauts légers) et Z=19 (Ar→K = 0,982, inversion isotopique réelle) + Z=86 (Rn = 0,990, anomaly actinide) ; la fenêtre 1908 stricte (Z≤59) donne 89,5 % / écart moyenne 5,85 % ; dette gelée : Tc absent (chaîne sautée), divergences carte-vs-livre arbitrées vers le livre (F 340, Mn 992, Mo 1746, Rb 1530)",
    }


def tr_conv4_seuil_z25() -> tuple[float, dict[str, Any]]:
    """« Les nucléides se stabilisent à partir de Z=25 (Manganèse) — il n'y
    a plus de variation significative des coefficients noologiques à partir
    de Z=25 » (Convergences IV).

    Contact de seuil : la déclaration se lit « aucun coefficient hors bande
    [1 ; 1,2] au-delà de Z=25 » (le diagramme du corpus croise la droite
    2^(1/12) et la décroissante logarithmique à Z=25). Pesée : fraction de
    positions hors bande dans la fenêtre Z=26..92 (66 ratios, Tc sauté)
    mesurée vs déclarée (0). mu_loc = écart absolu de fraction, theta abs
    gelé 0,02 (calibration famille CONV4). Extras : position réelle du
    dernier hors-bande, amplitude des coefficients au-delà de Z=25.
    """
    ratios, meta = _ratios_anu()
    fenetre = [(z, k) for z, k in ratios if z >= 26]
    hors = [(z, round(k, 4)) for z, k in fenetre if not (1.0 <= k <= 1.2)]
    frac_viol = len(hors) / len(fenetre)
    mu_loc = float(abs(frac_viol - 0.0))
    ks = [k for _, k in fenetre]
    return mu_loc, {
        **meta,
        "fenetre": "Z=26..92",
        "nb_ratios_fenetre": len(fenetre),
        "violations_hors_bande": hors,
        "fraction_violations": frac_viol,
        "amplitude_k_fenetre": [min(ks), max(ks)],
        "dernier_hors_bande_leger": "K (Z=19, k=0,982 — avant la fenêtre déclarée)",
        "note": "le seuil déclaré tient à une violation près : sur 66 coefficients Z=26..92, un seul sort de [1 ; 1,2] — Rn (Z=86, k = 3990/4032 = 0,990, l'anomalie actinide At→Rn où le module DÉCROÎT) ; l'amplitude réelle au-delà de Z=25 est [0,990 ; 1,077] (étroite, la physique qualitative du corpus — saturation des couches — tient) ; sans la violation Rn la fenêtre serait propre ; mu_loc = 1/66 = 1,52 % vs theta 2 % — S+ TENU (0,76 theta) ; dette nommée : « variation significative » n'a pas de seuil chiffré dans le corpus, la bande [1 ; 1,2] du claim 80 % est le calibre gelé",
    }


def tr_conv4_alcalins() -> tuple[float, dict[str, Any]]:
    """« ln(Ei) = -0,004 Z + 1,696 » pour les métaux alcalins (Convergences IV).

    Régression déclarée (pente et ordonnée à 3-4 chiffres significatifs),
    fenêtre nommée par le texte (« pour les métaux alcalins » — les six du
    groupe 1, périodes 2-7, dette nommée : la fenêtre est décrite, non
    déclarée comme telle). Ei gelées NIST/CRC (Fr = valeur calculée NIST).
    mu_loc = écart relatif max |ln(Ei)_recompute − ln(Ei)_déclaré| /
    ln(Ei)_déclaré sur les 6 lignes, theta abs gelé 0,02 (calibration
    famille CONV4). Dette : la régression n'a pas de budget de résidu
    déclaré (le corpus ne dit pas quel RMS il attend).
    """
    t = load_table("tr_alcalins_ei_LITERATURE-2018.json")
    p = t["params"]
    pente = float(p["regression_declaree"]["pente"])
    ordonnee = float(p["regression_declaree"]["ordonnee"])
    lignes = {}
    for z, sym, ei in p["rows"]:
        ln_mes = math.log(float(ei))
        ln_decl = pente * float(z) + ordonnee
        lignes[sym] = {
            "Z": z, "Ei_eV": float(ei), "ln_Ei_mesure": ln_mes,
            "ln_Ei_declare": ln_decl,
            "ecart_relatif": abs(ln_mes / ln_decl - 1.0),
        }
    mu_loc = float(max(v["ecart_relatif"] for v in lignes.values()))
    return mu_loc, {
        "table": t["vintage"],
        "table_sha256": t["_sha256"],
        "pente_declaree": pente,
        "ordonnee_declaree": ordonnee,
        "lignes": lignes,
        "pire_ligne": max(lignes, key=lambda s: lignes[s]["ecart_relatif"]),
        "note": "Li tient au cheveu (écart 0,048 % — la droite passe quasi exactement par Li) et Na à 0,90 % ; la dérive vient des alcalins lourds : K 9,38 % (pire ligne), Cs 7,91 %, Rb 7,47 % — la pente -0,004 sous-estime la courbure réelle du groupe (Ei décroît plus vite que logarithmique entre Na et Cs, puis remonte en Fr ce que la droite ne capture pas) ; la régression déclarée est un fit à 2 paramètres sans budget de résidu (dette nommée) — la machine pèse les écarts ligne à ligne au theta 2 % gelé ; Fr = 4,07274 eV valeur calculée NIST (pas de mesure directe), gelée en source",
    }




def tr_mda_suite_stable() -> tuple[float, dict[str, Any]]:
    """« Le modèle ajusté est précis et cohérent avec les données fournies »
    (Musique des Atomes II, 2025-02-26).

    Suite déclarée (10 termes, isotopes exclus) + paramètres déclarés
    T1=10, D1=5, T2=5, D2=3 pour h(n) = D1.sin(2πn/T1) + D2.sin(2πn/T2),
    progression géométrique de raison 2^(1/12). L'équation complète est une
    image perdue : deux lectures gelées et pesées, (a) additive
    a_n = a1.q^(n-1) + h(n), (b) multiplicative a_n = a1.q^(n-1).(1+h(n)).
    ε non chiffré par le corpus (gelé 0). mu_loc = pire écart relatif
    modèle-vs-suite sur les 10 termes (pire des deux lectures), theta abs
    gelé 0,02 (calibration famille CONV4/MDA). Extras : sous-claim « rapport
    moyen ≈ 2^(1/12) » sur la suite stable.
    """
    t = load_table("tr_mda_suite_LITTERATURE-2025.json")
    p = t["params"]
    suite = [float(v) for v in p["suite"]]
    q = 2.0 ** (1.0 / 12.0)
    d1, t1, d2, t2 = 5.0, 10.0, 3.0, 5.0

    def h(n: int) -> float:
        return d1 * math.sin(2.0 * math.pi * n / t1) + d2 * math.sin(2.0 * math.pi * n / t2)

    modeles = {}
    for lecture, fn in (("additive", lambda n: 18.0 * q ** (n - 1) + h(n)),
                        ("multiplicative", lambda n: 18.0 * q ** (n - 1) * (1.0 + h(n)))):
        pred = [fn(n) for n in range(1, len(suite) + 1)]
        ecarts = [abs(pr / da - 1.0) for pr, da in zip(pred, suite)]
        modeles[lecture] = {
            "prediction_termes": [round(v, 2) for v in pred],
            "ecarts_relatifs": [round(v, 4) for v in ecarts],
            "ecart_max": max(ecarts),
            "terme_pire": ecarts.index(max(ecarts)) + 1,
        }
    mu_loc = float(max(m["ecart_max"] for m in modeles.values()))
    rapports = [suite[i + 1] / suite[i] for i in range(len(suite) - 1)]
    moy_rapports = sum(rapports) / len(rapports)
    return mu_loc, {
        "table": t["vintage"],
        "table_sha256": t["_sha256"],
        "suite": suite,
        "q_declaree": q,
        "h_n_params": {"D1": d1, "T1": t1, "D2": d2, "T2": t2},
        "modeles": modeles,
        "sous_claim_rapport_moyen": {
            "moyenne_rapports_suite": moy_rapports,
            "ecart_vs_2pow1_12": abs(moy_rapports / q - 1.0),
            "note": "le saut H→He (×4) empoisonne la moyenne stable seule : 1,5450 vs 1,0595 (écart 45,8 %) ; sans lui 1,2382 (écart 16,9 %) — la suite stable des 10 premiers termes ne porte pas la raison 2^(1/12), la convergence ne peut venir que de la table complète (voir TR_CONV4_MoyenneKi : moyenne complète 1,0828, écart 2,20 %)",
        },
        "note": "les deux lectures du modèle échouent massivement : la lecture additive a un écart max de 93,3 % au terme 10 (la progression pure n'atteint que 30,2 ANU vs Néon 360 — les corrections h(n), amplitude ≤ 8 ANU et nulle à n=10, ne peuvent jamais combler un facteur ×12) et la lecture multiplicative explose dès le terme 1 (écart 579 %, h(1) = 5,8 fait passer c_1 à 6,8) — le modèle ajusté déclaré « précis et cohérent » ne reproduit pas la suite déclarée sous AUCUNE lecture ; dettes nommées : équation image perdue (deux lectures pesées, même verdict), ε non chiffré (gelé 0), a1 gelé 18 ; la conclusion du corpus est un verbatim pesable, pas une métaphore — la machine la pèse telle quelle",
    }


def tr_alpha_deltaanu() -> tuple[float, dict[str, Any]]:
    """« deltaANU = (1/alpha).Z^(-3/2) » (La Constante ALPHA, 2022).

    Pesée de cohérence INTERNE : la loi déclarée vs les points tracés par
    le corpus dans son propre graphe ANU-2.JPG (transcription gelée pixel
    par pixel, ±2 unités). mu_loc = écart relatif max point/loi là où la
    loi ≥ 1 (la division a un sens), theta abs gelé 0,02 ; les points où la
    loi prédit < 1 sont des violations absolues listées en extra (l'écart
    relatif y est indéfini). DETTE CENTRALE NOMMÉE : la
    définition opérationnelle de deltaANU (« l'erreur relative de la place
    de chaque atome dans le tout ») n'est pas récupérable (équations OLE du
    docx perdues) — la pesée porte sur la cohérence corpus loi-vs-graphe,
    pas sur une vérité externe ; la machine ne pèse pas ce qu'elle ne sait
    pas figer.
    """
    t = load_table("tr_deltaanu_plot_LITTERATURE-2022.json")
    p = t["params"]
    alpha_inv = float(p["alpha_inv"])
    expo = float(p["exposant"])
    comparaison = {}
    violations_absolues = []
    for nom, z, val, u in p["points"]:
        loi = alpha_inv * float(z) ** expo
        if float(val) > 0.0 and loi >= 1.0:
            ec = abs(float(val) / loi - 1.0)
        else:
            ec = None
            violations_absolues.append(
                {"point": nom, "Z": z, "valeur": float(val), "loi": round(loi, 3),
                 "motif": "point négatif (signe opposé à la loi)" if float(val) <= 0 else "loi < 1 (échelle de la loi sous la grille)"}
            )
        comparaison[nom] = {
            "Z": z, "point_gele": float(val), "u_point": float(u),
            "loi_recompute": loi, "ecart_relatif": ec,
        }
    definis = {k: v["ecart_relatif"] for k, v in comparaison.items() if v["ecart_relatif"] is not None}
    mu_loc = float(max(definis.values()))
    pire = max(definis, key=definis.get)
    ratios_point_sur_loi = sorted(v["point_gele"] / v["loi_recompute"] for v in comparaison.values() if v["ecart_relatif"] is not None)
    return mu_loc, {
        "table": t["vintage"],
        "table_sha256": t["_sha256"],
        "alpha_inv": alpha_inv,
        "comparaison": comparaison,
        "pire_point": pire,
        "ratio_point_loi_min": ratios_point_sur_loi[0],
        "ratio_point_loi_max": ratios_point_sur_loi[-1],
        "violations_absolues": violations_absolues,
        "note": "le graphe du corpus contredit sa propre loi déclarée à chaque point : écart relatif max Sc 167 % (3,8 vs 1,42), Li 150 % (66 vs 26,4) ; 13 violations absolues nommées — 11 points négatifs là où la loi est positive (de K −11,7 à Ge −1,2 : signe opposé, la loi ne peut pas être réparée) et 2 points positifs (Cu 2,0, Ga 2,9) où la loi prédit déjà < 1 (0,88 ; 0,79) ; sur les 18 comparaisons relatives possibles, les rapports point/loi vont de 0,35 (D) à 2,5 (Li), des deux côtés de la courbe : aucune renormalisation ne répare ; la courbe verte du graphe coïncide visuellement avec 137.Z^(-3/2), donc le corpus a tracé la loi et des points qui ne la suivent pas ; dette centrale nommée : la définition de deltaANU n'est pas opérationnelle dans le texte récupéré (« erreur relative de la place de chaque atome dans le tout », équations OLE perdues) — la pesée est une pesée de cohérence interne ; Si (Z=14) non transcrit (point masqué, 31 points gelés) ; lectures Ga/Ge ±2,5",
    }


def tr_tov_sn195pt() -> tuple[float, dict[str, Any]]:
    """« Ex pour 195Pt=>196Pt, Sn=6,5 MeV » (TOV, 2025-01-29).

    Exemple numérique de l'article « Nouvelles Perspectives en
    Astrophysique (Calculs) » (histoire-des-sciences.eu, 29 janvier
    2025), étape 3 de la simulation r-process : l'énergie de séparation
    neutronique du produit de capture, S_n(196Pt), déclarée 6,5 MeV.
    Recompute depuis les masses gelées NUBASE2020 (grille du chantier
    k(Z,N), sha256 partagé) : S_n = mex(195Pt) + mex(n) − mex(196Pt) =
    −32793,9 + 8071,3171 − (−32644,5) = 7921,9 keV (masses atomiques,
    les Z électroniques se compensent). mu_loc = écart relatif NUBASE vs
    déclaré, theta abs gelé 0,02 (tolérance de déclaration à deux
    chiffres, même grammaire que TR_KZN_B11_Liaison). Extras : la MÊME
    valeur 6,5 sert d'intrant à l'exponentiel de « Linéarisation »
    (TR_KZN_ExpQ65 pesait l'arithmétique, pas la valeur — trou bouché) ;
    tension « 1 ou 2 % sur El/A » (article TOV) vs RMS 12,36 % mesuré
    par TR_KZN_Modele_Grille sur le MÊME modèle — nommée, non pesée
    (formulation complète du modèle en images, dette identique à B1) ;
    « 2 % sur El/A → 10 % sur les abondances » — sensibilité sans
    mécanisme recomposable, dette nommée.
    """
    t = load_table("tr_tov_sn195pt_LITERATURE-2025.json")
    v = t["value"]
    decl = float(v["declare_MeV"])
    gt = load_table("tr_kzn_grille_NUBASE2020.json")
    g = gt["grille"]
    mex = {(r["Z"], r["A"]): (float(r["mex_keV"]), float(r["dmex_keV"]))
           for r in g}
    mex_195, dmex_195 = mex[(78, 195)]
    mex_196, dmex_196 = mex[(78, 196)]
    mex_n = 8071.3171  # CODATA-2018, m_n = 1,00866491588 u
    sn_keV = mex_195 + mex_n - mex_196
    sn = sn_keV / 1000.0
    mu_loc = abs(sn / decl - 1.0)
    return float(mu_loc), {
        "table": t["vintage"],
        "table_sha256": t["_sha256"],
        "grille_nubase_sha256": gt["_sha256"],
        "Sn_NUBASE2020_MeV": sn,
        "Sn_NUBASE2020_keV": sn_keV,
        "Sn_incertitude_keV": (dmex_195 ** 2 + dmex_196 ** 2) ** 0.5,
        "Sn_declare_MeV": decl,
        "ecart_relatif": mu_loc,
        "note": "S_n(196Pt) = 7921,9 keV (NUBASE2020 gelé : mex 195Pt −32793,9 ± 0,5 ; mex 196Pt −32644,5 ± 0,5 ; mex neutron 8071,3171 keV CODATA-2018) vs 6,5 MeV déclaré — écart 21,9 %, S− à ~10,9 θ ; la valeur déclarée est l'intrant de l'exemple de taux exp(−6,5/0,086) de « Linéarisation » (TR_KZN_ExpQ65) : l'exemple du second article repose sur une S_n erronée de 22 % ; les équations complètes du modèle k sont en images en fin d'article TOV (dette nommée, la machine ne devine pas la formule) ; la revendication « précisions suffisantes (1 ou 2 % sur El/A) » tensionne avec le RMS 12,36 % du même modèle pesé par TR_KZN_Modele_Grille — nommée, non pesée ici",
    }


def tr_pred23_edm() -> tuple[float, dict[str, Any]]:
    """« Moment dipolaire électrique du neutron : d_n < 3×10⁻²⁶ e·cm »
    (index portemann.eu, PRED-23, statut « en cours »).

    Pesée de type plafond sur une veille. Grammaire déclarée AVANT le
    run : pour une borne supérieure déclarée B présentée comme l'état de
    l'art, mu_loc = retard de veille = B_decl/B_best − 1, où B_best est
    la meilleure borne publiée gelée (Abel 2020, nEDM@PSI :
    1,8×10⁻²⁶ e·cm, 90 % CL). Le plafond du corpus est VRAI physiquement
    (1,8 < 3,0 — la déclaration « d_n < 3×10⁻²⁶ » tient contre le monde),
    mais la veille « en cours » fige le corpus à Pendlebury 2015 dont la
    borne 90 % CL est EXACTEMENT 3,0×10⁻²⁶ : mu = 66,7 % de retard sur
    la frontière. Extra nommé : n2EDM phase 1 vise le bas du 10⁻²⁷ e·cm
    d'ici fin 2026 — la veille passera un ordre de grandeur en retard si
    la projection tient.
    """
    t = load_table("tr_pred23_edm_LITTERATURE.json")
    p = t["params"]
    b_decl = float(p["borne_declaree_e_cm"])
    b_best = float(p["borne_litterature_2020_e_cm"])
    b_2015 = float(p["borne_litterature_2015_e_cm"])
    mu_loc = b_decl / b_best - 1.0
    return float(mu_loc), {
        "table": t["vintage"],
        "table_sha256": t["_sha256"],
        "borne_declaree_e_cm": b_decl,
        "borne_litterature_2020_e_cm": b_best,
        "borne_litterature_2015_e_cm": b_2015,
        "plafond_physiquement_vrai": b_best < b_decl,
        "ancrage_2015_exact": abs(b_decl - b_2015) / b_2015,
        "retard_veille": mu_loc,
        "note": "la borne déclarée 3,0×10⁻²⁶ e·cm coïncide EXACTEMENT avec Pendlebury 2015 (90 % CL, PRD 92, 092003) : la veille « en cours » du corpus est figée à l'état d'avant Abel 2020 (PRL 124, 081803, |d_n| < 1,8×10⁻²⁶ e·cm, 90 % CL, meilleure borne publiée confirmée en 2025-2026) — mu = 3,0/1,8 − 1 = 66,7 % de retard ; la déclaration reste VRAIE comme borne physique (le monde la satisfait), c'est son statut de veille actuelle qui casse ; n2EDM phase 1 (données jusqu'à fin 2026) vise le bas du 10⁻²⁷ e·cm : noté, hors mu",
    }
