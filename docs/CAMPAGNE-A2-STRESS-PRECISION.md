# CAMPAGNE A2 — stress de précision sur les divergences home/balayage (prototype local, 2026-09-14)

Question ouverte par la coloration par unité : le street sweep des 46
contacts sous les 4 paquets HL/Gauss/SI/1 donne des mots identiques
partout **sauf CKM, HVP_LO et HLbL**. Effet numérique (arrondi de
conversion) ou effet protocolaire ? Réponse : **protocolaire, à 100 %,
et le numerique est innocenté à 5,6e-17 près.**

Script : `campagne_a2_stress_precision.py` (résultat :
`a2_stress_precision.json`). Campagne dérivée : aucun contact nouveau,
aucun gel touché.

## 1. Le mécanisme — le sweep ne voit pas la couche GUM

`verdict_register.street_sweep` ne ré-exécute pas le runner sous
d'autres unités. Il reprend (μ_loc, μ_ref) du run maison et re-décide
avec `_verdict(δ, θ)` — **sans le GUM**. Pour un contact `decide="U"`,
le seuil maison est U = k·u_c et le seuil sweep est θ : les deux mots
ne sont pas censés coïncider quand U ≠ θ.

Règle vérifiée sur les 7 contacts `decide="U"` du registre — les 7
obéissent, sans exception :

| Contact | U/θ | home | sweep | Divergence | Pourquoi |
|---|---|---|---|---|---|
| CKM unitarité | 2,0000 | P | S− | **oui** | seuil sweep = θ = U/2 (deux fois plus strict) |
| HVP LO lat vs e⁺e⁻ | 2,0012 | P | S− | **oui** | idem (θ = 72,9 ≈ u_c = 72,945 déclaré arrondi) |
| HLbL lat vs pheno | 1,9980 | S+ | P | **oui** | idem |
| AMU Δ WP25 | 1,0000 | S+ | S+ | non | θ déclaré = U (k = 1) — mêmes seuils |
| AMU exp − WP20 | 1,0000 | S− | S− | non | idem |
| H1s Rydberg | 3,8000 | S+ | S+ | non | δ = 0 — insensible au seuil |
| P27 He HF | 0,0010 | S− | S− | non | δ = 21 θ — au-delà des deux régimes de seuil |

Preuve complémentaire : la re-décision `_adc(δ_maison, θ)` reproduit
exactement le mot sweep dans les 7 cas (`regle=True` partout). Le sweep
est un instrument à seuil θ ; le run maison est un instrument à seuil
U quand le contact le déclare. Comparer leurs mots, c'est comparer deux
étalonnages — c'est exactement ce que dit la doctrine (deux instruments
divergents documentés).

## 2. Le stress numérique — float64 innocenté

Recombinaison des budgets GUM en `decimal` (30 chiffres) vs float64 :

| Contact | écart relatif u_c | marge la plus mince |
|---|---|---|
| CKM | 0,0 | 0,29σ = 14,3 % du seuil |
| HVP LO | 3,6e−17 | 0,76σ = 37,8 % du seuil |
| HLbL | 5,6e−17 | 0,47σ = 23,7 % du seuil |

Le bruit numérique (~1 ulp) est à **~16 ordres de grandeur** sous la
marge la plus mince. Aucun arrondi de conversion d'unités ne peut
faire basculer un mot du registre. L'invariance unitaire annoncée
(43/46 identiques) devient, une fois la couche de décision tenue
constante : **46/46 invariants en numérique**.

## 3. Enseignements

1. **Les trois « divergences home/balayage » sont expliquées** — elles
   ne sont ni des bugs ni des effets flottants : c'est la comparaison
   de deux instruments à seuils différents (U vs θ), documentée par la
   doctrine depuis le jour J. La campagne A2 transforme la remarque en
   preuve.
2. **Le sweep historique compare des étalonnages, pas des unités.**
3. **Corollaire pour la carte** : la couche épaisseur (marge en σ,
   seuil U) et la géométrie δ/θ (seuil θ) sont deux lectures légitimes
   d'un même contact ; les trois contacts divergents vivent dans
   l'écart entre les deux — c'est une information, pas une contradiction.

## 4. Chantier soldé le 2026-09-14 — le balayage calibré

Le chantier identifié au §3.2 est monté, en local :

- `dictionaries.sweep_contact` gagne un paramètre `thr` (défaut None =
  θ seul — comportement historique **inchangé**, les gels « deux
  instruments » de test_verdicts_online ne sont pas touchés) ;
- `verdict_register.street_sweep_calibrated` rejoue le balayage au
  seuil gelé du contact (U si decide=U, θ sinon, règle `_thr_contact`
  partagée avec la couche épaisseur de `carte.py`) ;
- `tests/test_sweep_calibrated.py` fige l'invariance **46/46 à même
  étalonnage** (4 paquets licites, mot == home partout), thr CKM = U =
  0,0014, et la restoration des mots home pour HVP/HLbL.

Leçon de discipline : le premier jet du test écrivait les mots attendus
(P, S+) en boucle à côté des ids — la garde anti-tautologie de
`test_reproduce` (`expected_word` doit dire « non isolable » pour HVP)
l'a attrapé. **Un test ne porte jamais le mot d'un contact voisin : on
compare au registre live.** Corrigé avant consignation.

Suite complète après chantier : **206 tests OK** (203 + 3 nouveaux),
4 skippés réseau. Non commité à ce stade ; publication = décision
indépendante.

## Limites

1. Le stress numérique porte sur les budgets GUM recombines, pas sur
   chaque conversion de paquet du runner (les conversions de μ sont
   gelées dans les runners ; les vérifier une à une serait la campagne
   A2-bis).
2. Campagne locale : non commitée à ce stade ; la décision de
   publication est indépendante.
