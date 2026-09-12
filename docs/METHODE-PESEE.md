# Méthode de pesée MVC-G

Une pesée = un dossier \(D\), deux nombres, un mot. Pas un classement du réel.

## 1. Les trois capots

```
A  runner      →  μ_loc          (calcul ou lecture de table)
B  chaîne      →  même fibre     (pont Ha→eV, n_air, packet)
C  juge        →  S+ | P | S−    (δ contre θ ou contre U)
```

A ne tranche pas. C ne calcule pas. B ne change pas \(S\).

## 2. Le manifeste D

Champs obligatoires (`canonical_d`) :

```
id, s, packet, dimension, theta, mu_ref, lever, delta_kind
```

Souvent : table + `_sha256`, `runner_sha256`, `chain`, `gum`, tare, calibre.

Changer un de ces champs **après** \(\delta\), c’est un autre \(D\) (G2 si déjà gelé).

## 3. L’écart

```
delta_kind = rel     |μ_loc/μ_ref − 1|
delta_kind = abs     |μ_loc − μ_ref|
```

Le mot :

```
δ ≤ θ★      S+
θ★ < δ ≤ 2θ★ P
δ > 2θ★     S−
```

\(\theta_★ = \theta\) si `decide=theta`.  
\(\theta_★ = U = k\,u_c\) si `decide=U` (GUM).

P n’est pas un « presque vrai ». C’est la bande de garde.

## 4. Incertitude (quand elle existe)

Lignes type A : \(s/\sqrt{N}\).  
Lignes type B : \(u\) déclaré (certificat, WP, PDG).

\[
u_c^2 = c^{\mathsf T}(D R D)c
\]

\(R\) SDP : \(\lambda_{\min}\ge -\varepsilon\) (`eigvalsh`). Sinon Kill de budget, pas un P.

Le biais de modèle (Lowe, HF, CMD-3 vs KLOE) va dans \(\delta\), pas dans \(u_B\).

## 5. Fibre et couleur

`packet` ∈ {hl, gauss, si, 1}  
`dimension` : eV, Ha, cm⁻¹, Hz, 1, …

Même rue sous plusieurs paquets : `street_sweep`.  
Même \(D_e\) sous Ha / eV / cm⁻¹ : `lcao_unit_street` ( \(k\) gelés ).

Un S+ ne voyage pas (V7-a).  
I-V5 : S− a la même fiche que S+.  
I-V6 : un S+ exhibe \((\mu_{\mathrm{loc}},\mu_{\mathrm{ref}},\delta)\).

## 6. Déroulé d’une pesée

1. Écrire \(S\) (égalité de deux nombres).  
2. Geler \(D\) (θ, U, table, runner, fibre).  
3. `execute` le runner → μ_loc.  
4. Ponts B si besoin.  
5. `parse_units` : paquet illicite → S−.  
6. δ puis C.  
7. Option : `archive` JSONL ; option : G1 `freeze` / G2.

Rejeu : même SHA runner + table → même mot (I-V4).

## 7. Ce qui n’est pas une pesée

- moyenne de deux \(D\) (WP20+WP25, Planck+SH0ES) ;  
- \(\eta_{\mathrm{S+}}\) comme μ ;  
- « mécanisme connu = S+ » ;  
- élargir \(u\) après lecture ;  
- fetch HITRAN / PDG / NIST live.

## 8. Casier — la carte des modes

Un **mode fonctionnel** = un dossier D (règle, θ, table, fibre). Le
casier (`mvcg.casier.index()`) liste les modes : les cartes « pesé »
sont **dérivées du registre** — jamais déclarées, une étiquette ne ment
pas par construction ; les cartes « sans μ » sont des modes possibles
en attente d'extrait — elles ne pèsent rien et ne doivent rien
afficher. Le casier n'a pas de score SM : comparer les modes, oui ;
classer le réel, non.

## 9. Commandes

```bash
PYTHONPATH=src python3 -c "from mvcg.registers import run_registers; import json; print(json.dumps(run_registers()['counts'], indent=2))"
PYTHONPATH=src python3 -c "from mvcg.casier import index; print(index()['warning'])"
PYTHONPATH=src python3 -c "from mvcg.verdict_register import mode_unites; print(mode_unites('si','eV'))"
```
