# H0 — campagne 7 : refit à la sélection officielle SH0ES (USED_IN_SH0ES_HF)

Dérivé de campagne, local, non publié (2026-09-14). Aucun contact
créé, aucun gel touché (mots S−/S− inchangés). Suite directe de la
campagne 6 : le refit complet que le doc C6 désignait comme chantier
naturel — **sélection officielle, doublons portés par la covariance,
plus de dédoublonnage e-min**.

## Sélection officielle (vérifiée dans le .dat)

- `USED_IN_SH0ES_HF = 1` : **277 light curves, 238 noms uniques**,
  z ∈ [0,02343 ; 0,14898]. La coupure de vitesse particulière
  z > 0,0233 de l'analyse SH0ES 2022 (Brout et al.) y est déjà
  appliquée — vérifiée, pas supposée.
- Doublons : 39 LC supplémentaires portés (noms à LC multiples),
  **aucun dédoublonnage** — comme l'analyse officielle.
- Calibrateurs (`IS_CALIBRATOR = 1`, 77 LC / 43 noms, z ≤ 0,0168) :
  **non binés, déclarés**. Ancres de l'échelle Céphéide ; le fit
  d'échelle complet est hors doctrine de la forme gelée (les cartes
  posent les deux fabrications en amplitude, pas l'échelle absolue).
- Chevauchement : 236 des 238 noms officiels figuraient déjà dans la
  sélection C6 (via le dédoublonnage e-min).

## Protocole déclaré

- Grille de comparaison : les 8 frontières équipopulées des
  campagnes 4-6. **Bins 0 et 1 VIDES** (le z_min officiel tombe dans
  le bin 2) : χ² sur 6 bins peuplés, **ndof = 5**. Vide déclaré,
  pas masqué.
- `C_bins[b,b′]` = moyenne non pondérée des `C_ij` sur les LC
  membres (règle du contact gelée), en STAT+SYS **et** STATONLY.
- Contrôle de robustesse : rebinning équipopulé à 8 bins sur la
  sélection officielle (règle de binning de la doctrine), côté
  données (`MU_SH0ES` moyen par bin vs forme gelée libre en H0).

## Résultats

**Diagonale covariée (6 bins peuplés)** : σ SYS = 0,021–0,030 mag
(moyenne 0,0257, ratio 0,93 vs θ déclaré 0,02756) ; la part
systématique ajoute ~14 % à la diagonale (STATONLY moyenne 0,0225).
Corrélations inter-bins +0,02 à +0,21, **légèrement négatives avec le
bin 7** (−0,03 à −0,09) — signe opposé aux corrélations de
calibration, déclaré tel quel.

**χ² au centre (grille C4-C6, 6 bins, ndof = 5)** :

| Carte | H0* STATONLY | H0* STAT+SYS | χ²/ndof STATONLY | χ²/ndof STAT+SYS |
|---|---|---|---|---|
| Planck | 68,38 | 68,45 | 2,990 | **2,774** |
| SH0ES | 74,10 | 74,17 | 2,990 | **2,774** |

(χ²_min identique sur les deux cartes : attendu — les deux
fabrications sont la même forme à deux ancrages, miroir exact déjà
constaté en campagne 4.)

Verdicts des cartes **conservés** : sur la carte Planck,
χ²(67,4) = 22,4 ≫ χ²_min = 13,9 — la courbe Planck posée reste hors
zone à la sélection officielle, covariance complète ou pas.

**Vérification d'ancrage (côté données)** : `MU_SH0ES` officiel
moyen − carte gelée, sur les bins peuplés :

- carte Planck : −0,092 à −0,175 mag (moyenne **−0,125**)
- carte SH0ES : +0,014 à +0,083 mag (moyenne **+0,049**)

Les données officielles tombent **entre les deux fabrications, plus
près de SH0ES** — cohérent : ce sont les données de la collaboration
SH0ES elle-même. La dette de forme mesurée en C6 (+0,074 mag moyen)
retombe à +0,049 à la sélection officielle.

**Contrôle de robustesse (rebin équipopulé 8 bins, côté données,
forme gelée libre en H0)** : H0* = **73,36**, χ²/ndof = 2,21,
rms brut = 0,0385 mag. Avec Ω gelés (0,315/0,685), le fit des
données officielles binées retombe **en zone SH0ES**, à ~1,5 du
centre rms SH0ES (74,82) et hors de toute zone Planck. Le gel des
Ω ne déforme pas le résultat à bas z — mais il laisse une dette de
forme (χ²/ndof = 2,21 > 1) : la collaboration ajuste ses Ω, nous
gelons les nôtres.

## Lectures

1. **L'excès de dispersion fond de moitié à la sélection officielle.**
   χ²/ndof : 4,47 (C6, sélection large 591 SNe) → 2,77 (C7,
   sélection officielle 277 LC). Le facteur d'excès passe de ~2,1 à
   ~1,7 en dispersion. La partie basse de la fenêtre (z < 0,0234,
   vitesses particulières) et les SNe hors critères SH0ES
   portaient une vraie part de l'excès — l'hétérogénéité de
   sélection était un vrai ingrédient, pas un bruit de méthode.
2. **Le résidu n'est pas nul pour autant.** Même à la sélection
   officielle avec covariance complète, la forme gelée excède le
   bruit publié d'un facteur ~1,7. La dette n'est plus un artefact
   de sélection large ; c'est un écart de forme (gel des Ω,
   fabrication des cartes) plus un excès résiduel de dispersion.
3. **Côté données, la machine retombe en zone SH0ES.** H0* = 73,36
   sur le rebin équipopulé officiel : les cartes gelées, posées sur
   les données SH0ES elles-mêmes, se replacent là où la
   collaboration les a fabriquées. Les S−/S− gelés restent debout,
   et le centre « entre les deux fabrications » garde son sens :
   c'est le sens des données officielles elles-mêmes.

## Honnêteté (limites déclarées)

- Bins 0-1 vides sur la grille C4-C6 : le χ² ndof = 5 n'utilise que
  z ≥ 0,0234. Le rebin équipopulé (contrôle) couvre toute la
  sélection.
- Calibrateurs hors covariance et hors bins : le fit d'échelle
  Céphéide–SN complet n'est pas refait (hors doctrine gelée).
- Le χ²/ndof = 2,21 côté données mélange excès de dispersion réel
  et dette de forme des Ω gelés ; les deux ne sont pas séparés ici.
- Le contrôle de robustesse utilise `MU_SH0ES` (ancrage natif de la
  collaboration) comme module de distance : c'est la référence
  d'ancrage officielle, avec sa propre dette de forme (+0,049 mag
  vs carte SH0ES gelée).
