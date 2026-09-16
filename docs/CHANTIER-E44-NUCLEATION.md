# Chantier E44 — nucléation de l'enlacement : pesée des déclarations

**Statut : local, non publié (2026-09-16).** Ouverture : la note d'audit
E44 (« Programme 2027 — nucléation spontanée de l'enlacement »,
31/07/2026, corpus histoire-des-sciences.eu) est un protocole
**pré-enregistré** : v1 figé et haché SHA-256 avant calcul
(42c65a0c…), amendement v2 (bc977f17…), publication quelle que soit
l'issue (B3-F AIL). C'est la grammaire exacte de la machine —
déclarations gelées datées, transport reproductible.

**Ce que la machine pèse, et ce qu'elle ne pèse pas.** Elle ne rejoue
pas la simulation Gross–Pitaevskii (64³, 2 ensembles × 6 graines) :
aucun code ni donnée brute dans la note. Elle pèse les **déclarations
gelées de la note et leur arithmétique interne** — comme PF7 a pesé
l'arithmétique du tableau publié, comme le corridor E a pesé des
tensions inter-campagnes.

## Population : 3 contacts

| Contact | μ_loc (gelé) | μ_ref | δ | δ/θ | Verdict | Attendu |
|---|---|---|---|---|---|---|
| E44_T0_LienHopf | 0,994 | 1 (attendu T0) | 0,6 % | 0,06 | **S+** | S+ tenu |
| E44_Lk_PaireHopf | 1,004 | 1 (lien unitaire) | 0,4 % | 0,04 | **S+** | S+ tenu |
| E44_P3_Filaments | 14 | 4 (prédiction 4 ± 2) | 250 % | 25 | **S−** | S− tenu |

- **T0 — le détecteur se valide** (S+ à 0,06 θ) : lien de Hopf contrôlé
  Lk = +0,994 déclaré (attendu ±1), témoin non lié Lk = +0,007 déclaré
  (attendu 0) — 0,6 % et 0,7 % d'écart déclarés, extra en runner.
- **L'événement central** (S+ à 0,04 θ) : la paire de Hopf du run
  A/440103 (t = 12), trois estimations indépendantes déclarées du nombre
  de Gauss : −1,041 (image minimale), −0,967 (brut), −1,004 (appariement
  alternatif). |moyenne| = 1,004 — écart 0,4 % du lien unitaire. Extra :
  spread 0,074, les trois estimations passent le seuil déclaré
  |Lk| ≥ 0,5 — la robustesse annoncée « à trois estimations » tient sur
  les nombres gelés ; distance minimale 3,16 mailles déclarée (pas de
  contact numérique).
- **P3 réfutée, pesée** (S− à 25 θ) : prédiction pré-enregistrée
  « filaments axiaux 4 ± 2 » vs médiane déclarée 14 (étendue 9–19) —
  écart 5 σ de la prédiction. La note statue « réfutée » elle-même, et
  la machine confirme le mot sur les nombres gelés. Cas rare où le
  corpus et la machine portent le même verdict sur la même déclaration.

## Ce qui reste non pesé (dettes nommées)

- **P1 / P2 / P2a / P4 / P5** : statuts booléens ou dénombrants (6/6,
  0/6, 1 paire sur 307 boucles, mode de multiplicité) — pesables
  seulement avec les données brutes des runs (absentes de la note) ;
  l'inégalité P5 (202 > 43) est triviale et n'apporterait rien.
- **La simulation elle-même** : code et jeux de données non fournis —
  la machine ne rejoue pas, elle cite (dette de reproductibilité de la
  note, pas de la machine).
- **Le verdict global « dérivé partiel fort »** : un mot du corpus, pas
  une grandeur.

## Curation et état du registre

Table gelée : `data/tables/e44_LITTERATURE-2026.json` (transcription
verbatim de la note, copie de travail `_tmp_e44/Note_Audit_E44_
Nucleation_Enllacement.pdf`). Module : `src/mvcg/e44.py`.

Registre : **101 contacts**, 17 fibres — (1, 1) {S+ 11, P 4, S− 22} ;
série O 21 → **23** (les deux S+ E44 rejoignent la population serrage) ;
détente 8 (inchangée, pas de P nouveau). Suite complète : **328 tests
OK** (4 skipped). Cartes régénérées (101 verdicts).
