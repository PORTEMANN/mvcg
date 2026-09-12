# La machine en une page

Ce n’est pas une théorie du monde. C’est une **balance**.

On pose deux nombres et une phrase :

- ce que *vous* calculez ou lisez (`μ_loc`) ;
- ce que *vous* déclarez comme cible (`μ_ref`), tirée d’une table datée ;
- la phrase « ils sont assez proches » (`S`), avec un seuil (`θ`).

La machine répond par un mot : **S+** (oui), **P** (dans la bande), **S−** (non).

Elle n’invente ni la cible ni le seuil. Si vous changez `θ` après avoir vu le mot, ce n’est plus la même pesée : il faut un nouveau dossier.

## À quoi ça sert

À empêcher trois tricheries banales :

1. changer le dictionnaire d’unités (Gauss vs Heaviside) pour que le mot passe ;
2. changer le seuil après coup ;
3. republier un succès en recollant l’étiquette.

Le gel (G1/G2) enregistre *ce qui a été pesé*. L’ancre temps (OpenTimestamps) est optionnelle.

## Trois exemples

**Dirac.** Le produit `e·g` vaut `2π` en Heaviside–Lorentz et `1/2` en Gauss. Même physique, deux dictionnaires. La machine dit S+ dans l’un, S− dans l’autre. Ce n’est pas une découverte : c’est le refus de les mélanger.

**H₂⁺.** Un calcul LCAO à `R = 2` donne environ `1,46 eV` de dissociation. La table déclarée dit `2,65 eV`. Mot : S−. L’ansatz est trop pauvre. C’est voulu.

**Hélium.** L’énergie de corrélation tabulée vaut `−0,042 Ha`. Hartree–Fock récupère `0`. Mot : S−. Encore voulu.

## Ce que ce n’est pas

Pas un solveur de chimie universel.  
Pas une carte du cerveau.  
Pas une unification micro / méso / macro.  
Pas le corpus historique « Machine noétique » (P0–P48) : celui-là reste une *archive* à part.

## Comment un tiers s’en sert

1. Écrire un contact : phrase, table, seuil, levier (« si je change X, le mot doit bouger »).  
2. Répéter en local (`registers`, `campaign` sans `--publish`).  
3. Si le mot est celui prévu, publier : le manifeste `D` entre dans le hash.

Le détail des commandes : `docs/NOTE-INGENIEUR.md`.
