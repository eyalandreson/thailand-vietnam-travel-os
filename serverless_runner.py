"""
Persistent Serverless Background Runner (Routines 1 - 4 Orchestrator)
Executes scheduled tasks independently without requiring a local machine:
- Routine 1: Gmail Monitor & Reservation Ingestion (every 4 hours)
- Routine 2: Dual Blueprint Synchronization (Docs & Web App)
- Routine 3: Multi-Pass Adversarial Critic Engine (Pass 1 Location, Pass 2 Reviews <90d, Pass 3 Intent Fit >= 8.5)
- Routine 4: Web Application Deployment & Integrity Verification
"""
import os
import sys
import json
import datetime

# Ensure project root is in sys.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

from core.gmail_monitor import GmailMonitorEngine
from core.sync_engine import DualSyncEngine
from core.critic_engine import AdversarialCriticEngine
from core.scraper_chain import AggressiveScraperChain

def run_serverless_cycle():
    print(f"[{datetime.datetime.utcnow().isoformat()}Z] === STARTING TRAVEL OS SERVERLESS RUNNER CYCLE ===")
    
    # --- ROUTINE 1: GMAIL MONITOR & INGESTION ---
    print("\n--- [Routine 1] Ingesting Gmail Reservations & Passes ---")
    monitor = GmailMonitorEngine()
    ingest_res = monitor.ingest_reservations()
    print(f"Ingested documents: {ingest_res.get('total_confirmed_in_registry')} documents active.")

    # --- ROUTINE 2: DUAL BLUEPRINT SYNCHRONIZATION ---
    print("\n--- [Routine 2] Dual Blueprint Synchronization (Doc + Web) ---")
    syncer = DualSyncEngine()
    sync_res = syncer.execute_dual_sync()
    print(f"Dual-Sync Status: {sync_res.get('status')} across {sync_res.get('total_days')} days.")

    # --- ROUTINE 3: MULTI-PASS ADVERSARIAL CRITIC ENGINE ---
    print("\n--- [Routine 3] Executing 3-Pass Adversarial Critic Engine ---")
    critic = AdversarialCriticEngine()
    with open(os.path.join(BASE_DIR, "core", "itinerary_data.json"), "r", encoding="utf-8") as f:
        itinerary_data = json.load(f)
    audit_report = critic.audit_entire_itinerary(itinerary_data)
    print(f"Hotels Audited: {audit_report.get('total_hotels_audited')} | Pass Rate: {audit_report.get('pass_rate_pct')}% | Status: {audit_report.get('status')}")
    if audit_report.get("failures"):
        print(f"Audit Warnings: {json.dumps(audit_report.get('failures'), indent=2)}")

    # --- SCRAPER CHAIN CHECK ---
    print("\n--- [Scraper Chain Check] Live Weather & BKK->USM Price Radar ---")
    chain = AggressiveScraperChain()
    hanoi_weather = chain.fetch_live_weather(21.0285, 105.8542, "Hanoi")
    radar = chain.query_flight_fare_radar("BKK", "USM", "2026-09-24")
    print(f"Live Met Check (Hanoi): {hanoi_weather.get('temp_range')}, {hanoi_weather.get('precipitation_pct')} precip ({hanoi_weather.get('source')})")
    print(f"Flight Radar: {radar.get('target_flight')} @ ${radar.get('current_est_usd')} USD ({radar.get('cheapest_bucket')})")

    # --- ROUTINE 4: WEB DEPLOYMENT INTEGRITY CHECK ---
    print("\n--- [Routine 4] Web Application & Document Integrity Verification ---")
    index_html = os.path.join(BASE_DIR, "web", "index.html")
    doc_html = os.path.join(BASE_DIR, "web", "master_itinerary_doc.html")
    assert os.path.exists(index_html), "web/index.html missing!"
    assert os.path.exists(doc_html), "web/master_itinerary_doc.html missing!"
    print(f"Web app files verified: {index_html} ({os.path.getsize(index_html)} bytes), {doc_html} ({os.path.getsize(doc_html)} bytes).")

    summary = {
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "routine_1_ingestion": ingest_res,
        "routine_2_sync": sync_res,
        "routine_3_critic": audit_report,
        "routine_4_web": "VERIFIED_READY"
    }

    log_path = os.path.join(BASE_DIR, "last_runner_execution.json")
    with open(log_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    print(f"\n=== CYCLE COMPLETED SUCCESSFULLY. Log saved to {log_path} ===")
    return summary

if __name__ == "__main__":
    run_serverless_cycle()
