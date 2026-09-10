---
description: Instructs Antigravity agents on handling traveler change requests and maintaining dual-sync integrity
globs: ["*"]
---

# Antigravity Traveler Change Request Protocol & Dual-Sync Integrity

This workspace contains an autonomous feedback loop connecting traveler requests from the web platform to Google Antigravity agents.

## 1. Change Requests Registry (`change_requests.json`)
- All traveler requests submitted from the web dashboard (or via `agent_bridge_server.py`) are recorded in `change_requests.json`.
- Each request has a unique ticket ID (e.g. `CR-20260911-001`), target day (1–29), category (`plan` or `site`), priority, description, and status (`QUEUED`, `PROCESSING`, `RESOLVED`).

## 2. Processing Travel Plan Changes (`category: plan`)
When resolving travel plan change requests:
1. **Target Identification**: Locate the day in `core/itinerary_data.json`.
2. **Adversarial Critic Compliance**:
   - **Phase 1 (Sep 11–24, Vietnam Guys Trip)**: All accommodations must strictly have **Twin Beds / Two Separate Beds**.
   - **Phase 2 (Sep 24 – Oct 09, Thailand Couple Trip)**: Accommodations must strictly have **Romantic King Bed / Ocean View / Private Plunge Pool**.
   - **Pass 1 & 2**: Reject noise strips, active construction, mold, or AC complaints. Minimum critic score threshold: **8.5/10**.
3. **Execution of Dual-Sync**:
   - Always run `python core/sync_engine.py` or invoke `DualSyncEngine().execute_dual_sync()`.
   - This writes to `web/data.json`, `web/itinerary_data.js`, and `web/master_itinerary_doc.html`.
4. **Update Status**: Set ticket status to `RESOLVED` with diff summary in `change_requests.json`.

## 3. Processing Site / UI Changes (`category: site`)
1. Review requests in `.agents/tasks/` or `change_requests.json`.
2. Implement updates across `web/index.html`, `web/app.js`, and `web/styles.css`.
3. Verify both Light and Dark themes, mobile viewport responsiveness, and PWA offline capability.
4. Run tests: `python -m unittest discover -s tests`.
