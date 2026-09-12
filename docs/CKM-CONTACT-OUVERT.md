# CKM — contact ouvert : l'unitarité de la première ligne

Contact **ouvert** (mot découvert, pas choisi) — exploration locale,
non publiée. Premier contact de **physique des particules** : la somme
|V_ud|² + |V_us|² + |V_ub|² de la première ligne de la matrice CKM
contre l'identité du modèle à trois générations.

## Chronologie du gel

1. **Protocole écrit avant toute exécution** : règle déclarée — la
   première ligne est unitaire **de par la définition du modèle** ;
   μ_loc = somme déclarée de la table (`ckm_row1_LITERATURE.json`,
   extrait PDG déclaré, **pas un fetch pdgLive**), μ_ref = 1,0 —
   l'identité du modèle, jamais ajustée pour absorber un déficit.
   θ = 0,0007 abs (la u déclarée de la somme), GUM : decide=U, k=2,
   une seule ligne B (u = 0,0007) → U = 0,0014 ; le contact porte
   θ = 0,0007. Levier déclaré : somme ← autres entrées (V_us d'autres
   désintégrations) — jamais θ, jamais l'identité. Estimation pré-run
   honnête : δ = 0,0016, soit U < δ ≤ 2U — P attendu **au cheveu du
   S+** (δ/U = 1,14) : suspense réel.
2. **Premier run** : mot découvert : **P**, δ = 0,0016, U = 0,0014.
   Artefacts gelés offline (audits [HOLD] I-G1 / I-G2) :
   `examples/registre/CKM.*`.
3. **Figé** : mot dans `tests/test_open_ckm.py`.

## Le mot : P — au cheveu du S+

Avec δ/U = 1,14, le mot est tenu d'un cheveu : une réanalyse qui
déplacerait la somme d'environ 0,0003 (une révision de V_us au-delà
de sa u déclarée, exactement ce que le levier annonce) ferait basculer
le mot vers le S+. Le test fige le suspense : ratio borné dans
]1,0 ; 1,3[ et seuil decide=U, k=2 inchangé. Le P n'est pas un
confort : c'est un **cheveu sous tension**, et le registre le dit.

## Anti-tautologie — deux instruments, deux mots figés

Le geste interdit serait de déplacer μ_ref de 1,0 (ou de gonfler u)
pour absorber le déficit d'unitarité — transformer l'identité du
modèle en paramètre d'ajustement. Le test verrouille : μ_ref = 1,0
exact, u = 0,0007 exacte, U recombinée depuis la ligne B déclarée.

Premier cas où les deux instruments de la machine ne coïncident pas :
le mot home (GUM, decide=U, k=2) est **P**, le mot balayage (θ seul)
est **S−** partout — δ = 0,0016 dépasse 2θ = 0,0014 sans dépasser
2U = 0,0028. Ce n'est pas une contradiction : le balayage et le home
mesurent deux choses différentes, et le test fige les deux, séparément.
La doctrine qu'on en tire : l'invariance home/balayage n'est pas un
axiome, c'est une propriété qu'on vérifie — et qu'on documente quand
elle fait défaut.

## Pourquoi ce contact compte

Il prouve que la discipline du contact ouvert tient sur l'objet le
plus étalonné de la physique des particules : l'unitarité CKM, check
standard du modèle, devient ici un objet pesé avec son incertitude
déclarée — et le verdict n'est pas le confortable « tout va bien »,
mais un P au cheveu, avec un levier explicite. Le tiroir micro gagne
sa première carte de particules, en dehors de la série O et sans
ouvrir le tiroir macro.
