# Quatre portes — mode d’emploi

Même mécanique pour tous : table + \(\mu_{\mathrm{loc}}\) + \(\theta\) + levier.
Le contenu de \(S\) change. Commandes depuis la racine du dépôt :

```bash
export PYTHONPATH=src
python3 -m unittest discover -s tests -q
```

---

## 1. Physicien — dictionnaire et constante

**But.** Voir qu’un même nombre change de mot quand on change \(U\).

```bash
python3 -m mvcg dictionaries
```

Lignes Dirac (\(\mu_{\mathrm{loc}}=2\pi\)) :

| packet | mot |
|---|---|
| `hl` | S+ |
| `gauss` | S− |
| `si` (vide CODATA) | S− |
| `1` | S− (`units_kill`) |

**Exemple à recopier.** Gel d’un contact Dirac HL :

```python
from pathlib import Path
from mvcg.met_lib import MetLib15

D = {
    "id": "dirac_hl",
    "s": "eg = 2π (HL, n=1, ħ=1)",
    "packet": "hl", "dimension": "e*g",
    "theta": 1e-9, "sigma": None,
    "mu_ref": 6.283185307179586,
    "lever": "packet←gauss",
    "delta_kind": "rel", "register": "micro", "orig": "thm",
}
lib = MetLib15(Path("/tmp/phys"), offline_ots=True)
lib.freeze("dirac_hl", phys=1, orig="thm", kappa_hat="equilibre", dossier=D)
lib.freeze_units("dirac_hl", {"packet": "hl", "vintage": "convention"})
lib.record_metric("dirac_hl", 2 * 3.141592653589793, D["mu_ref"], 1e-9, "e*g", "rel")
lib.measure("dirac_hl", 0)   # 0 = S+
print(lib.audit_g1("dirac_hl"))
```

Levier : refaire le `record_metric` avec `mu_ref=0.5` et `packet=gauss` dans **un autre** id (`dirac_gauss`). Ne pas moyenner \(2\pi\) et \(1/2\).

Raie H 1s : `python3 -m mvcg registers` → `H1s_Rydberg` S+, `H1s_Rydberg_13p6` S− (levier vintage).

**Piège.** `packet=si`, `epsilon0=1`, dimension `e*g` : refusé (usurpation HL).

---

## 2. Chimiste — table moléculaire + ansatz

**But.** Un calcul pauvre contre une table datée. Le S− est le résultat.

```bash
python3 -m mvcg registers
```

| id | \(\mu_{\mathrm{loc}}\) | \(\mu_{\mathrm{ref}}\) | mot |
|---|---|---|---|
| `P20_H2plus_LCAO` | Lowe \(R=2\), \(\sim1{,}46\,\mathrm{eV}\) | \(2{,}6508\,\mathrm{eV}\) | S− |
| `P21_H2O_dipole` | \(1{,}50\,\mathrm{D}\) | \(1{,}8546\,\mathrm{D}\) | S− |
| `P27_He_HF` | \(0\) | \(-0{,}042044\,\mathrm{Ha}\) | S− |
| `P30_Kato_gaussian` | \(0\) | \(-1\) | S− |
| `P30_Kato_1s` | \(-1\) | \(-1\) | S+ |

**Exemple H₂⁺** (déjà dans `NOTE-INGENIEUR.md`) : `lcao_1s(2.0)["De_eV"]` vs `h2plus_de()["value"]`, \(\theta=0.05\) rel.

**Exemple P27 à lire comme recette :**

- table `data/tables/he_corr_LITERATURE-2018.json` ;
- runner HF : \(\mu_{\mathrm{loc}}=0\) (aucune corr. récupérée) ;
- `expected: S-` → si un jour le mot devient S+, `b3_fail` s’allume.

**Ajouter *votre* molécule.**

1. JSON dans `data/tables/` : `vintage`, `value`, `source`, `dimension`.  
2. Runner qui calcule autre chose que `value` (sauf contrôle tautologique).  
3. `Contact` + test `assertEqual(..., "S-")` ou `"S+"`.  
4. Levier écrit : `base←autre`, `R←Re`, `methode←HF`.

**Piège.** Appeler « corrélation » l’écart LCAO / exact de H₂⁺ (1 électron).

---

## 3. Cosmologue — un millésime, une fermeture

**But.** Peser un budget \(\Omega\) *ou* un \(H_0\), jamais les deux collés dans le même \(\mu\).

```bash
python3 -m mvcg registers
```

| id | \(S\) | mot |
|---|---|---|
| `FRW_lcdm_Planck` | \(\lvert 1-(\Omega_m+\Omega_\Lambda)\rvert\) petit | S+ |
| `FRW_baryons` | « les baryons ferment le plat » | S− |
| `FRW_lcdm_SH0ES` | mêmes \(\Omega\), autre étiquette \(H_0\) | S+ sur \(\Omega\) ; \(H_0\) n’entre pas dans \(\mu\) |

**Exemple à ne pas faire.**  
\(\mu = 67.4\) (Planck) comparé à \(73\) (SH0ES) en prétendant que c’est la fermeture de Friedmann. Ce sont deux contacts \(H_0\), deux vintages, deux `D`.

**Exemple chaîne \(H_0\)** (à déclarer dans `D.chain` le jour où vous le codez) :

```
km s⁻¹ Mpc⁻¹  →  s⁻¹  →  (option) × t_P
```

Un seul vintage par ligne (Planck-2018 **ou** SH0ES).

**Piège.** Moyenner les deux \(H_0\) pour « passer P ». I-V2.

---

## 4. Neurologue — échec déclaré, pas l’Allen

**But.** Un overlap ou un Dice entre deux partitions *que vous donnez*. Le modèle facile doit perdre.

```bash
python3 -m mvcg registers
```

| id | \(S\) | mot |
|---|---|---|
| `P35_sigma_spike` | σ logistique = spike | S− (B3-FAIL tenu) |
| `AAL_dice_atlas` | même atlas lissé vs lui-même / autre | S− dès `atlas←autre` |

**Exemple Dice (déjà dans le runner).** Grille \(32\times32\), 8 labels, lissage 3×3. Levier : permutation + 15 % de bruit → le Dice tombe, mot S− si \(\theta=0.05\) abs et cible \(1\).

**Exemple spike.** \(\mu_{\mathrm{ref}}=1\) (recouvrement parfait), \(\mu_{\mathrm{loc}}=0\) (σ n’est pas un potentiel d’action). \(\theta=0.05\) abs → S−. C’est le dossier à montrer en premier : la machine *refuse* le modèle scolaire.

**Ce que vous apportez.** Deux cartes (NIfTI → labels déjà discrétisés), une formule Dice ou Jaccard, un vintage d’atlas (AAL2 vs AAL3 = deux `D`). Pas le dépôt Allen Cell Types entier.

**Piège.** Lire P34 (neurone formel) comme une validation du cortex.

---

## Publier (les quatre)

```bash
python3 -m mvcg --root /tmp/mvcg-pub campaign --publish --offline
```

Vérifier qu’un `*.D.json` existe à côté du `*.bits.json`.  
Sans \(D\), le mot n’est pas un résultat scientifique de *cette* machine.

Répétition sans hash :

```bash
python3 -m mvcg --root /tmp/mvcg-rep campaign
```

---

## Rappels communs

- Un mot par contact, un `packet` par ligne.  
- Micro / méso / macro = classeurs, pas des laboratoires.  
- Archive historique : dépôt séparé de l’auteur, sans lien ici — pas une dépendance.
