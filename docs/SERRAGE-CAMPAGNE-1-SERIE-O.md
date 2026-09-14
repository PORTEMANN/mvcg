# SERRAGE — Campagne 1 : la série O (2026-09-14, locale)

Protocole gelé : `SERRAGE-PROTOCOLE.md`. Script : `campagnes_serrage_serie_o.py`.
La couleur du registre n'a pas été modifiée : θ\* et les étages sont des
mesures dérivées. Population figée : les 10 S+ à θ = 0,1 sans budget GUM.

## Résultats

| Contact | δ | θ\* = δ | Étages | Bascule |
|---|---|---|---|---|
| O10_PMMA_Carbonyl | 0,00634 | 0,00634 | **3** | P |
| O13_CO2_Isotopologue | 0,01029 | 0,01029 | **3** | P |
| O16_Cu_Gamma_Eff | 0,01015 | 0,01015 | **3** | P |
| O7_Carbon_D_Levier | 0,01357 | 0,01357 | 2 | P |
| Landau_Vc_He4 | 0,01342 | 0,01342 | 2 | P |
| O14_TK_Fenetre | 0,02222 | 0,02222 | 2 | P |
| NMR_Karplus_Helix | 0,02687 | 0,02687 | 1 | P |
| O8_BEC_Tc | 0,05015 | 0,05015 | **0** | P |
| O15_H2_Harmonique | 0,0583 | 0,0583 | **0** | P |
| O11_BEC_Healing | 0,08976 | 0,08976 | **0** | P |

Vérification de cohérence (O10) : trace complète conservée, bascule
exacte au premier seuil strictement inférieur à δ (0,00625 < 0,00634).
Monotonie de `_adc` respectée : tous les contacts basculent en P, jamais
directement en S−.

## Ce que le serrage révèle que la carte cachait

**Trois familles dans le même vert.**

1. **Vert profond (3 étages)** — O10 (carbonyle PMMA, δ = 0,63 %),
   O13 (isotopologue CO₂, 1,0 %), O16 (γ eff Cu, 1,0 %) : le S+ survit
   huit fois plus de seuil que déclaré. Justesse réelle.
2. **Vert moyen (1–2 étages)** — O7, Landau, O14, NMR hélice : le S+
   a de la marge mais il est déclaré au bon ordre de grandeur.
3. **Vert de surface (0 étage)** — O11 (BEC healing, δ = 9,0 % du seuil),
   O15 (H₂ harmonique, 5,8 %), O8 (BEC Tc, 5,0 %) : **le serrage d'un
   facteur 2 suffit à renverser le verdict**. Ces trois S+ étaient des
   verdicts minces déguisés en verdicts francs par l'échelle log de la
   carte (δ/θ = 0,5–0,9 paraît loin de la bande en y, mais c'est un
   facteur 2 en x).

## Lecture

L'alignement du vert sur θ = 0,1 se décompose en gradient : de 0,6 % à
9 % d'écart réel sous le même mot. La machine ne manquait pas de
discernement — il était numériquement présent (δ est calculé à chaque
pesée) mais il était jeté à la conversion 3 niveaux. Le serrage ne
change rien à la machine : il consigne ce qu'elle sait déjà.

## Limites déclarées

- δ est une mesure, pas une incertitude : θ\* n'est pas une p-value.
- Population volontairement étroite (10 S+ nus de la série O). Les
  contacts decide=U (régime U) ne sont pas serrables en θ — chantier
  séparé.
- Pas de moyenne entre contacts (protocole).

## Prolongements possibles

- Serrer les P de la série O (même échelle, bascule P→S+ ascendante).
- Étendre la population aux S+ des autres campagnes.
- Régime U : serrage de U jusqu'à bascule (contacts GUM).
- Ajouter θ\* comme couche dérivée de la carte principale (pastille ou
  teinte) — la carte devient un gradient de justesse au lieu d'un
  alignement.
