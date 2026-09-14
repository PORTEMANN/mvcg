# Chantier PRINCIPES — bilan (2026-09-14)

**Statut : local, non publié.** Protocole gelé avant run :
`docs/CHANTIER-PRINCIPES-PROTOCOLE.md`. Première pesée transposant les
cinq articles « Principes Fondamentaux de Physique Noétique » (I–V,
juin–oct 2025) en contacts de la machine. La machine pèse les nombres
publiés ; les équations des articles sont en images — seuls les nombres
du texte courant sont pesables. Pas de pointeur automatique vers
l'archive : les tables citent les volets par date, comme Lundeen-Pipkin.

## Population gelée : 4 contacts (PF1–PF4)

| Contact | Revendication pesée | μ_loc | δ | θ | Mot |
|---|---|---|---|---|---|
| PF1_RG_Unification | coïncidence des 4 couplages à ±1 % à 2·10¹⁶ GeV | 0,337925 | 32,79 | 0,05 | **S−** (attendu S−) |
| PF2_Graviton_25THz | E = h·f du pic 25 THz = 0,1 eV (II × V) | 0,103392 eV | 0,0339 | 0,10 | **S+** |
| PF3_Tau5_Jeu | recompute 10·e^(−0,023·22,67) ≈ 6,0 (jeu illustratif, V) | 5,93683 | 0,0105 | 0,10 | **S+** |
| PF4_Vide_Catastrophe | log₁₀(ρ_Planck/ρ_Λ) = 122 (V) | 122,945 | 0,0077 | 0,10 | **S+** |

Bilan : **1 S−, 3 S+**. Nouvelle fibre (si, 1) ouverte ; la fibre (si, eV)
passe à 5 S+ (PF2) ; la fibre (1, 1) à 6 S+ (PF3). Registre : 74 → 78
contacts, 14 fibres.

## Lecture des verdicts

**PF1 (S− à 655,8 θ).** La machine intègre le flux 1-loop gelé
(g₁=0,3570, g₂=0,6529, g₃=1,217, g_noet=0,50 ; b = 41/6, −19/6, −7, +4)
et mesure la dispersion relative minimale des quatre couplages sur
t ∈ [0, 36] : **33,8 %**, atteinte à μ ≈ 2,8·10¹⁴ GeV — et à l'échelle
revendiquée (2·10¹⁶ GeV) les quatre couplages valent ≈ 0,60, 0,52, 0,93,
0,28 : la coïncidence à 1 % **n'est pas tenue au 1-loop pur**. Ce n'est
pas un accident de la machine : l'article IV renvoie lui-même au
2-boucles pour la coïncidence, et les coefficients SM 2-boucles ne sont
pas gelés dans la source. Le S− pèse exactement ce que la source
revendique au niveau d'approximation où elle le revendique : un écart
nommé, pas une réfutation. C'est la lecture dominante de ce chantier :
le verdict dit *où* la revendication habite dans son propre espace de
calcul.

**PF2 (S+ à 0,34 θ).** Contact de cohérence interne entre deux volets :
le pic « graviton noétique » à 25 THz (II), transcrit en masse spectrale
par E = h·f avec h gelé CODATA-2018, donne **0,1034 eV** contre 0,1 eV
posé (V). Correction conservée en trace : le « P annoncé » de ma note de
montage venait d'une division par 10 erronée (0,0339/0,10 = 34 % < θ) ;
le mot du run est S+. La machine vérifie que deux volets du corpus se
citent correctement — elle ne mesure pas un spectre.

**PF3 (S+ à 0,11 θ).** Recompute arithmétique du jeu numérique
illustratif que l'article V déclare comme tel : 10·e^(−0,023·22,67) =
**5,9368** contre ≈ 6,0 annoncé. La machine vérifie l'arithmétique du
jeu, pas la physique. Déclaration de portée écrite dans le contact.

**PF4 (S+ à 0,08 θ).** log₁₀(ρ_Planck/ρ_Λ) recompute depuis les
constantes déclarées (CODATA-2018 + Planck-2018, table
DECLARED-2026) : ρ_Planck = c⁷/(ħG²) = 4,63·10¹¹³ J/m³,
ρ_Λ = Ω_Λ·ρ_crit·c² = 5,25·10⁻¹⁰ J/m³, ratio = **122,945** contre 122
revendiqué. Les densités annoncées (10¹¹³ / 10⁻⁹) sont des ordres de
grandeur ; l'exposant est la grandeur précise, et il tient à 0,8 % —
le meilleur S+ du chantier.

## Verrous techniques

- 5 tables gelées datées (LITTERATURE-2025 ×4, DECLARED-2026 ×1),
  sha256 tracés : pf1 `2e210107…`, pf2 `16d3a1e3…`, pf3 `ef016c79…`,
  pf4 `102a73f0…`, inputs `693fb647…`.
- `src/mvcg/principes.py` : 4 runners déterministes, relisent les tables
  gelées, zéro fetch. Bug du scan PF1 trouvé et corrigé en trace
  visible : `g_at_claim` n'était calculé que si le balayage tombait
  exactement sur t_claim = ln(2·10¹⁶/Mz) ≈ 33,02 (non multiple de 0,1 —
  valeur toujours None) ; le calcul est maintenant direct, le test
  `test_pf1_spread_1loop` fige la valeur.
- Suite complète verte après intégration : **290 tests, 0 failure**
  (compteurs figés 74→78, population SERRAGE 10→13 avec PF2/3/4,
  fibres 13→14, test sweep calibré étendu). Test `test_principes.py`
  nouveau : 6 verrous.
- Cartes régénérées : 78 verdicts sur les deux cartes (principale +
  identité).

## Limites déclarées

- PF1 au 1-loop seulement : un contact PF1b à 2-boucles exigerait le
  gel des coefficients SM complets — pas dans la source.
- PF2 est une transposition d'unités interne au corpus, pas une
  prédiction spectroscopique.
- Les contacts psy/RMN (ΔB, PF5/PF6) restent non montables : leurs
  formules sont en images dans les articles ; listés dans la
  prospective.

## Suite ouverte

1. PF5/PF6 : transcription des formules manquantes (psy, RMN ΔB) pour
   ouvrir les contacts non pesables — le seul verrou est documentaire.
2. PF1b (2-boucles) si les coefficients sont gelés depuis une source
   datée.
3. H(z) F4 : la table existe, le contact attend son montage.
