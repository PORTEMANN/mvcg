# Famille B — suite H0 : campagnes B1-B3 (local, 2026-09-14)

Dérivées de campagne : aucun contact créé, aucun gel touché (mots
S−/S− inchangés). Les trois pistes ouvertes du bilan (§6) sont
traitées ; la quatrième (V2 déclarative, ancrage MU_SH0ES) reste un
chantier de contacts, non une campagne — il attend une décision de
doctrine.

Scripts : `campagnes_b1_ps1md_zoom.py`, `campagnes_b2_cfa4p3_retest.py`,
`campagnes_b3_cov_petit_effectif.py`. mu_pred est utilisé en forme
close (mu = 5 log10 K(z) − 5 log10 H0 + 25), vérifiée contre la forme
historique à 1e-12.

## B1 — zoom PS1MD : un offset survey, pas un artefact de sous-groupe

Reproduction exacte de la campagne 9 : **+0,0284 ± 0,0139 (2,04 σ)**
sur les 20 LC PS1MD de la sélection HF.

- **Découpes internes** (z, FITPROB, HOST_LOGMASS, x1, c) : aucune
  moitié ne porte l'offset seule ; signal maximal côté x1 > 0,297
  (+0,040, 2,7 σ) — légèrement plus marqué pour les courbes larges,
  mais le bas-x1 reste positif (+0,019). Uniforme, pas dichotomique.
- **Leave-one-out intra-PS1MD** : aucun LC ne pilote — retirer le
  pire (+0,147) ne fait tomber l'offset qu'à +0,022. Signal collectif
  sur ~20 LC.
- **Diagnostic hors sélection** (déclaré, aucun mot n'en dépend) :
  les 249 PS1MD non-HF portent **+0,0183 ± 0,0090 (2,04 σ)**, même
  signe — l'offset est un fait de survey, dans ET hors sélection HF.
- **Levier** : retirer PS1MD déplace H0* de 73,35 à **73,90** (+0,55)
  — le plus gros levier survey unique du bas-z. À cote : FOUND porte
  le χ² (campagne 9), PS1MD porte la POSITION.

## B2 — paire CFA4p3 : signal confirmé, pas élevé

- Les 2 LC HF : **2010ag +0,0897 (FITPROB 2,3e-12)** et **2010dt
  +0,0779 (FITPROB 0,086)** — l'offset de paire (+0,0838) est *partagé*
  par les deux membres : l'hypothèse « porté par le FITPROB
  pathologique » n'est **pas** confirmée.
- Les 10 non-HF (z < 0,022) : +0,064 ± 0,067 — même signe,
  non conclusif seuls. (2010ai : +0,585, FITPROB = 1 — outlier isolé.)
- **Dette écrite** : la sélection HF officielle inclut 2010ag dont
  l'ajustement de courbe de lumière a FITPROB = 2,3e-12. Ni la paire
  (n = 2, deux fits douteux) ni les 10 exclues ne permettent de
  trancher « offset survey CFA4p3 » vs « deux mauvais fits d'accord
  par hasard ». Le signal reste CE QU'IL ÉTAIT : à confirmer par
  relevé d'origine (CfA), impossible en local.

## B3 — haut-z : le blanchiment est une fluctuation, pas une covariance
##     surestimée

- Reproduction exacte de la campagne 10 : χ²/ndof = **0,449** (66 LC
  haut-z, 8 bins, H0* = 73,34).
- Bootstrap paramétrique (2000 pseudo-jeux sous le modèle + covariance
  publiée, seed 20260914 gelé) : E[χ²/ndof] = **0,984** — la
  covariance binnée est calibrée en moyenne ; quantiles 5/50/95 %
  = 0,320 / 0,893 / 1,957.
- **p(χ²/ndof ≤ 0,449) = 0,131** : l'écart est une fluctuation à ndof
  faible (quantile 13 %), **pas** une preuve de surestimation de
  covariance à petit effectif. La piste (a) du bilan est fermée.
- Rappel honnête : le bootstrap teste la calibration INTERNE (modèle +
  covariance gelés) ; il ne peut pas juger la covariance publiée
  elle-même.

## Ce que la famille B change au bilan

1. **PS1MD passe de « signal isolé » à « fait survey documenté »** :
  uniforme en interne, présent hors sélection HF, plus gros levier de
   position (+0,55 sur H0*). Reste un diagnostic (campagne dérivée),
  pas un contact.
2. **CFA4p3** : signal confirmé mais non élevé ; la dette FITPROB de
  2010ag est écrite au registre du chantier.
3. **Le blanchiment haut-z n'est pas un artefact de covariance** :
  la dette bas-z reste un phénomène bas-z réel (dispersion), pas une
  illusion statistique du haut-z.
4. La **V2 (ancrage MU_SH0ES)** reste la seule piste ouverte — c'est
  une décision de doctrine (nouveau contact), pas une campagne.
