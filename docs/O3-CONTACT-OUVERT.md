# O3 — troisième contact ouvert : la bande D du graphite par une chaîne à forces égales

Un contact **ouvert** = le mot n'est pas connu au moment où le protocole
est gelé. O3 applique la discipline d'O1 et d'O2 à la frontière
**graphite / carbone amorphe**, lue par son marqueur Raman : la bande D.

## Pourquoi la bande D est le bon objet

Dans le graphite parfait, la bande D (~1350 cm⁻¹) est **interdite** en
Raman : c'est un mode de bord de zone (A₁g) que la sélection q ≈ 0 ne
peut pas éclairer. Le désordre (bords de domaines, défauts, structure
amorphe) relâche la conservation du vecteur d'onde et **active** D —
c'est exactement le marqueur qui distingue graphite et amorphe. Prédire
la position de D, c'est prédire où se trouve la frontière que le
désordre fait apparaître.

## Chronologie du gel (ordre qui fait la valeur)

1. **Protocole écrit avant toute exécution** :
   - table gelée `carbon_raman_LITERATURE-2018.json` (G graphite 1580,
     D graphite 1350, G amorphe 1595, I_D/I_G amorphe 1,0 — extrait
     textbook déclaré) ;
   - modèle déclaré : le graphite est une **chaîne 1D diatomique** de
     carbone (maille A–B, constantes k1 intra / k2 inter). Dispersion :
     mode optique au centre de zone ω²(G) = 2(k1+k2)/m ; bord de zone
     ω²(D) = 2·max(k1,k2)/m (modes dégénérés) ;
   - **transfert déclaré : k2 := k1** (égalisation des constantes de
     force) — à rapprocher du transfert k_r(CO₂) := k(CO) d'O2 : même
     geste, un cran plus minimal (on ne transfert pas entre deux
     molécules mais entre deux liaisons du même réseau) ;
   - à k2 = k1 : **D = G/√2** ;
   - θ = 0,10 rel **figé avant le run**, même compromis documenté
     qu'O2 : tolérance « entre labo » × modèle 1D volontairement
     grossier. Pas de nom de calibre ;
   - **anti-tautologie structurelle** : la bande D observée ne doit
     jamais entrer dans le calcul ; seule G pilote la prédiction.
2. **Premier run** : mot découvert, pas choisi : **P**,
   δ ≈ 17,24 % (zone 0,10 < δ ≤ 0,20). Artefacts gelés (offline) :
   `examples/registre/O3.{bits,units,metric,cost}.json` — audit
   relançable : `[HOLD] I-G1`, `[HOLD] I-G2`.
3. **Figé** : le mot entre dans le test `test_open_o3.py`, comme pour
   tout contact du registre. Après le gel, reclassement = autre D.

Estimation honnête pré-run : G/√2 ≈ 1117 cm⁻¹ contre D ≈ 1350 →
δ ≈ 17 % : zone **P** la plus probable, S+ et S− vivants. Le run a
confirmé la zone P sans toucher aux bornes.

## Le mot : P

μ_loc = 1117,23 cm⁻¹ (chaîne à forces égales) contre μ_ref = 1350 cm⁻¹
(bande D observée du graphite). δ = 17,24 % : au-delà du seuil « entre
labo », en deçà du double.

Lecture phénoménologique : le modèle **sous-estime** D de façon
systématique. La physique qu'il ignore est précisément celle qui rend D
visible : D n'est pas un mode mécanique ordinaire du réseau, c'est un
mode de **double résonance** (électron–phonon) dont la position est
pilotée par la structure électronique près du point K, pas par une
simple densité de force. La chaîne à constantes égales sait où se
trouve le bord de zone mécanique ; la physique du graphite place la
bande active du désordre ailleurs — plus haut.

## Le levier : k←déségaliser

Propriété exacte du modèle : D/G = √[max(1,r)/(1+r)] avec r = k2/k1.
Ce rapport est **minimal à r = 1**, monotone quand r s'éloigne de 1
dans les deux sens, symétrique r ↔ 1/r. L'égalisation déclarée est
donc le **pire cas** du modèle : toute inégalité réelle entre liaisons
intra et inter couche rapproche D de G, donc de la référence. Le test
de levier (hors gel) vérifie : D(0,5) = D(2,0) > D(1,0), et D monte
strictement quand r passe de 1 à 4 puis à 9.

Le levier dit ce qu'il faudrait changer : **une structure de forces
déségalisée**, jamais θ. Pour atteindre S+ il faudrait D/G ≥ 0,90,
soit max(1,r)/(1+r) ≥ 0,81, soit r ≤ 0,235 ou r ≥ 4,3 : les liaisons
inter-couche devraient être ~4 fois plus molles (ou plus dures) que les
liaisons intra — un ordre de grandeur physiquement discutable pour le
graphite, où k_inter ≈ k_intra/3 est déjà une approximation sévère.
Le P est donc structurel : il dit que « forces égales » n'est pas la
bonne ontologie pour le bord de zone actif, sans dire laquelle l'est.

## Règles de lecture

- **Un P ouvert est une dette de modèle**, pas une erreur de mesure :
  la machine tient un quantitatif (17,24 %) là où le discours qualitatif
  (« le désordre active D ») ne donnait aucun chiffre.
- **Rejouer O3** : `python3 -m mvcg registers` — tout tiers obtient le
  même mot avec les mêmes bits gelés, la même table, la même règle.
- **Suite naturelle** : un contact sur l'intensité I_D/I_G (loi de
  Tuinstra–Koenig) — la quantité que les spectroscopistes utilisent
  vraiment — qui mettrait le désordre dans μ lui-même plutôt que dans
  la note.

## Pourquoi O3 compte

O1 risquait une grille, O2 risquait un transfert entre molécules, O3
risque une **ontologie du réseau** : « toutes les liaisons du carbone
se valent ». Le mot P répond : non — et il quantifie le reste à payer
(17 %). La série O1→O2→O3 montre le protocole se généralisant : même
gel, même anti-tautologie, mêmes leviers directionnels, objets de plus
en plus phénoménologiques (atome → molécule → réseau désordonné).
