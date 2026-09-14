# H0 bas-z — le contact complet (DEMO) : H(z) déclarée contre les bins SNe

Contact **ouvert**, exploration locale du chantier H0 (2026-09-13),
non publié. Promouvoit l'étiquette `H0_Hz_SNe` du casier en carte
pesée — première promotion d'un candidat « sans μ » de l'histoire de
la machine.

## Chronologie du gel

1. **Protocole écrit avant toute exécution** : règle déclarée —
   μ_loc = rms des résidus μ_pred(zᵢ ; H(z) fabrication **Planck
   déclarée**, Ω gelés) − μ_obs,ᵢ sur 8 bins bas-z ; μ_ref = 0 (la
   courbe passe par les bins). θ = 0,05 mag **abs gelé avant run** ;
   GUM : une ligne B (dispersion des bins), decide=theta — budget
   porté, pas utilisé. Interdit : ajuster les bins sur la référence.
2. **L'extract est SYNTHÉTIQUE** (`hz_sne_LOWZ-DEMO-2026.json`,
   vintage DEMO-2026) : fiducial ΛCDM Ω_m = 0,315, **H0 = 70**
   (délibérément entre les deux fabrications — rend la tension
   lisible par la donnée), bruit gaussien σ = 0,05 mag, seed numpy
   20260913 gelé dans la table. Dette écrite dans la table : cette
   carte valide le **protocole** sur une réponse connue par
   construction ; elle ne dit **rien de l'univers réel**. La table
   LITERATURE (compilation publique vérifiée, ou contact d'un tiers)
   reste à déclarer — c'est le geste d'appropriation attendu.
3. **Estimation pré-run honnête** : écart systématique Planck-vs-70
   ≈ +0,082 mag quasi constant à bas z → δ attendu ≈ 0,096, zone P
   [θ, 2θ], à ~0,004 du bord S− : **suspense maximal, le bruit des
   8 bins décide**.
4. **Premier run** : mot découvert : **S−**, δ = 0,1173 mag.
   Le bruit réalisé (moyenne négative) a renforcé l'écart
   systématique — l'estimation P n'était pas un arrangement, elle
   était fausse de la part du hasard, comme annoncé possible.
5. **Figé** : mot dans `tests/test_open_hz_sne_lowz.py` (mot, valeur
   à 12 décimales, sensibilité au fiducial — rms(70) = 0,0506 ≈ σ
   des bins, la carte encode bien sa réponse — et aux données —
   déplacer un bin déplace μ ; GUM decide=theta avec U = 2θ exactement).

## Le mot : S− — ce que dit la machine (sur la carte DEMO)

La fabrication Planck (H0 = 67,4) manque les bins bas-z de
0,117 mag en rms, au-delà de 2θ = 0,10. Au fiducial déclaré
(H0 = 70), le rms retombe à 0,0506 ≈ σ des bins — le protocole
rend **P au cheveu du S+**, car θ gelé = dispersion déclarée des
bins : même une courbe parfaite ne fait pas mieux que le bruit, un
S+ exigerait plus de bins. Le S− Planck est plus du double du rms
fiducial : il mesure l'écart de la fabrication, pas un défaut du
mécanisme. Le minimum du rms se situe vers H0 ≈ 71 (décalage du
bruit réalisé — honnête, la carte ne connaît pas son propre centre
exact).

**Lecture en miroir du chantier H0** : la campagne 2 de la tension
disait S+ à −2,2 σ SH0ES. La carte bas-z, elle, déclare par
construction sa réponse à 70 — entre les deux fabrications. Rien de
physique : c'est exactement pour ça que la table s'appelle DEMO.

## Dettes déclarées

- **Dette de nature** : donnée synthétique. Le mot S− ne peut pas
  être cité comme une propriété des supernovées réelles.
- **Dette de compression** (à réécrire pour la LITERATURE) : les
  bins ignorent la covariance ; les systématiques des SNe Ia ne
  sont pas dans σ.
- **Dette d'indépendance** (à déclarer selon la source) : si
  l'extract LITERATURE vient de SH0ES, la donnée et l'échelle locale
  ne sont pas indépendantes — pendant de la dette Landau (le min de
  E/p *est* le roton).

## Levier : H0←SH0ES_ou_autre

Le levier déclaré change le H0 de la courbe prédite, jamais les
bins ni θ. **Campagne exécutée** — voir `H0-CAMPAGNE-3-FRONTIERE-HZ.md`
(2026-09-13 soir) : fenêtre S+ [70,04 ; 71,72], frontières S− à
H0 ≤ 67,99 et H0 ≥ 73,89, lecture miroir Planck=S− / SH0ES=P. La
doctrine tient sous le levier ; la carte se relira telle quelle
quand la table LITERATURE remplacera la table DEMO.

## Pourquoi ce contact compte malgré sa dette de nature

C'est la première fois que la machine pèse une **carte de données
binnée contre une prédiction déclarée** dans le domaine macro —
le geste Landau transposé au diagramme de Hubble. Le mécanisme
(intégrale H(z), rms, gel, mot découvert) est désormais armé : le
jour où une compilation réelle est déclarée (par nous après
vérification, ou par un tiers), seule la table change — le cœur
ne bouge pas.
