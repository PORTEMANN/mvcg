# Note ingénieur — faire tourner MVC-G

Environnement : Python 3.11+, `numpy`.  
CI : `.github/workflows/tests.yml`.  
`opentimestamps` est optionnel (ancre calendrier). Sans lui, les tests OTS sont skippés.

```bash
cd mvcg               # ou le dossier dézippé
export PYTHONPATH=src
python3 -m unittest discover -s tests -q
# attendu : OK, quelques skipped si pas d'OTS
```

## Cinq minutes — peser les contacts livrés

```bash
python3 -m mvcg registers
python3 -m mvcg dictionaries
python3 -m mvcg corridor
```

`registers` tire H 1s, H₂⁺, H₂O, Kato, He, Dice, Friedmann.  
Les S− (LCAO, dipôle pauvre, cusp gaussien, HF vs corrélation) sont des **succès de protocole**.

## Répéter puis publier

```bash
python3 -m mvcg --root /tmp/mvcg-rep campaign
# écrit rehearsal.json — pas de hash

python3 -m mvcg --root /tmp/mvcg-pub campaign --publish --offline
# écrit *.bits.json, *.D.json, *.cost.json
```

`--publish` sans `dossier` interne n’existe plus pour la campagne catalogue : chaque ligne gèle `D` (`θ`, paquet, `μ_ref`, levier).

Gel manuel d’un dossier :

```bash
python3 - <<'PY'
from pathlib import Path
from mvcg.met_lib import MetLib15
from mvcg.tables import h2plus_de
from mvcg.h2plus import lcao_1s

t = h2plus_de()
sol = lcao_1s(2.0)
D = {
    "id": "P20_H2plus_LCAO",
    "s": "De LCAO R=2 = table LITERATURE-2018",
    "packet": "si", "dimension": "eV",
    "theta": 0.05, "sigma": 0.01,
    "mu_ref": t["value"], "lever": "ansatz←table",
    "delta_kind": "rel", "register": "micro", "orig": "pred",
    "table": "h2plus_De_LITERATURE-2018.json",
}
lib = MetLib15(Path("/tmp/p20"), offline_ots=True)
lib.freeze("P20_H2plus_LCAO", phys=1, orig="pred", kappa_hat="equilibre", dossier=D)
lib.freeze_units("P20_H2plus_LCAO", {"packet": "si", "vintage": "LITERATURE-2018"})
lib.record_metric("P20_H2plus_LCAO", sol["De_eV"], t["value"], 0.05, "eV", "rel")
lib.measure("P20_H2plus_LCAO", 2)   # 2 = S−
print(lib.audit_g1("P20_H2plus_LCAO"))
print(lib.audit_g2("P20_H2plus_LCAO"))
PY
```

## Ajouter *votre* contact

1. Poser une table dans `data/tables/` (JSON, `vintage`, `value`, `source`). Pas de fetch.  
2. Un runner qui rend `(mu_loc, extra)` — calcul ou lecture, mais pas la cible recopiée sauf contrôle tautologique.  
3. Une ligne `Contact(...)` dans `src/mvcg/registers.py` (ou un protocole `data/protocols/*.json`).  
4. Un levier écrit : que changer pour que le mot bascule.  
5. Un test qui fixe le mot attendu (y compris S−).

Schéma minimal de `D` : `id, s, packet, dimension, theta, mu_ref, lever, delta_kind`.

## Dictionnaires

`packet` ∈ {`hl`, `gauss`, `si`, `1`}.  
`si` + grandeur EM (`e*g`, …) exige `ε0, μ0`.  
`si` + `ε0=1` sur un `e*g` est refusé (usurpation HL).

```bash
python3 -m mvcg dictionaries
```

## Ce que vous pouvez ignorer au début

- OpenTimestamps / Bitcoin (`--offline`).  
- Dynamique spectrale 2D/3D, padding 3/2 (jouets de stabilité numérique).  
- ASH / C5 (instrument, pas un préfiltre).  
- Groupoïde de ponts : utile seulement si vous convertissez des unités.

## Contrat court

- Après `measure`, plus de patch des bits (I-G2).  
- `measured_at` ≥ `frozen_at` (I-G1).  
- `θ` et `U` doivent être dans `D.json` si vous publiez un mot scientifique.  
- Un S+ n’est vrai que pour le `packet` de sa ligne.

Portes physicien / chimiste / cosmologue / neurologue : `docs/PORTES-METIERS.md`.

## Archive

Les campagnes historiques P0–P48 vivent dans un dépôt séparé de l’auteur,
sans lien depuis ce dépôt. Ce dépôt ne les télécharge pas.
