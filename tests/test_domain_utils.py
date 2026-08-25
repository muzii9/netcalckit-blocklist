#!/usr/bin/env python3
# SPDX-License-Identifier: MIT

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from domain_utils import load_domains


class DomainFileTests(unittest.TestCase):
    def load(self, content: str) -> list[str]:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "domains.txt"
            path.write_text(content, encoding="utf-8")
            return load_domains(path)

    def test_accepts_sorted_lowercase_domains_and_comments(self) -> None:
        self.assertEqual(
            self.load("# note\na.example.com\nb.example.com\n"),
            ["a.example.com", "b.example.com"],
        )

    def test_rejects_uppercase_domain(self) -> None:
        with self.assertRaisesRegex(ValueError, "invalid domain"):
            self.load("Tracker.example.com\n")

    def test_rejects_hosts_format(self) -> None:
        with self.assertRaisesRegex(ValueError, "invalid domain"):
            self.load("0.0.0.0 tracker.example.com\n")

    def test_rejects_inline_comment(self) -> None:
        with self.assertRaisesRegex(ValueError, "invalid domain"):
            self.load("tracker.example.com # reason\n")

    def test_rejects_duplicate(self) -> None:
        with self.assertRaisesRegex(ValueError, "duplicate"):
            self.load("tracker.example.com\ntracker.example.com\n")

    def test_rejects_unsorted_entries(self) -> None:
        with self.assertRaisesRegex(ValueError, "not sorted"):
            self.load("z.example.com\na.example.com\n")

    def test_rejects_ip_address_and_single_label(self) -> None:
        for value in ("127.0.0.1\n", "localhost\n"):
            with self.subTest(value=value), self.assertRaisesRegex(ValueError, "invalid domain"):
                self.load(value)


if __name__ == "__main__":
    unittest.main()
