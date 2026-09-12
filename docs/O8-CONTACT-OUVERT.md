# O8 — huitième contact ouvert : la température critique du gaz de Bose

Un contact **ouvert** = le mot n'est pas connu au gel. O8 est le premier
contact de la série à porter sur une **transition de phase** : non plus
une bande ou une vitesse, mais la température où le condensat apparaît.

## Chronologie du gel

1. **Protocole écrit avant toute exécution** : règle déclarée — gaz de
   Bose idéal, T_c = (2πħ²/mk_B)·(n/2,612)^{2/3} ; masse ⁸⁷Rb et
   n = 3·10¹⁹ m⁻³ de la table `bec_tc_LITERATURE-2018.json` (même nuage
   déclaré qu'O5) ; θ = 0,10 figé avant run ; référence = T_c observée
   170 nK. La référence ne participe jamais au calcul. Suspense déclaré
   réel au gel : les interactions (a_s > 0) déplacent T_c de quelques
   pourcents à plus de 10 % selon les mesures.
2. **Premier run** : mot découvert : **S+**, δ ≈ 5,01 % — tenu de
   justesse : la zone P commence à 10 %. Artefacts gelés offline
   (audit [HOLD] I-G1 / I-G2) : `examples/registre/O8.*`.
3. **Figé** : mot dans `tests/test_open_o8.py`.

## Le mot : S+ tenu de justesse

μ_loc = 178,53 nK (gaz idéal à n = 3·10¹⁹ m⁻³) contre μ_ref = 170 nK :
le gaz idéal **surestime** T_c de 5 % — ce qui est exactement le signe
attendu des interactions répulsives (elles stabilisent le condensat,
abaissant T_c dans les mesures ? non : elles l'élèvent théoriquement en
basse densité...). Le contact ne tranche pas la direction de la
correction — il dit : à 5 % près, l'idéal tient le seuil inter-labo, et
la dette d'interaction est encore sous le θ gelé.

## Levier : n←densité-effective

T_c ∝ n^{2/3} : monotone, échelle exacte vérifiée (n × 2,25 → T_c ×
2,25^{2/3}). Point de bascule vers P : T_c = 187 nK ↔ n ≈ 3,5·10¹⁹
m⁻³ (+17 % de densité). La même densité que la paire O5/O11 pilote
trois contacts : la cohérence du nuage déclaré est vérifiable en
croisant les trois mots (S+, P au seuil, S+).

## Pourquoi O8 compte

O5 a pesé une **réponse** du condensat (vitesse du son) ; O8 pèse sa
**naissance** (T_c) ; O11 pèse sa **échelle de cohérence** (ξ). Le même
objet physique, trois grandeurs, trois mots découverts — c'est la
définition d'un échantillon bien pesé.
