# Répétition locale puis publication

```
répéter  →  rehearsal.json     (pas de hash, pas d'OTS, pas de d)
choisir  →  éventuellement ajuster D / θ / levier
publier  →  freeze + hash + measure [+ OTS]
```

```bash
# local, défaut
python3 -m mvcg campaign --root /tmp/rep

# gel + d  (après lecture du rehearsal)
python3 -m mvcg campaign --publish --root /tmp/pub --offline
```

Les registres (`mvcg registers`) sont déjà une répétition : aucun fichier bits.
G1/G2 ne s'appliquent qu'au `--publish`.
