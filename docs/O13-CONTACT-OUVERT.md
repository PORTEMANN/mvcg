# O13 — treizième contact ouvert : l'isotopologue du CO2

Un contact **ouvert** = le mot n'est pas connu au gel. O13 pèse la
première **prédiction isotopique** de la série : non plus comparer un
modèle à une mesure, mais dériver la mesure d'un isotopologue depuis
celle d'un autre.

## Chronologie du gel

1. **Protocole écrit avant toute exécution** : règle déclarée —
   déplacement isotopique par la loi des masses,
   ν(13CO2) = ν(12CO2)·√(μ12/μ13), μ = m_C·m_O/(m_C+m_O), masses
   conventionnelles 12/16 et 13/16 ; la bande cible du 13CO2
   (2273,7 cm⁻¹) est stockée dans la table mais NE DOIT JAMAIS entrer
   dans le calcul — seule la bande du 12CO2 (2349,3 cm⁻¹) pilote ;
   θ = 0,10 figé avant run ; référence = bande observée du 13CO2.
   Estimation pré-run honnête : écart ~1 % (dettes anharmoniques
   résiduelles).
2. **Premier run** : mot découvert : **S+**, δ ≈ 1,03 %.
   Artefacts gelés offline (audit [HOLD] I-G1 / I-G2) :
   `examples/registre/O13.*`.
3. **Figé** : mot dans `tests/test_open_o13.py`.

## Le mot : S+

μ_loc = 2297,0868 cm⁻¹ (loi des masses depuis le 12CO2) contre
μ_ref = 2273,7 cm⁻¹ (bande ν₃ du 13CO2 observée). La constante de
force est pratiquement inchangée entre isotopologues : la fréquence
suit la masse réduite. L'écart résiduel de ~1 % est exactement l'ordre
de grandeur des couplages anharmoniques — la dette est petite, déclarée
et située sous θ.

## Levier : k←anharmonicité

Le levier recommande une constante de force isotopiquement ajustée
(jamais un θ déplacé). C'est la version douce du geste d'O12 : là où
le cuivre exigeait une masse effective (~37 %), le CO2 ne demande
qu'une correction anharmonique (~1 %). Même famille de mots, échelles
très différentes — le registre commence à cartographier *l'amplitude*
des dettes, pas seulement leur existence.

## Pourquoi O13 compte

C'est le premier contact où la **référence elle-même n'entre pas dans
le calcul** tout en étant stockée dans la même table : le test
anti-tautologie le verrouille (retirer la cible ne change rien). La
machine distingue désormais « table » et « règle » — elle peut porter
une réponse sans la lire. C'est le prérequis de tout contact où la
référence serait inconnue au moment du calcul.
