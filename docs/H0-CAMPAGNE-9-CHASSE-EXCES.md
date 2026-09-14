# H0 — campagne 9 : chasse à l'excès — décomposition par survey

Dérivé de campagne, local, non publié (2026-09-14). Aucun contact
créé, aucun gel touché (mots S−/S− inchangés). Suite de la campagne 8 :
l'excès de dispersion est réel (dette de forme négligeable) — **qui le
porte ?**

## Correspondance IDSURVEY (vérifiée)

Table officielle du README `4_DISTANCES_AND_COVAR` du dépôt
[PantheonPlusSH0ES/DataRelease](https://github.com/PantheonPlusSH0ES/DataRelease "citation")
(lue en entier ce jour, 2026-09-14) : 1 SDSS, 5 CSP, 15 PS1MD,
18 CNIa0.02, 50 LOWZ/JRK07, 51 LOSS1, 56 SOUSA, 57 LOSS2, 61 CFA1,
62 CFA2, 63 CFA3S, 64 CFA3K, 65 CFA4p2, 66 CFA4p3, 150 FOUND.

## Protocole déclaré

- Sélection officielle HF (277 LC), rebin équipopulé 8 bins (règle de
  la doctrine), covariance STAT+SYS binée, H0* re-fité en interne =
  **73,35 / χ²_min = 15,450** — reproduit la campagne 7 exactement.
- **1. Offsets par survey** : écart moyen `MU_SH0ES` − μ_pred(z ; H0*)
  par code IDSURVEY, erreur standard, significativité.
- **2. Jackknife LOSO** : retrait de chaque survey, mêmes frontières
  de bins, moyennes + covariance reconstruites, re-fit H0 (Ω gelée).
  Influence = χ²(complet) − χ²(−s) > 0 ⇒ le survey tirait *loin* du
  meilleur ajustement. Influences jackknife, **non additives** (bins
  corrélés) — déclaré.

## Résultats 1 — offsets par survey (significatifs ou notables)

| Survey | n | offset (mag) | SE | signif |
|---|---|---|---|---|
| PS1MD | 20 | +0,0284 | 0,0139 | **+2,0 σ** |
| SOUSA | 8 | **−0,185** | 0,077 | **−2,4 σ** |
| CFA4p3 | 2 | +0,084 | 0,004 | +20 σ (n=2, SE non fiable — voir honnêteté) |
| CSP | 27 | +0,039 | 0,024 | +1,6 σ |
| CFA3S | 10 | +0,041 | 0,024 | +1,7 σ |
| FOUND (plus gros, 72 LC) | 72 | +0,015 | 0,018 | +0,8 σ |

PS1MD est le seul offset positif bien mesuré au-delà de 2 σ ; SOUSA
porte le plus grand décalage en magnitude. FOUND — un quart de
l'échantillon — est *sur* la courbe.

## Résultats 2 — jackknife LOSO

| Survey | n | χ²(−s) | Δχ² | par LC | H0*(−s) |
|---|---|---|---|---|---|
| FOUND | 72 | 11,42 | **+4,04** | 0,056 | 73,55 |
| SOUSA | 8 | 12,28 | **+3,17** | **0,40** | 73,25 |
| CFA3K | 25 | 13,72 | +1,73 | 0,069 | 73,30 |
| LOWZ/JRK07 | 10 | 13,49 | +1,96 | 0,20 | 73,35 |
| CSP | 27 | 13,88 | +1,58 | 0,058 | 73,45 |
| LOSS2 | 26 | 17,75 | −2,30 | −0,088 | 73,40 |
| autres | — | — | < ±1,3 | — | 73,35-73,40 |

Somme des influences : +10,3 (non additive avec χ²_min = 15,45 —
déclaré). **H0* varie de 73,25 à 73,55 selon le retrait** : la position
ne tient à aucun survey.

## Lectures

1. **Pas de méchant unique, une empreinte d'hétérogénéité.** FOUND
   porte le χ² par la masse (72 LC, dispersion réelle, offset nul) ;
   SOUSA le porte par tête (0,40 χ²/LC, 7× FOUND) avec son offset
   −0,185 mag ; la paire CFA4p3 (2010ag + 2010dt) se décale ensemble à
   +0,084 mag. Trois mécanismes distincts, cohérents avec le
   diagnostic « Analysis of Variance » de Pantheon+
   [arXiv:2212.07917](https://arxiv.org/html/2212.07917v2 "citation").
2. **La position H0* est blindée.** Aucun retrait ne déplace H0* de
   plus de 0,2 (73,25-73,55). L'excès est de la dispersion, pas du
   biais : il gonfle le χ², il ne déplace pas le centre. C'est
   exactement la distinction que la métrologie de la machine
   distingue (variance vs offset).
3. **PS1MD mérite un œil** : seul offset positif significatif bien
   mesuré (+2,0 σ), survey qui s'étend jusqu'à z = 0,148 — son décalag
   si réel irait dans le sens d'un H0 plus haut côté haut-z, le sens
   de la tension H0. Dérivé, non gelé, piste pour une campagne
   ultérieure.

## Honnêteté (limites déclarées)

- CFA4p3 : n = 2 (2010ag, 2010dt, deux SNe distinctes vérifiées) ;
  l'erreur standard à n = 2 sous-estime énormément la dispersion —
  la significativité +20 σ n'est **pas** interprétable, l'offset
  +0,084 mag reste un signal à confirmer.
- Les offsets traitent les LC indépendamment : les 30 noms à LC
  multiples (portés par la covariance en C7) contribuent à deux
  surveys s'ils sont croisés — déclaré.
- Les influences jackknife ne se somment pas (bins corrélés) ; elles
  classent des influences, pas des parts de χ².
- Les offsets sont mesurés contre la courbe gelée à Ω gelée : un H0
  ou des Ω différents re-balanceraient partiellement les offsets
  entre surveys.
