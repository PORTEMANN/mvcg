# H0 — campagne 5 : sensibilité à la dette de compression (bins pondérés)

Dérivé de campagne, local, non publié (2026-09-13 soir). Aucun contact
créé, aucun gel touché : les contacts restent S−/S− sur les tables non
pondérées. Question posée : **que engage la dette de compression ?**

## Protocole déclaré

Même sélection que l'extraction LITERATURE (Table 7 Brout 2022,
dédoublonnage normalisé, fenêtre zHD [0,01 ; 0,15), 598 SNe, 8 bins
équipopulaires aux **mêmes frontières**), seul le binning change :
moyenne pondérée w = 1/e_mBcorr², σ_bin = 1/√Σw (diagonale seule :
C_stat/C_syst reste dette résiduelle). Transposition d'ancrage
identique (même K_B = 28,52698). Règle de pesée identique (rms des
résidus) : la différence mesurée est l'effet du binning seul.
θ de campagne = σ_bin pondéré (chaque carte son seuil, doctrine).

Estimation pré-campagne : le pondéré écrème les SNe bruyantes → bins
plus « FOUND-like » → σ_var pourrait diminuer ; ou le N effectif
réduit fait l'inverse. **Confirmée pour le sens** : σ_var diminue.

## Résultats comparés

| Grandeur | Non pondéré | Pondéré | Écart |
|---|---|---|---|
| θ (σ bins) | 0,02756 | 0,02421 | −12 % |
| σ_var (réalisé) | 0,04895 | 0,03984 | −19 % |
| rms_min | 0,04579 | 0,03726 | −19 % |
| rms_min / θ | 1,66 | 1,54 | −0,12 |
| H0* carte Planck | 69,04 | 68,97 | **−0,07** |
| H0* carte SH0ES | 74,82 | 74,74 | **−0,08** |
| Fenêtre P Planck | [68,07 ; 70,03] | [67,99 ; 69,96] | ≈ stable |
| Fenêtre P SH0ES | [73,77 ; 75,89] | [73,68 ; 75,81] | ≈ stable |

## Lectures

1. **La position est robuste, la profondeur ne l'est pas.** Le centre
   H0* bouge de moins de 0,1 km/s/Mpc quand on change de règle de
   binning : le « le centre des bins est entre les deux fabrications »
   de la campagne 4 survit à la dette de compression. Ce qui bouge,
   c'est la dispersion réalisée (−19 %) : la dette engage l'étendue
   des fenêtres, pas leur emplacement.

2. **Le facteur « bruit réalisé / bruit déclaré » est structurel.**
   rms_min/θ ne bouge presque pas (1,66 → 1,54) : les bins déclarés
   sous-estiment systématiquement le bruit réalisé d'un facteur ~1,5,
   dans les deux binnings. Ce n'est pas un artefact de la règle de
   binning — c'est l'hétérogénéité des surveys plus la covariance
   ignorée (dette résiduelle déclarée). Conséquence : le S+ reste
   inaccessible dans les deux binnings (1,54 θ_w > θ_w).

3. **Les mots des contacts sont robustes à la dette.** Posée à
   H0 = 67,4, la courbe Planck donne δ = 0,0695 (non pondéré) et
   0,0623 (pondéré) — tous deux > 2θ de leur campagne (0,0551 /
   0,0484) : **S− dans les deux binnings**. Même constat sur la carte
   SH0ES (0,2314 / 0,2275). La dette de compression ne peut pas
   retourner le verdict — elle peut seulement l'éclaircir.

4. **Un basculement à la frontière, déclaré honnêtement** : à
   H0 = 70,0 sur la carte Planck, le mot passe de P (non pondéré,
   0,0547 < 0,0551 au cheveu) à S− (pondéré, 0,0493 > 0,0484). Les
   cas au cheveu des frontières sont sensibles à la dette — c'est
   exactement là que la dette engage. Les points gelés des contacts
   (67,4) n'en sont pas.

## Honnêteté (limites déclarées)

- Pondération diagonale seule : la covariance C_stat/C_syst de
  Brout 2022 n'a pas été appliquée (elle corrèle les bins par
  calibration commune). Une application complète est le chantier
  suivant naturel — la dette résiduelle est écrite, pas soldée.
- Les tables pondérées sont des dérivés de campagne : aucun mot ne
  doit y être gelé (leur sha256_note le dit).
- rms_min/θ ≈ 1,5–1,7 mesuré sur 8 bins ; une binning différente
  (plus de bins, bins plus larges) déplacerait ce rapport — non
  exploré ici.
