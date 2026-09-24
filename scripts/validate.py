#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 NetCalcKit contributors
"""Validate NetCalcKit rule metadata and generated blocklist files."""

from __future__ import annotations

import sys
from pathlib import Path

from build import CURATED_HEADER, HEADER
from domain_utils import load_domains
from rule_db import approved_domains, domains_for_tier, load_rules

ROOT = Path(__file__).resolve().parents[1]
RULES = ROOT / "rules" / "rules.csv"
BLOCKLIST = ROOT / "blocklists" / "standard.txt"
ALLOWLIST = ROOT / "allowlists" / "allowlist.txt"
CURATED = ROOT / "sources" / "curated.txt"


def main() -> int:
    errors: list[str] = []

    try:
        rules = load_rules(RULES)
    except ValueError as error:
        errors.append(str(error).replace(str(ROOT) + "/", ""))
        rules = []

    loaded: dict[Path, list[str]] = {}
    for path in (BLOCKLIST, ALLOWLIST, CURATED):
        try:
            loaded[path] = load_domains(path)
        except ValueError as error:
            errors.append(str(error).replace(str(ROOT) + "/", ""))
            loaded[path] = []

    for rule in rules:
        evidence_path = ROOT / rule.evidence_file
        if not evidence_path.is_file():
            errors.append(
                f"rules/rules.csv: {rule.domain}: missing evidence file "
                f"{rule.evidence_file}"
            )

    curated_text = CURATED.read_text(encoding="utf-8")
    if not curated_text.startswith(CURATED_HEADER):
        errors.append("sources/curated.txt: missing or stale generated header")
    if curated_text and not curated_text.endswith("\n"):
        errors.append("sources/curated.txt: missing final newline")

    blocklist_text = BLOCKLIST.read_text(encoding="utf-8")
    if not blocklist_text.startswith(HEADER):
        errors.append("blocklists/standard.txt: missing or stale generated header")
    if blocklist_text and not blocklist_text.endswith("\n"):
        errors.append("blocklists/standard.txt: missing final newline")

    curated = loaded[CURATED]
    expected_curated = approved_domains(rules)
    if curated != expected_curated:
        errors.append(
            "sources/curated.txt is not reproducible from approved rows in "
            "rules/rules.csv; run scripts/build.py"
        )

    allowlist = set(loaded[ALLOWLIST])
    blocklist = loaded[BLOCKLIST]
    expected_standard = sorted(set(domains_for_tier(rules, "standard")) - allowlist)
    if blocklist != expected_standard:
        errors.append(
            "blocklists/standard.txt is not reproducible from rules/rules.csv "
            "minus allowlists/allowlist.txt; run scripts/build.py"
        )

    overlap = sorted(set(blocklist) & allowlist)
    if overlap:
        errors.append(f"blocklist/allowlist overlap: {', '.join(overlap)}")

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print(
        "Validation passed: "
        f"{len(rules)} metadata rows, {len(blocklist)} standard rules."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
