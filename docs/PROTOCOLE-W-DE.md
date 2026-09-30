# Protocole W-DE — gel de la fibre « équation d'état de l'énergie noire »

**Statut : FERMÉ (2026-09-30, gel avant toute lecture du mot ; DESI DR3
non publié à la fermeture).** Ligne θ choisie par le propriétaire :
**pauvre (k = 2)** — grammaire k = 2 du registre. Les quatre tables sont
gelées dans `data/tables/` (DESI DR2, arXiv:2503.14738v3 + compagnon
arXiv:2503.14743v2, citations dans chaque table) :

| table | fabrication | (w₀, w_a) gelés | σ_comb gelée | mot attendu |
|---|---|---|---|---|
| wde_pp | DESI+CMB+PantheonPlus | (−0.838 ± 0.055 ; −0.62 +0.22/−0.19) | 2.8σ | P 1,4 θ |
| wde_u3 | DESI+CMB+Union3 | (−0.667 ± 0.088 ; −1.09 +0.31/−0.27) | 3.8σ | P 1,9 θ |
| wde_y5 | DESI+CMB+DES Y5 | (−0.752 ± 0.057 ; −0.86 +0.23/−0.20) | 4.2σ | S− 2,1 θ |
| wde_free | bins z (compagnon) | plancher > 3σ au bin le plus bas | > 3σ | S− > 1,5 θ |

## Empreintes SHA-256 des tables gelées

``` Hérite du brouillon du lot ext v0.5 (2026-09-28)
et de la note H0/S8 absorbée en I-D5/I-D6/I-D9.

## Ce que cette fibre pèse

L'équation d'état de l'énergie noire : le point (w₀, w_a) de la
paramétrisation CPL vs la référence ΛCDM (−1, 0). Trois fabrications SN
(un contact chacune) plus un quatrième contact sans paramétrisation :

| id | fabrication | référence à geler (citation obligatoire) |
|---|---|---|
| `W-DE-PP` | DESI + CMB + Pantheon+ | ellipse (w₀, w_a) + σ_comb publiée |
| `W-DE-U3` | DESI + CMB + Union3 | ellipse (w₀, w_a) + σ_comb publiée |
| `W-DE-Y5` | DESI + CMB + DES Y5 | ellipse (w₀, w_a) + σ_comb publiée |
| `W-DE-FREE` | reconstruction par bins en z (pas CPL) | tableau de bins, tueur de Taylor |

## Bits à geler (fermeture)

```text
id           : W-DE-GELE-2026 (à dater à la fermeture)
fibre        : W-DE
phase        : fonds
theta_type   : ancrage (ellipse combinée publiée — U, k = 2)
dimension    : {M:0, L:0, T:0, Q:0, label: "1"}   # w est un rapport p/ρ
controleur   : (w0, wa) vs (-1, 0)
ordre_param  : null
ell_m        : 1.3e26 m          # ~ c/H0, échelle de Hubble (I-D3)
echelle      : macro
```

## Ligne θ — recommandation

**Pauvre : θ = 2 σ_comb** de l'ellipse combinée publiée autour de
(−1, 0). Justification :

1. **Grammaire du registre** : la machine utilise déjà des budgets
   k = 2 (CKM : decide=U, k=2 ; HVP LO et HLbL : decide=U, k=2). La
   ligne pauvre est l'homologue exact de cette grammaire pour une
   ellipse (w₀, w_a).
2. **Honneur de la zone grise** : avec θ = 2 σ_comb, les fabrications
   Pantheon+/Union3 tombent attendues **P** (tension entre 1 et 2 θ —
   la machine documente la tension au lieu de la trancher) et DES Y5
   tombe attendue **S−** — c'est le paysage 2024-2025 réel, lu avec la
   règle, pas ajusté à elle.
3. L'alternative (serrée, θ = 1 σ_comb → S− sur les trois SN) est
   moins lisible : elle écrase la différence entre les fabrications.

**Ne pas changer de ligne après d.** La ligne finale est un choix du
propriétaire à la fermeture ; la recommandation ci-dessus est motivée,
pas figée.

## Valeurs à geler AVANT le run (non gelées à ce jour)

Pour chaque contact SN : centre (w₀, w_a), σ_comb combinée (ou les deux
axes de l'ellipse + corrélation), citation exacte (DESI 2024/2025,
compilation SN concernée). **Interdit de geler depuis la mémoire** —
transcription depuis la publication ou sa table, pixel par pixel si
figure (grammaire B1). La fermeture du protocole exige ces quatre
gels (trois SN + bins).

## Tueurs actifs

- **I-D5/F1** : interdiction `paire_coexistence` avec H0, S8, TK-IDIG,
  EDE-H0, MG. Pas de moyennage des trois SN en un seul mot.
- **I-D6/R8** : Δlog L = 0 entre les trois SN → bascule de levier, pas
  transition d'échelle (H0 reste la fibre verticale).
- **I-D7** : si W-DE-FREE reste S+ pendant que W-DE-Y5 est S−, la
  dynamique CPL est un pli de paramétrisation — HOLD de récit, pas un
  nouveau fluide.
- **Anti-tautologie** : la référence (ellipse publiée) ne pilote pas le
  calcul ; seul le protocole gelé la cite.

## Ce que cette fibre ne pèse pas

ρ_Λ en unités de Planck, H0 local, S8, f(R), EDE précoce, matière noire
(Ω_c déjà traitée en copie par le contact TR_PRED_ZeroFalsification).
Chacun est une autre fibre ou une dette nommée.

## Discipline de fermeture

1. Geler les quatre tables (citations) ;
2. Choisir la ligne θ (recommandé : pauvre, k = 2) ;
3. Hasher le protocole (SHA-256) et fermer — **avant** le prochain
   data release ;
4. Un run par contact, mots découverts, jamais choisis ;
5. La classe (R5) ne s'ouvre que si un second protocole de classe est
   gelé (I-D7).

## Empreintes SHA-256 des tables gelées

```
data/tables/wde_pp_LITTERATURE-2025.json  4425ba94943ea1f9e0d500178a40c90f5f86a62720760336d7b5386a32cd8814
data/tables/wde_u3_LITTERATURE-2025.json  676a51e3c40a25e88d09ae327681924bb6c1d912558def293d703855032b8ad4
data/tables/wde_y5_LITTERATURE-2025.json  fb73748c86ec4e03179d06abfcdc9b767f7dd0c08e5b341132bd00ea95985657
data/tables/wde_free_LITTERATURE-2025.json  3e9fd16c720b831c927be5b3ec6c4a23afe040a870faa1a7bee922083b98a20c
```

Après la fermeture, ces octets ne bougent pas (I-G1) : un changement de
θ, de ligne, de référence ou de table est un HOLD de protocole. Les mots
seront découverts à la première exécution — jamais choisis.

## Run (2026-09-30) — mots découverts

| contact | mu_loc (σ publiée) | θ | mot |
|---|---|---|---|
| WDE_PantheonPlus | 2.8 | 2.0 | **P** à 1,4 θ |
| WDE_Union3 | 3.8 | 2.0 | **P** à 1,9 θ (au cheveu de S−) |
| WDE_DESY5 | 4.2 | 2.0 | **S−** à 2,1 θ (rouge de bord) |
| WDE_FREE | 3.0 (plancher) | 2.0 | **P** à 1,5 θ |

Lecture : la ligne pauvre documente les tensions au lieu de les
écraser — PantheonPlus et Union3 sont en zone grise (la machine note
que la tension existe sans la déclarer tranchée), DES Y5 dépasse la
ligne (S−), et la reconstruction sans forme confirme la dynamique à
bas z (pas de pli CPL, I-D7). Paysage gelé : quatre fabrications, deux
P, un S− de bord, une borne — cohérent avec la préférence publiée
3,1σ (DESI+CMB) et 2,8-4,2σ (avec SN) du paysage 2024-2025.
383 tests OK au run, registre 129 contacts.

---

## Annexe (postérieure au gel — le cœur fermé ne bouge pas)

**2026-09-30 — transcription des bins w(z) (dette nommée bouclée)** :
table `data/tables/wde_free_bins_FIG7-2025.json` — transcription pixel
par pixel de la Fig. 7 (panneau supérieur) du compagnon
arXiv:2503.14743v2 (grammaire B1 : rendu pypdfium2, ancre ligne
pointillée w = −1 à y = 239, tick −2,0 à y = 368, 129 px/unité, u =
0,05 lecture graphique) :

- bin le plus bas transcrit : w ≈ **−0,86** (3 unif), **−0,86** (4 unif),
  **−0,94** (5 unif) — les trois schémas au-dessus de −1, concordants
  avec la déclaration textuelle gelée « more than 3σ » ;
- motif du croisement fantôme visible dans la transcription : le bin
  bas est au-dessus de −1, les bins médians repassent en dessous
  (−1,16 à −1,67) avant de revenir vers −1 — géométrie du signal, pas
  un pli (I-D7 confirmé) ;
- la transcription est une **annexe de preuve** : le verdict WDE_FREE
  (P à 1,5 θ) porte sur la borne plancher gelée au gel — la table
  transcrite ne re-run pas le contact (anti-tautologie) ;
- sha256 de la table transcrite : `d33fdcd476a64d75c65e0b5e23edccb9d2d5af549e4df0c774dc388c985ea51e`.
