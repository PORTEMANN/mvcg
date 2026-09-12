# Contacts phénoménologiques admissibles

MVC-G ne produit pas de physique, de chimie, d’ingénierie ou de biologie.
Elle peut **interroger** un dossier de ces domaines si, et seulement si,
le dossier entre comme \((D,S,L)\) avec métrique externe.

Un contact n’est pas une unification. C’est une ligne du tableau
« nôtre / référence / écart ».

## Règle d’admission (tous domaines)

1. \(D\) public, versionné, SHA dans l’objet de verdict.
2. \(S\) sans élément de \(\mathrm{Free}(S)\) (I-V2).
3. Un levier \(L\) dont l’ablation fait chuter le score (I-V3).
4. Une référence que le domaine reconnaît déjà (I-V6).
5. Bits MÉT-LIB gelés *avant* \(d\) (I-G1).
6. Aucun mot satellite dans l’API (I-C4, I-A5).

Si une ligne du tableau « référence » est vide, ce n’est pas un contact.
C’est un récit.

## Physique

### Encore admissibles comme C1 / C2

| Contact | \(D\) typique | Référence | Ce qui est permis | Ce qui est interdit |
|---|---|---|---|---|
| Borne BPS / masse de monopole | constantes de jauge, \(\rho\), unités | littérature Georgi–Glashow / BPS | recalculer \(C(\rho)\) et l’écart | en faire une hydrodynamique du vide |
| Quantification de Dirac | \(e,g\) ou flux | \(eg=2\pi n\) | vérifier l’identité sur le banc | la vendre comme prédiction d’équilibre sans `orig=pred` gelé |
| Spectre coulombien de test | potentiel fixé dans \(D\) | Bohr / LRL, niveaux tabulés | erreur relative par niveau | « atome noétique » |
| Diagramme de phases d’un modèle nommé | \((g,v,\rho)\) figés | paper du modèle, pas un score interne | frontière \(\rho^{*}\) vs référence | pont vers \(E_8\) |
| Défaut topologique (tube, anneau) | ansatz + constantes | flux \(\Phi=4\pi n\), énergie de tension | coexistence comme verdict de structure | confinement « émergent du Koïlon » |
| Noyau : énergies de liaison | **AME complet**, pas un sous-échantillon | AME / SEMF publié | RMS sur tout le fichier | \(Z_{\max}=180\), \(120\leftrightarrow E_8\) |
| Matière condensée : gap / invariant \(\mathbb{Z}_2\) | structure de bande publiée | calcul DFT / modèle de Kane–Mele nommé | accord / désaccord chiffré | ASH comme preuve topologique |

### Non contacts (satellites)

Équation maîtresse fluide + torsion + mémoire fractionnaire comme gravité.
Ponts de racines exceptionnelles. Toute « prédiction exacte à zéro paramètre »
dont le zéro n’est pas un théorème listé dans `CONVENTIONS.md`.

## Chimie

### Encore admissibles

| Contact | \(D\) | Référence | Permis | Interdit |
|---|---|---|---|---|
| Énergies de molécules petites | géométries + jeu standard (G2/Pople, W4, NIST CCCBDB) | valeurs tabulées, même unité | un opérateur radial *déclaré*, RMS | « un potentiel pour toute la chimie » sans jeu nommé |
| Spectres vibrationnels | fréquences expérimentales figées | NIST / SDBS | écart cm⁻¹ | grille à 12 demi-tons comme ontologie moléculaire |
| Réactivité qualitative | barrière publiée pour *une* réaction | article source | tenir / rater la barrière | table périodique « bifurquée » par \(E_8\) |

La chimie entre comme table de nombres. Pas comme tableau de Mendeleïev
réinterprété.

## Ingénierie

### Encore admissibles

| Contact | \(D\) | Référence | Permis | Interdit |
|---|---|---|---|---|
| Signal mécanique / roulement | CWRU, Paderborn, ou fichier industriel versionné | F1 / AUC d’une baseline STFT-SVM ou équivalent | analyseur \(O(1)\) vs baseline, latence, stabilité au gain | « pression du vide » comme feature |
| Vibration / acoustique | même fenêtre pour les deux côtés | spectrogramme, CWT | \(\Delta\) de score et de temps | grille musicale comme loi |
| Diagnostic embarqué | trace + budget CPU/RAM | même métrique hors carte | invariant portable après renormalisation d’amplitude | firmware « noétique » |
| Conformité / preuve exécutable | artefact + protocole nommé | exigence d’un référentiel *externe* (pas un DCC inventé ici) | SHA + `Kill` + void | habiller une clause AI Act avec un fluide |

L’ingénierie est le contact le plus naturel de MVC-G : elle parle déjà
en protocoles, en traces, en non-régression. Encore faut-il une baseline.

## Biologie et signal du vivant

### Encore admissibles, étroitement

| Contact | \(D\) | Référence | Permis | Interdit |
|---|---|---|---|---|
| ECG | MIT-BIH ou équivalent versionné | détecteur publié (Pan–Tompkins, réseau nommé) | F1 / sensibilité sur le split figé | rythme comme « torsion » |
| EEG tâche motrice | BCI Competition IV-2a ou jeu nommé | EEGNet / CSP publié, même split | accuracy vs baseline | règles « zéro paramètre » seules, conscience |
| Spike / calcium | jeu public avec protocole d’acquisition | métrique de la paper source | tenir / rater la métrique | neurone = signature d’intention |
| Séquence / structure | FASTA + PDB figés | BLAST / RMSD / TM-score selon la tâche | un \(S\) sans fit après \(D\) | lecture symbolique du vivant |

La biologie n’entre pas par une analogie fluide–tissu. Elle entre par un
fichier et une métrique que *ce* sous-domaine utilise déjà. Tout vocabulaire
de conscience, d’intention ou de « champ » est un satellite, pas un contact.

## Ce qui n’est un contact dans aucun domaine

- Un score \(k/k\) interne.
- Un succès dont le levier n’a pas été ablaté.
- Un équilibre \(d=0\) déclaré `pred` après avoir vu le chiffre.
- Une famille combinatoire (parité, tri, tentes) présentée comme épreuve
  de physique.
- Un pont analogique (viscosité ↔ mémoire, pression ↔ gravité, octave ↔
  spectre atomique).

## Comment un contact entre dans le cœur

Ordre obligatoire :

1. Écrire l’énoncé \((D,S,L,\mu_{\mathrm{ref}})\) et geler les bits.
2. Tamponner \(\sigma(\beta)\) (OTS, sauf `--offline`).
3. Exécuter, publier \(V\) et \(d\).
4. Remplir la ligne nôtre / référence / écart.
5. Ne monter dans le cœur (≤ 5 scripts) qu’après un replay hors auteur.

Tant que l’étape 4 est vide, le dossier reste un satellite même s’il compile.

## Inventaire v0.1

Dans *ce* dépôt : **aucun** contact phénoménologique exécuté.
F22 est un contact de *protocole* (gel + OTS), pas de physique.

Les bancs historiques du corpus d’origine (jauge, AME partiel, « 32 tests »)
ne sont pas repris. Ils peuvent être recâblés plus tard, un par un, sous
les règles ci-dessus. Recâbler n’est pas valider.
