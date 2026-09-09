"""
Unit Tests for Dual-Sync Integrity
"""
import unittest
import os
import sys
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from core.sync_engine import DualSyncEngine

class TestDualSync(unittest.TestCase):
    def test_sync_execution_and_file_parity(self):
        engine = DualSyncEngine()
        result = engine.execute_dual_sync()

        self.assertEqual(result["status"], "DUAL_SYNC_COMPLETED")
        self.assertEqual(result["total_days"], 29)
        self.assertTrue(result["integrity_verified"])

        # Check that web data JSON matches master itinerary
        with open("core/itinerary_data.json", "r", encoding="utf-8") as f:
            master = json.load(f)
        with open("web/data.json", "r", encoding="utf-8") as f:
            web_data = json.load(f)

        self.assertEqual(len(master["days"]), len(web_data["days"]))
        self.assertEqual(master["title"], web_data["title"])

        # Check Google Doc HTML generated
        doc_path = os.path.join("google_docs", "master_itinerary_doc.html")
        self.assertTrue(os.path.exists(doc_path))
        with open(doc_path, "r", encoding="utf-8") as f:
            html = f.read()
        self.assertIn("Master Itinerary: Thailand & Vietnam", html)
        self.assertIn("Day 1 (Friday, 2026-09-11)", html)
        self.assertIn("Day 29 (Friday, 2026-10-09)", html)

if __name__ == "__main__":
    unittest.main()
