# H0 — campagne 10 : split d'échantillon en z — la micro-tension interne existe-t-elle ?

Dérivé de campagne, local, non publié (2026-09-14). Aucun contact
créé, aucun gel touché (mots S−/S− inchangés). Suite de la campagne 9 :
l'offset PS1MD invitait à tester une **dérive de position avec z**, pas
seulement de la dispersion.

## Protocole déclaré

- Sélection officielle HF (277 LC), deux coupures :
  a. **médiane** z = 0,0372 (règle équipopulée de la doctrine) ;
  b. **fixe z = 0,07** (physique : échantillon local vs étendu).
- Chaque sous-échantillon : rebinning équipopulé à 8 bins, observable
  `MU_SH0ES` moyen, covariance STAT+SYS binée, fit H0 seul (Ω gelée
  0,315), ndof = 7. Erreur par Δχ² = 1.
- Zoom : offsets PS1MD/SDSS restreints au haut-z.
- Limite déclarée d'emblée : les fits séparés rebinent 16 points (8+8)
  — les χ² ne sont **pas imbriqués** avec le fit unique (8 points), la
  comparaison directe des χ² n'est pas un test d'ajustement, seuls les
  ΔH0 et les χ²/ndof se lisent.

## Résultats

**Coupure médiane (138 / 139 LC)** :

| Moitié | z range | H0* | χ²/ndof |
|---|---|---|---|
| bas-z | 0,0234-0,0371 | 73,40 ± 0,58 | **2,287** |
| haut-z | 0,0372-0,1490 | 72,85 ± 0,47 | **0,916** |
| Δ | | −0,55 ± 0,74 | |

**Coupure z = 0,07 (211 / 66 LC)** :

| Moitié | z range | H0* | χ²/ndof |
|---|---|---|---|
| bas-z | 0,0234-0,0671 | 73,11 ± 0,48 | **1,906** |
| haut-z | 0,0702-0,1490 | 73,34 ± 0,69 | **0,449** |
| Δ | | +0,23 ± 0,83 | |

**Zoom offsets** : PS1MD haut-z (n=17) +0,030 ± 0,016 vs tout-z
+0,029 ± 0,014 — **inchangé par la coupure** : son offset est uniforme
sur toute son étendue en z, pas un phénomène haut-z. SDSS idem
(−0,009 vs −0,011).

## Lectures

1. **Pas de micro-tension interne.** ΔH0 = −0,55 ± 0,74 (médiane) et
   +0,23 ± 0,83 (0,07) : les deux moitiés de l'échantillon préfèrent
   le **même H0**. La position 73,3-73,4 n'est pas une moyenne de deux
   mondes qui se disputent — elle est unanime des deux côtés.
2. **L'excès est un phénomène bas-z.** Le haut-z blanchit à χ²/ndof =
   0,92 (médiane) et 0,45 (0,07) : au-delà de z ≈ 0,04-0,07, les
   données officielles suivent la forme gelée *à hauteur du bruit
   publié*. Toute la dette de dispersion de la C7/C8 se concentre
   sous z ≈ 0,07 — exactement le régime des vitesses particulières
   résiduelles et de l'hétérogénéité des surveys locaux (SOUSA,
   CFA4p3, LOSS, CSP, CFA — tous z < 0,08, tous porteurs d'offset en
   C9). Le χ²/ndof complet (2,21) est donc un **artefact de la zone
   locale**, pas une propriété de l'échantillon entier.
3. **Le centre H0 repose sur du propre.** C'est le haut-z qui ancre
   la position (73,34 ± 0,69), et il est blanc. La machine peut le
   dire désormais chiffré : le contact H0 est pesé par des données
   qui passent le test de blancheur, avec une dette localisée et
   cartographiée.

## Honnêteté (limites déclarées)

- χ² non imbriqués entre split et complet (16 vs 8 points rebinés) —
  seuls ΔH0 et χ²/ndof par moitié sont interprétés.
- haut-z 0,07 : bins minces (8 LC/bin), erreurs plus grandes ;
  χ²/ndof = 0,45 peut refléter une sur-estimation de la covariance à
  petit effectif — les deux splits concordent néanmoins.
- Les erreurs H0 viennent de Δχ² = 1 sur grille ; elles ignorent la
  dépendance au gel des Ω (la C8 a montré l'effet négligeable).
- Réserve de lecture : « bas-z porte l'excès » ne dit pas *pourquoi*
  (vitesses particulières résiduelles ? zERR ? hétérogénéité
  photométrique locale ?) — la campagne cartographie, n'identifie pas
  le mécanisme physique.
