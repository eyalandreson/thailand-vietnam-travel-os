"""
Unit tests for Cloud Agent Service (api/agent_fix.py & cloud_server.py)
"""
import unittest
import json
import os
import sys

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from api.agent_fix import process_cloud_request, handler


class TestCloudAgentService(unittest.TestCase):

    def test_process_cloud_request_structure(self):
        payload = {
            "category": "plan",
            "target_day": 4,
            "title": "Sunset Viewpoint Exploration",
            "description": "Add an evening viewpoint stop at 17:30 before homestay dinner.",
            "submitter": "Eyal Andreson"
        }
        res = process_cloud_request(payload)
        self.assertIn(res.get("status"), ["RESOLVED", "QUEUED", "REQUIRES_SPECIFICATION"])
        self.assertTrue(res.get("ticket_id", "").startswith("CR-"))
        self.assertIsInstance(res.get("diff_summary"), list)
        self.assertIn("itinerary", res)
        self.assertIn("days", res["itinerary"])

    def test_zero_pairing_guarantee(self):
        """Ensures request does NOT require client to provide any tokens or API keys."""
        payload = {
            "category": "site",
            "title": "Offline Map Layer",
            "description": "Cache topographic contour lines for mountain loop offline navigation."
        }
        res = process_cloud_request(payload)
        self.assertIn("status", res)
        self.assertIn("ticket_id", res)


if __name__ == "__main__":
    unittest.main()
