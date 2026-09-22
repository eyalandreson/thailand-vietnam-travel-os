"""
Gmail Monitor & Reservation Ingestion Engine (Routine 1)
Monitors incoming travel confirmations (flights, hotels, 12Go, Lomprayah, TDAC, AIRPORTELs),
extracts booking metadata, and updates booking_registry.json and itinerary_data.json.
Integrates directly with GmailLiveIngestion for autonomous retrieval.
"""
import os
import sys
import json
import re
from typing import Dict, Any, List

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from core.gmail_auth_ingest import GmailLiveIngestion

class GmailMonitorEngine:
    def __init__(self, registry_path: str = "core/booking_registry.json", itinerary_path: str = "core/itinerary_data.json"):
        self.registry_path = registry_path
        self.itinerary_path = itinerary_path
        self.live_ingestor = GmailLiveIngestion(registry_path=self.registry_path, itinerary_path=self.itinerary_path)

    def load_registry(self) -> Dict[str, Any]:
        if os.path.exists(self.registry_path):
            with open(self.registry_path, "r", encoding="utf-8") as f:
                return json.load(f)
        return {"confirmed_items": []}

    def save_registry(self, registry: Dict[str, Any]):
        with open(self.registry_path, "w", encoding="utf-8") as f:
            json.dump(registry, f, indent=2, ensure_ascii=False)

    def parse_confirmation_payload(self, text_payload: str) -> Dict[str, Any]:
        """
        Parses email text for booking references, dates, and carriers.
        """
        result = {}
        ref_match = re.search(r"(Booking|Ref|Confirmation|PNR|TDAC|Order)\s*[:#]?\s*([A-Z0-9\-]{5,15})", text_payload, re.IGNORECASE)
        if ref_match:
            result["reference_code"] = ref_match.group(2).strip()

        date_match = re.search(r"(\d{4}-\d{2}-\d{2})", text_payload)
        if date_match:
            result["date"] = date_match.group(1)

        return result

    def ingest_reservations(self) -> Dict[str, Any]:
        """
        Scans for newly confirmed vouchers in Gmail and ensures they are synchronized across the travel OS.
        """
        try:
            live_res = self.live_ingestor.sync_and_ingest()
            return {
                "status": "SUCCESS",
                "total_confirmed_in_registry": live_res.get("total_confirmed_in_registry", 0),
                "new_items_added": live_res.get("new_items_added", 0),
                "itinerary_days_synchronized": live_res.get("itinerary_days_synchronized", 0),
                "resolved_action_items": live_res.get("resolved_action_items", []),
                "message": f"Gmail Ingestion verified: {live_res.get('total_confirmed_in_registry', 0)} documents active."
            }
        except Exception as e:
            print(f"[GmailMonitorEngine] Live ingest notice, falling back to local registry sync: {e}")
            registry = self.load_registry()
            confirmed_count = len(registry.get("confirmed_items", []))
            return {
                "status": "FALLBACK_LOCAL_SYNC",
                "total_confirmed_in_registry": confirmed_count,
                "error": str(e)
            }

if __name__ == "__main__":
    monitor = GmailMonitorEngine()
    res = monitor.ingest_reservations()
    print("Gmail Monitor Ingestion Result:")
    print(json.dumps(res, indent=2))
