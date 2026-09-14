# H0 — H(z) bas-z, V2 : contacts ouverts sur MU_SH0ES natif

**Statut : deux contacts ouverts, mots découverts et figés le 2026-09-14.**
**Fibre :** `("1", "mag")` — la fibre des modules de distance.

## Ce que V2 change par rapport à V1

La paire LITERATURE (V1, `H0_Hz_SNe_LOWZ_LIT_*`) pesait les mêmes 8 bins
équipopulaires de Pantheon+ (Brout et al. 2022, Table 7, 598 SNe dans la
fenêtre zHD [0,01 ; 0,15)), mais l'amplitude de chaque bin était **transposée**
depuis l'ancrage déclaré (`mu = mBcorr + 5·log10(H0_ancrage) − K_B`). La
campagne 7 a mesuré la dette de cette transposition : **+0,049 mag** de forme
résiduelle (les ajustements propres de la collaboration — Ω_m, nuisance —
sont déjà dans les MU publiés, pas dans mBcorr brut).

V2 reprend **MU_SH0ES tel que publié dans la release Pantheon+** : ancrage
natif, dette de forme supprimée. Mêmes bins, même fenêtre, même règle de
dispersion (σ_bin = √(moyenne(e²)/N), e = MU_SH0ES_ERR_DIAG). θ gelé avant
run : **0,027737 mag**.

Correction de protocole : le runner V1 ignorait silencieusement son argument
d'ancrage et lisait H0 = 67,4 en dur. Le runner V2 lit le H0 de courbe **dans
la table** (`params.H0_courbe_*`) — le H0 posé est déclaré par la table,
jamais choisi après coup.

## Règle gelée (déclarée avant run, protocole H0-HZ-SNE-V2-PROTOCOLE.md)

- Courbe posée par le contact : `mu_pred(z ; H0_courbe déclaré, Ω gelés 0,315/0,685)`.
- `mu_loc = rms` des résidus `mu_pred − mu_obs` sur les 8 bins ; `mu_ref = 0`.
- θ = 0,027737 mag (σ bins déclarée, gelée avant run).
- GUM : une ligne B (incertitudes déclarées MU_SH0ES_ERR_DIAG/√N),
  `decide="theta"`, k=2. Note portée : calibration commune non réduite (dette).
- `expected = None` pour les deux : mot inconnu au gel.

## Mots découverts (premier run, figés ensuite dans les tests)

| Contact | Courbe posée | δ (mag) | δ/θ | Mot |
|---|---|---|---|---|
| `H0_Hz_SNe_LOWZ_V2_PLANCK` | Planck 67,4 | 0,178285002738 | 6,43 | **S−** |
| `H0_Hz_SNe_LOWZ_V2_SH0ES` | SH0ES 73,04 | 0,024876389328 | 0,897 | **S+** |

Estimations pré-run vs réalisé :

- **V2_PLANCK** : estimé S− sans suspense (décalage ~ +0,1766 mag quasi
  constant, miroir exact du V1 ancré SH0ES) → réalisé S− à 6,4 θ. Conforme.
- **V2_SH0ES** : estimé S+ au cheveu (bruit réalisé attendu ~ 0,897 θ) →
  réalisé S+ à 0,8969 θ. Conforme, au cheveu près. **Premier S+ de la
  fibre `("1","mag")`.**

## Ce que la carte en tire

Poser la courbe SH0ES sur les distances natives SH0ES donne un résidu qui
tient dans θ : la fabrication s'auto-étalonne de façon interne cohérente
à hauteur du bruit déclaré des bins. Poser la courbe Planck sur ces mêmes
distances décale les bins de plus de 6 θ. **La tension H0 se lit déjà dans
les modules de distance bas-z**, indépendamment de l'échelle absolue (la
dégénérescence M–H0 n'est pas levée par ces contacts, comme en V1) : ce que
les deux fabrications ne partagent pas, ce n'est pas l'étalonnage des SNe,
c'est H0 lui-même.

Miroir propre : V1_SH0ES (courbe Planck sur bins transposés SH0ES) était
S− à 0,2314 mag ; V2_PLANCK (courbe Planck sur MU natifs) est S− à
0,1783 mag. L'écart 0,2314 − 0,1783 = 0,053 ≈ la dette de forme mesurée
(+0,049, campagne 7) — la suppression de la dette se voit exactement là
où elle était annoncée.

## Dettes écrites (non levées par V2)

- Calibration commune des bins non réduite (GUM portée, non utilisée pour
  le mot).
- Forme résiduelle : Ω gelés 0,315/0,685 vs ajustements de la collaboration.
- V2 complète V1 sans la remplacer : les deux paires restent gelées côte à
  côte, la différence entre elles est elle-même une mesure (la dette de forme).

## Résidus calculés à l'extraction (validation croisée)

Courbe SH0ES : rms 0,02488 mag, offset moyen +0,0020. Courbe Planck : rms
0,17829 mag, offset +0,1766. Validation croisée V1(transposé SH0ES) vs V2
(natif) : écart moyen −0,0439 mag, max 0,0444 — cohérent avec la dette de
forme +0,049 mesurée par la campagne 7.
