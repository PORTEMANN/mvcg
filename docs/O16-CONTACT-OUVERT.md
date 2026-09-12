# O16 — seizième contact ouvert : le levier d'O12, activé

Un contact **ouvert** = le mot n'est pas connu au gel. O16 est le
geste disciplinaire auquel O12 donnait droit : **le levier écrit au
moment de l'échec, activé** — pendant exact d'O7 (qui activait le
levier d'O3).

## Chronologie du gel

1. **Protocole écrit avant toute exécution** : règle déclarée —
   même modèle de Sommerfeld qu'O12 (γ = π²k_B²n/(2E_F), n = 8,47·10²⁸
   m⁻³ de la même table), mais la masse déclarée est la masse
   effective de bande **m\* = 1,38 m_e** (Ashcroft-Mermin) — jamais
   dérivée de la référence : γ_ref/γ_modèle = 1,37 serait circulaire,
   la référence entrerait dans le calcul. La mesure du cuivre
   (96,6 J·m⁻³·K⁻²) NE DOIT JAMAIS entrer dans le calcul ; θ = 0,10
   figé avant run. Estimation pré-run honnête : δ ≈ 1 % — suspense
   faible **assumé au gel**, comme O10 : c'est un contact de geste,
   pas de suspense.
2. **Premier run** : mot découvert : **S+**, δ ≈ 1,01 %.
   Artefacts gelés offline (audit [HOLD] I-G1 / I-G2) :
   `examples/registre/O16.*`.
3. **Figé** : mot dans `tests/test_open_o16.py`.

## Le mot : S+ — et la nuance qu'il porte

μ_loc = 97,5804 J·m⁻³·K⁻² (Sommerfeld à m\* = 1,38 déclarée) contre
μ_ref = 96,6 mesuré. L'écart résiduel de 1,0 % est un vrai contenu
physique : la masse de bande (1,38, issue de la structure de bandes)
n'est pas exactement la masse thermodynamique déduite de la chaleur
(1,37). Le modèle réparé ne dit pas « exact » — il dit « plus juste
d'un facteur 26 », et il mesure lui-même la distance restante entre
deux notions de masse que la littérature distingue à peine.

## Anti-tautologie : la déclaration, pas la dérivation

Le test verrouille le point sensible : avec m\* déclarée = 1,38, la
référence est inutile au calcul ; le geste circulaire (calibrer m\*
sur γ_ref) produirait 1,37 — un *autre nombre*, explicitement exclu.
C'est la même discipline qu'O15 (référence choisie avant le run) :
ce qui est gelé est une **connaissance indépendante**, pas un ajustement.

## Pourquoi O16 compte

La paire O12 → O16 ferme la démonstration commencée par O1 → O6 et
généralisée par O3 → O7 : **tout contact a droit à son levier
activé, une fois, θ jamais déplacé**. O1 → O6 le montrait sur une
grille (paramètre de discrétisation), O3 → O7 sur un paramètre
phénoménologique (k₂/k₁), O12 → O16 sur un paramètre de théorie
effective (m\*) — le geste le plus profond, car ici la « correction »
est devenue un concept de la physique des solides. La machine n'a pas
inventé la masse effective ; elle a montré, en deux pesées, pourquoi
la physique en avait eu besoin.
