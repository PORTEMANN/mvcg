# Protocole gelé — Chantier CORR : le corridor croisé (2 contacts)

**Gelé avant run — 2026-09-14.** Mots inconnus au gel.
Suite de l'examen du corridor_E (série E44→E68 + T5/T6, publiée le
09/09/2026) : le corridor est déjà une machine de verdicts sœur (protocoles
gelés hachés, prédictions pré-enregistrées) — ce chantier n'y cherche pas de
suspense, il y apporte la grammaire croisée S+/P/S− + GUM sur **deux tensions
inter-campagnes que le corridor n'a jamais chiffrées comme telles**.

## Ce qui n'est pas pesé (écrit, pas masqué)

- **T6** (loi à deux étages : objet ⟺ non contractile ; relation ⟺ non
  contractile ∧ ancrage externe) : une classe de lois, pas un nombre.
- **La monotonie de τ(E59)** : une fonction, mesurée sur des snapshots
  espacés de 5 (τ ∈ {5,10,15…}) — le plateau τ=5 pour A≥1 cache tout ce qui
  vit dans [5,10) ; la résolution du verdict P1 est la quantization.
- **P0 E59** (Lk=0,975 ∈ [0,9;1,1]) : validation d'harnais, S+ trivial.

## Données gelées (table `corridor_cages_LITERATURE-E2026.json`)

| grandeur | valeur | statut |
|---|---|---|
| optimum de marge E63 (n) | 14 | mesuré, κ=0,05, t=90 ; n=18 dernier en échappement (1,18) |
| minimum d'énergie par anneau E65 (n) | 18 | mesuré, cage fixe, E/n = 5,27 |
| point E61 (κ) | 0,05 | SUCCÈS, cage tient à t=90 |
| bord bas fenêtre E64-A (κ) | 0,075 | bracket (0,075; 0,1), pas de grille 0,025, t=180, n=18 |

u déclarées : u(n) = 1 (comptage entier de cages, pas d'interpolation
publiée) ; u(bord) = 0,0125/√3 (demi-largeur du bracket rectangulaire) ;
u(κ_E61) = 0 (paramètre gelé par protocole, pas une mesure).

## Contacts (2, registre meso, fibre ("1","1"), abs)

1. **CORR_Stabilite_Energie** — pred : « l'optimum de stabilité minimise
   l'énergie par anneau » (les deux facettes d'une même structure, présentées
   unies par le corridor). mu_loc = 14 (E63), mu_ref = 18 (E65).
   theta = u_delta = √2 = 1.4142135623730951 (u(n)=1 de part et d'autre),
   decide=U k=1. Estimation pré-run : delta = 4, ratio **2,83 → S− attendu
   SANS suspense** : les facettes se découplent — E68 l'avait réfuté
   qualitativement (ordre de tenue 14≫18≫24 vs ordre de bassin 18≫14≫24),
   la machine le publie en verdict.
2. **CORR_Fenetre_Point** — pred : le point E61 (κ=0,05 tient à t=90) est
   compatible avec la fenêtre E64-A (bord bas 0,075, t=180) à face value.
   mu_loc = 0,05, mu_ref = 0,075. theta = u = 0.007216878364870325
   (bracket rectangulaire, ligne unique), decide=U k=1.
   Estimation pré-run : delta = 0,025, ratio **3,46 → S− attendu, suspense
   modéré** : le point est hors fenêtre à face value ; la dette nommée est
   une tare de temps de vol (90 vs 180 — la cage tient longtemps puis fuit :
   deux horizons, pas une contradiction, mais la machine mesure l'écart).

## Anti-fraude (gelée avant run)

- La référence n'entre jamais dans le calcul (lectures de table seulement).
- Les u sont des déclarations là où le corridor ne publie pas d'incertitudes
  — écrites dans la table et le protocole, jamais rétro-ajustées.
- Toute divergence mot attendu / mot découvert sera consignée, jamais
  corrigée en silence.
