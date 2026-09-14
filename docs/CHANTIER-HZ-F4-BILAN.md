# Chantier H(z) F4 — bilan (2026-09-14)

**Statut : local, non publié.** Protocole gelé avant run :
`docs/CHANTIER-HZ-F4-PROTOCOLE.md`. Dernier contact lourd de la
prospective (« modulation H(z) par filtrage entropique F4 = 0,035 — forme
de H(z) non spécifiée ») : la forme était en images, elle est transcrite
gelée et pesée. Suite directe du chantier PRINCIPES : mêmes articles
(volets I–V), même méthode (transcription curatorial des images
d'équations, tables gelées datées, zéro fetch dans la machine).

## Population gelée : 2 contacts (PF7–PF8) — un S+ et un S− attendus, les deux tenus

| Contact | Pesée | μ_loc | μ_ref | Mot |
|---|---|---|---|---|
| PF7_F4_Recompute | F₄ = e^(−0,060 × 55,95) recompté depuis le tableau | 0,034840 | 0,035 | **S+** à 0,046 θ |
| PF8_Hz_Filtrage_Ecart | écart max \|H_filtree − H_LCDM\|/H_LCDM, z ∈ [0 ; 2,1] | 0,682723 | 0,02 (borne du texte) | **S−** à 33,1 θ |

Bilan du chantier : **1 S+, 0 P, 1 S−**. Registre : 80 → 82 contacts,
16 fibres (PF7 et PF8 rejoignent la fibre sans dimension (1, 1) — S+ 6→7,
S− 15→16).

## Lecture des verdicts

**PF7 (S+) — l'arithmétique du tableau des plans tient.** Les sept F
recomputés depuis les (β_j, S_j) publiés coïncident avec les F publiés à
δ_max = 0,46 % (E1 : 0,154 28 vs 0,154 ; E2 : 0,601 79 vs 0,601 ; E3 :
0,701 71 vs 0,702 ; E4 : 0,034 84 vs 0,035 ; E5 : 0,711 73 vs 0,712 ;
E6 : 0,824 53 vs 0,825 ; E7 : 0,672 60 vs 0,673). Comme PF3 (jeu τ₅),
la machine vérifie l'arithmétique que la source publie comme jeu
numérique illustratif — pas la physique des plans. L'écart F₄ depuis N₄
direct (e^(−β ln N)) coïncide au tableau : le tableau est arithmétiquement
auto-cohérent.

**PF8 (S−) — la tension équation / revendication.** L'équation image-29
est prise telle que publiée : F₄ = 0,035 multiplie directement
Ω_m(1+z)³. F_U n'est chiffré nulle part dans le corpus — lecture neutre
F_U = 1 gelée dans le protocole, dette nommée (la normalisation
H²(0) = H₀² n'est pas tenue : H²(0)/H₀² ≈ 0,696). Sous cette lecture
gelée, l'écart à ΛCDM vaut déjà **16,6 % à z = 0** et croît jusqu'à
**68,3 % à z = 2,1** — la borne « variation <2 % sur H(z) » du texte
est dépassée dès z = 0, par un facteur 8, puis 34 à z = 2,1. S− à
33,1 θ. Le verdict pèse la tension entre l'équation publiée et la
revendication quantitative qui l'accompagne — pas la cosmologie elle-même
(la revendication <2 % serait tenable sous d'autres lectures de F_U,
mais aucune n'est déclarée dans le corpus).

## Ce que le chantier ajoute à la machine

- **Le corpus des Principes Fondamentaux est épuisé** : PF1–PF8, tous
  pesés. Bilan complet du corpus : 4 S+ (PF2, PF3, PF4, PF7), 0 P,
  4 S− (PF1, PF5, PF6, PF8).
- **Méthode confirmée sur un troisième type d'équation-en-image** :
  transcription gelée → tables datées → contact. Même acte curatorial
  que PSY-RMN, même discipline de traçabilité (sha256, zéro fetch).
- **Fibre (1, 1) désormais à 26 verdicts** — le casier le plus peuplé,
  où se logent les jeux numériques sans dimension et les dettes de
  normalisation. PF8 y apporte un S− de type nouveau : dette de
  *déclaration manquante* (F_U non chiffré), pas dette de valeur.

## Traçabilité

- 3 tables gelées : `pf7_hz_filtrage_LITTERATURE-2025.json`,
  `pf7_hz_inputs_DECLARED-2026.json`,
  `pf7_plans_tableau_LITTERATURE-2025.json` (sha256 tracés par
  `load_table`).
- Verrous figés : `tests/test_principes.py` (μ gelés PF7/PF8),
  `tests/test_verdicts_online.py` (n = 82, fibre (1, 1) à
  {S+7, P3, S−16}), `tests/test_sweep_calibrated.py` (n = 82),
  `tests/test_serrage_serie_o.py` (PF7 rejoint la population serrée).
- Cartes régénérées : 82 verdicts, rendu vérifié visuellement.
- Suite complète : 294 tests OK (4 skipped, attendus).
