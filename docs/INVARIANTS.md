# Invariants MVC-G

Chaque invariant a un tueur. Si le tueur est observé sur un artefact du cœur,
l’invariant sort du cœur ou le dépôt est en échec de protocole.

## Gel — famille G

**I-G1** — \(\sigma(\beta) \in \mathrm{inputs}(d)\) et \(t_d \ge t_\beta\).
Tueur : \(d\) sans bits, hash divergent, horloge inversée.

**I-G1-OTS** — preuve calendrier présente, digest identique, Date HTTP externe.
Tueur : ancre absente ou digest ≠ `bits_sha256`.

**I-G2** — bits immutables après gel. Tueur : `bits.json` dont le SHA interne
ne reproduit plus le payload. Un patch API est refusé ; ce refus n’est pas
un KILL d’état.

**I-G3** — L5 affichée seulement si `Kill(F) = 0`, avec

```
Kill = phys ∧ nouvelle ∧ mesurée ∧ (d_reg = 0) ∧ (orig = pred)
```

Non implémenté comme commande dans v0.1 (les bits sont déjà gelés pour le rendre calculable).

**I-G4** — une campagne dont l’objectif est `Kill = 1`.
Les familles à déficit forcé (parité, tri, tentes sous tarif \(2^j\)) ne comptent pas.

## Verdict — famille V (spécification, pas encore de scripts phénomène)

I-V2 zéro ajustement · I-V3 levier · I-V4 replay SHA · I-V5 schéma d’échec
identique · I-V6 métrique externe obligatoire.

## Coût — famille M

I-M1 deux tarifs `d_reg` ≠ `d_circ` · I-M2 \(\varnothing \neq 0\) ·
I-M3 monoïde · I-M4 additivité déclarée *avant* mesure · I-M6 ordre acyclique.

## Architecture

I-C1 pas d’arc vers un satellite · I-C2 ≤ 5 exécutables tant que le replay
tiers est incomplet · I-C4 un mot, un objet.


## Lecture — famille D (doctrine absorbée du lot ext v0.5, 2026-09-30)

Absorbée du paquet MVC-G ext v0.5 (2026-09-28) sans code, confirmée par
l'isotherme Tuinstra-Koenig (O4★, 2026-09-29). Chaque invariant a un
tueur, comme partout ailleurs.

**I-D1** — aucune lecture géométrique (carte d'échelle, isotherme)
d'un contact dont la dimension (M, L, T, Q) n'est pas déclarée.
Tueur : une carte d'échelle demandée pour un contact sans dimension.

**I-D2** — la phase d'une loi (fond, effectif, transition) est un champ
du gel, pas une déduction après d. Tueur : phase assignée après
lecture du mot.

**I-D3** — une isotherme exige une échelle spatiale `ell_m` déclarée au
gel. Tueur : isotherme sans `ell_m`.

**I-D4** — le type d'étalonnage (labo, ancrage, U) est déclaré au gel.
Tueur : θ dont le type est décidé après le run.

**I-D5** — jamais de comparaison inter-fibres : un contact n'est
comparable qu'à un contact de même fibre, même dimension, même type
d'étalonnage, même θ. Pas d'export d'un mot vers une autre fibre, pas
de moyennage des couleurs. Tueur : une paire `H0|TK-IDIG`,
`H0|S8`, ou tout mélange nommé de deux tensions en une.

**I-D6** — le mot « transition » est réservé à Δlog ℓ ≠ 0 entre les
deux côtés d'une paire. À Δlog ℓ = 0, c'est une bascule de levier, pas
une transition d'échelle. Tueur : « transition » prononcé à
Δlog ℓ = 0 (ex. H0, fibre verticale).

**I-D7** — deux étiquettes, jamais reclassement croisé : un d peut
produire un mot (R6) et une classe (R5) ; aucune des deux ne reclasse
l'autre. Tueur : un κ_class lu comme verdict, ou un mot lu comme
classe. Actif seulement pour les contacts dotés d'un protocole de
classe gelé (à ce jour : TK-DUAL).

**I-D8** — une veille chiffrée déclare sa date et sa source au gel ;
le statut « en cours » se pèse contre la littérature de référence, pas
contre lui-même. Tueur : une veille sans date (motif PRED-23, borne
EDM figée 2015).

**I-D9** — deux tensions, deux fibres : H0 (Δlog ℓ = 0, fibre
verticale) et S8 (σ8√(Ωm/0.3)) ne se moyennent pas ; S8 ne s'ouvre
qu'avec des contacts séparés par survey (S8-DES-Y6, S8-KIDS-LEGACY,
S8-CMB). Tueur : « secteur sombre » unique, ou `paire H0|S8`.
