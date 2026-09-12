# MVC-G

[![tests](https://github.com/PORTEMANN/mvcg/actions/workflows/tests.yml/badge.svg)](https://github.com/PORTEMANN/mvcg/actions/workflows/tests.yml)
[![sanity](https://github.com/PORTEMANN/mvcg/actions/workflows/sanity.yml/badge.svg)](https://github.com/PORTEMANN/mvcg/actions/workflows/sanity.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

Machine de verdict à coût gelé.

Si le dépôt GitHub n’est pas `PORTEMANN/mvcg`, remplacer l’OWNER/REPO dans les badges.

**Commencer ici**

- Deux pesées en 10 minutes : [`docs/QUICKSTART.md`](docs/QUICKSTART.md)
- Tiers, une page : [`docs/VULGARISATION.md`](docs/VULGARISATION.md)
- Faire tourner : [`docs/NOTE-INGENIEUR.md`](docs/NOTE-INGENIEUR.md)
- Quatre métiers : [`docs/PORTES-METIERS.md`](docs/PORTES-METIERS.md)
- Lecteur académique : [`docs/NOTE-DIFFERENCIATION.md`](docs/NOTE-DIFFERENCIATION.md)
- AI Act / normes (piste, pas notification) : [`docs/AI-ACT.md`](docs/AI-ACT.md)

Ce dépôt n’est pas une théorie du tout. Ce n’est pas un champ de conscience.
C’est un **opérateur** et un **protocole de registre**.

```
(D, S, L)  --Mhat-->  V
F, bits gelés  --M2-->  d
sigma(bits)    --OTS-->  calendrier, puis bloc Bitcoin quand disponible
```

## Nature conservée / nature abandonnée

Conservée : éprouver une structure sur des données figées, sans paramètre
ajusté après coup ; publier le succès et l’échec dans le même schéma ;
facturer la fermeture ; interdire de reclasseer l’étiquette une fois \(d\) lu.

Abandonnée : vide hydrodynamique, échelle musicale ontologique, \(E_8\),
viscosité comme conscience, réacteur, unification gravité–quantique–fluide.
Ces objets, s’ils existent quelque part, sont des *satellites*. Ils n’entrent
pas dans le graphe d’appel.

La machine expurgée **garde sa nature d’opérateur de verdict**.
Elle **perd la nature d’ontologie**. Confondre les deux était le défaut
de l’ancienne mouture.

## Archive, pas dépendance

Un corpus historique de l’auteur (chantiers P0–P48, séries A/M/E) vit dans
un dépôt séparé. Ce dépôt **ne l’importe pas** à l’exécution et ne pointe
pas vers lui : aucun badge, aucune dépendance, aucun lien automatique.
Un protocole local (`data/protocols/`) peut *citer* un chantier P ;
il ne télécharge rien.

`--publish` écrit `*.D.json` et en scelle le SHA dans G1. Sans dossier,
le gel scientifique est incomplet.

## Contenu

| Chemin | Rôle |
|---|---|
| `src/mvcg/met_lib.py` | MÉT-LIB-1.5 — gel, tueurs I-G1 / I-G2 |
| `src/mvcg/ots_anchor.py` | ancre OpenTimestamps + upgrade + vérif Blockstream |
| `src/mvcg/rationalization.py` | paquets HL / Gauss / SI, Dirac, flux |
| `src/mvcg/metrics.py` | métrique \((\mu_{\mathrm{loc}},\mu_{\mathrm{ref}},\delta,\theta,U)\) |
| `src/mvcg/ash_instrument.py` | C5 instrument (pas un tuyau) |
| `src/mvcg/dynamics.py` | EDP candidate forme MDU (pas un préfiltre) |
| `docs/C5-ET-DYNAMIQUE.md` | contrat C5 / dynamique |
| `docs/SPEC-architecture.pdf` | note d’ingénierie (interfaces, cœur à 5 scripts) |
| `docs/METRIQUES.md` | contrat de la métrique de contact |
| `docs/RATIONALISATION.md` | dictionnaire des champs |
| `docs/INVARIANTS.md` | rappel court I-V … I-C |
| `docs/INVARIANTS-MATH.md` | énoncés mathématiques, domaines, tueurs |
| `docs/CONTACTS-PHENOMENOLOGIQUES.md` | physique, chimie, ingénierie, biologie — contacts encore admissibles |
| `examples/registre/F22.*` | gel réel + preuve OTS pending |
| `tests/` | G1/G2 offline, OTS live, upgrade pending |

## Installer

```bash
python3 -m pip install opentimestamps
export PYTHONPATH=src
```

`opentimestamps` sert uniquement à sérialiser les preuves calendrier.
Le reste est la bibliothèque standard.

## Usage

```bash
export PYTHONPATH=src

python3 -m mvcg --root registre freeze --id F1 --phys 1 --orig pred --kappa deficit
python3 -m mvcg --root registre units --id F1 --packet hl --vintage convention
python3 -m mvcg --root registre metric --id F1 --mu-loc 6.283185307179586 --mu-ref 6.283185307179586 --theta 1e-12 --dimension 'e*g'
python3 -m mvcg --root registre measure --id F1 --d 1
python3 -m mvcg --root registre audit --id F1
python3 -m mvcg --root registre patch --id F1 --orig thm    # doit refuser
python3 -m mvcg --root registre upgrade-btc --id F1         # 3 = encore pending
```

`--offline` désactive l’ancre OTS (tests locaux).

`--d inf` et `--d empty` codent \(d=\infty\) et \(d=\varnothing\).
\(\varnothing\neq 0\).

## Tests

CI : `.github/workflows/tests.yml` (Python 3.11 et 3.12, `numpy`).  
OTS est un job à part ; sans la lib les tests concernés sont skippés.

```bash
PYTHONPATH=src python3 -m unittest discover -s tests -q
PYTHONPATH=src python3 tests/test_g1_g2.py
PYTHONPATH=src python3 tests/test_metrics_units.py
PYTHONPATH=src python3 tests/test_c5_dynamics.py
PYTHONPATH=src python3 tests/test_ots_anchor.py      # réseau
PYTHONPATH=src python3 tests/test_upgrade_btc.py     # réseau
```

## Contrat de gel

1. Les bits `phys`, `orig`, `kappa_hat` sont hachés **avant** \(d\).
2. \(\sigma(\beta)\) est une *entrée* de l’objet coût.
3. Après \(d\), les bits sont immutables. Seul `void` retire \(F\).
4. Sans `--offline`, `freeze` tamponne \(\sigma(\beta)\) chez Alice / Bob / Finney.
   L’horloge externe est la `Date` HTTP du calendrier.
5. L’attestation de bloc Bitcoin est un *upgrade*. Tant que les calendriers
   répondent 404, le statut reste `pending`. Ce n’est pas un HOLD on-chain.

## Contacts phénoménologiques

Solveurs livrés (maquettes) : LCAO H₂⁺ (`h2plus.py`), cusp Kato 1s, tables
`data/tables/*LITERATURE-2018.json`. Le dossier
`docs/CONTACTS-PHENOMENOLOGIQUES.md` liste ce qui *peut* encore entrer
comme contact. Un contact sans table vintage n’est pas un contact.

## Hors périmètre

Pas de modèle unifié, pas d’analyseur « noétique », pas d’API industrielle.
Un chantier phénoménologique n’entre ici que comme satellite, puis éventuellement
comme script de verdict avec une référence de littérature et des bits gelés
*a priori*.

## Licence

MIT. Voir `LICENSE`.
