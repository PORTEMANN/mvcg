# O9 — neuvième contact ouvert : le moment dipolaire de l'eau par Pauling

Un contact **ouvert** = le mot n'est pas connu au gel. O9 est le premier
contact de la série à avoir **piégé son concepteur** : l'estimation
pré-run manuscrite était erronée, et le run l'a révélée.

## Chronologie du gel

1. **Protocole écrit avant toute exécution** : règle déclarée —
   ionicité par l'échelle de Pauling, q = (χ_O − χ_H)/2,25 (en e),
   géométrie déclarée (r_OH = 0,958 Å, angle 104,5°), μ = 2qr·cos(angle/2),
   conversion 1 e·Å = 4,80320427 D ; θ = 0,10 figé avant run ;
   référence = moment observé 1,8546 D. La référence ne participe
   jamais au calcul.
2. **Premier run** : mot découvert : **S−**, δ ≈ 67,4 %.
   Artefacts gelés offline (audit [HOLD] I-G1 / I-G2) :
   `examples/registre/O9.*`.
3. **Figé** : mot dans `tests/test_open_o9.py`.

## Le mot : S− — et l'estimation erronée assumée

μ_loc = 3,105 D (charge partielle 0,551 e) contre μ_ref = 1,855 D.
L'estimation pré-run écrite avant le gel annonçait ~11 % — avec une
conversion e·Å → D **oubliée** (0,647 e·Å lue comme 1,64 D au lieu de
3,11 D). Le run a découvert S−, pas moi : c'est exactement la fonction
d'un contact ouvert — il corrige son concepteur.

Lecture phénoménologique : l'échelle de Pauling brute surdéclare
l'ionicité de la liaison O–H d'un facteur ~1,7. La charge effective
compatible avec le dipôle observé est ~0,34 e par liaison, pas 0,55 e :
le caractère covalent et la polarisation de l'environnement réduisent
la charge. Le S− dit : **l'échelle d'électronégativité n'est pas une
règle de moments dipolaires** — c'est un classement, pas une métrologie.

## Levier : q←polarisation

μ ∝ q : monotone ; le test calcule la charge effective compatible
(q_eff ≈ 0,34 e, dans la fenêtre 0,30–0,38 e) — ce que le levier
recommande : un modèle de charge effective (Mulliken, AIM), jamais un
θ déplacé.

## Pourquoi O9 compte

C'est le premier contact où la machine corrige **l'auteur du
protocole** — l'anti-tautologie a protégé la référence, le gel a
protégé le mot, et l'estimation erronée est documentée noir sur blanc
dans la doctrine. Un dépôt où le concepteur publie son erreur d'avance
est un dépôt qu'on peut croire quand il dit S+.
