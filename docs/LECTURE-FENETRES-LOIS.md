# Lecture par familles — fenêtres de validité des lois déclarées

Date : 2026-09-29. Document de lecture **au-dessus** du registre (124
contacts) — aucun verdict nouveau, aucune donnée nouvelle. Statut :
local, non commité. Provenance : doctrine proposée par le paquet
MVC-G ext v0.5 (2026-09-28), absorbée ici sans code (voir §1).

## 1. Doctrine absorbée (proposition d'extension des invariants — non intégrée)

Absorbée telle quelle du paquet ext, comme *doctrine* uniquement. Pas de
code greffé ; intégration aux invariants du dépôt en attente de décision.

- **D1–D4 (dimensionalité avant lecture)** : un contact ne se lit dans
  une carte d'échelle que si sa dimension est déclarée (M, L, T, Q) —
  sinon HOLD. Le registre possède déjà cette information par les fibres
  (packet, dimension) ; la règle la formalise pour toute lecture
  géométrique future.
- **F1 (jamais de comparaison inter-fibres)** : un contact n'est
  comparable qu'à un contact de même fibre, même dimension, même type
  d'étalonnage, même θ. Déjà la pratique du registre (VERDICTS-FIBRES,
  balayage calibré, « jamais de moyennage des couleurs ») ; le tueur la
  rend explicite.
- **R8 (« transition » réservé)** : le mot « transition » (de phase, de
  loi, d'échelle) n'est prononçable que si Δlog ℓ ≠ 0 entre les deux
  côtés. Sinon c'est un changement de levier, pas une transition.
  Pendant du gel existant : « verdict mince ≠ frontière ».
- **Note H0/S8 (deux tensions, deux fibres)** : H0 (taux d'expansion,
  fibre verticale Δlog ℓ = 0) et S8 (σ8√(Ωm/0.3), bifurquée 2026 :
  DES Y6 ~2,4-2,7σ vs CMB, KiDS-Legacy < 1σ) sont deux tensions à deux
  leviers — ne pas moyenner, ne pas fusionner en « secteur sombre »
  unique. La fibre S8 ne s'ouvrirait qu'avec des contacts séparés
  (S8-DES-Y6, S8-KIDS-LEGACY, S8-CMB).

## 2. La cartographie — chaque loi déclarée a une fenêtre

Principe de lecture : un S+ dit *où* une loi tient ; un S− dit *où*
elle casse ; la paire (S+, S−) sur la même loi **délimite sa fenêtre de
validité**. Le registre devient une carte de domaines, pas une liste de
mots.

| Loi déclarée | Tient (S+) | Casse (S−) | Fenêtre délimitée |
|---|---|---|---|
| Tuinstra-Koenig I_D/I_G = C/L_a (514 nm) | O14 : L_a = 10 nm, δ = 2,2 % | O4 : L_a = 3 nm, δ = 22,2 % | L_a ≳ 4 nm à 514 nm ; la loi s'effondre sous ~4 nm (régime Ferrari-Robertson C'/L_a²) |
| Karplus ³J(HN,Hα) | NMR hélice φ=−60° : δ = 2,7 % | NMR brin φ=−120° : δ = 16,1 % ; Vogeli-Bax 2007 : 18,7 % / 16,0 % | la loi « devient une carte » : fenêtre conformationnelle hélice, pas brin |
| Catalogue NIST rotationnel CO | Dunham 2B₀−4D₀ = ν(1−0) : δ = 280 Hz | règle μ ¹³CO : 412 θ | les identités internes du catalogue tiennent ; les règles de transfert isotopique approximatives ont une fenêtre étroite |
| Loi harmonique m = m_p·2^{n/12} | quinte μ (0,59 %), diagonale Z (0,30 %), Koide (9,2e−5 θ), up (3,1 %), charm (1,5 %), Zmax modes (0,21 %), gamme ANU (0,12 %) | sqf KO-6 (14 U), α double usage (630 %), pont RMS (138 %), G11 (2 002 θ), addendum corps (1 U) | **leptons + boson Z** tiennent à θ près ; quarks moyens/lourds gris (P × 3, δ 12-13 %) ; le reste de la loi n'a pas de fenêtre |
| Gamme 2^{1/12} comme moyenne des rapports ANU | LH_Anu_Gamme : 0,117 θ ; B3 seuil Z25 : 0,76 θ | B2 moyenne (0,15 θ, attendu S+), MDA suite (290 θ), linéaire 46,9Z−151,2 (340 θ), E30 (auto-réfutation corpus) | tient comme **statistique de rapports** sur la table 1908 ; ne tient pas comme **spectre de masses** ni comme **modèle en Z** — deux objets portent le même symbole |
| Modèle k(Z,N) (B1) | fusion D-T (0,56 θ), table comparaison (0,10 θ), B11 (0,94 θ, au cheveu) | grille NUBASE (6,18 θ, RMS 12,4 %), exp Q6,5 (5,95 θ), sensibilité shell (783 θ) | tient sur les **données standard citées** ; casse dès que le modèle extrapole hors ses exemples |
| Corridor F_exp ±3 % | — (le max tient) | plancher : 5 violations, u 0,917 (P 1,78 θ) | la prétention d'un corridor minimaliste tient en zone meso/macro grise, pas en plancher |
| Prédictions P1-P30 (page Brouillons) | les « vérifiées » sont des copies (25/26 paires identiques, S− meta 9,6 θ) | — | **aucune fenêtre** : la « loi » est une recopie de la mesure — tare nommée |
| Étalonnages croisés | Rydberg voie 2 (certification CODATA), g-2 WP25 (38/63 U), HLbL (dans 1 U), Lamb moderne (0,30 θ) | g-2 WP20 (279/76 U), HVP LO dispersif (P), Dirac historique | la physique tient ; chaque **fabrication** (lattice vs dispersif, calcul vs calcul) a sa propre fenêtre |

## 3. Les cinq types de frontière que le registre distingue déjà

La lecture fait émerger une taxonomie — les verdicts du registre
classent les frontières de validité en cinq familles :

1. **Frontière d'échelle spatiale** (TK 3↔10 nm) : la loi tient d'un
   côté, casse de l'autre, et le contact au cheveu (O4★, gelé) fermerait
   la frontière.
2. **Frontière conformationnelle / paramétrique** (Karplus hélice/brin) :
   mêmes coefficients gelés, deux mots — la loi est locale dans l'espace
   des paramètres.
3. **Frontière de population** (loi harmonique : leptons oui, quarks
   non) : la loi trie sa propre classe d'objets ; les P (12-13 %)
   marquent la limite grise entre population valide et non.
4. **Frontière de modèle approximatif** (Dunham tient, règle μ casse ;
   modèle k(Z,N) : exemples oui, grille non) : la loi est un développement
   limité dont la fenêtre est l'ordre du modèle.
5. **Frontière de fabrication** (g-2 WP25/WP20, HVP LO ; H0 Planck/SH0ES)
   : même observable, deux instruments — les S+ et S− se répartissent
   entre fabrications, pas entre théories.

Et une sixième catégorie, négative : les lois **sans fenêtre** — qui ne
tiennent nulle part (δANU : 83 θ ; linéaire ANU : 340 θ ; sensibilité
shell : 783 θ ; G11 : 2 002 θ). Leur S− massif dit : pas de domaine, pas
de loi.

## 4. Ce que ce document change pour la machine

- **Lecture** : un verdict se lit désormais comme une position dans un
  domaine (« TK tient à 10 nm » ≠ « TK tient »). Le BILAN-TRANSVERSALE
  classait les *défaillances* ; ce document cartographie les
  *validités*. Les deux couches se superposent.
- **Doctrine** : D1-D4/F1/R8 + note H0/S8 sont proposées pour intégration
  aux invariants du dépôt (décision à prendre ; aucun code avant que la
  géométrie ait ≥ 2 familles de lois porteuses d'échelle — O4★ et W-DE).
- **O4★ inchangé** : GELE_AVANT_D, en attente de la référence observée à
  L_a ≈ 5,5 nm. R5/R6 prêts, donnée manquante — dette nommée.
- **W-DE** : la note H0/S8 justifie l'unique fibre nouvelle prévue ;
  θ à gelier avant le prochain data release.
