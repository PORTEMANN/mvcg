# Capot — du discret au continu (et retour)

Sous le capot, il n’y a **pas** un pont ontologique discret ↔ continu.
Il y a **trois bascules** algorithmiques, dans les deux sens, et un interdit :
les fondre en une seule « structure noétique ».

## Vue d’ensemble

```
continu (réel, champ, flottant)
        │
        │  [A] échantillonnage / runner
        ▼
μ_loc , μ_ref     ∈ ℝ
        │
        │  [B] tare, chaîne d'unités (encore ℝ)
        ▼
δ ∈ ℝ ∪ {∞}
        │
        │  [C] calibre + θ + GUM → mot
        ▼
S+ | P | S−       discret à 3 lettres
```

L’inverse n’est pas une déquantification magique : c’est **relire** un mot
comme contrainte sur un continu (fenêtre, grille, paquet).

## C — continu → discret (le cœur)

Fichiers : `metrics.py`, `gum.py`, `balance.py`.

ADC à 3 niveaux : S+ si `δ ≤ θ★`, P si `θ★ < δ ≤ 2θ★`, S− sinon.

`θ★` vaut `θ` (`decide=theta`), `k u_c` (`decide=U`), ou l’héritage
`max(θ,σ)` (à ne plus étendre).

Rien n’explique le continu. On le **tranche**.

## A — continu → discret (avant μ)

| Module | Continu | Discret |
|---|---|---|
| `dynamics.py` / `spectral3d.py` | u(x,t) | modes k, grille n (FFT, ℙ, 2/3 ou pad 3/2) |
| `corridor.py` E68 | même EDP | couple (n, r(n)) → spread → mot |
| `h2plus.py` | R, ζ | un De |
| Dice / P35 | cartes, traces | un scalaire |

Le masque 2/3 jette du continu (hauts k) pour que le produit non linéaire
ne mente pas sur la grille. E68 : si le mot change avec n, la grille parle.

## B — continu → continu

`chain.py`, `rationalization.py`, `balance.after_tare`.

Multiplications et tare restent dans ℝ. Le discret, ici, est le **choix de
fibre** (`packet=hl|gauss|si|1`). `dictionaries.py` : même μ_loc, autre
μ_ref(U) → autre mot = C après un saut de fibre.

## Discret → continu

La machine ne reconstruit pas un champ depuis S+. Elle **contraint** :

| Discret | Préimage continue |
|---|---|
| mot P | δ ∈ (θ, 2θ] |
| E64 κ ∈ ]0.075, 0.125[ | un intervalle réel |
| packet=hl | une formule eg=2πn |
| calibre labo | une classe de θ |
| G1 frozen_at | t ≥ t0 |

Publier S+ sans (μ, θ, U) jette la préimage. D’où `D.json` dans le hash.
Pas d’algo « S− → champ corrigé » (solveur inverse, hors machine).

## Structures

```
Contact     id, packet, θ, μ_ref, runner, caliber, gum, tare
runner  →   (μ_loc: float, extra: dict)     extra hors δ
D.json      discret de décision + tare + gum
bits.json   G1 administratif
```

P27 (méthode sourde) et E68 (grille) sont deux **coupes** distinctes.
Les composer dans une phrase unique referme le capot avec de la prose.

## Phrase

Du continu au discret : échantillonner (A), transporter (B), trancher (C).
Du discret au continu : préimage d’un mot — une bande, un paquet, une fenêtre.
Pas d’autre engrenage.
