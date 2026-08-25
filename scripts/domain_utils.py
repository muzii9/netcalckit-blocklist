#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Shared strict parsing for NetCalcKit domain data files."""

from __future__ import annotations

import re
import ipaddress
from pathlib import Path

DOMAIN = re.compile(
    r"(?=^.{1,253}$)(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+"
    r"[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?$"
)


def active_entries(path: Path) -> list[tuple[int, str]]:
    """Return non-comment entries with their source line numbers."""
    return [
        (number, line.strip())
        for number, line in enumerate(
            path.read_text(encoding="utf-8").splitlines(), start=1
        )
        if line.strip() and not line.lstrip().startswith(("#", "!", "["))
    ]


def load_domains(path: Path, *, require_sorted: bool = True) -> list[str]:
    """Load a strict one-domain-per-line file or raise a useful error."""
    entries = active_entries(path)
    invalid: list[tuple[int, str]] = []
    for number, value in entries:
        try:
            ipaddress.ip_address(value)
            is_ip_address = True
        except ValueError:
            is_ip_address = False
        if is_ip_address or not DOMAIN.fullmatch(value):
            invalid.append((number, value))
    if invalid:
        details = ", ".join(f"line {number}: {value!r}" for number, value in invalid)
        raise ValueError(f"{path}: invalid domain rule(s): {details}")

    domains = [value for _, value in entries]
    if len(domains) != len(set(domains)):
        raise ValueError(f"{path}: duplicate rules found")
    if require_sorted and domains != sorted(domains):
        raise ValueError(f"{path}: rules are not sorted")
    return domains
