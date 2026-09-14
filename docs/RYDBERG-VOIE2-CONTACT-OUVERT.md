# Rydberg voie 2 — R∞ depuis α et m_e c² : le pendant du Dunham pour la constante fondamentale

Contact **ouvert** (mot découvert, pas choisi). Gelé en exploration
locale le 2026-09-14 — troisième brique de la **campagne croisée** :
deux voies vers la même constante de Rydberg, la spectroscopie
(table codata2018_extract, contact H1s_Rydberg) et le calcul depuis
les constantes fondamentales (cette voie).

## La règle

μ_loc = R∞ en eV **calculé** : R∞ = α² m_e c² / (2e), avec α =
7,2973525693(11)×10⁻³ et m_e c² = 8,1871057769(25)×10⁻¹⁴ J (CODATA
2018, incertitudes déclarées dans la table), e exacte (SI).
μ_ref = Rydberg_eV déclaré du même tableau. GUM : decide=U, k=1,
θ = u_delta = quadrature de l'incertitude propagée (2·u_α/α et
u_me/me dominent : u_rel ≈ 4,3×10⁻¹⁰) et de l'incertitude déclarée
de la référence.

## Dette de circularité — écrite avant le run

α, m_e c² et Rydberg_eV participent du **même ajustement CODATA-2018**.
Ce contact mesure la **cohérence interne du catalogue**, exactement
comme le contact SPEC_CO_Rot_Dunham (S+ à 0,028 θ, dette écrite au
gel) — il ne mesure pas une prédiction indépendante. C'est voulu :
la fibre eV du registre gagne sa case de certification, et les
contacts qui la citent (H1s_Rydberg et ses leviers) peuvent s'appuyer
sur un chiffre de cohérence pesé, pas déclaré.

## Chronologie du gel

1. **Protocole écrit avant toute exécution** : règle déclarée ci-dessus ;
   θ = u_delta gelée = 5,838364428925748×10⁻⁹ eV (calcul déterministe
   depuis les incertitudes déclarées de la table, écrite dans la table).
   **Suspense annoncé nul** : cohérence interne attendue à δ/U ≈ 0,02 —
   c'est un contact de certification catalogue, pas un contact de
   suspense. L'estimation n'en est pas moins écrite : S+ attendu à
   ~0,02 U.
2. Premier run : mot découvert, figé dans `tests/test_open_rydberg_voie2.py`.
3. Figé : mot + θ + règle dans le test.

## Lecture attendue

Un S+ quasi parfait dira : le catalogue CODATA-2018 est cohérent avec
lui-même à l'échelle 10⁻¹⁰ relative pour la constante de Rydberg —
certification pesée de la fibre. Ce serait un défaut du protocole que
de chercher un autre mot ici : l'honnêteté du contact est sa dette
écrite, pas son suspense.
