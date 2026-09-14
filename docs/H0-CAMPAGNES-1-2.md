# H0 — campagnes 1 & 2 : robustesse d'affichage et frontière du levier

Exploration locale du chantier H0 (2026-09-13 après-midi), non publiée.
Aucun gel modifié : θ = 0,05 abs, table `h0_LITERATURE-2018.json`
et mot **P** (δ = 8,368 %) restent figés. Ces campagnes testent le
contact, elles ne le rouvrent pas.

## Campagne 1 — street sweep (MVC-G-STREET-0.1)

Même couple (μ_loc, μ_ref) posé sous chaque paquet de la rue :

| paquet | δ | mot | kill |
|---|---|---|---|
| hl | 8,368 % | P | — |
| gauss | 8,368 % | P | — |
| si | 8,368 % | P | — |
| 1 (domicile) | 8,368 % | P | — |

Lecture : le mot est **indépendant de l'unité d'affichage**, aucun
paquet illicite. C'est la tension qui est pesée, pas sa présentation.

## Campagne 2 — frontière du levier déclaré (f←Planck_ou_SH0ES)

Balayage en pas de sigma **déclarés de chaque fabrication**
(u_SH0ES = 1,04 ; u_Planck = 0,5), l'autre fabrication fixe.
Règle de décision inchangée : δ = |S/P − 1| vs identité 0, θ gelé.

### Frontières exactes du changement de mot

| Levier | S+ si | soit | S− si | soit |
|---|---|---|---|---|
| SH0ES (P fixe) | S ≤ 70,77 | −2,2 σ | S ≥ 74,14 | +1,1 σ |
| Planck (S fixe) | P ≥ 69,56 | +4,3 σ | P ≤ 66,40 | −2,0 σ |

### Balayage complet (mot pesé par la machine)

SH0ES (P = 67,4 fixe) :

| σ | valeur | δ | mot |
|---|---|---|---|
| −3 σ | 69,92 | 3,739 % | S+ |
| −2 σ | 70,96 | 5,282 % | P |
| −1 σ | 72,00 | 6,825 % | P |
| 0 | 73,04 | 8,368 % | **P (figé)** |
| +1 σ | 74,08 | 9,911 % | P |
| +2 σ | 75,12 | 11,454 % | S− |

Planck (S = 73,04 fixe) :

| σ | valeur | δ | mot |
|---|---|---|---|
| −2 σ | 66,40 | 10,000 % | S− |
| −1 σ | 66,90 | 9,178 % | P |
| 0 | 67,40 | 8,368 % | **P (figé)** |
| +4 σ | 69,40 | 5,245 % | P |
| +5 σ | 69,90 | 4,492 % | S+ |

## Lectures

1. **Le levier déclaré est réel et quantifié.** La machine publie la
   frontière exacte du changement de mot, en sigma déclarés. Une
   réanalyse future se lira immédiatement sur cette carte.

2. **Le P est asymétriquement exposé.** Il est deux fois plus proche
   du S− par le haut SH0ES (+1,1 σ) que du S+ par le bas (−2,2 σ).
   Une réanalyse qui remonterait l'échelle locale transformerait la
   tension en dette structurelle au sens du protocole (zone ≥ 2θ).

3. **Côté Planck, le S+ est lointain (+4,3 σ).** Aucune réanalyse
   CMB raisonnable ne referme la tension par ce bord — cohérent avec
   le GUM (U = 3,42 % ≪ θ) : la tension n'est pas une fluctuation
   d'incertitude.

## Honnêteté (limites déclarées)

- Les pas de sigma sont les incertitudes **déclarées par chaque
  fabrication** ; comparer « +1,1 σ SH0ES » à « +4,3 σ Planck » est
  la carte du levier, pas un verdict sur les programmes. L'attribution
  physique (quel programme est susceptible de bouger) reste déclarée,
  jamais choisie par la machine.
- Les valeurs hors table sont des scénarios de levier, pas des
  mesures : elles ne modifient ni la table gelée ni le mot figé.
- Le mot du contact reste **P** jusqu'à ce qu'une fabrication
  déclarée nouvelle (réanalyse publiée) soit ajoutée à la table —
  geste qui reste celui d'un tiers.
