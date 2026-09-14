# SERRAGE — Campagne 2 : détente des P (2026-09-14, locale)

Protocole gelé : `SERRAGE-PROTOCOLE.md` (section Campagne 2, ajoutée
après feu vert). Script : `campagnes_detente_serie_o.py`. Population : les
5 P à θ = 0,1 sans budget GUM (O2, O3, et les trois NMR Vogeli–Bax —
la série O stricte n'en compte que 2 ; la population inclut ses voisins
NMR, comme en campagne 1).

## Résultats

| Contact | δ | δ/θ | pos_bande = log2(δ/θ) | Étages détente |
|---|---|---|---|---|
| O2_CO2_nu3 | 0,1448 | 1,448 | 0,534 | 1 |
| NMR_Karplus_Sheet_VogeliBax2007 | 0,1600 | 1,600 | 0,678 | 1 |
| NMR_Karplus_Sheet | 0,1612 | 1,612 | 0,689 | 1 |
| O3_Carbon_D_Raman | 0,1724 | 1,724 | 0,786 | 1 |
| NMR_Karplus_Helix_VogeliBax2007 | 0,1869 | 1,869 | 0,902 | 1 |

## Lecture

**Le k de détente ne discrimine pas — la position, si.** Tous les P de
la population ont δ/θ ∈ [1, 2] : ils remontent tous en S+ au premier
palier (θ×2 = 0,2 ≥ δ partout). Le verdict P à θ = 0,1 dit seulement
« entre 1 et 2 fois le seuil » ; c'est `pos_bande` qui répartit :

- **O2 (0,53)** : P collé à la frontière S+ — un modèle à peine plus
  juste (ou un δ à peine plus petit) le ferait basculer. Ambre chaud.
- **Trois milieux de bande (0,68–0,79)** : Sheet, Sheet_VogeliBax, O3 —
  P franc, à égale distance des deux verdicts voisins.
- **NMR hélice VogeliBax (0,90)** : P collé à la frontière S− — presque
  un désaccord. Ambre froid.

Symétrie frappante avec la campagne 1 : les S+ « de surface » (0 étage)
et ces P de bord de bande sont les mêmes objets vus de l'autre côté de
la règle. La bande P contient la frontière ; les deux campagnes en
cartographient les abords.

## Ce que les deux campagnes donnent ensemble

Chaque contact nu de la série O possède maintenant une coordonnée de
justesse continue : les S+ ont θ\* = δ (profondeur verte), les P ont
pos_bande (position ambre). Restaurée, l'information que la conversion
3 niveaux jetait : un gradient de 0,6 % à 18,7 % d'écart réel sous trois
couleurs.

## Limites déclarées

- Mêmes limites que la campagne 1 (δ mesure, pas incertitude ; pas de
  moyenne ; contacts decide=U hors population).
- Le k de détente est non informatif pour cette population (tous à 1) ;
  il ne deviendrait discriminant que pour des P « profonds » (δ/θ > 2 —
  impossible par définition de la règle) ou dans un régime U.

## Prolongements possibles

- Serrer les S− proches de la bande (δ/θ ∈ [2, 4]) : descente en P —
  la dernière arête non cartographiée.
- Couche carte : encoder pos_bande / θ\* en teinte des pastilles.
- Régime U : serrage de U (chantier séparé).
