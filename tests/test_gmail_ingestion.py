"""
Automated Unit Tests for Gmail Ingestion Engine (tests/test_gmail_ingestion.py)
Verifies:
1. Bangkok Airways flight confirmation parsing (PNR, flights, passengers).
2. Agoda hotel confirmation parsing (Booking ID, hotel name, checkin/checkout).
3. Vexere bus confirmation parsing (Ticket code, route, operator, departure).
4. Registry resolution of unbooked action items when Gmail confirmation arrives.
5. Itinerary dataset updates and Dual-Sync parity.
"""
import os
import json
import unittest
from core.gmail_auth_ingest import GmailLiveIngestion

class TestGmailIngestion(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ingestor = GmailLiveIngestion()

    def test_parse_bangkok_airways_confirmation(self):
        sample_body = """
        Itinerary Confirmation
        Booking Reference: D7XZQW
        BANGKOK AIRWAYS
        Flight Number
        PG169
        Operated by Bangkok Airways
        Status:
        Confirmed
        BANGKOK SUVARNABHUMI INTL
        Thursday, 24SEP
        16:40
        KO SAMUI KO SAMUI
        Thursday, 24SEP
        17:45
        Eyal Andreson
        """
        res = self.ingestor._parse_bangkok_airways(sample_body, "Bangkok Airways: Ticketed Bangkok Ko Samui")
        self.assertEqual(res["reference_code"], "D7XZQW")
        self.assertEqual(res["type"], "FLIGHT")
        self.assertEqual(len(res["flights"]), 1)
        self.assertEqual(res["flights"][0]["flight_number"], "PG169")
        self.assertEqual(res["flights"][0]["departure_time"], "16:40")
        self.assertEqual(res["flights"][0]["arrival_time"], "17:45")
        self.assertIn("Eyal Andreson", res["passengers"])

    def test_parse_agoda_hotel_confirmation(self):
        sample_body = """
        Booking confirmation -- Booking ID: 1777544987
        ההזמנה שלכם מאושרת כעת!
        היי Eyal Andreson,
        ניהול ההזמנה שלי
        The Fair House Beach Resort and Hotel
        124-124/1-2 Moo 3 T. Bophut Suratthani, קו-סמוי, תאילנד, 84320
        צ'ק-אין
        יום חמישי ספטמבר 24, 2026
        צ'ק-אאוט
        יום שבת ספטמבר 26, 2026
        סוג החדר
        בונגלו גרנד דלוקס
        סה"כ לחיוב
        ฿ 8,678.43
        """
        res = self.ingestor._parse_agoda(sample_body, "אישור ההזמנה עם Agoda 1777544987")
        self.assertEqual(res["reference_code"], "1777544987")
        self.assertEqual(res["type"], "ACCOMMODATION")
        self.assertEqual(res["hotel_name"], "The Fair House Beach Resort and Hotel")
        self.assertEqual(res["date"], "2026-09-24")
        self.assertEqual(res["checkout_date"], "2026-09-26")
        self.assertEqual(res["room_spec"], "בונגלו גרנד דלוקס")

    def test_parse_vexere_bus_confirmation(self):
        sample_body = """
        Confirmation of successful payment
        Hello Eyal Andreson,
        Vexere confirms that you have successfully paid for the bus ticket booking with Bằng Phấn bus.
        Hà Giang - Sapa (Cabin)
        Booking code:
        E8PB24
        18:00
        (15/09)
        Ha Giang Bus Station
        00:30
        (16/09)
        SaPa Office
        Bus Operator
        Bằng Phấn
        Bus type
        VIP Cabin bus
        Total amount
        VND1,250,000
        """
        res = self.ingestor._parse_vexere(sample_body, "[Vexere] Confirmation of successful payment, Booking code: E8PB24")
        self.assertEqual(res["reference_code"], "E8PB24")
        self.assertEqual(res["type"], "BUS_TRANSIT")
        self.assertIn("Hà Giang - Sapa", res["route"])
        self.assertEqual(res["operator"], "Bằng Phấn")
        self.assertEqual(res["departure_date"], "2026-09-15")
        self.assertEqual(res["departure_time"], "18:00")

    def test_booking_registry_confirmed_items_updated(self):
        with open("core/booking_registry.json", "r", encoding="utf-8") as f:
            reg = json.load(f)
        refs = [it.get("reference_code") for it in reg.get("confirmed_items", [])]
        self.assertIn("D7XZQW", refs, "Bangkok Airways PNR D7XZQW missing from registry!")
        self.assertIn("1777544987", refs, "The Fair House Samui booking missing from registry!")
        self.assertIn("1777345669", refs, "May De Ville Hanoi booking missing from registry!")
        self.assertIn("2051965881", refs, "La Lua Ninh Binh booking missing from registry!")
        self.assertIn("2051512276", refs, "The Moon Cat Ba booking missing from registry!")
        self.assertIn("2050577065", refs, "Sapa Praha booking missing from registry!")
        self.assertIn("2050574832", refs, "La Do Homestay Sapa booking missing from registry!")
        self.assertIn("E8PB24", refs, "Vexere E8PB24 missing from registry!")

    def test_unbooked_actions_resolved(self):
        with open("core/booking_registry.json", "r", encoding="utf-8") as f:
            reg = json.load(f)
        actions = {a["id"]: a.get("status", "") for a in reg.get("unbooked_action_items", [])}
        self.assertIn("RESOLVED", actions.get("ACTION-BKK-USM-FLIGHT", ""))
        self.assertIn("RESOLVED", actions.get("ACTION-SAMUI-STAYS", ""))
        self.assertIn("RESOLVED", actions.get("ACTION-HANOI-FINALE-STAYS", ""))
        self.assertIn("RESOLVED", actions.get("ACTION-SAPA-STAYS", ""))
        self.assertIn("RESOLVED", actions.get("ACTION-HG-SAPA-TRANSIT", ""))

    def test_itinerary_data_parity(self):
        with open("core/itinerary_data.json", "r", encoding="utf-8") as f:
            itinerary = json.load(f)
        days = {d["day_number"]: d for d in itinerary.get("days", [])}

        # Day 14: Bangkok -> Samui transition
        day14 = days.get(14)
        self.assertEqual(day14["status"], "[CONFIRMED - BOOKED]")
        self.assertIn("D7XZQW", json.dumps(day14))
        self.assertIn("The Fair House", json.dumps(day14))

        # Day 5: Ha Giang -> Sa Pa
        day5 = days.get(5)
        self.assertEqual(day5["status"], "[CONFIRMED - BOOKED]")
        self.assertIn("Sapa Praha", json.dumps(day5))

        # Day 10: Ninh Binh
        day10 = days.get(10)
        self.assertEqual(day10["status"], "[CONFIRMED - BOOKED]")
        self.assertIn("La Lua", json.dumps(day10))

    def test_web_documents_exist(self):
        web_docs = os.listdir("web/documents")
        self.assertTrue(any("EYAL ANDRESON" in f for f in web_docs), "Bangkok Airways voucher missing in web/documents")
        self.assertTrue(any("1777544987" in f for f in web_docs), "Fair House voucher missing in web/documents")
        self.assertTrue(any("1777345669" in f for f in web_docs), "May De Ville voucher missing in web/documents")

if __name__ == "__main__":
    unittest.main()
