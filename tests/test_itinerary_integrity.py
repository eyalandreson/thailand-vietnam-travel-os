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
                    # Only Sukhon Hotel (Day 1) can be confirmed accommodation
                    self.assertIn("Sukhon", hotel["hotel_name"])
                elif "UNBOOKED" in status or "ACTION REQUIRED" in status:
                    unbooked_count += 1

        self.assertEqual(confirmed_count, 1, "Only Sukhon Hotel should be marked CONFIRMED accommodation.")
        self.assertGreaterEqual(unbooked_count, 20, "All pending hotels should be marked ACTION REQUIRED - UNBOOKED.")

    def test_no_synthetic_files_referenced(self):
        """Verify that document files are not pointing to non-existent synthetic files."""
        for day in self.data.get("days", []):
            for doc in day.get("important_documents", []):
                file_status = doc.get("file_status", "")
                # If marked as verified local file, it must exist on disk
                if file_status == "LOCAL_FILE_VERIFIED":
                    self.assertTrue(os.path.exists(doc.get("file_path", "")), f"File {doc.get('file_path')} does not exist!")

if __name__ == "__main__":
    unittest.main()

