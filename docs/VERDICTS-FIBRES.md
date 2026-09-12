# Registre des verdicts — index par fibre

Méthode portée de la mouture de développement (module
`src/mvcg/verdict_register.py`, protocole MVC-G-VERDICT-REG-0.1) et
appliquée à la série en ligne le 2026-09-12.

## Ce que la méthode fait

Indexer les verdicts par **fibre** = couple (packet, dimension) du
dictionnaire d'unités, puis **balayer** chaque contact sous les quatre
paquets (hl, gauss, si, 1) à μ_loc et μ_ref gelés. Le paquet ne change
le mot que s'il est illicite pour la dimension (units_kill) — pour un
δ relatif, δ est invariant, donc le mot doit l'être aussi.

Trois opérations interdites, écrites dans le module :

- η (rendement) comme μ : le comptage ne produit jamais une métrique ;
- export d'un mot vers une autre fibre : un S+ de la fibre (1, cm⁻¹)
  n'est pas une entrée de la fibre (si, eV) ;
- moyennage des couleurs : trois fibres d'affichage d'un même calcul
  (cf. `lcao_unit_street`) donnent trois lignes, jamais une moyenne.

## Le classement de la série en ligne (2026-09-12)

31 lignes de registre, 9 fibres :

| Packet | Dimension | n | S+ | P | S− |
|---|---|---|---|---|---|
| 1 | 1 | 10 | 4 | 0 | 6 |
| 1 | cm⁻¹ | 6 | 4 | 2 | 0 |
| si | D | 2 | 0 | 0 | 2 |
| si | Ha | 2 | 1 | 0 | 1 |
| si | J m⁻³ K⁻² | 2 | 1 | 0 | 1 |
| si | eV | 6 | 3 | 0 | 3 |
| si | m/s | 1 | 0 | 1 | 0 |
| si | nK | 1 | 1 | 0 | 0 |
| si | µm | 1 | 1 | 0 | 0 |

## Le résultat qui compte : invariance totale

Les **16 contacts ouverts O1 → O16** ont été balayés chacun sous les
quatre paquets : **aucun units_kill, aucune divergence**. Chaque mot
découvert après gel est identique dans les quatre couleurs. La série
n'est pas un artefact du dictionnaire d'unités — un S+ pesé en cm⁻¹
(packet 1) reste S+ sous hl, gauss et si, au δ près strictement
identique (12 décimales pour O13 : 0,010285795843).

Deux lectures :

1. **Discipline** : le verdict appartient à la règle + θ + référence,
   pas au paquet. Le paquet est une étiquette d'affichage, pas une
   nouvelle pesée.
2. **Frontière** : si un jour un contact diverge sous balayage, le mot
   à examiner n'est pas « le paquet a changé le verdict » mais « la
   dimension déclarée était illicite quelque part » — c'est un signal
   de protocole, jamais une correction à faire au marteau.

## Campagnes

Chaque contact porte son identifiant de campagne (O1…O16) ; le
classement par fibre ne fusionne jamais deux campagnes. Compter les
mots d'une campagne se fait dans sa fibre d'origine, avec le warning
du module : *un S+ n'est pas une entrée d'une autre fibre*.

## Rejouer

```bash
PYTHONPATH=src python -m unittest tests.test_verdict_register tests.test_verdicts_online
```

Le test `test_verdicts_online.py` fige le classement (31 lignes, 9
fibres, invariance des 16 contacts) comme les tests O* figent les mots.
