# Invariants mathématiques — MVC-G

Objets seulement. Pas d’ontologie. Un invariant est une assertion
munie d’un domaine et d’un tueur.

## 0. Espaces

\[
D\in\mathcal{D},\;
S\in\mathcal{S},\;
L\in\mathcal{L},\;
V\in\{S^{+},P,S^{-}\}
\]

\[
\Mhat:\mathcal{D}\times\mathcal{S}\times\mathcal{L}\to\{S^{+},P,S^{-}\}
\]

\[
\beta(F)=(b_{\mathrm{phys}},b_{\mathrm{orig}},\hat\kappa,t_{\mathrm{freeze}},\mathrm{id})
\]

\[
d_{\mathrm{reg}}(F)\in\mathbb{N}\cup\{\infty,\varnothing\},\qquad
d_{\mathrm{circ}}(\rho)\in\mathbb{N}\cup\{\infty\}
\]

Convention : \(\varnothing\neq 0\).

Bits d’origine : \(\{ \mathrm{pred},\mathrm{thm},\mathrm{proto}\}\).

---

## 1. Famille V — verdict

| Id | Énoncé | Tueur |
|---|---|---|
| I-V1 | \(\mathrm{im}\,\Mhat=\{S^{+},P,S^{-}\}\) | autre symbole, ou \(D\) sans \(\sigma(D)\) |
| I-V2 | \(\mathrm{Free}(S)=\emptyset\) sinon pas de \(S^{+}\) | scalaire de \(S\) choisi après lecture de \(D\) |
| I-V3 | \(V=S^{+}\Rightarrow \Mhat(D,S,\varnothing)\) chute | succès inchangé sans levier |
| I-V4 | \(\sigma(\mathrm{script},D,\pi)\mapsto\sigma(V)\) stable | deux replays, deux empreintes |
| I-V5 | schéma d’artefact de \(S^{-}\) = schéma de \(S^{+}\) | échec seulement narratif |
| I-V6 | tout \(S^{+}\) exhibe \((\mu_{\mathrm{loc}},\mu_{\mathrm{ref}},\delta)\) | colonne référence vide |

\(\mathrm{Free}(S)\) : nombres présents dans \(S\) et absents de \(D\).

---

## 2. Famille M — coût

Monoïde : \((\overline{\mathbb{N}},+,0)\), \(\infty\) absorbant.

| Id | Énoncé | Tueur |
|---|---|---|
| I-M1 | \(d_{\mathrm{reg}}\) et \(d_{\mathrm{circ}}\) sont deux fonctions | les additionner ou les substituer |
| I-M2 | \(\varnothing\neq 0\) | hygiène enregistrée en équilibre |
| I-M3 | associativité et absorption | règle publiée qui les viole |
| I-M4 | \(A,B\) déclarés indépendants *avant* mesure \(\Rightarrow d_{\mathrm{reg}}(A\oplus B)=d_{\mathrm{reg}}(A)+d_{\mathrm{reg}}(B)\) | écart, ou indépendance posée après \(d\) |
| I-M5 | sur une famille listée \(\mathcal{T}\) : \(d_{\mathrm{circ}}(t^{m}\circ t^{k})=d_{\mathrm{circ}}(t^{m})+d_{\mathrm{circ}}(t^{k})\) | un couple de \(\mathcal{T}\) qui échoue |
| I-M6 | \(\sqsubseteq\) préordre acyclique sur \(\mathcal{F}\) | cycle dans le registre |
| I-M7 | sous le tarif \(d_{\mathrm{circ}}(t^{j})=2^{j}\) et \(\sum j_i=m\), \(d^{*}=2m\) est une propriété du tarif ; un tarif \(d_{\mathrm{alt}}(t^{j})=j\) est publié | vendre \(2m\) comme géométrie |
| I-M8 | \(d_{\mathrm{circ}}(\tau)\ge B(\tau)\) si \(B\) est une borne de littérature | réalisation sous \(B\) qui passe \(\pi\) |

L’homomorphisme n’est exigé que sur \(d_{\mathrm{circ}}\) et sur \(\mathcal{T}\).
Il n’est pas étendu par analogie à \(d_{\mathrm{reg}}\).

---

## 3. Famille G — gel

\[
\sigma(\beta)=\mathrm{SHA256}(\mathrm{canonical}(\beta))
\]

\[
\mathrm{Kill}(F)
=
[b_{\mathrm{phys}}=1]
\land[b_{\mathrm{nouvelle}}=1]
\land[b_{\mathrm{mesurée}}=1]
\land[d_{\mathrm{reg}}(F)=0]
\land[b_{\mathrm{orig}}=\mathrm{pred}]
\]

| Id | Énoncé | Tueur |
|---|---|---|
| I-G1 | \(\sigma(\beta)\in\texttt{inputs\_sha256}(d)\) et \(t_d\ge t_\beta\) (datetimes, pas lex) | \(d\) sans bits, hash divergent, horloge inversée |
| I-G1-OTS | preuve calendrier, digest identique, Date HTTP | ancre absente ou digest ≠ `bits_sha256` |
| I-G2 | payload des bits reproduit `bits_sha256` après gel | mutation du fichier bits |
| I-G3 | L5 affichée \(\iff\neg\mathrm{Kill}\) | \(\mathrm{Kill}=1\) et L5 encore écrite |
| I-G4 | une campagne dont l’objectif est \(\mathrm{Kill}=1\) | seule batterie = familles à déficit forcé |

`void` retire \(F\) des nouvelles mesures. Il ne mute pas \(\beta\).
Un clone \(F^{\star}\) sur le même \((\sigma(D),\sigma(S))\) est un B3-FAIL d’identité (à indexer).

L’horloge locale n’est pas une ancre. L’ancre temporelle admissible est
la `Date` HTTP d’un calendrier OTS, puis — après upgrade — le temps de bloc.

---

## 4. Famille A — acquisition (si un analyseur entre au cœur)

Signature déclarée :

\[
\mathrm{ASH}(x|_{W};f_0,N_{\mathrm{oct}},\tau)=(R_c,R_{\mathrm{top}},R_{\mathrm{dyn}},E_{1..n})
\]

\((f_0,N_{\mathrm{oct}},\tau)\in D\), paramètres de domaine, pas des théorèmes.

| Id | Énoncé | Tueur |
|---|---|---|
| I-A1 | paramètres ∈ \(D\) | les dériver d’un satellite |
| I-A2 | aucun poids appris | fit / grille choisie sur l’épreuve |
| I-A3 | si \(R\) est dit invariant d’amplitude : \(R(\lambda x)=R(x)\) | dérive sous gain |
| I-A4 | comparaison STFT ou CWT, même fenêtre | score interne seul |
| I-A5 | API sans lexique satellite | identifiant interdit |

---

## 5. Famille C — architecture

| Id | Énoncé | Tueur |
|---|---|---|
| I-C1 | pas d’arc cœur → satellite | import ou \(S\) définie dehors |
| I-C2 | ≤ 5 exécutables tant que replay tiers incomplet | 6ᵉ script dans l’image |
| I-C3 | ≤ 30 min CPU, pas de GPU requis | dépendance GPU non satellite |
| I-C4 | un mot, un objet | troisième référent pour *liberté* ou *pression* |
| I-C5 | \(n+1\) admissible ssi cœur plus petit *ou* plus de replays, et I-G2 tient | plus de chantiers, bits retouchés |

---

## 6. Invariant directeur

\[
\mathrm{MVC\text{-}G}
=\Mhat\times\mathcal{M}_2\times(\mathrm{ASH})
\quad\text{sous I-G1--I-G4, hors satellite.}
\]

ASH est optionnel. Sans lui le produit reste un éprouveur + un registre.

Tout ajout qui n’est pas un facteur de ce produit, ou qui viole le gel,
n’est pas une optimisation. C’est une autre machine.
