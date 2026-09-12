# O1 — premier contact ouvert

Un contact **ouvert** = le mot n'est pas connu au moment où le protocole
est gelé. Ni identité (S+ garanti), ni ansatz condamné (S− garanti) :
une mesure d'inconnu, avec la discipline du gel quand même.

## Chronologie du gel (ordre qui fait la valeur)

1. **Protocole écrit avant toute exécution** : runner (différences finies
   2e ordre), paramètres déclarés (n = 200, r_max = 25 a₀, Dirichlet),
   table (`codata2018_extract.json`, R∞ CODATA-2018), θ = 10⁻³ rel gelé,
   chaîne Ha → eV, dimension, fibre SI.
2. **Premier run** : σ(bits) scellé *avant* le mot (I-G1), bits intacts
   (I-G2). Le mot est alors découvert : **S−**, δ ≈ 3,8·10⁻³ > θ.
   Artefacts gelés (offline) : `examples/registre/O1.{bits,units,metric,cost}.json` —
   audit relançable : `[HOLD] I-G1`, `[HOLD] I-G2`.
3. **Figé** : le mot entre dans le test `test_open_o1.py`, comme pour
   tout contact du registre. Après le gel, reclassement = autre D.

Ce qui était su avant le run : l'ordre de grandeur théorique de l'erreur
(O(h²) avec h = 0,125 a₀), donc une *plage* plausible pour δ. Ce qui
n'était pas su : où δ tombe par rapport à θ = 10⁻³. S+, P et S− étaient
tous trois possibles.

## Le mot : S−

μ_loc = −13,5535 eV (grille n=200) contre μ_ref = −13,6057 eV
(R∞ CODATA-2018). La grille déclarée est trop grossière pour le seuil
gelé. La machine le dit avec les mêmes formules qu'un succès.

Le levier gelé `grille←raffiner` dit ce qu'il faudrait changer : raffiner
la grille, jamais déplacer θ. Le test de levier (`n = 1600`, hors gel)
vérifie la direction : δ diminue d'un facteur > 10 — le S− est un
artefact de grille, pas une physique nouvelle. C'est exactement la
fonction d'un levier discriminant.

## Règles de lecture

- **Un S− ouvert n'est pas un échec** : c'est la première fois que la
  machine risque quelque chose — et elle a raison de risquer petit
  (une grille, pas une théorie).
- **Rejouer O1** : `python3 -m mvcg registers` — tout tiers obtient le
  même mot avec les mêmes bits gelés.
- **Un O2 doit être ouvert de la même façon** : protocole gelé avant le
  premier run, mot découvert, levier écrit, jamais de θ déplacé après
  coup.

## Pourquoi O1 compte

Tous les contacts livrés avant lui avaient leur mot décidé par
construction (identités → S+ ; ansatz pauvres → S−). O1 est le premier
dont le mot **exposait la machine à être réfutée** au moment du gel.
C'est la différence entre un banc d'étalonnage et une balance qui pèse.
