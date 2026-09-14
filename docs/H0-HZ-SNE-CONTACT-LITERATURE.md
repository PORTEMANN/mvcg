# H0 bas-z LITERATURE — la paire ancrée (contact complet)

Contacts **ouverts**, chantier local (2026-09-13 soir), non publiés.
`H0_Hz_SNe_LOWZ_LIT_PLANCK` et `H0_Hz_SNe_LOWZ_LIT_SH0ES` — mots figés :
**S− / S−** (δ = 0,0695 mag / δ = 0,2314 mag), θ = 0,02756 mag gelé
avant run. Première pesée de la machine sur une **carte réelle** dans
le domaine macro — la dette de nature du contact DEMO est soldée,
les dettes de compression, d'ancrage et d'indépendance sont écrites.

## Chronologie du gel

1. **Protocole écrit avant toute table** (`H0-HZ-SNE-PROTOCOLE-
   LITERATURE.md`) : règle gelée du contact DEMO réutilisée telle
   quelle (rms des résidus, μ_ref = 0), θ = dispersion déclarée de la
   table fixée avant tout run, GUM une ligne B decide=theta.
2. **Faisabilité** (`H0-HZ-SNE-LITERATURE-FAISABILITE.md`) : Pantheon+
   vérifie A1–A3 (références relues, diagramme binned publié,
   dispersion BS21 publiée) ; diagnostic A5 : les μ BBC sont sans
   amplitude ancrée (dégénérescence M–H0, Brout et al. 2022 §2.3) —
   l'ancrage devient partie de la déclaration, chaque ancrage sa
   carte.
3. **Extraction déclarée** (`extraction_literature.py`) : Table 7 de
   Brout et al. 2022 (VizieR J/ApJ/938/110) — 1701 light curves
   dédoublonnées par nom normalisé (1542 SNe ; règle : e_mBcorr
   minimal), fenêtre zHD [0,01 ; 0,15) = 598 SNe (calibrateurs
   Céphéides exclus, tous z < 0,01), 8 bins équipopulaires à moyenne
   arithmétique déclarée, σ_bin = √(moyenne(e_mBcorr²)/N) = 0,02756.
   Amplitude : transposition exacte à Ω gelés identiques,
   μ = mBcorr + 5·log10(H0_A) − K_B, K_B = 28,52698 (convention de
   la table mesurée à la forme gelée). Validation croisée : std(A−m) =
   0,160 mag à z ≥ 0,01 vs rms ~0,15 publié (Table 2) — écart des Ω
   gelés déclaré, non corrigé.
4. **Estimation pré-run honnête** : carte Planck — résidu = bruit
   réalisé des bins, δ ~0,02–0,04 attendu, zone P au cheveu, suspense
   réel ; carte SH0ES — résidu moyen +0,1745 mag quasi constant
   (exact à Ω gelés identiques), S− attendu sans suspense.
5. **Premier run** : mots découverts — **S− / S−**. Carte Planck :
   δ = 0,0695 mag, le bruit réalisé des bins (hétérogénéité surveys,
   vitesses résiduelles, écarts de forme Ω gelés vs données) dépasse
   2θ = 0,0551 : l'estimation P était fausse du côté du bruit, comme
   annoncé possible. Carte SH0ES : δ = 0,2314 mag, estimation
   confirmée.
6. **Figés** : mots et valeurs à 12 décimales dans
   `tests/test_open_hz_lit_planck.py` et `tests/test_open_hz_lit_
   sh0es.py` ; compteur de la série local 44 → 46 ; fibre (« 1 », mag)
   1 S− → 3 S−. Suite locale : 203 tests verts.

## Ce que dit la machine (sur ces cartes déclarées)

- **Carte Planck (ancrage 67,4)** : la courbe Planck (Ω gelés
  0,315/0,685) manque les bins Pantheon+ ancrés Planck de 0,0695 mag
  en rms — au-delà de 2θ. Les μ binnés non pondérés ne passent pas
  par la courbe « à hauteur du bruit déclaré » (σ_bin = 0,0276). Le
  défaut mesuré est de l'ordre de 2,5 σ déclarés des bins — la dette
  de compression (calibration commune non réduite en √N, bins non
  pondérés) participe de ce résidu : lecture honnête = défaut mixte
  (forme Ω gelés vs données + hétérogénéité), pas un verdict Planck.
- **Carte SH0ES (ancrage 73,04)** : la courbe Planck manque les bins
  de 0,2314 mag — la tension H0 relue par les SNe binnées, dans la
  carte de l'échelle locale. L'écart de fabrication 0,1745 mag y est
  majoritaire (en quadrature : √(0,0695² + 0,1745²) = 0,188 ; le
  réalisé 0,231 montre que bruit réalisé et décalage ne s'additionnent
  pas en quadrature pure — déclaré, pas ajusté).
- **Les deux cartes S−** : aucun ancrage ne rend la courbe Planck
  compatible des bins au seuil déclaré. Le miroir exact (transposition
  de 0,1745 mag, gelée comme propriété de déclaration) veut que les
  deux contacts portent la même information sous deux dettes — c'est
  écrit dans les tables, pas découvert.

## Lectures

1. **La machine a pesé son premier objet macroscopique réel.** Même
   mécanisme que la DEMO (intégrale H(z), rms, gel, mot découvert) —
   seule la table a changé, comme annoncé. La doctrine a tenu la
   promesse du protocole.
2. **Le suspense de la carte Planck était réel et il a parlé.** Le
   bruit réalisé a basculé le mot dans la zone S− — exactement le
   genre de décision que la campagne 3 avait cartographiée sur la
   DEMO (fenêtre P au cheveu). Une campagne de frontière sur la carte
   LITERATURE (levier H0, modèle campagne 3) montrerait où le mot
   bascule — chantier ouvert.
3. **L'ancrage est devenu visible comme dette.** La dégénérescence
   M–H0 interdît l'amplitude sans échelle ; la machine ne choisit pas
   l'ancrage, elle pèse les deux cartes et écrit les dettes. Si un
   tiers déclare un troisième ancrage (BAO, chronomètres cosmiques
   comme amplitude indépendante), la carte correspondante entrera
   dans le même casier.

## Dettes (récapitulatif, écrites dans les tables)

- D-nature : soldée (donnée réelle) — remplacée par la compression.
- D-compression : bins non pondérés ; C_stat/C_syst ignorées ;
  calibration commune non réduite en √N.
- D-ancrage / D-indépendance : la paire (miroir exact) ; pour SH0ES
  la donnée et le levier ne sont pas indépendants (pendant Landau).
- D-vitesses : zHD corrigé 2M++, sensibilité résiduelle (R22 n'use
  le flux Hubble que pour z > 0,023 ; notre fenêtre basse en porte).

## Honnêteté (limites déclarées)

- La comparaison DEMO ↔ LITERATURE se lit avec la conscience que
  leurs θ diffèrent (0,05 vs 0,02756) — chacun = sa dispersion.
- Le S− de la carte Planck engage la chaîne d'extraction déclarée ;
  une extraction pondérée (covariance officielle) déplacerait le
  résidu — c'est la dette de compression, pas un oubli.
- La campagne de frontière (levier H0) n'est pas encore jouée sur
  ces cartes : elle est le pendant naturel de la campagne 3.
