# G2 — contact ouvert : le complexe g-2, les trois couleurs d'un coup

Contacts **ouverts** (mots découverts, pas choisis) — montés en
exploration locale, publiés comme tranche distincte. Trois contacts,
une seule fibre (1, 1e-11), **les trois couleurs** : AMU_exp_minus_WP20
(**S−**), HVP_LO_lat_vs_ee (**P**), HLbL_lat_vs_pheno (**S+**).

## Chronologie du gel

1. **Protocoles écrits avant toute exécution**. Le cœur du gel est
   ici un choix d'étalonnage, et il a été fait **avant** le premier
   run, par nature d'objet :
   - *AMU_exp_minus_WP20* est un écart expérience−théorie, de la même
     nature que tout contact AMU : l'étalonnage de la doctrine AMU
     s'applique — θ = u_delta déclarée, decide=U, **k=1** (le seuil
     EST l'incertitude de l'écart). μ_loc = Δ porté par la table
     (pas reconstructible depuis a_exp seul — et c'est voulu),
     μ_ref = identité 0, jamais ajustée.
   - *HVP_LO_lat_vs_ee* et *HLbL_lat_vs_pheno* sont des écarts entre
     **deux fabrications du même terme** : l'étalonnage standard de
     la machine s'applique — decide=U, **k=2**, R identité déclarée
     (indépendance assumée).
   Estimations pré-run honnêtes : WP20 S− net (δ/U = 3,67) ; HVP P
   au cheveu du S− (δ/U = 1,38 — S− à k=1) ; HLbL S+ (δ/U = 0,76 —
   P à k=1). Le suspense sur k est déclaré, pas découvert après coup.
2. **Premiers runs** : mots découverts = estimations tenues : S−, P,
   S+. Artefacts gelés offline (audits [HOLD] I-G1 / I-G2) :
   `examples/registre/{AMU20,HVP,HLBL}.*`.
3. **Figé** : mots dans `tests/test_open_g2.py`.

## La doctrine de l'étalonnage

Le complexe g-2 est la démonstration que **le choix de k fait partie
du protocole**, au même titre que la règle. Un écart exp−théorie se
normalise par son incertitude (k=1) ; un écart entre deux fabrications
se lit au standard k=2. Le même δ peut changer de couleur quand k
change — HVP et HLbL le montrent : à k=1, HVP serait S− et HLbL
serait P. Le mot publié appartient au k déclaré avant le run, et le
test fige le suspense (ratio borné, seuil déclaré) au lieu de le
cacher. La note de la mouture 6 annonçait « HLbL, k=2 → P » : erreur
arithmétique (19,2 ≤ 25,2), corrigée dans la table re-déclarée — la
table porte même la mention de sa propre correction.

## La paire d'identifications

Au gel, l'identification dispersive (e+e-) a été déclarée comme
**seconde identification** — honnêteté O15 généralisée : chaque
identification déclarée a droit à son contact séparé, et aucune n'est
choisie après coup. Le contraste est frappant et il est **porté par
le protocole, pas choisi** : l'identification lattice (WP25) donne
un écart qui tient dans une incertitude (**S+** à 0,6 U, publié dans
cette tranche) ; l'identification dispersive (WP20) donne un écart à
3,7 incertitudes (S−, publié ici). La leçon n'est pas « un des deux a
tort » — c'est que *le mot g-2 dépend de l'identification*, et que la
machine est précisément l'endroit où cette dépendance se pèse au lieu
de se décréter. La doctrine complète de la paire, y compris la
confrontation à la question de l'étalonnage (identité d'étalonnage
comme condition de comparabilité), est dans
[`WP25-WP20-PAIRE.md`](WP25-WP20-PAIRE.md).

## Périmètre et dette déclarée

Cette tranche publiait les trois contacts g-2 **sans** le contact AMU
WP25 (identification lattice) et **sans** le contact H0 : le tiroir
macro ne s'ouvrait qu'à moitié, par décision explicite. **Dette
soldée le 2026-09-13** (commit dédié, jour J) : le contact AMU WP25
est désormais publié, la paire d'identifications WP25/WP20 est
complète dans le registre — {S+:2, P:1, S−:1} dans la fibre
(1, 1e-11). H0 reste une décision indépendante, non liée à ce geste.
La doctrine interdisait que la paire soit publiée « en douce » par le
biais d'un `expected` : elle l'a été par un sync explicite, sur feu
vert, avec les deux mots côte à côte dans le README. CMD-3 est hors
moyenne e+e- déclarée dans la table HVP_LO ; c'est un levier écrit,
pas une omission.

## Pourquoi cette tranche compte

Elle prouve que la discipline du contact ouvert survit à l'objet le
plus disputé de la physique de précision : identifications multiples
déclarées, étalonnage justifié par la nature de l'objet, suspense sur
k figé, erreur de la mouture 6 corrigée et assumée. La machine n'a
pas choisi un camp dans la querelle g-2 — elle a pesé les trois
composantes et affiché trois couleurs, chacune avec son seuil gelé.
