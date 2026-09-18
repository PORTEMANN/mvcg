# Fouille transversale — prospective de contacts (2026-09-16 soir)

**Statut : exploration locale, RIEN publié.** Ce document est une carte de
mines, pas un run. Aucune table gelée ici, aucun verdict — seulement des
déclarations du corpus repérées, datées, et leur potentiel de pesée
estimé. Les écarts indiqués sont des ordres de grandeur calculés depuis
les valeurs standard (PDG/CODATA), à refaire proprement au moment du
gel (vintage, fenêtre, θ — la doctrine habituelle).

Sources fouillées : accueil histoire-des-sciences.eu (menus et tables
externes), index.portemann.eu (routeur : 61 concepts, 110 prédictions),
references.histoire-des-sciences.eu (compilation, trois versants),
articles : « La Constante ALPHA de Structure fine » (2022-12-11),
« Convergences Cosmologiques et Noologiques (IV) » (2025-01-19),
« Linéarisation du calcul de l'énergie de liaison par nucléon »
(2025-04-20), « La Musique des Atomes (II) » (2025-02-26),
« Electron – Part. 2 » (2020-12-13, série énumérée : parts 1-5).

---

## A. Contacts prêts à peser (déclarations chiffrées, intrants standard)

### A1. ALPHA-Davies — le trio mésonique de Paul Davies

**MONTÉ en local le 2026-09-16 soir** (contact 103
`TR_Davies_TrioMesons`, chantier TRANSVERSALE) — verdict **S+ à 0,71 θ**,
attendu S+ tenu. Table gelée `tr_davies_trio_LITTERATURE-2022.json`,
runner `src/mvcg/transversale.py`, verrous `tests/test_transversale.py`.
Non publié.

Source : « La Constante ALPHA de Structure fine », 2022-12-11 (citation
gelée de Davies, *Les forces de la nature*) : « les masses du muon, du
pion et du kaon valent presque exactement 3/2 × 1/α, 2 × 1/α et
7 × 1/α fois la masse de l'électron ».

Ordres de grandeur (α⁻¹ = 137,036 CODATA-2018) :

| Lien | Déclaré (m_x/m_e) | Mesuré | Écart rel. |
|---|---|---|---|
| muon | 205,554 | 206,768 | 0,59 % |
| pion ± | 274,072 | 273,132 | 0,34 % |
| kaon ± | 959,252 | 966,102 | 0,71 % |

**Dette à nommer au gel** : quels mésons ? π± tient à 0,34 % mais π0
casse à 3,6 % ; K± à 0,71 % mais K0 à 1,5 %. Le choix « mesure chargé »
est le seul qui tienne — la machine doit geler cette ambiguïté comme
dette (le corpus ne précise pas). À θ = 1 % : trois S+ plausibles ;
θ = 0,5 % : trois P. Contact doublement intéressant : le trio est
*presque* cohérent — c'est exactement le genre de loi « presque vraie »
que la machine sait trancher.

### A2. ALPHA-ProtonMuon — le 9 du paragraphe radio

**MONTÉ en local le 2026-09-17** (contact 104
`TR_Alpha_ProtonMuonNeuf`, chantier TRANSVERSALE) — verdict **S− à
3,38 θ**, attendu S+ non tenu ; nouveau S− de bord (population de
remontée 5 → 6). Table gelée `tr_proton_muon_LITTERATURE-2022.json`,
runner `tr_alpha_proton_muon` dans `src/mvcg/transversale.py`, verrous
dans `tests/test_transversale.py` et `tests/test_remontee_bord.py`.
Non publié.

Même source : « le muon vaut 200 fois la masse de l'électron et le
proton vaut 1800 fois la masse de l'électron, **donc la masse d'un
proton est 9 fois supérieure à celle du muon** ».

m_p/m_μ mesuré = 8,880 vs 9 déclaré → 1,33 % d'écart. Notez la
déclaration doublement gelable : « 1800 » (vs 1836,15 mesuré, 2,0 %)
et la conclusion « ×9 » (1,33 %) — l'inférence interne (1800/200 = 9)
est exacte, c'est l'ancrage expérimental qui bouge. Bel exemple de
déclaration dont l'arithmétique interne tient et la donnée d'entrée
non. À θ = 1 % : P chaud ; θ = 2 % : S+.

### A3. KZN-B11 — l'énergie de liaison du bore 11

Source : « Linéarisation du calcul de l'énergie de liaison par
nucléon », 2025-04-20 : « Pour 11B (Z=5 et N=6) on a Elie/A = 6,8 MeV
avec deltashell ajusté pour Z=5 ».

NUBASE2020 : B/A(11B) = 6,928 MeV → écart 1,85 %. Le « ajusté » est
nommé dans le texte — contact de type déclaration semi-empirique
(calibrée, pas ab initio). θ = 2 % : S+ ; θ = 1 % : P. Table NUBASE2020
déjà en circulation dans l'écosystème (tables physico-chimiques).

**MONTÉ (2026-09-17)** — contact n° 105 `TR_KZN_B11_Liaison` : S+ tenu
de justesse (mu_loc = 1,878 % vs θ = 2 % gelé = 0,94 θ). Gel depuis
nubase_1.mas20 (mirroir php1ic/nuclearmasses, citation Kondev et al.
2021), Δ(11B) = 8667,708 ± 0,012 keV, conversion u et masses H/n
CODATA-2018. Verrous : tests/test_transversale.py (TestB11Liaison).

### A4. KZN-Sn132 — la préférence du tin 132

Même source : « 132Sn est favorisé par rapport à 133Sn car
8,40 MeV > 8,35 MeV » — deux valeurs d'énergie de liaison déclarées
+ une inégalité. Pesable en une passe NUBASE2020 (inégalité et
valeurs). Contact fin : c'est une déclaration à deux colonnes.

**MONTÉ (2026-09-17)** — contact n° 106 `TR_KZN_Sn132_Preference` : S+
tenu (mu_loc = 0,537 % vs θ = 2 % gelé, même calibration que B11,
article unique). B/A(132Sn) = 8,354873 MeV (Δ = −76546,6 ± 2,0 keV) vs
8,40 déclaré ; B/A(133Sn) = 8,310089 MeV (Δ = −70873,9 ± 1,9 keV) vs
8,35 déclaré ; l'inégalité déclarée est vraie côté NUBASE2020 (le 133e
neutron quitte la couche magique N=82, moins lié de 45 keV/nucléon).
Verrous : tests/test_transversale.py (TestSn132Preference).

---

## B. Contacts à curation (transcription d'images ou complétion de table)

### B1. KZN-Modèle — la linéarisation El/A = −0,185 k(Z,N) + 8,090 + Δpairing

Le chantier le plus lourd et le plus riche : le corpus déclare la
forme linéaire finale avec **coefficients chiffrés** (−0,185 ; 8,090)
mais la définition complète de k(Z,N) (Bethe-Weizsäcker adaptée,
coefficients aV/aS/aC/Asym, deltashell par Z) vit dans des **images**
(sections « Equations et calibrage », exemples chiffrés Q = 6,5 MeV,
capture neutronique…). Travail : transcription gelée des images puis
pesée systématique vs NUBASE2020 (le modèle revendique un facteur
10⁵ de gain calculatoire — la machine peut mesurer le prix en justesse
de ce gain, comme PF1/PF1b l'ont fait pour les couplages).
Dette nommée d'office : coefficients « ajustés sur données
expérimentales » — calibration déclarée, pas ontologie.

**MONTÉ (2026-09-17)** — contact n° 107 `TR_KZN_Modele_Grille` :
transcription gelée pixel par pixel de l'image « Equations et
calibrage » (formule complète El/A = −0,185·k(Z,N) + 8,090 + δ_pairing,
k(Z,N) avec dénominateur coulombien A^{4/3} **vérifié au zoom** — pas
le A^{1/3} standard, terme surface A^{−1/3}, paramètres recalibrés par
morceaux, S(Z,N) gaussienne σ² = 4 sur 7 nombres magiques) + grille
NUBASE2020 gelée de 235 noyaux stables mesurés du domaine déclaré
(12 ≤ A ≤ 200). **Verdict : S− à 6,18 θ — RMS 12,36 % (max 22,1 % en
12C, médiane 10,9 %, 3/235 lignes dans ±2 %) vs θ = 2 % gelé
(calibration famille article). Attendu S+ non tenu : le prix en
justesse du facteur 10⁵.** Extra décisif : le modèle ne reproduit pas
ses propres exemples publiés (11B : 8,55 vs 6,8 déclaré ; 132Sn : 9,46
vs 8,40 ; 133Sn : 9,22 vs 8,35) — deux jeux de coefficients cohabitent
dans l'article. Dettes nommées : signe ± du pairing non déclaré (gelé +
pour pairs-pairs), couplage −0,185 non dérivé. Verrous :
tests/test_transversale.py (TestKZNGrille). Suite du chantier B1 :
images restantes (réseau réactionnel image3, Q = 6,5 MeV image9,
fusion D-T image16, deltashell image18) et pesée par régime.

**2e fournée MONTÉE (2026-09-17 soir)** — contacts 108-111 + extras
régimes de la grille 107 :

- **108 `TR_KZN_FusionDT_Liaisons`** (image « Énergies de liaison ») :
  **S+ à 0,56 θ TENU** — D 2,2246 vs 2,2 (1,12 %, pire ligne), T 8,4818
  vs 8,5, 4He 28,2957 vs 28,3, Q_DT 17,589 vs 17,6 (0,061 %). Première
  fournée k(Z,N) verte : données standard citées correctement.
- **109 `TR_KZN_TableComparaison`** (image « Comparaison des
  Réactions ») : **S+ à 0,10 θ TENU** — D+T 0,061 %, p+11B 8,682 vs 8,7
  (0,208 %). La ligne D+D « ~3,6 » a deux canaux ouverts NUBASE
  (3,269 ³He+n ; 4,033 T+p) non déclarés par le corpus — **dette
  nommée, hors mu_loc** (la machine ne devine pas le canal).
- **110 `TR_KZN_ExpQ65`** (image « Exemple chiffré Q = 6,5 MeV ») :
  **S− à 5,95 θ** — étape 1 tient (75,581 → « 75,6 », 0,025 %), étape 2
  casse : exp(−75,581) = 1,498×10⁻³3 ≠ 1,7×10⁻³3 déclaré (11,90 %).
  Dette arithmétique interne au corpus (pendant PF5).
- **111 `TR_KZN_SensibiliteShell`** (texte « 1 % dans deltashell → 0,1
  MeV ») : **S− à 783 θ** — le modèle gelé donne terme de couches 4He
  = 0,3×S(2,2) = 0,6 MeV → 1 % = 0,006 MeV ; la déclaration implique
  deltashell(4He) = 10 MeV, incompatible avec le modèle de la même
  page. Dette nommée : identification deltashell = a_shell·S non écrite.
- **Extras régimes de la grille 107** : RMS par bande — A<20 : 14,35 %
  (n=8), 20≤A≤100 : **7,07 %** (n=98), A>100 : 15,08 % (n=129) : le
  calage casse aux deux extrémités, tient le mieux en vallée. Verrous :
  tests/test_transversale.py (TestKZNFusion, TestKZNComparaison,
  TestKZNExpQ65, TestKZNSensibilite, TestKZNGrille.test_regimes).

Le chantier B1 est épuisé côté déclarations chiffrées pesables de
l'article (le réseau réactionnel image3 est une équation générique sans
nombre ; image19 est un résumé qualitatif). Reste en perspective :
pesée par sous-régimes fins (par Z parcouru, par distance aux nombres
magiques) si la machine veut cartographier plus finement le résidu du
calage.

### B2. CONV4-MoyenneKi — la moyenne 2^(1/12) et les 80 %

Source : « Convergences IV », 2025-01-19 : « La moyenne des
coefficients noologiques des nucléides est égale à 2^(1/12) » et
« 80 % des nucléides possèdent un coefficient noologique compris
entre 1 et 1,2 ».

Contrôle rapide sur les fenêtres déjà gelées de la table ANU 1908 :
Z=1-12 plein → 2/9 ≈ 22 % dans [1 ; 1,2] ; suite stable seule
(18, 72, 127, 164, 200, 216, 261, 290, 340, 360 — « Musique des
Atomes II ») → 4/9 ≈ 44 %, et la moyenne des rapports y est à 46 %
de 2^(1/12) (le saut H→He ×4 empoisonne toute moyenne naïve).
La revendication 80 % n'est tenable que sur le tableau complet
(Z=1-92, 59 éléments de 1908) — **exactement la dette déjà nommée
« table Z=13-92 »** du chantier ANU. Séquence naturelle : compléter
la transcription de la table 1908, puis peser moyenne et fraction.

### B3. CONV4-SeuilZ25 — « stabilité à partir du manganèse »

Même source : « les nucléides se stabilisent à partir de
l'intersection (Z=25 Manganèse)… il n'y a plus de variation
significative des coefficients noologiques à partir de Z=25 ».
Contact de seuil : position du dernier k(i) hors bande. Même dépendance
: table complète requise (B2). Une fois B2 gelé, B3 est un run de plus.

### B4. CONV4-Alcalins — la régression ln(Ei) = −0,004 Z + 1,696

Même source : coefficients de pente et d'ordonnée déclarés, sans
fenêtre. Ordres de grandeur : Li (Z=3) tient au cheveu (ln 5,39 =
1,684 vs 1,684), Cs (Z=55) dérive à ~7 %. Fenêtre à nommer (les 6
alcalins ? les périodes 2-7 ?). Tables physico-chimiques de
l'écosystème pour les Ei. Dette : fit sans budget de résidu déclaré.

### B5. MDA-SuiteStable — la gamme sur nucléides stables seulement

Source : « Musique des Atomes (II) », 2025-02-26 : la suite 18, 72,
127, 164, 200, 216, 261, 290, 340, 360 (isotopes exclus) + paramètres
de correction périodique **déclarés** (T₁=10, D₁=5, T₂=5, D₂=3).
Le modèle complet (progression géométrique × 2^(1/12) + h(n) + ε) est
en images — transcription nécessaire. Une fois gelé : contact neuf
sur table neige (stable-only ≠ la fenêtre Z=1-12 déjà pesée par
Anu_Gamme/Anu_Pont_RMS). Voisinage déclaré de deux contacts existants
— le casier pourra comparer.

### B6. ALPHA-DeltaANU — la loi f(x) = 137 x^(−3/2)

Source : « La Constante ALPHA », 2022 : « deltaANU = (1/α).Z^(−3/2) »
décrite comme « l'erreur relative de la place de chaque atome dans le
tout ». Définition floue (erreur relative à quoi ? à la racine
douzième de 2 ?). Premier test numérique : à Z=6 la loi donne ~9,3
alors que les rapports ANU réels sont ~1,08 — écart d'un facteur ~9.
Probablement S− massif, mais la définition ambiguë impose une dette
avant tout gel (la machine ne pèse pas ce qu'elle ne sait pas figer).

### B2-B6 — pesées réalisées (2026-09-17 soir, contacts 112-116)

Les cinq contacts ont été montés, gelés et pesés. Bilan : **1 S+ tenu
(B3), 4 S− dont 1 attendu-S+ non tenu (B2)**.

- **B2 → contact 112 `TR_CONV4_MoyenneKi` : S− à 0,15 θ** (attendu S+
  gelé non tenu). Table ANU complète gelée
  (`tr_anu_complet_LITTERATURE-1908.json`, double transcription carte
  Crookes + Occult Chemistry Gutenberg #16058, 91 lignes Z=1-92, Tc
  absent ; arbitrage carte-vs-livre toujours vers le livre : F 340,
  Mn 992, Mo 1746, Rb 1530, « Canadium » = Pt B 3514 — sha256
  ec4a9ae80d54cf36…). Recompute : 92,22 % des ANU dans [1 ; 1,2] (le
  80 % déclaré est dépassé, pas violé), mais la moyenne 1,0828 vs
  2^(1/12) à 2,20 % casse le S+. Les deux déclarations ne tiennent pas
  ensemble. Dette « table Z=13-92 » du chantier ANU **bouchée**.
- **B3 → contact 113 `TR_CONV4_SeuilZ25` : S+ à 0,76 θ TENU** — seul
  tenu des cinq. 66 ratios Z=26..92 (Tc sauté) : 1 seul hors bande
  [1 ; 1,2] (Rn Z=86, k=0,990). La bande est calibrée sur le claim 80 %
  de la même page (« variation significative » non définie) — dette
  nommée.
- **B4 → contact 114 `TR_CONV4_Alcalins` : S− à 4,7 θ.** K (Z=19)
  seul dépassement de la régression ln(Ei) = −0,004 Z + 1,696 (table
  Ei gelée 2018) ; Li tient à 0,048 %. Fit sans budget de résidu
  déclaré — dette nommée dès la prospective.
- **B5 → contact 115 `TR_MDA_SuiteStable` : S− à 290 θ.** Deux
  lectures gelées (équation-image perdue) : multiplicative, le premier
  terme 5,792 vs 18 déclaré ; additive, 93,3 % d'écart au terme 10.
  Les deux cassent. ε gelé 0.
- **B6 → contact 116 `TR_ALPHA_DeltaANU` : S− à 83 θ.** Pesée en
  cohérence **interne** uniquement (loi vs graphe gelé
  `tr_deltaanu_plot_LITTERATURE-2022.json`, 31 points Plotnikov ±2,
  Si Z=14 masqué) — la définition de deltaANU n'étant pas
  opérationnelle (équations OLE perdues), la machine ne pèse jamais ce
  contact contre une vérité externe. Sc 167 %, Li 150 %, 13
  violations absolues, 18 comparaisons relatives.

Le motif transversal des quatre S− : le corpus déclare des régularités
qui tiennent localement (fenêtres étroites, premiers termes) mais pas
sur leur domaine annoncé — exactement le tranchant dont B3 mesure la
limite (0,76 θ, juste sous le seuil).

---

## C. Exploré à faible densité pesable

- **Série « Electron » (parts 1-5, 2020-2021)** : essentiellement
  historique et analogique (renormalisation, ANU/théosophie,
  polyèdres). Fil numérique mince : arithmétique interne des
  assemblages H (9+/9−) et H+ (10+/8−) — vérifiable mais trivial ;
  échelles 10⁻³⁰…10⁻¹⁹ m — ordres de grandeur standard. Rendement
  faible, à ne creuser que si les séries A/B s'épuisent.
- **Musique des Atomes (II), volet métaphorique** : le mappage
  Z mod 12 → note est qualitatif (le corpus le dit lui-même) :
  rien à peser hors B5.
- **Index portemann.eu (110 prédictions)** : PRED-12 (muon g-2),
  PRED-15 (Z_max), PRED-16 (shift masse), PRED-31 (KO-6) déjà couverts
  par les chantiers g-2 / Z_max / G11 / KO-6. Reste PRED-23
  (EDM neutron < 3e-26 e·cm) — borne, pas valeur : pesée de type
  « plafond » possible mais mince. Veille à garder en tiroir.

  **PESÉ (2026-09-18)** — contact 118 `TR_PRED23_EDMNeutron` : **S− à
  6,7 θ**. Grammaire du plafond déclarée avant le run : mu_loc = retard
  de veille = B_decl/B_best − 1. La borne du corpus (3,0×10⁻²⁶ e·cm)
  coïncide **exactement** avec Pendlebury 2015 (90 % CL) : la veille
  « en cours » est figée d'avant Abel 2020 (nEDM@PSI, 1,8×10⁻²⁶ e·cm,
  90 % CL, toujours la meilleure borne publiée en 2025-2026) — retard
  66,7 %. La borne reste vraie physiquement (le monde la satisfait) :
  c'est son statut de veille actuelle qui casse. Ouvre la fibre
  (si, e·cm). n2EDM phase 1 vise le bas du 10⁻²⁷ e·cm d'ici fin 2026
  (noté, hors mu).
- **Nouvelles Perspectives en Astrophysique (Calculs)** (TOV) :
  repéré au catalogue, non encore lu — candidat B de la prochaine
  rotation de fouille.

### C1. TOV-Sn195Pt — « Ex pour 195Pt=>196Pt, Sn=6,5 MeV »

Article lu le 2026-09-18 (rotation de fouille). C'est le **même
modèle k(Z,N)** que le chantier B1 (déjà pesé : S− à 6,18 θ, RMS
12,36 %), appliqué à l'astrophysique. Les équations complètes du modèle
sont en images en fin d'article (dette identique à B1 — la machine ne
devine pas la formule), mais l'article contient un exemple numérique
recomposable : l'énergie de séparation neutronique du produit de
capture, S_n(196Pt), déclarée **6,5 MeV**. Référence directe : masses
gelées NUBASE2020 déjà dans le dépôt (grille du chantier k(Z,N)).

Reste dans l'article, non pesé (dettes nommées) : la revendication
« précisions suffisantes (1 ou 2 % sur El/A) » (tension avec le RMS
12,36 % du même modèle pesé par TR_KZN_Modele_Grille), la sensibilité
« 2 % sur El/A → 10 % sur les abondances » (sans mécanisme
recomposable), le pic d'or « autour de A=195 » (qualitatif), les
scénarios « résultat envisagé » (Z=126/N=184, ⁵He, ¹⁵N — cadre
hypothétique explicite, pas des déclarations).

**PESÉ (2026-09-18)** — contact 117 `TR_TOV_Sn195Pt` : **S− à 10,9 θ**.
S_n(196Pt) recompute = mex(195Pt) + mex(n) − mex(196Pt) = −32793,9 +
8071,3171 − (−32644,5) = **7921,9 keV** vs 6,5 MeV déclaré — écart
21,9 %. La valeur 6,5 est en fait l'intrant de l'exemple
exp(−6,5/0,086) de « Linéarisation » (contact 110 TR_KZN_ExpQ65 pesait
l'arithmétique de l'exponentielle sans peser la valeur : trou bouché —
l'exemple du second article repose sur une S_n erronée de 22 %).

---

## Recommandation

Première fournée suggérée (quatre contacts légers, zéro transcription
d'image) : **A1 (Davies trio), A2 (proton/muon ×9), A3 (B11), A4
(Sn132)** — tous pesables avec des tables déjà en circulation (CODATA/
PDG, NUBASE2020), tous de la famille « déclaration chiffrée à θ
gélable », et leurs verdicts seront directement comparables aux P
chauds du chantier LOI-HARMONIQUE (mêmes objets : muon, quarks légers
→ mésons). Ensuite seulement : B1 (le chantier lourd k(Z,N) —
transcription d'images à cadrer comme pour PF/CTFT).
