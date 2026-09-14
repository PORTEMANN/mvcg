# CAMPAGNE A3 — 5ᵉ paquet : unités naturelles ℏ = c = 1 (prototype local, 2026-09-14)

Question du catalogue : l'invariance des verdicts tient-elle hors
HL/Gauss/SI/1 ? Réponse : **46/46 licites, 46/46 mots identiques** —
et la raison est architecturale, pas empirique.

Script : `campagne_a3_unites_naturelles.py` (résultat :
`a3_unites_naturelles.json`). Campagne dérivée : aucun contact
nouveau, aucun gel touché, **zéro modification du cœur** (PACKETS
intact, gels « 4 paquets » des tests inchangés).

## 1. La sonde

Les unités naturelles ne sont pas enregistrées comme 5ᵉ paquet : la
sonde est un `UnitSystem` existant (`packet="hl"`, `hbar=1`, `c=1`,
vintage `nat-A3-2026-09-14` déclaré). Les unités naturelles sont un
membre déclaré de la famille HL — pas une extension du registre des
paquets. Ajouter `"nat"` à `PACKETS` changerait les balayages existants
(5 lignes au lieu de 4) et casserait les gels : interdit.

## 2. Les 12 dimensions en puissances de l'eV

| Dimension | Expression naturelle | Convention |
|---|---|---|
| eV | eV | dimension native |
| Ha | eV (× 27,2114) | Hartree = énergie atomique |
| cm⁻¹ | eV (× hc) | nombre d'onde → énergie |
| D | e·eV⁻¹ | dipôle = charge × longueur |
| Hz | eV (× h) | fréquence → énergie |
| m/s | 1 | vitesse = 1/c, sans dimension |
| nK | eV (× k_B) | température → énergie |
| µm | eV⁻¹ | longueur = 1/énergie |
| J m⁻³ K⁻² | eV⁴ | γ = densité d'énergie / T² |
| mag | 1 | rapport logarithmique |
| 1, 1e-11 | 1 | sans dimension |

Subtilité EM consignée : le Debye devient e·eV⁻¹ — **la convention EM
n'est pas supprimée par les unités naturelles, elle est déplacée** (la
charge s'écrit √4πα). La campagne note la subtilité, ne la résout pas :
c'est la dette que porte toute comparaison dipolaire, dans tous les
systèmes.

## 3. Le résultat et sa vraie nature

46/46 mots identiques au home. Ce résultat ne pouvait pas être
autrement : **le paquet n'entre jamais dans l'arithmétique de la
machine**. Les μ sont gelés, le δ est recomputé à l'identique, la
re-décision au seuil calibré rend le mot home. Le paquet vit dans la
garde de dimension (parse_units, conventions EM) — pas dans le calcul.

L'invariance est donc en deux étages, chacun vérifié séparément :

1. **l'arithmétique est propre** — campagne A2 : float64 vs decimal 30
   chiffres, ≤ 5,6e−17, ~16 ordres sous la marge la plus mince ;
2. **la garde généralise** — campagne A3 : le 5ᵉ système accepte les 12
   dimensions du registre, aucun mot ne bouge.

Une conséquence honnête pour la doctrine : le balayage multi-paquets ne
« teste » pas l'invariance des verdicts (elle tient par construction) —
il teste la **licité dimensionnelle** des contacts sous chaque système
de conventions. C'est la garde EM (usurpation HL/SI, ε₀/μ₀ exigés) que
le balayage vérifie réellement, et c'est déjà utile.

## Limites

1. `NAT_MAP` est déclarée dans le script, non gelée — une convention
   d'exploration, pas un standard de la machine.
2. La conversion des μ entre systèmes (ex. eV → eV⁻¹ pour µm) n'est
   pas faite : μ gelés, la machine ne convertit pas, elle compare des
   déclarations. Toute conversion réelle resterait une dette à écrire.
3. Campagne locale : non commitée à ce stade ; publication = décision
   indépendante.
