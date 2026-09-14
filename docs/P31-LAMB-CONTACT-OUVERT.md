# Contact ouvert P31 — Le couplet Lamb (Dirac / Mohr / Erickson)

Campagne : P31. Date de gel du protocole : 2026-09-14, **avant** le premier run.
Chantier : atome (la fibre la plus polarisée du registre : 5 S+ / 4 S−,
S+ = identités et certifications, S− = dettes de modèle — il manquait une
prédiction calculée contre une mesure indépendante).

## La dette historique

Dirac seul prédit la **dégénérescence** 2S₁/₂ = 2P₁/₂ (déplacement nul).
Lamb & Retherford (1947) mesurent ~1050 MHz — la dette qui fait naître la
QED. Trois déclarations figées (`data/tables/lamb_shift_P31_LITERATURE-1981.json`,
sources citées dans la table) :

| Déclaration | Valeur | u |
|---|---|---|
| Mesure Lundeen–Pipkin 1981 | 1057,845 MHz | 0,009 |
| Calcul QED Mohr (années 1970) | 1057,864 MHz | 0,014 |
| Calcul QED Erickson (années 1970) | 1057,912 MHz | 0,011 |
| Dirac seul | 0 | — |

Vintages distincts déclarés : la mesure est **postérieure** aux calculs —
aucune constante n'est dérivée de la référence.

## Les trois contacts

1. **`P31_Lamb_Dirac`** — grammaire du score normalisé de `P30_Kato_gaussian`
   (dimension « 1 », abs, θ = 0,05 gelé) : Dirac prédit 0, la mesure
   normalisée vaut 1 → delta = 1,0. Estimation pré-run : **S− à 20 θ**,
   sans suspense — la machine quantifie la dette historique.
2. **`P31_Lamb_Mohr`** — θ = u_delta = √(0,014² + 0,009²) =
   **0,016643316977093238 MHz**, decide = U, k = 1. Estimation pré-run :
   delta ≈ 0,019 → ratio ≈ **1,14** → **P au cheveu de S+** (bande P =
   [θ, 2θ], vérifiée contre `_adc`). Suspense réel, mot inconnu au gel.
3. **`P31_Lamb_Erickson`** — θ = u_delta = √(0,011² + 0,009²) =
   **0,014212670403551895 MHz**, decide = U, k = 1. Estimation pré-run :
   delta ≈ 0,067 → ratio ≈ **4,71** → S− attendu, sans suspense — à
   l'époque, Lundeen & Pipkin écrivaient eux-mêmes « not in good agreement
   with theory » (PRL 46, 232).

## Ce que le couplet démontre

Même mesure, deux calculs QED de la même époque : la machine peut donner
**deux verdicts différents** (P vs S− attendus) — elle pèse des déclarations
avec leurs incertitudes déclarées, elle ne sacralise pas « la théorie ».
C'est l'approche croisée appliquée à l'histoire de la physique.

## Honnêtetés écrites

- La référence (mesure) ne doit JAMAIS entrer dans un calcul.
- Les deux calculs QED ne s'accordent pas entre eux (0,048 MHz d'écart) —
  c'est écrit dans la table, pas lissé.
- θ = u_delta (convention GUM k = 1, précédents Rydberg voie 2, O17, O18).
