# H0 bas-z — protocole de déclaration d'une table LITERATURE

Document de chantier, local, non publié (2026-09-13 soir).
Ce protocole s'applique le jour où une **compilation réelle** de bins
du diagramme de Hubble bas-z sera déclarée pour remplacer la table
DEMO `hz_sne_LOWZ-DEMO-2026.json`. Il est écrit **avant toute table** :
aucun chiffre de données réelle n'apparaît ici, aucune source n'est
encore retenue. Ce document ne pèse rien ; il fixe les règles de la
pesée à venir.

## 1. Doctrine : ce qui change, ce qui ne change pas

**Ne change pas** (gelés, réutilisés tels quels) :

- la règle de pesée : μ_loc = rms des résidus μ_pred(zᵢ ; H(z)
  fabrication Planck déclarée, Ω gelés) − μ_obs,ᵢ sur les bins ;
  μ_ref = 0 (la courbe passe par les bins) ;
- le GUM : une ligne B (dispersion des bins déclarée), R identité,
  decide=theta — le budget est porté, pas utilisé pour blanchir ;
- l'interdiction : ajuster les bins, la dispersion, les Ω ou θ sur
  la référence. Le levier `H0<-SH0ES_ou_autre` reste le seul degré
  de liberté déclaré (voir campagne 3) ;
- le contact DEMO `H0_Hz_SNe_LOWZ_DEMO` : son mot S− reste figé
  pour toujours. Une table LITERATURE ne réécrit jamais l'histoire.

**Ne se transpose pas mécaniquement** :

- θ. Sur le contact DEMO, θ = 0,05 mag *parce que* la dispersion
  déclarée de la table valait 0,05 mag — le seuil gelé codait le
  sens physique « la courbe passe par les bins à hauteur du bruit ».
  Pour le contact LITERATURE, θ = **la dispersion déclarée de sa
  propre table**, fixée avant le premier run dans la déclaration de
  table (§5.3) — jamais ajustée après coup sur des résultats. Le
  « 0,05 » de la DEMO n'est donc pas un seuil universel : chaque
  contact porte son θ gelé. Conséquence honnête : le mot LITERATURE
  et le mot DEMO ne seront comparables qu'avec la conscience que
  leurs θ diffèrent (chacun = sa dispersion). La campagne 3 reste
  le modèle du balayage ; ses frontières numériques, elles, ne se
  transposent pas.

**Change** :

- la table (id, vintage, source, bins, dispersion) ;
- **un contact nouveau** est créé (`H0_Hz_SNe_LOWZ_LITERATURE` ou id
  fixé à la déclaration), avec son propre test de gel. Le mot du
  contact DEMO (S−, table synthétique) et le mot du contact
  LITERATURE (mot à découvrir) coexistent — deux cartes, deux
  natures, deux dettes.

## 2. Admissibilité d'une compilation candidate

Une compilation est admissible si et seulement si tous les critères
ci-dessous sont **vérifiés et écrits dans la table** :

| # | Critère | Vérification |
|---|---|---|
| A1 | Publication référencée (revue, DOI ou prépublication datée) | référence copiée dans `doi_or_ref`, non paraphrasée |
| A2 | Extraction des bins reproductible | la chaîne compilation → bins est décrite (agrégation, coupures en z, statistique de centralité) ou déclarée comme dette de compression |
| A3 | Dispersion des bins déclarée ou dérivable | valeur écrite dans la table ; sinon la table est irrecevable (θ exige une dispersion déclarée) |
| A4 | Vintage daté | `vintage` = année de la compilation utilisée, pas l'année de l'extract |
| A5 | Indépendance documentée | voir §4 — les dettes d'ancrage et d'indépendance sont écrites, jamais supposées nulles |

**Critères de rejet immédiat** : extraction non traçable (bins « trouvés
quelque part »), dispersion non déclarable, compilation dont la chaîne
de dérivation des μ est inconnue et non déclarée en dette, table
modifiée après gel (changer params = autre D, la table est figée par
son empreinte).

## 3. Sources candidates et leur statut

État au 2026-09-13 : **aucune retenue, toutes à vérifier**. Le
protocole n'endosse pas une source ; il exige que la vérification de
§5 soit faite et consignée avant gel.

| Compilation | Couverture | Point de vigilance principal |
|---|---|---|
| Pantheon+ (Scolnic et al., 2022) | SNe Ia, z 0,01–2,3 | distances relatives ; ancrage de magnitude dépendant du programme d'étalonnage |
| JLA (Betoule et al., 2014) | SNe Ia, z 0,01–1,2 | μ dérivés sous fiducial ΛCDM déclaré — ancrage à documenter |
| DES 5 yr (DES Collaboration, 2024) | SNe Ia haut-z dominé | bas-z moins profond ; chaîne d'étalonnage propre au projet |
| Compilations bas-z dédiées (CfA/LOSS/CSP, selon disponibilité) | z < 0,1 | hétérogénéité des chaînes photométriques |

Références bibliographiques exactes, numéros de version des catalogues
et colonnes utilisées : à recopier **depuis la source** lors de la
vérification — jamais de mémoire. Une référence non relue n'entre pas
dans la table.

## 4. Dettes obligatoires (modèle de blocs)

La table LITERATURE porte les quatre blocs de dette suivants, chacun
renseigné ou explicitement marqué « non applicable, justifié » :

- **D-nature** (résiduelle) : la donnée est réelle mais binnée ; les
  bins sont une compression d'événements individuels.
- **D-compression** : les bins ignorent la covariance intra-bin et
  inter-bins ; les systématiques des SNe Ia (stretch, couleur,
  sélection, extinction) ne sont pas dans σ sauf déclaration explicite
  du contraire.
- **D-ancrage** : les μ publiés d'une compilation sont un produit
  d'analyse. La table doit déclarer le fiducial sous lequel μ a été
  dérivé (cosmologie, H0 marginalisé ou fixé, traitement de M).
  Peser H(z) Planck contre des μ construits sous un fiducial proche
  de Planck testerait la cohérence interne de la compilation, pas
  l'univers : cette dette se lit, elle ne se supprime pas.
- **D-indépendance** : si la compilation est étalonnée par l'échelle
  locale (ancrage SH0ES ou équivalent), la donnée et le levier
  `H0<-SH0ES` ne sont pas indépendants — pendant exact de la dette
  Landau (le min de E/p *est* le roton). Écrite dans la table.

## 5. Procédure de vérification avant gel (checklist)

1. **Relecture de la source primaire** : la référence est ouverte, les
   valeurs d'extract sont copiées depuis le document (pas de source
   secondaire, pas de mémoire).
2. **Reconstruction d'un bin** : au moins un bin est re-dérivé à la
   main depuis les données de la compilation pour valider la chaîne
   d'extraction.
3. **Écriture de la table JSON** : format calqué sur
   `hz_sne_LOWZ-DEMO-2026.json` (mêmes champs : id, vintage, source,
   doi_or_ref, species, quantity, dimension, packet, bins, sigma_mag,
   params, blocs de dette, sha256_note). La dispersion des bins —
   donc la valeur θ du contact à venir — y est déclarée ici, avant
   tout run.
4. **Estimation pré-run honnête** : calculée et écrite AVANT le premier
   run, avec zone attendue et suspense déclaré (comme DEMO : δ ≈ 0,096,
   zone P au bord S−). Une estimation n'est jamais un arrangement :
   elle peut être fausse de la part du hasard, et le protocole le dit.
5. **Gel** : empreinte de la table fixée, contact créé dans le registre
   local, θ = dispersion déclarée de la table réaffirmé (valeur fixée
   au §5.3, pas au moment du run), test de gel écrit (mot découvert
   au run, jamais anticipé dans le test).
6. **Premier run** : le mot est découvert. Consignation dans un doc
   `H0-HZ-SNE-CONTACT-LITERATURE.md` (chronologie du gel numérotée,
   comme le contact DEMO).
7. **Campagne de frontière** : le balayage du levier H0 (modèle de la
   campagne 3) est rejoué sur la table LITERATURE et consigné.

## 6. Qui déclare

Deux voies, même protocole :

- **Nous** : après exécution complète de la checklist §5, la table est
  déclarée localement avec sa chronologie. Publication éventuelle
  ensuite, comme tout chantier — un feu vert explicite, un commit
  propre, aucun point automatique vers l'archive.
- **Un tiers** : ajoute sa table, sa compilation, son contact. C'est
  le seul signal d'appropriation de la machine — le tiers pèse son
  objet, la machine prête le mécanisme et le θ gelé.

Dans les deux cas, la doctrine est identique : la table dit d'où elle
vient, le mot dit ce qu'il dit, les dettes disent ce qu'on ne sait pas.

## 7. Ce que ce protocole interdit à lui-même

- De choisir maintenant la source (§3 reste ouvert) ;
- De promettre le mot du contact LITERATURE — il sera découvert ;
- De toucher au contact DEMO et à son S− figé ;
- D'utiliser la fenêtre S+ de la campagne 3 comme attente : la table
  DEMO a montré que le bruit réalisé décide, et la table LITERATURE
  aura son propre bruit, sa propre dispersion, sa propre carte.
