# O5 — cinquième contact ouvert : la vitesse du son d'un condensat de Bose

Un contact **ouvert** = le mot n'est pas connu au moment où le protocole
est gelé. O5 est le premier contact de la série qui tentait un S+ :
non plus peser la dette d'un modèle, mais vérifier si un modèle
quantique déclaré tient le seuil d'une grandeur mesurée en vrai.

## Pourquoi la vitesse du son du condensat

Dans un gaz de Bose condensé dilué, la relation de dispersion des
excitations devient phononique à basse énergie : ε(p) ≈ c·p avec
**c = √(g·n/m)**, g = 4πħ²a_s/m (Bogolioubov, 1947 ; Gross–Pitaevskii).
C'est l'une des prédictions les plus franches de la physique quantique
des corps dilués : une formule close, trois paramètres déclarés
(masse, longueur de diffusion, densité), une grandeur mesurable par
propagation d'impulsion. Mesurée dès 1997 dans les condensats de ⁸⁷Rb
(Andrews et al.).

## Chronologie du gel (ordre qui fait la valeur)

1. **Protocole écrit avant toute exécution** :
   - table gelée `bec_sound_LITERATURE-2018.json` : m(⁸⁷Rb) = 86,909187 u,
     a_s = 100 a₀, **n = 3·10¹⁹ m⁻³** (densité caractéristique déclarée,
     géométrique de la fourchette usuelle 10¹⁹–10²⁰ pour ces
     expériences), c observée = 1,1 mm/s ;
   - règle déclarée : **c = (ħ/m)·√(4πa_s·n)** (condensat homogène,
     interactions de contact, T = 0) ;
   - θ = 0,05 rel **figé avant le run**. Rationale déclaré : accord
     inter-labo sur une vitesse du son **+** incertitude de densité d'un
     nuage inhomogène — le paramètre le moins contraint du contact est
     nommé *avant* le run, et c'est exactement là que vit le levier.
     Pas de nom de calibre ;
   - **anti-tautologie structurelle** : la vitesse observée ne doit
     jamais entrer dans le calcul ; seuls m, a_s, n pilotent.
2. **Premier run** : mot découvert, pas choisi : **P**,
   δ ≈ 6,17 % (θ = 5 %). Artefacts gelés (offline) :
   `examples/registre/O5.{bits,units,metric,cost}.json` — audit
   relançable : `[HOLD] I-G1`, `[HOLD] I-G2`.
3. **Figé** : le mot entre dans le test `test_open_o5.py`, comme pour
   tout contact du registre. Après le gel, reclassement = autre D.

Estimation honnête pré-run : c ≈ 1,03 mm/s → δ ≈ 6 % : **S+ probable,
P vivant** — la frontière passait à n = 3,4·10¹⁹ m⁻³, au-dessus de la
valeur déclarée. Suspense réel, pour la première fois en faveur du S+.
Le run a tranché : P, à 1,2 point de pourcentage du seuil.

## Le mot : P

μ_loc = 1,032 mm/s (Bogolioubov à n = 3·10¹⁹ m⁻³) contre μ_ref = 1,1 mm/s
(mesure de propagation). La prédiction **manque le S+ d'un cheveu** :
elle retombe dans la zone « bon accord, seuil non tenu ».

Lecture phénoménologique : ce P est la réponse la plus honnête que la
physique pouvait donner. La théorie de Bogolioubov homogène appliquée à
un nuage inhomogène, avec une densité « caractéristique » déclarée,
reproduit 94 % de la vitesse mesurée — mais le seuil de 5 % est le prix
d'une *mesure* : il exige que la densité du chemin de propagation soit
connue à mieux que ~6 % en échelle √n, c'est-à-dire n à ~3 % près. Or
la densité moyennée d'un nuage fini est précisément la grandeur que deux
laboratoires ne reproduisent pas au pour cent. Le P dit : **la formule
est juste, la grandeur d'entrée est au bord de sa métrologie**.

## Le levier : n←profil

c ∝ √n : monotone croissante, échelle exacte (n × 4 → c × 2). Le test
de levier (hors gel) vérifie la direction et calcule le point de
bascule : vers S+ (δ = 5 %), il faut c = 1,048 mm/s, soit
**n ≈ 3,08·10¹⁹ m⁻³ : +2,5 %** sur la densité déclarée. Le verdict est
donc *fragile en densité* — comme annoncé au gel. Physiquement, une
densité moyenne de chemin légèrement plus haute (profil Thomas–Fermi
plus plat que gaussien, par exemple) absorbe l'écart. Ce que le levier
recommande : une meilleure mesure du profil, jamais un θ déplacé.

## Règles de lecture

- **Ce P-là est le meilleur résultat de la série** : la machine a visé
  un S+, elle a manqué le seuil de 1,2 point, et elle le dit. Personne
  ne peut accuser ce verdict d'être arrangement : le θ=5 % était gelé,
  la densité déclarée, la règle déclarée.
- **Rejouer O5** : `python3 -m mvcg registers` — tout tiers obtient le
  même mot avec les mêmes bits gelés.
- **La suite logique** : O6 = raffinage d'O1 (levier grille←raffiner),
  qui *doit* donner S+ avec le θ=1e−3 gelé d'O1 — la seconde moitié
  de la démonstration : la machine sait aussi gagner.

## Pourquoi O5 compte

La série O disait jusqu'ici « combien coûte un modèle simple »
(S−, P, P, S−). O5 demande « un modèle quantique déclaré tient-il une
mesure réelle ? » et la réponse est : **à 6 %, au seuil près, non
encore**. C'est un P plus fort que bien des S+ garantis — et il rend
credible le S+ à venir : quand la machine dira « tenu », on saura qu'elle
sait dire « pas tenu » à 1,2 point près.
