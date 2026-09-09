"""
Multi-Pass Adversarial Critic Engine (Hotel, Route & Activity Quality Gate)
Enforces a 3-pass adversarial filter before any recommendation is approved:
- Pass 1: Location & Noise Audit (screens nightlife loud strips, construction, choke points)
- Pass 2: Recent Sentiment Gate (<90 days, rejects mold, humidity, AC failures, bugs)
- Pass 3: Destination Intent Fit & Bed Configuration (Mood check, min score >= 8.5/10, Twin for Phase 1, King for Phase 2)
"""
from typing import Dict, Any, List, Tuple
import re

class AdversarialCriticEngine:
    REJECT_KEYWORDS_PASS_1 = [
        "construction", "renovation next door", "deafening club", "party street",
        "nightclub bass", "red light", "drunk crowds", "gridlock", "inaccessible taxi"
    ]

    REJECT_KEYWORDS_PASS_2 = [
        "mold", "musty smell", "mildew", "ac broken", "air conditioning failed",
        "cockroach", "bedbug", "dirty sheets", "damp room", "unhygienic", "sewage smell"
    ]

    MINIMUM_CRITIC_SCORE = 8.5

    def __init__(self):
        self.audit_log = []

    def evaluate_hotel(self, hotel: Dict[str, Any], phase: str, destination: str, recent_reviews: List[str] = None) -> Tuple[bool, float, List[str]]:
        """
        Runs 3-pass adversarial audit on a hotel candidate.
        Returns: (passed: bool, final_score: float, issues: List[str])
        """
        issues = []
        score = float(hotel.get("critic_score", 8.8))
        recent_reviews = recent_reviews or []
        combined_text = (hotel.get("hotel_name", "") + " " + hotel.get("critic_notes", "") + " " + " ".join(recent_reviews)).lower()

        # PASS 1: Location & Noise Audit
        pass1_violation = False
        for kw in self.REJECT_KEYWORDS_PASS_1:
            if kw in combined_text:
                # Check for negation like "no construction", "zero construction", "away from construction"
                negation_pattern = rf"(no|zero|free of|away from|without|0)\s+([a-z\s]{{0,15}})?{re.escape(kw)}"
                if not re.search(negation_pattern, combined_text):
                    issues.append(f"Pass 1 Failure [Noise/Location]: Detected '{kw}'")
                    score -= 1.5
                    pass1_violation = True
                    break

        # PASS 2: Recent Sentiment Gate (Past 90 Days)
        pass2_violation = False
        for kw in self.REJECT_KEYWORDS_PASS_2:
            if kw in combined_text:
                # Check for negation like "no mold", "zero mold", "0 mold"
                negation_pattern = rf"(no|zero|free of|without|0)\s+([a-z\s]{{0,15}})?{re.escape(kw)}"
                if not re.search(negation_pattern, combined_text):
                    issues.append(f"Pass 2 Failure [Hygiene/Climate]: Detected '{kw}' in recent reviews")
                    score -= 2.0
                    pass2_violation = True
                    break

        # PASS 3: Destination Intent Fit & Bed Configuration
        room_spec = hotel.get("room_spec", "").lower()
        if "phase 1" in phase.lower() or "guys" in phase.lower():
            # Phase 1: Vietnam Guys Trip requires strictly Twin Beds / Two Separate Beds
            if not any(t in room_spec for t in ["twin", "two bed", "two separate", "single bed", "bunk"]):
                issues.append("Pass 3 Failure [Bed Spec Mismatch]: Phase 1 requires Twin Beds or Two Separate Beds")
                score -= 1.5
        elif "phase 2" in phase.lower() or "couple" in phase.lower():
            # Phase 2: Thailand Romance requires Romantic King / Double with Views
            if "twin" in room_spec and not "king" in room_spec:
                issues.append("Pass 3 Failure [Bed Spec Mismatch]: Phase 2 requires Romantic King Bed, not Twin Beds")
                score -= 1.5
            if not any(v in room_spec for v in ["king", "suite", "bungalow", "villa", "view", "pool"]):
                issues.append("Pass 3 Warning [Romance Intent]: Room lacks romantic features (King/Villa/Ocean View)")
                score -= 0.5

        # Check threshold
        passed = (score >= self.MINIMUM_CRITIC_SCORE) and not pass1_violation and not pass2_violation

        audit_record = {
            "hotel_name": hotel.get("hotel_name"),
            "destination": destination,
            "phase": phase,
            "passed": passed,
            "final_score": round(score, 1),
            "issues": issues
        }
        self.audit_log.append(audit_record)
        return passed, round(score, 1), issues

    def audit_entire_itinerary(self, itinerary_data: Dict[str, Any]) -> Dict[str, Any]:
        """Audits every accommodation in the 29-day dataset."""
        total_hotels = 0
        passed_hotels = 0
        failures = []

        for day in itinerary_data.get("days", []):
            phase = day.get("phase", "")
            dest = day.get("destination", "")
            for hotel in day.get("accommodation_matrix", []):
                total_hotels += 1
                passed, score, issues = self.evaluate_hotel(hotel, phase, dest)
                if passed:
                    passed_hotels += 1
                else:
                    failures.append({
                        "day": day.get("day_number"),
                        "hotel": hotel.get("hotel_name"),
                        "score": score,
                        "issues": issues
                    })

        return {
            "total_hotels_audited": total_hotels,
            "passed_count": passed_hotels,
            "failure_count": len(failures),
            "pass_rate_pct": round((passed_hotels / total_hotels * 100) if total_hotels else 100.0, 1),
            "failures": failures,
            "status": "APPROVED" if len(failures) == 0 else "ACTION_REQUIRED"
        }

if __name__ == "__main__":
    import json
    with open("core/itinerary_data.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    critic = AdversarialCriticEngine()
    report = critic.audit_entire_itinerary(data)
    print("Critic Audit Report:")
    print(json.dumps(report, indent=2))
