# Corpus Principes Fondamentaux — bilan transversal (2026-09-15)

**Statut : local, non publié.** Clôture du chantier PRINCIPES
(PF1–PF8, volet par volet dans `CHANTIER-PRINCIPES-BILAN.md`,
`CHANTIER-PSY-RMN-BILAN.md`, `CHANTIER-HZ-F4-BILAN.md`). Ce document
est la lecture d'ensemble : que pèse exactement la machine quand le
matériau n'est plus un spectre ni une mesure, mais un *corpus
théorique auto-publié* avec ses équations, ses tableaux, ses jeux
numériques et ses revendications ?

## Le tableau d'ensemble

| Contact | Ce qui est pesé | Mot | θ | Type de dette |
|---|---|---|---|---|
| PF1 | dispersion 1-loop des 4 couplages vs unification à 1 % | S− 655,8 | 0,05 | revendication hors périmètre (l'article renvoie au 2-boucles) |
| PF2 | E = h·f du pic 25 THz, cohérence interne II × V | S+ 0,34 | 0,10 | — |
| PF3 | arithmétique du jeu τ₅ (10·e^(−0,023·22,67) vs ~6) | S+ 0,11 | 0,10 | — |
| PF4 | log₁₀(ρ_Planck/ρ_Λ) = 122,945 vs 122 | S+ 0,08 | 0,10 | — |
| PF5 | ħ_N image vs exemple-texte (facteur 10, même volet) | S− 9,0 | 0,10 | dette interne au corpus (image ≠ texte) |
| PF6 | ΔB RMN sous c_éth = 10⁹ c (4,19·10³² T vs 0,5 mT) | S− 8,4·10³⁵ | 0,10 | identification non tenable sous déclaration |
| PF7 | les 7 F = e^(−βS) recomputés vs publiés (δ_max 0,46 %) | S+ 0,046 | 0,10 | — |
| PF8 | écart H_filtree/H_LCDM vs borne « <2 % » déclarée | S− 33,1 | 0,10 | déclaration manquante (F_U non chiffré) |

**Bilan : 4 S+, 0 P, 4 S−. 8/8 attendus gelés tenus.** Aucun P : le
corpus ne laisse rien au cheveu — chaque contact tranche.

## Première lecture : trois poids, trois matières

Le corpus se répartit en **trois types de pesées**, et la machine les
distingue sans qu'on le lui demande :

1. **La cohérence interne (4 S+ : PF2, PF3, PF4, PF7).** La machine
   recompte ce que la source affirme et trouve les nombres d'accord
   avec eux-mêmes : le pic 25 THz converti en eV coïncide avec le seuil
   d'un autre volet ; le jeu τ₅ annoncé « ~6 » vaut 5,937 ; le vide se
   recompte à 122,945 contre 122 ; les sept plans satisfont F = e^(−βS)
   à 0,46 %. C'est le poids le plus doux : la machine certifie
   l'arithmétique, pas la physique. Remarque : ce sont des S+ très
   fins (0,046 à 0,34 θ), dans la classe des re-computes exacts du
   registre — Rydberg voie 2 (0,017 θ) et Dunham (0,028 θ) restent
   les S+ non triviaux les plus serrés, et PF7 (0,046 θ) les rejoint
   immédiatement. Peser des nombres qui coïncident, la machine le fait
   avec une précision que peu de contacts atteignent.

2. **La dette interne au corpus (2 S− : PF5, PF6).** Le corpus se
   contredit lui-même et la machine le nomme : l'équation-image pose
   ħ_N = 1,054·10⁻³⁴ J·s, l'exemple-texte du même volet n'est cohérent
   qu'avec 1,054·10⁻³³ (facteur 10, S− à 9 θ) ; la prédiction RMN
   affichée n'est pas recomputable sous l'identification déclarée
   c_éth = c_N (écart 36 ordres de grandeur, S− à 8,4·10³⁵ θ — le
   verdict le plus éloigné du registre entier). Ici la machine fait ce
   qu'aucun lecteur ne fait : tenir l'image et le texte dans la même
   balance.

3. **La tension revendication / équation (2 S− : PF1, PF8).** La source
   affirme une borne quantitative et publie une équation qui la dément
   : la dispersion 1-loop pure ne tient pas l'unification à 1 % (PF1,
   et l'article lui-même renvoie au 2-boucles — c'est une information,
   pas un accident) ; la borne « variation <2 % sur H(z) » est dépassée
   dès z = 0 sous l'équation publiée (16,6 %, puis 68,3 % — PF8). La
   machine pèse l'écart entre ce qui est *dit* et ce qui est *écrit*.

## Deuxième lecture : la typologie des dettes, enrichie

Avant ce corpus, la machine connaissait des dettes de *valeur* (un
nombre publié ne tient pas) et des dettes de *modèle* (une approximation
cache un terme). Le chantier PRINCIPES y ajoute **quatre dettes
nouvelles**, toutes nommées, jamais corrigées en silence :

- **dette de périmètre** (PF1) : la revendication appartient à un ordre
  de calcul que le texte cité n'atteint pas ;
- **dette d'incohérence image/texte** (PF5) : deux formulations du même
  volet se contredisent d'un facteur 10 ;
- **dette d'identification** (PF6) : une constante est posée égale à une
  autre sous laquelle l'affirmation centrale s'effondre ;
- **dette de déclaration manquante** (PF8) : un paramètre de l'équation
  (F_U) n'est chiffré nulle part ; la machine gèle une lecture neutre
  et nomme la normalisation non tenue.

Cette taxonomie est réutilisable : tout corpus auto-publié pourra être
balayé contre ces six types de dettes (les deux anciens + les quatre
nouveaux).

## Troisième lecture : ce que la machine a appris à peser

Le chantier a exigé un **acte curatorial nouveau** : les équations
n'étaient pas dans le texte, elles étaient dans des *images*. La machine
a transcrit 14 images d'équations (5 volet V : 29–33 ; 9 volets I/III :
61, 63, 90, 92, 93, 94, 95, 96, 97), gelé chaque transcription en table
datée avec sha256, puis pesé. C'est la troisième fois que ce mécanisme s'installe (PSY-RMN l'a
prouvé sur deux volets, H(z) F4 sur le cinquième), et il est désormais
une voie pérenne : tout matériau « non pesable car équations perdues en
images » devient pesable par transcription gelée. Le coût curatorial est
le prix de la traçabilité : chaque chiffre du run est rattaché à une
image, une table, un hachage.

Deuxième compétence : le champ `Contact.u_doc` (premier contact si +
grandeur électromagnétique) est né ici et a déjà été réutilisé par
PSY-RMN — la machine sait maintenant *où ranger* une équation transposée.

## Les limites, honnêtement posées

- **La machine ne juge pas la physique des plans, du filtrage F4 ni du
  graviton** : elle pèse des déclarations chiffrées entre elles. Les 4 S+
  disent « le corpus est arithmétiquement auto-cohérent », pas « le
  modèle est vrai ». La frontière est écrite dans chaque contact.
- **θ = 0,10 par défaut** sur 7 contacts sur 8 (seul PF1, une
  revendication à 1 %, porte θ = 0,05). Le θ est le seul levier
  discrétionnaire du protocole ; le chantier ne l'a pas fait varier.
  C'est la brique naturelle d'une campagne de serrage future.
- **Un 0 P sans complaisance** : aucun contact n'a été re-découpé pour
  tomber dans la zone d'indifférence. Le 0 P est une information sur le
  corpus (revendications franches) autant que sur la machine.

## Ce qui reste ouvert (prochaines briques)

1. **PF1b — le 2-boucles** : l'article renvoie lui-même au calcul
   2-boucles pour tenir l'unification ; c'est le contact le plus
   naturel du registre (il répond à un S− par le calcul que la source
   désigne).
2. **Serrage θ du corpus PF** : 7 contacts à θ = 0,10 — une campagne de
   recalibrage dirait où le vert se termine.
3. **Export de la taxonomie des dettes** : les six types pourraient
   devenir un vocabulaire contrôlé du registre (`docs/VERDICTS-FIBRES.md`
   et la carte).

## Traçabilité

Sources : 12 tables gelées `data/tables/pf*` (sha256 par
`load_table`). Verrous : `tests/test_principes.py` (8 μ figés),
`tests/test_verdicts_online.py` (fibres (si,1), (1,1), (si,eV), (si,J),
(si, T)). Bilans par chantier : `CHANTIER-PRINCIPES-BILAN.md`,
`CHANTIER-PSY-RMN-BILAN.md`, `CHANTIER-HZ-F4-BILAN.md`.
