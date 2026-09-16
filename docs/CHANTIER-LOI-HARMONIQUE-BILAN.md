# Chantier LOI-HARMONIQUE — bilan du run (2026-09-15)

**Statut : run exécuté, verrous verts, non publié.** Protocole :
`docs/CHANTIER-LOI-HARMONIQUE-PROTOCOLE.md` (amendé par le run).
Prospective : `docs/PROSPECTIVE-LOI-HARMONIQUE.md`.

## Population : 3 contacts — 2 attendus tenus, 1 S− inattendu

| Contact | μ_loc (gelé) | μ_ref | δ | Verdict | Attendu |
|---|---|---|---|---|---|
| LH_KO6_Racines | 14 U | 0 | 14,0 U | **S−** | S+ non tenu |
| LH_Muon_Quinte | 105,037 877 MeV | 105,658 375 5 MeV | 0,587 % | **S+ à 0,059 θ** | S+ tenu |
| LH_Z_Diagonale | 90 917,706 MeV | 91 187,6 MeV | 0,296 % | **S+ à 0,030 θ** | S+ tenu |

## La capture KO-6

C'est le résultat le plus important du chantier. La prospective
annonçait S+ pour l'arithmétique des modules et racines — annonce
basée sur un calcul préparatoire sympy qui avait **échoué
silencieusement** sur la fonction `sqf`. Le run, lui, a re-computé :

- `sqf(63)` déclaré **7** par le corpus, recomputé **21** → écart 14
  (c'est lui qui porte μ_loc et le verdict S− à 14 U) ;
- `sqf(36)` déclaré **1**, recomputé **6** → écart 5 ;
- `sqf(24) = 6`, `sqf(120) = 30`, `sqf(54) = 6` : exactes.

Deux valeurs fausses sur cinq, sous la propre définition du corpus.
Conséquence directe : l'**exclusion d'E6** (« sqf(36) = 1 ») est bâtie
sur une valeur fausse — elle s'effondre. En revanche les identités
module ↔ racines (24/D4, 63/E7, 120/E8) restent à écart nul : la
correspondance KO-6 ↔ ADE tient, c'est l'usage arithmétique qu'on en
fait qui est défaillant.

La machine a attrapé ce que la préparation avait raté — c'est le rôle
exact du run, et c'est la grammaire PF2 : le protocole ne retouche
jamais en silence, le verdict est ce qui compte.

## Ce que les deux S+ disent

Le muon comme quinte (m_μ ≈ m_e·(3/2)/α, écart 0,587 %) et le Z comme
diagonale (m_Z ≈ m_p/α/√2, écart 0,296 %) tiennent tous deux au seuil
θ = 0,10 — les revendications du corpus (~99,4 % et ~99,7 %) sont
**sous-évaluées** par la machine (les écarts réels sont plus petits que
les pourcentages arrondis annoncés). Première pesée d'une loi interne
au corpus : la loi harmonique d'échelle m = m_p·2^{n/12} et ses
instances particule par particule.

## État du registre après chantier

- **86 contacts** (83 → 86), suite complète : **304 tests OK**
  (4 skipped), aucun verrou rompu.
- **17 fibres** : (si, MeV) nouvelle {S+ 2, P 0, S− 0} — la case de
  référence MeV existe maintenant pour les contacts de masse ;
  (1, 1) passe à {S+ 7, P 3, S− 17} avec LH_KO6_Racines.
- Population série O (S+ θ) : 14 → **16** (les deux S+ du chantier ;
  KO-6 est S−, hors population comme tout S−).

## Leçons pour la machine

1. **Une prospective n'est pas un verdict.** L'échec silencieux du
   préparatoire sympy aurait laissé passer deux sqf faux si le
   protocole s'en était tenu à sa promesse. Le gel des attendus *avant*
   le run rend l'écart lisible au lieu de le masquer.
2. **Le corpus noétique se prête au même traitement que les tables
   externes.** Emprunt curatorial gelé daté (PF1b), zéro fetch, sha256
   tracés — la machine pèse les déclarations du corpus avec la même
   exigence que celles de CODATA ou du PDG.
3. **L'arithmétique est un contact comme un autre.** δ en U absolu pour
   les identités entières déclarées exactes : même grammaire que les
   re-computes exacts du registre.

## Deuxième fournée G4/G6 (2026-09-15 soir)

Trois contacts, trois verdicts P — les attendus S− gelés ne sont **pas**
tenus : δ/θ = 1,21 (strange), 1,30 (bottom), 1,24 (arithmétique du
texte), tous dans la bande P (1–2 θ). La prospective lisait « la loi
lâche à 12–13 % » ; la machine dit plus finement : la frontière de la
loi harmonique côté quarks est **grise**.

**L'information la plus riche est structurelle** : la dette
arithmétique du texte (« 5000/1,0593 ~ 4200 ») produit un nombre qui
tombe par hasard près du PDG (4 180), alors que la formule elle-même
donne 4 723. Sans le contact `LH_Bottom_Arith`, l'échec de la formule
aurait été invisible — l'erreur d'arithmétique le masquait. Deux
verdicts séparés rendent l'invisible visible : la loi est en zone P, et
le texte contient une erreur de 520 unités qui faisait croire à un
accord.

Bilan de la loi harmonique à ce stade (6 instances pesées) : μ S+,
Z S+, strange P, bottom P ; + KO-6 S− (arithmétique interne) et sa
dette sqf. La loi tient pour les leptons lourds et le Z, reste dans
la zone grise pour les quarks moyens/lourds — exactement la frontière
que le corpus lui-même désigne en invoquant des « corrections
harmoniques ».

Registre après fournée : **89 contacts**, 17 fibres, détente 8,
série O 16. Suite complète : **307 tests OK** (4 skipped).

## Troisième fournée G7/G9/G10 (2026-09-15 nuit) — attendus tous tenus

**Trois contacts, trois verdicts comme gelés : Koide S+ à 9,2×10⁻⁵ θ**
(le plus serré du registre — la loi empirique tient sur PDG-2024 gelé à
un dix-millionième près), **Z_max S+ à 0,022 θ** (le « ~ 179 » du corps
tient ; N_modes ~ 120 tient aussi en extra), **tension addendum/corps
S− à 1 U** (180 « recomputé exact » vs ~ 179 — dette de présentation,
pendant PF5).

Leçon méthodologique inscrite dans le chantier : la formule de Koide a
été fausse **deux fois** en préparation (variante sans racines Q =
0,373 ; variante inversée Q = 0,500) et attrapée avant le gel — la
leçon KO-6 (le préparatoire peut échouer silencieusement) est désormais
appliquée *en amont*, plus seulement lue en aval du run.

Registre : **92 contacts**, 17 fibres — (1, 1) {S+ 8, P 4, S− 18},
(si, 1) {S+ 2, P 0, S− 2} ; série O 18 ; détente 8. Suite complète :
**311 tests OK** (4 skipped).

## Quatrième fournée G3/G5 (2026-09-15 nuit) — clôture du sextuor

**Deux contacts, deux S+ tenus : up (2,226 MeV dans la fourchette PDG,
0,307 θ) et charm (1 251,029 MeV, 0,95 σ du centre, 0,149 θ).** Le
sextuor G1–G6 est clos : la loi harmonique tient pour le up, le muon,
le charm et le Z, reste grise (P) pour le strange et le bottom — la
frontière nommée est celle des quarks moyens/lourds, exactement là où
le corpus invoque des « corrections harmoniques ».

Cartographie finale du chantier (11 contacts pesés) : S+ tenus — up,
muon, charm, Z, Koide (9,2×10⁻⁵ θ), Z_max ; P — strange, bottom,
arithmétique G6 ; S− — KO-6 (dette sqf), tension addendum/corps.
Trois dettes internes au corpus nommées en passant.

Registre : **94 contacts**, 17 fibres — (si, MeV) {S+ 4, P 2, S− 0} ;
série O 20 ; détente 8. Suite complète : **314 tests OK** (4 skipped).

## Cinquième fournée C1/G12 (2026-09-15 nuit) — versant chimie occulte

**Deux contacts, deux attendus tenus.** `LH_Anu_Gamme` : la gamme du
Koïlon tient — GM des rapports N(Z)/N(Z−1) sur Z = 11–30 recomptée =
1,060 704 vs 2^{1/12} (0,117 θ), et le « 1,0607 » annoncé par le corpus
est exactement la valeur recomptée : les deux déclarations tiennent.
`LH_Alpha_DoubleUsage` : dette d'identification nommée — deux
constantes sous un même symbole α (1/137 et 10⁻³), écart 630 % → S−.
Extra probant : la formule k(Z) est aveugle à sa propre ambiguïté
(sensibilité 4,8×10⁻⁴) — la dette est dans la déclaration, pas dans
l'instrument.

Curation : table n°2 ANU (1908) gelée depuis koilon-scale-e8, vérifiée
contre le scan Z = 1–12 (concordance exacte) ; table α gelée.

Registre : **96 contacts**, 17 fibres — (1, 1) {S+ 9, P 4, S− 19} ;
série O 21 ; détente 8. Suite complète : **317 tests OK** (4 skipped).
Chantier LOI-HARMONIQUE après 5 fournées : 13 contacts pesés, tous les
candidats pesables de la prospective G/C sauf C3 (RMS 1,42 % — tables
nucléides requises) et G11 (contact expérimental, cap de la
prospective mécanique).

Bilan complet de la loi harmonique après 9 contacts pesés : S+ tenus —
muon (0,059 θ), Z (0,030 θ), Koide (9,2×10⁻⁵ θ, loi citée), Z_max
(0,022 θ) ; P — strange (1,21 θ), bottom (1,30 θ), arithmétique G6
(1,24 θ) ; S− — KO-6 (14 U, dette sqf), tension addendum/corps (1 U).
La loi tient pour leptons et boson, reste grise pour les quarks, et le
corpus porte trois dettes internes nommées — c'est une cartographie,
pas un verdict global.

## Sixième fournée C3 (2026-09-16) — le pont des ANU ne tient pas

**Un contact, attendu S+ non tenu → S− à 13,8 θ.** `LH_Anu_Pont_RMS` :
le corpus déclare un RMS isotopique global de 1,42 % (addendum
07/09/2026) ; le recompute sur la fenêtre vérifiable Z = 1–12 donne
3,376 %. Hors bore 10B (+10,97 %, porté par la table du corpus
lui-même), la fenêtre tombe à 1,225 % — cohérente avec 1,42 %. C'est
l'isotope 10B choisi par le corpus qui casse la fenêtre : le verdict
pèse la déclaration globale, pas le choix isotopique.

Dette nommée : la table isotopique Z = 13–92 du corpus est absente en
local (la note d'audit E44 fournie — nucléation de l'enlacement, paire
de Hopf en trempe GP — ne contient aucune table isotopique ; la source
de la table reste non identifiée) — la déclaration globale reste non vérifiable. La
machine pèse ce qu'elle peut vérifier et nomme le reste.

Curation : table `lh_anu_pont_LITTERATURE-1908.json` gelée (12 lignes,
transcription verbatim du scan ANU.JPG) ; tare de transport corrigée
(runner renvoie la fraction, les % en extras).

Registre : **97 contacts**, 17 fibres — (1, 1) {S+ 9, P 4, S− 20} ;
série O 21 ; détente 8. Suite complète : **319 tests OK** (4 skipped).
Chantier LOI-HARMONIQUE après 6 fournées : 14 contacts pesés —
S+ : up, muon, charm, Z, Koide, Z_max, Anu_Gamme ; P : strange,
bottom, arithmétique G6 ; S− : KO-6 (dette sqf), addendum/corps,
α double usage, Anu_Pont_RMS. G11 est pesé (7e fournée ci-dessous) : la prospective LOI-HARMONIQUE est épuisée.

## Septième fournée G11 (2026-09-16) — le cap expérimental : doublement non tenu

**Un contact, attendu S+ non tenu → S− à 20 022 θ.** `LH_G11_MassShift` :
le corpus déclare Δm/m ≈ 6,5e-8 pour E = 1e15 V/m (eq. 26, « Géométrie
spectrale et physique », août 2026) comme dérivé de sa formule (21)
Δm/m ≈ ε₀E²/8P_K. Recompute strict de (21) depuis les intrants gelés
(P_K gelé tel que déclaré, 8,5e21 Pa, dette explicite — grammaire PF6)
: **1,302e-4**, écart facteur ~2 002. Deux dettes nommées : le numérateur
du corpus est P_ext = ε₀E²/2 là où (21) exige ε₀E² (facteur 2, type PF5) ;
et P_K déclaré ne suit pas de ses propres intrants déclarés (0,5 MeV,
3,9e-13 m → 1,35e24 Pa, facteur ~159).

L'information : le seul contact à effet mécanique mesurable du corpus
(déplacement de masse indépendant de ω, protocole 800/400 nm, rapport
attendu QED 4 vs polytropique 1) est doublement non tenu sur sa propre
arithmétique — avant toute confrontation au banc. Le rapport 4-vs-1,
lui, reste la partie tranchable et n'est pas pesée (aucune donnée
d'expérience gelée) : la machine nomme ce qui l'empêche de le peser.

Curation : table `lh_g11_LITTERATURE-2026.json` gelée (déclarations
verbatim de l'article, datées) ; ε₀ = SI_VACUUM (CODATA-2018). Tare de
transport corrigée (conversion MeV→J).

Registre : **98 contacts**, 17 fibres — (1, 1) {S+ 9, P 4, S− 21} ;
série O 21 ; détente 8. Suite complète : **321 tests OK** (4 skipped).
Chantier LOI-HARMONIQUE : 15 contacts pesés, **prospective épuisée** —
la machine a atteint le cap prospectif ; l'étage 3 (prédiction hors-table
tranchable au banc) reste à ouvrir avec des données d'expérience.

## Huitième fournée — corridor F_exp (2026-09-16) : la déclaration tient en zone grise

**Un contact, attendu S+ non tenu → P à 1,78 θ.** `LH_Fexp_Corridor` :
à la demande « creuse », retour dans « Unification analytique et
fondements mathématiques de la physique noétique » au-delà de la
prospective épuisée — section « Loi Harmonique d'Échelle et Calibration
Analytique ». Le corpus y déclare : le facteur de correction empirique
F_exp (= m_exp/m_théo) « demeure strictement confiné dans un corridor
de variance minimaliste de ±3 % pour l'intégralité du spectre
particulaire, oscillant entre 0,973 (charm) et 1,028 (down) », avec un
ansatz M = m_p·δ^n·(1 + Δ_k·F(α, χ, σ)), F = a_f·α + b_f·χ·α +
c_f·s·α² (coefficients non déclarés — fit) et un Modèle Tri-Régime
(Micro u/d/e, Méso s/c/τ, Macro b/t/W/Z/H).

Pesée sur la table « Calibration de l'Approximation Harmonique de Base »
(10 lignes transcrites verbatim de l'image) : le corridor recompté vaut
[0,917 ; 1,016] — le maximum tient (μ à 1,016), le plancher casse :
**5 violations de 0,973** (u 0,917, e 0,964, s 0,960, c 0,969, Z 0,970),
soit μ_loc = 0,0833 vs 0,03 déclaré → P à 1,78 θ (b3_fail, pas S−).

Dettes nommées : (1) **aucune des 10 lignes ne coïncide avec son F
imprimé** — écart max 11,0 points (u : imprimé 1,027, recompté 0,917),
la colonne F n'est ni m_exp/m_théo ni vérifiable ; (2) tensions
texte/table : « down 1,028 » absent de la table (max imprimé 1,027, up),
bottom absent alors que le texte dit « l'intégralité du spectre », et
le charm — cité comme minimum du corridor — le viole dès qu'on le
recompte ; (3) l'ansatz F(α, χ, σ) n'est pas pesable (coefficients du
fit non déclarés — dette nommée, la machine refuse de deviner un fit).

L'information : la prétention d'un corridor minimaliste ±3 % casse
exactement là où l'ansatz dit agir — versant méso/macro du tri-régime
(s, c) et boson Z. Comme G11, le motif est constant du corpus : les
grosses déclarations (universelles, « intégralité du spectre ») se
révèlent tenables seulement en zone grise une fois la table refaite.

Curation : table `lh_fexp_LITTERATURE-2026.json` gelée (rows =
[particule, m_exp, n, m_théo, F imprimé] ×10, transcription verbatim
datée) ; images sources archivées `_tmp_fexp/`.

Registre : **102 contacts**, 17 fibres — (1, 1) {S+ 11, P 5, S− 22} ;
série O 23 ; détente 8. Suite complète : **330 tests OK** (4 skipped).
Chantier LOI-HARMONIQUE : 16 contacts pesés.


