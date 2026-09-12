# Quickstart — deux pesées en 10 minutes (+ une sous le capot)

Prérequis : Python 3.11+, `numpy`. Aucune autre dépendance (l'ancre
OpenTimestamps est optionnelle ; ici `--offline`).

Les exemples 1 et 2 sont le cœur : 10 minutes, un S+ et un S−.
L'exemple 3 (5 min de plus, optionnel) ouvre le capot : tare, chaîne
typée, calibre.

```bash
cd mvcg                      # dossier dézippé ou cloné
export PYTHONPATH=src        # Windows (cmd) : set PYTHONPATH=src
mkdir -p /tmp/mvcg-quick     # n'importe quel dossier de travail
```

Chaque pesée suit le même cycle : **geler les bits → geler les unités →
peser → mesurer le coût → auditer**. Le gel passe *avant* le chiffre :
c'est tout le protocole (I-G1, I-G2).

## Exemple 1 — Dirac : `e·g = 2π` en Heaviside–Lorentz (5 min)

La quantification de Dirac dit `e·g = 2π n` en paquet HL (`n = 1` ici).
On déclare le dictionnaire d'unités *avant* de peser, avec un seuil
`θ = 10⁻¹²` gelé.

```bash
python3 -m mvcg --offline --root /tmp/mvcg-quick freeze --id F30 --phys 1 --orig thm --kappa equilibre
python3 -m mvcg --offline --root /tmp/mvcg-quick units --id F30 --packet hl --vintage convention
python3 -m mvcg --offline --root /tmp/mvcg-quick metric --id F30 \
  --mu-loc 6.283185307179586 --mu-ref 6.283185307179586 \
  --theta 1e-12 --dimension 'e*g' --kind rel
python3 -m mvcg --offline --root /tmp/mvcg-quick measure --id F30 --d 0
python3 -m mvcg --offline --root /tmp/mvcg-quick audit --id F30
```

Attendu :

- `metric` → `"verdict": "S+"` (δ = 0 ≤ θ) ;
- `measure` → `d_reg = 0`, `b_mesuree = 1` ;
- `audit` → deux lignes `[HOLD]` : I-G1 (σ(bits) ∈ inputs(d), horloge
  cohérente) et I-G2 (bits intacts depuis le gel).

Ce qui est prouvé : l'identité est pesée *dans un dictionnaire déclaré*,
sous un seuil gelé, avec les bits scellés avant le chiffre. En paquet
Gauss la même physique s'écrirait `e·g = 1/2` — un S+ Gauss et un S+ HL
ne se mélangent jamais : le paquet fait partie de l'objet gelé. Essayez
de re-geler `units` avec `--packet gauss` sur F30 : le gel est déjà posé,
c'est refusé.

## Exemple 2 — H₂⁺ : un LCAO trop pauvre, pesé honnêtement (5 min)

Un calcul LCAO minimal (`R = 2`, base 1s) rend une énergie de
dissociation ; la table vintage de littérature (`data/tables/
h2plus_De_LITERATURE-2018.json`) rend la cible. Le seuil gelé est
`θ = 0,05` relatif.

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
    "mu_ref": t["value"], "lever": "ansatz<-table",
    "delta_kind": "rel", "register": "micro", "orig": "pred",
    "table": "h2plus_De_LITERATURE-2018.json",
}
lib = MetLib15(Path("/tmp/mvcg-quick"), offline_ots=True)
lib.freeze("P20_H2plus_LCAO", phys=1, orig="pred", kappa_hat="equilibre", dossier=D)
lib.freeze_units("P20_H2plus_LCAO", {"packet": "si", "vintage": "LITERATURE-2018"})
m = lib.record_metric("P20_H2plus_LCAO", sol["De_eV"], t["value"], 0.05, "eV", "rel")
c = lib.measure("P20_H2plus_LCAO", 2)
print("mu_loc =", round(sol["De_eV"], 4), "eV ; mu_ref =", t["value"],
      "eV ; mot =", m["verdict"], "; d =", c.d_reg)
print(lib.audit_g1("P20_H2plus_LCAO").reason)
print(lib.audit_g2("P20_H2plus_LCAO").reason)
PY
```

Attendu : `mu_loc = 1.4632 eV ; mu_ref = 2.6508 eV ; mot = S- ; d = 2`
— δ ≈ 0,45 ≫ θ. Le mot est **S−** : l'ansatz est trop pauvre, et la
machine le dit avec les mêmes formules qu'un succès. C'est un *succès de
protocole* : un S− honnête vaut plus qu'un S+ raccommodé. Le levier gelé
(`ansatz<-table`) dit ce qu'il faudrait changer pour que le mot bascule :
enrichir l'ansatz, jamais déplacer θ.

## Exemple 3 (optionnel) — sous le capot : tare, chaîne typée, calibre (5 min)

Le même contact H₂⁺, vu par les trois bascules du capot
(`docs/DISCRET-CONTINU.md`). Le runner rend μ en Ha *avec la tare déjà
ôtée* ; la chaîne transporte Ha → eV ; le calibre est un poids étalon
déclaré avant le run.

```bash
python3 - <<'PY'
from mvcg.registers import run_registers

by = {r["id"]: r for r in run_registers()["rows"]}
r = by["P20_H2plus_LCAO"]
print("mu_raw  =", round(r["extra"]["mu_raw"], 6), "Ha  (tare déjà ôtée dans le runner)")
print("chaîne  = k", round(r["extra"]["chain"]["k"], 6),
      r["extra"]["chain"]["src"], "->", r["extra"]["chain"]["dst"],
      "| kill:", r["extra"]["chain"]["kill"])
print("mu_loc  =", round(r["mu_loc"], 4), "eV ; tare =", r["tare"],
      "Ha ; calibre =", r["caliber"])
g = r["extra"]["gum"]
print("gum     = u_c", g["uc"], "U", g["U"], "decide", g["decide"])
print("mot     =", r["verdict"], "| delta =", round(r["delta"], 4))
PY
```

Attendu (valeurs réelles) :

```
mu_raw  = 0.053771 Ha  (tare déjà ôtée dans le runner)
chaîne  = k 27.211386 Ha -> eV | kill: None
mu_loc  = 1.4632 eV ; tare = -0.5 Ha ; calibre = labo
gum     = u_c 0.0005 U 0.001 decide theta
mot     = S- | delta = 0.448
```

Trois règles du capot, visibles ligne par ligne :

1. **La tare reste dans le runner** (`-0.5` Ha = plateau vide, atomes
   séparés). La chaîne vient *après* — la soustraire une deuxième fois
   serait un double zéro.
2. **La chaîne est typée** : une 1-cellule `{τ=energy, src=Ha, dst=eV, k}`,
   vérifiée avant usage. Une rupture de τ ou de branche force **S−** —
   jamais de verdict sur la mauvaise fibre (test
   `test_chain_kill_forces_sminus`).
3. **Le calibre est un poids étalon, pas un levier** : `labo` déclare la
   classe de θ *avant* le run ; il ne recalcule jamais le verdict.
   Le budget GUM ne comptabilise que la ligne de table
   (`u_c = 0.0005` eV, `U = 2·u_c`), jamais une « erreur de modèle ».

## Ensuite

- Peser les contacts livrés : `python3 -m mvcg registers` (H, H₂⁺, H₂O,
  Kato, He, Dice, Friedmann) — les S− y sont voulus.
- Ajouter *votre* contact : une table dans `data/tables/`, un runner qui
rend `(mu_loc, extra)`, une ligne `Contact(...)` dans
`src/mvcg/registers.py`, un levier écrit, un test qui fixe le mot attendu.
  Voir `docs/NOTE-INGENIEUR.md` et `docs/PORTES-METIERS.md`.
- Le détail du protocole de gel : `docs/INVARIANTS-MATH.md`.
