# H0 — campagne 3 : frontière du levier sur le contact bas-z

Exploration locale du chantier H0 (2026-09-13 soir), non publiée.
Suite directe des campagnes 1 & 2 (`H0-CAMPAGNES-1-2.md`) et du contact
bas-z (`H0-HZ-SNE-CONTACT-OUVERT.md`). Aucun gel modifié : θ = 0,05 mag
abs, table `hz_sne_LOWZ-DEMO-2026.json`, mot **S−** (δ = 0,1173 mag)
figés. Cette campagne pèse le levier `H0<-SH0ES_ou_autre` annoncé dans
le doc du contact — elle teste la carte, elle ne la rouvre pas.

## Protocole

Le levier déplace le H0 de la **courbe prédite** H(z) — jamais les
bins, jamais θ, jamais les Ω gelés. Pour chaque valeur H0 levier :
μ_pred(zᵢ) = 5 log₁₀ d_L(zᵢ ; H0) + 25, δ = rms des résidus sur les
8 bins, mot par la règle gelée (S+ si δ < θ, P si θ ≤ δ < 2θ, S− si
δ ≥ 2θ). Frontières localisées par bisection à 10⁻¹⁵ mag.

## Balayage (mot pesé par la machine)

| H0 courbe | rms (mag) | δ/θ | mot |
|---|---|---|---|
| 65,00 | 0,1927 | 3,85 | S− |
| 67,40 (Planck) | 0,1173 | 2,35 | **S− (figé)** |
| 68,50 | 0,0855 | 1,71 | P |
| 69,50 | 0,0604 | 1,21 | P |
| 70,00 (fiducial) | 0,0506 | 1,01 | P (au cheveu) |
| 70,50 | 0,0444 | 0,89 | S+ |
| 71,00 | 0,0430 | 0,86 | S+ |
| 72,50 | 0,0653 | 1,31 | P |
| 73,04 (SH0ES) | 0,0782 | 1,56 | P |
| 74,00 | 0,1031 | 2,06 | S− |
| 76,00 | 0,1576 | 3,15 | S− |

## Frontières exactes

| Frontière | H0 | en sigma déclarés |
|---|---|---|
| S− → P (montée) | 67,99 | Planck +1,2 σ_P |
| P → S+ | 70,04 | — |
| S+ → P | 71,72 | — |
| P → S− (descente) | 73,89 | SH0ES +0,8 σ_S |

Minimum du rms : H0* = 70,87, rms_min = 0,0429 mag — **sous** θ.
Fenêtre S+ : [70,04 ; 71,72], largeur 1,68 km/s/Mpc.

## Lectures

1. **La fenêtre S+ existe à 8 bins.** Le doc du contact écrivait « un
   S+ exigerait plus de bins » — c'était l'estimation honnête au point
   H0 = 70 (P à 0,0506, marge de 0,0013 sous θ). Le balayage complet
   montre une fenêtre S+ réelle, centrée sur le bruit réalisé
   (H0* = 70,87, décalage du bruit, honnêtement déclaré dans le doc).
   La correction est consignée ici, pas rétroactivement : l'estimation
   était fausse de la part du hasard, comme annoncé possible.

2. **Lecture miroir des deux fabrications.** Sur la carte bas-z :
   la fabrication **Planck (67,4) est S−** ; la fabrication **SH0ES
   (73,04) est P**. La tension entre fabrications se lit donc aussi
   dans ce contact : il faudrait monter la courbe Planck de +1,2 σ_P
   pour qu'elle entre en zone P, alors que SH0ES n'est qu'à +0,8 σ_S
   du bord S− haut. Même asymétrie qualitative que la campagne 2 de
   la tension (le P y était exposé au S− par le haut SH0ES à +1,1 σ).
   Deux cartes indépendantes, même penchant — coché.

3. **La doctrine tient sous le levier.** Bins et θ gelés, seul le H0
   de la fabrication bouge : la carte répond comme annoncé. Quand la
   table LITERATURE remplacera la table DEMO, ce balayage se relit
   tel quel — seule la géométrie des frontières changera.

## Honnêteté (limites déclarées)

- Table SYNTHÉTIQUE : les frontières quantifient la réponse du
  protocole sur une réponse connue par construction, rien de l'univers
  réel. La dette de nature du contact n'est pas soldée.
- Les sigmas du tableau sont les incertitudes **déclarées** des
  fabrications (u_P = 0,5 ; u_S = 1,04) : c'est la carte du levier,
  pas un verdict attribuant le tort à un programme.
- H0* = 70,87 ≠ 70 : le minimum suit le bruit réalisé (seed gelée
  20260913). La carte ne connaît pas son propre centre exact — le
  fiducial 70 reste la déclaration, pas H0*.
- Le mot du contact reste **S−** : ces scénarios de levier ne
  modifient ni la table gelée ni le mot figé.
