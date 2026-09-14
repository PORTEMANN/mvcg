#!/usr/bin/env python3
"""reproduce.py --contact <id> — la réplication, c'est le test figé.

Prototype local (principe 4 de la ligne directrice). Le protocole de
réplication de la machine existe déjà : chaque contact ouvert a un
test qui fige son mot AVANT exécution. Ce script enveloppe : il
recalcule la ligne (obtenu), retrouve le test figé (attendu),
l'exécute pour de vrai, et confronte.

    python reproduce.py --contact H0_Ecart_Planck_SH0ES
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from mvcg.reproduce import main_reproduce  # noqa: E402

if __name__ == "__main__":
    raise SystemExit(main_reproduce())
