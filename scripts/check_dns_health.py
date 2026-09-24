#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Check current DNS resolution health for rules or staged candidates using dig."""

from __future__ import annotations

import argparse
import csv
import shutil
import subprocess
from pathlib import Path

from candidate_db import load_candidates
from rule_db import approved_domains, load_rules

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RULES = ROOT / "rules" / "rules.csv"
DEFAULT_CANDIDATES = ROOT / "candidates" / "candidates.csv"


def dig(domain: str, record_type: str, timeout: int) -> tuple[str, str]:
    try:
        completed = subprocess.run(
            [
                "dig",
                "+short",
                f"+time={timeout}",
                "+tries=1",
                domain,
                record_type,
            ],
            text=True,
            capture_output=True,
            timeout=timeout + 2,
            check=False,
        )
    except subprocess.TimeoutExpired:
        return "", "subprocess-timeout"

    if completed.returncode != 0:
        error = completed.stderr.strip() or f"dig-exit-{completed.returncode}"
        return "", error

    answers = " ".join(
        line.strip()
        for line in completed.stdout.splitlines()
        if line.strip()
    )
    return answers, ""


def main() -> int:
    parser = argparse.ArgumentParser()
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--rules", type=Path, nargs="?", const=DEFAULT_RULES)
    source.add_argument(
        "--candidates", type=Path, nargs="?", const=DEFAULT_CANDIDATES
    )
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--timeout", type=int, default=3)
    args = parser.parse_args()

    if shutil.which("dig") is None:
        raise SystemExit("ERROR: dig is required (install dnsutils/bind-tools).")

    if args.rules is not None:
        domains = approved_domains(load_rules(args.rules))
        source_name = "rules"
    else:
        candidates = load_candidates(args.candidates)
        domains = [
            candidate.domain
            for candidate in candidates
            if candidate.status != "rejected"
        ]
        source_name = "candidates"

    rows: list[dict[str, str]] = []
    counts = {"resolving": 0, "no-address": 0, "error": 0}

    for domain in domains:
        a_answers, a_error = dig(domain, "A", args.timeout)
        aaaa_answers, aaaa_error = dig(domain, "AAAA", args.timeout)

        errors = "; ".join(
            value for value in (a_error, aaaa_error) if value
        )

        if errors and not a_answers and not aaaa_answers:
            status = "error"
        elif a_answers or aaaa_answers:
            status = "resolving"
        else:
            status = "no-address"

        counts[status] += 1
        rows.append(
            {
                "domain": domain,
                "status": status,
                "a_answers": a_answers,
                "aaaa_answers": aaaa_answers,
                "error": errors,
            }
        )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=("domain", "status", "a_answers", "aaaa_answers", "error"),
        )
        writer.writeheader()
        writer.writerows(rows)

    print(
        f"DNS health ({source_name}): {len(rows)} total | "
        f"resolving {counts['resolving']} | "
        f"no-address {counts['no-address']} | error {counts['error']}"
    )
    print(f"Wrote DNS health report to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
