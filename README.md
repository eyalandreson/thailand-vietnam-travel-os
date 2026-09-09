# Thailand & Vietnam [Live Travel OS]

An autonomous, headless Travel Logistics Orchestrator and Full-Stack Two-Tier Travel Platform running on Google Antigravity.

- **Responsive Web Dashboard**: [https://eyalandreson.github.io/thailand-vietnam-travel-os/](https://eyalandreson.github.io/thailand-vietnam-travel-os/)
- **Master Google Doc Blueprint**: [https://eyalandreson.github.io/thailand-vietnam-travel-os/master_itinerary_doc.html](https://eyalandreson.github.io/thailand-vietnam-travel-os/master_itinerary_doc.html)
- **GitHub Repository**: [https://github.com/eyalandreson/thailand-vietnam-travel-os](https://github.com/eyalandreson/thailand-vietnam-travel-os)

---

## 1. Confirmed Travel Profile & Party Phases

### Phase 1: Northern Vietnam Loop (Sep 11–24, 2026) [With Friend]
- **Vibe**: Adventure, trekking, scenic loops, active transport, and authentic local street cuisine.
- **Room Specification**: **Strictly Twin Beds / Two Separate Beds per room** (enforced by Adversarial Critic Engine).
- **Luggage Mandate**: Strictly **55L+ clamshell travel backpack ONLY**.
- **Geographic Sequence**: Hanoi Base (Night 1) $\rightarrow$ Ha Giang Loop 3D/2N (Quan Ba, Ma Pi Leng Pass, Tu San Canyon boat, Meo Vac homestay with licensed Easy-Riders) $\rightarrow$ Sa Pa 2D/2N (Muong Hoa Valley golden harvest trekking) $\rightarrow$ Cat Ba Island & Lan Ha Bay 3D/3N (private junk boat & kayaking) $\rightarrow$ Ninh Binh 2D/2N (Tam Coc, Trang An UNESCO water caves, Mua Cave dawn ascent) $\rightarrow$ Hanoi Base & Pre-Flight Finale (2 days).

### Transition Day (Sep 24, 2026)
- **Flight**: Hanoi (HAN) $\rightarrow$ Bangkok (BKK) at 12:45 PM (Booking: `1145-554-179`, arr 14:35).
- **Party Separation**: Friend departs/separates on international connection.
- **Luggage Retrieval**: Traveler collects checked suitcase at AIRPORTELs Suvarnabhumi Basement (Floor B).
- **Reunion**: Traveler reunites with girlfriend at Bangkok Suvarnabhumi terminal.
- **Transit South**: Direct Bangkok Airways flight to Koh Samui (USM).

### Phase 2: Gulf of Thailand & Bangkok (Sep 24 – Oct 09, 2026) [With Girlfriend]
- **Vibe**: Boutique romantic stays, beaches, high-end island dining, relaxed diving/snorkeling, and scenic viewpoints.
- **Room Specification**: **Strictly Double / Romantic King Bed with Ocean Views / Private Plunge Pool**.
- **Pacing Calibration**: Combined Gulf stay equals **13 nights** (1 Samui + 6 Phangan + 6 Tao) + **2 nights** in Bangkok Finale = **15 nights total**.
  - Koh Samui (1 Night): Arrival decompression & beachfront dinner at Fisherman's Village Bophut.
  - Koh Phangan (6 Nights): Thong Nai Pan Noi private pool villas, couple spa, Bottle Beach, Than Sadet waterfalls, Haad Yuan.
  - Koh Tao (6 Nights): Hillside luxury pool villa, Shark Bay turtles & blacktip sharks, Koh Nang Yuan private charter, Sail Rock scuba diving, Hin Wong bay kayaking.
  - Bangkok Finale (2 Nights, Oct 07–09): Riverside boutique stay facing Wat Arun, private Thonburi canal cruise, ICONSIAM, fine dining.
- **Return Flight**: Oct 09 BKK $\rightarrow$ TLV via AUH (Booking: `9KDEH2`).

---

## 2. Checked Luggage Drop & Storage Plan (Sep 12–24)

- **Storage Facility**: **AIRPORTELs / SmileLugg Suvarnabhumi (BKK) Basement (Floor B, Airport Rail Link concourse)**.
- **Deposit**: Morning of Sep 12 before the 11:55 AM flight to Hanoi.
- **Retrieval**: Sep 24 upon landing from Hanoi at 14:35 PM before flying South.
- **Storage Slip Ref**: `BKK-LK-20260912-771`.
- **Strategic Advantage**: Eliminates hauling heavy rolling luggage through Vietnamese mountain roads, buses, and ferries.

---

## 3. Direct Flight to South: Pricing Radar & Strategy (Sep 24)

- **Target Route**: Bangkok Suvarnabhumi (BKK) $\rightarrow$ Koh Samui (USM) direct nonstop (1h 05m).
- **Recommended Flight**: **Bangkok Airways PG 169 (Dep 17:15 - Arr 18:20)**.
  - Leaves an optimal **2h 40m** buffer after your 14:35 arrival from Hanoi to clear immigration, pick up luggage at Floor B, and access the complimentary Bangkok Airways Boutique Lounge.
- **Cheapest Fare Tier**: **Web Saver** (Approx. **$115 – $135 USD / ~4,200 THB** one-way per person).
- **When to Buy**: **6 to 8 weeks before departure (Mid-July to Early August 2026)**. Bangkok Airways holds monopoly pricing on USM; Web Saver seats open 90 days out and sell out 3–4 weeks prior to flight.

---

## 4. Multi-Pass Adversarial Critic Engine

All recommended hotels and transit routes must pass three adversarial filters:
1. **Pass 1 (Location & Noise Audit)**: Rejects nightlife loud strips, active construction zones, and bad taxi choke points.
2. **Pass 2 (Recent Sentiment Gate)**: Scrapes reviews from the past 90 days; strictly rejects properties with recurring complaints regarding mold, humidity, air conditioning failures, or poor hygiene.
3. **Pass 3 (Destination Intent Fit & Bed Spec)**: Enforces Twin Beds for Phase 1 and Romantic King Beds for Phase 2. Minimum quality score threshold: **8.5 / 10**.

---

## 5. Autonomous Serverless Runner (Routines 1–4)

The platform runs continuously via:
1. **GitHub Actions Serverless Cron**: `cloud_workflows/travel_os_runner.yml` runs every 4 hours headlessly without requiring a local machine.
2. **Standalone Runner**:
   ```bash
   python serverless_runner.py
   ```
3. **Unit Tests**:
   ```bash
   python -m unittest discover -s tests
   ```
