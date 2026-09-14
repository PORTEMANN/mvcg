# Contact ouvert O17 — H₂ anharmonique (Dunham ordre 1)

Campagne : O17. Date de gel du protocole : 2026-09-14, **avant** le premier run.

## Règle déclarée

**nu_pred(1-0) = omega_e − 2 · omega_e x_e** (développement de Dunham à l'ordre 1),
avec omega_e = 4401,2 cm⁻¹ et omega_e x_e = 121,34 cm⁻¹ — extraits déclarés
Huber & Herzberg (`data/tables/h2_anharmonic_LITERATURE-2018.json`).

**mu_ref = 4160,0 cm⁻¹** — le fondamental déclaré, repris de la note de la table
gelée `h2_vibration_LITERATURE-2018.json` (« le fondamental anharmonique est
4160 cm⁻¹ »). Cette note, écrite au gel d'O15, est la dette promise : le
prédicteur harmonique d'O15 ne pouvait pas la lever ; ce contact la lève.

## La tare assumée

La référence 4160 est un **arrondi au cm⁻¹** : u = 0,5 déclaré. Le prédicteur
Dunham propage u(omega_e) = 0,05 et u(omega_e x_e) = 0,005 (arrondis
d'extraction déclarés). L'écart attendu n'est donc pas une affaire de physique
anharmonique — nu_pred ≈ 4158,5 est la physique correcte — mais la **tare de
l'arrondi de déclaration** (~1,5 cm⁻¹).

## θ gelé : convention GUM k = 1 (precedent Rydberg voie 2)

θ = u_delta = √(u(nu_pred)² + u(nu_ref)²)
  = √(0,0026 + 0,25) ≈ **0,5026 cm⁻¹**, decide = U, k = 1, déclarés avant run.
Geste interdit : déplacer θ après le run ; corriger une constante pour rapprocher
la référence (autre D).

## Estimation pré-run honnête

delta ≈ |4158,52 − 4160,0| = **1,48 cm⁻¹** → delta/theta ≈ **2,94** → **P au
cheveu de la borne S−** (bande P = [θ, 3θ]). Suspense réel, annoncé : le mot
peut basculer S− selon les derniers chiffres de l'extraction déclarée
(robustesse : omega_e x_e extrait ± 0,05 → ratio 2,7–3,1, encore dans la zone
P/S−). Premier contact de la machine qui pèse explicitement une **tare de
déclaration** plutôt qu'une physique — la métrologie de la liberté appliquée
au corpus lui-même.

> **Correction de gel — 2026-09-14, après premier run (trace conservée,
> jamais effacée).** La phrase ci-dessus contient une erreur de règle :
> la bande P de la machine est **[θ, 2θ]** (règle `_adc`, niveaux S+ / P /
> S−), et non [θ, 3θ] comme écrit au gel. L'estimation pré-run honnête
> corrigée est donc : ratio ~ 2,94 > 2 → **S− attendu**, au cheveu de la
> borne P (2θ = 1,0052 cm⁻¹). Mot découvert au run : **S− à 2,9447 θ**
> (delta = 1,480000000000473 cm⁻¹). L'erreur de bande et sa correction
> restent visibles ici, comme l'exige la doctrine (incident Karplus du
> 2026-09-14, même traitement).
>
> **Leçon n° 2, même trace** : l'arrondi « 4160 » est lu ici à u = 0,5
> (dizaine ? unité ?). Lu à u = 1,44 (arrondi 3 chiffres significatifs,
> u = 5/√12), le ratio tomberait à ~1,03 → S+ au cheveu. La tare détectée
> par le S− tient donc à la **déclaration de précision** du fondamental,
> pas à sa physique : l'over-read d'un arrondi est exactement le genre de
> dette que ce contact est venu peser. Changement de la déclaration u =
> autre D, jamais glissé en réparation silencieuse.

## Honnêtetés écrites

- Circularité partielle déclarée : omega_e est le même extrait que dans la
  table d'O15 (gel commun), la référence 4160 aussi. La dette est écrite ici,
  jamais réparée après coup.
- omega_e x_e = 121,34 cm⁻¹ est un extrait arrondi (HH 1979 : 121,336) — la
  sensibilité −2 cm⁻¹ par cm⁻¹ rend l'écart robuste à cet arrondi (± 0,008).
- La référence 4160 ne doit JAMAIS entrer dans le calcul.
