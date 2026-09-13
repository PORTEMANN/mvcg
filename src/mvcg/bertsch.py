#!/usr/bin/env python3
"""Paramètre de Bertsch — gaz de Fermi dilué à l'unitarité (1/k_F a_s = 0).

Ansatz : BCS mean-field à T = 0 (Leggett 1980 ; Randeria 1995). Deux
équations adimensionnées (u = k/k_F, x = μ/ε_F, y = Δ/ε_F) :

    nombre : 1 = (3/2) ∫₀^∞ du u² (1 − (u²−x)/Ẽ),  Ẽ = √((u²−x)²+y²)
    gap (unitarité) : 0 = ∫₀^∞ du (u²/Ẽ − 1)

puis l'énergie interne par particule, E = E_gc + μN :

    E/(N ε_F) = (3/2) ∫₀^∞ du u² [(u²−x) − Ẽ + (y²/2)(1/Ẽ)] + x

et le paramètre de Bertsch, défini par E = ξ (3/5) N ε_F :

    ξ = (5/3) · E/(N ε_F)

Deux pièges historiques du contact, tous deux documentés dans la doctrine :

1. Normalisation : ξ porte le facteur (3/5) de l'énergie du gaz idéal.
   Oublier le 5/3 rapporte 0,3564 au lieu de 0,5905 — c'est l'écart
   systématique que la machine a d'abord cru être une intégrande fautive.
2. Convergence : les intégrales du nombre et du gap convergent
   seulement en 1/u². Une quadrature à cutoff fini sans correction de
   queue dérive (~+0,0035 sur ξ à Λ = 100, croissante avec Λ car la
   grille uniforme sous-échantillonne le pic à u ≈ √x). Les queues sont
   ici corrigées analytiquement (∫_Λ^∞ y²/(2u²) du = y²/(2Λ) pour le
   nombre, x/Λ pour le gap), d'où l'indépendance à Λ ≥ 60.

Valeurs mean-field de littérature reproduites : x = 0,5906, y = 0,6864,
ξ = 0,5905. La référence expérience/QMC est ξ ≈ 0,370 : l'écart (~37 %)
est la dette structurelle du mean-field, exactement du calibre de
P27 (He Hartree-Fock) — un ansatz pauvre ne récupère pas la
corrélation forte de l'unitarité.
"""

from __future__ import annotations

import math
from typing import Any

_QUEUE_LAM = 100.0  # cutoff de travail ; les corrections de queue rendent le résultat indépendant de Λ


def _simpson(f, a: float, b: float, n: int) -> float:
    if n % 2:
        n += 1
    h = (b - a) / n
    s = f(a) + f(b)
    for i in range(1, n):
        s += (4 if i % 2 else 2) * f(a + i * h)
    return s * h / 3.0


def _x_of_y(y: float, lam: float = _QUEUE_LAM, n: int = 5000) -> float:
    """x = μ/ε_F résolvant l'équation du nombre pour y donné,
    avec correction analytique de queue y²/(2Λ)."""

    def nombre(x: float) -> float:
        def f(u: float) -> float:
            e = math.hypot(u * u - x, y)
            return u * u * (1.0 - (u * u - x) / e)
        return 1.0 - 1.5 * (_simpson(f, 0.0, lam, n) + y * y / (2.0 * lam))

    lo, hi = -5.0, 400.0
    flo = nombre(lo)
    if flo * nombre(hi) > 0:
        raise ValueError("bracket x")
    for _ in range(45):
        mid = 0.5 * (lo + hi)
        fm = nombre(mid)
        if flo * fm <= 0:
            hi = mid
        else:
            lo, flo = mid, fm
    return 0.5 * (lo + hi)


_CACHE: dict[float, dict[str, Any]] = {}


def bertsch_xi(lam: float = _QUEUE_LAM) -> dict[str, Any]:
    """Résout gap + nombre à l'unitarité, retourne (x, y, ξ).

    Mémoïsé par cutoff : le résultat ne dépend que de lam, un seul
    calcul par processus quel que soit le nombre de contacts.
    """
    if lam in _CACHE:
        return dict(_CACHE[lam])

    n = 5000

    def gap_res(y: float) -> float:
        x = _x_of_y(y, lam, n)

        def f(u: float) -> float:
            e = math.hypot(u * u - x, y)
            return u * u / e - 1.0
        # gap à l'unitarité, queue analytique ∫_Λ^∞ x/u² du = x/Λ
        return _simpson(f, 1e-12, lam, n) + x / lam

    lo, hi = 0.05, 1.5
    glo = gap_res(lo)
    if glo * gap_res(hi) > 0:
        raise ValueError("bracket y")
    for _ in range(45):
        mid = 0.5 * (lo + hi)
        gm = gap_res(mid)
        if glo * gm <= 0:
            hi = mid
        else:
            lo, glo = mid, gm
    y = 0.5 * (lo + hi)
    x = _x_of_y(y, lam, n)

    def fE(u: float) -> float:
        e = math.hypot(u * u - x, y)
        # u²(ξ_k − E_k) + (y²/2)(u²/Ẽ) : le crochet complet est le
        # ξ_k − E_k + y²/(2Ẽ) standard, convergent en u⁻⁶ sans
        # correction de queue.
        return u * u * (u * u - x - e) + 0.5 * y * y * (u * u / e)

    e_over_nef = 1.5 * _simpson(fE, 1e-9, lam, n) + x
    xi = (5.0 / 3.0) * e_over_nef

    _CACHE[lam] = {"xi": xi, "mu_over_ef": x, "delta_over_ef": y}
    return dict(_CACHE[lam])
