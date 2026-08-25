#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 NetCalcKit contributors
"""Validate NetCalcKit source, blocklist, and allowlist files."""

from __future__ import annotations

import sys
from pathlib import Path

from build import HEADER
from domain_utils import load_domains

ROOT = Path(__file__).resolve().parents[1]
BLOCKLIST = ROOT / "blocklists" / "standard.txt"
ALLOWLIST = ROOT / "allowlists" / "allowlist.txt"
CURATED = ROOT / "sources" / "curated.txt"
FILES = (BLOCKLIST, ALLOWLIST, CURATED)


def main() -> int:
    errors: list[str] = []

    loaded: dict[Path, list[str]] = {}
    for path in FILES:
        try:
            loaded[path] = load_domains(path)
        except ValueError as error:
            errors.append(str(error).replace(str(ROOT) + "/", ""))
            loaded[path] = []

    blocklist_text = BLOCKLIST.read_text(encoding="utf-8")
    if not blocklist_text.startswith(HEADER):
        errors.append("blocklists/standard.txt: missing or stale generated header")
    if blocklist_text and not blocklist_text.endswith("\n"):
        errors.append("blocklists/standard.txt: missing final newline")

    blocklist = loaded[BLOCKLIST]
    allowlist = set(loaded[ALLOWLIST])
    overlap = sorted(set(blocklist) & allowlist)
    if overlap:
        errors.append(f"blocklist/allowlist overlap: {', '.join(overlap)}")

    expected = sorted(set(loaded[CURATED]) - allowlist)
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
