# O2 — deuxième contact ouvert : ν₃(CO₂) par transfert de constante de force

Un contact **ouvert** = le mot n'est pas connu au moment où le protocole
est gelé. O2 applique la même discipline qu'O1 à un objet de physique
moléculaire : une bande IR (ν₃ du ¹²CO₂, 2349,3 cm⁻¹) mesurée par une
règle de force déclarée a priori — un **transfert de constante de force**
de la liaison C≡O du CO vers les liaisons C=O du CO₂.

## Chronologie du gel (ordre qui fait la valeur)

1. **Protocole écrit avant toute exécution** :
   - table gelée `co2_bands_LITERATURE-2018.json` (bandes textbook
     CO, CO₂, isotopologue ¹³C) ;
   - règle déclarée : **k_r(C=O du CO₂) := k(CO)**, extraite de la
     bande CO par le modèle diatomique harmonique k = μω²
     (μ = m_C·m_O/(m_C+m_O) = 6,857 amu) ;
   - modèle prévisionnel : ν₃^harm = √(2k_r/m_O)/(2πc), force centrale
     1D, masses conventionnelles 12,0 / 16,0 amu ;
   - θ = 0,10 rel **figé avant le run**. Rationale déclaré : tolérance
     « entre labo » (accord inter-laboratoires sur les bandes) × modèle
     1D volontairement grossier. Pas de nom de calibre : c'est un
     compromis documenté, pas un étalon ;
   - **anti-tautologie structurelle** : la bande ν₃ du CO₂ ne doit
     jamais entrer dans le calcul. Seule la bande CO pilote k_r.
     La référence et la prédiction restent dans la même table sans
     se toucher.
2. **Premier run** : mot découvert, pas choisi : **P**,
   δ ≈ 14,48 % (zone 0,10 < δ ≤ 0,20). Artefacts gelés (offline) :
   `examples/registre/O2.{bits,units,metric,cost}.json` — audit
   relançable : `[HOLD] I-G1`, `[HOLD] I-G2`.
3. **Figé** : le mot entre dans le test `test_open_o2.py`, comme pour
   tout contact du registre. Après le gel, reclassement = autre D.

Estimation honnête pré-run : k_CO ≈ 19 mdyn/Å → ν₃ ≈ 2 000 cm⁻¹,
δ ≈ 14–15 % : zone **P** la plus probable, S+ et S− vivants. Le run a
confirmé la zone P sans toucher aux bornes.

## Le mot : P

μ_loc = 2009,21 cm⁻¹ (VFF harmonique à k transférée) contre
μ_ref = 2349,3 cm⁻¹ (bande observée du ¹²CO₂). L'écart relatif
δ = 14,48 % dépasse le seuil S+ (10 %) sans atteindre le double (20 %).

Lecture phénoménologique : le transfert de constante de force **sous-estime
systématiquement** ν₃ — le couplage ν₃/ν₁ (mixing Fermi-adjacent), la
double dégénérescence du mode et l'anharmonicité déplacent la bande
au-delà de ce qu'un ressort harmonique indépendant peut porter. Le mot P
dit exactement ça : la règle est au bon ordre de grandeur (le transfert
n'est pas absurde, contrairement à un S−), mais le seuil labo exige plus
que le modèle 1D déclaré.

## Le levier : k←autre-liaison

Le levier gelé dit ce qu'il faudrait changer : **une meilleure constante
de liaison déclarée**, jamais θ. Le test de levier (hors gel) vérifie la
monotonie : ν₃ ∝ √k_r ∝ ν(CO) — une bande CO déclarée plus haute pousse
ν₃ strictement vers le haut. Pour passer de P à S+ il faudrait k_r plus
forte d'environ (2349,3/2009,2)² ≈ 1,37 — une constante de liaison 37 %
plus dure que celle du CO, ce qui n'est **pas** une correction de modèle
raisonnable (une liaison C=O du CO₂ n'est pas plus dure que C≡O) : le P
est donc structurel, pas un artefact de paramétrage.

## Règles de lecture

- **Un P ouvert est la réponse la plus informative** : la machine distingue
  « bonne règle, mauvaise finesse » d'« identité » (S+) et de « règle
  à jeter » (S−). C'est le verdict qui demande un travail conceptuel.
- **Rejouer O2** : `python3 -m mvcg registers` — tout tiers obtient le
  même mot avec les mêmes bits gelés, la même table, la même règle.
- **Ajouter un contact = le seul signal d'appropriation** : sa molécule,
  sa table, son θ gelé avant le run.

## Pourquoi O2 compte

O1 montrait qu'un S− peut être un artefact de discrétisation. O2 montre
qu'un contact chimique « entre labo » peut rester **ouvert** avec une
tolerance honnête : θ = 10 % n'est pas un seuil mou choisi pour passer,
c'est la tolérance que deux laboratoires s'accordent sur une bande IR —
et le modèle déclaré ne la remplit pas. La machine a risqué un
quantitatif sur un objet phénoménologique, et elle a perdu proprement :
le mot P est une dette de modèle, pas une erreur de mesure.
