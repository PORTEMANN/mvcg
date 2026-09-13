# Hyperfluidité — contacts ouverts

Contacts **ouverts** (mots découverts, pas choisis) — exploration locale,
non publiée. Tiroir hyperfluidité : la condition de Landau (1941) du
⁴He II, puis le paramètre de Bertsch ξ du gaz de Fermi unitaire.

## Contact 1 — Landau : la vitesse critique du ⁴He

### Chronologie du gel

1. **Protocole écrit avant toute exécution** : v_c = min_p E(p)/p sur
   le spectre déclaré de la table (`he4_spectrum_LANDAU.json`) — scan
   fin + parabole locale, pur standard, aucun point ajusté sur la
   référence. La référence v_c ≈ 58 m/s est un ordre de grandeur de
   littérature déclaré. **Dette assumée et écrite au gel** : spectre
   et v_c ne sont pas physiquement indépendants — le minimum de E/p
   *est* le roton, donc ce contact mesure la cohérence interne de la
   carte spectrale déclarée, pas une prédiction. C'est plus faible
   qu'un contact exp−théorie ; le dire fait partie du protocole.
   θ = 0,10 rel gelé avant run. Levier : spectre←autre-mesure (jamais
   la référence, jamais θ). Estimation pré-run honnête : v_c ≈ 58,8
   m/s au roton, δ ≈ 1,3 % → S+ attendu ; suspense faible, dette
   assumée.
2. **Premier run** : mot découvert : **S+**, δ = 1,34 %, mécanisme
   roton confirmé au point déclaré (k* = 1,920 Å⁻¹, E/k_B = 8,62 K).
   La pente phonon (238 m/s) ne gagne pas : le min de E/p est bien au
   roton, comme la physique l'exige. Artefacts gelés offline (audits
   [HOLD] I-G1 / I-G2) : `examples/registre/LANDAU.*`.
3. **Figé** : mot dans `tests/test_open_landau.py`.

## Le mot : S+ — et sa lecture exacte

S+ dit : la carte spectrale déclarée est cohérente avec la vitesse
critique de littérature à 1,3 % près. Ce n'est **pas** « la
superfluidité est comprise » : c'est « le spectre déclaré et le seuil
critique déclaré racontent la même physique ». Le test verrouille
l'anti-tautologie : la loi de Landau recombinée depuis la table donne
exactement le μ du registre, et les points du spectre sont ceux déclarés
— le geste interdit (déplacer les points pour caler v_c) transformerait
le contact en cercle vicieux, et il est maintenant testé comme tel.

### Pourquoi ce contact compte

- **L'hyperfluidité entre dans la machine par sa condition**, pas par
  sa constante : on ne pèse pas T_λ (constante de table, contact
  d'identité), on pèse le *critère* qui fait qu'un fluide peut
  écouler sans dissipation. C'est le pendant hydrodynamique de la
  famille « loi devient carte » (Karplus) : le spectre déclaré est la
  carte, Landau la règle, v_c le mot.
- **La fibre des vitesses** : Landau rejoint O5 (vitesse du son du
  condensat) dans la fibre (si, m/s) — le BEC dilué et le superfluide
  fort se retrouvent dans le même classement, avec deux mots
  différents (P et S+). Le casier gagne la famille hyperfluidité.
- **La dette quasi-tautologique comme discipline** : ce contact
  montre que la machine peut peser honnêtement un objet dont la
  force probante est limitée — à condition que la limite soit écrite
  *dans le protocole*, pas découverte par un lecteur hostile.

## Contact 2 — Bertsch : le paramètre ξ du gaz unitaire

### Chronologie du gel

1. **Protocole écrit avant toute exécution** : ξ = (5/3)·E/(Nε_F)
   en ansatz BCS mean-field à T = 0 (Leggett 1980), équations gap +
   nombre résolues par quadrature (Simpson) avec corrections de queue
   analytiques (`bertsch.py`), aucun point ajusté sur la référence.
   La référence ξ ≈ 0,370 est le consensus expérience/QMC déclaré
   (Ku et al. 2012 ; Zürn et al. 2013) de la table
   (`xi_unitary_LITERATURE.json`). **Dette assumée et écrite au gel** :
   l'ansatz mean-field ne récupère pas la corrélation forte de
   l'unitarité — pendant exact de P27 (He Hartree-Fock). C'est la
   leçon du contact, pas un accident. θ = 0,10 abs gelé avant run.
   Levier : ξ←autre-ansatz (jamais la référence, jamais θ). Estimation
   pré-run honnête : ξ_MF = 0,5905, δ ≈ 60 % → S− attendu net ;
   suspense quasi nul — contact de calibre de l'erreur mean-field.
2. **Premier run** : mot découvert : **S−**, δ = 0,2206 abs > 2θ =
   0,20. Le solveur reproduit le triplet mean-field de littérature :
   μ/ε_F = 0,5906, Δ/ε_F = 0,6864, ξ = 0,5905 (à 6 décimales, stable
   sur le cutoff Λ ∈ [60, 150]). Artefacts gelés offline (audits
   [HOLD] I-G1 / I-G2) : `examples/registre/BERTSCH.*`.
3. **Figé** : mot dans `tests/test_open_bertsch.py`.

### Le mot : S− — et sa lecture exacte

S− dit : l'ansatz BCS mean-field surévalue l'énergie du gaz unitaire
de 37 % environ par rapport au consensus expérience/QMC. Ce n'est **pas**
« la superfluidité de Fermi est réfutée » : c'est « l'ansatz à un
corps corrélé (gap moyen) ne suffit pas là où la corrélation forte
règne » — exactement la dette annoncée. Le test verrouille
l'anti-tautologie : le solveur recombiné donne le μ du registre, et la
table déclarée est celle du run — ajuster le solveur sur la référence
ξ ≈ 0,370 est le geste interdit, testé comme tel.

### Les deux pièges documentés (valeur pédagogique du contact)

- **Normalisation** : ξ porte le facteur (3/5) de l'énergie du gaz
  idéal (E = ξ (3/5) N ε_F). L'oublier rapporte 0,3564 au lieu de
  0,5905 — l'écart systématique que la machine a d'abord cru être une
  intégrande fautive. La leçon : vérifier la *définition dimensionnée*
  de la référence avant de soupçonner la quadrature.
- **Convergence** : les intégrales du nombre et du gap ne convergent
  qu'en 1/u² ; un cutoff fini sans correction de queue dérive d'autant
  plus qu'on augmente Λ (la grille uniforme sous-échantillonne le pic
  à u ≈ √x). Les queues analytiques (∫_Λ^∞ y²/2u² du = y²/2Λ, x/Λ)
  rendent le résultat indépendant du cutoff dès Λ = 60.

### Pourquoi ce contact compte

- **Le pendant de P27 côté hyperfluidité** : l'helium Hartree-Fock
  (S−, corrélation manquante) trouve son miroir exact dans le gaz
  unitaire mean-field (S−, corrélation forte manquante). La machine
  calibre maintenant la même dette dans deux tiroirs.
- **La fibre (1, 1)** : Bertsch rejoint la fibre des grandeurs
  adimensionnées — le S− de l'erreur mean-field côtoie le P de CKM
  et le S− de H0, trois dettes de nature différente dans le même
  classement.
- **Un S− utile** : contrairement à un S− accidentel, celui-ci était
  annoncé au protocole — il mesure la taille de la dette structurelle,
  et il le fait dans le sens où la machine est honnête : la dette est
  écrite, pas cachée derrière un ajustement.

## Contact 3 — KSS : la marge η/s du ⁴He au plancher

### Chronologie du gel

1. **Protocole écrit avant toute exécution** : la conjecture
   Kovtun-Son-Starinets (2005), η/s ≥ ℏ/(4πk_B), est une BORNE —
   démontrée en holographie, avec des contre-exemples théoriques en
   théorie effective, jamais violée expérimentalement. La fabrication
   est la borne inférieure expérimentale déclarée du ⁴He liquide
   (η/s ≥ 8,8 planchers, évaluation Schafer & Teaney 2009 reprise
   dans Kagamihara et al. 2019) lue dans la table
   (`eta_s_kss_LITERATURE.json`), la référence est le plancher
   lui-même (1 en unités du plancher). **Dette assumée et écrite au
   gel** : 8,8 est une borne inférieure déclarée, pas une mesure au
   minimum exact de η/s(T). Le geste interdit est double et écrit :
   déplacer 8,8 vers le plancher, ou lire un mot S− comme une
   réfutation de KSS — un fluide au-dessus de la borne la satisfait.
   θ = 0,10 rel gelé avant run. Levier : η/s←autre-mesure (jamais la
   référence, jamais θ). Estimation pré-run honnête : δ = 780 % → S−
   net attendu ; suspense structurellement nul — c'est un contact de
   marge, comme Bertsch est un contact de dette.
2. **Premier run** : mot découvert : **S−**, δ = 7,8 = 780 % > 2θ =
   0,20. Artefacts gelés offline (audits [HOLD] I-G1 / I-G2) :
   `examples/registre/KSS.*`.
3. **Figé** : mot dans `tests/test_open_kss.py`.

### Le mot : S− — et sa lecture exacte

S− dit : le ⁴He déclaré se tient à ≥ 8,8 planchers du plancher KSS.
Ce n'est **pas** « KSS est réfutée » : la conjecture est une borne
inférieure, et le fluide est du bon côté. Le mot mesure la *marge* —
la distance qui sépare le fluide réel de la saturation conjecturée. La
règle gelée l'interdit littéralement : la borne n'est pas une identité,
et aucun fluide déclaré (⁴He à 8,8, ⁶Li à 6,3, QGP à 2-3 planchers)
ne la viole — la saturation reste ouverte. Le test verrouille
l'anti-tautologie : la table déclarée est celle du run, la référence
est le plancher (1), et rapprocher 8,8 du plancher est le geste
interdit, testé comme tel.

### Pourquoi ce contact compte

- **La borne entre dans la machine comme borne, pas comme identité** :
  le plancher ℏ/4πk_B est la *référence*, jamais la valeur attendue par
  construction. C'est la discipline annoncée au prolongement de
  Landau : dire ce qu'un objet n'est pas fait partie de la règle.
- **Trois S−, trois natures** : la fibre (1, 1) tient maintenant le S−
  de marge (KSS), le S− de dette (Bertsch) et le S− d'écart de
  modèle (H0) — la machine distingue trois façons d'être loin.
- **Le QGP en réserve déclarée** : le fluide le plus proche du
  plancher (2-3 unités, incertitudes grandes) est le candidat naturel
  d'un futur contact à suspense réel — la saturation de KSS n'est pas
  tranchée, et la machine le dit.

## Contact 4 — KSS/QGP : le suspense dévoilé

### Chronologie du gel

1. **Protocole écrit avant toute exécution** : premier contact du
   tiroir dont le mot tranche une question ouverte — la saturation de
   la borne KSS par le plasma quarks-gluons, fluide déclaré le plus
   proche du plancher. Fabrication : la borne INFÉRIEURE de
   l'extraction la plus citée (η/s ≈ (2-3) unités KSS, Luzum &
   Romatschke, repris dans arXiv:1108.0734), la déclaration la plus
   favorable au suspense ; référence : le plancher (1). **Dette
   assumée et écrite au gel** : les extractions ne coïncident pas, la
   fourchette large (0,6-2,5 planchers, arXiv:2604.04222) chevauche
   le plancher ; un mot S− dira « non-saturation établie pour la
   déclaration choisie », jamais « KSS violée ». Le geste interdit :
   descendre la borne inf sous 2 planchers en invoquant la fourchette
   large pour rapprocher μ_loc du plancher. θ = 0,10 rel gelé avant
   run. Suspense limité mais réel — c'est le dévoilement qui compte.
2. **Premier run** : mot découvert : **S−**, δ = 1,0 = 100 % > 2θ =
   0,20. Le suspense se dévoile : même la borne inf déclarée est à 2
   planchers — la saturation KSS par le QGP n'est PAS établie à
   θ = 0,10 près. Artefacts gelés offline (audits [HOLD] I-G1 / I-G2)
   : `examples/registre/QGP.*`.
3. **Figé** : mot dans `tests/test_open_qgp.py`.

### Le mot : S− — et sa lecture exacte

S− dit : la prétention « le QGP est un fluide parfait qui sature le
plancher KSS » n'est pas dans les données déclarées — même la borne
inférieure de l'extraction la plus favorable se tient à 2 planchers,
soit 100 % au-dessus à θ = 0,10. Ce n'est **pas** « KSS est violée » :
aucune valeur centrale déclarée n'est sous le plancher, et la
fourchette large (0,6-2,5 planchers) reste déclarée comme dette —
l'incertitude chevauche le plancher, mais la machine ne pèse que ce
qui est déclaré comme valeur. Le test verrouille le geste interdit :
la borne inf figée est 2,0 et la référence est le plancher, pas une
valeur de la fourchette large.

### Pourquoi ce contact compte

- **Le premier mot à suspense du tiroir** : les trois contacts
  précédents annonçaient leur mot au protocole (suspense nul) ; celui-
  ci posait une question ouverte (le QGP sature-t-il ?) et le mot y
  répond : non, pas à θ = 0,10 pour la déclaration choisie. La machine
  distingue désormais « S− annoncé » et « S− dévoilé ».
- **La discipline de la fourchette** : peser une borne inf déclarée
  quand la littérature donne un intervalle qui chevauche la référence
  — et écrire que c'est la borne inf qui est pesée, pas l'intervalle —
  est exactement le genre de choix que la doctrine doit rendre
  explicite au lieu de laisser un lecteur hostile le découvrir.
- **Quatre S−, quatre lectures** : la fibre (1, 1) tient le S− de
  marge (KSS ⁴He), le S− de dette (Bertsch), le S− de saturation
  dévoilée (KSS/QGP) et le S− d'écart de modèle (H0) — être loin n'a
  jamais eu autant de nuances.

## Prolongements déclarés (pas montés)

- **Seconde vitesse du son** (⁴He) : c_2² = (ρ_s/ρ_n)(T S²/C) —
  trop de paramètres intermédiaires pour une maquette honnête en
  l'état.
- **Contact exp−théorie à l'unitarité** : une fabrication QMC ou
  expérimentale de ξ (pas une extraction déclarée) permettrait de
  transformer la dette mean-field en test à deux instruments, comme
  CKM et g-2. Besoin : fabrication locale indépendante.
- **Deuxième extraction QGP** : le levier η/s←autre-extraction de
  KSS_EtaS_QGP est déclaré mais non exercé — une autre extraction
  (quenching, transport coefficients récents) produirait le premier
  balayage de levier du tiroir.
