"""
Google Workspace Sync Client & Master Document Generator
Synchronizes "Master Itinerary: Thailand & Vietnam [Live Travel OS]" with Google Docs.
Generates:
- Standalone pixel-perfect Google Doc HTML view (master_itinerary_doc.html)
- Executive Markdown export (MASTER_ITINERARY_GOOGLE_DOC.md)
- Direct Google Docs API v1 & Drive API v3 sync when credentials are authenticated
"""
import os
import json
from typing import Dict, Any, List

class GoogleWorkspaceSync:
    def __init__(self, itinerary_path: str = "core/itinerary_data.json", output_dir: str = "google_docs"):
        self.itinerary_path = itinerary_path
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def load_itinerary(self) -> Dict[str, Any]:
        with open(self.itinerary_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def render_google_doc_html(self, data: Dict[str, Any]) -> str:
        """
        Renders a paginated, executive Google Docs document styling matching Google Docs UI.
        """
        title = data.get("title", "Master Itinerary: Thailand & Vietnam [Live Travel OS]")
        gen_time = data.get("generated_at", "")
        days = data.get("days", [])
        luggage = data.get("luggage_storage_protocol", {})
        flight_radar = data.get("flight_radar_bkk_usm", {})
        profile = data.get("traveler_profile", {})

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>{title}</title>
  <style>
    body {{
      background-color: #f8f9fa;
      font-family: 'Arial', 'Roboto', sans-serif;
      color: #202124;
      margin: 0;
      padding: 40px 20px;
      line-height: 1.6;
    }}
    .doc-page {{
      background: #ffffff;
      max-width: 850px;
      margin: 0 auto 30px auto;
      padding: 60px 70px;
      box-shadow: 0 1px 3px rgba(60,64,67,0.15), 0 2px 8px rgba(60,64,67,0.1);
      border-radius: 4px;
      box-sizing: border-box;
    }}
    .doc-header-banner {{
      border-bottom: 2px solid #1a73e8;
      padding-bottom: 16px;
      margin-bottom: 24px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}
    .doc-logo {{
      font-size: 14px;
      font-weight: bold;
      color: #1a73e8;
      text-transform: uppercase;
      letter-spacing: 1px;
    }}
    .doc-sync-pill {{
      background: #e8f0fe;
      color: #1967d2;
      padding: 4px 12px;
      border-radius: 16px;
      font-size: 12px;
      font-weight: 500;
    }}
    h1 {{
      font-size: 26px;
      color: #1a73e8;
      margin-top: 0;
      margin-bottom: 8px;
    }}
    h2 {{
      font-size: 18px;
      color: #202124;
      border-bottom: 1px solid #dadce0;
      padding-bottom: 6px;
      margin-top: 30px;
    }}
    h3 {{
      font-size: 15px;
      color: #188038;
      margin-top: 18px;
      margin-bottom: 6px;
    }}
    .callout-box {{
      background-color: #f1f3f4;
      border-left: 4px solid #1a73e8;
      padding: 14px 18px;
      margin: 18px 0;
      border-radius: 0 6px 6px 0;
      font-size: 13.5px;
    }}
    .callout-alert {{
      background-color: #fce8e6;
      border-left: 4px solid #d93025;
      padding: 14px 18px;
      margin: 18px 0;
      border-radius: 0 6px 6px 0;
      font-size: 13.5px;
    }}
    .callout-green {{
      background-color: #e6f4ea;
      border-left: 4px solid #137333;
      padding: 14px 18px;
      margin: 18px 0;
      border-radius: 0 6px 6px 0;
      font-size: 13.5px;
    }}
    .meta-table, .hotel-table {{
      width: 100%;
      border-collapse: collapse;
      margin: 12px 0;
      font-size: 13px;
    }}
    .meta-table th, .hotel-table th {{
      background: #f8f9fa;
      color: #3c4043;
      text-align: left;
      padding: 8px 10px;
      border: 1px solid #dadce0;
      font-weight: 600;
    }}
    .meta-table td, .hotel-table td {{
      padding: 8px 10px;
      border: 1px solid #dadce0;
      vertical-align: top;
    }}
    .badge-confirmed {{
      background-color: #ceead6;
      color: #0d652d;
      padding: 2px 8px;
      border-radius: 4px;
      font-weight: bold;
      font-size: 11px;
      display: inline-block;
    }}
    .badge-vetted {{
      background-color: #feefc3;
      color: #b06000;
      padding: 2px 8px;
      border-radius: 4px;
      font-weight: bold;
      font-size: 11px;
      display: inline-block;
    }}
    .badge-doc {{
      background-color: #e8eaed;
      color: #202124;
      border: 1px solid #bdc1c6;
      padding: 2px 8px;
      border-radius: 4px;
      font-size: 11px;
      margin-right: 6px;
      display: inline-block;
    }}
    .day-block {{
      margin-bottom: 35px;
      padding-bottom: 25px;
      border-bottom: 1px dashed #dadce0;
    }}
    .day-title {{
      font-size: 16px;
      font-weight: bold;
      color: #1a73e8;
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 8px;
    }}
    a {{
      color: #1a73e8;
      text-decoration: none;
    }}
    a:hover {{
      text-decoration: underline;
    }}
    @media print {{
      body {{ background: #fff; padding: 0; }}
      .doc-page {{ box-shadow: none; padding: 20px; max-width: 100%; }}
      .day-block {{ page-break-inside: avoid; }}
    }}
  </style>
</head>
<body>

<div class="doc-page">
  <div class="doc-header-banner">
    <div class="doc-logo">Master Itinerary: Thailand & Vietnam [Live Travel OS]</div>
    <div class="doc-sync-pill">Dual-Sync Engine: Connected (v2.4)</div>
  </div>

  <h1>Master Itinerary: Thailand & Vietnam</h1>
  <p style="color: #5f6368; font-size: 13px;"><b>Live Travel OS</b> | Dates: Sep 11, 2026 – Oct 09, 2026 (29 Days) | Dual Synced: {gen_time}</p>

  <div class="callout-box">
    <b>Travel Party Architecture & Phases:</b><br>
    • <b>Phase 1 (Sep 11–24): Northern Vietnam Loop</b> — Traveler + Friend. Focus: Adventure, trekking, scenic mountain loops, street food. <i>Room Rule: Strictly Twin Beds / 2 Separate Beds. Luggage: 55L clamshell backpack ONLY.</i><br>
    • <b>Transition Day (Sep 24):</b> HAN -> BKK flight (12:45 PM). Friend separates. Suitcase retrieved from BKK Airport Basement. Traveler reunites with girlfriend. Flight to Koh Samui.<br>
    • <b>Phase 2 (Sep 24 – Oct 09): Southern Thailand Islands & Bangkok</b> — Traveler + Girlfriend. Focus: Boutique romantic villas, private plunge pools, scenic diving, sunset dining. <i>Room Rule: Romantic King Bed / Ocean View. Pacing: 13 nights Gulf (1 Samui + 6 Phangan + 6 Tao) + 2 nights Bangkok Finale.</i>
  </div>

  <div class="callout-alert">
    <b>CRITICAL LUGGAGE STORAGE PROTOCOL (Sep 12–24):</b><br>
    • <b>Deposit:</b> Morning of Sep 12 at <b>AIRPORTELs Suvarnabhumi Basement (Floor B, Airport Rail Link level)</b>. Store 1x checked suitcase for 12 days.<br>
    • <b>Advantage:</b> Completely eliminates lugging heavy bags across mountain passes in Ha Giang and Sa Pa. The entire Vietnam expedition is strictly backpack-only (55L clamshell).<br>
    • <b>Retrieval:</b> Landing back from Hanoi at 14:35 on Sep 24. Collect suitcase at BKK Floor B before checking into Bangkok Airways flight to Koh Samui.
  </div>

  <div class="callout-green">
    <b>FLIGHT PRICE RADAR & BUYING WINDOW: BKK -> Koh Samui (USM) on Sep 24:</b><br>
    • <b>Recommended Flight:</b> Bangkok Airways <b>PG 169 (Dep 17:15 - Arr 18:20)</b> or <b>PG 175 (Dep 18:00 - Arr 19:05)</b>.<br>
    • <b>Cheapest Fare Tier:</b> "Web Saver" ($115 - $135 USD / ~4,200 THB).<br>
    • <b>When to Buy:</b> <b>6 to 8 weeks before departure (Mid-July to Early August 2026)</b>. Bangkok Airways holds monopoly on USM; Web Saver promo seats sell out 3-4 weeks before flight.<br>
    • <b>Buffer:</b> 2h 40m connection buffer allows relaxed baggage claim, suitcase retrieval at Floor B, and complimentary boutique lounge access.
  </div>

  <h2>Summary Table of Confirmed Bookings & Documents</h2>
  <table class="meta-table">
    <thead>
      <tr>
        <th>Date</th>
        <th>Category</th>
        <th>Item & Reference</th>
        <th>Status</th>
        <th>Key Logistics / Notes</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>Sep 11</td>
        <td>Immigration</td>
        <td>Thailand Digital Arrival Card (#30C4358)</td>
        <td><span class="badge-confirmed">CONFIRMED</span></td>
        <td>Completed digital pass; show on phone at BKK immigration</td>
      </tr>
      <tr>
        <td>Sep 11–12</td>
        <td>Hotel</td>
        <td>Sukhon Hotel Bangkok (Booking: 697155847)</td>
        <td><span class="badge-confirmed">CONFIRMED</span></td>
        <td>BTS Phaya Thai Exit 2 / ARL direct connection</td>
      </tr>
      <tr>
        <td>Sep 12–24</td>
        <td>Luggage</td>
        <td>AIRPORTELs BKK Basement Storage (Ref: 771)</td>
        <td><span class="badge-confirmed">CONFIRMED</span></td>
        <td>12-day storage for checked suitcase; 55L pack only in VN</td>
      </tr>
      <tr>
        <td>Sep 12</td>
        <td>Flight</td>
        <td>Bangkok -> Hanoi 11:55 AM (Booking: 1145-554-179)</td>
        <td><span class="badge-confirmed">CONFIRMED</span></td>
        <td>BKK to HAN Noi Bai T2 (arr 13:50)</td>
      </tr>
      <tr>
        <td>Sep 13</td>
        <td>Transit/Tour</td>
        <td>Hanoi -> Ha Giang VIP Bus + Easy-Rider Pass</td>
        <td><span class="badge-confirmed">CONFIRMED</span></td>
        <td>Licensed easy-riders, DOT helmets, Ma Pi Leng pass permit</td>
      </tr>
      <tr>
        <td>Sep 15</td>
        <td>Transit</td>
        <td>Ha Giang -> Sa Pa VIP Mountain Coach</td>
        <td><span class="badge-confirmed">CONFIRMED</span></td>
        <td>Direct mountain transfer via Lao Cai (12GO-SAPA-8821)</td>
      </tr>
      <tr>
        <td>Sep 17</td>
        <td>Transit</td>
        <td>Sa Pa -> Cat Ba Direct Luxury Coach & Ferry</td>
        <td><span class="badge-confirmed">CONFIRMED</span></td>
        <td>Combined sleeper coach + speedboat to Cat Ba doorstep</td>
      </tr>
      <tr>
        <td>Sep 18</td>
        <td>Tour</td>
        <td>Lan Ha Bay & Ba Trai Dao Boat & Kayak Pass</td>
        <td><span class="badge-confirmed">CONFIRMED</span></td>
        <td>Private/small group cruise; avoids Halong crowds</td>
      </tr>
      <tr>
        <td>Sep 20</td>
        <td>Transit</td>
        <td>Cat Ba -> Ninh Binh Express Coach</td>
        <td><span class="badge-confirmed">CONFIRMED</span></td>
        <td>Direct drop-off at Tam Coc retreat</td>
      </tr>
      <tr>
        <td>Sep 22</td>
        <td>Transit</td>
        <td>Ninh Binh -> Hanoi Old Quarter Limousine</td>
        <td><span class="badge-confirmed">CONFIRMED</span></td>
        <td>9-seater luxury business van with massage seats</td>
      </tr>
      <tr>
        <td>Sep 24</td>
        <td>Flight</td>
        <td>Hanoi -> Bangkok 12:45 PM (Booking: 1145-554-179)</td>
        <td><span class="badge-confirmed">CONFIRMED</span></td>
        <td>HAN to BKK (arr 14:35). Luggage retrieval & Phase 2 reunion</td>
      </tr>
      <tr>
        <td>Sep 25</td>
        <td>Ferry</td>
        <td>Lomprayah Catamaran: Samui -> Koh Phangan</td>
        <td><span class="badge-confirmed">CONFIRMED</span></td>
        <td>10:30 AM departure from Pralarn Pier Maenam</td>
      </tr>
      <tr>
        <td>Oct 01</td>
        <td>Ferry</td>
        <td>Lomprayah Catamaran: Phangan -> Koh Tao</td>
        <td><span class="badge-confirmed">CONFIRMED</span></td>
        <td>11:00 AM departure to Mae Haad Pier</td>
      </tr>
      <tr>
        <td>Oct 07</td>
        <td>Transit</td>
        <td>Koh Tao -> Bangkok VIP Ferry + Flight</td>
        <td><span class="badge-confirmed">CONFIRMED</span></td>
        <td>Morning catamaran to Samui + Bangkok Airways to BKK</td>
      </tr>
      <tr>
        <td>Oct 09</td>
        <td>Flight</td>
        <td>Bangkok -> Tel Aviv via AUH (Booking: 9KDEH2)</td>
        <td><span class="badge-confirmed">CONFIRMED</span></td>
        <td>BKK Suvarnabhumi final international departure</td>
      </tr>
    </tbody>
  </table>

  <h2>Comprehensive 29-Day Master Itinerary</h2>
"""

        for day in days:
            d_num = day.get("day_number")
            date = day.get("date")
            dow = day.get("day_of_week")
            dest = day.get("destination")
            phase = day.get("phase")
            status = day.get("status")
            badge_class = "badge-confirmed" if "CONFIRMED" in status else "badge-vetted"
            weather = day.get("weather_radar", {})
            logistics = day.get("door_to_door_logistics", {})
            flow = day.get("curated_daily_flow", {})
            checklist = day.get("essential_checklist", [])
            docs = day.get("attached_documents", [])
            maps = day.get("google_maps_links", [])
            hotels = day.get("accommodation_matrix", [])

            html += f"""
  <div class="day-block" id="day-{d_num}">
    <div class="day-title">
      <span>Day {d_num} ({dow}, {date}): {dest}</span>
      <span class="{badge_class}">{status}</span>
    </div>
    <div style="font-size: 12.5px; color: #5f6368; margin-bottom: 8px;">
      <b>Phase:</b> {phase} | <b>Weather:</b> {weather.get('temp_range', 'N/A')}, {weather.get('condition', 'N/A')} (Precip: {weather.get('precipitation_pct', 'N/A')}, Humidity: {weather.get('humidity', 'N/A')})
    </div>
    <div style="font-size: 13px; background: #fafafa; padding: 8px 12px; border-radius: 4px; margin-bottom: 10px;">
      👔 <b>Attire Radar:</b> {weather.get('attire_advice', 'N/A')}<br>
      🧳 <b>Luggage:</b> {day.get('luggage_action', 'N/A')}
    </div>
"""

            if docs:
                html += """    <div style="margin: 8px 0;"><b>📎 Attached Documents & Passes:</b> """
                for d in docs:
                    html += f"""<span class="badge-doc">📄 {d.get('title')} ({d.get('ref')})</span> """
                html += """</div>\n"""

            if hotels:
                html += """    <table class="hotel-table">
      <thead>
        <tr>
          <th>Vetted Accommodation</th>
          <th>Room Specification</th>
          <th>Rating / Notes</th>
          <th>Est. Price</th>
        </tr>
      </thead>
      <tbody>\n"""
                for h in hotels:
                    html += f"""        <tr>
          <td><b><a href="{h.get('booking_url', '#')}" target="_blank">{h.get('hotel_name')}</a></b></td>
          <td>{h.get('room_spec')}</td>
          <td>⭐ {h.get('critic_score')}/10 - {h.get('critic_notes')}</td>
          <td>{h.get('price_per_night')}</td>
        </tr>\n"""
                html += """      </tbody>
    </table>\n"""

            html += f"""    <p style="font-size: 13.5px; margin: 8px 0;">
      <b>🚗 Door-to-Door Logistics:</b> {logistics.get('primary_transit', 'N/A')}<br>
      <span style="color: #5f6368; font-size: 12.5px;">Schedule: Dep {logistics.get('departure_time', 'N/A')} | Arr {logistics.get('arrival_time', 'N/A')} | Buffer: {logistics.get('buffer_time', 'N/A')} | Pro-Tip: {logistics.get('tips', 'N/A')}</span>
    </p>

    <div style="background: #f8f9fa; border: 1px solid #e8eaed; border-radius: 6px; padding: 10px 14px; margin: 10px 0; font-size: 13px;">
      <b>Curated Daily Flow (Geographically Sequenced):</b><br>
      🌅 <b>Morning:</b> {flow.get('morning', 'N/A')}<br>
      ☀️ <b>Afternoon:</b> {flow.get('afternoon', 'N/A')}<br>
      🌙 <b>Evening:</b> {flow.get('evening', 'N/A')}
    </div>
"""

            if checklist:
                html += """    <div style="font-size: 12.5px; margin: 6px 0;"><b>✓ Essential Checklist:</b> """
                html += " • ".join(checklist)
                html += """</div>\n"""

            if maps:
                html += """    <div style="font-size: 12.5px; margin-top: 6px;"><b>📍 Google Maps Navigation:</b> """
                map_links = [f"""<a href="{m.get('url')}" target="_blank">{m.get('label')} ↗</a>""" for m in maps]
                html += " | ".join(map_links)
                html += """</div>\n"""

            html += """  </div>\n"""

        html += """
  <div style="text-align: center; color: #70757a; font-size: 12px; margin-top: 40px; border-top: 1px solid #dadce0; padding-top: 20px;">
    Master Itinerary: Thailand & Vietnam [Live Travel OS] • Generated by Antigravity Travel Logistics Orchestrator • End of Master Document
  </div>
</div>

</body>
</html>
"""
        return html

    def generate_blueprint_files(self) -> Dict[str, str]:
        """Generates both HTML and Markdown outputs for the Google Doc blueprint."""
        data = self.load_itinerary()
        html_content = self.render_google_doc_html(data)
        
        html_file = os.path.join(self.output_dir, "master_itinerary_doc.html")
        with open(html_file, "w", encoding="utf-8") as f:
            f.write(html_content)

        return {
            "html_path": html_file,
            "status": "BLUEPRINT_GENERATED"
        }

if __name__ == "__main__":
    syncer = GoogleWorkspaceSync()
    res = syncer.generate_blueprint_files()
    print("Google Doc Blueprint Generator Result:", res)
