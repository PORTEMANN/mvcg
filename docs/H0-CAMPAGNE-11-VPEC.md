# H0 — campagne 11 : test VPEC — l'excès bas-z est-il cinématique ?

Dérivé de campagne, local, non publié (2026-09-14). Aucun contact
créé, aucun gel touché (mots S−/S− inchangés). Suite de la campagne 10 :
l'excès est concentré sous z ≈ 0,07 — le régime des vitesses
particulières. Le `.dat` porte `VPEC`/`VPECERR` par SN, et `zHD` est
déjà *« with CMB and VPEC corrections »* ([README officiel du dépôt](https://github.com/PantheonPlusSH0ES/DataRelease "citation"), vérifié campagne 9).

## Correction de protocole (déclarée, corrigée avant consignation)

Premier jet du script : garde anti-sentinelles `VPEC > −100` excluant
112 LC. **Erreur** : inspection directe — ces 112 valeurs sont des
vitesses particulières **négatives réelles** (−101 à −447 km/s,
VPECERR = 250 km/s plat), pas des sentinelles (le −9 du format est
réservé à d'autres colonnes, ex. HOST_ANGSEP). Script corrigé, les
résultats ci-dessous portent sur **les 277 LC**.

## Protocole

Diagnostic niveau LC (pas de χ² biné — simplification déclarée) :
résidu d_i = `MU_SH0ES`ᵢ − μ_pred(zHDᵢ ; H0* = 73,36), prédicteur
x_i = VPECᵢ/(c·zHDᵢ). Si la correction VPEC était **absente**, la
pente attendue serait b = 5/ln 10 = 2,171 mag par unité x ; si elle
est **parfaite**, b = 0. Régression pondérée (w = 1/e_diag²),
variance résiduelle rééchelonnée.

## Résultats

| Échantillon | n | pente b | SE | b/SE | r |
|---|---|---|---|---|---|
| tout-z | 277 | +0,19 | 0,54 | 0,35 | +0,02 |
| bas-z (z < 0,07) | 211 | +0,29 | 0,59 | 0,49 | +0,03 |
| très bas-z (z < 0,0372) | 138 | +0,11 | 0,67 | 0,16 | +0,01 |
| haut-z (≥ 0,07, contrôle) | 66 | −2,82 | 8,14 | 0,35 | −0,04 |

Offsets a ≈ +0,004 à +0,011 mag — nuls. Levier faible au haut-z
(|VPEC| médian 0,009 mag-équivalent après la coupure z > 0,0233).

## Lectures

1. **L'hypothèse VPEC est innocentée.** La pente mesurée (+0,19 ± 0,54)
   est compatible avec 0 à 0,35 σ, et l'hypothèse « correction absente »
   (b = 2,171) est exclue à ~3,7 σ. La correction de vitesses
   particulières appliquée par la collaboration fait son travail : il
   ne reste **aucune structure résiduelle dans la direction VPEC**,
   y compris dans la zone bas-z qui porte tout l'excès.
2. **L'excès bas-z n'est donc pas cinématique.** Restent sur la table
   les offsets de surveys (C9 : SOUSA −0,185, paire CFA4p3 +0,084,
   PS1MD +0,028) et/ou un scatter intrinsèque au-delà du modèle — une
   hétérogénéité photométrique/local, pas un résidu de bulk flow.
3. **Honnetete de puissance** : r ≈ 0,02, le test est davantage
   confirmatoire (la correction est bien là) qu'exhaustif (une
   structure résiduelle < ~0,5 σ serait invisible). La C10 a montré
   que le haut-z est blanc : la combinaison des deux campagnes dit
   « dispersion locale sans signature cinématique ».

## Honnêteté (limites déclarées)

- Diagnostic par régression non binée : ne remplace pas un χ² avec
  covariance complète ; déclaré comme tel.
- VPECERR = 250 km/s plat : le modèle d'erreur de la collaboration,
  pas une quantité mesurée SN par SN ; pris tel quel.
- H0* gelé à 73,36 pour tous les sous-échantillons (les fits séparés
  C10 bougent de ±0,3, sans effet sur les pentes à cette précision).
- La non-détection reste une non-détection : un signal < 0,5 σ dans la
  direction VPEC ne serait pas visible avec ce levier.
