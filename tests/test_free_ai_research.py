"""Offline regression tests for free-tier research budget and exact-host filtering."""
import importlib.util
from pathlib import Path
import unittest

p = Path(__file__).resolve().parents[1] / "scripts/free_ai_research.py"
spec = importlib.util.spec_from_file_location("free_ai_research", p)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

class ResearchBudgetTests(unittest.TestCase):
    def test_daily_search_ceiling(self):
        self.assertLessEqual(module.MAX_SEARCHES, 8)

    def test_exact_host_not_substring(self):
        hits = [{"content_excerpt": "https://collect.example.com/v1"}]
        self.assertTrue(module.exact_excerpt_host("collect.example.com", hits))
        self.assertFalse(module.exact_excerpt_host("lect.example.com", hits))
        self.assertFalse(module.exact_excerpt_host("example.com", hits))

    def test_known_host_filter_inputs(self):
        known = module.known_hosts()
        self.assertIn("cdn.pendo.io", known)
        self.assertIn("bam.nr-data.net", known)

if __name__ == "__main__":
    unittest.main()
