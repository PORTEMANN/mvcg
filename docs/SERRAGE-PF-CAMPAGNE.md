# Campagne SERRAGE-PF — le corpus PRINCIPES sous balayage d'étalonnage (2026-09-15)

**Statut : local, non publié.** Mesures dérivées — la couleur du registre
n'est pas modifiée. Protocole `MVC-G-SERRAGE-PF-1.0`
(`campagnes_serrage_pf.py`, verrous figés dans `tests/test_serrage_pf.py`).
La machine apprend de ses propres verdicts : chaque contact PF est repesé
sous une grille θ ∈ {0,20 ; 0,10 ; 0,05 ; 0,02 ; 0,01 ; 0,005}, et deux
frontières exactes sont extraites par contact.

## Le tableau de la campagne

| Contact | Mot domicile | δ | θ* (S+↔P) | Marge δ/θ | Bascule de la grille |
|---|---|---|---|---|---|
| PF7_F4_Recompute | S+ | 0,004 58 | 0,004 58 | 0,046 | **aucune — S+ partout** |
| PF4_Vide_Catastrophe | S+ | 0,007 75 | 0,007 75 | 0,078 | P à θ = 0,005 |
| PF3_Tau5_Jeu | S+ | 0,010 53 | 0,010 53 | 0,105 | P à θ = 0,01 |
| PF2_Graviton_25THz | S+ | 0,033 92 | 0,033 92 | 0,339 | P à θ = 0,02 |
| PF5_Psy_Energie | S− | 0,900 | 0,900 | 9,0 | aucune — S− partout |
| PF8_Hz_Filtrage_Ecart | S− | 33,14 | 33,14 | 331 | aucune |
| PF1_RG_Unification | S− | 32,79 | 32,79 | 656 | aucune |
| PF1b_RG_Unification_2Loop | S− | 32,70 | 32,70 | 654 | aucune |
| PF6_RMN_DeltaB | S− | 8,37·10³⁵ | — | 8,4·10³⁶ | aucune |

## Lecture : ce que la machine a appris d'elle-même

**1. Le corpus est bimodal, sans contact fragile.** Aucun P ne surgit
sous la grille pour les contacts à θ = 0,10 sans que la campagne ne
l'ait cherché : les quatre S+ gardent leur vert jusqu'à des θ deux à
vingt fois plus serrés que le domicile, et les cinq S− gardent leur
rouge même à θ = 0,20 relâché (le θ de relâchement P↔S−, δ/2, vaut au
minimum 0,45 pour PF5 — hors grille). Le θ = 0,10 par défaut n'était
donc ni trop lâche ni trop serré pour ce corpus : il laissait chaque
verdict à une distance d'au moins un facteur 2 de sa frontière, sauf
pour les S+ fins où il laissait une décade.

**2. Hiérarchie de solidité des S+.** PF7 est le S+ le plus solide du
corpus : il survit à θ = 0,005 (δ = 0,46 %). Puis PF4 (θ* = 0,78 %),
PF3 (1,05 %), PF2 (3,4 %). Si un jour le corpus est contesté sur son
aritéthmétique, ce sera par le bas : PF2 est le S+ le moins ancré —
mais il reste S+ jusqu'à quatre fois sous son domicile.

**3. Les S− sont structurels, pas des artefacts d'étalonnage.** Les
cinq S− ont des marges ≥ 9 θ et des θ de relâchement hors de toute
grille raisonnable : resserrer ou relâcher l'étalonnage ne les fera
jamais passer au vert. Leur rouge dit quelque chose du corpus, pas du
θ choisi. C'est la propriété qu'on attend d'un verdict de dette.

**4. Le θ = 0,05 de PF1/PF1b est justifié rétroactivement.** Les deux
contacts portent θ = 0,05 car la revendication est à 1 % ; la campagne
montre qu'à θ = 0,10 ils seraient restés identiques (marge 654–656 θ
dans les deux cas) — le choix du θ n'a joué sur aucun verdict du corpus.

## Règle dérivée proposée (pour débat, non adoptée)

La campagne suggère une graduation de confiance des S+ selon θ*/θ_dom :
ancrage ≥ 10 (PF7, PF4, PF3) = arithmétique vérifiée serrée ;
ancrage 3–10 (PF2) = cohérence interne standard. Reste une mesure
dérivée : la couleur du registre ne change pas.

## Traçabilité

- Module : `campagnes_serrage_pf.py` (population figée 9 contacts,
  grille figée 6 θ). Verrous : `tests/test_serrage_pf.py` (4 tests :
  population, mots domicile, θ* gelés, bascules de grille).
- Résultat : 9 contacts balayés, 3 bascules S+→P localisées, 0
  bascule S−, 0 modification de couleur.
