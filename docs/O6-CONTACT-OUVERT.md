# O6 — sixième contact ouvert : le levier d'O1 tient son seuil

Un contact **ouvert** = le mot n'est pas connu au moment où le protocole
est gelé. O6 est la seconde moitié de la démonstration commencée à O1 :
**non seulement la machine sait perdre honnêtement — elle sait gagner
quand son propre levier est activé, sans jamais toucher au θ gelé.**

## Chronologie du gel (ordre qui fait la valeur)

1. **Protocole écrit avant toute exécution** : même table
   (`codata2018_extract.json`, R∞ CODATA-2018), même chaîne Ha → eV,
   **même θ = 1e−3 gelé qu'O1** — le seuil d'un contact ne bouge jamais,
   même quand on sait qu'il va être tenu. Le levier `grille←raffiner`
   est activé : n = 1600 au lieu de 200 (h ÷ 8), r_max = 25 inchangé,
   différences finies 2e ordre, Dirichlet. Ce qui était su : l'ordre de
   l'erreur (O(h²) → division attendue par ~64). Ce qui n'était pas su :
   la valeur exacte de δ à n = 1600.
2. **Premier run** : mot découvert, pas choisi : **S+**,
   δ ≈ 6,1·10⁻⁵ << θ = 10⁻³. Artefacts gelés (offline) :
   `examples/registre/O6.{bits,units,metric,cost}.json` — audit
   relançable : `[HOLD] I-G1`, `[HOLD] I-G2`.
3. **Figé** : le mot entre dans le test `test_open_o6.py`, comme pour
   tout contact du registre.

## Le mot : S+

μ_loc = −13,60486384 eV (grille n = 1600) contre μ_ref = −13,60569312 eV
(R∞ CODATA-2018) : la grille raffinée tient le seuil d'un facteur
**16** (θ/δ ≈ 16,4).

C'est le **premier S+ ouvert** de la série — et il n'a rien d'un S+
garanti par construction : il est arrivé après un S− honnête (O1),
quatre contacts qui ont exposé la machine à la réfutation, avec le θ
gelé *avant* le run. La différence avec les S+ en verre du registre
(H1s_Rydberg à θ = 1e−12) tient en une phrase : ici, le mot aurait pu
être P ou S− si l'ordre 2 n'avait pas tenu — le gel le dit, le test
de levier le vérifie (l'erreur passe de 3,8·10⁻³ à 6,1·10⁻⁵ quand h
est divisé par 8, soit ÷63 : l'ordre 2 est confirmé, pas supposé).

## La paire O1 → O6, qui est la démonstration

| | O1 (grille n=200) | O6 (grille n=1600) |
|---|---|---|
| μ_ref | −13,60569312 eV | identique |
| θ | 1e−3 | **identique, gelé** |
| μ_loc | −13,5535 eV | −13,60486 eV |
| δ | 3,84·10⁻³ | 6,10·10⁻⁵ |
| mot | S− | **S+** |

Même objet, même référence, même seuil, seul le levier déclaré à O1
a bougé. C'est la différence entre un banc d'étalonnage et une balance :
la machine ne « valide » pas son modèle — elle encaisse un S−, écrit
ce qu'il faudrait changer, et quand le changement est fait, elle tient
le seuil qu'elle avait raté. Le S+ d'O6 doit sa crédibilité aux P et
S− d'O2–O5 : personne ne peut dire que le jeu est truqué, puisque la
machine a montré qu'elle sait dire « pas tenu » à 1,2 point près (O5).

## Règles de lecture

- **Un S+ ouvert ne s'exporte pas non plus** : il se rejoue.
  `python3 -m mvcg registers` — tout tiers obtient le même mot avec
  les mêmes bits gelés, en ~1 seconde de calcul.
- **Le θ gelé est la star du contact** : la seule différence entre
  le S− d'O1 et le S+ d'O6 est n — jamais θ, jamais μ_ref.
- **La série est désormais complète** : S− (artefact), P (transfert),
  P (ontologie), S− (frontière de loi), P (au seuil), S+ (levier tenu).
  Les six mots ont été découverts après le gel, jamais choisis.

## Pourquoi O6 compte

O1 posait la question : « une machine qui dit S− honnêtement, sait-elle
un jour dire S+ sans tricher ? » O6 y répond : oui — par le seul chemin
légitime, celui du levier déclaré. C'est le certificat d'apprentissage
de la machine : pas une amélioration de θ, pas une nouvelle référence
plus facile, mais la direction écrite au moment de l'échec, suivie.
