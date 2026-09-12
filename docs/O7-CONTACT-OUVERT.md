# O7 — septième contact ouvert : le levier d'O3 tient son seuil

Un contact **ouvert** = le mot n'est pas connu au moment où le protocole
est gelé. O6 a montré que la machine sait gagner quand le levier d'une
**grille** est activé. O7 pose la question plus dure : le levier d'un
modèle *phénoménologique* (une constante de force effective) peut-il
produire un S+ honnête ?

## Chronologie du gel (ordre qui fait la valeur)

1. **Protocole écrit avant toute exécution** :
   - même table bandes `carbon_raman_LITERATURE-2018.json` (G graphite
     1580, référence D observée 1350) ;
   - nouvelle table `carbon_raman_forces_LITERATURE-2018.json` :
     **r = k₂/k₁ = 3,0**, paramètre *effectif* du modèle chaîne 1D,
     déclaré — et la table dit noir sur blanc que ce n'est **pas une
     constante mesurée** ;
   - règle déclarée : D = G·√[max(1,r)/(1+r)], le levier
     `k<-desegaliser` d'O3 activé ;
   - **MÊME θ = 0,10 gelé qu'O3** — le seuil ne bouge jamais ;
   - anti-tautologie maintenue : la bande D observée ne participe
     toujours pas au calcul ; seuls G et r pilotent.
2. **Premier run** : mot découvert, pas choisi : **S+**,
   δ ≈ 1,36 % (θ = 10 %, tenu d'un facteur 7). Artefacts gelés
   (offline) : `examples/registre/O7.{bits,units,metric,cost}.json` —
   audit relançable : `[HOLD] I-G1`, `[HOLD] I-G2`.
3. **Figé** : le mot entre dans le test `test_open_o7.py`.

## Le mot : S+

μ_loc = 1368,32 cm⁻¹ (chaîne à r = 3) contre μ_ref = 1350 cm⁻¹
(bande D observée) : le premier **S+ ouvert sur un objet
phénoménologique** — pas une grille numérique, une grandeur physique de
spectroscopie.

## La fenêtre de robustesse — et une propriété exacte du modèle

Le test de levier (hors gel) calcule les bornes exactes du S+ :
r ∈ [1,447 ; 7,574], soit un **facteur 5,2** sur le paramètre. Le
contact gelé (r = 3) est dedans, à distance 1,55 de la borne basse :
le verdict est **robuste** — contrairement au P fragile en n d'O5
(bascule à +2,5 %).

Propriété honnête que le calcul impose : ce modèle ne fait **jamais
S−** pour r > 0 (hors fenêtre, δ reste bornée dans [13,8 % ; 17,0 %]).
Le S− n'est pas accessible à la chaîne à deux constantes : le contact
O3 (P) ne pouvait pas être « raté » en S− par malchance de paramètre.
Cela ne diminue pas le S+ — cela borne la promesse du modèle, ce que
le levier doit toujours faire.

## La paire O3 → O7

| | O3 (r = 1, forces égales) | O7 (r = 3, levier activé) |
|---|---|---|
| θ | 0,10 | **inchangé** |
| μ_ref | 1350 cm⁻¹ | identique |
| μ_loc | 1117,23 cm⁻¹ | 1368,32 cm⁻¹ |
| mot | P | **S+** |

Deuxième démonstration du geste « levier écrit à l'échec, activé plus
tard, θ jamais déplacé ». Avec O1 → O6, la règle se généralise :
**tout contact a droit à son levier activé** — c'est devenu un schéma
de la machine, pas une anecdote.

## Règles de lecture

- **Robuste ≠ garanti** : le S+ survit à un facteur 5,2 sur r, mais il
  est arrivé après le gel comme les autres — il était découvert.
- **Le paramètre effectif est déclaré comme tel** : r = 3 n'est pas
  une constante de la nature ; c'est un ordre de grandeur de la
  littérature des solides lamellaires, gelé dans une table vintage qui
  l'assume. Confondre les deux serait une usurpation de calibre.
- **Rejouer O7** : `python3 -m mvcg registers` — même S+, mêmes bits.

## Pourquoi O7 compte

La série disait : S−, P, P, S−, P, S+. Avec O7 elle dit aussi :
le S+ n'est pas réservé aux grilles numériques — un modèle de force
déclaré honnêtement (avec ses limites écrites dedans) peut tenir un
seuil de spectroscopie. C'est la réponse la plus directe à la question
« y a-t-il des contacts en physique quantique en S+ ? » : oui, à
condition d'accepter que le paramètre soit un paramètre — déclaré,
gelé, à sa place.
