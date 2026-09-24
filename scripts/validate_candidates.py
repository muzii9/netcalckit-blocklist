#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Validate staged candidates against the published rule and allowlist data."""

from __future__ import annotations

import sys
from pathlib import Path

from candidate_db import load_candidates
from domain_utils import load_domains
from rule_db import load_rules

ROOT = Path(__file__).resolve().parents[1]
CANDIDATES = ROOT / "candidates" / "candidates.csv"
RULES = ROOT / "rules" / "rules.csv"
ALLOWLIST = ROOT / "allowlists" / "allowlist.txt"


def main() -> int:
    errors: list[str] = []

    try:
        candidates = load_candidates(CANDIDATES)
    except ValueError as error:
        print(f"ERROR: {str(error).replace(str(ROOT) + '/', '')}", file=sys.stderr)
        return 1

    try:
        rules = load_rules(RULES)
    except ValueError as error:
        errors.append(str(error).replace(str(ROOT) + "/", ""))
        rules = []

    try:
        allowlisted = set(load_domains(ALLOWLIST))
    except ValueError as error:
        errors.append(str(error).replace(str(ROOT) + "/", ""))
        allowlisted = set()

    rule_domains = {rule.domain for rule in rules}

    for candidate in candidates:
        if candidate.domain in rule_domains:
            errors.append(
                f"candidates/candidates.csv: {candidate.domain} already exists "
                "in rules/rules.csv"
            )
        if candidate.domain in allowlisted:
            errors.append(
                f"candidates/candidates.csv: {candidate.domain} is allowlisted"
            )

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print(f"Candidate validation passed: {len(candidates)} staged candidate(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
