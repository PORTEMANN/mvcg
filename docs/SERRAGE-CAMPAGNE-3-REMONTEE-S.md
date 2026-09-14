# SERRAGE — Campagne 3 : remontée des S− de bord de bande (2026-09-14, locale)

Protocole gelé : `SERRAGE-PROTOCOLE.md` (section Campagne 3 + correction
de direction). Script : `campagnes_remontee_bord.py` (MVC-G-SERRAGE-3.1).
Population : les 5 S− nus avec 2 ≤ δ/thr_home < 4, tout registre — figée :
Bertsch_Xi_Unitary, O1_Grille_H1s, O12_Cu_Gamma, O4_TK_ID_IG,
P21_H2O_dipole. Les 7 S− de la même fenêtre avec budget GUM (O17, CORR ×2,
H0 DEMO/LIT_PLANCK, AMU WP20, HVP CMD3) sont hors population (règle des
campagnes 1-2).

## Erreur conservée en trace

Première version (MVC-G-SERRAGE-3.0) : échelle descendante. Erreur de
direction — par monotonie de `_adc`, serrer le seuil d'un S− creuse
δ/thr : remontée impossible, 5 contacts plafonnés à 60 étages sans
bascule. L'échec du run a révélé l'erreur AVANT toute consigne : c'est
la machine fonctionnant comme prévu (une mesure qui ne peut pas arriver
dénonce le protocole, pas la réalité). Correction gelée au protocole,
même jour ; la direction correcte est la détente (seuil de remontée
exact : δ/2).

## Résultats

| Contact | δ | thr_home | frontière δ/2 | pos_rouge = log2(δ/2thr) | Étages | Remontée |
|---|---|---|---|---|---|---|
| Bertsch_Xi_Unitary | 0,2206 | 0,1000 | 0,1103 | 0,141 | 1 | P |
| O4_TK_ID_IG | 0,2222 | 0,1000 | 0,1111 | 0,152 | 1 | P |
| O12_Cu_Gamma | 0,2680 | 0,1000 | 0,1340 | 0,422 | 1 | P |
| P21_H2O_dipole | 0,1912 | 0,0500 | 0,0956 | 0,935 | 1 | P |
| O1_Grille_H1s | 0,0038 | 0,0010 | 0,0019 | 0,940 | 1 | P |

## Lecture

Comme en campagne 2, le k ne discrimine pas (fenêtre [2,4) ⇒ δ/2 < 2·thr
partout ⇒ remontée au premier palier). La position, si — et elle
répartit les rouges en trois mêmes familles que les verts :

- **Rouge chaud (0,14–0,15)** : Bertsch Ξ unitaire, O4 (TK ID/IG) —
  collés à la frontière P : un δ à peine plus petit et c'était un P.
  Désaccords marginaux, pas des échecs de modèle.
- **Rouge moyen (0,42)** : O12 (γ Cu) — au milieu de la fenêtre.
- **Rouge franc (0,94)** : P21 (dipôle H₂O Pauling), O1 (grille H1s) —
  au bord haut de la fenêtre : proche du double de la frontière. Là le
  désaccord est structurel.

## Les trois campagnes forment un système complet

Chaque contact nu du registre possède désormais une coordonnée continue
dans sa zone : θ\* (profondeur verte, camp 1), pos_bande (position ambre,
camp 2), pos_rouge (profondeur du rouge, camp 3). Les trois mesures sont
des lectures du même δ sous trois angles de la règle `_adc` — jamais
une modification de celle-ci. L'information de justesse n'est plus jetée.

## Limites déclarées

- δ mesure, pas incertitude ; pas de moyenne ; erreurs en trace.
- Contacts GUM hors population (7 S− de la même fenêtre non lus —
  chantier régime U, distinct).
- Fenêtre [2,4) arbitraire mais gelée ; les S− profonds (δ/thr ≥ 4, la
  majorité du rouge) restent non gradués — leur profondeur se lit déjà
  directement sur l'axe δ/θ de la carte.

## Prolongements possibles

- Couche carte : encoder les trois positions en teinte des pastilles —
  la carte devient un gradient de justesse sous les trois couleurs figées.
- Régime U : serrage/détente de U jusqu'à bascule (population : contacts
  decide=U, les 7 exclus de cette campagne + les S+/P du régime U).
