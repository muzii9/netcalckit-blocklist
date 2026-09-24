#!/usr/bin/env python3
# SPDX-License-Identifier: MIT

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from candidate_db import load_candidates, score_candidate  # noqa: E402


HEADER = (
    "domain,vendor,category,evidence_url,evidence_type,dedicated_service,"
    "shared_infrastructure,essential_function,false_positive_risk,status,"
    "observed_date,notes\n"
)


class CandidateDatabaseTests(unittest.TestCase):
    def write_csv(self, body: str) -> Path:
        temp = tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", newline="", delete=False
        )
        temp.write(HEADER + body)
        temp.close()
        self.addCleanup(Path(temp.name).unlink)
        return Path(temp.name)

    def test_empty_queue_is_valid(self) -> None:
        path = self.write_csv("")
        self.assertEqual(load_candidates(path), [])

    def test_high_signal_candidate_scores_high(self) -> None:
        path = self.write_csv(
            "track.example.com,Vendor,analytics,https://example.com/docs,"
            "vendor-doc,yes,no,no,low,new,2026-09-24,exact telemetry host\n"
        )
        candidate = load_candidates(path)[0]
        scored = score_candidate(candidate)
        self.assertEqual(scored.band, "HIGH")
        self.assertGreaterEqual(scored.score, 8)

    def test_shared_infrastructure_forces_hold(self) -> None:
        path = self.write_csv(
            "shared.example.com,Vendor,analytics,https://example.com/docs,"
            "vendor-doc,yes,yes,no,low,new,2026-09-24,shared host\n"
        )
        candidate = load_candidates(path)[0]
        self.assertEqual(score_candidate(candidate).band, "HOLD")

    def test_essential_function_forces_hold(self) -> None:
        path = self.write_csv(
            "auth.example.com,Vendor,auth,https://example.com/docs,"
            "vendor-doc,yes,no,yes,low,new,2026-09-24,auth endpoint\n"
        )
        candidate = load_candidates(path)[0]
        self.assertEqual(score_candidate(candidate).band, "HOLD")

    def test_third_party_signal_cannot_score_high(self) -> None:
        path = self.write_csv(
            "track.example.com,Vendor,analytics,https://example.com/report,"
            "third-party-signal,yes,no,no,low,new,2026-09-24,discovery only\n"
        )
        candidate = load_candidates(path)[0]
        self.assertNotEqual(score_candidate(candidate).band, "HIGH")

    def test_duplicate_domain_rejected(self) -> None:
        row = (
            "a.example.com,Vendor,analytics,https://example.com/docs,"
            "vendor-doc,yes,no,no,low,new,2026-09-24,note\n"
        )
        path = self.write_csv(row + row)
        with self.assertRaisesRegex(ValueError, "duplicate domain"):
            load_candidates(path)

    def test_unsorted_queue_rejected(self) -> None:
        path = self.write_csv(
            "b.example.com,Vendor,analytics,https://example.com/docs,"
            "vendor-doc,yes,no,no,low,new,2026-09-24,note\n"
            "a.example.com,Vendor,analytics,https://example.com/docs,"
            "vendor-doc,yes,no,no,low,new,2026-09-24,note\n"
        )
        with self.assertRaisesRegex(ValueError, "not sorted"):
            load_candidates(path)

    def test_http_evidence_rejected(self) -> None:
        path = self.write_csv(
            "a.example.com,Vendor,analytics,http://example.com/docs,"
            "vendor-doc,yes,no,no,low,new,2026-09-24,note\n"
        )
        with self.assertRaisesRegex(ValueError, "https URL"):
            load_candidates(path)


if __name__ == "__main__":
    unittest.main()
