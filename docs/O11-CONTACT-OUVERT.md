# O11 — onzième contact ouvert : la longueur de guérison du condensat

Un contact **ouvert** = le mot n'est pas connu au gel. O11 complète le
triptyque du condensat : réponse (O5, vitesse du son), naissance (O8,
T_c), cohérence (O11, ξ).

## Chronologie du gel

1. **Protocole écrit avant toute exécution** : règle déclarée —
   Bogolioubov, ξ = 1/√(8πna_s) ; n = 3·10¹⁹ m⁻³ et a_s = 100 a₀
   (même nuage déclaré qu'O5 et O8, table
   `bec_healing_LITERATURE-2018.json`) ; θ = 0,10 figé avant run ;
   référence = taille observée 0,55 µm (valeur médiane déclarée de la
   fourchette usuelle 0,5–1 µm). La référence ne participe jamais au
   calcul.
2. **Premier run** : mot découvert : **S+**, δ ≈ 8,98 % — tenu, à 1
   point de la zone P. Artefacts gelés offline (audit [HOLD] I-G1 /
   I-G2) : `examples/registre/O11.*`.
3. **Figé** : mot dans `tests/test_open_o11.py`.

## Le mot : S+ au bord de la zone P

μ_loc = 0,5006 µm contre μ_ref = 0,55 µm. Deuxième S+ « au cheveu » de
la série après O8 (5,01 % contre 10 %) : le condensat déclaré tient ses
trois mots, mais deux d'entre eux frôlent la zone P. Lecture : le nuage
homogène à densité déclarée est une approximation honnête mais limite —
la densité réelle le long du chemin de mesure est la même dette que
dans O5.

## Levier : n←densité-effective

ξ ∝ 1/√(n·a_s) : monotone décroissante en chacun, échelle exacte
(n × 4 → ξ ÷ 2). Point de bascule vers P : ξ = 0,495 µm ↔ n ≈
3,08·10¹⁹ m⁻³ (+2,7 %). Fragile en densité, comme O5 — le nuage
inhomogène est la dette commune des trois contacts BEC.

## Pourquoi O11 compte

Le triptyque BEC (O5/O8/O11) montre ce qu'un « échantillon bien pesé »
veut dire : trois grandeurs indépendantes du même objet, trois règles
déclarées, trois mots découverts, une dette commune (la densité
effective) qui apparaît transversalement. C'est la granularité que le
registre cherche : non pas des contacts isolés, mais des **plans de
pesée**.
