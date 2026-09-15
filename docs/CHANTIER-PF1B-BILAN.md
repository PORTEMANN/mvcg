# Chantier PF1b — RG unification au 2-boucles : bilan (2026-09-15)

**Statut : local, non publié.** Protocole gelé avant run :
`docs/CHANTIER-PF1B-PROTOCOLE.md`. PF1 (S− à 655,8 θ) pesait la
revendication « les quatre couplages coïncident à ±1 % : g_U = 0,512 à
μ_U = 2·10¹⁶ GeV » au 1-loop pur ; le volet IV renvoie lui-même au
2-boucles pour la coïncidence. PF1b effectue le calcul désigné : même
transport que PF1, mêmes entrées gelées, seul l'ordre change.

## Population gelée : 1 contact (PF1b) — S− attendu, S− tenu

| Contact | Pesée | μ_loc | μ_ref | Mot |
|---|---|---|---|---|
| PF1b_RG_Unification_2Loop | dispersion min. des 4 couplages au 2-boucles | 0,337 04 | 0,01 | **S− à 654 θ** |

Bilan du chantier : **0 S+, 0 P, 1 S−**. Registre : 82 → 83 contacts,
16 fibres (PF1b rejoint la fibre (si, 1) : S− 1→2 — couplet PF1/PF1b
dans la même case).

## Lecture du verdict

**Le calcul que la source désigne ne ferme pas la dette.** Au
2-boucles, les trois couplages SM se rapprochent effectivement — à
μ_U = 2·10¹⁶ GeV : g₁ = 0,448 5, g₂ = 0,523 7, g₃ = 0,524 4 (la
quasi-unification connue du SM, les termes b₂₃ = 12 et b₁₃ = 8,8
serrant g₂ et g₁ vers g₃). Mais le secteur noétique, sous ses
coefficients déclarés (b_noet = +4 au 1-loop, b_njn = +10 au 2-boucles,
g_noet(Mz) = 0,50), court à **0,656 7** — loin des 0,512 revendiqués
(écart 28 %) et du trio SM. Le spread minimal sur t ∈ [0 ; 36] vaut
0,337 (à t = 23,6) contre 0,337 9 au 1-loop pur : le passage au
2-boucles ne dégrade rien et ne répare rien. δ = 32,7 relatif → **S−
à 654 θ**, miroir quasi exact de PF1 (655,8 θ).

**Information émergente : la revendication a deux dettes, pas une.**
La dette de PF1 n'était pas « mauvais ordre de calcul » : c'est le
quatrième couplage qui écarte le quartet, et ce à tous les ordres
testés. Pour tenir la coïncidence à ±1 %, il faudrait soit un
coefficient noétique très différent de ceux déclarés (lecture non
déclarée — la machine n'en propose pas), soit des termes croisés
noétique × SM que le corpus ne chiffre pas (dettes nommées, gelées à 0
par lecture neutre). Le S− de PF1b est donc un verdict *sur les
coefficients déclarés*, pas sur la possibilité générale d'unifier.

## Ce que le chantier ajoute à la machine

- **Premier contact à coefficients empruntés hors corpus** : la matrice
  b_ij SM (Machacek & Vaughn 1983) n'existe pas dans la source. La
  table gelée date l'emprunt, cite la référence, conserve les fractions
  exactes et nomme la convention. La règle « zéro fetch, zéro pointeur »
  tient : l'emprunt est un acte curatorial gelé, pas une correction en
  silence. Grammaire réutilisable pour tout contact dont le calcul
  désigné exige des constantes standard absentes du corpus.
- **Couplet d'ordres sur une même revendication** : PF1/PF1b est le
  premier couplet « 1-loop / 2-loop » du registre — même transport,
  même θ, même référence, verdicts alignés (654 / 655,8 θ). La machine
  sait maintenant suivre une revendication à travers l'ordre de calcul
  que la source invoque.
- **Intégrateur RK4** : premier runner à intégrer numériquement un
  système couplé (dX_i/dt avec termes croisés), pas une forme close.
  Le pas interne (0,02) est figé dans le code ; la grille de balayage
  (0,1) est identique à PF1.

## Limites, honnêtement posées

- **Emprunt = hypothèse ouverte** : si le corpus entendait une autre
  normalisation des coefficients 2-boucles (ex. b_njn lu dans une
  autre convention), le chiffre changerait. La convention choisie est
  écrite dans la table ; la lecture alternative est nommée dette.
- **Le spread minimal sur grille est généreux** : la revendication
  concerne μ_U = 2·10¹⁶ GeV précisément, où le spread vaut 38,7 % —
  encore plus S−. Le verdict minimal est la borne basse de l'écart.
- **θ = 0,05 repris de PF1** : non serré sur ce contact.

## Traçabilité

- 1 table gelée : `data/tables/pf1b_rg_2loop_LITTERATURE-2026.json`
  (sha256 tracé par `load_table`, fractions exactes MV1983 conservées).
- Verrous figés : `tests/test_principes.py` (μ gelé 0,337 043 559 727
  800 04, attendu S−), `tests/test_verdicts_online.py` (n = 83, fibre
  (si, 1) à {S+1, P0, S−2}), `tests/test_sweep_calibrated.py` (n = 83).
- Cartes régénérées : 83 verdicts, rendu vérifié visuellement.
- Suite complète : 295 tests OK (4 skipped, attendus).
