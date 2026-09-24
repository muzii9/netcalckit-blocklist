#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Strict parsing and deterministic triage scoring for candidate domains."""

from __future__ import annotations

import csv
import ipaddress
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from urllib.parse import urlparse

from domain_utils import DOMAIN

REQUIRED_COLUMNS = (
    "domain",
    "vendor",
    "category",
    "evidence_url",
    "evidence_type",
    "dedicated_service",
    "shared_infrastructure",
    "essential_function",
    "false_positive_risk",
    "status",
    "observed_date",
    "notes",
)

ALLOWED_EVIDENCE_TYPES = {
    "vendor-doc",
    "vendor-code",
    "first-party-config",
    "repro-observation",
    "community-report",
    "third-party-signal",
}
ALLOWED_TRISTATE = {"yes", "no", "unknown"}
ALLOWED_RISKS = {"low", "low-moderate", "moderate", "high", "unknown"}
ALLOWED_STATUSES = {"new", "research", "review", "hold", "rejected"}

EVIDENCE_SCORE = {
    "vendor-doc": 4,
    "vendor-code": 4,
    "first-party-config": 3,
    "repro-observation": 2,
    "community-report": 1,
    "third-party-signal": 0,
}
RISK_SCORE = {
    "low": 2,
    "low-moderate": 1,
    "moderate": 0,
    "high": -3,
    "unknown": -1,
}


@dataclass(frozen=True)
class Candidate:
    domain: str
    vendor: str
    category: str
    evidence_url: str
    evidence_type: str
    dedicated_service: str
    shared_infrastructure: str
    essential_function: str
    false_positive_risk: str
    status: str
    observed_date: str
    notes: str


@dataclass(frozen=True)
class CandidateScore:
    domain: str
    score: int
    band: str
    reasons: tuple[str, ...]


def _valid_domain(value: str) -> bool:
    try:
        ipaddress.ip_address(value)
        return False
    except ValueError:
        return bool(DOMAIN.fullmatch(value))


def _valid_https_url(value: str) -> bool:
    parsed = urlparse(value)
    return parsed.scheme == "https" and bool(parsed.netloc)


def load_candidates(path: Path, *, require_sorted: bool = True) -> list[Candidate]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames != list(REQUIRED_COLUMNS):
            raise ValueError(
                f"{path}: expected columns {', '.join(REQUIRED_COLUMNS)}"
            )

        candidates: list[Candidate] = []
        seen: set[str] = set()

        for line_number, row in enumerate(reader, start=2):
            values = {key: (row.get(key) or "").strip() for key in REQUIRED_COLUMNS}
            domain = values["domain"]

            if not _valid_domain(domain):
                raise ValueError(
                    f"{path}: line {line_number}: invalid domain {domain!r}"
                )
            if domain in seen:
                raise ValueError(
                    f"{path}: line {line_number}: duplicate domain {domain!r}"
                )
            seen.add(domain)

            for field in ("vendor", "category"):
                if not values[field]:
                    raise ValueError(
                        f"{path}: line {line_number}: {field} must not be empty"
                    )

            if not _valid_https_url(values["evidence_url"]):
                raise ValueError(
                    f"{path}: line {line_number}: evidence_url must be an https URL"
                )

            if values["evidence_type"] not in ALLOWED_EVIDENCE_TYPES:
                raise ValueError(
                    f"{path}: line {line_number}: invalid evidence_type "
                    f"{values['evidence_type']!r}"
                )

            for field in (
                "dedicated_service",
                "shared_infrastructure",
                "essential_function",
            ):
                if values[field] not in ALLOWED_TRISTATE:
                    raise ValueError(
                        f"{path}: line {line_number}: {field} must be "
                        "yes, no, or unknown"
                    )

            if values["false_positive_risk"] not in ALLOWED_RISKS:
                raise ValueError(
                    f"{path}: line {line_number}: invalid false_positive_risk "
                    f"{values['false_positive_risk']!r}"
                )

            if values["status"] not in ALLOWED_STATUSES:
                raise ValueError(
                    f"{path}: line {line_number}: invalid status "
                    f"{values['status']!r}"
                )

            try:
                date.fromisoformat(values["observed_date"])
            except ValueError as error:
                raise ValueError(
                    f"{path}: line {line_number}: observed_date must be YYYY-MM-DD"
                ) from error

            candidates.append(Candidate(**values))

    domains = [candidate.domain for candidate in candidates]
    if require_sorted and domains != sorted(domains):
        raise ValueError(f"{path}: candidates are not sorted by domain")

    return candidates


def score_candidate(candidate: Candidate) -> CandidateScore:
    score = EVIDENCE_SCORE[candidate.evidence_type]
    reasons: list[str] = [
        f"evidence:{candidate.evidence_type}={EVIDENCE_SCORE[candidate.evidence_type]:+d}"
    ]

    dedicated_scores = {"yes": 2, "no": -2, "unknown": 0}
    value = dedicated_scores[candidate.dedicated_service]
    score += value
    reasons.append(f"dedicated_service:{candidate.dedicated_service}={value:+d}")

    shared_scores = {"yes": -3, "no": 1, "unknown": -1}
    value = shared_scores[candidate.shared_infrastructure]
    score += value
    reasons.append(f"shared_infrastructure:{candidate.shared_infrastructure}={value:+d}")

    essential_scores = {"yes": -5, "no": 1, "unknown": -1}
    value = essential_scores[candidate.essential_function]
    score += value
    reasons.append(f"essential_function:{candidate.essential_function}={value:+d}")

    value = RISK_SCORE[candidate.false_positive_risk]
    score += value
    reasons.append(f"false_positive_risk:{candidate.false_positive_risk}={value:+d}")

    hard_hold = (
        candidate.shared_infrastructure == "yes"
        or candidate.essential_function == "yes"
        or candidate.dedicated_service == "no"
        or candidate.false_positive_risk == "high"
    )

    if candidate.status in {"hold", "rejected"}:
        band = "HOLD"
    elif hard_hold or score <= 3:
        band = "HOLD"
    elif score >= 8 and candidate.evidence_type not in {
        "community-report",
        "third-party-signal",
    }:
        band = "HIGH"
    else:
        band = "REVIEW"

    return CandidateScore(
        domain=candidate.domain,
        score=score,
        band=band,
        reasons=tuple(reasons),
    )
