# CAMPAGNE MARGE — l'épaisseur de chaque verdict (prototype local, 2026-09-14)

Campagne dérivée du registre : aucun contact nouveau, aucun gel touché,
aucune donnée nouvelle. La question : **à quelle distance de sa frontière
chaque verdict tient-il ?** Un mot au cheveu n'est pas un mot fragile
par nature — mais il faut le savoir au cheveu, et de combien.

## Définition

Règle de verdict de la machine (`_adc`) : δ ≤ thr → S+ ; thr < δ ≤ 2·thr
→ P ; δ > 2·thr → S−, avec thr = θ (`decide=theta`) ou U = k·u_c
(`decide=U`).

La **marge** est la distance positive à la frontière de bascule :

- S+ : marge = thr − δ (montée en P à δ = thr)
- P : marge = min(δ − thr, 2·thr − δ) (frontière la plus proche, des deux côtés)
- S− : marge = δ − 2·thr (redescente en P à δ = 2·thr)

Exprimée en deux unités :

- **marge(thr)** : en fractions du seuil de décision — universel, les
  46 contacts la portent ;
- **marge(σ)** : en u_c GUM gelé — là seulement où un budget d'incertitude
  est déclaré (9 contacts). C'est l'épaisseur face à une réanalyse qui
  remonterait les incertitudes déclarées sans toucher au protocole.

Script : `campagne_marge_verdicts.py` (résultat : `marge_verdicts.json`).
La définition de la marge vit désormais dans le cœur (`metrics.marge_adc`,
à côté de `_adc`) — la carte et la campagne partagent la même règle.
Convention de signe corrigée au premier run (distances P négatives) —
la définition ci-dessus est la seule valable.

**Couche cartographique (14/09, après le run)** : `carte.py` encode la
marge en σ partout où un budget GUM est gelé — taille des pastilles sur
la carte principale (pastille fine = verdict mince), case pâlie vers le
blanc sur la carte d'identité. Sans budget : taille/opacité neutres, la
couche ne montre que ce qui est déclaré. Cartes régénérées (46 verdicts),
suite complète 203 tests OK, déterminisme inchangé.

## Le tableau des σ — les verdicts les plus minces du registre

Tri par marge(σ) croissante (contacts à budget GUM déclaré) :

| Contact | Mot | δ/U | marge(σ) | Lecture |
|---|---|---|---|---|
| CKM unitarité | P | 1,143 | **0,29** | Le plus mince du registre : 0,29σ du S+. Coherent avec la divergence home/sweep (P maison / S− balayage) — le mot vit dans le chemin de conversion. |
| AMU Δ WP25 | S+ | 0,603 | **0,40** | Le S+ célèbre est mince : à 0,4σ du P. Un budget lattice révisé à la hausse le fait basculer. |
| HLbL lattice vs pheno | S+ | 0,763 | **0,47** | Même famille : S+ de 0,47σ. La divergence home/sweep le renvoyait déjà P sous balayage. |
| H(z) LIT Planck | S− | 2,522 | **0,52** | S− à 0,52σ du retour P : mince *vis-à-vis de son θ calibré*. |
| HVP LO lattice vs e+e− | P | 1,378 | **0,76** | P à 0,76σ de la frontière la plus proche. |
| H0 Écart | P | — | **0,95** du S− | Exposition asymétrique confirmée (campagne 2 : frontière +1,1σ SH0ES) : à 1σ du S−, à ~4σ du S+. |
| H(z) DEMO | S− | 2,345 | 0,35 | Le plus mince en σ — mais la dette est de nature (table synthétique de validation). |
| H(z) LIT SH0ES | S− | 8,395 | 6,39 | Épais — le miroir SH0ES ne repasse pas P sans révision majeure. |
| H1s Rydberg | S+ | 0,000 | 2,00 | Identité exacte, marge = U entier (k = 2). |

## Le tableau des θ — dette structurelle vs verdict de frontière

Tri par marge(thr) (tous contacts) :

- **S− de frontière** (marge < 0,05 θ) : O1 Grille H1s (0,0018), H1s
  vintage 13,6 (4e-4), O4_TK à 3 nm (0,022), Bertsch (0,021). Un
  raffinement déclaré modeste les renvoie P — *ce sont des verdicts de
  progression, pas des condamnations*.
- **S− structurels** (marge ≥ 0,8 θ) : KSS ⁴He (7,6), P30 gaussien, P35
  spike, FRW baryons, dés atlas (0,87-0,90). Aucune réanalyse honnête
  ne les blanchit — *c'est là que le S− est une mesure, pas une étape*.
- **S+ de frontière** : O6 grille raffinée (marge 6e-5 θ), O11 healing
  (0,010). Le geste juste tient, mais de justesse — le progrès se lira
  sur ces marges.
- **Identités exactes** (δ = 0) : marge(thr) = thr entier — robustesse
  maximale par construction (table vs même table), écart = 0 à noter
  comme dette quasi-tautologique déjà assumée au gel.

## Lecture croisée avec la campagne 8 (H(z))

Apparente tension, en réalité deux axes orthogonaux :

- **marge(σ)** mesure la sensibilité à la *calibration* (θ, incertitudes
  déclarées des bins) : les S− H(z) y sont minces (0,35-0,52σ).
- **Δχ² ≈ 21** de la campagne 8 mesure la robustesse à l'*adversaire de
  forme* (refit 2-paramètres) : les mêmes S− y sont épais.

Les deux sont vraies ensemble : les S− H(z) résistent à un adversaire qui
déforme la courbe, pas à une révision du bruit déclaré. C'est une
propriété, pas une contradiction — à écrire au bilan.

## Limites de la campagne

1. **marge(σ) n'existe que pour 9 contacts** — les budgets GUM déclarés
   sont l'exception, pas la règle. Étendre : chaque contact gagnerait un
   budget minimal (au moins la ligne de répétabilité) — chantier à
   trancher séparément.
2. **La marge mesure la distance, pas la probabilité** : une réanalyse
   future n'est pas obligée de bouger de σ entiers. La marge est un
   classement d'exposition, pas une p-value.
3. **Les identités exactes polluent le tri par marge(thr)** (δ = 0 en
   tête) — le tri par σ ou par δ/thr est plus informatif.
4. Campagne locale : non commitée à ce stade ; la décision de
   publication est indépendante.
