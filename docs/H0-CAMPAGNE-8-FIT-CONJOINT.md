# H0 — campagne 8 : fit conjoint (H0, Ω_m) — séparation dette de forme / excès de dispersion

Dérivé de campagne, local, non publié (2026-09-14). Aucun contact
créé, aucun gel touché (mots S−/S− inchangés). Suite de la campagne 7.

**Question unique :** le χ²/ndof ≈ 2,2–2,8 résiduel des campagnes 6-7
est-il une dette de **forme** (Ω gelés imposés à la collaboration qui
ajuste les siens) ou un **excès de dispersion réel** ? Et les verdicts
S−/S− gelés résistent-ils à un adversaire plus fort que le gel (H0 et
Ω_m libres simultanément) ?

## Protocole déclaré

- Forme : ΛCDM courbure nulle, Ω_Λ = 1 − Ω_m, **Ω_m libre** —
  sortie explicite de la doctrine gelée (dérivé, jamais côté contact).
- Grille : H0 ∈ [60 ; 85] (pas 0,05), Ω_m ∈ [0,02 ; 0,65] (pas 0,005),
  χ² complet à chaque nœud.
- **A. Séparation (côté données)** : rebin équipopulé 8 bins sur la
  sélection officielle (`MU_SH0ES` moyen par bin), covariance STAT+SYS
  binée (construction identique campagne 7), ndof = 8 − 2 = 6.
- **B. Robustesse des verdicts (côté cartes gelées)** : grille C4-C6,
  bruit de référence = covariance C6 (sélection 591) — choix
  conservateur. ndof = 6.

## Résultats A — la dette de forme est négligeable

| Fit | H0* | Ω_m* | χ²_min | χ²/ndof |
|---|---|---|---|---|
| Ω gelée 0,315 (réf. C7) | 73,35 | (0,315) | 15,450 | 2,208 (ndof 7) |
| Ω_m libre | 73,20 | 0,360 | 15,389 | 2,565 (ndof 6) |

- **Δχ² = 0,062 pour un paramètre ajouté** : libérer Ω_m n'achète
  presque rien. À bas z, la dette de forme des Ω gelés est **minime**.
- Le χ²/ndof résiduel (~2,2-2,6) est donc **essentiellement un excès
  de dispersion réel**, pas une dette de forme.
- Ω_m sans levier : contour 1σ [0,090 ; 0,650] — presque tout le
  domaine grille, attendu à z < 0,15. H0 au contraire serré :
  1σ [72,05 ; 74,30], 2σ [71,50 ; 75,05]. Le fit est **tendu dans la
  direction H0, mou dans la direction Ω_m** — dégénérescence standard
  des SNe Ia bas-z.
- Validation croisée : la branche gelée du nouveau code reproduit la
  campagne 7 **exactement** (73,35/15,45 vs 73,36/15,45).

## Résultats B — les verdicts gelés résistent à l'adversaire 2-paramètres

| Carte | Meilleur couple | χ²/ndof min | χ²(ancre officielle) | Δχ² ancre |
|---|---|---|---|---|
| Planck | 69,30 / 0,180 | 5,074 | 51,77 (67,4 ; 0,315) | **21,3** |
| SH0ES | 75,10 / 0,180 | 5,074 | 51,50 (73,04 ; 0,315) | **21,1** |

- Même l'adversaire **optimal** (H0 et Ω_m libres) ne ramène pas le
  χ²/ndof sous ~5 sur les cartes gelées : la dispersion de fabrication
  des cartes n'est pas absorbable par une famille de courbes lisses —
  c'est la constatation C4 (σ_var réalisé) vue de l'autre côté.
- L'ancre Planck (67,4 ; 0,315) reste à **Δχ² = 21,3** du meilleur
  ajustement possible — loin au-delà du 2σ joint (6,18). À Ω libre,
  la courbe Planck reste **hors zone** : le verdict S− gelé a de la
  marge, pas de la fragilité.
- Validation croisée : χ²(67,4 ; 0,315) = 51,77 reproduit la campagne 6
  (51,8) à 0,1 % près — deux implémentations indépendantes, même
  nombre.
- Détail déclaré : les deux cartes préfèrent Ω_m ≈ 0,18 (bord bas de
  grille dans le contour 1σ) — goût de forme des fabrications, sans
  conséquence sur les fenêtres H0.

## Lectures

1. **L'excès est de la dispersion, pas de la forme.** C'est la réponse
   nette à la question de la campagne : à sélection et covariance
   officielles, geler Ω = 0,315 coûte Δχ² = 0,06. Tout ce qui reste
   (χ²/ndof ~2,2-2,6) est du bruit réel au-delà du publié — le même
   que la littérature de diagnostic Pantheon+ (arXiv:2212.07917).
2. **Le gel des Ω est gratuit à bas z** pour H0 : le centre bouge de
   0,15 (73,35 → 73,20) quand on les libère. La machine ne paie
   presque rien pour sa doctrine de gel sur ce contact — c'est un
   point de solidité, pas de faiblesse.
3. **Les S−/S− ont ~21 χ² de marge.** L'adversaire le plus fort
   possible (2 paramètres libres, bruit conservateur) ne rapproche pas
   l'ancre condamnée. Les verdicts gelés du chantier H0 sont robustes
   à tout ce qui reste accessible dans la famille ΛCDM lisse.

## Honnêteté (limites déclarées)

- Ω_m libre sort de la doctrine : résultat **dérivé**, jamais
  réinjecté dans les contacts ni les cartes.
- L'analyse B utilise le bruit C6 (sélection large 591) : conservateur
  pour le test, mais pas le bruit de la sélection officielle — un
  refit avec le bruit C7 donnerait des χ²/ndof plus bas (cf. C7 :
  4,47 → 2,77), sans changer la conclusion Δχ² ≫ 1.
- Grille Ω_m bornée à 0,02 : le contour 1σ touche des bords de grille
  dans la direction Ω — la bornification est déclarée, sans effet sur
  la direction H0 (la seule qui porte le verdict).
