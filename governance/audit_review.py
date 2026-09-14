"""Read-only review of allowlisted governance audit JSONL files.

The reviewer intentionally returns aggregate counts only. It never returns raw
``user_hash``/``document_hash`` values and does not open MongoDB or the network.
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
import json
from pathlib import Path
from typing import Iterable

from .audit import CATEGORIES, EVENTS, RESULTS

DEFAULT_DAYS = 30
DEFAULT_THRESHOLDS = {
    "login_failure": 5,
    "denied_access": 5,
    "error": 1,
    "retention_error": 1,
    "malformed": 1,
}
ACCESS_CATEGORIES = frozenset({"dashboard", "event_detail", "governance_review"})


class AuditReviewError(ValueError):
    """Raised for an invalid review request without exposing source content."""


def _utc_now(now: datetime | None = None) -> datetime:
    stamp = datetime.now(timezone.utc) if now is None else now
    if stamp.tzinfo is None or stamp.utcoffset() is None:
        raise AuditReviewError("review timestamp must be timezone-aware")
    return stamp.astimezone(timezone.utc)


def _parse_timestamp(value) -> datetime | None:
    if not isinstance(value, str) or len(value) > 80:
        return None
    try:
        stamp = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except (ValueError, TypeError):
        return None
    if stamp.tzinfo is None or stamp.utcoffset() is None:
        return None
    return stamp.astimezone(timezone.utc)


def audit_paths(directory: str | Path | None = None) -> tuple[Path, ...]:
    """Return current + rotated audit files in deterministic oldest-to-newest order."""
    root = Path(directory) if directory is not None else Path(__file__).resolve().parents[1] / "logs"
    current = root / "audit.jsonl"
    rotated = []
    for path in root.glob("audit.jsonl.*") if root.exists() else ():
        suffix = path.name.removeprefix("audit.jsonl.")
        if suffix.isdigit():
            rotated.append((int(suffix), path))
    # Higher rotation suffix is older. Review old -> current for deterministic output.
    ordered = [path for _, path in sorted(rotated, reverse=True)]
    if current.exists():
        ordered.append(current)
    return tuple(ordered)


def _iter_lines(paths: Iterable[Path]):
    for path in paths:
        try:
            with path.open("r", encoding="utf-8") as handle:
                for line in handle:
                    yield line
        except (OSError, UnicodeError):
            # A file that cannot be safely read is an integrity/review problem.
            yield None


def review(directory: str | Path | None = None, *, days: int = DEFAULT_DAYS,
           now: datetime | None = None, thresholds: dict[str, int] | None = None) -> dict:
    """Review audit logs and return aggregate evidence only.

    No raw audit record, pseudonymous identifier, request data, or exception text is
    returned. Invalid/unreadable lines are counted as ``malformed``.
    """
    if type(days) is not int or not 1 <= days <= 3650:
        raise AuditReviewError("days must be an integer between 1 and 3650")
    stamp = _utc_now(now)
    cutoff = stamp - timedelta(days=days)
    limits = dict(DEFAULT_THRESHOLDS if thresholds is None else thresholds)
    if set(limits) != set(DEFAULT_THRESHOLDS) or any(type(v) is not int or v < 1 for v in limits.values()):
        raise AuditReviewError("invalid review thresholds")

    counts = {
        "records_in_window": 0,
        "login_failure": 0,
        "denied_access": 0,
        "error": 0,
        "retention_error": 0,
        "malformed": 0,
    }
    paths = audit_paths(directory)
    for raw in _iter_lines(paths):
        if raw is None:
            counts["malformed"] += 1
            continue
        if not raw.strip():
            continue
        try:
            record = json.loads(raw)
        except (json.JSONDecodeError, TypeError):
            counts["malformed"] += 1
            continue
        if not isinstance(record, dict):
            counts["malformed"] += 1
            continue
        observed = _parse_timestamp(record.get("timestamp"))
        if observed is None or observed > stamp + timedelta(minutes=5):
            counts["malformed"] += 1
            continue
        if observed < cutoff:
            continue

        event = record.get("event")
        category = record.get("category")
        result = record.get("result")
        if event not in EVENTS or category not in CATEGORIES or result not in RESULTS:
            counts["malformed"] += 1
            continue

        counts["records_in_window"] += 1
        if event == "login_failure":
            counts["login_failure"] += 1
        if result == "denied" and category in ACCESS_CATEGORIES:
            counts["denied_access"] += 1
        if result == "error":
            counts["error"] += 1
            if category == "retention":
                counts["retention_error"] += 1

    breaches = {name: counts[name] >= threshold for name, threshold in limits.items()}
    attention = any(breaches.values())
    return {
        "reviewed_at": stamp.isoformat(),
        "window_days": days,
        "status": "ATTENTION" if attention else "OK",
        "counts": counts,
        "thresholds": limits,
        "breaches": breaches,
        "files_reviewed": len(paths),
        "privacy": "aggregate_only_no_raw_identifiers",
    }
