# NMR — contact ouvert : la loi de Karplus devient une carte

Contacts **ouverts** (mots découverts, pas choisis) — exploration locale,
non publiée. Une seule loi, deux conformations : la paire
**NMR_Karplus_Helix** (S+) / **NMR_Karplus_Sheet** (P). Avec elle, la loi
cesse d'être une formule et devient une **carte** : mêmes coefficients
gelés, deux points de la conformation, deux mots différents.

## Chronologie du gel

1. **Protocole écrit avant toute exécution** : règle déclarée —
   ³J(HN,Hα) = A cos²(φ − 60°) + B cos(φ − 60°) + C avec A = 6,51,
   B = −1,76, C = 1,60 Hz (table `karplus_peptide_LITERATURE.json`,
   vintage littérature déclaré). μ_loc = J calculé à φ_helix = −60°
   (resp. φ_sheet = −120°), μ_ref = ordre de grandeur typique déclaré
   de la littérature : 4,0 Hz (hélice) resp. 8,5 Hz (brin). θ = 0,10
   rel, gelé avant run. La référence est **explicitement « pas un PDB »**
   : un ordre de grandeur de la littérature, pas une structure résolue
   assignée au couplé — la dette est déclarée au lieu d'être cachée.
   Levier déclaré : coefficients ← autre paramétrisation (jamais φ,
   jamais la référence). Estimation pré-run honnête : hélice ~3 %
   (S+ attendu), brin ~16 % — zone P [θ, 2θ], avec un suspense réel
   au bord de la zone S− (20 %).
2. **Premiers runs** : mots découverts : **S+** (hélice, δ = 2,69 %)
   et **P** (brin, δ = 16,1 %). La paire tient l'estimation — y compris
   le suspense du brin, à 16,1 % contre une zone S− qui commence à 20 %.
   Artefacts gelés offline (audits [HOLD] I-G1 / I-G2) :
   `examples/registre/KARPLUS_H.*`, `examples/registre/KARPLUS_S.*`.
3. **Figé** : mots dans `tests/test_open_nmr.py`.

## Le mot : S+ et P — et ce que la paire dit

Le S+ de l'hélice dit : la loi, avec ses coefficients gelés, retombe
sur l'ordre de grandeur typique à 2,7 % près — bien à l'intérieur du
seuil. Le P du brin dit autre chose, plus intéressant : **la même loi,
sur sa deuxième conformation, rate l'ordre de grandeur typique de
16 %** — un écart à la fois trop grand pour le S+ et trop petit pour
le S−. Ce n'est ni une confirmation ni une réfutation : c'est une
**dette localisée**, exactement du calibre qu'un contact ouvert existe
pour porter.

## Anti-tautologie

Le geste interdit serait de faire glisser A, B ou C jusqu'à ce que le
brin tombe dans le S+. Le test verrouille : les coefficients gelés dans
la table sont ceux de la littérature, la loi est une **carte avec les
mêmes coefficients** sur les deux conformations, et aucun ajustement
n'est permis après coup. La carte ne ment pas : elle montre un point
conforme et un point débiteur, avec la même encre.

## Pourquoi ce contact compte

C'est le premier contact où l'objet pesé est une **loi** et non une
constante ou un spectre. La machine y gagne un mode : la paire de
conformations est le pendant conformationnel de la paire de fibres —
même objet, deux affichages, deux mots. Le casier y gagne la famille
NMR déjà esquissée par Knight et δ_ppm (toujours « sans μ ») : le
tiroir NMR a désormais ses deux premières cartes pesées.
