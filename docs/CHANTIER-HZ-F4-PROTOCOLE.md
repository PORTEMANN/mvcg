# Chantier H(z) F4 — protocole gelé (2026-09-14)

**Statut : gelé avant run. Local, non publié.** Dernier contact lourd de
la prospective ( « modulation H(z) par filtrage entropique F4 = 0,035 —
forme de H(z) non spécifiée » ) : la forme est maintenant spécifiée —
elle était en images. Transcription gelée des images du volet V
(22/10/2025), lues le 2026-09-14 sur la publication en ligne.

## La transcription (l'acte curatorial)

| Image | Contenu transcrit |
|---|---|
| image-29 (V) | **H²(z) = H₀² [ Ω_m(1+z)³F₄ + Ω_r(1+z)⁴F₁ + Ω_k(1+z)² + Ω_ΛF_U ]** |
| image-30 (V) | Tableau des plans E1–E7 : N_j, S_j = ln N_j, α_j, β_j, I_{j,0} (E4 : N=2,0·10²⁴, S=55,95, β=0,060, I₀=5) |
| image-31 (V) | **F_j = e^(−β_j·S_j)** ; valeurs publiées : F₁=0,154, F₂=0,601, F₃=0,702, **F₄=0,035**, F₅=0,712, F₆=0,825, F₇=0,673 |
| image-32 (V) | d_L(z) = (1+z) c ∫₀^z dz'/H(z') |
| image-33 (V) | q(z) = −1 − Ḣ/H² |

Cohérence vérifiée à la transcription : les F cités par le texte du
volet V (0,035 cosmologie/neutrinos ; 0,712 QCD ; 0,154/0,601/0,702
neurosciences) coïncident exactement avec e^(−βS) du tableau.

## Population gelée : 2 contacts (PF7–PF8)

### PF7_F4_Recompute — l'arithmétique du tableau des plans

- **μ_loc** : F₄ recompté depuis les paramètres publiés :
  e^(−0,060 × 55,95) = 0,03484.
- **μ_ref** : 0,035 (tableau image-31, cité par le texte).
- **Ce que la machine pèse** : la cohérence arithmétique du jeu
  numérique illustratif (comme PF3) — le tableau est publié comme tel.
- Attendu gelé : **S+** (δ ≈ 0,46 % à θ = 0,10).
- θ = 0,10.

### PF8_Hz_Filtrage_Ecart — la tension équation / revendication

- **Lecture gelée** : l'équation image-29 est prise telle que publiée,
  avec F₄ = 0,035 multipliant directement Ω_m(1+z)³. **F_U n'est chiffré
  nulle part dans le corpus** — dette nommée ici, pas corrigée en
  silence. Valeurs neutres gelées : F_U = 1 (pas de filtrage du vide),
  Ω_k = 0. Conséquence déclarée : la normalisation H²(0) = H₀² n'est
  pas tenue (H²(0)/H₀² = 0,035·Ω_m + F₁·Ω_r + Ω_Λ ≈ 0,696) — c'est une
  information du contact.
- **μ_loc** : écart relatif max |H_filtree − H_LCDM|/H_LCDM sur
  z ∈ [0 ; 2,1] (plage Pantheon+ des contacts H0_Hz_SNe de la machine),
  H₀ se canelant dans le rapport.
- **μ_ref** : 0,02 — la borne du texte : « variation <2 % sur H(z)
  difficile à distinguer sans méga-surveys ».
- **Ce que la machine pèse** : la tension entre l'équation publiée
  (frein ×0,035 sur la matière) et la déclaration d'un effet <2 %.
  Calcul préparatoire du protocole : l'écart vaut déjà ~16,6 % à z = 0
  et croît jusqu'à ~68 % à z = 2,1 — la borne <2 % est dépassée dès
  z = 0 sous la lecture gelée.
- Attendu gelé : **S−**.
- θ = 0,10 (la revendication est quantitative : une borne de variation).

## Règles

- 3 tables gelées datées (2 × LITTERATURE-2025, 1 × DECLARED-2026) ;
  sha256 tracés par load_table ; zéro fetch dans la machine.
- Pas de moyenne entre contacts ; chaque verdict se lit seul.
- La lecture F_U = 1 est gelée et portée par le protocole : une autre
  lecture (ex. renormalisation imposant H(0) = H₀, qui fixerait
  F_U ≈ 1,44) serait un autre contact, à monter séparément si l'un
  le demande.
- Ω_m et Ω_Λ repris du gel existant pf_vide_inputs_DECLARED-2026
  (Planck 2018 déclaré par la machine) — cohérence des déclarations.
