"""Pure checks for the Pinterest A/B risk triage (no browser/network in unit tests)."""
import importlib.util
import unittest
from pathlib import Path

source = Path(__file__).resolve().parents[1] / "scripts/pinterest_retry_audit.py"
spec = importlib.util.spec_from_file_location("pinterest_retry_audit", source)
audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)

def trial(requests=3, intercepted=0, body=6000, dom_ms=400,
          http=200, title=True):
    return {"requests": requests, "intercepted": intercepted, "body": body,
            "dom_ms": dom_ms, "http": http, "title": title}

class PinterestRetryAuditTests(unittest.TestCase):
    def test_previous_burst_requires_review(self):
        baseline = [trial(), trial()]
        blocked = [trial(requests=32, intercepted=32), trial(requests=32, intercepted=32)]
        status, reasons = audit.audit_pair(baseline, blocked)
        self.assertEqual(status, "review-required")
        self.assertTrue(any("Repeat-request amplification" in x for x in reasons))

    def test_missing_natural_requests_are_inconclusive(self):
        status, _ = audit.audit_pair([trial(requests=0), trial()], [trial(intercepted=1)] * 2)
        self.assertEqual(status, "inconclusive")

    def test_simple_low_request_comparison(self):
        status, reasons = audit.audit_pair(
            [trial(), trial(requests=4)],
            [trial(requests=4, intercepted=4), trial(requests=4, intercepted=4)])
        self.assertEqual(status, "limited-smoke-pass")

    def test_body_regression_requires_review(self):
        status, reasons = audit.audit_pair(
            [trial(), trial()],
            [trial(requests=3, intercepted=3, body=1000),
             trial(requests=3, intercepted=3, body=1000)])
        self.assertEqual(status, "review-required")
        self.assertTrue(any("rendering" in x for x in reasons))

    def test_dom_timing_warning_requires_review(self):
        status, reasons = audit.audit_pair(
            [trial(), trial()],
            [trial(requests=3, intercepted=3, dom_ms=3200),
             trial(requests=3, intercepted=3, dom_ms=3200)])
        self.assertEqual(status, "review-required")
        self.assertTrue(any("timing warning" in x for x in reasons))

    def test_missing_repeat_is_inconclusive(self):
        status, _ = audit.audit_pair([trial()], [trial()])
        self.assertEqual(status, "inconclusive")

if __name__ == "__main__":
    unittest.main()
