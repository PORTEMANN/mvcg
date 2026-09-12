# C5 et dynamique candidate

Deux modules **optionnels**. Ils ne s’intercalent pas entre \(D\) et \(\hat M\).

## C5 — `src/mvcg/ash_instrument.py`

Instrument : grilles \(f_n=f_0\cdot 2^{n/12}\), \(f_0,N_{\mathrm{oct}},\tau\in D\).

Sortie : \(R_c,R_{\mathrm{top}},R_{\mathrm{dyn}},E_i\), comparaison à un périodogramme,
test de gain I-A3.

```bash
PYTHONPATH=src python3 -m mvcg ash --f0 1 --octaves 4 --tone 4 --fs 256
```

Interdit : servir de vanne d’entrée, nommer \(R_c\) une pression de vide.

## Dynamique — `src/mvcg/dynamics.py`

Structure candidate, forme discrète 2D périodique :

\[
\partial_t\mathbf v=-\nabla P+\mathbf v\wedge T+\nu(S)\Delta\mathbf v,
\qquad
\nu(S)=\nu_0 e^{-S},\ 
S=\langle v^2/2\rangle.
\]

Levier I-V3 : \(T=0\) vs \(T\neq 0\) (écart sur le ratio d’énergie).

```bash
PYTHONPATH=src python3 -m mvcg dynamics --torsion 0.4 --n 32 --steps 40
```

Ce n’est pas Navier–Stokes + gravité + conscience. C’est une EDP jouable,
avec \(P,T,\nu_0,\mathrm{seed}\in D\), comparable à la même EDP à \(T=0\).

## Branchement

`freeze` / `measure` n’appellent ni C5 ni la dynamique.
Pour en faire un contact : geler \(U\), publier une métrique
\((\mu_{\mathrm{loc}},\mu_{\mathrm{ref}},\delta)\) — p.ex. `gain_ratio` vs \(0\),
ou `|energy_ratio(T)-energy_ratio(0)|` vs un seuil déclaré.
