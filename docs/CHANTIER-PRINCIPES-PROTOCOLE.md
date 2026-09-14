# CHANTIER PRINCIPES — protocole gelé avant run (2026-09-14)

## Motif

Les « Principes Fondamentaux de Physique Noétique » (I–V, juin–octobre
2025) contiennent des nombres revendiqués. Le chantier SERRAGE a restauré
la justesse continue ; la machine peut maintenant peser ces revendications
avec la même règle de verdict, sans rien modifier à son protocole.

Population : 4 contacts (série PF). Sources gelées : les affirmations
publiées sont transcrites dans des tables datées (`data/tables/pf*_LITTERATURE-2025.json`),
avec citation du volet et de la date — jamais de pointeur automatique vers
l'archive. Les entrées calculatoires (constantes) sont déclarées dans
`pf_vide_inputs_DECLARED-2026.json`.

## Les 4 contacts (gelés avant run)

1. **PF1_RG_Unification** (volet IV, 2025-08-07). Revendication : avec
   b_noet = +4 (1-loop), b_njn = +10 (2-boucles), k = 0 et
   g_noet(Mz) = 0,50, « les quatre couplages coïncident à ±1 % près :
   g_U = 0,512 à µ_U = 2·10¹⁶ GeV ». La machine n'intègre QUE le 1-loop
   (les coefficients SM à deux boucles ne sont pas gelés dans la source) ;
   elle balaie t de 0 à 36 et consigne la dispersion relative minimale
   des quatre couplages. μ_ref = 0,01 (le ±1 % revendiqué). θ = 0,05
   (barre de la série P : c'est une prédiction d'unification). Le verdict
   S− attendu n'est pas un échec de la machine : c'est la revendication
   1-loop qui est mesurée honnêtement — l'article lui-même renvoie au
   2-boucles.
2. **PF2_Graviton_25THz** (volet II 2025-06-28 × volet V 2025-10-22).
   Pic « graviton noétique » à 25 THz (II) ; masse spectrale des neutrinos
   0,1 eV (V). μ_loc = h·f en eV ; μ_ref = 0,1 eV ; θ = 0,1.
3. **PF3_Tau5_Jeu** (volet V, 2025-10-22). Jeu illustratif :
   « τ5_eff ≈ 10·e^{−0,023·22,67} ≈ 6,0 ». μ_loc = recompute ; μ_ref = 6,0 ;
   θ = 0,1. Vérifie l'arithmétique du jeu numérique, rien de plus
   (jeu illustratif déclaré comme tel par l'article).
4. **PF4_Vide_Catastrophe** (volets IV–V × CODATA 2018 + Planck 2018).
   μ_loc = log10(ρ_Planck/ρ_Λ) calculé depuis les constantes déclarées ;
   μ_ref = 122 (l'exposant revendiqué) ; θ = 0,1.

## Règles du chantier

- Protocole gelé avant run ; erreurs conservées en trace visible.
- Compteurs figés datés ; rien de poussé sans feu vert explicite.
- La machine ne flatte pas : un S− sur une revendication de la théorie
  est une information, pas un accident.
- Pas de moyenne entre contacts.
