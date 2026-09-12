# MVC-G

[![tests](https://github.com/PORTEMANN/mvcg/actions/workflows/tests.yml/badge.svg)](https://github.com/PORTEMANN/mvcg/actions/workflows/tests.yml)
[![sanity](https://github.com/PORTEMANN/mvcg/actions/workflows/sanity.yml/badge.svg)](https://github.com/PORTEMANN/mvcg/actions/workflows/sanity.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

Machine de verdict à coût gelé.

Si le dépôt GitHub n’est pas `PORTEMANN/mvcg`, remplacer l’OWNER/REPO dans les badges.

**Commencer ici**

- Tiers, une page : [`docs/VULGARISATION.md`](docs/VULGARISATION.md)
- Faire tourner : [`docs/NOTE-INGENIEUR.md`](docs/NOTE-INGENIEUR.md)
- Quatre métiers : [`docs/PORTES-METIERS.md`](docs/PORTES-METIERS.md)
- Lecteur académique : [`docs/NOTE-DIFFERENCIATION.md`](docs/NOTE-DIFFERENCIATION.md)
- AI Act / normes (piste, pas notification) : [`docs/AI-ACT.md`](docs/AI-ACT.md)
- Capot discret ↔ continu : [`docs/DISCRET-CONTINU.md`](docs/DISCRET-CONTINU.md)
- Justesse des pesées : [`docs/JUSTESSE.md`](docs/JUSTESSE.md)
- Incertitude / métrologie quantique : [`docs/METROLOGIE-QUANTIQUE.md`](docs/METROLOGIE-QUANTIQUE.md)

## Contacts ouverts (série O1 → O16)

Seize pesées dont le mot est **découvert après le gel du protocole** — θ
figé, table vintage, anti-tautologie, levier directionnel — jamais
choisi. Rejouer : `PYTHONPATH=src python3 -m mvcg registers`.

| Contact | Règle déclarée | θ gelé | Mot | δ |
|---|---|---|---|---|
| O1 | E_1s(H), différences finies n=200 | 1e−3 | S− | 3,8e−3 |
| O2 | ν₃(CO₂), constante de force transférée du CO | 0,10 | P | 14,5 % |
| O3 | bande D graphite, chaîne 1D k₂ = k₁ | 0,10 | P | 17,2 % |
| O4 | I_D/I_G, loi Tuinstra–Koenig C/L_a | 0,10 | S− | 22,2 % |
| O5 | c(son) condensat ⁸⁷Rb, Bogolioubov | 0,05 | P | 6,2 % |
| O6 | E_1s(H), grille raffinée n=1600, θ inchangé | 1e−3 | **S+** | 6,1e−5 |
| O7 | bande D, levier k₂/k₁ = 3 activé, θ inchangé | 0,10 | **S+** | 1,4 % |
| O8 | T_c gaz de Bose idéal | 0,10 | **S+** | 5,0 % |
| O9 | μ(H₂O) par électronégativités Pauling | 0,10 | S− | 67,4 % |
| O10 | ν(C=O PMMA), transfert de force (étalon) | 0,10 | **S+** | 0,6 % |
| O11 | ξ longueur de guérison du condensat | 0,10 | **S+** | 9,0 % |
| O12 | γ(Cu), Sommerfeld masse libre | 0,10 | S− | 26,8 % |
| O13 | ν₃(¹³CO₂), loi des masses depuis ν₃(¹²CO₂) | 0,10 | **S+** | 1,0 % |
| O14 | I_D/I_G charbon graphitisé, TK dans sa fenêtre | 0,10 | **S+** | 2,2 % |
| O15 | ω_e(H₂), oscillateur harmonique k = 510 N/m | 0,10 | **S+** | 5,8 % |
| O16 | γ(Cu), levier d'O12 activé (m\* = 1,38 m_e déclarée) | 0,10 | **S+** | 1,0 % |

La paire O1 → O6 est la démonstration : même objet, même référence,
même θ, seul le levier écrit au moment de l'échec a bougé. O3 → O7
généralise le geste à un paramètre effectif phénoménologique. La
paire O4 → O14 pèse une même loi des deux côtés de sa frontière
(S− à 3 nm, S+ à 10 nm) : le verdict est une mesure locale dans le
plan des paramètres. O13 sépare table et règle (la référence est
portée, jamais lue) ; O15 protocolise l'honnêteté de la comparaison
(référence choisie avant le run, quand le mot est encore inconnu) ;
la paire O12 → O16 active le levier d'O12 (masse effective déclarée,
jamais dérivée de la référence) — la démonstration « chaque échec a
son levier » passe de la grille (O1→O6) au paramètre phénoménologique
(O3→O7) au paramètre de théorie effective. Chaque
doctrine : [`docs/O1-CONTACT-OUVERT.md`](docs/O1-CONTACT-OUVERT.md) …
[`docs/O16-CONTACT-OUVERT.md`](docs/O16-CONTACT-OUVERT.md). Artefacts
gelés et audit rejouable : `examples/registre/O{1..16}.{bits,units,metric,cost}.json`.
Classement par fibre (packet, dimension) et invariance sous balayage :
[`docs/VERDICTS-FIBRES.md`](docs/VERDICTS-FIBRES.md).

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

Le corpus historique (P0–P48, série A, corridor E, SHA) vit dans
[`PORTEMANN/noetic-machine-complete`](https://github.com/PORTEMANN/noetic-machine-complete).
Ce zip **ne l’importe pas** à l’exécution. Un protocole local
(`data/protocols/`) peut *citer* un chantier P ; il ne télécharge rien.

Banc SU(2) : [`PORTEMANN/noetic-machine`](https://github.com/PORTEMANN/noetic-machine).

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
| `examples/registre/O{1..6}.*` | contacts ouverts gelés offline, audit [HOLD] I-G1 / I-G2 |
| `tests/` | G1/G2 offline, OTS live, upgrade pending, contacts ouverts O1–O6 |

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

# trois registres (micro / meso / macro) + contacts ouverts O1–O6 :
python3 -m mvcg registers

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

Un contact **ouvert** ajoute la discipline du gel *avant* le premier
run : la machine risque un mot (S+, P ou S−) au lieu de le choisir —
voir la série O1 → O16 ci-dessus. Ajouter le sien = sa molécule, sa
table, son θ gelé : c'est le seul signal d'appropriation.

## Hors périmètre

Pas de modèle unifié, pas d’analyseur « noétique », pas d’API industrielle.
Un chantier phénoménologique n’entre ici que comme satellite, puis éventuellement
comme script de verdict avec une référence de littérature et des bits gelés
*a priori*.

## Licence

MIT. Voir `LICENSE`.
