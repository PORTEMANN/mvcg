# Rationalisation des champs

Module : `src/mvcg/rationalization.py`.

Trois paquets : `hl`, `gauss`, `si`.

\[
q_{\mathrm{HL}}=\sqrt{4\pi}\,q_{\mathrm{G}}
\]

Dirac (\(\hbar=c=1\)) :

\[
eg=
\begin{cases}
2\pi n & \text{HL}\\
n/2 & \text{Gauss}
\end{cases}
\qquad
e_{\mathrm{HL}}g_{\mathrm{HL}}=4\pi\,e_{\mathrm{G}}g_{\mathrm{G}}.
\]

Flux du monopôle \(n=1\) (formules de dictionnaire, \(e\) numérique du paquet) :

\[
\Phi_{\mathrm{HL}}=\frac{2\pi}{e},\qquad
\Phi_{\mathrm{G}}=\frac{4\pi}{e}.
\]

Le facteur 2 n’est pas une physique. C’est le dictionnaire.

`units` gèle \(U\) dans `{id}.units.json` **avant** `d`.
Sans \(U\), `metric` refuse : la métrique ne coopère avec aucune constante.
