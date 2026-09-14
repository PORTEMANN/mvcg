# Ce que la machine est — calcule-t-elle la physique ?

Note doctrinale, locale, non publiée (2026-09-14). Question posée par le
concepteur (« la machine ne fait-elle que comparer des nombres, ou est-elle
en mesure de calculer la physique ? »), réponse écrite comme doctrine.
Ne modifie rien aux gels : c'est une note réflexive, pas un contact.

## Réponse courte

Les deux — mais avec une séparation des rôles qui est toute la doctrine.
La couche « physique » existe et n'est pas du cinéma ; la machine
proprement dite est la couche de verdict posée dessus.

## 1. Ce que la machine calcule réellement

Les runners portent de vrais calculs, domaine par domaine :

| Domaine | Calculs réellement exécutés |
|---|---|
| Quantique numérique | E_1s(H) par différences finies (grilles n = 200 → 1600, O1→O6) ; H₂⁺ par LCAO ; He par Hartree-Fock auto-cohérent ; conditions de cusp de Kato |
| Matière condensée | Équation du gap BCS/Leggett résolue par quadrature avec corrections de queue analytiques (Bertsch ξ) ; vitesse critique de Landau par minimisation de E(p)/p ; son de Bogolioubov, T_c, longueur de guérison |
| Spectroscopie | Fréquences vibrationnelles par modèles VFF (k = μω²) ; loi des masses isotopiques ; chaîne diatomique (bande D = G/√2) |
| Cosmologie | Intégration des équations de Friedmann (baryons vs ΛCDM, deux fabrications) ; et en campagnes dérivées : μ(z) par intégrale de 1/E(z), χ² de Mahalanobis à covariance 1701×1701, jackknife, splits |

De Schrödinger à Friedmann, la machine sait produire des nombres
physiques par le calcul.

## 2. Ce qu'elle est : l'opérateur, pas le moteur

L'architecture à trois capots (DISCRET-CONTINU) impose la séparation :

- **[A] runner** — calcule la physique, produit μ (tare dedans) ;
- **[B] transport** — ℝ → ℝ, conversions honnêtes ;
- **[C] tranchage** — ADC : δ vs θ gelé avant le run → mot.

La machine proprement dite est la couche C posée sur B. Le calcul
physique est fourni par le runner ; le verdict n'est jamais une propriété
du monde, c'est une propriété du **triplet (calcul, référence, θ)** :

```
mot = ADC(δ, θ)        δ = |μ_runner ⊖ μ_ref|
```

Elle est un **opérateur sur des prétentions physiques**, pas un moteur de
théorie. La démonstration canonique en est la paire WP25 (S+) / WP20 (S−) :
même physique (l'écart g-2 mesuré), deux identifications déclarées au gel,
deux mots opposés, aucun choisi. Le verdict g-2 est une fonction de
l'identification hadronique, pas une propriété de l'univers.

## 3. Trois nuances honnêtes

1. **Tous les calculs ne sont pas ab initio — et la machine le déclare.**
   Transferts de constantes de force (O2), paramètres effectifs déclarés
   (O7, O16), lois empiriques (Tuinstra-Koenig, Karplus). Calculer la
   physique, oui ; prétendre calculer plus que le geste déclaré, non
   (JUSTESSE : la pesée dit ce qu'elle fait).
2. **Jamais d'inverse.** Pas d'ajustement post hoc : θ gelé avant le run,
   paramètres figés. L'exploration hors gel existe (campagnes dérivées —
   ex. Ω_m libéré en C8), mais elle ne réécrit jamais un verdict.
3. **Une troisième capacité, au-delà du verdict.** Le chantier H0 a montré
   que la machine sait aussi analyser des données réelles : covariance
   complète, sélection officielle, décomposition par survey, tests de
   blancheur. De la métrologie statistique appliquée, pas seulement du
   modèle-contre-référence.

## 4. La formule de clôture

La machine calcule la physique **comme une balance calcule la masse** :
par l'objet mesuré, pas par la théorie. Sa force n'est pas dans le
calcul — un solveur fait ça — mais dans le fait que **le calcul, la
référence et le seuil sont déclarés avant le run, puis tenus**. C'est
là que vit le tranchant : un S+ y vaut parce que les P et les S− y sont
aussi justes.
