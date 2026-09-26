"""Offline contract tests for configurable live-site coverage; no network calls."""
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "real_site_smoke.py"
spec = importlib.util.spec_from_file_location("real_site_smoke", SCRIPT)
smoke = importlib.util.module_from_spec(spec)
spec.loader.exec_module(smoke)

BASE_CSV = "domain,vendor,category,evidence_file,false_positive_risk,tier,status,last_reviewed\n"
ROW = "ping.chartbeat.net,Chartbeat,web_analytics,evidence/x.md,moderate,standard,approved,2026-09-26\n"
NEW_ROW = "queue.simpleanalyticscdn.com,Simple Analytics,web_analytics,evidence/x.md,low-moderate,standard,approved,2026-09-26\n"


class LiveSiteConfigTests(unittest.TestCase):
    def write_fixture(self, case, approved=BASE_CSV + ROW):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        root = Path(temp.name)
        manifest = root / "cases.json"
        rules = root / "rules.csv"
        manifest.write_text(json.dumps({"schema_version": 1, "cases": [case]}), encoding="utf-8")
        rules.write_text(approved, encoding="utf-8")
        return manifest, rules

    @staticmethod
    def case():
        return {"vendor": "Chartbeat", "host": "ping.chartbeat.net",
                "wait_seconds": 18, "pages": ["https://www.ctvnews.ca/"]}

    def test_repo_cases_target_approved_exact_rules(self):
        cases = smoke.load_cases()
        self.assertEqual({c[1] for c in cases},
                         {"ping.chartbeat.net", "queue.simpleanalyticscdn.com"})

    def test_manifest_accepts_exact_known_domain(self):
        manifest, rules = self.write_fixture(self.case())
        cases = smoke.load_cases(manifest, rules)
        self.assertEqual(len(cases), 1)
        self.assertEqual(cases[0][1], "ping.chartbeat.net")

    def test_manifest_rejects_unapproved_or_wildcard(self):
        c = self.case()
        c["host"] = "*.chartbeat.net"
        manifest, rules = self.write_fixture(c)
        with self.assertRaises(ValueError):
            smoke.load_cases(manifest, rules)
        c["host"] = "missing.chartbeat.net"
        manifest, rules = self.write_fixture(c)
        with self.assertRaises(ValueError):
            smoke.load_cases(manifest, rules)

    def test_manifest_rejects_private_query_and_http(self):
        for bad_url in ("http://www.ctvnews.ca/",
                        "https://www.ctvnews.ca/?api_key=secret",
                        "https://person:secret@www.ctvnews.ca/",
                        "https://localhost/",
                        "https://www.ctvnews.ca:8443/"):
            with self.subTest(url=bad_url):
                c = self.case()
                c["pages"] = [bad_url]
                manifest, rules = self.write_fixture(c)
                with self.assertRaises(ValueError):
                    smoke.load_cases(manifest, rules)

    def test_manifest_rejects_empty_registry(self):
        manifest, rules = self.write_fixture(self.case())
        manifest.write_text(json.dumps({"schema_version": 1, "cases": []}), encoding="utf-8")
        with self.assertRaises(ValueError):
            smoke.load_cases(manifest, rules)

    def test_manifest_rejects_duplicate_hosts(self):
        c = self.case()
        manifest, rules = self.write_fixture(c)
        manifest.write_text(json.dumps({"schema_version": 1, "cases": [c, c]}),
                            encoding="utf-8")
        with self.assertRaises(ValueError):
            smoke.load_cases(manifest, rules)

    def test_detects_newly_approved_hosts_in_pr(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        rules = Path(temp.name) / "rules.csv"
        rules.write_text(BASE_CSV + ROW + NEW_ROW, encoding="utf-8")
        with patch.object(smoke.subprocess, "run",
                          return_value=SimpleNamespace(stdout=BASE_CSV + ROW)) as mocked:
            added = smoke.newly_approved_hosts("a" * 40, rules)
        self.assertEqual(added, {"queue.simpleanalyticscdn.com"})
        self.assertEqual(mocked.call_args.args[0][0:2], ["git", "show"])

    def test_aggressive_only_rules_do_not_trigger_standard_gate(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        rules = Path(temp.name) / "rules.csv"
        aggressive = "advanced.example.com,Vendor,telemetry,evidence/x.md,high,aggressive,approved,2026-09-26\n"
        rules.write_text(BASE_CSV + ROW + aggressive, encoding="utf-8")
        with patch.object(smoke.subprocess, "run",
                          return_value=SimpleNamespace(stdout=BASE_CSV + ROW)):
            added = smoke.newly_approved_hosts("a" * 40, rules)
        self.assertEqual(added, set())

    def test_manual_run_does_not_invent_changes(self):
        self.assertEqual(smoke.newly_approved_hosts(""), set())

    def test_invalid_base_sha_rejected(self):
        with self.assertRaises(ValueError):
            smoke.newly_approved_hosts("; do something unsafe")


if __name__ == "__main__":
    unittest.main()
