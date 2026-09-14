# SERRAGE — protocole de serrage d'étalonnage (gelé avant run, 2026-09-14)

## Motif

Constat carte (2026-09-14) : 12 des 26 S+ sont alignés sur θ = 0,1, seuil
déclaré standard de la série O. La couleur ne distingue pas un modèle à 9 %
d'un modèle à 0,1 % : l'information de justesse est jetée à chaque pesée.
La justesse existe pourtant, sous forme continue : le seuil de bascule.

## Définitions

- **Régime du contact** : `theta` (le seuil de décision est θ) ou `U`
  (le seuil de décision est U, budget GUM gelé, decide=U). Règle partagée
  avec le reste de la machine : `_thr_contact`.
- **θ\* de bascule** : valeur exacte du seuil où le verdict quitte S+.
  La règle `_adc` étant monotone en le seuil, pour un δ fixé :
  bascule S+→P à `thr = δ`, bascule P→S− à `thr = δ/2`.
- **Étages de serrage** : nombre de divisions par 2 du seuil home que le
  verdict S+ survit : `étages = floor(log2(thr_home / δ))` pour le régime
  theta. Grandeur binaire en octaves — la justesse mesurée telle que la
  machine peut l'atteindre sans rien changer à sa règle de verdict.

## Protocole (gelé avant run)

1. Population : les contacts S+ à θ = 0,1 sans budget GUM — la série O
   plus ses deux voisins NMR et Landau (10 contacts, rel, decide=-).
2. Pour chaque contact : échelle de serrage `thr_k = thr_home / 2^k`,
   k = 0, 1, 2, … jusqu'au premier verdict ≠ S+, plafonné à 60 étages.
   La trace complète (seuil, verdict) est conservée — jamais tronquée.
3. Mesures consignées par contact : `delta`, `theta_etoile = delta`
   (frontière exacte), `etages` (floor(log2(thr_home/δ))), et la trace.
4. La couleur du contact n'est PAS modifiée : le serrage est une mesure
   dérivée additionnelle, le registre figé reste la seule source des mots.
5. Erreurs conservées : un contact dont la re-lecture échoue apparaît
   en trace avec son échec, pas filtré.

## Ce que le protocole ne fait pas

- Pas de modification de θ déclaré des contacts (l'étalonnage gelé reste).
- Pas de serrage de U (contacts decide=U hors population : régime distinct,
  chantier séparé si demandé).
- Pas de moyenne entre contacts : chaque θ\* est lu seul.

## Statut

Campagne 1 (série O, 10 contacts) : résultats dans
`SERRAGE-CAMPAGNE-1-SERIE-O.md`. Locale, non publiée.

## Campagne 2 — détente des P (ajout gelé 2026-09-14, après feu vert)

Symétrique de la campagne 1. Population : les P à θ = 0,1 sans budget
GUM — 5 contacts (O2, O3, NMR_Karplus_Sheet, NMR_Karplus_Helix_VogeliBax2007,
NMR_Karplus_Sheet_VogeliBax2007 ; la série O au sens strict n'en compte
que 2 — la population retenue inclut ses voisins NMR, comme en campagne 1).

1. Échelle de détente `thr_k = thr_home · 2^k` jusqu'au premier S+, plafond 60.
2. Mesures : `etages_detente` (k de bascule) et `pos_bande = log2(δ/θ_home)`
   — position dans la bande P, 0 = frontière S+, 1 = frontière S−. C'est
   `pos_bande` qui discrimine : tous les P de la population ont δ/θ ∈ [1,2],
   donc basculent au palier k = 1.
3. Mêmes règles que la campagne 1 : trace complète conservée, couleur
   non modifiée, pas de moyenne, erreurs en trace.

## Campagne 3 — descente des S− de bord de bande (ajout gelé 2026-09-14)

Dernière arête. Population : contacts NUS (sans budget GUM — même règle
que les campagnes 1-2), verdict S−, 2 ≤ δ/thr_home < 4, sur tout le
registre (toute θ). Figée à 5 contacts : Bertsch_Xi_Unitary, O1_Grille_H1s,
O12_Cu_Gamma, O4_TK_ID_IG, P21_H2O_dipole. Les 7 S− de la même fenêtre
avec budget GUM (O17, CORR ×2, H0 DEMO/LIT_PLANCK, AMU WP20, HVP CMD3)
sont HORS population : régime déclaré distinct, chantier séparé.

1. Échelle descendante `thr_k = thr_home / 2^k` jusqu'au premier verdict
   ≠ S−, plafond 60.
2. Mesures : `frontiere_remontee = δ/2` (seuil exact où le S− remonte en
   P, par monotonie de `_adc`), `profondeur = log2(2·thr_home/δ)` —
   octaves sous la frontière : 0 = collé au P, 1 = au double de la
   frontière (bord haut de la fenêtre).
3. Mêmes règles : trace complète conservée, couleur non modifiée, pas de
   moyenne, erreurs en trace.

### Correction de direction (gelée, même jour)

La section Campagne 3 ci-dessus serrait le seuil VERS LE BAS — erreur.
Par monotonie de `_adc`, serrer le seuil d'un S− creuse δ/thr : le S− ne
peut JAMAIS remonter. Le premier run (protocole MVC-G-SERRAGE-3.0) a
plafonné les 5 contacts à 60 étages sans remontée : l'échec est conservé
en trace et à motivé cette correction. Direction correcte : détente
`thr×2^k` jusqu'au premier ≠ S− (seuil de remontée exact : δ/2).
Script définitif : `campagnes_remontee_bord.py` (MVC-G-SERRAGE-3.1).
Mesure discriminante : `pos_rouge = log2(δ/(2·thr_home))` ∈ [0, 1) —
0 = collé au P, 1 = bord haut de la fenêtre.
