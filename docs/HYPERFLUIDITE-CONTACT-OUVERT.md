# Hyperfluidité — contact ouvert : la vitesse critique de Landau du ⁴He

Contact **ouvert** (mot découvert, pas choisi) — exploration locale,
non publiée. Premier contact du tiroir hyperfluidité : la condition de
Landau (1941) appliquée au spectre phonon-roton déclaré de ⁴He II.

## Chronologie du gel

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

## Pourquoi ce contact compte

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

## Prolongements déclarés (pas montés)

- **Paramètre de Bertsch ξ** (gaz unitaire) : ξ_BCS = 0,5905 vs
  ξ_exp ≈ 0,370 → S− probable au θ = 0,10 — pendant de P27
  (l'ansatz pauvre rate), besoin : table ξ vintage.
- **Borne KSS η/s** : le plancher ℏ/4πk_B n'est pas une identité ;
  la règle devra le dire. Besoin : table η/s déclarée.
- **Seconde vitesse du son** (⁴He) : c_2² = (ρ_s/ρ_n)(T S²/C) —
  trop de paramètres intermédiaires pour une maquette honnête en
  l'état.
