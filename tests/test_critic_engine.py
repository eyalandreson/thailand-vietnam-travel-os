"""
Unit Tests for Multi-Pass Adversarial Critic Engine
"""
import unittest
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from core.critic_engine import AdversarialCriticEngine

class TestCriticEngine(unittest.TestCase):
    def setUp(self):
        self.critic = AdversarialCriticEngine()

    def test_pass_1_rejects_nightclub_noise(self):
        noisy_hotel = {
            "hotel_name": "Party Central Hostel",
            "room_spec": "Twin Room",
            "critic_notes": "Located right above deafening club with nightclub bass all night.",
            "critic_score": 9.0
        }
        passed, score, issues = self.critic.evaluate_hotel(noisy_hotel, "Phase 1: Vietnam", "Hanoi")
        self.assertFalse(passed)
        self.assertTrue(any("Pass 1 Failure" in i for i in issues))

    def test_pass_2_rejects_mold_in_reviews(self):
        moldy_hotel = {
            "hotel_name": "Damp Caves Retreat",
            "room_spec": "Twin Room",
            "critic_notes": "Beautiful views but recurring mold and mildew complaints.",
            "critic_score": 8.8
        }
        passed, score, issues = self.critic.evaluate_hotel(moldy_hotel, "Phase 1: Vietnam", "Ninh Binh")
        self.assertFalse(passed)
        self.assertTrue(any("Pass 2 Failure" in i for i in issues))

    def test_pass_3_rejects_single_bed_in_phase_1(self):
        double_bed_only = {
            "hotel_name": "Hanoi Boutique",
            "room_spec": "One King Bed only",
            "critic_notes": "Very quiet luxury room.",
            "critic_score": 9.2
        }
        passed, score, issues = self.critic.evaluate_hotel(double_bed_only, "Phase 1: Vietnam", "Hanoi")
        self.assertFalse(passed)
        self.assertTrue(any("Pass 3 Failure [Bed Spec Mismatch]" in i for i in issues))

    def test_approved_hotel_passes_cleanly(self):
        perfect_resort = {
            "hotel_name": "Anantara Rasananda Koh Phangan Villas",
            "room_spec": "Ocean Pool Suite (Romantic King Bed)",
            "critic_notes": "World-class quiet sanctuary away from construction, zero mold.",
            "critic_score": 9.6
        }
        passed, score, issues = self.critic.evaluate_hotel(perfect_resort, "Phase 2: Thailand", "Koh Phangan")
        self.assertTrue(passed)
        self.assertGreaterEqual(score, 8.5)
        self.assertEqual(len(issues), 0)

if __name__ == "__main__":
    unittest.main()
