# HVP ππ — CMD-3 vs moyenne pré-CMD-3 : le désaccord exp-exp du canal dominant

Contact **ouvert** (mot découvert, pas choisi). Gelé en exploration
locale le 2026-09-14 — premier contact de la **campagne croisée** :
deux fabrications expérimentales du même terme, portées telles que
publiées, jamais recombinées.

## Pourquoi ce contact, pourquoi maintenant

La doctrine du chantier SPEC a montré que le tranchant de la machine
vient du croisement de deux voies indépendantes vers le même objet.
Le canal 2π de a_μ^had,LO est l'observable du moment : il domine le
terme HVP (~70 %) et deux fabrications en portent des valeurs qui
divergent au-delà de trois incertitudes, la comparaison étant publiée
par la collaboration CMD-3 elle-même.

## Chronologie du gel

1. **Protocole écrit avant toute exécution** : règle déclarée —
   μ_loc = écart porté tel que publié dans le PRL CMD-3 :
   a_μ^had,LO(2π, CMD-3) = 5260(42) ×10⁻¹¹ contre
   a_μ^had,LO(2π, moyenne pré-CMD-3) = 5060(34) ×10⁻¹¹
   → δ = 200 ×10⁻¹¹, **porté, pas calculé** depuis les sections
   efficaces. La référence est l'identité (deux fabrications du même
   objet → écart attendu nul). θ = u_delta gelé avant run =
   √(42² + 34²) = 54,037 ×10⁻¹¹, **indépendance assumée** (même
   convention que la table hvp_lo). GUM : decide=U, k=1 — l'étalonnage
   de la doctrine AMU (l'incertitude EST le seuil pour un écart
   normalisé entre fabrications).
   **Identification multiple déclarée** : la moyenne pré-CMD-3 est
   KLOE-dominée (KLOE, BABAR, CMD-2, SND). Un contact « KLOE seul »
   exigerait une valeur KLOE sur la fenêtre exacte CMD-3, non publiée
   — identifiée, jamais choisie après coup (honnêteté O15/AMU).
   **Dette de fenêtre** : CMD-3 exclusif sur 0,327–1,2 GeV + moyenne
   des autres mesures au-delà ; la moyenne précédente porte le canal
   entier. La comparaison est celle que CMD-3 publie, portée telle
   quelle — la dette est écrite, pas corrigée.
   Estimation pré-run : 200 > 54 → zone S− à ~3,7 θ — suspense
   faible, assumé : c'est un contact de **calibre** (le désaccord
   exp-exp central de la physique actuelle), pas de suspense.
2. **Premier run** : mot découvert : **S−**, δ = 200,0 contre θ = 54,037 —
   à **3,70 θ** : deux fabrications expérimentales du même terme se
   séparent au-delà de trois incertitudes déclarées, exactement
   l'estimation pré-run annoncée (~3,7 θ). Le protocole a dit vrai :
   suspense nul, calibre total.
3. **Figé** : mot dans `tests/test_open_hvp_pipi_cmd3.py`.

## Lecture attendue du mot

Avec decide=U et k=1, un S− dira « deux fabrications du même terme
se séparent au-delà de trois incertitudes déclarées » — jamais « une
expérience a tort » : la machine pèse l'écart, elle n'arbitre pas
l'expérience. Un S+ inattendu dirait « la tension CMD-3/pré-CMD-3 ne
sort pas du bruit déclaré » — ce serait un résultat au moins aussi
fort, dans l'autre sens.

## Place dans la fibre

Dimension 1e-11, packet « 1 » : le contact rejoint la fibre g-2
(WP25, WP20, HVP_LO, HLbL) — même terme physique, nouvelle paire de
fabrications : expérience scan (CMD-3, VEPP-2000) contre moyenne
dominée par l'ISR (KLOE). C'est le premier contact exp-vs-exp de la
machine : jusqu'ici, la fibre croisait fabrication exp vs fabrication
lattice/pheno.
