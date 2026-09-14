# NMR Karplus — la seconde voie : Vogeli-Bax 2007 contre la même référence

Contacts **ouverts** (mots découverts, pas choisis). Gelés en exploration
locale le 2026-09-14 — deuxième brique de la **campagne croisée** : la
paire hélice/brin existante portait les coefficients Vuister-Bax 1993 ;
cette paire porte les coefficients **Vogeli-Bax 2007** sur la *même
géométrie* (φ déclarés) et la *même référence typique* — seuls les
coefficients changent, jamais l'objet.

## Pourquoi cette paramétrisation

³J(HN,Hα) = 7,97 cos²θ − 1,26 cosθ + 0,63 Hz (θ = φ − 60°) —
« the previously parameterized Karplus equation [13] » de
Lee et al. 2014 (ChemPhysChem 16:572) ; la référence [13] est
Vogeli, Ying, Grishaev, Bax, JACS 2007, 129, 9377. Seconde
paramétrisation canonique de la littérature, indépendante de la
table Vuister-Bax déjà gelée (6,51 / −1,76 / 1,60).

## Chronologie du gel

1. **Protocole écrit avant toute exécution** : règle déclarée —
   μ_loc = ³J calculé par la loi Vogeli-Bax 2007 aux φ déclarés de la
   table (−60° hélice, −120° brin), θ = 0,10 rel gelé **au même
   étalonnage que la paire Vuister-Bax** (la comparaison des deux voies
   n'a de sens qu'à θ identique). Références typiques 4,0 / 8,5 Hz —
   ordres de grandeur déclarés (« pas un PDB »), dette identique à la
   paire VB, assumée. Aucun coefficient ajusté sur les références.
   **Honnêteté de sélection** : la paramétrisation a été choisie pour
   sa canonicité et sa vérifiabilité (source traçable), **jamais** pour
   un mot attendu — choisir des coefficients pour fabriquer un suspense
   au bord du seuil serait le geste interdit.
   **Estimation pré-run (CORRIGÉE après run — l'estimation initiale
   était fautive)** : l'estimation écrite avant le premier run disait
   hélice J ≈ 4,2525 → S+ à ~0,63 θ ; c'était une **erreur d'addition
   du rédacteur** (1,9925 + 0,63 + 0,63 = 3,2525, pas 4,2525). Le
   protocole (règle, θ, références) n'était pas en cause : la machine a
   découvert le vrai mot. Valeurs exactes : hélice J = 3,2525 vs 4,0
   → 18,69 % → **P à 1,87 θ** (à 0,13 θ de la frontière S−) ; brin
   J = 9,86 vs 8,5 → 16,0 % → P à ~1,60 θ. L'erreur est conservée
   ici visible, comme les réfutations du registre.
2. **Premier run** : mots découverts : hélice **P à 1,87 θ** (δ = 18,69 %,
   à 0,13 θ de la frontière S−), brin **P à 1,60 θ**. L'estimation
   pré-run écrite au §1 était fautive pour l'hélice (erreur d'addition
   du rédacteur : 1,9925 + 0,63 + 0,63 = 3,2525 — la machine a découvert
   le vrai mot ; le protocole n'était pas en cause). L'erreur est
   conservée en §1, corrigée ici.
3. Figé : mots + θ + règle dans `tests/test_open_karplus_vogelibax2007.py`.

## Le résultat qui compte

La question de la campagne croisée trouve une réponse nette : sur la
**même conformation hélice**, la 1re voie (Vuister-Bax 1993) disait
**S+ à 0,27 θ** et la 2e voie (Vogeli-Bax 2007) dit **P à 1,87 θ** —
les deux paramétrisations canoniques de la même loi ne donnent **pas**
le même mot à θ = 0,10 de la référence typique. La loi de Karplus,
à cet étalonnage et contre une référence « pas un PDB », n'est pas
robuste au choix des coefficients : l'écart entre les voies (~0,86 Hz,
soit ~21 % de la prédiction) est la dette à écrire — c'est écrit ici.
Avec la référence typique déclarée grossière, ce contact mesure la
**sensibilité de la loi à sa paramétrisation**, pas la physique du
peptide.
