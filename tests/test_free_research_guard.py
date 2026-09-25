"""Regression tests for conservative documentation hostname staging."""
import importlib.util
import pathlib
import unittest

path = pathlib.Path(__file__).resolve().parents[1] / "scripts/free_research.py"
spec = importlib.util.spec_from_file_location("free_research", path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

class CollectorGuardTests(unittest.TestCase):
    def test_reject_non_collection_and_mixed_use_hosts(self):
        for host in ("academy.pendo.io", "support.pendo.io", "app.eu.pendo.io",
                     "portal.pendo.io", "cdn.pendo.io", "data.pendo.io",
                     "api.feedback.eu.pendo.io", "agent.pendo.io",
                     "collect.app.pendo.io", "srm.cdn.contentsquare.net"):
            with self.subTest(host=host):
                self.assertFalse(module.plausible_collector(host))

    def test_allow_only_plausible_hosts_still_hold(self):
        for host in ("collect.example.com", "ingest.example.com",
                     "srm.af.contentsquare.net", "events.vendor.example"):
            with self.subTest(host=host):
                self.assertTrue(module.plausible_collector(host))

if __name__ == "__main__":
    unittest.main()
