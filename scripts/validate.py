#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 NetCalcKit contributors
"""Validate NetCalcKit source, blocklist, and allowlist files."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BLOCKLIST = ROOT / "blocklists" / "standard.txt"
ALLOWLIST = ROOT / "allowlists" / "allowlist.txt"
CURATED = ROOT / "sources" / "curated.txt"
FILES = (BLOCKLIST, ALLOWLIST, CURATED)
DOMAIN = re.compile(
    r"(?=^.{1,253}$)(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+"
    r"[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?$"
)


def rules(path: Path) -> list[str]:
    return [
        line.strip()
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.lstrip().startswith(("#", "!", "["))
    ]


def main() -> int:
    errors: list[str] = []

    for path in FILES:
        entries = rules(path)
        relative = path.relative_to(ROOT)

        invalid = [entry for entry in entries if not DOMAIN.fullmatch(entry)]
        if invalid:
            errors.append(f"{relative}: invalid domain rule(s): {', '.join(invalid)}")
        if entries != sorted(entries):
            errors.append(f"{relative}: rules are not sorted")
        if len(entries) != len(set(entries)):
            errors.append(f"{relative}: duplicate rules found")

    blocklist = rules(BLOCKLIST)
    allowlist = set(rules(ALLOWLIST))
    overlap = sorted(set(blocklist) & allowlist)
    if overlap:
        errors.append(f"blocklist/allowlist overlap: {', '.join(overlap)}")

    expected = sorted(set(rules(CURATED)) - allowlist)
    if blocklist != expected:
        errors.append(
            "blocklists/standard.txt is not reproducible from "
            "sources/curated.txt minus allowlists/allowlist.txt; run scripts/build.py"
        )

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print("Validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
