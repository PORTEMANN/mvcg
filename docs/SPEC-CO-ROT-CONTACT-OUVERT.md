# SPEC — CO rotationnel : contacts ouverts

**Statut : deux contacts ouverts, mots découverts et figés le 2026-09-14.**
**Fibre :** `("si", "Hz")` — la fibre ouverte au rotationnel (jusque-là
NMR seule, δ rel) ; les deux contacts CO y sont en δ absolu.

## Pourquoi ce chantier

La fibre (1, cm⁻¹) ne pèse que des oscillateurs vibrationnels 1D.
Le geste complémentaire de la spectroscopie moléculaire est le
**rotor rigide** — et son ancrage dans la recherche actuelle est
maximal : les catalogues micro-ondes (NIST JPCRD 53 / CDMS) sous-tendent
toute l'astrochimie millimétrique (ALMA, > 300 molécules ; JWST ;
ELT-HARMONI). ¹²C¹⁶O X¹Σ⁺ est le calibrateur universel de cette
astronomie : ν(1-0) = 115 271,204 MHz.

## Les deux contacts (règles gelées avant run, protocole SPEC-CO-ROT-PROTOCOLE.md)

| Contact | Règle | θ | Mot | δ/θ |
|---|---|---|---|---|
| `SPEC_CO_Rot_AbInitio` | \|B_e,calc − B₀,obs\|, B_e = ℏ/(4πμr_e²) | 3 000 Hz | **S−** | 87 465 |
| `SPEC_CO_Rot_Dunham` | \|2B₀ − 4D₀ − ν(1-0)\| | 10 000 Hz | **S+** | 0,028 |
| `SPEC_CO13_Rot_MuRule` | \|B₀·μ/μ′ − B₀′(¹³CO)\| | 12 000 Hz | **S−** | 412 |
| `SPEC_CO_Rot_Kratzer` | \|4B_e³/ω_e² − D₀\| | 70 Hz | **P** | 1,394 |

Sources déclarées : NIST JPCRD 53 (μ, B₀, D₀, ν) ; Huber & Herzberg
1979 via RIOS FHI-MPG (r_e, B_e, α_e) ; CODATA 2018 (ℏ, c, u).

## Ce que les mots disent

**S− à 87 465 θ (ab initio)** — le plus grand écart relatif au seuil de
tout le registre, et le plus nommé : B_e calculé depuis la géométrie
(r_e déclaré, mesure de structure indépendante des raies micro-ondes)
dépasse B₀ mesuré de 262 394 407,38 Hz — ce qui reproduit α_e/2
attendu (262 318 400,75 Hz) à 76 kHz près (0,03 %). Le rotor rigide à
l'équilibre ne prédit pas le niveau v=0 : **l'écart s'appelle α_e**, la
couplage vibration-rotation. S− de dette de modèle pauvre, dans
l'esprit O1 grille → O6 : chaque échec a droit à son levier (ici
déclaré, non encore monté : ajouter α_e/2).

**S+ à 0,028 θ (Dunham)** — le catalogue NIST se transporte lui-même :
2B₀ − 4D₀ reproduit ν(1-0) à 280 Hz, soit 2,8e-6 du budget déclaré.
Calibre du transport de table. Dette écrite : **circularité** — B₀, D₀
et ν issus du même ajustement global ; contrairement au contact ab
initio, ce n'est pas une prédiction indépendante.

## Lecture croisée de la paire

L'entrée r_e (géométrie, H&H 1979) est indépendante des raies micro-ondes
(NIST) : le S− ab initio est donc un vrai test physique (modèle pauvre
nommé par α_e), pendant que le S+ Dunham est un test logistique (la
table est cohérente à hauteur de ses incertitudes). Les deux répondent
à deux questions différentes et leurs mots ne se contredisent pas.

## Dettes écrites

1. **Vintage H&H** : r_e, B_e, α_e arrondis à 6 chiffres (1976/1979) —
   l'écart ~3 MHz entre B_e,calc et B_e(H&H en cm⁻¹) est une dette de
   vintage, pas une erreur de calcul.
2. **Circularité du contact Dunham** (détaillée ci-dessus).
3. **Masse standard** : μ prise pour les isotopes dominants (¹²C, ¹⁶O).

## Prolongements déclarés

- **Isotopologues ¹³CO / C¹⁸O** : B₀ prédite par la règle de la masse
  réduite depuis B₀(¹²CO) — prédiction quasi indépendante (suspense
  réel à évaluer : les effets au-delà de la règle μ sont petits mais
  non nuls à la précision NIST).
- **Levier α_e** du contact ab initio (montée en température du modèle).
- **O₃ ν₃** : rotateur asymétrique, molécule tellurique du front
  HITRAN (répond au fil ozone de l'écosystème ANU).

## Ajout 2026-09-14 : le contact isotopologue (réponse au suspense)

`SPEC_CO13_Rot_MuRule` monté après les deux premiers runs, règle
déclarée avant son run (protocole §3) : **le suspense ne tient pas** —
mot S− à 412 θ, δ = 4 940 938,13 Hz, conforme à l'estimation pré-run
(~4 MHz annoncé). À la précision NIST (10⁻⁷ relative), la règle de la
masse réduite appliquée telle quelle au niveau v=0 échoue : l'écart
nomme la correction isotopique de la vibration-rotation (α_e n'est
pas purement en 1/μ) et les effets au-delà de Born-Oppenheimer. La
leçon est symétrique du contact ab initio : les gestes minimaux ont
chacun une limite précise, et la machine la nomme. Levier déclaré
(non monté) : α_e′ isotopique — absent de la table extraite.
Estimation pré-run vs réalisé : ~4,3 MHz / ~360 θ annoncé, 4,94 MHz /
412 θ réalisé — même ordre, le run a tranché sans surprise.

## Ajout 2026-09-14 : le contact Kratzer (la prédiction croisée — le suspense tient)

`SPEC_CO_Rot_Kratzer` monté sur la clé du chantier : passer de la
comparaison de nombres déclarés à la **prédiction croisée**
D_e = 4B_e³/ω_e², entrées H&H indépendantes de l'ajustement NIST de
D₀. Estimation pré-run honnête : δ ~ 70-80 Hz, δ/θ ~ 1,0-1,1 — zone
P [θ, 2θ] au cheveu, suspense maximal annoncé (P, S+ et S− accessibles
selon les arrondis H&H). Premier run : mot découvert **P**, δ =
97,551447 Hz (1,394 θ) — le suspense tenait, et le run a tranché dans
la bande annoncée. La carte dit : la physique anharmonique gelée
(Kratzer + constantes H&H 1979) **tient au cheveu mais pas dans le
budget** — elle ne reproduit pas D₀ au niveau de son incertitude
moderne (70 Hz) sans échec franc. C'est le pendant exact du S− ¹³CO :
là où la règle μ a une limite nommée (412 θ), la relation de Kratzer
tient au cheveu. Le P nomme le statut de la physique anharmonique :
« tenu mais pas exact » à la précision NIST. Dettes écrites : D_e
(équilibre) pesé contre D₀ (v=0), écart vibrationnel ~0,2 Hz << θ ;
arrondis H&H ; Kratzer = Morse seulement.
