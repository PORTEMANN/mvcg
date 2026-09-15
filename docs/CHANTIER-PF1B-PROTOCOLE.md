# Chantier PF1b — RG unification au 2-boucles : protocole gelé (2026-09-15)

**Statut : gelé avant run. Local, non publié.** Suite du chantier
PRINCIPES : PF1 (S− à 655,8 θ) pesait la dispersion 1-loop pure contre
la revendication « les quatre couplages coïncident à ±1 % : g_U = 0,512
à μ_U = 2·10¹⁶ GeV ». Le texte du volet IV renvoie lui-même au
2-boucles pour la coïncidence. PF1b effectue le calcul désigné : même
transport que PF1, même entrées gelées 1-loop, seul l'ordre change.

## Ce qui est emprunté (trace écrite, pas correction en silence)

Les coefficients SM au 2-boucles **ne sont pas dans le corpus**. Ils
sont empruntés à la littérature standard (Machacek & Vaughn 1983,
conventions PDG 2020, g₁ en normalisation GUT), gelés datés dans
`data/tables/pf1b_rg_2loop_LITTERATURE-2026.json` avec les valeurs
exactes en fractions et leur arrondi gelé. Convention :
dg_i/dt = g_i³/(16π²) [b_i + Σ_j b_ij g_j²/(16π²)], t = ln(μ/Mz).

Dettes nommées dans la table : termes croisés secteur noétique × SM non
déclarés → 0 gelé (lecture neutre) ; b_njn = +10 lu comme coefficient
2-boucles diagonal du secteur noétique dans la même normalisation que
b_noet = +4.

## Calcul préparatoire du protocole (avant runner)

Intégration RK4 de dX_i/dt = −(1/2π)[b_i + Σ_j b_ij/X_j], X = 4π/g²
(forme équivalente de la convention ci-dessus) :

- **à μ_U = 2·10¹⁶ GeV** : g = (0,4485 ; 0,5237 ; 0,5244 ; 0,6567) —
  spread = **38,7 %** contre ±1 % revendiqué ; g_noétique = 0,6567 contre
  g_U = 0,512 revendiqué (écart 28 %).
- **spread minimal sur t ∈ [0 ; 36]** : **0,337 à t = 23,6**
  (le 1-loop pur donnait 0,3379 — le 2-boucles ne dégrade pas mais ne
  répare rien).

## Population gelée : 1 contact (PF1b)

### PF1b_RG_Unification_2Loop — la coïncidence au calcul désigné

- **μ_loc** : dispersion relative minimale des 4 couplages au
  2-boucles sur la même grille que PF1 (transport strictement identique,
  autre ordre — grammaire O18/O19/O20).
- **μ_ref** : 0,01 (la revendication, inchangée).
- **Ce que la machine pèse** : si le calcul que la source désigne elle-
  même tient la coïncidence. Les trois couplages SM se rapprochent au
  2-boucles (0,448 / 0,524 / 0,524 à μ_U — la quasi-unification connue
  du SM), mais le secteur noétique, sous ses coefficients déclarés
  (b_noet = +4, b_njn = +10), court à 0,657 et écarte le quartet.
- Attendu gelé : **S−** (δ ≈ 0,327 à θ = 0,05 → ≈ 6,5 θ, au-delà de la
  borne P à 2 θ ; le 2-boucles ne ferme pas la dette de PF1).
- θ = 0,05 (identique à PF1 — la revendication est la même).

## Règles

- 1 table gelée datée (LITTERATURE-2026), sha256 tracé par `load_table` ;
  zéro fetch dans la machine ; emprunt littérature écrit dans la source
  de la table, valeurs exactes conservées.
- Extras attendus dans le run : spread à μ_U revendiqué, g_i(μ_U),
  g_noet(μ_U) vs g_U = 0,512, comparaison 1-loop vs 2-loop du best
  spread.
