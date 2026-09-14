# H0 bas-z LITERATURE — rapport de faisabilité (étape §5.1–§5.2)

Chantier local, non publié (2026-09-13 soir).
Périmètre de cette passe : **vérification documentaire uniquement** —
aucune donnée réelle extraite, aucun bin construit, aucun mot pesé.
Question : Pantheon+ satisfait-elle les critères d'admissibilité A1–A3
du protocole, et que dit le diagnostic A5 (ancrage) ?

## Références vérifiées (relues, non de mémoire)

| Référence | Rôle pour le contact |
|---|---|
| Scolnic et al. 2022, ApJ, 938, 113 | release complet : 1701 courbes de lumière, 1550 SNe Ia uniques, z = 0,001–2,26, 18 surveys |
| Brout et al. 2022, ApJ, 938, 110 | distances + covariance : diagramme de Hubble binned et unbinned (procédé BBC/SALT2mu), Table 2 (rms résiduel par modèle de dispersion), Table 7 (magnitudes corrigées par SN) |
| Carr et al. 2022, PASA, 39, 46 | redshifts + vitesses particulières des SNe |
| Peterson et al. 2022, ApJ, 938, 112 | analyse des vitesses particulières |
| Riess et al. 2022, ApJ, 934, L7 | SH0ES : H0 = 73,04 ± 1,04 (l'échelle locale, pour la dette d'indépendance) |

Données publiques : VizieR J/ApJ/938/110, dépôt du projet, et
photométrie brute repackagée (Zenodo, sans distances pré-calculées).
Aucun accès payant n'est nécessaire.

## A1 — publication référencée : ✅

Références ci-dessus, toutes en revue à comité de lecture (ApJ, PASA).
`doi_or_ref` sera recopié depuis la source primaire au moment de
l'écriture de la table.

## A2 — extraction reproductible : ✅

- BBC produit **un diagramme de Hubble binned ET unbinned** : la
  chaîne compilation → bins est documentée par les auteurs eux-mêmes.
- Table 7 de Brout et al. 2022 : magnitude corrigée par SN —
  l'agrégation en bins peut être refaite et vérifiée.
- Critère §5.2 du protocole (reconstruction d'un bin à la main) est
  exécutable sur ces données.

## A3 — dispersion déclarable : ✅

- Modèle de dispersion BS21 documenté : σ_tot² = σ_meas² + σ_scat²(c,
  x1, M*) + σ_gray² + σ_lens² + σ_vpec² + σ_z² ; **σ_gray est ajusté
  pour ramener le χ² réduit à l'unité** — la dispersion standardisée
  est donc une valeur publiée, pas une supposition.
- Table 2 de Brout et al. 2022 : rms résiduel du diagramme pour
  chaque modèle de dispersion (BS21 le plus bas). Valeur exacte à
  recopier lors de la déclaration.
- Matrices C_stat et C_syst **publiées** : la dette de compression
  (D-compression) sera chiffrable, pas seulement déclarée.

## A5 — diagnostic ancrage : le point qui structure tout

Fait vérifié dans Brout et al. 2022 : le fit BBC minimise (α, β, γ,
σ_gray) de façon **cosmology-independent**, et l'amplitude absolue
des μ est portée par M = M0 + 5 log₁₀(c/H0). Les μ publiés Pantheon+
sont donc des **distances relatives sans amplitude ancrée** — M est
un paramètre de nuisance marginalisé dans l'analyse cosmologique
standard.

Or le contact exige μ_ref = 0 (« la courbe passe par les bins ») :
le rms des résidus n'est défini qu'une fois l'amplitude des μ fixée.
Trois voies, deux admissibles :

| Voie | Mécanisme | Statut |
|---|---|---|
| M ajustée sur les bins | recaler l'amplitude sur les données elles-mêmes | **INTERDIT** (doctrine : ajuster sur la référence) |
| Ancrage SH0ES | M fixée par l'échelle locale → les μ portent H0 = 73,04 | admissible, dette **D-indépendance** maximale (donnée et levier non indépendants — pendant Landau exact) |
| Ancrage Planck | amplitude recalée au fiducial H0 = 67,4 | admissible, dette **D-ancrage** (la carte mesure aussi le choix d'amplitude) |

**Conséquence structurante** : l'ancrage fait partie de la déclaration
de table, et chaque ancrage définit sa propre carte. Le chantier devra
donc produire **deux tables et deux contacts** (id par ex.
`..._LITERATURE_SH0ES` et `..._LITERATURE_PLANCK`) — mêmes bins, même
dispersion, deux amplitudes déclarées. La doctrine interdit à la
machine de choisir l'ancrage : elle pèse les deux cartes, chacune
avec sa dette écrite.

## Tranchant estimé (estimation, PAS un verdict)

Raisonnement pré-déclaration, à confirmer par les valeurs recopiées :

- écart d'amplitude entre fabrications à bas-z : 5 log₁₀(73,04/67,4)
  ≈ 0,166 mag, quasi constant sur z < 0,15 ;
- Pantheon+ est riche en bas-z (sa force vs Pantheon originel) :
  des dizaines de SNe par bin Δz = 0,02 → σ_bin dérivable de
  σ_gray/√N_eff plausiblement sous 0,03 mag ;
- alors rms(courbe de l'ancrage) ≈ σ_bin (P/S+ selon θ = σ_bin),
  rms(autre fabrication) ≈ √(σ_bin² + 0,166²) ≈ 0,17 mag ≥ 2θ
  (S−). Le contact distinguerait les deux fabrications **si** les
  bins portent N et σ déclarés.

Risque identifié honnêtement : si les bins sont construits avec un N
trop faible, σ_bin monte, et le S− de « l'autre fabrication » reste
mais le P/S+ de l'ancrage se dégrade. Le nombre de SNe par bin est
donc un paramètre de déclaration, pas un détail.

## Prochaine étape (§5.1–§5.3 complètes)

Sur feu vert : extraction réelle — télécharger le diagramme binned
Brout et al. 2022 (VizieR), recopier Table 2 (rms BS21), construire
8–10 bins bas-z (z < 0,15) avec N et σ par bin, écrire les deux
tables JSON avec dettes, estimation pré-run pour chaque ancrage,
puis premier run.
