"""
Unit tests for Gemini 3.8 Flash Assistant integration and grounding
"""
import unittest
import json
import os
import base64

class TestGeminiAssistant(unittest.TestCase):
    def setUp(self):
        self.data_path = os.path.join(os.path.dirname(__file__), "..", "core", "itinerary_data.json")
        with open(self.data_path, "r", encoding="utf-8") as f:
            self.data = json.load(f)

    def test_gemini_config_file_exists(self):
        config_path = os.path.join(os.path.dirname(__file__), "..", "web", "config.js")
        self.assertTrue(os.path.exists(config_path), "web/config.js does not exist")
        with open(config_path, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("gemini-3.8-flash", content)
        self.assertIn("TRAVEL_OS_CONFIG", content)

    def test_gemini_key_decoding(self):
        encoded = "QVEuQWI4Uk42TDh1ay1JWlZVcm1HSG9jTFgxSk4tSUExR2p3OEd5VjdSYVg5bi1sbFhDSXc="
        decoded = base64.b64decode(encoded).decode("utf-8")
        self.assertTrue(decoded.startswith("AQ.Ab8RN6L"), f"Unexpected key format: {decoded}")

    def test_itinerary_grounding_coverage(self):
        """Verify that all 29 days have primary plan, contingency, and status for AI grounding."""
        days = self.data.get("days", [])
        self.assertEqual(len(days), 29)
        for day in days:
            experiences = day.get("experiences") or day.get("daily_experience_hub")
            self.assertIsNotNone(experiences, f"Day {day['day_number']} missing experiences")
            self.assertTrue("primary" in experiences or "primary_plan" in experiences, f"Day {day['day_number']} missing primary experience")
            self.assertTrue("contingency" in experiences or "contingency_plan" in experiences, f"Day {day['day_number']} missing contingency experience")
            self.assertIn("door_to_door_logistics", day)

if __name__ == "__main__":
    unittest.main()
