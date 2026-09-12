# O15 — quinzième contact ouvert : l'harmonique du H2 et sa dette

Un contact **ouvert** = le mot n'est pas connu au gel. O15 pèse le
geste le plus ancien de la chimie quantique : l'oscillateur harmonique
appliqué à la vibration de H2 — avec un contrat d'honnêteté explicite.

## Chronologie du gel

1. **Protocole écrit avant toute exécution** : règle déclarée —
   oscillateur harmonique, ν_harm = √(k/μ)/(2πc), k = 510 N/m
   (constante de force de Morse au minimum, valeur usuelle déclarée
   dans la table), μ = m_H/2 ; **comparaison honnête** : contre
   ω_e = 4401,2 cm⁻¹ (constante harmonique expérimentale), PAS contre
   le fondamental anharmonique (4160 cm⁻¹, porté par la note de la
   table, hors contrat) ; la cible ω_e NE DOIT JAMAIS entrer dans le
   calcul ; θ = 0,10 figé avant run. Estimation pré-run honnête :
   l'harmonique pur sous-estime ω_e d'environ 6 % — la dette
   anharmonique attendue.
2. **Premier run** : mot découvert : **S+**, δ ≈ 5,8 %.
   Artefacts gelés offline (audit [HOLD] I-G1 / I-G2) :
   `examples/registre/O15.*`.
3. **Figé** : mot dans `tests/test_open_o15.py`.

## Le mot : S+ — et pourquoi le test verrouille l'honnêteté

μ_loc = 4144,5979 cm⁻¹ (harmonique pur à k = 510 N/m) contre
μ_ref = 4401,2 cm⁻¹ (ω_e expérimentale). δ ≈ 5,8 % : sous θ, donc S+.
Mais le même calcul comparé au fondamental anharmonique (4160) donnerait
~0,4 % — un « faux S+ » bien plus flatteur. Le test fige le contrat :
la référence est ω_e, la dette anharmonique est réelle (~6 %), et la
comparaison « maline » au fondamental est écartée par construction.
La machine ne choisit pas sa référence après coup.

## Levier : k←Morse

Le levier déclaré : remplacer la constante harmonique par le potentiel
de Morse complet (k au minimum + anharmonicité), qui reproduit à la
fois ω_e et le fondamental. La dette de 5,8 % est exactement ce que
l'anharmonicité ω_e·x_e ≈ 121 cm⁻¹ explique — le levier est quantifié
par le mot lui-même.

## Pourquoi O15 compte

C'est le premier contact dont le **contrat de comparaison** fait
partie du gel : deux références plausibles existaient (ω_e et ν₀),
et le protocole en a choisi une *avant* le run, quand le résultat
était encore inconnu. Si l'honnêteté n'est pas protocolisée, le
verdict devient un choix après coup. O15 est donc autant un contact de
vibration moléculaire qu'un contact de **méthode** — le pendant
disciplinaire d'O13 (qui séparait table et règle).
