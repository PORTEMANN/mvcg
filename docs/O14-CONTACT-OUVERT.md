# O14 — quatorzième contact ouvert : Tuinstra–Koenig dans sa fenêtre

Un contact **ouvert** = le mot n'est pas connu au gel. O14 est le
pendant d'O4 : **même loi, autre échantillon** — la loi de
Tuinstra–Koenig pesée au cœur de sa fenêtre de validité.

## Chronologie du gel

1. **Protocole écrit avant toute exécution** : règle déclarée —
   I_D/I_G = C(λ)/L_a avec C = 4,4 nm (même constante empirique
   qu'O4, aucune recalibration) et L_a = 10 nm (charbon graphitisé,
   cœur de la fenêtre de phase 1) ; le rapport observé (0,45) est
   stocké dans la table mais NE DOIT JAMAIS entrer dans le calcul ;
   θ = 0,10 figé avant run ; référence = rapport observé de
   l'échantillon. Estimation pré-run honnête : écart ~2 %.
2. **Premier run** : mot découvert : **S+**, δ ≈ 2,2 %.
   Artefacts gelés offline (audit [HOLD] I-G1 / I-G2) :
   `examples/registre/O14.*`.
3. **Figé** : mot dans `tests/test_open_o14.py`.

## Le mot : S+

μ_loc = 0,44 (C/L_a à 10 nm) contre μ_ref = 0,45 (rapport observé).
Là où O4 pesait la loi à 3 nm — sur un nanodiamant, hors de sa
phase — et découvrait un S− frontière de loi, O14 la pèse à 10 nm,
en plein cœur de la fenêtre : la loi tient. Même constante C, deux
échantillons, deux verdicts : la loi devient une **carte** avec
un domaine de validité, pas une formule universelle.

## Levier : La←recalibrer

Le levier déclaré reste un recalibrage de L_a (jamais un θ déplacé) :
la dette résiduelle de 2 % peut se lire comme une incertitude de
~2 Å sur la taille de domaine — métrologiquement banale, physiquement
sans conséquence.

## Pourquoi O14 compte

Avec O4, le registre a désormais pesé une même loi **des deux côtés
de sa frontière** : S− à 3 nm, S+ à 10 nm. C'est la première paire
« carte » de la série — elle montre que le verdict n'est pas une
étiquette globale sur une loi, mais une mesure locale dans le plan
des paramètres. Le S+ d'O14 n'annule pas le S− d'O4 : les deux sont
vrais, à des endroits différents du plan (L_a, phase).
