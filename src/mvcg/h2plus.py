#!/usr/bin/env python3
"""LCAO 1s de H2+ — formules Lowe (R en bohr, ζ=1).

E_elec = (H_aa + H_ab) / (1+S)
E = E_elec + 1/R
De = E(H) - E   avec E(H) = -1/2
"""

from __future__ import annotations

import math
from typing import Any

HA_TO_EV = 27.211386245988  # CODATA-2018 déclaré


def lcao_1s(R: float = 2.0) -> dict[str, Any]:
    if R <= 0:
        raise ValueError("R > 0")
    S = math.exp(-R) * (1.0 + R + R * R / 3.0)
    H_aa = -0.5 - (1.0 / R) * (1.0 - math.exp(-2.0 * R) * (1.0 + R))
    H_ab = -S / 2.0 - math.exp(-R) * (1.0 + R)
    E_elec = (H_aa + H_ab) / (1.0 + S)
    E = E_elec + 1.0 / R
    De_ha = -0.5 - E
    return {
        "R_bohr": R,
        "zeta": 1.0,
        "S": S,
        "H_aa": H_aa,
        "H_ab": H_ab,
        "E_elec": E_elec,
        "E": E,
        "De_Ha": De_ha,
        "De_eV": De_ha * HA_TO_EV,
        "formula": "Lowe 7-88..90",
    }
