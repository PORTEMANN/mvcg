# Inviter — ajouter un contact, le seul geste d'appropriation

Ce dépôt n'est pas une communauté de code : c'est un **registre de
pesées**. Le seul geste qui y ait du sens est d'y ajouter **son
contact** : sa molécule, son solide, sa loi — pesé avec la discipline
du gel. Un fork, une étoile ou un ticket ne pèsent rien ici ; un
contact tiers, si.

## Le geste en une phrase

Déclarer une règle **avant** le premier run, avec θ gelé et une table
vintage, et laisser la machine découvrir le mot (S+, P ou S−) — jamais
le choisir.

## Ce qu'un contact exige

1. **Un objet** : molécule, bande spectroscopique, solide, fluide,
   grandeur d'un condensat, loi empirique… pas une fonction de test,
   pas une identité mathématique.
2. **Une table vintage** dans `data/tables/` (millésime déclaré,
   source citée, `sha256_note` de gel). Un contact sans table vintage
   n'est pas un contact.
3. **Un protocole écrit avant le run** : la règle de calcul, θ, la
   référence — et la déclaration que la référence ne participe jamais
   au calcul (anti-tautologie). Si deux références plausibles
   existent, en choisir une *avant* le run et l'écrire (honnêteté de
   comparaison, cf. O15).
4. **Un levier directionnel** : ce qui serait modifié si le mot est
   un échec — jamais θ.
5. **Un runner** dans `src/mvcg/registers.py` + une entrée `Contact`.
6. **Un test qui fixe le mot découvert** (cf. `tests/test_open_o14.py`,
   le plus court de la série).
7. **Une doctrine courte** (`docs/O17-CONTACT-OUVERT.md`…) : chronologie
   du gel, le mot, le levier, pourquoi ça compte.

## La discipline (non négociable)

- Le mot est **découvert**, pas choisi. Un S− honnête vaut mieux
  qu'un S+ flatteur.
- θ ne bouge **jamais** après le gel.
- La référence ne choisit **jamais** la règle après coup.
- Pas de modèle unifié, pas d'API industrielle, pas de grand récit :
  un objet, une règle, un mot.

## Chemin conseillé (≈ 30 min)

1. [`docs/QUICKSTART.md`](docs/QUICKSTART.md) — deux pesées en
   10 minutes (Dirac, H₂⁺), le cycle geler → peser → auditer.
2. Relire [`docs/O13-CONTACT-OUVERT.md`](docs/O13-CONTACT-OUVERT.md)
   et `tests/test_open_o13.py` — le gabarit le plus petit de la série.
3. Écrire la table, le runner, le `Contact` ; premier run honnête ;
   gel offline (audits [HOLD] I-G1 / I-G2) ; test figé sur les
   valeurs réelles.
4. Ouvrir une PR. Le critère de relecture est la **discipline du
   protocole**, pas le verdict : S+, P et S− sont tous les trois des
   mots acceptables.

Le numéro du contact est le suivant de la série (O17 au moment de
l'écriture). La série complète : [`README.md`](README.md).
