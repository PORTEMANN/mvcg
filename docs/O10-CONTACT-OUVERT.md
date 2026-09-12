# O10 — dixième contact ouvert : la bande carbonyle du PMMA par transfert

Un contact **ouvert** = le mot n'est pas connu au gel. O10 assume une
chose au gel que les autres contacts ne supposaient pas : **son
suspense est minimal**, et il le dit.

## Chronologie du gel

1. **Protocole écrit avant toute exécution** : règle déclarée — transfert
   de constante de force k(C=O ester) := k(C=O formaldéhyde), extrait
   par le modèle harmonique k = μω² ; les liaisons source et cible sont
   de **mêmes atomes** (C=O) : la masse réduite est identique et la
   prédiction est exacte par construction arithmétique ; θ = 0,10 figé
   avant run ; référence = bande PMMA 1735 cm⁻¹. La note du contact
   écrit : « suspense minimal assumé au gel ». La bande PMMA ne
   participe jamais au calcul.
2. **Premier run** : mot découvert : **S+**, δ ≈ 0,63 %.
   Artefacts gelés offline (audit [HOLD] I-G1 / I-G2) :
   `examples/registre/O10.*`.
3. **Figé** : mot dans `tests/test_open_o10.py`.

## Le mot : S+ — et pourquoi il ne trompe personne

μ_loc = 1746 cm⁻¹ (transfert exact, masses identiques) contre
μ_ref = 1735 cm⁻¹. Le test le dit explicitement : ce S+ est
**structurel au geste** — il ne peut pas venir d'un accident de
paramètre, parce que le geste n'a pas de paramètre libre (même masse
réduite des deux côtés).

Ce qui distingue O10 d'un S+ en verre : la doctrine assume le suspense
nul. La valeur du contact n'est pas le mot — c'est la **frontière
tracée** : le transfert de force marche à 0,6 % entre liaisons de mêmes
atomes (O10), à 14 % entre liaisons voisines (O2), et rate à 22 %
quand la loi empirique sort de sa fenêtre (O4). O10 est l'étalonneur
du geste transfert : il donne le zéro de la règle.

## Levier : k←conjugaison

L'écart réel (1746 vs 1735, −11 cm⁻¹) est le doigt de la conjugaison
et de l'environnement électrostatique de l'ester. Le levier dit ce
qu'il faudrait : une correction de constante de force par
environnement chimique — pas un θ déplacé.

## Pourquoi O10 compte

Un instrument honnête a besoin d'étalons à suspense nul autant que de
mesures d'inconnu : O10 est l'étalon du geste transfert, O6 l'étalon du
geste grille. La série O sait désormais dire, pour chacun de ses gestes,
où est son zéro.
