# H0 — campagne 6 : covariance complète (C_stat+syst) sur les 8 bins

Dérivé de campagne, local, non publié (2026-09-13 soir). Aucun contact
créé, aucun gel touché (mots S−/S− inchangés). La dette de compression
est **chiffrée**, et la réponse est nette : **elle ne blanche pas les
résidus de la forme gelée**.

## Sources (vérifiées)

- Matrices : `Pantheon+SH0ES_STATONLY.cov` / `STAT+SYS.cov` (1701×1701,
  ordre = `Pantheon+SH0ES.dat`), dépôt officiel
  [PantheonPlusSH0ES/DataRelease](https://github.com/PantheonPlusSH0ES/DataRelease "citation").
- Le README du dépôt avertit noir sur blanc : `m_b_corr_err_DIAG`
  (nos e_mBcorr, donc notre θ déclaré) *« DO NOT FIT COSMOLOGICAL
  PARAMETERS WITH THESE UNCERTAINTIES — YOU MUST USE THE FULL
  COVARIANCE »* [README DataRelease](https://github.com/PantheonPlusSH0ES/DataRelease "citation").
  La dette était documentée par la source elle-même.

## Protocole déclaré et réserves

- Sélection depuis le `.dat` officiel : IS_CALIBRATOR = 0, zHD ∈
  [0,01 ; 0,15), dédoublonnage e-min → **591 SNe** (campagne 4 : 598 —
  les critères de nommage/e_diag diffèrent légèrement entre la table 7
  VizieR et le .dat ; réserve déclarée, effet attendu faible).
- C_bins[b,b′] = moyenne des C_ij sur les membres des bins (règle non
  pondérée du contact gelé, appliquée à la covariance).
- Cohérence vérifiée : m_b_corr table 7 = .dat à 3×10⁻⁴ mag (médiane
  sur 1650 SNe croisées par nom) ; les écarts max ne touchent que les
  doublons. Les μ_bins des cartes gelées sont utilisables avec cette
  covariance.
- Réserve : la covariance des doublons écartés et Céphéide n'est pas
  portée (sous-matrice des retenus) ; la comparaison ligne-à-ligne
  table7/.dat est invalide (ordres différents) — le croisement s'est
  fait par nom.

## Résultats

**Diagonale covariée** : σ = 0,019–0,030 mag par bin (moyenne
0,0243) — du même ordre que θ déclaré 0,02756 (ratio 0,88). Pas de
gonflement dramatique de la diagonale.

**Corrélations inter-bins** : +0,16 à +0,39 (calibration commune,
décroissante avec la séparation en z). Réelle mais modérée.

**χ² = rᵀ C⁻¹ r au centre, ndof = 7** :

| Carte | H0* Mahalanobis | H0* rms (campagne 4) | χ²_min | χ²/ndof |
|---|---|---|---|---|
| Planck | 68,78 | 69,04 | 31,26 | **4,47** |
| SH0ES | 74,54 | 74,82 | 31,26 | **4,47** |

χ²(67,4) = 51,8 et χ²(70,0) = 46,5 (carte Planck) : la courbe Planck
posée reste moins bonne que la courbe à 70, les deux très au-dessus
du bruit covarié.

**Vérification d'ancrage** : MU_SH0ES officiel (ancrage natif du
.dat) − notre transposition = **+0,045 à +0,114 mag, décroissant en
z** (moyenne +0,074). Un pur offset de convention serait constant :
c'est une différence de **forme** — la collaboration ajuste les Ω
dans son fit, nous gelons Ω = 0,315/0,685. Notre transposition reste
interne à la forme gelée (cohérente avec le contact) ; l'écart de
forme est une information de la source, pas une erreur d'extraction.

## Lectures

1. **La dette ne blanchit pas.** χ²/ndof = 4,47 avec la covariance
   complète : les résidus de la forme gelée excèdent le bruit
   publié d'un facteur ~2,1 en dispersion (4,47 ≈ 2,1²). Le facteur
   « bruit réalisé / déclaré » 1,5–1,7 des campagnes 4–5 n'était pas
   un artefact de la diagonale ni des corrélations de calibration :
   c'est un **excès réel de dispersion** à la sélection et au binning
   déclarés (hétérogénéité surveys, non-gaussianité — cohérent avec
   la littérature de diagnostic de Pantheon+ [Analysis of Variance,
   arXiv:2212.07917](https://arxiv.org/html/2212.07917v2 "citation")).
2. **La position reste robuste.** H0* Mahalanobis 68,78/74,54 vs rms
   69,04/74,82 (−0,26) : la métrique complète tire légèrement le
   centre vers le bas mais ne le déplace pas qualitativement. Le
   « centre entre les deux fabrications » survit à la covariance.
3. **Le verdict des contacts survit aussi** : χ²(67,4) ≫ χ²_min sur
   les deux cartes — la courbe Planck posée reste hors zone,
   covariance ou pas. Les S−/S− gelés ne sont pas menacés par la
   dette ; ils la portaient sans la connaître.

## Honnêteté (limites déclarées)

- Sélection 591 vs 598 (nommage/e_diag VizieR vs .dat) — l'effet sur
  χ² est de l'ordre des pourcents, non nul.
- Sous-matrice des retenus : doublons écartés et Céphéide hors
  covariance. Le refit complet à la sélection officielle (doublons
  portés par la covariance, USED_IN_SH0ES_HF) est le chantier suivant
  naturel.
- L'écart de forme MU_SH0ES (+0,074 mag moyen) rappelle que
  l'ancrage natif de la collaboration porte ses propres ajustements —
  nos cartes restent des cartes de la **forme gelée**, c'est leur
  doctrine.
