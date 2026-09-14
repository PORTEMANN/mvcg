#!/usr/bin/env python3
"""Réplication externe — prototype (principe 4, ligne directrice).

Le protocole de réplication de la machine EXISTE DÉJÀ : c'est son
test figé — le mot attendu y est écrit avant toute exécution, et la
suite complète le vérifie à chaque run. Ce module n'invente donc
aucun mécanisme : il enveloppe ce qui existe.

Convention gelée de la machine : un contact est figé par un test
qui affirme son mot — `tests/test_open_*.py` pour les contacts
ouverts (assertion du mot avant le run), et tout autre fichier de
test pour les contacts pred (audit 2026-09-13 : leurs mots étaient
verrouillés dans test_registers, test_p1_p2, etc.). reproduce.py :

1. recalcule la ligne du contact depuis le registre (mot « obtenu ») ;
2. retrouve le(s) test(s) qui figent ce contact (« attendu ») ;
3. les exécute pour de vrai (sous-processus = vraie réplication) ;
4. affiche attendu / obtenu et [OK] ou [ECART].

Limite déclarée : pour les contacts figés uniquement par le classement
(fibres), le mot attendu n'est pas isolable par contact — le statut
porte alors sur les tests, pas sur le mot seul.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
TESTS = ROOT / "tests"
WORD_RE = re.compile(r'assertEqual\(\s*r\["verdict"\]\s*,\s*"(S[+-]|P)"\s*\)')

# Tout fichier de test peut figer un mot (audit 2026-09-13 : les mots
# des contacts pred étaient verrouillés hors de la convention
# test_open_*). test_reproduce.py est exclu : il ne peut pas s'y
# auto-découvrir (pas de récursion).
FREEZERS = [
    p for p in sorted(TESTS.glob("test_*.py"))
    if p.name != "test_reproduce.py"
]


def live_row(contact_id: str) -> dict[str, Any]:
    """La ligne recalculée main — le mot « obtenu »."""
    from mvcg.registers import run_registers

    by = {r["id"]: r for r in run_registers()["rows"]}
    if contact_id not in by:
        raise KeyError(f"contact inconnu du registre: {contact_id}")
    r = by[contact_id]
    return {"verdict": r["verdict"], "delta": r["delta"], "theta": r["theta"]}


def freezing_files(contact_id: str) -> list[Path]:
    """Les fichiers de test qui mentionnent ce contact (convention)."""
    return [p for p in FREEZERS if contact_id in p.read_text(encoding="utf-8")]


def expected_word(contact_id: str, files: list[Path]) -> str | None:
    """Le mot attendu, extrait de l'assertion figée du test dédié.

    Règle en deux temps :
    1. un bloc de test qui mentionne ce contact y fige son mot — cela
       isole les contacts dans les fichiers multi-contacts (jamais la
       première assertion du fichier : ce serait prendre le mot du
       voisin) ;
    2. sinon, repli : tous les mots figés du fichier — unique → ce
       mot ; plusieurs → None (un fichier ambigu ne doit pas deviner).
       Couvre le cas où l'id vit dans un helper (`def row`) et le mot
       dans le bloc de test.

    test_verdicts_online.py est exclu : il fige le classement par
    fibres (assertions génériques en boucle) — pas un mot par contact.
    Y lire un mot « par bloc » est le faux ami qui a attribué un S− de
    boucle au HVP le 2026-09-13 (audit reproduce).
    """
    for p in files:
        if p.name == "test_verdicts_online.py":
            continue
        text = p.read_text(encoding="utf-8")
        block: list[str] = []
        for line in text.splitlines():
            # Toute méthode (test OU helper comme `def row`) ferme le
            # bloc précédent : sinon l'assertion du test d'avant fuit
            # dans le helper voisin et s'attribue à tort son id.
            if re.match(r"^\s*def ", line):
                block = []
            block.append(line)
            if contact_id in "\n".join(block):
                m = WORD_RE.search("\n".join(block))
                if m:
                    return m.group(1)
        words = {m.group(1) for m in WORD_RE.finditer(text)}
        if len(words) == 1:
            return words.pop()
    return None


def run_tests(files: list[Path]) -> dict[str, Any]:
    """Exécute les tests figés pour de vrai (sous-processus)."""
    modules = [p.stem for p in files]
    env = dict(os.environ)
    env["PYTHONPATH"] = str(ROOT / "src")
    proc = subprocess.run(
        [sys.executable, "-m", "unittest", *modules, "-q"],
        cwd=TESTS,
        capture_output=True,
        text=True,
        env=env,
    )
    tail = (proc.stdout + proc.stderr).strip().splitlines()
    return {"modules": modules, "ok": proc.returncode == 0, "tail": tail[-1:] if tail else []}


def reproduce(contact_id: str) -> dict[str, Any]:
    files = freezing_files(contact_id)
    if not files:
        return {
            "contact": contact_id,
            "status": "NON FIGÉ",
            "expected": None,
            "obtained": live_row(contact_id),
            "tests": [],
            "note": "aucun test ne mentionne ce contact (audit complet des fichiers de test)",
        }
    got = live_row(contact_id)
    exp = expected_word(contact_id, files)
    res = run_tests(files)
    if exp is not None and exp != got["verdict"]:
        status = "ÉCART"
    else:
        status = "OK" if res["ok"] else "ÉCHEC DES TESTS"
    return {
        "contact": contact_id,
        "status": status,
        "expected": exp,
        "obtained": got,
        "tests": res["modules"],
        "tail": res["tail"],
    }


def main_reproduce(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="répliquer un contact : attendu (test figé) vs obtenu (registre live)")
    p.add_argument("--contact", required=True, help="id du contact (ex. H0_Ecart_Planck_SH0ES)")
    args = p.parse_args(argv)
    try:
        out = reproduce(args.contact)
    except KeyError as exc:
        print(str(exc))
        return 2
    print(json.dumps(out, indent=2, ensure_ascii=False))
    print(f"# Résultat attendu : {out['expected']} — obtenu : {out['obtained']['verdict']} "
          f"(delta={out['obtained']['delta']:.6g}) [{out['status']}]")
    return 0 if out["status"] == "OK" else 1


if __name__ == "__main__":
    raise SystemExit(main_reproduce())
