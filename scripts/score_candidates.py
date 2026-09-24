#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Score staged candidates for research prioritization; never auto-approve rules."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

from candidate_db import load_candidates, score_candidate

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = ROOT / "candidates" / "candidates.csv"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    candidates = load_candidates(args.input)
    rows: list[dict[str, str | int]] = []

    for candidate in candidates:
        scored = score_candidate(candidate)
        rows.append(
            {
                "domain": scored.domain,
                "score": scored.score,
                "band": scored.band,
                "status": candidate.status,
                "evidence_type": candidate.evidence_type,
                "false_positive_risk": candidate.false_positive_risk,
                "reasons": "; ".join(scored.reasons),
            }
        )

    counts = {"HIGH": 0, "REVIEW": 0, "HOLD": 0}
    for row in rows:
        counts[str(row["band"])] += 1

    print(
        "Candidate triage: "
        f"{len(rows)} total | HIGH {counts['HIGH']} | "
        f"REVIEW {counts['REVIEW']} | HOLD {counts['HOLD']}"
    )
    for row in rows:
        print(
            f"{str(row['band']):6} {int(row['score']):>3}  "
            f"{row['domain']}"
        )

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(
                handle,
                fieldnames=(
                    "domain",
                    "score",
                    "band",
                    "status",
                    "evidence_type",
                    "false_positive_risk",
                    "reasons",
                ),
            )
            writer.writeheader()
            writer.writerows(rows)
        print(f"Wrote triage report to {args.output}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
