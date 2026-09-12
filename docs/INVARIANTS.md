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
