# AMU — second contact du tiroir macro : la tension en unités de son incertitude

Contact **ouvert** (mot découvert, pas choisi). Gelé en exploration
locale le 2026-09-12, **publié le 2026-09-13** (jour J de la paire —
la dette G2 est soldée dans [`G2-CONTACT-OUVERT.md`](G2-CONTACT-OUVERT.md),
la doctrine de la paire dans [`WP25-WP20-PAIRE.md`](WP25-WP20-PAIRE.md)).
Second contact de désaccord, de nature opposée à H0 : précision de
haute énergie, écart millimétrique entre expérience et théorie,
incertitudes dominées par la physique hadronique.

## Chronologie du gel

1. **Protocole écrit avant toute exécution** : règle déclarée —
   μ_loc = l'écart déclaré de la table (a_exp − a_SM lattice WP25) =
   38·10⁻¹¹, **porté, pas calculé** depuis a_SM et a_exp séparément
   (la table ne porte pas a_exp seul : la reconstruction est
   impossible, et c'est voulu). La référence est l'identité (un SM
   complet prédit l'écart nul). θ = 63 abs gelé avant run **= u_delta
   déclarée** : le seuil est l'incertitude de l'écart elle-même.
   GUM : decide=U, k=1. Autre identification (HVP e+e−) déclarée
   dans la note, jamais choisie après coup (même honnêteté qu'O15) —
   elle aura droit à son contact séparé si quelqu'un le monte.
   Estimation pré-run : 38 ≤ 63, à 0,6 θ — suspense faible, assumé :
   c'est un contact de **calibre** de la tension, pas de suspense.
2. **Premier run** : mot découvert : **S+**, δ = 38 ≤ 63.
   Artefacts gelés offline (audit [HOLD] I-G1 / I-G2) :
   `examples/registre/AMU.*`.
3. **Figé** : mot dans `tests/test_open_amu.py`.

## Le mot : S+ — et sa lecture exacte

Avec decide=U et k=1, le seuil du verdict est l'incertitude : S+ veut
dire **« l'écart tient dans une incertitude »** — jamais « le SM est
confirmé ». C'est le pendant exact du P de H0 : là où H0 disait « l'écart
est réel mais pas encore dette structurelle au seuil choisi », AMU dit
« l'écart ne sort pas du bruit déclaré ». La tension g-2, qui fut annoncée
comme une révolution, se pesée ainsi : pas tenue *à l'échelle de son
incertitude*.

Le test verrouille la robustesse : le mot ne change pas pour k = 1, 2, 3
— un S+ à 0,6 θ n'est pas une affaire de couverture choisie après coup.

## La différence de calibre avec H0

Les deux contacts posent la même question (deux fabrications coïncident-
elles ?) avec deux étalonnages opposés :

- **H0** : θ arbitraire gelé (5 % abs) — l'incertitude est portée dans
  le GUM sans décider. Verdict : P. Le protocole parle le langage des
  écarts relatifs.
- **AMU** : θ = u_delta déclarée, decide=U — l'incertitude EST le
  seuil. Verdict : S+. Le protocole parle le langage des écarts
  normalisés.

Le tiroir macro révèle ici sa vraie question : **θ d'un contact de
désaccord doit-il être arbitraire (H0) ou naturel (AMU) ?** Les deux
choix sont honnêtes s'ils sont gelés avant le run ; le mélange des deux
sans écriture serait la faute. La doctrine provisoire : le choix d'étalonnage
fait partie du protocole, au même titre que la règle — et doit être
justifié par la nature de l'objet (échelle relative vs écart normalisé).

## Pourquoi ce contact compte (et reste local)

Il prouve que la discipline du désaccord tient sur un second objet de
nature très différente : porté-pas-calculé (anti-reconstruction),
identification multiple déclarée (honnêteté O15 généralisée), seuil
naturel gelé. La paire H0/AMU est la démonstration complète du tiroir :
même protocole, deux étalonnages honnêtes, deux mots différents —
et aucun choisi.
