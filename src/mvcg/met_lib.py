#!/usr/bin/env python3
"""MÉT-LIB-1.5 — gel des bits et tueurs I-G1 / I-G2.

I-G1  bits hachés avant d ; sigma(bits) ∈ inputs_sha256(d)
I-G2  bits immutables après lecture de d (seul statut void autorisé)

Ce module n'évalue aucune physique. Il rend Kill_G1 et Kill_G2 calculables.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

from mvcg.ots_anchor import audit_anchor, stamp_digest, upgrade_and_verify

ORIGINS = ("pred", "thm", "proto")
KAPPA = ("equilibre", "deficit", "non_contraint", "famille", "hors_domaine")
PROTOCOL = "MET-LIB-1.5"
ISO = "%Y-%m-%dT%H:%M:%S.%fZ"


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime(ISO)


def parse_iso(value: str) -> datetime:
    raw = value.strip()
    if raw.endswith("Z"):
        raw = raw[:-1] + "+00:00"
    return datetime.fromisoformat(raw)


def canonical(obj: Any) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode(
        "utf-8"
    )


def sha256_obj(obj: Any) -> str:
    return hashlib.sha256(canonical(obj)).hexdigest()


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _bits_payload(bits: dict) -> dict:
    body = {
        "protocol": bits["protocol"],
        "frontier_id": bits["frontier_id"],
        "b_phys": bits["b_phys"],
        "b_orig": bits["b_orig"],
        "kappa_hat": bits["kappa_hat"],
        "frozen_at": bits["frozen_at"],
    }
    if bits.get("d_sha256"):
        body["d_sha256"] = bits["d_sha256"]
    return body


@dataclass
class BitsRecord:
    protocol: str
    frontier_id: str
    b_phys: int
    b_orig: str
    kappa_hat: str
    frozen_at: str
    bits_sha256: str
    d_sha256: str = ""

    def payload_for_hash(self) -> dict:
        body = {
            "protocol": self.protocol,
            "frontier_id": self.frontier_id,
            "b_phys": self.b_phys,
            "b_orig": self.b_orig,
            "kappa_hat": self.kappa_hat,
            "frozen_at": self.frozen_at,
        }
        if self.d_sha256:
            body["d_sha256"] = self.d_sha256
        return body


@dataclass
class CostRecord:
    protocol: str
    frontier_id: str
    d_reg: Any
    b_mesuree: int
    measured_at: str
    inputs_sha256: dict
    cost_sha256: str


@dataclass
class Audit:
    invariant: str
    frontier_id: str
    kill: bool
    reason: str
    details: dict


class MetLib15:
    """Registre fichier : registre/<id>.bits.json et registre/<id>.cost.json."""

    def __init__(self, root: Path, offline_ots: bool = False):
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)
        self.log_path = self.root / "mutations.log.jsonl"
        self.offline_ots = offline_ots

    def _bits_path(self, fid: str) -> Path:
        return self.root / f"{fid}.bits.json"

    def _cost_path(self, fid: str) -> Path:
        return self.root / f"{fid}.cost.json"

    def _void_path(self, fid: str) -> Path:
        return self.root / f"{fid}.void.json"

    def _units_path(self, fid: str) -> Path:
        return self.root / f"{fid}.units.json"

    def _metric_path(self, fid: str) -> Path:
        return self.root / f"{fid}.metric.json"

    def _d_path(self, fid: str) -> Path:
        return self.root / f"{fid}.D.json"

    def is_void(self, fid: str) -> bool:
        return self._void_path(fid).exists()

    def freeze(
        self,
        frontier_id: str,
        phys: int,
        orig: str,
        kappa_hat: str,
        frozen_at: Optional[str] = None,
        dossier: Optional[dict] = None,
    ) -> BitsRecord:
        if self.is_void(frontier_id):
            raise RuntimeError(f"{frontier_id}: void, gel interdit")
        if self._cost_path(frontier_id).exists():
            raise RuntimeError(f"{frontier_id}: d déjà mesuré — I-G2 interdit un nouveau gel")
        if self._bits_path(frontier_id).exists():
            raise RuntimeError(f"{frontier_id}: bits déjà gelés — pas de re-gel (I-G2)")
        if phys not in (0, 1):
            raise ValueError("b_phys ∈ {0,1}")
        if orig not in ORIGINS:
            raise ValueError(f"b_orig ∈ {ORIGINS}")
        if kappa_hat not in KAPPA:
            raise ValueError(f"kappa_hat ∈ {KAPPA}")

        d_sha = ""
        if dossier is not None:
            from mvcg.dossier import canonical_d

            can = canonical_d(dossier)
            self._d_path(frontier_id).write_text(
                json.dumps(can, indent=2, sort_keys=True) + "\n", encoding="utf-8"
            )
            d_sha = sha256_obj(can)
        rec = BitsRecord(
            protocol=PROTOCOL,
            frontier_id=frontier_id,
            b_phys=int(phys),
            b_orig=orig,
            kappa_hat=kappa_hat,
            frozen_at=frozen_at or utc_now(),
            bits_sha256="",
            d_sha256=d_sha,
        )
        rec.bits_sha256 = sha256_obj(rec.payload_for_hash())
        self._bits_path(frontier_id).write_text(
            json.dumps(asdict(rec), indent=2, ensure_ascii=True) + "\n", encoding="utf-8"
        )
        if not self.offline_ots:
            stamp_digest(rec.bits_sha256, frontier_id, self.root)
        return rec

    def measure(
        self,
        frontier_id: str,
        d_reg: Any,
        measured: bool = True,
        measured_at: Optional[str] = None,
    ) -> CostRecord:
        if self.is_void(frontier_id):
            raise RuntimeError(f"{frontier_id}: void, mesure interdite")
        if self._cost_path(frontier_id).exists():
            raise RuntimeError(f"{frontier_id}: d déjà publié — pas de re-mesure silencieuse")
        bits_path = self._bits_path(frontier_id)
        if not bits_path.exists():
            raise RuntimeError(f"{frontier_id}: pas de bits — I-G1 tuerait toute mesure")
        if not self.offline_ots:
            bits_preview = json.loads(bits_path.read_text(encoding="utf-8"))
            ots = audit_anchor(self.root, frontier_id, bits_preview["bits_sha256"])
            if ots["kill"]:
                raise RuntimeError(f"{frontier_id}: mesure refusée — {ots['reason']}")

        bits = json.loads(bits_path.read_text(encoding="utf-8"))
        bits_sha = bits["bits_sha256"]
        recomputed = sha256_obj(_bits_payload(bits))
        if recomputed != bits_sha:
            raise RuntimeError(f"{frontier_id}: bits.json corrompu (sha interne)")

        stamp = measured_at or utc_now()
        if stamp < bits["frozen_at"]:
            raise RuntimeError(
                f"{frontier_id}: measured_at < frozen_at — I-G1 tuerait cette mesure"
            )

        inputs = {
            "bits_sha256": bits_sha,
            "bits_file_sha256": sha256_file(bits_path),
            "protocol": PROTOCOL,
        }
        if self._units_path(frontier_id).exists():
            inputs["units_sha256"] = sha256_file(self._units_path(frontier_id))
        if self._metric_path(frontier_id).exists():
            inputs["metric_sha256"] = sha256_file(self._metric_path(frontier_id))
        if self._d_path(frontier_id).exists():
            inputs["d_sha256"] = bits.get("d_sha256")
            inputs["d_file_sha256"] = sha256_file(self._d_path(frontier_id))
        body = {
            "protocol": PROTOCOL,
            "frontier_id": frontier_id,
            "d_reg": d_reg,
            "b_mesuree": int(bool(measured)),
            "measured_at": stamp,
            "inputs_sha256": inputs,
        }
        rec = CostRecord(
            protocol=PROTOCOL,
            frontier_id=frontier_id,
            d_reg=d_reg,
            b_mesuree=int(bool(measured)),
            measured_at=stamp,
            inputs_sha256=inputs,
            cost_sha256=sha256_obj(body),
        )
        self._cost_path(frontier_id).write_text(
            json.dumps(asdict(rec), indent=2, ensure_ascii=True) + "\n", encoding="utf-8"
        )
        return rec

    def void(self, frontier_id: str, reason: str) -> dict:
        """Annule F. N'autorise pas la mutation des bits. I-G2 reste intact."""
        doc = {
            "protocol": PROTOCOL,
            "frontier_id": frontier_id,
            "status": "void",
            "reason": reason,
            "voided_at": utc_now(),
        }
        doc["void_sha256"] = sha256_obj(doc)
        self._void_path(frontier_id).write_text(
            json.dumps(doc, indent=2, ensure_ascii=True) + "\n", encoding="utf-8"
        )
        return doc

    def freeze_units(self, frontier_id: str, units_doc: dict[str, Any]) -> dict:
        """Gèle le paquet d'unités U avant ou avec la mesure. Pas de re-gel après d."""
        from mvcg.rationalization import parse_units, units_payload

        if self.is_void(frontier_id):
            raise RuntimeError(f"{frontier_id}: void")
        if self._cost_path(frontier_id).exists():
            raise RuntimeError(f"{frontier_id}: d déjà mesuré — U immuable")
        if self._units_path(frontier_id).exists():
            raise RuntimeError(f"{frontier_id}: U déjà gelé")
        U = parse_units(units_doc)
        payload = units_payload(U)
        rec = {
            "protocol": PROTOCOL + "-U",
            "frontier_id": frontier_id,
            "units": payload,
            "frozen_at": utc_now(),
        }
        rec["units_sha256"] = sha256_obj(payload)
        rec["record_sha256"] = sha256_obj({k: v for k, v in rec.items()})
        self._units_path(frontier_id).write_text(
            json.dumps(rec, indent=2, ensure_ascii=True) + "\n", encoding="utf-8"
        )
        return rec

    def record_metric(
        self,
        frontier_id: str,
        mu_loc: float,
        mu_ref: float,
        theta: float,
        dimension: str,
        delta_kind: str = "rel",
    ) -> dict:
        from dataclasses import asdict as _asdict

        from mvcg.metrics import audit_metric, build_metric
        from mvcg.rationalization import parse_units

        if not self._units_path(frontier_id).exists():
            raise RuntimeError(f"{frontier_id}: pas de U gelé — la métrique ne coopère avec rien")
        units_rec = json.loads(self._units_path(frontier_id).read_text(encoding="utf-8"))
        U = parse_units(units_rec["units"])
        rec = build_metric(frontier_id, mu_loc, mu_ref, theta, U, dimension, delta_kind)
        audit = audit_metric(rec)
        if audit["kill"]:
            raise RuntimeError(f"{frontier_id}: métrique refusée — {audit['reasons']}")
        path = self._metric_path(frontier_id)
        if path.exists():
            raise RuntimeError(f"{frontier_id}: métrique déjà publiée")
        payload = _asdict(rec)
        path.write_text(json.dumps(payload, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
        return payload

    def try_patch_bits(self, frontier_id: str, **fields: Any) -> Audit:
        """Toute tentative de mutation après gel. Si d existe : Kill G2."""
        if self.is_void(frontier_id):
            return Audit(
                "I-G2",
                frontier_id,
                kill=False,
                reason="void : mutation ignorée, bits historiques conservés",
                details={"void": True, "attempt": fields},
            )
        path = self._bits_path(frontier_id)
        if not path.exists():
            return Audit(
                "I-G2",
                frontier_id,
                kill=False,
                reason="pas de bits, rien à muter",
                details={"attempt": fields},
            )
        before = json.loads(path.read_text(encoding="utf-8"))
        attempt = {k: v for k, v in fields.items() if k in ("b_phys", "b_orig", "kappa_hat")}
        changed = {k: {"from": before.get(k), "to": v} for k, v in attempt.items() if before.get(k) != v}
        cost_exists = self._cost_path(frontier_id).exists()

        event = {
            "at": utc_now(),
            "frontier_id": frontier_id,
            "attempt": attempt,
            "changed": changed,
            "cost_exists": cost_exists,
        }
        with self.log_path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(event, ensure_ascii=True) + "\n")

        if not changed:
            return Audit("I-G2", frontier_id, False, "aucune modification réelle", event)

        if cost_exists:
            return Audit(
                "I-G2",
                frontier_id,
                kill=True,
                reason="diff bits après d — I-G2 tué (écriture refusée)",
                details=event,
            )
        return Audit(
            "I-G2",
            frontier_id,
            kill=True,
            reason="re-gel / patch des bits après freeze — écriture refusée",
            details=event,
        )

    def audit_g1(self, frontier_id: str) -> Audit:
        if self.is_void(frontier_id):
            return Audit("I-G1", frontier_id, False, "void : hors domaine de mesure", {"void": True})
        bits_path, cost_path = self._bits_path(frontier_id), self._cost_path(frontier_id)
        if not bits_path.exists() and not cost_path.exists():
            return Audit("I-G1", frontier_id, False, "frontière absente", {})
        if cost_path.exists() and not bits_path.exists():
            return Audit(
                "I-G1",
                frontier_id,
                kill=True,
                reason="d sans bits — sigma(bits) absent des entrées",
                details={},
            )
        if bits_path.exists() and not cost_path.exists():
            return Audit("I-G1", frontier_id, False, "bits gelés, d non encore publié", {})

        bits = json.loads(bits_path.read_text(encoding="utf-8"))
        cost = json.loads(cost_path.read_text(encoding="utf-8"))
        details = {
            "frozen_at": bits.get("frozen_at"),
            "measured_at": cost.get("measured_at"),
            "bits_sha256": bits.get("bits_sha256"),
            "inputs": cost.get("inputs_sha256", {}),
        }
        if cost.get("measured_at") < bits.get("frozen_at"):
            return Audit("I-G1", frontier_id, True, "measured_at < frozen_at", details)
        inputs = cost.get("inputs_sha256") or {}
        if inputs.get("bits_sha256") != bits.get("bits_sha256"):
            return Audit(
                "I-G1",
                frontier_id,
                True,
                "bits_sha256 absent ou différent de inputs_sha256(d)",
                details,
            )
        expected = sha256_obj(_bits_payload(bits))
        if expected != bits.get("bits_sha256"):
            return Audit("I-G1", frontier_id, True, "intégrité interne bits.json cassée", details)
        if not self.offline_ots:
            ots = audit_anchor(self.root, frontier_id, bits.get("bits_sha256"))
            details["ots"] = ots
            if ots["kill"]:
                return Audit("I-G1-OTS", frontier_id, True, ots["reason"], details)
            if ots.get("frozen_at_ots") and parse_iso(cost.get("measured_at")) < parse_iso(
                ots["frozen_at_ots"]
            ):
                return Audit(
                    "I-G1-OTS",
                    frontier_id,
                    True,
                    "measured_at < Date HTTP calendrier",
                    details,
                )
        return Audit("I-G1", frontier_id, False, "sigma(bits) ∈ inputs(d) et horloge cohérente", details)

    def audit_g2(self, frontier_id: str) -> Audit:
        if self.is_void(frontier_id):
            return Audit(
                "I-G2",
                frontier_id,
                False,
                "void : bits historiques figés, mutation non appliquée",
                {"void": True},
            )
        if not self._bits_path(frontier_id).exists():
            return Audit("I-G2", frontier_id, False, "pas de bits", {})
        incidents = []
        if self.log_path.exists():
            for line in self.log_path.read_text(encoding="utf-8").splitlines():
                if not line.strip():
                    continue
                ev = json.loads(line)
                if ev.get("frontier_id") == frontier_id and ev.get("changed"):
                    incidents.append(ev)
        bits = json.loads(self._bits_path(frontier_id).read_text(encoding="utf-8"))
        expected = sha256_obj(_bits_payload(bits))
        if expected != bits.get("bits_sha256"):
            return Audit(
                "I-G2",
                frontier_id,
                True,
                "bits.json muté hors API (sha interne ≠ contenu)",
                {"expected": expected, "stored": bits.get("bits_sha256")},
            )
        return Audit(
            "I-G2",
            frontier_id,
            False,
            "bits intacts depuis le gel",
            {"bits_sha256": bits.get("bits_sha256"), "incidents_refuses": len(incidents)},
        )

    def audit_all(self) -> list[Audit]:
        ids = sorted({p.name.split(".")[0] for p in self.root.glob("*.json") if not p.name.endswith(".jsonl")})
        out: list[Audit] = []
        for fid in ids:
            if fid.endswith("mutations"):
                continue
            out.append(self.audit_g1(fid))
            out.append(self.audit_g2(fid))
        return out


def _print(audit: Audit) -> None:
    flag = "KILL" if audit.kill else "HOLD"
    print(f"[{flag}] {audit.invariant} {audit.frontier_id}: {audit.reason}")


def main(argv: Optional[list[str]] = None) -> int:
    p = argparse.ArgumentParser(prog="met_lib_15", description="Tueurs I-G1 et I-G2")
    p.add_argument("--root", default=str(Path.cwd() / "registre"))
    p.add_argument("--offline", action="store_true", help="sans ancre OTS (tests)")
    sub = p.add_subparsers(dest="cmd", required=True)

    f = sub.add_parser("freeze", help="geler phys/orig/kappa_hat avant d")
    f.add_argument("--id", required=True)
    f.add_argument("--phys", type=int, required=True, choices=(0, 1))
    f.add_argument("--orig", required=True, choices=ORIGINS)
    f.add_argument("--kappa", required=True, dest="kappa_hat", choices=KAPPA)

    m = sub.add_parser("measure", help="publier d avec bits_sha256 en entrée")
    m.add_argument("--id", required=True)
    m.add_argument("--d", required=True, help="entier, inf, ou empty")
    m.add_argument("--not-measured", action="store_true")

    v = sub.add_parser("void", help="annuler F sans muter les bits")
    v.add_argument("--id", required=True)
    v.add_argument("--reason", required=True)

    t = sub.add_parser("patch", help="tenter une mutation (doit tuer G2 si d existe)")
    t.add_argument("--id", required=True)
    t.add_argument("--phys", type=int, choices=(0, 1))
    t.add_argument("--orig", choices=ORIGINS)
    t.add_argument("--kappa", dest="kappa_hat", choices=KAPPA)

    a = sub.add_parser("audit", help="I-G1 et I-G2")
    a.add_argument("--id")

    u = sub.add_parser("upgrade-btc", help="upgrade OTS + vérif attestation de bloc")
    u.add_argument("--id", required=True)

    un = sub.add_parser("units", help="geler le paquet d'unités (hl|gauss|si|1)")
    un.add_argument("--id", required=True)
    un.add_argument("--packet", required=True, choices=("hl", "gauss", "si", "1"))
    un.add_argument("--vintage", default="unspecified")
    un.add_argument("--hbar", type=float, default=1.0)
    un.add_argument("--c", type=float, default=1.0)
    un.add_argument("--epsilon0", type=float, default=None)
    un.add_argument("--mu0", type=float, default=None)

    met = sub.add_parser("metric", help="publier (mu_loc, mu_ref, theta, U)")
    met.add_argument("--id", required=True)
    met.add_argument("--mu-loc", type=float, required=True)
    met.add_argument("--mu-ref", type=float, required=True)
    met.add_argument("--theta", type=float, required=True)
    met.add_argument("--dimension", required=True)
    met.add_argument("--kind", default="rel", choices=("rel", "abs"))

    ash = sub.add_parser("ash", help="C5 instrument — pas un tuyau")
    ash.add_argument("--fs", type=float, default=256.0)
    ash.add_argument("--f0", type=float, default=1.0)
    ash.add_argument("--octaves", type=int, default=4)
    ash.add_argument("--tau", type=float, default=0.1)
    ash.add_argument("--seconds", type=float, default=2.0)
    ash.add_argument("--tone", type=float, default=4.0)
    ash.add_argument("--no-renorm", action="store_true")

    dyn = sub.add_parser("dynamics", help="S candidate forme MDU — pas un préfiltre")
    dyn.add_argument("--n", type=int, default=32)
    dyn.add_argument("--steps", type=int, default=40)
    dyn.add_argument("--nu", type=float, default=0.05)
    dyn.add_argument("--torsion", type=float, default=0.4)
    dyn.add_argument("--seed", type=int, default=0)
    dyn.add_argument("--poisson", action="store_true")
    dyn.add_argument("--spectral", action="store_true")
    dyn.add_argument("--dealias", action="store_true")
    dyn.add_argument("--pad32", action="store_true", help="padding 3/2 au lieu du 2/3")
    dyn.add_argument("--nu-local", action="store_true")
    dyn.add_argument("--3d", dest="dim3", action="store_true")
    dyn.add_argument("--band", action="store_true", help="IC bande limitée")
    dyn.add_argument("--nu-const", action="store_true", help="ν=ν0 (pas e^{-S})")
    dyn.add_argument("--pjp", action="store_true", help="générateur PJP au lieu de J")

    camp = sub.add_parser("campaign", help="campagne (défaut : répétition locale)")
    camp.add_argument("--local", action="store_true", default=True,
                      help="répéter sans gel ni OTS (défaut)")
    camp.add_argument("--publish", action="store_true",
                      help="geler, hasher, mesurer — après répétition")
    sub.add_parser("registers", help="trois tiroirs micro/meso/macro")
    sub.add_parser("dictionaries", help="balayer hl|gauss|si|1 à μ_loc gelé")
    sub.add_parser("corridor", help="P2 discret-dans-continu (n, κ)")

    args = p.parse_args(argv)
    lib = MetLib15(Path(args.root), offline_ots=args.offline)

    if args.cmd == "freeze":
        rec = lib.freeze(args.id, args.phys, args.orig, args.kappa_hat)
        print(json.dumps(asdict(rec), indent=2))
        return 0
    if args.cmd == "measure":
        raw = args.d
        if raw == "inf":
            dval: Any = "inf"
        elif raw == "empty":
            dval = None
        else:
            dval = int(raw)
        rec = lib.measure(args.id, dval, measured=not args.not_measured)
        print(json.dumps(asdict(rec), indent=2))
        return 0
    if args.cmd == "void":
        print(json.dumps(lib.void(args.id, args.reason), indent=2))
        return 0
    if args.cmd == "patch":
        fields = {}
        if args.phys is not None:
            fields["b_phys"] = args.phys
        if args.orig is not None:
            fields["b_orig"] = args.orig
        if args.kappa_hat is not None:
            fields["kappa_hat"] = args.kappa_hat
        audit = lib.try_patch_bits(args.id, **fields)
        _print(audit)
        return 2 if audit.kill else 0
    if args.cmd == "audit":
        audits = [lib.audit_g1(args.id), lib.audit_g2(args.id)] if args.id else lib.audit_all()
        killed = False
        for au in audits:
            _print(au)
            killed = killed or au.kill
        return 2 if killed else 0
    if args.cmd == "upgrade-btc":
        out = upgrade_and_verify(Path(args.root), args.id)
        print(json.dumps(out, indent=2))
        return 0 if out["status"] == "confirmed" else 3
    if args.cmd == "units":
        doc = {
            "packet": args.packet,
            "vintage": args.vintage,
            "hbar": args.hbar,
            "c": args.c,
            "epsilon0": args.epsilon0,
            "mu0": args.mu0,
        }
        print(json.dumps(lib.freeze_units(args.id, doc), indent=2))
        return 0
    if args.cmd == "metric":
        print(
            json.dumps(
                lib.record_metric(
                    args.id,
                    args.mu_loc,
                    args.mu_ref,
                    args.theta,
                    args.dimension,
                    args.kind,
                ),
                indent=2,
            )
        )
        return 0
    if args.cmd == "ash":
        from mvcg.ash_instrument import AshParams, analyze, report_dict
        import numpy as np

        t = np.arange(0.0, args.seconds, 1.0 / args.fs)
        x = np.sin(2.0 * np.pi * args.tone * t)
        rep = analyze(
            x,
            args.fs,
            AshParams(f0=args.f0, n_oct=args.octaves, tau=args.tau, renorm=not args.no_renorm),
        )
        print(json.dumps(report_dict(rep), indent=2))
        return 0 if rep.gain_stable else 2
    if args.cmd == "dynamics":
        if getattr(args, "dim3", False):
            from mvcg.spectral3d import DynParams3, analyze3, report_dict as d3

            rep = analyze3(
                DynParams3(
                    n=args.n,
                    steps=args.steps,
                    nu0=args.nu,
                    torsion=args.torsion,
                    seed=args.seed,
                    dealias=args.dealias,
                    nu_local=args.nu_local,
                )
            )
            print(json.dumps(d3(rep), indent=2))
            return 0
        from mvcg.dynamics import DynParams, analyze as dyn_analyze, report_dict as dyn_dict

        rep = dyn_analyze(
            DynParams(
                n=args.n,
                steps=args.steps,
                nu0=args.nu,
                torsion=args.torsion,
                seed=args.seed,
                pressure_mode=(
                    "spectral" if args.spectral else "poisson" if args.poisson else "prescribed"
                ),
                dealias=args.dealias or args.pad32,
                dealias_mode="3/2" if args.pad32 else "2/3",
                nu_local=args.nu_local,
                ic="band" if args.band else "white",
                nu_mode="const" if args.nu_const else "entropic",
                generator="PJP" if args.pjp else "J",
            )
        )
        print(json.dumps(dyn_dict(rep), indent=2))
        return 0
    if args.cmd == "campaign":
        from mvcg.campaign import run_campaign

        out = run_campaign(
            Path(args.root),
            offline_ots=args.offline,
            commit=bool(args.publish),
        )
        print(json.dumps(out, indent=2))
        return 0
    if args.cmd == "registers":
        from mvcg.registers import run_registers

        out = run_registers()
        print(json.dumps(out, indent=2))
        return 0
    if args.cmd == "dictionaries":
        from mvcg.dictionaries import run_dictionaries

        print(json.dumps(run_dictionaries(), indent=2))
        return 0
    if args.cmd == "corridor":
        from mvcg.corridor import run_corridor

        print(json.dumps(run_corridor(), indent=2))
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())
