# Chantier PSY-RMN — protocole gelé (2026-09-14)

**Statut : gelé avant run. Local, non publié.** Extension du chantier
PRINCIPES : les deux contacts que la prospective classait « non pesables
(équations perdues en images) » deviennent pesables par transcription
gelée des images d'équations du volet I (17/06/2025) et de la déclaration
de vitesse du volet III (28/07/2025).

## Principe de transcription

Les articles publient leurs équations comme images PNG. La transcription
est un acte curatorial daté : chaque table gelée cite l'image transcrite
(image-NN.png du volet I, lue le 2026-09-14), la formule en clair et la
phrase du texte qui l'entoure. Figer le fichier ; changer la
transcription = autre D. Zéro pointeur automatique vers l'archive : les
tables citent les volets par date, comme Lundeen-Pipkin.

## Population gelée : 2 contacts (PF5–PF6)

### PF5_Psy_Energie — la cohérence de l'unité psy (volet I)

- **Transcription image-94** : « 1 psy = ħ_N ; ħ_N = (1,054 × 10⁻³⁴)
  J·s (constante noétique) » + échelle millipsy/kilopsy/mégapsy.
- **Transcription image-95** : « E_noét [J] = N_psy · ħ_N / Δt ».
- **Affirmation texte (volet I)** : « Une intention de 500 psy durant
  1 seconde libère 5,25·10⁻³¹ J ».
- **μ_loc** : recompute de l'exemple avec la constante de l'équation :
  E = 500 × 1,054·10⁻³⁴ / 1 = 5,27·10⁻³² J.
- **μ_ref** : 5,25·10⁻³¹ J (affirmation publiée).
- **Ce que la machine pèse** : la cohérence interne entre l'équation-image
  (10⁻³⁴) et l'exemple-texte (10⁻³³) — un écart structurel d'un facteur
  10, pas une imprécision. Attendu gelé : **S−** (le texte est cohérent
  avec ħ_N = 1,054·10⁻³³ J·s, l'image avec 10⁻³⁴ ; les deux sont publiés).
- θ = 0,10 (cohérence interne, barre des contacts PF2/PF3).

### PF6_RMN_DeltaB — la prédiction RMN des ANU (volet I × III)

- **Transcription image-61** : « ΔB = (m_e c / (g e)) · (c_éth k /
  √(a² + b²)) » (prédiction de pics de résonance RMN paramagnétique).
- **Transcription image-63** (tableau des paramètres clés) : a = 1,5·10⁻¹⁸ m
  (rayon moyen) ; b = 0,7a (amplitude) ; k = 3 (base) ; ω_k = 10¹⁸ rad/s ;
  E_courb = 10⁻³³ J.
- **Texte volet I** : « Pour k=3, ΔB = 0,5 mT (environ), détectable en
  RMN haute résolution » ; « g (=2 environ) est le facteur de Landé ».
- **Déclaration volet III** : « c_N = 10⁹ c, la vitesse noétique qui
  explique la synchronisation neuronale instantanée (EEG à 40 Hz) ».
- **Identification déclarée dans ce protocole (gelée)** : c_éth (formule
  du volet I) ≡ c_N (volet III) — c'est l'unique vitesse noétique chiffrée
  du corpus. Sans cette identification, la prédiction n'est pas
  recomputable ; avec elle, elle l'est. La portée de l'hypothèse est
  écrite ici, pas cachée dans le code.
- **μ_loc** : ΔB recomputée depuis la formule transcrite, paramètres
  gelés, m_e/e gelés CODATA-2018 (table DECLARED-2026), c_éth = 10⁹ c.
- **μ_ref** : 5·10⁻⁴ T (0,5 mT, affirmation publiée).
- **extra** : c_éth requis pour que la prédiction tienne (déduction
  inverse, information) ; ΔB si c_éth = c (mémoire).
- **Attendu gelé** : **S−** — sous l'identification déclarée, la formule
  transcrite ne produit pas 0,5 mT. Le verdict pèse la recomputableité
  de la prédiction sous les déclarations du corpus, pas la physique des
  ANU (qui n'a pas de statut dans la machine).
- θ = 0,10 (prédiction expérimentale quantitative, barre de la série P).

## Règles

- 4 tables gelées datées (3 × LITTERATURE-2025, 1 × DECLARED-2026) ;
  sha256 tracés par load_table.
- Runners déterministes dans principes.py ; zéro fetch réseau dans la
  machine (la transcription est figée dans les tables).
- Pas de moyenne entre contacts ; chaque verdict se lit seul.
- Les erreurs de transcription éventuelles ne se corrigent pas en
  silence : elles se réécrivent en amendement daté (autre D).

## Conséquence cartographique (déclarée)

PF6 porte un δ/θ d'environ 10³⁶ — hors échelle de la carte principale.
Règle d'affichage ajoutée et datée dans carte.py : les ordonnées sont
bornées à Y_MAX = 5·10² (le haut des bandes de la règle) ; un point au-
delà est tracé sur la ligne du bord, sa valeur exacte restant dans le
registre et les fibres. La carte reste dérivée : la borne touche
l'affichage, jamais le verdict ni le δ.
