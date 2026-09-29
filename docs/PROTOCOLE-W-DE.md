# Protocole W-DE — gel de la fibre « équation d'état de l'énergie noire »

**Statut : BROUILLON EN COURS DE FERMETURE (2026-09-30).** À hasher et
fermer *avant* le prochain data release (DR3 / nouvelle compilation SN),
pas après avoir lu le σ. Hérite du brouillon du lot ext v0.5 (2026-09-28)
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
