# Protocole gelé — Chantier L4 : le gyrocorpus (pont P4 pesé par la machine)

**Gelé avant run — 2026-09-14.** Mots inconnus au gel pour les trois contacts.
Transposition comparée demandée : la machine noétique complète a fermé son
canal hors-programme « gap gyroscopique comme observable de L4 » (notes D1–D4,
P1–P3 + addendum + P4, versions datées) ; la loi arithmétique y a été **ajustée
par les dernières campagnes** — l'addendum P3 a rétracté le maximum à k₂
(mélange d'amplitudes, protocole uniforme AMP=0,15) et reformulé la contrainte 2
de P4. Ce chantier transpose en contacts MVC-G ce qui, dans ce corpus, est un
nombre prédit contre un nombre mesuré.

## Ce qui est pesé, ce qui ne l'est pas (gelé)

- **Pesé** : (a) le gap universel ω(k₁) insensible à l'inertie (propriété la
  plus robuste du corpus, confirmée à deux amplitudes) ; (b) la transposabilité
  de la branche gappée gelée ω²=ω₀²+β²k⁴ (P1–P2, ω₀=0,45, β=11,2, arrondis
  déclarés) au régime fin AMP=0,15 à k₂ — la dette ouverte du corpus
  (dépendance en amplitude) y devient un écart chiffré ; (c) la prédiction de
  la fenêtre inertielle D₃ ≈ 7–8 par la branche rapportée à la ligne vide
  calibrée — la contrainte 1 de P4 (deux nombres liés, ω₀ et β d'une même
  circulation) y est pesée **indirectement** : si la branche, gelée avant
  l'addendum, prédit la fenêtre reformulée, le pont tient à ce niveau.
- **Non pesé** (écrit, pas masqué) : la contrainte 1 comme telle (le lien
  ω₀–β–κ_eff n'est pas un nombre dans le corpus — décliné) ; la contrainte 3
  (exclusion des lois de masse ajoutée simples — une **classe** de lois, pas un
  nombre — déclinée) ; les points rétractés (ω(k₂) à AMP=0,3 — sortis du corpus
  par l'addendum, jamais re-pesés ici).

## Données gelées (table `l4_gyrocorps_LITERATURE-HP2027.json`)

Unités internes GP du corpus (ℏ=m=g=1), modes d'anneau k = 2πm/32, m = 1,2,3.
Vague fine AMP=0,15 (addendum P3, protocole uniforme) sauf mention :

| grandeur | valeur gelée | u déclarée | statut |
|---|---|---|---|
| ω₀, β (P1–P2, arrondis) | 0,45 / 11,2 | 0,005 / 0,05 | paramètres de branche gelés |
| ligne vide k₁,k₂,k₃ | 0,079 / 0,298 / 0,515 | 0,02 (lecture déclarée) | référence calibrée |
| ω(k₁) m=5 / m=12 | 0,630 / 0,640 | 0,02 (dispersion corpus) | vague fine |
| ω(k₂) m=8 (addendum) | 0,58 | 0,02 (lecture déclarée) | régime fin |
| ω(k₃) m=8 (addendum, pic dominant) | 3,57 | 0,5 (pic dominant, dédoublement déclaré à m=10) | régime fin |
| D₃(m=8) addendum | 6,9 | 0,5 | fenêtre inertielle |

Branche évaluée (gelé avant run) : k₁ → 0,6237 · k₂ → 1,7848 · k₃ → 3,9121.
D₃_pred = ω_branche(k₃)/ω_vide(k₃) = 7,5964.

## Contacts (3, registre meso, fibre ("1","1"), abs)

1. **L4_Gap_Universel** — pred : ω(k₁, m=12) = ω(k₁, m=5) (gap commun,
   deux masses de la vague fine, même protocole). theta = u_delta =
  0.0282842712474619 (u=0,02 déclarée de part et d'autre), decide=U k=1.
   Estimation pré-run honnête : delta = 0,010, ratio 0,354 → **S+ attendu,
   suspense faible** : la propriété la plus robuste du corpus confirmée en
   pesée croisée fine/fine.
2. **L4_Branche_k2_RegimeFin** — pred : la branche gelée évaluée à k₂ au régime
   fin = mesure addendum m=8. theta = u_delta = 0.02138372495786989
   (u(branch)=0,007567 par propagation des arrondis ω₀,β ; u(obs)=0,02),
   decide=U k=1. Estimation pré-run : delta = 1,2048, ratio 56,3 → **S− attendu
   SANS suspense** : la rétractation de l'addendum devient un écart chiffré —
   la branche ne se transpose pas à k₂ en régime fin ; la dépendance en
   amplitude, dette ouverte du corpus, est pesée à 56 uc.
3. **L4_Fenetre_Branche** — pred : D₃_pred = 7,5964 (branche gelée rapportée à
   la ligne vide) = D₃(m=8) addendum = 6,9. theta = u_delta =
  0.5815053896029518 (u(D_pred)=0,2969 en propagation relative branche+ligne
   vide ; u(D_obs)=0,5 déclarée), decide=U k=1. Estimation pré-run :
   delta = 0,6964, ratio 1,198 → **P annoncé AU CHEVEU, suspense maximal** :
   le pont « deux nombres liés » tient indirectement à ~1,2 uc — la branche
   calibrée à AMP=0,3 prédit la fenêtre reformulée à AMP=0,15 à 8 % près.

## Anti-fraude et dettes (gelées avant run)

- La référence NE DOIT JAMAIS entrer dans le calcul (transport = table + branche
  gelée seulement).
- Dettes déclarées : arrondis P1–P2 (u propagée, pas rétro-ajustée) ; u de
  lecture 0,02 déclarées là où le corpus ne publie pas d'incertitude ; le
  dédoublement spectral m=10 (bord de fenêtre) exclu du contact 3 (pic dominant
  m=8 seul pesé).
- Vintage HP distinct déclaré : le corpus est un canal séparé, hors Programme
  2027 — aucune rétro-injection, la table cite ses notes par date.
- Toute divergence mot attendu / mot découvert sera consignée, jamais corrigée
  en silence.
