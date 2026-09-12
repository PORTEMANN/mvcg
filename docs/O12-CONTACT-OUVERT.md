# O12 — douzième contact ouvert : la chaleur électronique du cuivre

Un contact **ouvert** = le mot n'est pas connu au gel. O12 est le
contact le plus chargé d'histoire de la série : le S− qu'il découvre
est celui qui, dans les années 1950, a obligé la physique des solides à
inventer la **masse effective**.

## Chronologie du gel

1. **Protocole écrit avant toute exécution** : règle déclarée —
   modèle de Sommerfeld avec **masse libre** (m_e, écrite dans le
   runner), γ = π²k_B²n/(2E_F), E_F = ħ²(3π²n)^{2/3}/(2m_e) ; densité
   électronique du cuivre n = 8,47·10²⁸ m⁻³ de la table
   `cu_gamma_LITERATURE-2018.json` ; θ = 0,10 figé avant run ;
   référence = γ mesuré 96,6 J·m⁻³·K⁻². La référence ne participe
   jamais au calcul. Estimation pré-run honnête : sous-estimation
   attendue ~27 % — c'est l'ecart historique.
2. **Premier run** : mot découvert : **S−**, δ ≈ 26,8 %.
   Artefacts gelés offline (audit [HOLD] I-G1 / I-G2) :
   `examples/registre/O12.*`.
3. **Figé** : mot dans `tests/test_open_o12.py`.

## Le mot : S− historique

μ_loc = 70,71 J·m⁻³·K⁻² (masse libre) contre μ_ref = 96,6 (cuivre
mesuré). Le modèle de l'électron libre — celui qui donne E_F ≈ 7 eV
correct — sous-estime la chaleur électronique d'un facteur ~1,37 :
exactement le rapport m*/m_e du cuivre. Le S− dit : **la masse libre
est une dette structurelle**, pas une erreur de calcul. C'est le même
type de mot qu'O4 (frontière de loi) mais plus profond : ici la loi est
correcte et c'est le *paramètre* (la masse) qui est faux — l'inverse du
geste O7 où le paramètre r=3 réparait le modèle.

## Levier : m←masse-effective

γ ∝ m_eff : le test calcule m* = γ_ref/γ_modèle ≈ 1,37 m_e — dans la
fenêtre 1,30–1,45 de la littérature du cuivre. Le levier recommande :
une masse effective de bande, jamais un θ déplacé. (Un contact O13
« levier activé » avec m* = 1,37 déclarée serait le pendant d'O7 —
mais il attendra : trois S+ d'affilée suffisent pour aujourd'hui.)

## Pourquoi O12 compte

La série a désormais pesé : un atome, deux molécules, un réseau
désordonné, une loi empirique du carbone, un fluide quantique (trois
grandeurs), un polymère, et un **solide**. Le S− d'O12 est le premier
qui pointe vers une quantité que la métrologie ne mesure pas directement
(la masse effective se déduit) — le registre commence à peser des
objets dont la référence est elle-même un modèle. C'est le bord
intéressant.
