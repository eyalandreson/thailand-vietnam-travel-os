"""
Automated Integrity Tests for 29-Day Itinerary Dataset
"""
import unittest
import json
import os
from datetime import datetime, timedelta

class TestItineraryIntegrity(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        path = os.path.join(os.path.dirname(__file__), "..", "core", "itinerary_data.json")
        with open(path, "r", encoding="utf-8") as f:
            cls.data = json.load(f)

    def test_total_calendar_days_and_dates(self):
        """Verify exactly 29 days from 2026-09-11 to 2026-10-09 with zero date gaps."""
        days = self.data.get("days", [])
        self.assertEqual(len(days), 29, f"Expected 29 days, got {len(days)}")

        start_date = datetime.strptime("2026-09-11", "%Y-%m-%d")
        for idx, day in enumerate(days):
            expected_date = (start_date + timedelta(days=idx)).strftime("%Y-%m-%d")
            self.assertEqual(day["day_number"], idx + 1)
            self.assertEqual(day["date"], expected_date)

    def test_phase_1_bed_configuration(self):
        """Verify Phase 1 (Vietnam Guys Trip) enforces Twin Beds / 2 Separate Beds."""
        for day in self.data.get("days", []):
            if day["day_number"] in range(1, 14): # Sep 11 to Sep 23
                for hotel in day.get("accommodation_matrix", []):
                    spec = hotel.get("room_spec", "").lower()
                    self.assertTrue(
                        any(t in spec for t in ["twin", "two bed", "two separate", "single bed", "bunk"]),
                        f"Day {day['day_number']} Hotel '{hotel['hotel_name']}' lacks twin bed specification: {spec}"
                    )

    def test_phase_2_bed_configuration(self):
        """Verify Phase 2 (Thailand Couple Trip) enforces Romantic King / Ocean View."""
        for day in self.data.get("days", []):
            if day["day_number"] >= 14 and day["accommodation_matrix"]: # Sep 24 onwards
                for hotel in day.get("accommodation_matrix", []):
                    spec = hotel.get("room_spec", "").lower()
                    self.assertTrue(
                        any(t in spec for t in ["king", "suite", "villa", "bungalow", "ocean", "river"]),
                        f"Day {day['day_number']} Hotel '{hotel['hotel_name']}' lacks king/romantic spec: {spec}"
                    )

    def test_confirmed_references_present(self):
        """Verify critical confirmed booking references exist in itinerary."""
        data_str = json.dumps(self.data)
        self.assertIn("G5M8CF", data_str, "Emirates flight booking G5M8CF missing!")
        self.assertIn("1145-554-179", data_str, "Flight booking 1145-554-179 missing!")
        self.assertIn("697155847", data_str, "Sukhon Hotel booking 697155847 missing!")
        self.assertIn("30C4358", data_str, "TDAC card #30C4358 missing!")
        self.assertIn("9KDEH2", data_str, "Flight booking 9KDEH2 missing!")
        self.assertIn("AIRPORTELs", data_str, "AIRPORTELs luggage plan missing!")

    def test_gulf_pacing_calibration(self):
        """Verify Gulf islands total 13 nights (1 Samui + 6 Phangan + 6 Tao) + 2 Bangkok."""
        samui_days = [d for d in self.data.get("days", []) if "Samui" in d["destination"] and d["day_number"] == 14]
        phangan_days = [d for d in self.data.get("days", []) if "Phangan" in d["destination"] and d["day_number"] in range(15, 21)]
        tao_days = [d for d in self.data.get("days", []) if "Tao" in d["destination"] and d["day_number"] in range(21, 27)]
        bkk_finale_days = [d for d in self.data.get("days", []) if d["day_number"] in [27, 28]]

        self.assertEqual(len(samui_days), 1, "Expected 1 night Samui decompression")
        self.assertEqual(len(phangan_days), 6, "Expected 6 nights Koh Phangan")
        self.assertEqual(len(tao_days), 6, "Expected 6 nights Koh Tao")
        self.assertEqual(len(bkk_finale_days), 2, "Expected 2 nights Bangkok Finale")

    def test_confirmed_vs_unbooked_status_integrity(self):
        """Verify strict segregation: only the 5 true bookings are marked CONFIRMED, all others UNBOOKED."""
        confirmed_count = 0
        unbooked_count = 0
        for day in self.data.get("days", []):
            for hotel in day.get("accommodation_matrix", []):
                status = hotel.get("status", "")
                if "CONFIRMED" in status:
                    confirmed_count += 1
                    self.assertIn("Sukhon", hotel["hotel_name"])
                elif "UNBOOKED" in status or "ACTION REQUIRED" in status:
                    unbooked_count += 1

        self.assertEqual(confirmed_count, 1, "Only Sukhon Hotel should be marked CONFIRMED accommodation.")
        self.assertGreaterEqual(unbooked_count, 20, "All pending hotels should be marked ACTION REQUIRED - UNBOOKED.")

    def test_all_days_have_dual_experiences(self):
        """Verify all 29 days contain Plan A (Primary) and Plan B (Contingency) with rich metadata."""
        days = self.data.get("days", [])
        self.assertEqual(len(days), 29)
        for day in days:
            d_num = day["day_number"]
            exp = day.get("experiences")
            self.assertIsNotNone(exp, f"Day {d_num} is missing experiences block")
            self.assertIn("primary", exp, f"Day {d_num} is missing primary experience")
            self.assertIn("contingency", exp, f"Day {d_num} is missing contingency experience")

            p = exp["primary"]
            self.assertTrue(len(p.get("title", "")) > 0, f"Day {d_num} primary title is empty")
            self.assertTrue(len(p.get("duration", "")) > 0, f"Day {d_num} primary duration is empty")
            self.assertTrue(len(p.get("cost_estimate", "")) > 0, f"Day {d_num} primary cost is empty")
            self.assertTrue(len(p.get("time_sensitive_tip", "")) > 0, f"Day {d_num} primary tip is empty")

            c = exp["contingency"]
            self.assertTrue(len(c.get("title", "")) > 0, f"Day {d_num} contingency title is empty")
            self.assertTrue(len(c.get("trigger", "")) > 0, f"Day {d_num} contingency trigger is empty")
            self.assertTrue(len(c.get("cost_estimate", "")) > 0, f"Day {d_num} contingency cost is empty")

    def test_transit_days_have_transport_module(self):
        """Verify that designated transit days have door-to-door transport modules."""
        key_transit_days = [1, 2, 3, 5, 7, 9, 12, 14, 15, 21, 27, 29]
        days_map = {d["day_number"]: d for d in self.data.get("days", [])}
        for d_num in key_transit_days:
            day = days_map[d_num]
            trans = day.get("transport_module")
            self.assertIsNotNone(trans, f"Day {d_num} should have transport_module")
            route_val = trans.get("route") or trans.get("route_title") or ""
            self.assertTrue(len(route_val) > 0, f"Day {d_num} transport title empty")
            self.assertTrue(len(trans.get("pickup_hub", "")) > 0, f"Day {d_num} pickup hub empty")
            self.assertTrue(len(trans.get("dropoff_terminal", "")) > 0, f"Day {d_num} dropoff terminal empty")
            self.assertTrue(len(trans.get("duration", "")) > 0, f"Day {d_num} duration empty")
            self.assertTrue(len(trans.get("booking_url", "")) > 0, f"Day {d_num} booking url empty")

    def test_packing_master_list_integrity(self):
        """Verify Split-Luggage packing master list contains Bag A, Bag B, and Pre-departure."""
        packing = self.data.get("packing_master_list")
        self.assertIsNotNone(packing, "packing_master_list is missing from root")
        self.assertIn("bag_a_backpack", packing)
        self.assertIn("bag_b_suitcase", packing)
        self.assertIn("pre_departure_inspection", packing)

        self.assertGreaterEqual(len(packing["bag_a_backpack"]), 10, "Bag A should have >= 10 items")
        self.assertGreaterEqual(len(packing["bag_b_suitcase"]), 10, "Bag B should have >= 10 items")
        self.assertGreaterEqual(len(packing["pre_departure_inspection"]), 5, "Pre-departure should have >= 5 items")

    def test_translations_dictionary_integrity(self):
        """Verify Offline Translations phrasebook contains essential categories and dual-language scripts."""
        trans = self.data.get("translations_dictionary")
        self.assertIsNotNone(trans, "translations_dictionary is missing from root")
        self.assertIn("taxi_transit", trans)
        self.assertIn("food_dietary", trans)
        self.assertIn("emergency_medical", trans)
        self.assertIn("airport_luggage", trans)

        for cat, phrases in trans.items():
            self.assertGreaterEqual(len(phrases), 4, f"Category {cat} should have >= 4 phrases")
            for p in phrases:
                self.assertTrue(len(p.get("en", "")) > 0)
                self.assertTrue(len(p.get("th", "")) > 0)
                self.assertTrue(len(p.get("th_phonetic", "")) > 0)
                self.assertTrue(len(p.get("vi", "")) > 0)
                self.assertTrue(len(p.get("vi_phonetic", "")) > 0)

    def test_currency_benchmarks_integrity(self):
        """Verify 4-way Currency benchmarks exist with valid rates and advisories."""
        curr = self.data.get("currency_benchmarks")
        self.assertIsNotNone(curr, "currency_benchmarks is missing from root")
        rates = curr.get("rates", {})
        self.assertEqual(rates.get("USD"), 1.0)
        self.assertAlmostEqual(rates.get("ILS"), 3.7, places=1)
        self.assertAlmostEqual(rates.get("THB"), 36.5, places=1)
        self.assertEqual(rates.get("VND"), 25400.0)
        self.assertGreaterEqual(len(curr.get("advisory", [])), 3)

if __name__ == "__main__":
    unittest.main()
