# H0 — Bilan consolidé du chantier (campagnes 1-11)

Document de synthèse, local, non publié (2026-09-14). **Aucun contact
créé, aucun gel touché** pendant tout le chantier (les deux mots
S−/S− sont restés figes). Suite de tests : 203/203 verts au dernier
run. Ce document consolide — il ne remplace pas les documents de
campagne, qui portent les protocoles et les limites déclarées.

## 1. Les deux contacts gelés (rappel verbatim)

| Contact | Mot | δ | θ |
|---|---|---|---|
| `H0_Hz_SNe_LOWZ_LIT_PLANCK` | **S−** | 0,06949833902331774 | 0,02756 |
| `H0_Hz_SNe_LOWZ_LIT_SH0ES` | **S−** | 0,23136304438473587 | 0,02756 |

Cartes fabriquées en campagne 4 : μ_binned(z) sur 8 bins équipulés,
deux fabrications Planck (67,4) et SH0ES (73,04) à Ω gelés
0,315/0,685. Tout le chantier est **dérivé** : mesurer la marge, la
dette et le bruit autour de ces deux mots, sans jamais les rouvrir.

## 2. Le fil des onze campagnes

| C | Question | Réponse chiffrée |
|---|---|---|
| 1-2 | Relance du protocole (LOWZ, bins) | faisabilité, frontières, 8 bins |
| 3 | Frontière du contact sur H(z) | protocole verrouillé |
| 4 | Frontière littérature (θ = 0,02756) | fenêtres P [68,07 ; 70,03] / [73,77 ; 75,89], S+ inaccessible, miroir exact |
| 5 | Sensibilité à la compression | position robuste < 0,1, σ_var −19 % |
| 6 | Covariance complète STAT+SYS 1701×1701 | **χ²/ndof = 4,47** : la dette ne blanchit pas ; σ covariée ratio 0,88 θ |
| 7 | Sélection officielle (277 LC, doublons portés) | χ²/ndof = 2,774 ; ancrage données +0,049 mag vs carte SH0ES ; **H0* données = 73,36** |
| 8 | Fit conjoint (H0, Ω_m) | dette de forme **Δχ² = 0,062** (négligeable) ; verdicts à **Δχ² ≈ 21** de marge |
| 9 | Chasse par survey | FOUND par masse (+4,04) / SOUSA par tête (0,40 χ²/LC, −0,185 mag) / paire CFA4p3 (+0,084) / PS1MD +0,028 (2σ) ; H0* stable ±0,2 |
| 10 | Split en z | **pas de micro-tension** (ΔH0 < 1σ) ; excès = phénomène **bas-z** ; haut-z blanc (0,92 / 0,45) |
| 11 | Test VPEC | **innocenté** : pente +0,19 ± 0,54 (0,35 σ), « correction absente » exclue à 3,7 σ |

## 3. Ce que la machine sait maintenant (réponses consolidées)

**Sur la position.**
H0* = 73,3-73,4 est robuste à tout ce qui a été tenté : binnings
(C5), sélection (C7, 236/238 noms déjà présents), retraits survey par
survey (C10 : 73,25-73,55), split bas/haut-z (C10 : ΔH0 < 1σ), gel ou
libération des Ω (C8 : 73,35 → 73,20). Côté données officielles, la
forme gelée à Ω constants retombe à **73,36**, en zone SH0ES, à ~1,5
du centre rms SH0ES gelé (74,82).

**Sur les verdicts gelés.**
Leur marge n'a pas été érodée, elle a été **mesurée** : même l'adversaire
optimal à deux paramètres libres (C8) laisse l'ancre Planck (67,4 ;
0,315) à Δχ² = 21,3 du meilleur ajustement possible. Les S−/S− sont
des verrous à ~4,6 σ, pas des jugements à l'emporte-pièce.

**Sur la dette.**
Elle est passée de soupçon (C4) à chiffrage (C6 : ×2,1 en dispersion)
à localisation (C10 : bas-z uniquement) à mécanisme testé (C11 : pas
cinématique). Le haut-z blanchit à χ²/ndof < 1 : la dette complète du
contact est une **dette locale**, portée par l'hétérogénéité des
surveys bas-z (C9) — dispersion réelle au-delà du publié, cohérente
avec la littérature de diagnostic Pantheon+ (arXiv:2212.07917).

## 4. Honnêteté (limites ouvertes du chantier)

1. **Sélection 591 vs 598** (nommage/e_diag VizieR vs .dat) : effet
   de l'ordre des pourcents, non nul (C6).
2. **Fit d'échelle Céphéide–SN non refait** : les calibrateurs (77 LC /
   43 noms) sont déclarés hors doctrine de la forme gelée (C7).
3. **Mécanisme exact de l'excès bas-z non identifié** : cartographié
   (surveys, zone z, non-VPEC), pas expliqué physiquement (C9-C11).
4. **Paire CFA4p3** (+0,084 mag à n = 2) : signal à confirmer, SE non
   interprétable (C9).
5. **Analyses dérivées Ω libre** : jamais réinjectées dans les
   contacts ni les cartes (C8).
6. **Puissance limitée** du test VPEC (r ≈ 0,02) : non-détection ≠
   preuve d'absence totale (C11).

## 5. Artéfacts du chantier (tous locaux, non suivis)

Scripts : `campagnes_h0_relance.py`, `campagnes_h4_literature.py`,
`campagnes_h5_compression.py`, `campagnes_h6_covariance.py`,
`campagnes_h7_selection_officielle.py`,
`campagnes_h8_separation_forme_dispersion.py`,
`campagnes_h9_chasse_exces.py`, `campagnes_h10_split_z.py`,
`campagnes_h11_vpec.py`.
Docs : `H0-CAMPAGNES-1-2`, `H0-CAMPAGNE-3` à `H0-CAMPAGNE-11`,
`H0-HZ-SNE-CONTACT-OUVERT`, `H0-HZ-SNE-CONTACT-LITERATURE`,
`H0-HZ-SNE-LITERATURE-FAISABILITE`, `H0-HZ-SNE-PROTOCOLE-LITERATURE`.
Données : `pantheon_ref.dat`, `pantheon_t7.csv`,
`pantheon_STATONLY.cov`, `pantheon_STAT+SYS.cov`, `brout2022.pdf`,
tables dérivées `hz_sne_LOWZ-LITERATURE-{Planck,SH0ES}[-WEIGHTED].json`.

## 6. Pistes ouvertes (prochaines campagnes possibles)

- **Zoom PS1MD** : seul offset positif significatif, uniforme en z —
  étendre le diagnostic (sous-échantillons PS1MD internes).
- **Rétest de la paire CFA4p3** : chercher 2010ag/2010dt dans les
  relevés d'origine (CfA) pour confirmer l'offset +0,084 mag.
- **Excès résiduel haut-z** : χ²/ndof = 0,45 sur le split 0,07 —
  tester la sur-estimation de covariance à petit effectif.
- **V2 déclarative** : si un jour la machine ouvre une V2 des
  contacts, l'ancrage natif est `MU_SH0ES` (référence d'ancrage
  officielle, dette de forme +0,049 mag à écrire dans la doctrine).
