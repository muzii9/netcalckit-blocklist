"""Offline tests; no network, browser, credentials or real DNS required."""
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

SRC=Path(__file__).resolve().parents[1]/"scripts/false_positive_investigator.py"
spec=importlib.util.spec_from_file_location("false_positive_investigator",SRC)
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
CANDIDATES="""domain,vendor,category,evidence_url,evidence_type,dedicated_service,shared_infrastructure,essential_function,false_positive_risk,status,observed_date,notes
unseen.vendor.net,Example,analytics,https://example.com,vendor-doc,yes,no,no,moderate,hold,2026-09-26,No evidence of compatibility
bat.bing.com,Microsoft Advertising,analytics,https://example.com,vendor-doc,unknown,unknown,unknown,high,hold,2026-09-26,Retry watch
"""
REGISTRY=json.dumps({"cases":[{"host":"new.example.org","pages":["https://newsite.example.org/"]}]})

def record(req=3,intercept=0,body=1200,links=15,dom=1000,js=0,
           other=0,http=200,title=True,error=""):
    return {"http":http,"body_chars":body,"links":links,"dom_ms":dom,
            "title_present":title,"natural_requests":req,"intercepted":intercept,
            "uncaught_js_errors":js,"other_request_failures":other,
            "navigation_error":error}
class TestPolicy(unittest.TestCase):
    def setUp(self):
        self.config=m.validate_config(json.loads(m.CONFIG_FILE.read_text()))

    def test_public_urls_only(self):
        self.assertTrue(m.public_page("https://oddmuse.co.uk/"))
        for u in ("http://site.example.com/","https://localhost/",
                  "https://127.0.0.1/","https://site.example.com/?token=x",
                  "https://user:pass@site.example.com/","https://site.example.com:8443/",
                  "https://site.local/private"):
            with self.subTest(u=u):
                self.assertFalse(m.public_page(u))

    def test_invalid_config_rejected(self):
        for payload in (
            {**self.config,"schema_version":9},
            {**self.config,"site_pool":["https://localhost/"]},
            {**self.config,"max_hosts_per_run":500},
            {**self.config,"targets":self.config["targets"]+[self.config["targets"][0]]},
            {**self.config,"targets":[{"host":"*.example.com","mode":"research-only",
                                      "vendor":"x","pages":[]}]},
        ):
            with self.subTest(payload=payload):
                with self.assertRaises(ValueError):
                    m.validate_config(payload)

    def test_actual_repository_config(self):
        self.assertIn("ct.pinterest.com",{x["host"] for x in self.config["targets"]})
        self.assertEqual(self.config["max_hosts_per_run"],3)

    def test_new_approved_host_prioritized_and_includes_registry(self):
        selected,omitted=m.select_targets(self.config,CANDIDATES,REGISTRY,{"new.example.org"},week=1)
        self.assertFalse(omitted)
        self.assertEqual(selected[0]["host"],"new.example.org")
        self.assertEqual(selected[0]["source"],"NEW_APPROVED_PROPOSAL")
        self.assertIn("https://newsite.example.org/",selected[0]["pages"])

    def test_new_rules_beyond_capacity_stay_omitted(self):
        new={"a.example.org","b.example.org","c.example.org","d.example.org"}
        selected,omitted=m.select_targets(self.config,CANDIDATES,REGISTRY,new,week=2)
        self.assertEqual(len(selected),3)
        self.assertEqual(omitted,["d.example.org"])

    def test_rotating_hold_when_capacity_available(self):
        small={**self.config,"targets":[],"max_hosts_per_run":3}
        selected,_=m.select_targets(small,CANDIDATES,REGISTRY,set(),week=1)
        self.assertEqual(len(selected),1)
        self.assertEqual(selected[0]["source"],"ROTATING_HOLD")

    def test_proposed_host_sha_checked_before_git(self):
        with self.assertRaises(ValueError):
            m.proposed_hosts("HEAD;echo unsafe")

    def test_conservative_retry_burst_review(self):
        b=[record(),record()]
        f=[record(req=32,intercept=32),record(req=32,intercept=32)]
        status,why=m.classify(b,f)
        self.assertEqual(status,m.REVIEW)
        self.assertTrue(any("amplification" in r for r in why))

    def test_valid_low_request_smoke(self):
        b=[record(),record(req=4)]
        f=[record(req=4,intercept=4),record(req=4,intercept=4)]
        status,_=m.classify(b,f)
        self.assertEqual(status,m.LIMITED)

    def test_unexercised_cannot_pass(self):
        b=[record(req=0),record(req=0)]
        f=[record(intercept=3),record(intercept=3)]
        self.assertEqual(m.classify(b,f)[0],m.INCONCLUSIVE)

    def test_zero_interceptions_cannot_pass(self):
        b=[record(),record()]
        f=[record(),record()]
        self.assertEqual(m.classify(b,f)[0],m.INCONCLUSIVE)

    def test_body_breakage_flagged(self):
        b=[record(),record()]
        f=[record(body=300,intercept=3),record(body=300,intercept=3)]
        self.assertEqual(m.classify(b,f)[0],m.REVIEW)

    def test_js_regression_flagged(self):
        b=[record(js=0),record(js=0)]
        f=[record(js=5,intercept=3),record(js=5,intercept=3)]
        self.assertEqual(m.classify(b,f)[0],m.REVIEW)

    def test_other_requests_regression_flagged(self):
        b=[record(other=0),record(other=0)]
        f=[record(other=6,intercept=3),record(other=6,intercept=3)]
        self.assertEqual(m.classify(b,f)[0],m.REVIEW)

    def test_dom_degradation_flagged(self):
        b=[record(dom=800),record(dom=800)]
        f=[record(dom=4200,intercept=3),record(dom=4200,intercept=3)]
        self.assertEqual(m.classify(b,f)[0],m.REVIEW)

    def test_redirect_or_incomplete_is_inconclusive(self):
        b=[record(error="External-or-regional redirect"),record()]
        f=[record(intercept=3),record(intercept=3)]
        self.assertEqual(m.classify(b,f)[0],m.INCONCLUSIVE)

    def test_report_refuses_to_label_review_clearance(self):
        report={"utc":"2026-09-27T00:00:00Z","mode":"report-only","omitted_new_rules":[],
                "targets":[{"host":"ct.pinterest.com","source":"RESEARCH_PIN",
                            "status":m.REVIEW,"probed":[],"sites":[],"reasons":["Amplification"]}]}
        msg=m.report_text(report)
        self.assertIn("REVIEW_REQUIRED",msg)
        self.assertIn("No rules or candidate statuses were changed",msg)

if __name__=="__main__":
    unittest.main()
