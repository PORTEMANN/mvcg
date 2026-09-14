# Protocole gelé — Contacts affinés « les quatre P » (D-bump)

**Gelé avant run — 2026-09-14.** Mot inconnu au gel pour chacun des quatre contacts.
Réponse à la directive « attaque les quatre P / affiner la mesure » : la machine
re-pèse quatre contacts déjà publiés en ne changeant **que les déclarations
d'incertitude** (D-bump). Aucun runner modifié, aucune table modifiée : les
versions affinées partagent le runner et le sha256 de leur contact d'origine.
C'est l'honnêteté du geste : seule la métrologie change, pas le transport.

## Principe

| contact affiné | contact d'origine | runner partagé | ce qui change |
|---|---|---|---|
| O19_CO2_nu3_Fine | O2_CO2_nu3 | o2_co2_nu3 | theta 0.10 (tol. labo) → u_delta GUM |
| O20_Carbon_D_Raman_Fine | O3_Carbon_D_Raman | o3_carbon_d_raman | idem |
| SPEC_CO_Rot_Kratzer_Fine | SPEC_CO_Rot_Kratzer | co_rot_kratzer | u(D0) 70 Hz → u_delta GUM déclaré |
| P31_Lamb_Mohr_K2 | P31_Lamb_Mohr | p31_lamb_mohr | couverture k=1 → k=2 |

## 1. O19_CO2_nu3_Fine (micro, ("1","cm^-1"), abs)

- s : nu3(CO2) VFF a k transferee de CO = bande IR observee (12CO2) — même
  transport que O2, comparaison posée en cm^-1 (delta_kind abs, déclaré).
- GUM : decide=U, k=1, lignes B : nu_pred_VFF u=0.1 cm^-1 ; nu3_obs u=0.1 cm^-1
  (dispersion déclarée, bande rotation-vibration fine sous le paquet nu3).
  theta = u_delta = sqrt(2)*0.1 = 0.1414213562373095 cm^-1.
- mu_ref = 2349.3 (inchangé). Estimation pré-run honnête : mu_loc = 2009.2147805263908
  (runner inchangé), delta = 340.085 cm^-1, ratio delta/theta ~ 2405 → **S- attendu
  SANS suspense**. Le P grossier d'O2 (theta=0.10 rel) cachait une dette de
  modèle : le VFF 1D a k transférée de CO ne reproduit pas le paquet nu3 du CO2
  (coupure des modes, Fermi résonance avec 2*nu2). Affiner ne « change » pas la
  physique, il la nomme.

## 2. O20_Carbon_D_Raman_Fine (micro, ("1","cm^-1"), abs)

- s : bande D(graphite) = bande G / sqrt(2) (chaine 1D k2=k1) = bande D observee —
  même transport que O3, comparaison en cm^-1 (abs, déclaré).
- GUM : decide=U, k=1, lignes B : D_pred u(G)=0.5 → 0.5/sqrt(2) = 0.3535533905932738
  (dispersion déclarée sur G) ; D_obs u=5.0 (bande de défaut, dispersion
  inter-échantillons déclarée). theta = u_delta = 5.0124844139408555 cm^-1.
- mu_ref = 1350.0. Estimation pré-run : mu_loc = 1117.228714274745, delta = 232.771
  cm^-1, ratio ~ 46.4 → **S- attendu SANS suspense**. Dette nommée : la chaîne 1D
  égale ne porte pas la physique de la bande D (relaxation de la règle de
  sélection par défauts, double résonance).

## 3. SPEC_CO_Rot_Kratzer_Fine (meso, ("si","Hz"), abs)

- s : 4*B_e^3/omega_e^2 (Kratzer, entrees H&H) = D0 (mesure NIST) — même transport.
- GUM : decide=U, k=1, lignes B : De_pred_HH u=1.0 Hz (bornes prudentes déclarées
  sur les entrées H&H arrondies — PAS des chiffres NIST) ; D0_obs u=5.0 Hz
  (dispersion déclarée). theta = u_delta = 5.0990195135927845 Hz.
- mu_ref = 0.0 (le runner retourne D0 prédit en Hz, comparaison directe).
  Estimation pré-run : mu_loc = 97.55144740839023, delta = 97.551 Hz,
  ratio ~ 19.1 → **S- attendu SANS suspense**. Le P au cheveu du contact grossier
  (theta=70 Hz, ratio 1,39) fondait sur une u(D0) trop étroite ; la dette
  nommée est vibrationnelle : Kratzer relie des constantes d'équilibre
  (B_e, omega_e), D0 mesuré est v=0 — l'écart ~0,05 % est la correction
  vibrationnelle attendue.

## 4. P31_Lamb_Mohr_K2 (micro, ("si","MHz"), abs)

- s : Lamb(QED Mohr, annees 1970) = Lamb(mesure Lundeen-Pipkin 1981) — même
  transport, même témoin, mêmes lignes GUM que P31_Lamb_Mohr.
- GUM : decide=U, **k=2** (couverture standard GUM 95 %, justifié comme contact
  de couverture — pendant de la tare de lecture O18). uc inchangé =
  0.016643316977093238 MHz ; theta = uc ; U(k=2) = 0.033286633954186476 MHz.
- Estimation pré-run : delta = 0.019000000000005457 MHz, ratio delta/U ~ 0.571
  → **S+ attendu**, avec la trace écrite : le mot dépend de la couverture —
  à k=1 le même écart est P (1,14 uc). La dette vintage Mohr est à ~1 sigma,
  compatible au seuil 95 %. Suspense : faible sur le mot, réel sur la leçon.

## Lecture d'ensemble (gelée avant run)

Affiner révèle : deux dettes de modèle (O19, O20 → S-), une dette vibrationnelle
(Kratzer → S-), une compatibilité statistique dépendante du niveau de couverture
(Mohr_K2 → S+ attendu). Ce n'est pas un bilan négatif : c'est la machine qui,
en resserrant la demande de preuve, sépare la dette de modèle du bruit de
laboratoire. Les contacts grossiers (P) restent publiés et inchangés : la
mémoire de la machine est la somme des verdicts, pas le dernier.

## Anti-fraude (gelée avant run)

- Les quatre contacts affinés partagent le runner et le sha256 de leur original :
  test bit-à-bit mu_loc affiné == mu_loc original.
- Les mots ne sont connus qu'après run ; toute divergence entre mot attendu et
  mot découvert sera consignée, jamais corrigée en silence.
