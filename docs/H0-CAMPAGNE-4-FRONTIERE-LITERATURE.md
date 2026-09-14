# H0 — campagne 4 : frontière du levier H0 sur les cartes LITERATURE

Exploration locale (2026-09-13 soir), non publiée. Pendant exact de la
campagne 3 (DEMO), jouée sur la paire de cartes réelles
(`H0-HZ-SNE-CONTACT-LITERATURE.md`). Aucun gel modifié : θ = 0,02756,
les deux tables, les mots S−/S− figés. Le levier déplace le H0 de la
courbe — jamais les bins, jamais θ, jamais les Ω gelés.

## Estimation pré-campagne (écrite avant le run)

σ_var attendu ≈ 0,065–0,070 > 2θ = 0,05512 → S− universel prévu, aucune
fenêtre P/S+ accessible. Suspense borné : σ_var réalisé vs 2θ ; H0*
attendu ≈ l'ancrage à ±0,5.

**L'estimation était fausse — le suspense a parlé**, comme annoncé
possible : σ_var réalisé = 0,0489 < 2θ. La fenêtre P existe.

## Balayage (mot pesé par la machine)

Carte Planck (ancrage 67,4) :

| H0 courbe | rms (mag) | mot |
|---|---|---|
| 65,00 | 0,1388 | S− |
| 66,00 | 0,1080 | S− |
| **67,40 (posée)** | **0,0695** | **S− (figé)** |
| 68,50 | 0,0489 | P |
| 69,04 | 0,0458 | **P (minimum)** |
| 70,00 | 0,0547 | P |
| 71,50 | 0,0887 | S− |
| 73,04 | 0,1305 | S− |

Carte SH0ES (ancrage 73,04) :

| H0 courbe | rms (mag) | mot |
|---|---|---|
| 70,00 | 0,1517 | S− |
| 71,50 | 0,1087 | S− |
| 73,04 | 0,0695 | S− |
| 74,50 | 0,0467 | P |
| **74,82** | **0,0458** | **P (minimum)** |
| 76,00 | 0,0570 | S− |

## Frontières exactes

| Carte | S− → P (montée) | P → S− (descente) | P/S+ |
|---|---|---|---|
| Planck | 68,07 | 70,03 | aucune (rms_min = 1,66 θ) |
| SH0ES | 73,77 | 75,89 | aucune |

## Lectures

1. **L'estimation « S− universel » était fausse du côté de σ_var** :
   le rms à l'ancrage (0,0695) mêlait décalage moyen et dispersion ;
   au minimum, décalage nul et σ_var = 0,0489 < 2θ. La fenêtre P
   existe sur les deux cartes — exactement le type de correction
   honnête que la campagne 3 avait apprise sur la DEMO.

2. **Le miroir est complet.** rms_SH0ES(H0) = rms_Planck(H0 ×
   67,4/73,04) — relation exacte, vérifiée numériquement : les minima
   se correspondent (69,04 et 74,82, même ratio 1,0837), mêmes
   rms_min, même σ_var. Les deux cartes portent un seul et même
   balayage exprimé dans deux unités d'amplitude.

3. **Le centre des bins n'est ni Planck ni SH0ES.** Le meilleur fit
   (courbe Ω gelés, bins non pondérés) est à +0,0519 mag de chaque
   ancrage (miroir exact) — le centre physique est *entre* les deux
   fabrications, à ~1,06 σ_var de chaque frontière de la fenêtre P.
   Chaque ancrage est à 2,6 σ_var de son propre centre. La carte
   bas-z LITERATURE ne tranche pour aucune fabrication : elle dit que
   le flux Hubble binné, pesé tel quel, préfère un H0 intermédiaire —
   à la précision σ_var = 0,049 mag des 8 bins non pondérés.

4. **Le S+ est inaccessible aux deux cartes** (rms_min = 1,66 θ) :
   8 bins non pondérés ne valident jamais une courbe « à hauteur du
   bruit déclaré » — le bruit réalisé des bins dépasse le bruit
   déclaré d'un facteur 1,66. C'est la dette de compression
   chiffrée par le levier, pas une hypothèse.

## Honnêteté (limites déclarées)

- H0* dépend de la chaîne d'extraction déclarée (bins non pondérés,
  dédoublonnage, fenêtre z) ; une extraction pondérée par la
  covariance officielle déplacerait le centre — dette de compression.
- Les fenêtres P tiennent à σ_var < 2θ réalisé ; ce σ_var porte
  l'hétérogénéité des surveys (FOND/PS1MD/SDSS) et les vitesses
  résiduelles — dettes écrites, non corrigées.
- Le levier H0 est le seul degré de liberté balayé ; Ω gelés fixés,
  les fenêtres se déplaceraient avec d'autres Ω (non exploré ici,
  gelé par doctrine).
- Les mots des contacts restent S−/S− : ces scénarios de levier ne
  modifient ni les tables ni les mots figés.
