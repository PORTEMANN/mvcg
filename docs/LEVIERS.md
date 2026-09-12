# Leviers branchés

| Levier | CLI | Prévision |
|---|---|---|
| `renorm ← off` | `mvcg ash --no-renorm` | I-A3 relatif → S− (énergies brutes) |
| `nu ← nu0` | `dynamics --nu-const` | référence chaleur licite |
| `IC ← band` | `dynamics --band` | `r(n)` plat |
| `generateur ← PJP` | `dynamics --pjp` | moins de fente gyro |
| `2/3 ← 3/2` | `dynamics --pad32` | produits quadratiques |
| `paquet` | `units --packet` | Dirac |

Toujours un seul levier à la fois, déclaré dans D avant μ.
