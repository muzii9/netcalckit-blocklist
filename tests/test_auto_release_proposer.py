"""Offline tests for automatic *draft* RC preparation. No network or GitHub writes."""
import csv
import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from candidate_db import Candidate

spec = importlib.util.spec_from_file_location(
    "auto_release_proposer", ROOT / "scripts" / "auto_release_proposer.py"
)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


def candidate(**overrides):
    values = dict(
        domain="collect.example.com",
        vendor="Example Analytics",
        category="web_analytics",
        evidence_url="https://docs.example.com/network",
        evidence_type="vendor-doc",
        dedicated_service="unknown",
        shared_infrastructure="unknown",
        essential_function="unknown",
        false_positive_risk="unknown",
        status="research",
        observed_date="2026-09-30",
        notes="Exact collection hostname in official documentation",
    )
    values.update(overrides)
    return Candidate(**values)


def trial(mode, natural=3, intercepted=0, dom=1000):
    return {
        "mode": mode,
        "http": 200,
        "body_chars": 2000,
        "links": 20,
        "dom_ms": dom,
        "title_present": True,
        "natural_requests": natural,
        "intercepted": intercepted,
        "uncaught_js_errors": 0,
        "other_request_failures": 0,
        "navigation_error": "",
    }


def good_site(url):
    return {
        "url": url,
        "status": "LIMITED_SMOKE_PASS",
        "reasons": ["Limited smoke signals retained"],
        "trials": [
            trial("normal"),
            trial("blocked", natural=3, intercepted=3),
            trial("blocked", natural=3, intercepted=3),
            trial("normal"),
        ],
    }


def report(host="collect.example.com", status="LIMITED_SMOKE_PASS", sites=None):
    return {
        "targets": [{
            "host": host,
            "status": status,
            "sites": sites if sites is not None else [
                good_site("https://shop-one.example/"),
                good_site("https://shop-two.example/"),
            ],
        }]
    }


class AutomaticReleasePolicyTests(unittest.TestCase):
    def test_research_primary_candidate_can_reach_browser_gate(self):
        allowed, reasons = m.candidate_gate(candidate())
        self.assertTrue(allowed)
        self.assertEqual(reasons, [])

    def test_explicit_hold_never_auto_proposed(self):
        allowed, reasons = m.candidate_gate(candidate(status="hold"))
        self.assertFalse(allowed)
        self.assertTrue(any("hold" in x for x in reasons))

    def test_high_risk_and_shared_service_are_rejected(self):
        self.assertFalse(m.candidate_gate(candidate(false_positive_risk="high"))[0])
        self.assertFalse(m.candidate_gate(candidate(shared_infrastructure="yes"))[0])
        self.assertFalse(m.candidate_gate(candidate(essential_function="yes"))[0])

    def test_broad_apex_is_rejected(self):
        self.assertFalse(m.candidate_gate(candidate(domain="example.com"))[0])

    def test_mixed_use_notes_are_rejected(self):
        self.assertFalse(m.candidate_gate(candidate(notes="Same host also serves guide metadata"))[0])

    def test_sdk_delivery_category_is_rejected(self):
        self.assertFalse(m.candidate_gate(candidate(category="product_experience_sdk"))[0])

    def test_third_party_only_evidence_is_rejected(self):
        self.assertFalse(m.candidate_gate(candidate(evidence_type="third-party-signal"))[0])

    def test_selection_skips_existing_and_allowlisted(self):
        first = candidate(domain="a.collect.example.com")
        second = candidate(domain="b.collect.example.com")
        rules = [{"domain": first.domain}]
        chosen, audit = m.select_candidate([first, second], rules, set())
        self.assertEqual(chosen.domain, second.domain)
        chosen, _ = m.select_candidate([second], [], {second.domain})
        self.assertIsNone(chosen)

    def test_review_status_is_prioritized(self):
        a = candidate(domain="a.collect.example.com", status="research")
        b = candidate(domain="b.collect.example.com", status="review")
        chosen, _ = m.select_candidate([a, b], [], set())
        self.assertEqual(chosen.domain, b.domain)

    def test_investigator_config_is_one_host_and_public_pool_only(self):
        c = candidate()
        base = {
            "max_seed_pages_per_host": 6,
            "observe_seconds": 7,
            "targets": [{"host": c.domain, "pages": ["https://known.example/"]}],
            "site_pool": ["https://public.example/", "http://unsafe.example/"],
        }
        live = {"cases": [{"host": c.domain, "pages": ["https://second.example/"]}]}
        cfg = m.make_investigator_config(c, base, live)
        self.assertEqual(cfg["max_hosts_per_run"], 1)
        self.assertEqual(cfg["targets"][0]["host"], c.domain)
        self.assertEqual(cfg["site_pool"], ["https://public.example/"])
        self.assertIn("https://known.example/", cfg["targets"][0]["pages"])

    def test_two_independent_limited_sites_are_required(self):
        decision = m.report_decision(
            "collect.example.com",
            report(sites=[good_site("https://one.example/")]),
        )
        self.assertFalse(decision["ready"])
        self.assertIn("need 2", decision["reason"])
        self.assertTrue(m.report_decision("collect.example.com", report())["ready"])

    def test_review_or_inconclusive_never_becomes_ready(self):
        self.assertFalse(m.report_decision("collect.example.com", report(status="REVIEW_REQUIRED"))["ready"])
        self.assertFalse(m.report_decision("collect.example.com", report(status="INCONCLUSIVE"))["ready"])

    def test_unknown_candidate_risk_is_promoted_only_as_moderate(self):
        self.assertEqual(m.release_risk(candidate(false_positive_risk="unknown")), "moderate")
        self.assertEqual(m.release_risk(candidate(false_positive_risk="low-moderate")), "low-moderate")

    def test_apply_stages_draft_rc_files_but_does_not_publish_itself(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "candidates").mkdir()
            (root / "rules").mkdir()
            (root / "tests").mkdir()
            (root / "evidence").mkdir()
            c = candidate()
            candidate_fields = [
                "domain","vendor","category","evidence_url","evidence_type",
                "dedicated_service","shared_infrastructure","essential_function",
                "false_positive_risk","status","observed_date","notes",
            ]
            cpath = root / "candidates/candidates.csv"
            with cpath.open("w", newline="", encoding="utf-8") as f:
                w = csv.DictWriter(f, fieldnames=candidate_fields)
                w.writeheader()
                w.writerow({k:getattr(c,k) for k in candidate_fields})
            rpath = root / "rules/rules.csv"
            rule_fields = ["domain","vendor","category","evidence_file","false_positive_risk","tier","status","last_reviewed"]
            with rpath.open("w", newline="", encoding="utf-8") as f:
                w = csv.DictWriter(f, fieldnames=rule_fields)
                w.writeheader()
                w.writerow({
                    "domain":"old.example.net","vendor":"Old","category":"web_analytics",
                    "evidence_file":"evidence/old.md","false_positive_risk":"low",
                    "tier":"standard","status":"approved","last_reviewed":"2026-09-01",
                })
            cases = root / "tests/live-site-cases.json"
            cases.write_text(json.dumps({"schema_version":1,"cases":[]})+"\n")
            readme = root / "README.md"
            tick = chr(96)
            readme.write_text(
                "The current " + tick + "main" + tick +
                " list contains 1 analytics, telemetry, advertising-measurement, and observability hostnames.\n"
            )
            rep = report(c.domain)
            dec = m.report_decision(c.domain, rep)
            result = m.apply_proposal(
                c, rep, dec, candidates_path=cpath, rules_path=rpath,
                live_cases_path=cases, readme_path=readme, root=root,
            )
            self.assertTrue(result["changed"])
            self.assertEqual(result["proposed_standard_count"], 2)
            self.assertEqual(m.load_candidates(cpath), [])
            rows = m.read_rules(rpath)
            new = next(x for x in rows if x["domain"] == c.domain)
            self.assertEqual(new["status"], "approved")
            self.assertEqual(new["false_positive_risk"], "moderate")
            self.assertTrue((root / new["evidence_file"]).exists())
            manifest = json.loads(cases.read_text())
            self.assertEqual(manifest["cases"][0]["host"], c.domain)
            self.assertIn("contains 2 analytics", readme.read_text())

    def test_not_ready_decision_causes_no_changes(self):
        result = m.apply_proposal(
            candidate(), report(), {"ready":False,"host":"collect.example.com","reason":"no evidence","sites":[]}
        )
        self.assertFalse(result["changed"])


if __name__ == "__main__":
    unittest.main()
