# Chantier LOI-HARMONIQUE — protocole gelé (2026-09-15)

**Statut : gelé avant run. Local, non publié.** Premier chantier où la
machine pèse une **loi interne au corpus noétique** et non des tables
externes : la loi harmonique d'échelle m = m_p·2^{n/12} et ses
instances particule par particule (prospective :
`docs/PROSPECTIVE-LOI-HARMONIQUE.md`). Première fournée : trois
contacts — l'arithmétique KO-6 (chauffe la grammaire) et les deux
instances les plus solides de la loi (muon, Z).

## Ce qui est emprunté (trace écrite)

Le corpus déclare ses lois mais pas les valeurs de référence : m_e, m_p
et α sont gelés depuis CODATA-2018, m_μ et m_Z depuis PDG-2024, les
comptages de racines depuis Bourbaki — chacun cité en source de sa
table (`lh_masses_LITTERATURE-2026.json`, `lh_ko6_LITTERATURE-2026.json`).
Grammaire PF1b : l'emprunt est un acte curatorial gelé daté, jamais une
correction en silence. Zéro fetch dans la machine.

## Population gelée : 3 contacts

### LH_KO6_Racines — l'arithmétique des modules et des racines

- **μ_loc** : écart maximal des six identités entières : modules 24/63/
  120 vs racines D4/E7/E8 ; 36 vs racines E6 ; factorisations coquilles
  54 = 3²·6 et 36 = 6²·1.
- **μ_ref** : 0 (ce sont des identités déclarées exactes).
- Attendu gelé : **S+ à écart nul** (comme les re-computes exacts du
  registre). Information si tenu : la correspondance KO-6 ↔ ADE est
  arithmétiquement exacte ; l'exclusion d'E6 par sqf(36) = 1 tient.

### LH_Muon_Quinte — le muon comme quinte amplifiée

- **μ_loc** : m_μ = m_e·(3/2)/α (CODATA-2018 gelées) = 105,041 MeV.
- **μ_ref** : 105,658 375 5 MeV (PDG-2024 gelé).
- **Ce que la machine pèse** : l'instance « quinte » de la loi
  harmonique — l'article revendique ~99,4 %.
- Attendu gelé : **S+** (δ ≈ 0,58 % à θ = 0,10).

### LH_Z_Diagonale — le Z comme tension diagonale

- **μ_loc** : m_Z = m_p/α/√2 (CODATA-2018 gelées) = 90 918 MeV.
- **μ_ref** : 91 187,6 ± 2,1 MeV (PDG-2024 gelé).
- **Ce que la machine pèse** : l'instance « diagonale » — l'article
  revendique ~99,7 %.
- Attendu gelé : **S+** (δ ≈ 0,30 % à θ = 0,10).

## Calcul préparatoire du protocole

- Muon : 0,510 998 95 × 1,5 / 0,007 297 352 569 3 = 105,041 1 MeV →
  δ = 0,584 %.
- Z : 938,272 088 16 / 0,007 297 352 569 3 / √2 = 90 917,9 MeV →
  δ = 0,296 %.
- KO-6 : sqf(24) = 6, sqf(63) = 7, sqf(120) = 30, sqf(36) = 1,
  sqf(54) = 6 — toutes identités exactes, écart nul.

## Règles

- 2 tables gelées datées, sha256 tracés par `load_table` ; zéro fetch.
- θ = 0,10 (relatif) pour les trois — les revendications du corpus sont
  des pourcentages ; l'arithmétique KO-6 est exacte (δ = 0 → S+ à 0 U,
  grammaire des re-computes exacts).
- Nouvelles fibres attendues : (si, MeV) pour muon et Z ; (1, 1) pour
  KO-6 (δ = 0 rejoint les re-computes exacts de la fibre).

## Résultat du run (2026-09-15) — amendement du protocole

- **LH_Muon_Quinte : S+ tenu**, δ = 0,005 873 (0,587 %) → 0,059 θ.
  μ_loc gelé 105,037 877 465 954 27 MeV (le calcul préparatoire à la
  main du protocole annonçait 105,041 MeV — écart de préparation sans
  conséquence sur le verdict attendu S+, tenu).
- **LH_Z_Diagonale : S+ tenu**, δ = 0,002 960 (0,296 %) → 0,030 θ.
  μ_loc gelé 90 917,706 090 722 77 MeV.
- **LH_KO6_Racines : S− à 14 U — attendu S+ NON tenu.** Le run corrige
  la prospective (grammaire PF2 : jamais de retouche en silence, le
  verdict est ce qui compte). Deux valeurs sqf publiées par le corpus
  sont fausses sous sa propre définition : sqf(63) déclaré 7, recomputé
  21 (écart 14 — c'est lui qui porte μ_loc) ; sqf(36) déclaré 1,
  recomputé 6 (écart 5). Les trois autres (24, 120, 54) sont exactes et
  les identités module ↔ racines (24/D4, 63/E7, 120/E8) restent à écart
  nul — la correspondance KO-6 ↔ ADE tient ; ce qui s'effondre, c'est
  l'exclusion d'E6 par « sqf(36) = 1 », bâtie sur une valeur fausse.
- **Transport corrigé pour KO-6** : le protocole prévoyait δ relatif à
  θ = 0,10 ; pour des identités entières déclarées exactes, le transport
  retenu est en **U absolu** (μ_ref = 0, δ = 14 U, decide=U). Même
  grammaire que les re-computes exacts du registre.
- La prospective annonçait S+ pour KO-6 parce que le calcul préparatoire
  sympy avait échoué silencieusement sur `sqf` : la machine a attrapé
  ce que la préparation avait raté — c'est exactement le rôle du run.
- Nouvelles fibres obtenues : (si, MeV) {S+ 2, P 0, S− 0} ; KO-6
  rejoint (1, 1) en S− (17 contacts, fibre {S+ 7, P 3, S− 17}).

## Deuxième fournée G4/G6 — résultat du run (2026-09-15 soir)

Population : 3 contacts — `LH_Strange_Quarte` (G4), `LH_Bottom_G6` (G6),
`LH_Bottom_Arith` (dette arithmétique interne du corpus, pendant PF5).
Table gelée `lh_quarks_LITTERATURE-2026.json` (m_s = 93 +11/−5 MeV,
m_b = 4180 MeV, valeurs centrales PDG-2024 MSbar ; « 5000/1,0593 ~ 4200 »
corpus). Attendus gelés : S− pour les trois (δ ≈ 12 %, 13 %, 12,4 %).

**Les trois attendus S− ne sont PAS tenus : les trois verdicts sont P.**
La bande P s'étend de 1 à 2 θ ; les écarts tombent dedans :

| Contact | μ_loc (gelé) | μ_ref | δ | δ/θ | Verdict |
|---|---|---|---|---|---|
| LH_Strange_Quarte | 104,252 454 MeV | 93 MeV | 12,10 % | 1,21 | **P** |
| LH_Bottom_G6 | 4 723,258 MeV | 4 180 MeV | 13,00 % | 1,30 | **P** |
| LH_Bottom_Arith | 4 720,098 | 4 200 déclaré | 12,38 % | 1,24 | **P** |

Le run corrige la prospective (grammaire PF2). Information : la
frontière de la loi harmonique côté quarks moyens/lourds est **grise,
pas rouge** — la loi n'est pas franchement hors-la-loi à θ = 0,10,
elle est dans la zone d'incertitude. Conséquence notable : la dette
arithmétique du texte (« 5000/1,0593 ~ 4200 ») produisait par hasard un
nombre proche du PDG (4 180) — l'erreur d'arithmétique masquait
l'écart réel de la formule (4 723). La machine nomme les deux
séparément.

Fibre (si, MeV) : {S+ 2, P 2, S− 0} ; fibre (1, 1) : {S+ 7, P 4,
S− 17}. Population détente (P sans GUM) : 5 → 8. Série O inchangée
(16). Suite complète : 307 tests OK.

## Troisième fournée G7/G9/G10 — résultat du run (2026-09-15 nuit)

Population : 3 contacts — `LH_Koide_Q` (G7, loi empirique citée par le
corpus), `LH_Zmax_Modes` (G9, échelle koïlon), `LH_Addendum_Corps` (G10,
tension interne 180 vs 179). Curation datée : m_τ (1 776,86 ± 0,12 MeV,
PDG-2024) ajouté à `lh_masses_LITTERATURE-2026.json` (acte daté, la
table change de D) ; table corpus gelée `lh_zmax_LITTERATURE-2026.json`
(α_hydro = 10⁻³, Z_max ≈ 179, N_modes ≈ 120, addendum 180 « recomputé
exact » à α_K = 2⁻¹⁰).

**Les trois attendus sont TENUS.**

| Contact | μ_loc (gelé) | μ_ref | δ | δ/θ | Verdict |
|---|---|---|---|---|---|
| LH_Koide_Q | 0,666 660 5 | 2/3 | 9,2×10⁻⁶ | 9,2×10⁻⁵ | **S+** |
| LH_Zmax_Modes | 179,384 117 | 179 | 0,215 % | 0,022 | **S+** |
| LH_Addendum_Corps | 1,0 U | 0 | 1,0 U | — (abs) | **S−** |

- **Koide** : le S+ le plus serré du registre (9,2×10⁻⁵ θ). Deux erreurs
  de préparation sur la formule (variante sans racines : Q = 0,373 ;
  variante inversée : Q = 0,500) ont été attrapées **avant** le gel —
  la leçon KO-6 appliquée : vérifier avant de geler, pas seulement
  après le run.
- **Z_max** : le « ~ 179 » du corps tient au seuil (0,215 %), N_modes
  ~ 120 tient aussi (0,342 %, extra) — l'échelle koïlon est
  arithmétiquement cohérente à α_hydro gelé.
- **Addendum/corps** : deux énoncés se disant « recomputé exact » (180
  à α_K = 2⁻¹⁰, ~ 179 à α_hydro = 10⁻³), écart 1 U absolu → S−. Dette
  de présentation nommée (explication candidate en extra : α différent,
  mais les deux énoncés ne le disent pas).

Fibre (1, 1) : {S+ 8, P 4, S− 18} ; fibre (si, 1) : {S+ 2, P 0, S− 2}.
Série O : 16 → 18 (Koide et Z_max, deux S+ θ). Détente inchangée (8).
Suite complète : 311 tests OK.

## Quatrième fournée G3/G5 — clôture du sextuor (2026-09-15 nuit)

Population : 2 contacts — `LH_Up_G3` (G3), `LH_Charm_G5` (G5). Curation
datée : m_u = 2,16 (+0,49/−0,26) MeV et m_c = 1 270 ± 20 MeV ajoutés à
`lh_quarks_LITTERATURE-2026.json`.

**Les deux attendus S+ sont TENUS.**

| Contact | μ_loc (gelé) | μ_ref | δ | δ/θ | Verdict |
|---|---|---|---|---|---|
| LH_Up_G3 | 2,226 430 MeV | 2,16 MeV | 3,08 % | 0,307 | **S+** |
| LH_Charm_G5 | 1 251,029 MeV | 1 270 MeV | 1,49 % | 0,149 | **S+** |

- **Up** : la valeur locale tombe dans la fourchette PDG déclarée
  (2,16 + 0,49 = 2,65 ; 2,226 < 2,65) — position en sigma notée en
  extra. La fourchette du up est large et asymétrique : le verdict
  pèse les valeurs centrales, la position dans l'intervalle est
  l'information.
- **Charm** : écart 1,49 %, position 0,95 σ du centre PDG — S+ sans
  ambiguïté.

Fibre (si, MeV) : {S+ 4, P 2, S− 0}. Série O : 18 → 20. Détente
inchangée (8). Suite complète : 314 tests OK. **Sextuor G1–G6 clos.**
Cartographie finale de la loi harmonique : S+ — up (0,307 θ), muon
(0,059 θ), charm (0,149 θ), Z (0,030 θ) ; P — strange (1,21 θ), bottom
(1,30 θ) ; dettes internes — KO-6 (S−), arithmétique G6 (P), tension
addendum/corps (S−).

## Cinquième fournée C1/G12 — versant chimie occulte (2026-09-15 nuit)

Population : 2 contacts — `LH_Anu_Gamme` (C1, gamme du Koïlon),
`LH_Alpha_DoubleUsage` (G12, dette d'identification α). Tables gelées :
`lh_koilon_gamme_LITTERATURE-1908.json` (table n°2 ANU transcrite
depuis koilon-scale-e8, vérifiée contre le scan Z = 1–12) et
`lh_alpha_LITTERATURE-2026.json` (α = 1/137 et α = 10⁻³ déclarés).

**Les deux attendus sont TENUS.**

| Contact | μ_loc (gelé) | μ_ref | δ | δ/θ | Verdict |
|---|---|---|---|---|---|
| LH_Anu_Gamme | 1,060 704 | 2^{1/12} = 1,059 463 | 0,117 % | 0,117 | **S+** |
| LH_Alpha_DoubleUsage | 1/137 | 10⁻³ | 630 % | 63 | **S−** |

- **Gamme koïlon** : le corpus déclare « converge vers 2^{1/12} » ET la
  valeur recomptée « 1,0607 » — le recompute donne 1,060 704 : les deux
  déclarations tiennent au seuil (0,117 %). Versant chimie occulte
  ouvert avec la table 1908 gelée.
- **α double usage** : deux constantes sous un même symbole, écart
  630 % → S− à 63 θ. Extra probant : la formule k(Z) est aveugle à
  l'ambiguïté (sensibilité 4,8×10⁻⁴) — la dette est dans la
  déclaration, pas dans l'instrument.

Fibre (1, 1) : {S+ 9, P 4, S− 19}. Série O : 20 → 21. Détente
inchangée (8). Suite complète : 317 tests OK.


## Sixième fournée C3 — RMS des ponts ANU 1908 (2026-09-16)

Population : 1 contact — `LH_Anu_Pont_RMS`. Table gelée :
`lh_anu_pont_LITTERATURE-1908.json` (12 lignes Z/sym/N_ANU/poids_isotope,
transcription verbatim du scan ANU.JPG, Z = 1–12). Le corpus déclare
(addendum 07/09/2026) un RMS isotopique global de **1,42 %**.

**Attendu gelé : S+ — NON TENU. Verdict : S− à 13,8 θ.**

| Grandeurs | Valeur |
|---|---|
| RMS recompté (Z = 1–12) | 3,376 % |
| RMS hors bore 10B | 1,225 % |
| Déclaration corpus | 1,42 % |
| δ | 1,3778 (fraction) |
| δ/θ | 13,8 |

- **L'information** : hors le bore 10B (+10,97 %, porté par la table du
  corpus lui-même), la fenêtre vérifiable Z = 1–12 donne 1,225 % —
  cohérent avec le 1,42 % déclaré. C'est l'isotope 10B choisi par le
  corpus qui casse la fenêtre. Le verdict porte sur la déclaration
  globale, pas sur le choix isotopique.
- **Dette nommée** : la table isotopique Z = 13–92 du corpus est absente
  en local — la note d'audit E44 fournie (nucléation de l'enlacement,
  paire de Hopf en trempe GP) ne contient aucune table isotopique ; la
  source de la table reste non identifiée — la déclaration globale reste non vérifiable. La
  machine pèse ce qu'elle peut vérifier et nomme le reste.
- **Tare de transport** : premier run incohérent (δ = 236,78) par mismatch
  d'unités — le runner renvoyait le RMS en % alors que μ_ref est en
  fraction. Corrigé en transport strict (le runner renvoie la fraction,
  les % restent en extras).


## Septième fournée G11 — le contact expérimental (2026-09-16)

Population : 1 contact — `LH_G11_MassShift`. Table gelée :
`lh_g11_LITTERATURE-2026.json` (déclarations verbatim de « Géométrie
spectrale et physique », août 2026 : formule (21) Δm/m ≈ ε₀E²/8P_K,
E = 1e15 V/m déclaré, P_K = 8,5e21 Pa déclaré, Δm/m = 6,5e-8 déclaré,
protocole 800/400 nm). P_K gelé tel que déclaré avec sa dette explicite
(grammaire PF6) : estimation « ~ », sans budget.

**Attendu gelé : S+ (le corpus présente 6,5e-8 comme dérivé de (21)) —
NON TENU. Verdict : S− à 20 022 θ.**

| Grandeurs | Valeur |
|---|---|
| Δm/m recompute strict de (21) | 1,302e-4 |
| Δm/m déclaré (eq. 26) | 6,5e-8 |
| δ (rel) | 2 002 |
| δ/θ (rel 0,10) | 20 022 |

- **Dette arithmétique interne (type PF5)** : le corpus a calculé
  4,4e15/(8 × 8,5e21) avec P_ext = ε₀E²/2 au numérateur là où la
  formule (21) exige ε₀E² = 2·P_ext — facteur 2, pendant PF3/PF7.
- **Dette d'estimation** : P_K déclaré (8,5e21 Pa) ne suit pas de ses
  propres intrants déclarés (0,5 MeV, 3,9e-13 m → 1,35e24 Pa,
  facteur ~159).
- **L'information** : la prédiction expérimentale du corpus (le seul
  contact à effet mécanique mesurable, indépendant de ω, falsifiable en
  800/400 nm) est doublement non tenue sur sa propre arithmétique —
  avant même toute confrontation au banc. Le rapport QED 4 /
  polytropique 1, lui, reste indépendant de ces dettes : c'est la
  partie tranchable de la prédiction, et elle n'est pas pesée ici
  (aucune donnée d'expérience).
- **Tare de transport** : premier run du runner avec une conversion
  MeV→J sans le 10⁶ (ratio P_K renvoyé 1,6e-4 au lieu de 158,9) —
  corrigé, re-run vérifié.
