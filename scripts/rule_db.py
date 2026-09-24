#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Structured rule database parsing for NetCalcKit blocklists."""

from __future__ import annotations

import csv
import ipaddress
from dataclasses import dataclass
from datetime import date
from pathlib import Path

from domain_utils import DOMAIN

REQUIRED_COLUMNS = (
    "domain",
    "vendor",
    "category",
    "evidence_file",
    "false_positive_risk",
    "tier",
    "status",
    "last_reviewed",
)
ALLOWED_RISKS = {"low", "low-moderate", "moderate", "high"}
ALLOWED_TIERS = {"lite", "standard", "aggressive"}
ALLOWED_STATUSES = {"approved", "hold", "removed"}
TIER_RANK = {"lite": 0, "standard": 1, "aggressive": 2}


@dataclass(frozen=True)
class Rule:
    domain: str
    vendor: str
    category: str
    evidence_file: str
    false_positive_risk: str
    tier: str
    status: str
    last_reviewed: str


def _validate_domain(value: str) -> bool:
    try:
        ipaddress.ip_address(value)
        return False
    except ValueError:
        return bool(DOMAIN.fullmatch(value))


def load_rules(path: Path, *, require_sorted: bool = True) -> list[Rule]:
    """Load and strictly validate the structured rule database."""
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames != list(REQUIRED_COLUMNS):
            raise ValueError(
                f"{path}: expected columns {', '.join(REQUIRED_COLUMNS)}"
            )

        rules: list[Rule] = []
        seen: set[str] = set()

        for line_number, row in enumerate(reader, start=2):
            values = {key: (row.get(key) or "").strip() for key in REQUIRED_COLUMNS}
            domain = values["domain"]

            if not _validate_domain(domain):
                raise ValueError(
                    f"{path}: line {line_number}: invalid domain {domain!r}"
                )
            if domain in seen:
                raise ValueError(
                    f"{path}: line {line_number}: duplicate domain {domain!r}"
                )
            seen.add(domain)

            for field in ("vendor", "category", "evidence_file"):
                if not values[field]:
                    raise ValueError(
                        f"{path}: line {line_number}: {field} must not be empty"
                    )

            if not values["evidence_file"].startswith("evidence/"):
                raise ValueError(
                    f"{path}: line {line_number}: evidence_file must be under evidence/"
                )
            if values["false_positive_risk"] not in ALLOWED_RISKS:
                raise ValueError(
                    f"{path}: line {line_number}: invalid false_positive_risk "
                    f"{values['false_positive_risk']!r}"
                )
            if values["tier"] not in ALLOWED_TIERS:
                raise ValueError(
                    f"{path}: line {line_number}: invalid tier {values['tier']!r}"
                )
            if values["status"] not in ALLOWED_STATUSES:
                raise ValueError(
                    f"{path}: line {line_number}: invalid status {values['status']!r}"
                )
            try:
                date.fromisoformat(values["last_reviewed"])
            except ValueError as error:
                raise ValueError(
                    f"{path}: line {line_number}: last_reviewed must be YYYY-MM-DD"
                ) from error

            rules.append(Rule(**values))

    domains = [rule.domain for rule in rules]
    if require_sorted and domains != sorted(domains):
        raise ValueError(f"{path}: rules are not sorted by domain")

    return rules


def approved_domains(rules: list[Rule]) -> list[str]:
    return sorted(rule.domain for rule in rules if rule.status == "approved")


def domains_for_tier(rules: list[Rule], tier: str) -> list[str]:
    if tier not in TIER_RANK:
        raise ValueError(f"unknown tier: {tier}")
    max_rank = TIER_RANK[tier]
    return sorted(
        rule.domain
        for rule in rules
        if rule.status == "approved" and TIER_RANK[rule.tier] <= max_rank
    )
