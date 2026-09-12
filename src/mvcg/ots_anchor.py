#!/usr/bin/env python3
"""Ancrage OpenTimestamps de sigma(beta).

Soumet le SHA-256 des bits gelés aux calendriers publics.
La Date HTTP du calendrier est l'horloge externe (D4).
La preuve .ots reste pending jusqu'à confirmation Bitcoin — suffisant
comme témoin d'existence, pas encore comme datation de bloc.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path
from typing import Any, Optional
from urllib.error import HTTPError
from urllib.parse import urljoin
from urllib.request import Request, urlopen

def _ots():
    """Import tardif : les tests G1/G2 offline n'ont pas besoin du paquet."""
    from opentimestamps.core.notary import BitcoinBlockHeaderAttestation, PendingAttestation
    from opentimestamps.core.op import OpSHA256
    from opentimestamps.core.serialize import (
        BytesDeserializationContext,
        BytesSerializationContext,
        StreamDeserializationContext,
    )
    from opentimestamps.core.timestamp import DetachedTimestampFile, Timestamp

    return {
        "BitcoinBlockHeaderAttestation": BitcoinBlockHeaderAttestation,
        "PendingAttestation": PendingAttestation,
        "OpSHA256": OpSHA256,
        "BytesDeserializationContext": BytesDeserializationContext,
        "BytesSerializationContext": BytesSerializationContext,
        "StreamDeserializationContext": StreamDeserializationContext,
        "DetachedTimestampFile": DetachedTimestampFile,
        "Timestamp": Timestamp,
    }

CALENDARS = (
    "https://alice.btc.calendar.opentimestamps.org",
    "https://bob.btc.calendar.opentimestamps.org",
    "https://finney.calendar.eternitywall.com",
)

ACCEPT = "application/vnd.opentimestamps.v1"
USER_AGENT = "mvcg-met-lib-15/0.1"


def _parse_http_date(value: Optional[str]) -> Optional[str]:
    if not value:
        return None
    try:
        dt = parsedate_to_datetime(value)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    except (TypeError, ValueError, OverflowError):
        return None


@dataclass
class CalendarReceipt:
    url: str
    ok: bool
    http_date: Optional[str]
    error: Optional[str] = None
    proof_len: int = 0


@dataclass
class OtsAnchor:
    protocol: str
    frontier_id: str
    bits_sha256: str
    status: str
    calendars: list[dict]
    frozen_at_ots: Optional[str]
    receipts_ok: int
    ots_file: str
    note: str = ""


def _submit(url: str, digest: bytes, timeout: float):
    req = Request(
        urljoin(url.rstrip("/") + "/", "digest"),
        data=digest,
        headers={"Accept": ACCEPT, "User-Agent": USER_AGENT},
        method="POST",
    )
    with urlopen(req, timeout=timeout) as resp:
        if resp.status != 200:
            raise RuntimeError(f"calendar {url} status {resp.status}")
        http_date = _parse_http_date(resp.headers.get("Date"))
        body = resp.read(10000)
        if len(body) >= 10000:
            raise RuntimeError(f"calendar {url} response too large")
        o = _ots()
        ts = o["Timestamp"].deserialize(o["BytesDeserializationContext"](body), digest)
        return ts, http_date


def stamp_digest(
    digest_hex: str,
    frontier_id: str,
    dest_dir: Path,
    calendars: tuple[str, ...] = CALENDARS,
    timeout: float = 20.0,
    min_ok: int = 1,
) -> OtsAnchor:
    digest = bytes.fromhex(digest_hex)
    if len(digest) != 32:
        raise ValueError("bits_sha256 must be 32 bytes hex")

    o = _ots()
    ts = o["Timestamp"](digest)
    receipts: list[CalendarReceipt] = []
    for url in calendars:
        try:
            sub, http_date = _submit(url, digest, timeout)
            ts.merge(sub)
            receipts.append(CalendarReceipt(url, True, http_date, proof_len=0))
        except Exception as exc:  # noqa: BLE001 — on journalise et on continue
            receipts.append(CalendarReceipt(url, False, None, error=str(exc)))

    ok = [r for r in receipts if r.ok]
    if len(ok) < min_ok:
        raise RuntimeError(
            "OTS stamp failed: "
            + "; ".join(f"{r.url}: {r.error}" for r in receipts if not r.ok)
        )

    detached = o["DetachedTimestampFile"](o["OpSHA256"](), ts)
    ctx = o["BytesSerializationContext"]()
    detached.serialize(ctx)
    ots_bytes = ctx.getbytes()
    ots_path = Path(dest_dir) / f"{frontier_id}.bits.ots"
    ots_path.write_bytes(ots_bytes)
    for r in receipts:
        if r.ok:
            r.proof_len = len(ots_bytes)

    dates = sorted(r.http_date for r in ok if r.http_date)
    frozen_at_ots = dates[0] if dates else None
    anchor = OtsAnchor(
        protocol="MET-LIB-1.5-OTS",
        frontier_id=frontier_id,
        bits_sha256=digest_hex,
        status="pending",
        calendars=[asdict(r) for r in receipts],
        frozen_at_ots=frozen_at_ots,
        receipts_ok=len(ok),
        ots_file=ots_path.name,
        note="pending calendar attestation; bitcoin upgrade not required for G1-OTS",
    )
    meta_path = Path(dest_dir) / f"{frontier_id}.ots.json"
    meta_path.write_text(json.dumps(asdict(anchor), indent=2) + "\n", encoding="utf-8")
    return anchor


def load_anchor(dest_dir: Path, frontier_id: str) -> Optional[dict[str, Any]]:
    path = Path(dest_dir) / f"{frontier_id}.ots.json"
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def audit_anchor(dest_dir: Path, frontier_id: str, bits_sha256: str) -> dict[str, Any]:
    """HOLD ssi preuve présente, digest = bits_sha256, >=1 calendrier OK."""
    dest_dir = Path(dest_dir)
    meta = load_anchor(dest_dir, frontier_id)
    if meta is None:
        return {"kill": True, "reason": "pas d'ancre OTS", "invariant": "I-G1-OTS"}
    if meta.get("bits_sha256") != bits_sha256:
        return {
            "kill": True,
            "reason": "digest OTS ≠ bits_sha256",
            "invariant": "I-G1-OTS",
            "details": {"ots": meta.get("bits_sha256"), "bits": bits_sha256},
        }
    ots_file = dest_dir / meta.get("ots_file", f"{frontier_id}.bits.ots")
    if not ots_file.exists() or ots_file.stat().st_size == 0:
        return {"kill": True, "reason": "fichier .ots manquant", "invariant": "I-G1-OTS"}
    if int(meta.get("receipts_ok") or 0) < 1:
        return {"kill": True, "reason": "aucun calendrier n'a accepté le digest", "invariant": "I-G1-OTS"}
    if not meta.get("frozen_at_ots"):
        return {
            "kill": True,
            "reason": "Date HTTP calendrier absente — pas d'horloge externe",
            "invariant": "I-G1-OTS",
        }
    return {
        "kill": False,
        "reason": f"ancre pending {meta.get('receipts_ok')} calendrier(s), Date {meta.get('frozen_at_ots')}",
        "invariant": "I-G1-OTS",
        "frozen_at_ots": meta.get("frozen_at_ots"),
        "status": meta.get("status"),
    }


def _load_detached(ots_path: Path):
    o = _ots()
    with Path(ots_path).open("rb") as fd:
        return o["DetachedTimestampFile"].deserialize(o["StreamDeserializationContext"](fd))


def _save_detached(ots_path: Path, detached) -> None:
    o = _ots()
    ctx = o["BytesSerializationContext"]()
    detached.serialize(ctx)
    Path(ots_path).write_bytes(ctx.getbytes())


def _http_body(url: str, timeout: float = 20.0) -> str:
    req = Request(url, headers={"User-Agent": USER_AGENT})
    with urlopen(req, timeout=timeout) as resp:
        return resp.read().decode("utf-8")


def _http_json(url: str, timeout: float = 20.0) -> Any:
    return json.loads(_http_body(url, timeout=timeout))


def upgrade_proof(ots_path: Path, timeout: float = 20.0) -> dict[str, Any]:
    """Rapatrie les attestations calendrier. 404 = toujours pending."""
    ots_path = Path(ots_path)
    o = _ots()
    detached = _load_detached(ots_path)
    pending = 0
    upgraded = 0
    bitcoin = 0
    errors: list[str] = []
    heights: list[int] = []

    for msg, att in list(detached.timestamp.all_attestations()):
        if isinstance(att, o["BitcoinBlockHeaderAttestation"]):
            bitcoin += 1
            heights.append(att.height)
            continue
        if not isinstance(att, o["PendingAttestation"]):
            continue
        pending += 1
        url = urljoin(att.uri.rstrip("/") + "/", "timestamp/" + msg.hex())
        try:
            req = Request(url, headers={"Accept": ACCEPT, "User-Agent": USER_AGENT})
            with urlopen(req, timeout=timeout) as resp:
                body = resp.read(20000)
            remote = o["Timestamp"].deserialize(o["BytesDeserializationContext"](body), msg)
            detached.timestamp.merge(remote)
            upgraded += 1
            for _, att2 in remote.all_attestations():
                if isinstance(att2, o["BitcoinBlockHeaderAttestation"]):
                    bitcoin += 1
                    heights.append(att2.height)
        except HTTPError as exc:
            if exc.code == 404:
                errors.append(f"{att.uri}: pending (404)")
            else:
                errors.append(f"{att.uri}: HTTP {exc.code}")
        except Exception as exc:  # noqa: BLE001
            errors.append(f"{att.uri}: {exc}")

    if upgraded:
        _save_detached(ots_path, detached)

    status = "confirmed" if bitcoin else "pending"
    return {
        "ots_file": str(ots_path),
        "file_digest": detached.file_digest.hex(),
        "status": status,
        "pending_seen": pending,
        "upgraded": upgraded,
        "bitcoin_attestations": bitcoin,
        "heights": heights,
        "errors": errors,
    }


def verify_bitcoin_attestation(ots_path: Path, timeout: float = 20.0) -> dict[str, Any]:
    """Vérifie chaque attestation de bloc via l'API Blockstream (en-tête public)."""
    o = _ots()
    detached = _load_detached(ots_path)
    results = []
    for msg, att in detached.timestamp.all_attestations():
        if not isinstance(att, o["BitcoinBlockHeaderAttestation"]):
            continue
        height = att.height
        try:
            block_hash = _http_body(
                f"https://blockstream.info/api/block-height/{height}", timeout=timeout
            ).strip()
            header = _http_json(f"https://blockstream.info/api/block/{block_hash}", timeout=timeout)
        except Exception as exc:  # noqa: BLE001
            results.append(
                {
                    "height": height,
                    "ok": False,
                    "reason": f"blockstream: {exc}",
                }
            )
            continue
        merkle = header.get("merkle_root")
        digest_hex = msg.hex()
        ok = merkle == digest_hex
        results.append(
            {
                "height": height,
                "block_hash": block_hash,
                "merkle_root": merkle,
                "attestation_digest": digest_hex,
                "ok": ok,
                "block_time": header.get("timestamp"),
                "reason": "merkle_root = digest" if ok else "merkle_root ≠ digest",
            }
        )
    confirmed = [r for r in results if r.get("ok")]
    return {
        "ots_file": str(ots_path),
        "file_digest": detached.file_digest.hex(),
        "attestations": results,
        "confirmed": len(confirmed),
        "kill": len(confirmed) == 0,
        "reason": (
            f"{len(confirmed)} attestation(s) de bloc vérifiée(s)"
            if confirmed
            else "aucune attestation Bitcoin vérifiable (preuve encore pending)"
        ),
    }


def upgrade_and_verify(dest_dir: Path, frontier_id: str) -> dict[str, Any]:
    dest_dir = Path(dest_dir)
    meta = load_anchor(dest_dir, frontier_id) or {}
    ots_path = dest_dir / meta.get("ots_file", f"{frontier_id}.bits.ots")
    up = upgrade_proof(ots_path)
    ver = verify_bitcoin_attestation(ots_path)
    status = "confirmed" if not ver["kill"] else "pending"
    meta.update(
        {
            "status": status,
            "bitcoin": ver,
            "upgrade": up,
        }
    )
    (dest_dir / f"{frontier_id}.ots.json").write_text(
        json.dumps(meta, indent=2) + "\n", encoding="utf-8"
    )
    return {"upgrade": up, "verify": ver, "status": status}
