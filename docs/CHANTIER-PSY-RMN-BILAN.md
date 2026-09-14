# Chantier PSY-RMN — bilan (2026-09-14)

**Statut : local, non publié.** Protocole gelé avant run :
`docs/CHANTIER-PSY-RMN-PROTOCOLE.md`. Suite du chantier PRINCIPES :
les deux contacts que la prospective classait « non pesables (équations
perdues en images) » sont pesés par transcription gelée des images
d'équations des volets I (17/06/2025) et III (28/07/2025), lues le
2026-09-14 sur la publication en ligne (les images PNG des équations
ont été transcrites une à une, chacune citée dans sa table).

## La transcription (l'acte curatorial du chantier)

| Image | Contenu transcrit |
|---|---|
| image-94 (I) | 1 psy = ħ_N ; **ħ_N = 1,054 × 10⁻³⁴ J·s** (constante noétique) ; échelle millipsy/kilopsy/mégapsy |
| image-95 (I) | E_noét [J] = N_psy · ħ_N / Δt |
| image-61 (I) | ΔB = (m_e c / (g e)) · (c_éth k / √(a² + b²)) |
| image-63 (I) | a = 1,5·10⁻¹⁸ m ; b = 0,7a ; k = 3 (base) ; ω_k = 10¹⁸ rad/s ; E_courb = 10⁻³³ J |
| texte (III) | c_N = 10⁹ c, « la vitesse noétique qui explique la synchronisation neuronale instantanée » |

Les images 90 (dérivation dimensionnelle de η), 92 (correction V_c),
93 (seuil η_c ≈ 10¹⁵ bits/m³), 96 (u_N = ⟨Â²⟩/2χ, χ = 5,2·10⁻⁴² J⁻¹·m³),
97 (P_N = u_N/3 + (κ/V)(∂S_N/∂V)_T) sont transcrites en annexe du
protocole pour mémoire — pas de contact dérivable seul (déclarations
sans affirmation chiffrée à recomputer).

## Population gelée : 2 contacts (PF5–PF6) — deux S− attendus, deux S− tenus

| Contact | Pesée | μ_loc | μ_ref | Mot |
|---|---|---|---|---|
| PF5_Psy_Energie | E = 500 psy × 1,054·10⁻³⁴ / 1 s | 5,27·10⁻³² J | 5,25·10⁻³¹ J | **S−** à 9,0 θ |
| PF6_RMN_DeltaB | ΔB recomputée, c_éth = c_N = 10⁹ c | 4,19·10³² T | 5·10⁻⁴ T | **S−** à 8,4·10³⁵ θ |

Bilan du chantier : **0 S+, 0 P, 2 S−**. Nouvelles fibres (si, J) et
(si, T). Registre : 78 → 80 contacts, 16 fibres.

## Lecture des verdicts

**PF5 (S−) — la dette interne du volet I.** L'équation-image pose
ħ_N = 1,054·10⁻³⁴ J·s ; l'exemple-texte affirme que 500 psy pendant
1 s « libèrent 5,25·10⁻³¹ J » — ce qui est exactement cohérent avec
ħ_N = 1,054·10⁻³³ J·s. L'image et le texte du **même volet** se
contredisent d'un facteur 10. La machine ne choisit pas : elle recompte
avec la constante de l'équation et pèse l'écart — 90 %, S−. La constante
implicite du texte (1,05·10⁻³³ J·s) est consignée en extra. C'est la
première fois que la machine pèse une contradiction *interne à un seul
document* (PF2 pesait un croisement entre deux volets).

**PF6 (S−) — la prédiction qui n'est pas recomputable sous ses propres
déclarations.** La formule transcrite demande c_éth, jamais chiffrée
dans le volet I. L'unique vitesse noétique chiffrée du corpus est
c_N = 10⁹ c (volet III) — identification déclarée dans le protocole,
avec sa portée écrite. Sous cette identification : ΔB = 4,19·10³² T
contre 0,5 mT revendiqué (écart ~10³⁶). En déduction inverse, la
revendication ne tient que pour c_éth ≈ 3,58·10⁻¹⁹ m/s — une vitesse
que le corpus ne déclare nulle part. Le verdict pèse la recomputableité
de la prédiction sous les déclarations du corpus ; il ne dit rien des
ANU. Note de lecture : le volet V qualifie lui-même c_N de « solution
ad hoc et problématique » — le corpus contient sa propre mise en
garde, la machine la chiffre.

## Verrous techniques

- 4 tables gelées (3 × LITTERATURE-2025, 1 × DECLARED-2026) ; sha256
  tracés. La transcription elle-même est figée : la corriger = autre D.
- `Contact.u_doc` (nouveau champ, 2026-09-14) : dictionnaire d'unités
  déclaré du contact. PF6 est le premier contact (si, T) — le home
  check exigeait ε0/μ0 déclarés pour SI + grandeur EM, que le balayage
  fournit via SI_VACUUM : l'incohérence home-kill / sweep-ok est levée
  par la déclaration, sans relâcher le garde-fou pour les autres.
- `carte.py` : borne d'affichage Y_MAX = 5·10² déclarée et datée (le
  δ/θ de PF6, ~8,4·10³⁶, ecraserait l'échelle log) ; un point au-delà
  est tracé sur la ligne du bord. L'affichage seul est borné — verdict,
  δ et position dans la zone (test_carte_position, inchangé) ne bougent
  pas.
- Suite complète verte après intégration : **293 tests, 0 failure**
  (compteurs 78→80, fibres 14→16, 6 verrous nouveaux dans
  test_principes.py).

## Portée et limites

- La transcription est un acte humain daté ; la machine ne fetch rien.
  Une erreur de transcription se corrige en amendement daté, jamais en
  silence.
- g = 2 « environ » et « 0,5 mT (environ) » sont gelés tels que publiés ;
  le caractère approximatif des revendications fait partie de ce qui est
  pesé.
- Suite ouverte : PF1b (2-boucles si coefficients gelés), H(z) F4,
  et les contacts C1–C3 de la prospective (faible intérêt déclaré).
