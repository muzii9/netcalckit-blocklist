#!/usr/bin/env python3
# SPDX-License-Identifier: MIT

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from rule_db import domains_for_tier, load_rules  # noqa: E402


HEADER = (
    "domain,vendor,category,evidence_file,false_positive_risk,"
    "tier,status,last_reviewed\n"
)


class RuleDatabaseTests(unittest.TestCase):
    def write_csv(self, body: str) -> Path:
        temp = tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", newline="", delete=False
        )
        temp.write(HEADER + body)
        temp.close()
        self.addCleanup(Path(temp.name).unlink)
        return Path(temp.name)

    def test_valid_rows_load(self) -> None:
        path = self.write_csv(
            "a.example.com,Vendor,analytics,evidence/a.md,low,standard,"
            "approved,2026-09-24\n"
            "b.example.com,Vendor,telemetry,evidence/b.md,moderate,"
            "aggressive,hold,2026-09-24\n"
        )
        rules = load_rules(path)
        self.assertEqual([rule.domain for rule in rules], [
            "a.example.com", "b.example.com"
        ])

    def test_duplicate_domain_rejected(self) -> None:
        path = self.write_csv(
            "a.example.com,Vendor,analytics,evidence/a.md,low,standard,"
            "approved,2026-09-24\n"
            "a.example.com,Vendor,analytics,evidence/a.md,low,standard,"
            "approved,2026-09-24\n"
        )
        with self.assertRaisesRegex(ValueError, "duplicate domain"):
            load_rules(path)

    def test_unsorted_rows_rejected(self) -> None:
        path = self.write_csv(
            "b.example.com,Vendor,analytics,evidence/a.md,low,standard,"
            "approved,2026-09-24\n"
            "a.example.com,Vendor,analytics,evidence/a.md,low,standard,"
            "approved,2026-09-24\n"
        )
        with self.assertRaisesRegex(ValueError, "not sorted"):
            load_rules(path)

    def test_invalid_status_rejected(self) -> None:
        path = self.write_csv(
            "a.example.com,Vendor,analytics,evidence/a.md,low,standard,"
            "maybe,2026-09-24\n"
        )
        with self.assertRaisesRegex(ValueError, "invalid status"):
            load_rules(path)

    def test_invalid_date_rejected(self) -> None:
        path = self.write_csv(
            "a.example.com,Vendor,analytics,evidence/a.md,low,standard,"
            "approved,24-09-2026\n"
        )
        with self.assertRaisesRegex(ValueError, "last_reviewed"):
            load_rules(path)

    def test_tier_selection_is_cumulative(self) -> None:
        path = self.write_csv(
            "a.example.com,Vendor,analytics,evidence/a.md,low,lite,"
            "approved,2026-09-24\n"
            "b.example.com,Vendor,analytics,evidence/b.md,low,standard,"
            "approved,2026-09-24\n"
            "c.example.com,Vendor,analytics,evidence/c.md,low,aggressive,"
            "approved,2026-09-24\n"
        )
        rules = load_rules(path)
        self.assertEqual(domains_for_tier(rules, "standard"), [
            "a.example.com", "b.example.com"
        ])


if __name__ == "__main__":
    unittest.main()
