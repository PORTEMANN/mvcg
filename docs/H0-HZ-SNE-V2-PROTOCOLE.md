# H0-HZ-SNE — PROTOCOLE V2 : ancrage natif MU_SH0ES (déclaré avant run, 2026-09-14)

Statut : protocole gelé avant le premier run des contacts V2. Chaque
estimation pré-run ci-dessous est une honnêteté de suspense, pas un
réglage : les mots seront découverts (expected=None) et figés ensuite.

## 1. Pourquoi une V2

La paire V1 (`H0_Hz_SNe_LOWZ_LIT_{Planck,SH0ES}`) transpose l'amplitude
des bins depuis mBcorr : `mu_ancre = mBcorr + 5·log10(H0_ancrage) − K_B`,
avec K_B = convention de la table mesurée à la forme gelée. La
transposition est exacte à Ω gelés identiques, mais elle porte une
**dette d'indépendance** (la courbe de l'ancrage passe par les bins en
moyenne *par construction de conversion d'unité*) et une dette de
forme (campagne 7 : ancrage données vs carte SH0ES +0,049 mag).

La V2 retire la transposition : les bins sont les **modules de distance
publiés MU_SH0ES** (estimateur propre de la collaboration, ancrage
Céphéides natif), extraits du fichier de release Pantheon+SH0ES
(`pantheon_ref.dat`). La Table 7 VizieR ne porte pas MU_SH0ES : la
source change et est déclarée.

## 2. Méthodologie déclarée

1. Source : release Pantheon+SH0ES, 1701 LC, colonne MU_SH0ES publiée.
2. Dédoublonnage : même règle que V1 (nom normalisé, e minimal — ici
   e = MU_SH0ES_ERR_DIAG). Résultat : 1542 SNe uniques.
3. Fenêtre zHD ∈ [0,01 ; 0,15) : 598 SNe (même effectif que V1).
4. 8 bins équipopulaires, moyenne arithmétique déclarée (dette de
   compression identique à V1).
5. θ = moyenne des σ_bin, σ_bin = √(moyenne(e²)/N) : **θ = 0,02774
   mag, gelé avant le run** (règle identique à V1, valeurs quasi
   identiques : 0,02756).
6. GUM : une ligne B, decide=theta, dette de calibration commune non
   réduite (miroir V1).
7. Validation croisée (faite à l'extraction) : écart moyen V1(SH0ES
   transposé) vs V2(natif) = −0,0439 mag — cohérent avec la dette de
   forme +0,049 mag mesurée en campagne 7. La V2 ne contredit pas la
   V1, elle la mesure.

## 3. Les deux contacts miroirs (règle identique à la paire V1)

Courbe gelée posée par le contact, μ_ref = 0 (la courbe déclarée passe
par les bins), μ_loc = rms des résidus sur 8 bins :

| Contact | Courbe | Estimation pré-run honnête |
|---|---|---|
| `H0_Hz_SNe_LOWZ_V2_PLANCK` | mu_pred(z ; 67,4, Ω gelés) | résidu ≈ amplitude 5·log10(73,04/67,4) = 0,175 mag quasi constant → δ ≈ 0,178 > 2θ = 0,0555 : **S− attendu sans suspense** (miroir de V1_SH0ES, sans dette de transposition) |
| `H0_Hz_SNe_LOWZ_V2_SH0ES` | mu_pred(z ; 73,04, Ω gelés) | offset de forme attendu 0 à +0,05 mag, bruit réalisé des bins ~0,025 → δ attendu 0,025-0,056 pour θ = 0,0277 : **zone S+/P au cheveu — suspense réel** (le bruit réalisé décide) |

## 4. Dettes écrites au gel

- Calibration commune des bins non réduite (identique V1).
- MU_SH0ES incorpore les ajustements propres de la collaboration
  (Ω_m nuisance, corrections BBC) : dette de forme, non une mesure
  indépendante de la fabrication.
- Fenêtre et dédoublonnage identiques à V1 : la comparaison V1/V2 est
  appariée (mêmes SNe, deux conventions d'amplitude).
- La V2 ne remplace pas la V1 : elle la complète (ancrage natif vs
  transposition). Les quatre contacts cohabitent, fibres identiques.

## 5. Anti-tautologie

Les mots ne sont écrits nulle part avant le run (expected=None dans le
registre). Les tests figeront les mots découverts, avec la valeur exacte
du δ pour reproductibilité.
