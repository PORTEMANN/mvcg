# WP25/WP20 — doctrine de la paire : un objet, deux identifications, deux mots

Document d'exploration écrite **avant** la décision, publié avec elle :
le 2026-09-13 (jour J), la paire a été montée — contact `AMU_Delta_WP25`
synchronisé, les deux mots sont publics côte à côte. Ce texte garde la
chronologie telle qu'elle s'est passée et la doctrine qui la tient ;
la confrontation à la question de l'étalonnage (§ bas) a été ajoutée
le jour même, avant le sync.

## Chronologie telle qu'elle s'est passée

1. **WP25 gelé en premier** (contact `AMU_Delta_WP25`, local) : écart
   porté 38·10⁻¹¹, θ = u_delta = 63, decide=U, **k=1** — l'étalonnage
   de l'écart normalisé. Mot découvert : **S+** (à 0,6 θ). Au même
   gel, l'identification dispersive (e+e-/WP20) était déclarée comme
   identification sœur — honnêteté O15 : elle aurait droit à son
   contact séparé.
2. **WP20 monté ensuite** (`AMU_exp_minus_WP20`) : même objet, même
   étalonnage (θ = u_delta = 76, k=1). Mot découvert : **S−** (à
   3,67 U, net jusqu'à k = 3). Publié seul (commit `89498dd`), avec
   la dette WP25 écrite dans la doctrine G2.
3. **La paire existe donc déjà** — dans l'arbre local. Ce document
   dit ce qu'elle vaut et ce que sa publication exigerait.

## Ce que la paire prouve

Même objet (Δa_μ), même protocole (écart porté, identité de
référence, θ = u_delta, k=1 gelé avant run), **deux mots opposés** :
S+ à 0,6 incertitude d'un côté, S− à 3,7 de l'autre. La conclusion
que la machine autorise — et qu'elle seule autorise proprement — est :

> **Le verdict g-2 n'est pas une propriété de l'univers. C'est une
> fonction de l'identification hadronique.** Lattice : l'écart tient
> dans une incertitude. Dispersif : l'écart est une dette de 3,7 σ.

Tout le reste du débat public (qui a tort, quelle collaboration a
raison) est en dehors du périmètre : la machine pèse les
identifications déclarées, elle ne juge pas les collaborations.

## Les deux interdits de la paire

- **Interdit de moyenner.** Combiner WP25 et WP20 en un « consensus »
  pour fabriquer un mot unique serait exactement le geste que la
  doctrine H0 a proscrit (« ne pas moyenner deux fabrications »).
  La paire vit parce que ses deux mots restent intacts et opposés.
- **Interdit de choisir.** Publier WP25 *parce que* son mot est S+,
  ou le garder local *parce que* WP20 est déjà S−, serait le péché
  originel du registre : un mot choisi après coup. L'ordre de
  publication (WP20 d'abord) est un fait historique gelé, pas une
  préférence. Si WP25 est un jour publié, ce sera pour une raison
  écrite avant le run — comme tout le reste.

## Leviers déclarés (chaque mot a le sien)

- **WP25** (S+) : levier `HVP←e+e-` — déjà exercé par le contact WP20.
  Autres leviers lattice : autre ensemble (le u=63 porte déjà
  l'incertitude des ensembles déclarée), autre extrapolation
  RBC/UKQCD. Le mot S+ de WP25 est *fragile par construction* :
  c'est un contact de calibre, pas de suspense.
- **WP20** (S−) : levier `ee←autre-moyenne` — CMD-3 déjà hors
  moyenne, déclaré dans la table. Le mot S− est robuste (k jusqu'à 3).
- **La paire elle-même** : son levier est la publication — une
  réanalyse lattice qui déplacerait 38 au-delà de 63 ferait basculer
  le S+ ; une réanalyse dispersive qui rapprocherait 279 de 76 ferait
  remonter le S−. La paire transforme deux contacts de calibre en un
  instrument de veille sur l'état de l'art hadronique.

## Ce que la publication de la paire exigerait (checklist du jour J)

1. **Décision écrite avant tout sync** : WP25 seul, ou la paire, et
   dans les deux cas la doctrine G2 révisée (la section « périmètre
   et dette » doit devenir fausse proprement — une dette soldée se
   déclare comme telle, elle ne s'efface pas).
2. **H0 reste une décision indépendante.** La paire WP25/WP20 ouvre
   le tiroir macro AMU ; H0 est un objet de nature différente
   (deux fabrications d'une constante, θ arbitraire gelé). Rien ne
   les lie ; les publier ensemble « parce que c'est le tiroir macro »
   serait un geste de paquet, pas de protocole.
3. **Matériel déjà prêt** (local) : contact `AMU_Delta_WP25`, gel
   offline `examples/registre/AMU.*` (audits [HOLD]), tests figés
   `tests/test_open_amu.py`, doctrine `docs/AMU-CONTACT-OUVERT.md`.
   Le sync serait chirurgical : ce bloc, et rien d'autre.
4. **Frozen counts à reboucher** : local 39 lignes / 11 fibres ;
   le dépôt passerait de 37 à 38 lignes, la fibre (1, 1e-11) de
   {S+:1, P:1, S−:1} à {S+:2, P:1, S−:1} — la paire visible dans le
   classement, ce qui est précisément le but.
5. **Le README devra dire les deux mots côte à côte** — WP25 S+ à
   0,6 U, WP20 S− à 3,7 U — sans ligne de commentaire qui explique
   lequel croire. La machine n'a pas à croire : elle a pesé.

## Pourquoi attendre (et pourquoi ce document)

La paire publiée est l'exposition maximale de la machine : elle dit,
en plein champ de bataille, « nos propres identifications déclarées
se contredisent au-delà de 3 σ, et nous publions les deux ». C'est la
preuve ultime de discipline — et un invitation directe aux
évaluateurs. Ce document existe pour que ce jour-là, si vous le
choisissez, le geste soit aussi propre que les six contacts déjà
publiés : écrit avant, gelé, testé, sans surprise.

## Confrontation à la question de l'étalonnage (2026-09-13)

La synthèse du 2026-09-12 laissait ouverte la vraie question du
tiroir macro : **θ d'un contact de désaccord doit-il être arbitraire
(H0 : 5 % abs gelé) ou naturel (AMU : θ = u_delta) ?** La doctrine
provisoire répondait : « justifié par la nature de l'objet ». La
confrontation de la paire à cette question y ajoute trois points qui
doivent être écrits avant le jour J.

### 1. L'étalonnage fait partie du contact, pas du seuil

Changer d'étalonnage, ce n'est pas changer le seuil d'un même
contact — c'est changer de contact. Test de cohérence : H0 au θ
naturel (θ = u ≈ 0,5-1 %) donnerait δ = 8,4 % > 2θ, donc **S−**, là
où le θ arbitraire gelé donne **P**. Même objet, deux étalonnages,
deux mots opposés. Corollaire, cohérent avec la doctrine CKM (home
GUM vs balayage θ : deux instruments, deux mots figés séparément) :
un contact n'a jamais qu'un seul étalonnage, et celui-ci est gelé
avant le run, au même titre que la règle.

### 2. La corrélation calibre/objet du θ naturel

Pour AMU, θ = u_delta partage une source avec l'écart pesé :
u_delta² = u_exp² + u_SM². Ce n'est pas un cercle vicieux (le test
figé verrouille la robustesse k = 1, 2, 3), mais c'est une corrélation
structurelle entre le calibre et l'objet — exactement le genre de
dette que la machine déclare plutôt que cache. Elle est neutralisée
par le gel vintage : θ est gelé à la valeur déclarée de la table
(LITERATURE-2018), jamais liée au vivant — si une collaboration
révise son u_delta, le contact gelé ne bouge pas ; c'est un *nouveau*
contact qui devra être monté.

### 3. La comparabilité de la paire repose sur l'identité d'étalonnage

Les deux mots de la paire (S+ à 0,6 U / S− à 3,7 U) ne sont
comparables que parce que les deux contacts partagent **le même
protocole au complet** : même objet, règle identique (écart porté vs
identité), même étalonnage (θ = u_delta, k = 1 gelé). Seule
l'identification hadronique change. Si les étalonnages différaient
(θ = 63 d'un côté, θ = 76 ou θ arbitraire de l'autre), la paire
serait invalide : on ne pourrait plus dire « le verdict est une
fonction de l'identification », puisque le verdict serait aussi une
fonction de l'étalonnage. C'est la condition de validité du geste —
elle doit être écrite dans la doctrine publiée, pas seulement ici.

**Conséquence pour le jour J** : publier la paire, c'est publier le
premier grand exemple *positif* de la doctrine de l'étalonnage :
θ naturel justifié par la nature de l'objet (écart normalisé dont
l'incertitude est déclarée), comparabilité assurée par l'identité
d'étalonnage, corrélation calibre/objet neutralisée par le gel
vintage. H0 reste le pendant arbitraire — les deux étalonnages
cohabiteront publiquement, et c'est la démonstration elle-même que
la machine sait tenir les deux dialectes sans les mélanger.
