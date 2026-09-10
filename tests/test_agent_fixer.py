"""
Unit tests for Autonomous Antigravity Agent Fixer Engine (core/agent_fixer.py)
"""
import unittest
import os
import json
import tempfile
import shutil

from core.agent_fixer import AgentFixerEngine

class TestAgentFixer(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.test_itinerary_path = os.path.join(self.test_dir, "itinerary.json")
        self.test_requests_path = os.path.join(self.test_dir, "requests.json")

        sample_itinerary = {
            "days": [
                {
                    "day_number": 1,
                    "date": "Sep 11, 2026",
                    "day_of_week": "Friday",
                    "destination": "Bangkok Base",
                    "phase": "Phase 1: Northern Vietnam",
                    "status": "CONFIRMED - BOOKED",
                    "weather_radar": {"temp_range": "28-32C", "condition": "Partly Cloudy", "attire_advice": "Light"},
                    "door_to_door_logistics": {"primary_transit": "Direct Flight", "departure_time": "11:55", "arrival_time": "13:45", "buffer_time": "3h"},
                    "accommodation_matrix": [],
                    "curated_daily_flow": {"morning": "Arrival", "afternoon": "Check in", "evening": "Dinner"},
                    "essential_checklist": ["Confirm transit"]
                },
                {
                    "day_number": 15,
                    "date": "Sep 25, 2026",
                    "day_of_week": "Friday",
                    "destination": "Koh Samui",
                    "phase": "Phase 2: Gulf of Thailand",
                    "status": "VETTED",
                    "weather_radar": {"temp_range": "29-33C", "condition": "Tropical Sun", "attire_advice": "Beachwear"},
                    "door_to_door_logistics": {"primary_transit": "Speedboat", "departure_time": "10:00", "arrival_time": "11:30", "buffer_time": "1h"},
                    "accommodation_matrix": [],
                    "curated_daily_flow": {"morning": "Beach", "afternoon": "Snorkel", "evening": "Sunset"},
                    "essential_checklist": []
                }
            ]
        }
        with open(self.test_itinerary_path, "w", encoding="utf-8") as f:
            json.dump(sample_itinerary, f, indent=2)

        sample_requests = [
            {
                "id": "CR-20260911-001",
                "category": "plan",
                "target_day": 1,
                "title": "Stay at Bangkok Heritage Hotel",
                "description": "Please update hotel to Bangkok Heritage Hotel and add evening street food crawl",
                "priority": "normal",
                "submitter": "Eyal",
                "status": "QUEUED"
            },
            {
                "id": "FEAT-20260911-001",
                "category": "site",
                "target_day": None,
                "title": "Add Currency Quick Tap",
                "description": "Add quick tap buttons for common amounts in currency modal",
                "priority": "normal",
                "submitter": "Eyal",
                "status": "QUEUED"
            }
        ]
        with open(self.test_requests_path, "w", encoding="utf-8") as f:
            json.dump(sample_requests, f, indent=2)

        self.fixer = AgentFixerEngine(
            itinerary_path=self.test_itinerary_path,
            requests_path=self.test_requests_path
        )

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_find_target_day_index(self):
        days = [{"day_number": 1, "destination": "Bangkok Base"}, {"day_number": 2, "destination": "Sa Pa"}]
        self.assertEqual(self.fixer.find_target_day_index(days, 1, ""), 0)
        self.assertEqual(self.fixer.find_target_day_index(days, None, "Going to Sa Pa today"), 1)
        self.assertEqual(self.fixer.find_target_day_index(days, None, "Change day 2 itinerary"), 1)

    def test_process_plan_change(self):
        result = self.fixer.process_ticket("CR-20260911-001")
        self.assertEqual(result.get("status"), "RESOLVED")
        self.assertIsNotNone(result.get("critic_audit"))
        self.assertTrue(len(result.get("diff_summary")) >= 1)

        # Verify itinerary file was updated
        with open(self.test_itinerary_path, "r", encoding="utf-8") as f:
            updated = json.load(f)
        day1 = updated["days"][0]
        self.assertTrue(len(day1["accommodation_matrix"]) > 0)
        # Phase 1 constraint check
        self.assertIn("Twin Beds", day1["accommodation_matrix"][0]["room_spec"])

    def test_process_site_change(self):
        result = self.fixer.process_ticket("FEAT-20260911-001")
        self.assertEqual(result.get("status"), "QUEUED_FOR_AGENT")
        self.assertIn(".agents/tasks", result.get("resolution"))

    def test_process_all_pending(self):
        summary = self.fixer.process_all_pending()
        self.assertEqual(summary.get("total_pending_found"), 2)
        self.assertEqual(summary.get("processed_count"), 2)

if __name__ == "__main__":
    unittest.main()
