# Métrique de contact

Module : `src/mvcg/metrics.py`. Commandes : `units`, `metric`.

\[
\mu=(\mu_{\mathrm{loc}},\mu_{\mathrm{ref}},\delta,\theta,U,[\cdot])
\]

- \(\delta_{\mathrm{rel}}=|\mu_{\mathrm{loc}}/\mu_{\mathrm{ref}}-1|\), \(\delta_{\mathrm{abs}}=|\mu_{\mathrm{loc}}-\mu_{\mathrm{ref}}|\)
- \(S^{+}\) si \(\delta\le\theta\), \(P\) si \(\delta\le 2\theta\), sinon \(S^{-}\)
- \(U\) gelé à part (paquet HL/Gauss/SI + millésime + \(\hbar,c,\varepsilon_0,\mu_0\))

I-V6 est exécutable : pas de `mu_ref` ou pas de \(U\) → refus.

Exemple Dirac en HL (identité, `orig=thm`) :

```bash
PYTHONPATH=src python3 -m mvcg --offline --root registre freeze --id F30 --phys 1 --orig thm --kappa equilibre
PYTHONPATH=src python3 -m mvcg --offline --root registre units --id F30 --packet hl --vintage convention
PYTHONPATH=src python3 -m mvcg --offline --root registre metric --id F30 \
  --mu-loc 6.283185307179586 --mu-ref 6.283185307179586 \
  --theta 1e-12 --dimension 'e*g' --kind rel
PYTHONPATH=src python3 -m mvcg --offline --root registre measure --id F30 --d 0
```

`measure` accroche `units_sha256` et `metric_sha256` dans `inputs_sha256` de \(d\).
