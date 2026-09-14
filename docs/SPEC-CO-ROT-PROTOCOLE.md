# SPEC — CO rotationnel : protocole du chantier (écrit AVANT tout run)

**Date de gel : 2026-09-14.** Chantier : ouvrir le rotationnel (la fibre cm⁻¹ ne
pèse que des oscillateurs 1D) avec ¹²C¹⁶O X¹Σ⁺, la molécule de référence de
l'astrochimie millimétrique (calibrateur ALMA).

## Sources déclarées (tables vintage, jamais choisies après coup)

- **NIST JPCRD 53** (Microwave Spectral Tables, refit CDMS) :
  μ = 6,85620871(6) u ; B₀ = 57 635,969(3) MHz ; D₀ = 183,57(7) kHz ;
  ν(1-0) = 115 271,204(10) MHz.
- **Huber & Herzberg 1979** (via base RIOS/FHI-MPG, API interrogée le
  2026-09-14) : r_e = 1,128323 Å ; B_e = 1,93128 cm⁻¹ ; α_e = 0,0175 cm⁻¹.
- **CODATA 2018** : ℏ = 1,054571817e-34 J·s (exacte) ; c = 299792458 m/s
  (exacte) ; u = 1,66053906660e-27 kg.

## Deux contacts déclarés (expected=None, mots inconnus au gel)

### 1. SPEC_CO_Rot_AbInitio — « le rotor rigide à l'équilibre »

- Règle gelée : μ_loc = |B_e,calc − B₀,obs| en Hz, avec
  B_e,calc = ℏ / (4π μ r_e²) (μ en kg depuis NIST, r_e déclaré H&H) ;
  μ_ref = B₀ mesuré NIST.
- θ = 3 000 Hz = u(B₀) déclarée NIST, gelé avant run.
- **Estimation pré-run honnête** : B_e,calc ≈ 57,9 GHz ; B₀ = 57,636 GHz ;
  δ ≈ 265 MHz ≈ α_e/2 (le zéro vibratoire : B₀ = B_e − α_e/2). δ/θ ≈ 9e4
  → **S− attendu SANS suspense**. Leçon attendue : le rotor rigide à
  l'équilibre ne prédit pas le niveau v=0 ; l'écart s'appelle α_e.
  C'est un S− de dette de modèle pauvre (dans l'esprit O1 grille → O6).
- GUM : une ligne B (u = u(B₀) déclarée), decide=theta, k=2.
- Levier déclaré pour plus tard (non monté) : ajouter α_e/2 → B₀ prédit.

### 2. SPEC_CO_Rot_Dunham — « la table se tient-elle elle-même »

- Règle gelée : μ_loc = |ν_pred − ν_obs| en Hz, avec
  ν_pred = 2B₀ − 4D₀ (B₀, D₀ déclarés NIST) ; μ_ref = ν(1-0) NIST.
- θ = 10 000 Hz = u(ν) déclarée NIST, gelé avant run.
- **Estimation pré-run honnête** : ν_pred = 115 271,20372 MHz ;
  δ ≈ 280 Hz, δ/θ ≈ 0,03 → **S+ attendu SANS suspense** : le catalogue est
  interne cohérent à ~3e-6 de son budget déclaré. Leçon attendue : le
  transport (B₀, D₀) → ν ne s'égare pas au-delà du budget.
- **Dette écrite : circularité** — B₀, D₀ et ν viennent du même ajustement
  global ; ce contact calibre le transport de table, ce n'est pas une
  prédiction indépendante (contrairement au contact 1, dont l'entrée r_e
  est une mesure de géométrie indépendante des raies micro-ondes).
- GUM : une ligne B (u = u(ν) déclarée), decide=theta, k=2.

## Dettes du chantier (écrites avant run)

1. **Vintage H&H** : B_e, α_e, r_e arrondis à 6 chiffres (1976/1979) —
   l'écart ~3 MHz entre B_e,calc et B_e(H&H) en cm⁻¹ est une dette de
   vintage, pas une erreur de calcul.
2. **Circularité du contact 2** : constantes d'un même ajustement.
3. Prolongements déclarés : isotopologues ¹³CO/C¹⁸O (règle de la masse
   réduite — prédiction quasi indépendante, suspense réel à évaluer),
   puis O₃ ν₃ (rotateur asymétrique).

## Interdits

Ajuster r_e, μ, B₀, D₀, ν, θ ou les constantes CODATA après le run.
Écrire le mot attendu dans le test avant le premier run (garde
anti-tautologie : un test ne porte jamais le mot d'un contact voisin).

## 3. Contact isotopologue SPEC_CO13_Rot_MuRule (ajout 2026-09-14, après
les deux premiers runs — règle déclarée avant SON run)

- Règle gelée : mu_loc = |B0_pred − B0′(mesure)| en Hz, avec
  B0_pred = B0(¹²CO) × μ/μ′ (règle de la masse réduite appliquée
  telle quelle au niveau v=0) ; μ = 6,85620871(6) u, μ′ = 7,17227491(14) u
  (NIST JPCRD 53) ; B0′ mesuré = 55 101,021(12) MHz (NIST JPCRD 53).
  mu_ref = B0′(mesure). θ = 12 000 Hz = u(B0′) déclarée NIST, gelé
  avant run. GUM : une ligne B (u(B0′) déclarée), decide=theta, k=2.
- **Estimation pré-run honnête** : B0_pred ≈ 57 635,969 × 6,85620871 /
  7,17227491 ≈ 55 096,7 MHz ; δ ≈ 4,3 MHz, δ/θ ≈ 360 → **S− attendu
  SANS suspense**. La règle de la masse réduite s'applique rigoureusement
  à B_e, pas à B₀ : l'écart attendu nomme la correction isotopique de la
  vibration-rotation (α_e n'est pas purement en 1/μ) + effets au-delà de
  Born-Oppenheimer. Le suspense porte sur la taille de l'écart, pas sur
  le mot.
- Levier déclaré (non monté) : B₀′ prédit avec α_e′ isotopique — α_e′
  n'est pas dans la table extraite (dette écrite).
- Dette : μ′ et B₀′ extraits de la même table NIST JPCRD 53 (validation
  croisée interne, pas indépendance d'ajustement).

## 4. Contact SPEC_CO_Rot_Kratzer (ajout 2026-09-14 — la prédiction
## croisée, règle déclarée avant SON run)

- Règle gelée : mu_loc = |D_e,calc − D₀,obs| en Hz, avec la relation de
  Kratzer pour l'oscillateur de Morse : D_e = 4·B_e³/ω_e². Entrées
  déclarées : B_e = 1,93128 cm⁻¹ et ω_e = 2169,81538 cm⁻¹ (Huber &
  Herzberg 1979 via RIOS — INDÉPENDANTS de l'ajustement NIST de D₀).
  mu_ref = D₀ mesuré = 183,57(7) kHz (NIST JPCRD 53). θ = 70 Hz =
  u(D₀) déclarée NIST, gelé avant run. GUM : une ligne B (u(D₀)
  déclarée), decide=theta, k=2.
- **Estimation pré-run honnête** : D_e,calc = 4×1,93128³/2169,81538²
  ≈ 6,120e-6 cm⁻¹ ≈ 183,6 kHz ; δ ≈ 70–80 Hz ; δ/θ ≈ 1,0–1,1 — zone
  **P [θ, 2θ] au cheveu** : SUSPENSE MAXIMAL. Le mot est réellement
  inconnu : P, S+ et S− sont tous accessibles selon les arrondis H&H
  (dette de vintage). C'est le premier contact SPEC à suspense, et le
  pendant du S− ¹³CO : là où la règle μ échoue à 412 θ, la relation
  anharmonique de Kratzer teste si la physique tient au niveau 10⁻⁴.
- Dettes écrites : (a) D_e théorique (Kratzer, équilibre) pesé contre
  D₀ mesuré (v=0) — l'écart vibrationnel de D est ~10⁻³ rel (~0,2 Hz),
  négligeable devant θ, mais écrit ; (b) B_e et ω_e arrondis H&H
  6 chiffres — la propagation de ces arrondis produit l'écart attendu,
  pas une erreur de calcul ; (c) Kratzer est exact pour le potentiel de
  Morse seulement — CO s'en écarte légèrement.
- Interdit : ajuster B_e, ω_e, D₀ ou θ après le run. Le mot découvert
  est figé tel quel, quel qu'il soit.
