# O4 — quatrième contact ouvert : I_D/I_G par la loi de Tuinstra–Koenig

Un contact **ouvert** = le mot n'est pas connu au moment où le protocole
est gelé. O4 descend d'un cran dans l'échelle du désordre : ne plus
prédire où est la bande D (O3), mais **combien de désordre** le spectre
mesure — la quantité que les spectroscopistes du carbone utilisent
vraiment au quotidien.

## Pourquoi I_D/I_G est le bon objet

I_D/I_G est le marqueur opérationnel de la taille des domaines
cristallins L_a dans le carbone partiellement désordonné. La loi de
Tuinstra–Koenig (1970) le relie à L_a en phase 1 (domaines de quelques
nm) : chaque domaine contribue au D par ses bords et au G par son aire,
d'où I_D/I_G = C(λ)/L_a, avec C(514 nm) ≈ 4,4 nm. C'est une loi
empirique avec une fenêtre de validité — exactement le genre de règle
qu'un contact ouvert doit exposer à être réfutée.

## Chronologie du gel (ordre qui fait la valeur)

1. **Protocole écrit avant toute exécution** :
   - table gelée `carbon_disorder_LITERATURE-2018.json` : C(λ = 514 nm)
     = 4,4 nm (constante empirique), L_a = 3,0 nm (taille de domaine
     déclarée de l'échantillon suie/nanographite, dans la fenêtre de
     validité de la phase 1), I_D/I_G observé = 1,2 (extrait textbook
     déclaré) ;
   - règle déclarée : **I_D/I_G = C(λ)/L_a** ;
   - θ = 0,10 rel **figé avant le run**. Rationale déclaré : un rapport
     d'intensités Raman est une grandeur préparation-dépendante ; la
     répétabilité inter-labo d'environ 10 % est le compromis honnête.
     Pas de nom de calibre ;
   - **anti-tautologie structurelle** : le rapport observé ne doit
     jamais entrer dans le calcul ; seuls C et L_a pilotent la
     prédiction.
2. **Premier run** : mot découvert, pas choisi : **S−**,
   δ ≈ 22,22 % > 2θ = 20 %. Artefacts gelés (offline) :
   `examples/registre/O4.{bits,units,metric,cost}.json` — audit
   relançable : `[HOLD] I-G1`, `[HOLD] I-G2`.
3. **Figé** : le mot entre dans le test `test_open_o4.py`, comme pour
   tout contact du registre. Après le gel, reclassement = autre D.

Estimation honnête pré-run : C/L_a = 4,4/3,0 ≈ 1,467 contre 1,2 →
δ ≈ 22 % : zone **S− la plus probable** — première fois de la série O
que le mot probable n'était pas P. Le run a confirmé sans toucher aux
bornes.

## Le mot : S−

μ_loc = 1,467 (Tuinstra–Koenig à C = 4,4 nm, L_a = 3,0 nm) contre
μ_ref = 1,2 (rapport observé). La loi **surestime le désordre apparent**
de ~22 %.

Lecture phénoménologique : à L_a ≈ 3 nm, on est à la fin de la fenêtre
de phase 1 — le sommet de la cloche de Ferrari–Robertson est dans cette
zone (L_a ≈ 2–3 nm), où la réponse D cesse d'être strictement en
1/L_a avant de s'inverser en phase 2 (amorphe : I_D/I_G croît avec
L_a²). La constante C(λ) elle-même a une dispersion documentée selon
les échantillons et les lasers. Le S− dit : **la loi TK appliquée au
voisin de sa frontière de validité ne tient pas le seuil inter-labo** —
pas que la loi est fausse partout.

## Le levier : La←recalibrer

μ ∝ 1/L_a : monotone décroissante, croissante en C. Le test de levier
(hors gel) vérifie la direction et calcule les points de bascule :
- vers P (δ = 20 %) : μ = 1,44 → L_a = 3,056 nm — **+2 %** sur L_a ;
- vers S+ (δ = 10 %) : μ = 1,20 → L_a = 3,667 nm — **+22 %** sur L_a.

Le levier dit donc quelque chose de précis : le S− est **fragile en
L_a** (une calibration TEM déplacée de 2 % le ferait basculer en P) mais
**tenace en physique** (il faut L_a = 3,7 nm — au-delà de la fenêtre
phase 1 déclarée — pour l'absorber complètement). Ce que la machine
recommande par son levier, c'est une meilleure mesure de L_a et une
C(λ) ré-étalonnée sur l'échantillon — jamais un déplacement de θ.

## Règles de lecture

- **Un S− ouvert sur une loi empirique n'est pas un échec de la loi** :
  c'est la carte de sa frontière de validité, à 22 % près.
- **Rejouer O4** : `python3 -m mvcg registers` — tout tiers obtient le
  même mot avec les mêmes bits gelés, la même table, la même règle.
- **O2/O3 prédisaient des positions, O4 prédit un rapport d'intensités**
  : la machine s'est mise à peser des grandeurs que le Raman mesure
  vraiment, avec la répétabilité réelle du geste expérimental.

## Pourquoi O4 compte

O1 S− (artefact de grille), O2 P (transfert de force), O3 P (ontologie
du réseau), O4 S− (frontière d'une loi empirique). La série couvre
maintenant les quatre configurations du ADC 3 niveaux : échec d'échelle
(O1), dette de modèle ×2 (O2, O3), dépassement de seuil sur une loi à
fenêtre (O4). Le protocole tient : à chaque fois le mot est découvert
après le gel, à chaque fois le levier dit ce qu'il faudrait changer sans
jamais toucher θ.
