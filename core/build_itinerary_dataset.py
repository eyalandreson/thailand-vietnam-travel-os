"""
Master Dataset Builder for Thailand & Vietnam [Live Travel OS] (Audited Version)
Accurately reflects:
- ONLY verified confirmed bookings are marked [CONFIRMED - BOOKED]:
  * Sep 11: Sukhon Hotel (Booking: 697155847) + TDAC #30C4358
  * Sep 12: Flight BKK -> HAN (Booking: 1145-554-179)
  * Sep 24: Flight HAN -> BKK (Booking: 1145-554-179)
  * Oct 09: Flight BKK -> TLV via AUH (Booking: 9KDEH2)
- All unbooked legs (Ha Giang Easy-Riders, Sa Pa hotels, Cat Ba cruises, Ninh Binh, Gulf hotels & ferries, BKK finale) are marked [ACTION REQUIRED - VETTED / UNBOOKED].
- No synthetic files are generated. Documents explicitly state whether a verified local file is present or awaiting sync from Gmail.
"""
import json
import os

def build_itinerary():
    days = [
        # --- DAY 1: Bangkok Arrival ---
        {
            "day_number": 1,
            "date": "2026-09-11",
            "day_of_week": "Friday",
            "destination": "Bangkok (Arrival Base)",
            "phase": "Guys Trip - Vietnam Expedition",
            "phase_short": "Phase 1: Guys Trip",
            "status": "[CONFIRMED - BOOKED]",
            "status_badge": "CONFIRMED",
            "booking_summary": "Sukhon Hotel Confirmed (Booking: 697155847) • TDAC #30C4358",
            "weather_radar": {
                "temp_range": "27°C - 33°C",
                "condition": "Tropical Evening Shower possible",
                "precipitation_pct": "40%",
                "humidity": "75%",
                "attire_advice": "Breathable travel clothes, light trainers, compact umbrella in backpack"
            },
            "luggage_action": "Arrive with 1x 55L clamshell backpack + 1x checked suitcase. Prepare suitcase for basement storage tomorrow morning.",
            "accommodation_matrix": [
                {
                    "hotel_name": "Sukhon Hotel Bangkok",
                    "status": "CONFIRMED_BOOKED",
                    "booking_reference": "697155847",
                    "room_spec": "Superior Twin / Double (Two Separate Beds)",
                    "critic_score": 9.2,
                    "critic_notes": "Confirmed booked. Located directly at BTS Phaya Thai Exit 2 & Airport Rail Link. Soundproof glazing, pristine reviews.",
                    "price_per_night": "Booked ($72 USD / ~2,550 THB)",
                    "booking_url": "https://www.booking.com/hotel/th/sukhon.html",
                    "map_query": "Sukhon+Hotel+Bangkok"
                }
            ],
            "door_to_door_logistics": {
                "primary_transit": "Airport Rail Link (ARL) from BKK Suvarnabhumi Basement directly to Phaya Thai Station (45 THB / 26 mins). Walk 80m to Sukhon Hotel.",
                "departure_time": "Upon clearing BKK immigration",
                "arrival_time": "Evening check-in",
                "buffer_time": "60 mins for baggage claim and immigration line",
                "tips": "Show TDAC #30C4358 at passport control. ARL trains run every 10-12 mins until midnight."
            },
            "curated_daily_flow": {
                "morning": "Flight arrival into Bangkok Suvarnabhumi (BKK). Pass immigration using verified TDAC pass.",
                "afternoon": "Board Airport Rail Link City Line to Phaya Thai terminus. Check-in at Sukhon Hotel.",
                "evening": "Stroll down Phetchaburi Soi 5 for Pe Aor Tom Yum Kung Noodles, crispy pork, and iced Thai tea."
            },
            "essential_checklist": [
                "Have Thailand Digital Arrival Card (TDAC #30C4358) ready on phone",
                "Withdraw 5,000 THB from Krungsri ATM (yellow machine)",
                "Repack checked suitcase with all Phase 2 items; isolate 55L backpack for Vietnam"
            ],
            "attached_documents": [
                {
                    "doc_id": "DOC-TDAC-30C4358",
                    "title": "Thailand Digital Arrival Card (TDAC)",
                    "ref": "TDAC #30C4358",
                    "status": "Verified Official Document (Gmail)",
                    "badge": "CONFIRMED & DOWNLOADED",
                    "file_path": "documents/TDAC_Arrival_Card_30C4358.pdf",
                    "file_name": "TDAC_Arrival_Card_30C4358.pdf"
                },
                {
                    "doc_id": "HOTEL-SUKHON-697155847",
                    "title": "Sukhon Hotel Bangkok (Agoda Voucher)",
                    "ref": "Booking: 697155847",
                    "status": "Verified Official Voucher (Gmail)",
                    "badge": "CONFIRMED & DOWNLOADED",
                    "file_path": "documents/Sukhon_Hotel_Agoda_697155847.pdf",
                    "file_name": "Sukhon_Hotel_Agoda_697155847.pdf"
                }
            ],
            "google_maps_links": [
                {"label": "Sukhon Hotel Bangkok", "url": "https://maps.google.com/?q=Sukhon+Hotel+Bangkok"},
                {"label": "Phaya Thai ARL Station", "url": "https://maps.google.com/?q=Phaya+Thai+Station+Bangkok"}
            ]
        },

        # --- DAY 2: Suitcase Drop & Flight to Hanoi ---
        {
            "day_number": 2,
            "date": "2026-09-12",
            "day_of_week": "Saturday",
            "destination": "Bangkok -> Hanoi Old Quarter",
            "phase": "Guys Trip - Vietnam Expedition",
            "phase_short": "Phase 1: Guys Trip",
            "status": "[FLIGHT BOOKED / HOTEL UNBOOKED]",
            "status_badge": "PARTIAL",
            "booking_summary": "Flight BKK->HAN Confirmed (Booking: 1145-554-179) • Hanoi Hotel Unbooked",
            "weather_radar": {
                "temp_range": "25°C - 32°C",
                "condition": "Warm, high humidity with afternoon breeze in Hanoi",
                "precipitation_pct": "30%",
                "humidity": "80%",
                "attire_advice": "Comfortable flight clothes, slip-on shoes for airport security, rain poncho ready in top lid of 55L pack"
            },
            "luggage_action": "ACTION REQUIRED: Drop checked suitcase at AIRPORTELs Suvarnabhumi Basement (Floor B, next to ARL) for 12 days (Sep 12-24). Keep ONLY 55L clamshell backpack!",
            "accommodation_matrix": [
                {
                    "hotel_name": "La Siesta Classic Ma May (Hanoi Old Quarter)",
                    "status": "UNBOOKED_VETTED_OPTION",
                    "room_spec": "Deluxe Twin Room (Two Separate Single Beds)",
                    "critic_score": 9.4,
                    "critic_notes": "Vetted recommendation (Not yet booked). Heart of Old Quarter, soundproof windows, top-tier hospitality, zero mold complaints.",
                    "price_per_night": "Est. $85 USD / 2,150,000 VND",
                    "booking_url": "https://lasiestahotels.vn/mamay/",
                    "map_query": "La+Siesta+Classic+Ma+May+Hanoi"
                },
                {
                    "hotel_name": "JM Marvel Hotel & Spa",
                    "status": "UNBOOKED_VETTED_ALTERNATIVE",
                    "room_spec": "Premier Twin Room (Two Single Beds)",
                    "critic_score": 9.2,
                    "critic_notes": "Vetted alternative (Not yet booked). Excellent Hang Da location, rooftop bar overlooking Hoan Kiem.",
                    "price_per_night": "Est. $78 USD / 1,980,000 VND",
                    "booking_url": "https://jmmarvelhotel.com/",
                    "map_query": "JM+Marvel+Hotel+Hanoi"
                }
            ],
            "door_to_door_logistics": {
                "primary_transit": "08:30 AM: ARL from Phaya Thai -> BKK Airport. 09:15 AM: Drop suitcase at AIRPORTELs Floor B. 11:55 AM: Flight BKK->HAN (Booking: 1145-554-179). 13:50 PM: Arrive Hanoi Noi Bai T2. Transfer to Old Quarter.",
                "departure_time": "08:30 AM Sukhon checkout",
                "arrival_time": "15:30 PM Hanoi hotel",
                "buffer_time": "2h40m pre-departure buffer at BKK",
                "tips": "AIRPORTELs luggage deposit takes <5 minutes at Floor B next to train ticket counter."
            },
            "curated_daily_flow": {
                "morning": "ARL to Suvarnabhumi, drop suitcase at AIRPORTELs basement, board confirmed flight to Hanoi.",
                "afternoon": "Touchdown Hanoi Noi Bai Airport. Pass e-visa immigration checkpoint. Check-in to Hanoi Old Quarter hotel.",
                "evening": "Walk Hoan Kiem Lake. Authentic Bun Cha Ta (14 Hang Buom) with fried crab spring rolls & Egg Coffee at Cafe Giang."
            },
            "essential_checklist": [
                "Deposit suitcase at AIRPORTELs BKK Basement; retain receipt",
                "Apply for Vietnam e-Visa approval letter online at least 2 weeks prior",
                "Withdraw 3M-5M VND from VPBank or TPBank ATM (no local ATM fee)"
            ],
            "attached_documents": [
                {
                    "doc_id": "FLIGHT-BKK-HAN-1145554179",
                    "title": "Flight: Bangkok (BKK) -> Hanoi (HAN)",
                    "ref": "Mytrip: 1145-554-179",
                    "status": "Verified Flight E-Ticket / Receipt (Gmail)",
                    "badge": "CONFIRMED & DOWNLOADED",
                    "file_path": "documents/Flight_Mytrip_BKK_HAN_BKK_1145-554-179.pdf",
                    "file_name": "Flight_Mytrip_BKK_HAN_BKK_1145-554-179.pdf"
                }
            ],
            "google_maps_links": [
                {"label": "AIRPORTELs BKK Basement", "url": "https://maps.google.com/?q=AIRPORTELs+Suvarnabhumi+Airport"},
                {"label": "Noi Bai Airport Hanoi", "url": "https://maps.google.com/?q=Noi+Bai+International+Airport"}
            ]
        },

        # --- DAY 3: Hanoi -> Ha Giang (Loop Day 1) ---
        {
            "day_number": 3,
            "date": "2026-09-13",
            "day_of_week": "Sunday",
            "destination": "Ha Giang Loop: Bac Sum Pass & Quan Ba",
            "phase": "Guys Trip - Vietnam Expedition",
            "phase_short": "Phase 1: Guys Trip",
            "status": "[ACTION REQUIRED - VETTED / UNBOOKED]",
            "status_badge": "UNBOOKED",
            "booking_summary": "Easy-Rider tour & VIP bus NOT yet booked (Action Required)",
            "weather_radar": {
                "temp_range": "20°C - 28°C",
                "condition": "Mountain mist morning, clear afternoon passes, cool mountain air",
                "precipitation_pct": "25%",
                "humidity": "70%",
                "attire_advice": "Trekking pants, windbreaker jacket, buff/bandana for dust, sturdy closed-toe shoes"
            },
            "luggage_action": "Backpack-only. Store extra gear at Ha Giang base camp locker; carry 25-30L dry bag on motorcycle rack.",
            "accommodation_matrix": [
                {
                    "hotel_name": "Dao Lodge (Nam Dam Village, Quan Ba)",
                    "status": "UNBOOKED_VETTED_OPTION",
                    "room_spec": "Twin Bedded Earth-Lodge Room",
                    "critic_score": 9.1,
                    "critic_notes": "Vetted recommendation. Rammed-earth architecture by Red Dao minority, wood fires, herbal foot baths.",
                    "price_per_night": "Est. $45 USD / 1,150,000 VND (Includes family dinner)",
                    "booking_url": "https://daolodge.com/",
                    "map_query": "Dao+Lodge+Nam+Dam+Ha+Giang"
                },
                {
                    "hotel_name": "Hmong Village Resort (Yen Minh)",
                    "status": "UNBOOKED_VETTED_ALTERNATIVE",
                    "room_spec": "Deluxe Twin Bungalow (Two Beds)",
                    "critic_score": 8.9,
                    "critic_notes": "Infinity pool overlooking karst valleys, private bungalows.",
                    "price_per_night": "Est. $75 USD / 1,900,000 VND",
                    "booking_url": "https://hmongvillage.com.vn/",
                    "map_query": "Hmong+Village+Resort+Ha+Giang"
                }
            ],
            "door_to_door_logistics": {
                "primary_transit": "Proposed: 07:30 AM VIP Limousine Cabin Bus from Hanoi to Ha Giang city (~6 hrs). Meet licensed Easy-Riders, gear fitting. Ride Bac Sum Pass to Quan Ba.",
                "departure_time": "07:30 AM from Hanoi hotel",
                "arrival_time": "17:30 PM at Nam Dam village lodge",
                "buffer_time": "60 mins for briefing and safety checks",
                "tips": "User selected Easy-Riders. Recommend booking with Cheers Ha Giang or QT Motorbikes with full protective armor."
            },
            "curated_daily_flow": {
                "morning": "Board VIP Limousine bus speeding north on the Tuyen Quang expressway.",
                "afternoon": "Rendezvous at Ha Giang base. Briefing with licensed Easy-Riders. Ascend Bac Sum switchbacks and Quan Ba Heaven Gate.",
                "evening": "Nam Dam Dao ethnic village. Traditional family dinner and hot medicinal herb foot bath."
            },
            "essential_checklist": [
                "Book Ha Giang 3D/2N Easy-Rider package & Hanoi bus",
                "Ha Giang Provincial Border Permit ($10 USD / arranged by tour operator)",
                "Full protective gear (DOT helmet + knee/elbow armor)",
                "Bring 3M VND cash for loop expenses (ATMs are rare)"
            ],
            "attached_documents": [],
            "google_maps_links": [
                {"label": "Bac Sum Pass", "url": "https://maps.google.com/?q=Doc+Bac+Sum+Ha+Giang"},
                {"label": "Quan Ba Heaven Gate", "url": "https://maps.google.com/?q=Quan+Ba+Heaven+Gate"}
            ]
        },

        # --- DAY 4: Ha Giang Loop (Day 2) ---
        {
            "day_number": 4,
            "date": "2026-09-14",
            "day_of_week": "Monday",
            "destination": "Ha Giang Loop: Ma Pi Leng Pass & Meo Vac",
            "phase": "Guys Trip - Vietnam Expedition",
            "phase_short": "Phase 1: Guys Trip",
            "status": "[ACTION REQUIRED - VETTED / UNBOOKED]",
            "status_badge": "UNBOOKED",
            "booking_summary": "Loop day 2 • Homestay / lodge unbooked",
            "weather_radar": {
                "temp_range": "18°C - 26°C",
                "condition": "Crisp mountain sun, high visibility across karst canyon",
                "precipitation_pct": "15%",
                "humidity": "65%",
                "attire_advice": "Trekking jacket, sunglasses, windproof gloves, action camera mount on helmet"
            },
            "luggage_action": "Backpack strapped to bike rack in waterproof cover.",
            "accommodation_matrix": [
                {
                    "hotel_name": "Auberge de Meo Vac (Mountain Lodge)",
                    "status": "UNBOOKED_VETTED_OPTION",
                    "room_spec": "Twin Hmong Wood Chamber (Two Separate Beds)",
                    "critic_score": 9.3,
                    "critic_notes": "Vetted recommendation. 100-year-old restored Hmong clay fortress, exceptional mountain cuisine, total serenity.",
                    "price_per_night": "Est. $60 USD / 1,500,000 VND",
                    "booking_url": "https://aubergedemeovac.com/",
                    "map_query": "Auberge+de+Meo+Vac"
                }
            ],
            "door_to_door_logistics": {
                "primary_transit": "Motorbike ride with Easy-Riders: Nam Dam -> Tham Ma Pass -> H'mong King Palace -> Dong Van -> Ma Pi Leng Pass -> Tu San Canyon Boat -> Meo Vac.",
                "departure_time": "08:00 AM",
                "arrival_time": "17:30 PM Meo Vac",
                "buffer_time": "Ample stops for canyon photography and boat ride",
                "tips": "Tu San boat ride on Nho Que River is the highlight of the loop."
            },
            "curated_daily_flow": {
                "morning": "Ride Tham Ma slope. Explore 100-year-old H'mong King's Palace in Sa Phin.",
                "afternoon": "Ascend Ma Pi Leng Pass. Descend to Nho Que River for motorboat cruise through Tu San Chasm.",
                "evening": "Check into Auberge de Meo Vac. Communal dinner with smoked mountain beef and wild greens."
            },
            "essential_checklist": [
                "Full battery charge on phone / camera for Ma Pi Leng panoramas",
                "Warm fleece layer for high elevation evening in Meo Vac"
            ],
            "attached_documents": [],
            "google_maps_links": [
                {"label": "Ma Pi Leng Pass Monument", "url": "https://maps.google.com/?q=Ma+Pi+Leng+Pass"},
                {"label": "Tu San Canyon Dock", "url": "https://maps.google.com/?q=Nho+Que+River+Boat+Dock"}
            ]
        },

        # --- DAY 5: Ha Giang -> Sa Pa ---
        {
            "day_number": 5,
            "date": "2026-09-15",
            "day_of_week": "Tuesday",
            "destination": "Meo Vac -> Du Gia -> Sa Pa",
            "phase": "Guys Trip - Vietnam Expedition",
            "phase_short": "Phase 1: Guys Trip",
            "status": "[ACTION REQUIRED - VETTED / UNBOOKED]",
            "status_badge": "UNBOOKED",
            "booking_summary": "Ha Giang -> Sa Pa transfer & Sa Pa stay unbooked",
            "weather_radar": {
                "temp_range": "17°C - 24°C",
                "condition": "Cool alpine mist in Sa Pa, crisp evening air",
                "precipitation_pct": "30%",
                "humidity": "82%",
                "attire_advice": "Fleece jacket, thermal mid-layer, sturdy hiking shoes for Sa Pa hills"
            },
            "luggage_action": "Reunite with main 55L clamshell pack at Ha Giang base camp; load onto mountain coach to Sa Pa.",
            "accommodation_matrix": [
                {
                    "hotel_name": "Eco Palms House - Sapa Retreat",
                    "status": "UNBOOKED_VETTED_OPTION",
                    "room_spec": "Private Hmong Wooden Bungalow (Two Twin Beds)",
                    "critic_score": 9.4,
                    "critic_notes": "Vetted recommendation. Located in Lao Chai overlooking golden terraced rice fields, away from town noise.",
                    "price_per_night": "Est. $90 USD / 2,280,000 VND",
                    "booking_url": "https://ecopalmshouse.com/",
                    "map_query": "Eco+Palms+House+Sapa"
                }
            ],
            "door_to_door_logistics": {
                "primary_transit": "08:00 AM: Ride Meo Vac through Du Gia scenic valley to Ha Giang City. 15:30 PM: Mountain express minibus Ha Giang -> Sa Pa via Lao Cai (5.5 hrs, arr 21:00 PM).",
                "departure_time": "08:00 AM Meo Vac / 15:30 PM Ha Giang",
                "arrival_time": "21:30 PM Sa Pa",
                "buffer_time": "1.5 hours in Ha Giang City for lunch and pack consolidation",
                "tips": "Direct minibus avoids backtracking to Hanoi; saves 1 full travel day."
            },
            "curated_daily_flow": {
                "morning": "Ride winding road through Mau Due to Du Gia waterfall.",
                "afternoon": "Return to Ha Giang City base. Repack, board minibus to Sa Pa across Hoang Lien Son range.",
                "evening": "Arrive Sa Pa. Transfer down into Muong Hoa Valley to Eco Palms House. Hot salmon hotpot by the fire."
            },
            "essential_checklist": [
                "Book Ha Giang -> Sa Pa mountain shuttle (via 12Go Asia or local operator)",
                "Confirm Sa Pa local trekking guide for tomorrow"
            ],
            "attached_documents": [],
            "google_maps_links": [
                {"label": "Eco Palms House Sapa", "url": "https://maps.google.com/?q=Eco+Palms+House+Sapa"}
            ]
        },

        # --- DAY 6: Sa Pa (Golden Harvest Trekking) ---
        {
            "day_number": 6,
            "date": "2026-09-16",
            "day_of_week": "Wednesday",
            "destination": "Sa Pa: Muong Hoa Valley & Tribal Villages",
            "phase": "Guys Trip - Vietnam Expedition",
            "phase_short": "Phase 1: Guys Trip",
            "status": "[ACTION REQUIRED - VETTED / UNBOOKED]",
            "status_badge": "UNBOOKED",
            "booking_summary": "Sa Pa trekking guide & night 2 unbooked",
            "weather_radar": {
                "temp_range": "18°C - 25°C",
                "condition": "Clear mountain morning, dramatic afternoon cloud rolling over terraces",
                "precipitation_pct": "20%",
                "humidity": "75%",
                "attire_advice": "Trekking boots/shoes with good lugs, moisture-wicking shirt, sun hat, daypack"
            },
            "luggage_action": "Bags safely in bungalow.",
            "accommodation_matrix": [
                {
                    "hotel_name": "Eco Palms House - Sapa Retreat",
                    "status": "UNBOOKED_VETTED_OPTION",
                    "room_spec": "Private Hmong Wooden Bungalow (Two Twin Beds)",
                    "critic_score": 9.4,
                    "critic_notes": "Night 2 in Sa Pa. Direct access to trekking trailheads from property door.",
                    "price_per_night": "Est. $90 USD / 2,280,000 VND",
                    "booking_url": "https://ecopalmshouse.com/",
                    "map_query": "Eco+Palms+House+Sapa"
                }
            ],
            "door_to_door_logistics": {
                "primary_transit": "Guided trek on foot (12 km loop): Eco Palms House -> Y Linh Ho -> Lao Chai (Black Hmong) -> Ta Van (Giay) -> Bamboo forest -> Return.",
                "departure_time": "08:30 AM guided trek start",
                "arrival_time": "15:30 PM trek completion",
                "buffer_time": "Flexible lunch & tea breaks at local village homestead",
                "tips": "September is the golden harvest season in Sa Pa when terraced fields turn vibrant gold."
            },
            "curated_daily_flow": {
                "morning": "Balcony breakfast watching mist lift over golden terraces. Meet local Black Hmong guide. Trek along ridge paths.",
                "afternoon": "Cross hanging bridges into Ta Van village. Authentic lunch at local Giay family home.",
                "evening": "Return to lodge. Traditional Red Dao wooden barrel herbal bath. Sapa grilled skewers."
            },
            "essential_checklist": [
                "Support local guide: 300k-500k VND customary tip for full day",
                "Prepare 55L pack for departure to Cat Ba Island tomorrow"
            ],
            "attached_documents": [],
            "google_maps_links": [
                {"label": "Lao Chai Village", "url": "https://maps.google.com/?q=Lao+Chai+Village+Sapa"}
            ]
        },

        # --- DAY 7: Sa Pa -> Cat Ba Island ---
        {
            "day_number": 7,
            "date": "2026-09-17",
            "day_of_week": "Thursday",
            "destination": "Sa Pa -> Cat Ba Island",
            "phase": "Guys Trip - Vietnam Expedition",
            "phase_short": "Phase 1: Guys Trip",
            "status": "[ACTION REQUIRED - VETTED / UNBOOKED]",
            "status_badge": "UNBOOKED",
            "booking_summary": "Sa Pa to Cat Ba coach & hotel unbooked",
            "weather_radar": {
                "temp_range": "26°C - 32°C",
                "condition": "Sunny coastal breeze, calm emerald waters in Lan Ha Bay",
                "precipitation_pct": "20%",
                "humidity": "78%",
                "attire_advice": "Linen shirts, swim shorts, flip-flops, sunglasses"
            },
            "luggage_action": "55L clamshell pack rides in coach luggage bay directly onto island ferry.",
            "accommodation_matrix": [
                {
                    "hotel_name": "Hôtel Perle d'Orient Cat Ba - MGallery",
                    "status": "UNBOOKED_VETTED_OPTION",
                    "room_spec": "Classic Twin Bay View (Two Single Beds)",
                    "critic_score": 9.3,
                    "critic_notes": "Vetted recommendation. Cliffside at Cat Co 3 beach overlooking Lan Ha Bay. Indochine design, private beach, zero noise.",
                    "price_per_night": "Est. $125 USD / 3,180,000 VND",
                    "booking_url": "https://all.accor.com/hotel/B557/index.en.shtml",
                    "map_query": "Hotel+Perle+d+Orient+Cat+Ba"
                }
            ],
            "door_to_door_logistics": {
                "primary_transit": "08:00 AM: Cat Ba Express bus from Sa Pa -> Tan Vu sea bridge -> Speedboat to Cat Ba Island (arr 16:00 PM).",
                "departure_time": "08:00 AM from Sa Pa",
                "arrival_time": "16:00 PM at Cat Ba hotel",
                "buffer_time": "Combined bus + ferry ticket handles transit seamlessly",
                "tips": "Book Cat Ba Express or Good Morning Cat Ba direct coach."
            },
            "curated_daily_flow": {
                "morning": "Board express coach descending from mountains to coastal highway.",
                "afternoon": "Cross sea bridge to Hai Phong, speedboat hop to Cat Ba Island. Check in to resort.",
                "evening": "Hike up Cannon Fort peak for panoramic sunset over Lan Ha Bay. Seafood dinner in town."
            },
            "essential_checklist": [
                "Book Sa Pa to Cat Ba direct express bus (Cat Ba Express)",
                "Waterproof phone sleeve for sea excursions"
            ],
            "attached_documents": [],
            "google_maps_links": [
                {"label": "Hôtel Perle d'Orient Cat Ba", "url": "https://maps.google.com/?q=Hotel+Perle+d+Orient+Cat+Ba"}
            ]
        },

        # --- DAY 8: Lan Ha Bay Kayak & Cruise ---
        {
            "day_number": 8,
            "date": "2026-09-18",
            "day_of_week": "Friday",
            "destination": "Lan Ha Bay & Ba Trai Dao Archways",
            "phase": "Guys Trip - Vietnam Expedition",
            "phase_short": "Phase 1: Guys Trip",
            "status": "[ACTION REQUIRED - VETTED / UNBOOKED]",
            "status_badge": "UNBOOKED",
            "booking_summary": "Lan Ha Bay boat cruise / kayak unbooked",
            "weather_radar": {
                "temp_range": "27°C - 33°C",
                "condition": "Brilliant sunshine over emerald bay, calm sea swell",
                "precipitation_pct": "10%",
                "humidity": "72%",
                "attire_advice": "Swimwear, rashguard/sun shirt, polarized sunglasses, reef-safe sunscreen"
            },
            "luggage_action": "Bags at hotel. Bring only waterproof dry-bag onto boat.",
            "accommodation_matrix": [
                {
                    "hotel_name": "Hôtel Perle d'Orient Cat Ba - MGallery",
                    "status": "UNBOOKED_VETTED_OPTION",
                    "room_spec": "Classic Twin Bay View (Two Single Beds)",
                    "critic_score": 9.3,
                    "critic_notes": "Night 2 on Cat Ba.",
                    "price_per_night": "Est. $125 USD / 3,180,000 VND",
                    "booking_url": "https://all.accor.com/hotel/B557/index.en.shtml",
                    "map_query": "Hotel+Perle+d+Orient+Cat+Ba"
                }
            ],
            "door_to_door_logistics": {
                "primary_transit": "08:15 AM: Transfer to Cai Beo pier. Board traditional wooden junk boat into Lan Ha Bay (avoids Halong crowds).",
                "departure_time": "08:15 AM",
                "arrival_time": "16:30 PM",
                "buffer_time": "Full-day boat charter including freshly cooked seafood lunch",
                "tips": "Lan Ha Bay shares the exact karst geology of Halong Bay but without the mega-cruise traffic."
            },
            "curated_daily_flow": {
                "morning": "Board junk boat at Cai Beo harbor. Navigate floating fishing villages. Kayak through Dark & Bright cave tunnels into hidden lagoons.",
                "afternoon": "Swim at secluded Ba Trai Dao beaches. Seafood lunch onboard (grilled prawns, calamari, sea bass).",
                "evening": "Sail back through sunset karsts. Casual dinner at Secret Garden Cat Ba."
            },
            "essential_checklist": [
                "Book private or small-group Lan Ha Bay day cruise",
                "Reef-safe sunscreen SPF 50+"
            ],
            "attached_documents": [],
            "google_maps_links": [
                {"label": "Cai Beo Fishing Village", "url": "https://maps.google.com/?q=Cai+Beo+Fishing+Village"}
            ]
        },

        # --- DAY 9: Cat Ba Island National Park ---
        {
            "day_number": 9,
            "date": "2026-09-19",
            "day_of_week": "Saturday",
            "destination": "Cat Ba Island: Ngu Lam Peak & Hospital Cave",
            "phase": "Guys Trip - Vietnam Expedition",
            "phase_short": "Phase 1: Guys Trip",
            "status": "[ACTION REQUIRED - VETTED / UNBOOKED]",
            "status_badge": "UNBOOKED",
            "booking_summary": "Cat Ba night 3 unbooked",
            "weather_radar": {
                "temp_range": "25°C - 31°C",
                "condition": "Warm tropical sun with afternoon coastal breeze",
                "precipitation_pct": "25%",
                "humidity": "76%",
                "attire_advice": "Breathable hiking shorts, trail shoes, t-shirt, insect repellent"
            },
            "luggage_action": "Bags at hotel.",
            "accommodation_matrix": [
                {
                    "hotel_name": "Hôtel Perle d'Orient Cat Ba - MGallery",
                    "status": "UNBOOKED_VETTED_OPTION",
                    "room_spec": "Classic Twin Bay View (Two Single Beds)",
                    "critic_score": 9.3,
                    "critic_notes": "Night 3 on Cat Ba.",
                    "price_per_night": "Est. $125 USD / 3,180,000 VND",
                    "booking_url": "https://all.accor.com/hotel/B557/index.en.shtml",
                    "map_query": "Hotel+Perle+d+Orient+Cat+Ba"
                }
            ],
            "door_to_door_logistics": {
                "primary_transit": "Scooter rental or taxi into island interior (14 km to National Park HQ).",
                "departure_time": "08:30 AM",
                "arrival_time": "16:00 PM",
                "buffer_time": "Self-paced mountain hiking and historic cave walkthrough",
                "tips": "Ngu Lam peak summit hike takes ~1.5 hours return."
            },
            "curated_daily_flow": {
                "morning": "Hike jungle trail to Ngu Lam Peak for 360-degree panorama of limestone mountain peaks rolling into the sea.",
                "afternoon": "Explore Hospital Cave (Quan Y)—bomb-proof 3-story underground hospital cavern from wartime.",
                "evening": "Relax on Cat Co 1 beach. Dinner at Yummy Restaurant (fresh crab & cold Bia Saigon)."
            },
            "essential_checklist": [
                "Insect repellent for jungle hike",
                "Pack bags for morning transfer to Ninh Binh tomorrow"
            ],
            "attached_documents": [],
            "google_maps_links": [
                {"label": "Cat Ba National Park", "url": "https://maps.google.com/?q=Cat+Ba+National+Park"}
            ]
        },

        # --- DAY 10: Cat Ba -> Ninh Binh ---
        {
            "day_number": 10,
            "date": "2026-09-20",
            "day_of_week": "Sunday",
            "destination": "Cat Ba -> Ninh Binh (Tam Coc)",
            "phase": "Guys Trip - Vietnam Expedition",
            "phase_short": "Phase 1: Guys Trip",
            "status": "[ACTION REQUIRED - VETTED / UNBOOKED]",
            "status_badge": "UNBOOKED",
            "booking_summary": "Cat Ba to Ninh Binh bus & retreat unbooked",
            "weather_radar": {
                "temp_range": "24°C - 31°C",
                "condition": "Warm and pleasant among river valleys, calm waters",
                "precipitation_pct": "20%",
                "humidity": "74%",
                "attire_advice": "Light cycling clothes, sunglasses, sun hat, comfortable walking shoes"
            },
            "luggage_action": "55L backpack stored in coach cargo hold; direct drop-off at retreat doorstep.",
            "accommodation_matrix": [
                {
                    "hotel_name": "Tam Coc Garden Resort",
                    "status": "UNBOOKED_VETTED_OPTION",
                    "room_spec": "Premium Twin Bungalow (Two Separate Beds)",
                    "critic_score": 9.5,
                    "critic_notes": "Vetted recommendation. Nestled amid rice fields and karst pinnacles. Complimentary bicycles, zero traffic noise, exceptional dining.",
                    "price_per_night": "Est. $140 USD / 3,550,000 VND",
                    "booking_url": "https://tamcocgarden.com/",
                    "map_query": "Tam+Coc+Garden+Resort+Ninh+Binh"
                }
            ],
            "door_to_door_logistics": {
                "primary_transit": "09:00 AM: Daichi / Good Morning Cat Ba bus from Cat Ba hotel -> Island ferry -> Highway -> Ninh Binh Tam Coc (3.5 hrs, arr 13:30 PM).",
                "departure_time": "09:00 AM Cat Ba",
                "arrival_time": "13:30 PM Tam Coc",
                "buffer_time": "Direct coach transfers passengers and luggage onto ferry without shifting bags",
                "tips": "Book bus ticket 2 days in advance via 12Go Asia or Cat Ba hotel desk."
            },
            "curated_daily_flow": {
                "morning": "Board tourist express coach from Cat Ba town across ferry channel to Ninh Binh's inland karst empire.",
                "afternoon": "Check in Tam Coc Garden Resort. Pedal bicycles along quiet dirt tracks to Bich Dong Pagoda.",
                "evening": "Sunset cocktails overlooking rice paddies. Dinner at Tam Coc Garden (Ninh Binh crispy burned rice and roasted goat)."
            },
            "essential_checklist": [
                "Book Cat Ba -> Ninh Binh express bus",
                "Bicycle lock provided by resort"
            ],
            "attached_documents": [],
            "google_maps_links": [
                {"label": "Tam Coc Garden Resort", "url": "https://maps.google.com/?q=Tam+Coc+Garden+Resort"}
            ]
        },

        # --- DAY 11: Ninh Binh (Mua Cave & Trang An) ---
        {
            "day_number": 11,
            "date": "2026-09-21",
            "day_of_week": "Monday",
            "destination": "Ninh Binh: Mua Cave & Trang An UNESCO",
            "phase": "Guys Trip - Vietnam Expedition",
            "phase_short": "Phase 1: Guys Trip",
            "status": "[ACTION REQUIRED - VETTED / UNBOOKED]",
            "status_badge": "UNBOOKED",
            "booking_summary": "Ninh Binh night 2 unbooked",
            "weather_radar": {
                "temp_range": "23°C - 30°C",
                "condition": "Crisp clear morning for sunrise climb, warm afternoon",
                "precipitation_pct": "15%",
                "humidity": "70%",
                "attire_advice": "Sturdy trainers for 500 stone steps at Mua Cave, light breathable clothes"
            },
            "luggage_action": "Bags at resort.",
            "accommodation_matrix": [
                {
                    "hotel_name": "Tam Coc Garden Resort",
                    "status": "UNBOOKED_VETTED_OPTION",
                    "room_spec": "Premium Twin Bungalow (Two Separate Beds)",
                    "critic_score": 9.5,
                    "critic_notes": "Night 2 at Tam Coc Garden Resort.",
                    "price_per_night": "Est. $140 USD / 3,550,000 VND",
                    "booking_url": "https://tamcocgarden.com/",
                    "map_query": "Tam+Coc+Garden+Resort+Ninh+Binh"
                }
            ],
            "door_to_door_logistics": {
                "primary_transit": "06:00 AM: 15-min taxi to Hang Mua. 09:30 AM: 20-min taxi to Trang An UNESCO Boat Wharf (Route 3 boat tour, 3 hrs).",
                "departure_time": "06:00 AM (beats crowds and heat)",
                "arrival_time": "15:00 PM return",
                "buffer_time": "Early start ensures climbing Mua Cave before tour groups arrive from Hanoi",
                "tips": "At Trang An, pick Route 3 for the 1,000m Dot Cave and King Kong film set."
            },
            "curated_daily_flow": {
                "morning": "Dawn ascent of Hang Mua (500 stone steps) to Lying Dragon peak for golden morning light over Tam Coc valley.",
                "afternoon": "Sampan boat ride at Trang An UNESCO complex gliding through illuminated underground water caves.",
                "evening": "Resort pool swim overlooking lotus lagoon. Chookie's Beer Garden dinner."
            },
            "essential_checklist": [
                "Arrive at Hang Mua at 06:15 AM",
                "Trang An ticket: 250,000 VND / person (buy at wharf counter)"
            ],
            "attached_documents": [],
            "google_maps_links": [
                {"label": "Hang Mua (Mua Cave)", "url": "https://maps.google.com/?q=Hang+Mua+Ninh+Binh"},
                {"label": "Trang An Boat Wharf", "url": "https://maps.google.com/?q=Trang+An+Departure+Boat+Ticket"}
            ]
        },

        # --- DAY 12: Ninh Binh -> Hanoi ---
        {
            "day_number": 12,
            "date": "2026-09-22",
            "day_of_week": "Tuesday",
            "destination": "Ninh Binh -> Hanoi (Old Quarter Finale Base)",
            "phase": "Guys Trip - Vietnam Expedition",
            "phase_short": "Phase 1: Guys Trip",
            "status": "[ACTION REQUIRED - VETTED / UNBOOKED]",
            "status_badge": "UNBOOKED",
            "booking_summary": "Ninh Binh -> Hanoi limo & Hanoi hotel unbooked",
            "weather_radar": {
                "temp_range": "25°C - 32°C",
                "condition": "Warm urban sun, breezy evening",
                "precipitation_pct": "20%",
                "humidity": "72%",
                "attire_advice": "Casual urban street clothes, comfortable walking shoes"
            },
            "luggage_action": "55L backpack loaded into limousine van trunk.",
            "accommodation_matrix": [
                {
                    "hotel_name": "La Siesta Classic Ma May (Hanoi Old Quarter)",
                    "status": "UNBOOKED_VETTED_OPTION",
                    "room_spec": "Deluxe Twin Room (Two Separate Single Beds)",
                    "critic_score": 9.4,
                    "critic_notes": "Vetted recommendation. Returning to Old Quarter base for pre-flight finale. Central location, quiet street.",
                    "price_per_night": "Est. $85 USD / 2,150,000 VND",
                    "booking_url": "https://lasiestahotels.vn/mamay/",
                    "map_query": "La+Siesta+Classic+Ma+May+Hanoi"
                }
            ],
            "door_to_door_logistics": {
                "primary_transit": "11:00 AM: VIP 9-seater Limousine Van pickup from Tam Coc. Expressway to Hanoi Old Quarter (90 mins, arr 12:45 PM).",
                "departure_time": "11:00 AM Tam Coc",
                "arrival_time": "12:45 PM Hanoi",
                "buffer_time": "Expressway route avoids highway traffic",
                "tips": "Book Trang An Limousine via 12Go or resort front desk."
            },
            "curated_daily_flow": {
                "morning": "Breakfast at resort. Board luxury limousine van to Hanoi.",
                "afternoon": "Check in Hanoi Old Quarter hotel. Hanoi Train Street coconut coffee as locomotive rumbles past.",
                "evening": "Pho Gia Truyen Bat Dan beef pho, Banh Mi 25, and fresh draught Bia Hoi on Ta Hien corner."
            },
            "essential_checklist": [
                "Book Ninh Binh -> Hanoi limousine van (Trang An Limousine)",
                "Prepare laundry at hotel for quick overnight turnaround before Thailand"
            ],
            "attached_documents": [],
            "google_maps_links": [
                {"label": "Hanoi Train Street", "url": "https://maps.google.com/?q=Hanoi+Train+Street"}
            ]
        },

        # --- DAY 13: Hanoi Base (Finale Rest) ---
        {
            "day_number": 13,
            "date": "2026-09-23",
            "day_of_week": "Wednesday",
            "destination": "Hanoi: French Quarter & Farewell Dinner",
            "phase": "Guys Trip - Vietnam Expedition",
            "phase_short": "Phase 1: Guys Trip",
            "status": "[ACTION REQUIRED - VETTED / UNBOOKED]",
            "status_badge": "UNBOOKED",
            "booking_summary": "Hanoi night 2 unbooked",
            "weather_radar": {
                "temp_range": "26°C - 33°C",
                "condition": "Warm tropical sun, ideal cafe terrace weather",
                "precipitation_pct": "15%",
                "humidity": "70%",
                "attire_advice": "Smart casual, comfortable shoes, daypack for shopping/souvenirs"
            },
            "luggage_action": "Evening full pack & consolidate of 55L clamshell backpack for tomorrow's international flight.",
            "accommodation_matrix": [
                {
                    "hotel_name": "La Siesta Classic Ma May (Hanoi Old Quarter)",
                    "status": "UNBOOKED_VETTED_OPTION",
                    "room_spec": "Deluxe Twin Room (Two Separate Single Beds)",
                    "critic_score": 9.4,
                    "critic_notes": "Finale night in Vietnam.",
                    "price_per_night": "Est. $85 USD / 2,150,000 VND",
                    "booking_url": "https://lasiestahotels.vn/mamay/",
                    "map_query": "La+Siesta+Classic+Ma+May+Hanoi"
                }
            ],
            "door_to_door_logistics": {
                "primary_transit": "Walking and short Grab taxi hops within central Hanoi.",
                "departure_time": "Self-paced",
                "arrival_time": "Self-paced",
                "buffer_time": "Pre-flight prep day with zero tight deadlines",
                "tips": "Use Grab app linked to credit card for 30k-50k VND rides."
            },
            "curated_daily_flow": {
                "morning": "French Quarter boulevards, Temple of Literature, The Note Coffee overlooking Hoan Kiem.",
                "afternoon": "West Lake Tran Quoc Pagoda, souvenir shopping for artisan ceramics and Vietnamese coffee beans.",
                "evening": "Phase 1 Guys Trip Farewell Feast: Cha Ca Thang Long (turmeric-marinated grilled catfish sizzled with dill). Toast the northern loop at Moonlight Sky Bar."
            },
            "essential_checklist": [
                "Pack and zip 55L pack; weigh under 15kg for cabin/carry-on",
                "Confirm Vietnam departure flight 1145-554-179 status for tomorrow"
            ],
            "attached_documents": [],
            "google_maps_links": [
                {"label": "Temple of Literature", "url": "https://maps.google.com/?q=Temple+of+Literature+Hanoi"},
                {"label": "Cha Ca Thang Long", "url": "https://maps.google.com/?q=Cha+Ca+Thang+Long+Duong+Thanh"}
            ]
        },

        # --- DAY 14: TRANSITION DAY ---
        {
            "day_number": 14,
            "date": "2026-09-24",
            "day_of_week": "Thursday",
            "destination": "Transition: Hanoi -> Bangkok -> Koh Samui",
            "phase": "Transition & Couple Trip - Thailand Romance",
            "phase_short": "Transition -> Phase 2",
            "status": "[TRANSITION FLIGHT BOOKED / SOUTH UNBOOKED]",
            "status_badge": "PARTIAL",
            "booking_summary": "Flight HAN->BKK Confirmed (Booking: 1145-554-179) • BKK->USM Flight & Samui Hotel Unbooked",
            "weather_radar": {
                "temp_range": "26°C - 32°C",
                "condition": "Warm tropical sun over Gulf of Thailand, balmy coastal evening",
                "precipitation_pct": "20%",
                "humidity": "75%",
                "attire_advice": "Transition from trekking clothes to chic island resort attire: linen shirt, tailored shorts"
            },
            "luggage_action": "RETRIEVAL ACTION: Upon landing at BKK (14:35), proceed to Airport Rail Link level (Floor B) and retrieve checked suitcase from AIRPORTELs locker. Reunite with girlfriend with all gear ready for the South!",
            "accommodation_matrix": [
                {
                    "hotel_name": "Hansar Samui Resort & Spa (Bophut Beach)",
                    "status": "UNBOOKED_VETTED_OPTION",
                    "room_spec": "Sea View King Room (Romantic King Bed + Ocean Balcony Daybed)",
                    "critic_score": 9.4,
                    "critic_notes": "Vetted recommendation. 2-minute beach walk to Fisherman's Village dining, stunning infinity pool, sound of gentle waves.",
                    "price_per_night": "Est. $165 USD / ~5,800 THB",
                    "booking_url": "https://www.hansarsamui.com/",
                    "map_query": "Hansar+Samui+Resort+Bophut"
                },
                {
                    "hotel_name": "SALA Samui Choengmon Beach Resort",
                    "status": "UNBOOKED_VETTED_ALTERNATIVE",
                    "room_spec": "Deluxe Balcony King Room / Plunge Pool Villa",
                    "critic_score": 9.3,
                    "critic_notes": "Intimate couple haven, private open-air bathtubs, white sand cove.",
                    "price_per_night": "Est. $195 USD / ~6,900 THB",
                    "booking_url": "https://www.salahospitality.com/choengmon/",
                    "map_query": "SALA+Samui+Choengmon"
                }
            ],
            "door_to_door_logistics": {
                "primary_transit": "10:15 AM: Taxi to Noi Bai Airport. 12:45 PM: Flight HAN -> BKK (Booking: 1145-554-179, arr 14:35). Friend departs. 14:50 PM: Retrieve suitcase from Floor B. 15:15 PM: Reunite with girlfriend at BKK Terminal. Proposed: 17:15 PM Bangkok Airways PG 169 to Koh Samui (arr 18:20 PM). Transfer to resort.",
                "departure_time": "10:15 AM Hanoi / 17:15 PM BKK",
                "arrival_time": "19:00 PM Koh Samui resort",
                "buffer_time": "2h40m connection buffer at BKK terminal for bag retrieval and terminal transit",
                "tips": "Bangkok Airways operates exclusive boutique lounges with complimentary snacks and espresso for all passengers at BKK Concourse A/F."
            },
            "curated_daily_flow": {
                "morning": "Checkout Hanoi hotel. Board confirmed flight 1145-554-179 to Bangkok. Bid farewell to friend as journeys branch.",
                "afternoon": "Land at Suvarnabhumi. Head to Floor B locker desk, retrieve large suitcase. Reunite with girlfriend at arrivals hall! Check in for flight to Koh Samui.",
                "evening": "Touchdown Koh Samui. Check-in to oceanfront King room at Hansar Samui. Welcome cocktails & candlelit dinner at Coco Tam's in Fisherman's Village with fire dancer show."
            },
            "essential_checklist": [
                "Book direct BKK -> USM flight (Bangkok Airways PG 169 in mid-July / early Aug)",
                "Book Koh Samui arrival resort (Hansar Samui)",
                "Retrieve suitcase from AIRPORTELs Floor B upon landing"
            ],
            "attached_documents": [
                {
                    "doc_id": "FLIGHT-HAN-BKK-1145554179",
                    "title": "Flight: Hanoi (HAN) -> Bangkok (BKK)",
                    "ref": "Mytrip: 1145-554-179",
                    "status": "Verified Flight E-Ticket / Receipt (Gmail)",
                    "badge": "CONFIRMED & DOWNLOADED",
                    "file_path": "documents/Flight_Mytrip_BKK_HAN_BKK_1145-554-179.pdf",
                    "file_name": "Flight_Mytrip_BKK_HAN_BKK_1145-554-179.pdf"
                }
            ],
            "google_maps_links": [
                {"label": "Hansar Samui Resort", "url": "https://maps.google.com/?q=Hansar+Samui+Resort"},
                {"label": "Fisherman's Village Bophut", "url": "https://maps.google.com/?q=Fishermans+Village+Bophut"}
            ]
        },

        # --- DAY 15: Koh Samui -> Koh Phangan ---
        {
            "day_number": 15,
            "date": "2026-09-25",
            "day_of_week": "Friday",
            "destination": "Koh Samui -> Koh Phangan (Thong Nai Pan)",
            "phase": "Couple Trip - Southern Thailand Romance",
            "phase_short": "Phase 2: Couple Trip",
            "status": "[ACTION REQUIRED - VETTED / UNBOOKED]",
            "status_badge": "UNBOOKED",
            "booking_summary": "Lomprayah catamaran & Phangan resort unbooked",
            "weather_radar": {
                "temp_range": "27°C - 32°C",
                "condition": "Tropical sunshine, gentle sea breeze, calm bay",
                "precipitation_pct": "15%",
                "humidity": "72%",
                "attire_advice": "Linen shirts, sundresses, swimwear, polarized sunglasses, flip-flops"
            },
            "luggage_action": "Suitcase + backpack transferred via Lomprayah ferry luggage crew.",
            "accommodation_matrix": [
                {
                    "hotel_name": "Anantara Rasananda Koh Phangan Villas",
                    "status": "UNBOOKED_VETTED_OPTION",
                    "room_spec": "Ocean Pool Suite / Garden Pool Suite (Romantic King Bed + Private Plunge Pool)",
                    "critic_score": 9.6,
                    "critic_notes": "Vetted recommendation. Premier romance resort on Thong Nai Pan Noi. Secluded, private plunge pools, five-star dining, far from party noise.",
                    "price_per_night": "Est. $260 USD / ~9,200 THB",
                    "booking_url": "https://www.anantara.com/en/rasananda-koh-phangan",
                    "map_query": "Anantara+Rasananda+Koh+Phangan"
                },
                {
                    "hotel_name": "Santhiya Koh Phangan Resort & Spa",
                    "status": "UNBOOKED_VETTED_ALTERNATIVE",
                    "room_spec": "Supreme Deluxe Sea View King",
                    "critic_score": 9.2,
                    "critic_notes": "Teakwood cliffside architecture, panoramic Gulf vistas.",
                    "price_per_night": "Est. $180 USD / ~6,400 THB",
                    "booking_url": "https://www.santhiya.com/kohphangan/",
                    "map_query": "Santhiya+Koh+Phangan+Resort"
                }
            ],
            "door_to_door_logistics": {
                "primary_transit": "Proposed: 10:00 AM taxi to Lomprayah Pralarn Pier (Maenam). 10:30 AM Catamaran to Koh Phangan Thong Sala (20 mins). Resort 4x4 transfer to Thong Nai Pan Noi (35 mins).",
                "departure_time": "10:00 AM Samui",
                "arrival_time": "12:00 PM Phangan resort",
                "buffer_time": "Smooth 20-min catamaran crossing",
                "tips": "Book Lomprayah tickets online at lomprayah.com 1 month prior."
            },
            "curated_daily_flow": {
                "morning": "Breakfast on beach at Hansar. Catamaran across Gulf.",
                "afternoon": "Jungle drive descending to Thong Nai Pan Noi crescent bay. Check in Anantara Rasananda. Plunge into private pool with chilled champagne.",
                "evening": "Sunset cocktails at Bistro @ The Beach. Barefoot candlelit dinner listening to gentle waves."
            },
            "essential_checklist": [
                "Book Lomprayah catamaran (Samui to Phangan 10:30 AM)",
                "Book Koh Phangan resort (Anantara Rasananda for 6 nights)"
            ],
            "attached_documents": [],
            "google_maps_links": [
                {"label": "Anantara Rasananda Villas", "url": "https://maps.google.com/?q=Anantara+Rasananda+Koh+Phangan"}
            ]
        },

        # --- DAYS 16-20: Koh Phangan Stays (Days 16, 17, 18, 19, 20) ---
        {
            "day_number": 16,
            "date": "2026-09-26",
            "day_of_week": "Saturday",
            "destination": "Koh Phangan: Thong Nai Pan Bay & Couple Spa",
            "phase": "Couple Trip - Southern Thailand Romance",
            "phase_short": "Phase 2: Couple Trip",
            "status": "[ACTION REQUIRED - VETTED / UNBOOKED]",
            "status_badge": "UNBOOKED",
            "booking_summary": "Phangan night 2 unbooked",
            "weather_radar": {"temp_range": "28°C - 33°C", "condition": "Golden sunshine, azure sea", "precipitation_pct": "10%", "humidity": "70%", "attire_advice": "Bathing suits, linen cover-ups, sandals"},
            "luggage_action": "Resort stay.",
            "accommodation_matrix": [{"hotel_name": "Anantara Rasananda Koh Phangan Villas", "status": "UNBOOKED_VETTED_OPTION", "room_spec": "Ocean Pool Suite (Romantic King Bed)", "critic_score": 9.6, "critic_notes": "Night 2 on Phangan.", "price_per_night": "Est. $260 USD", "booking_url": "https://www.anantara.com/en/rasananda-koh-phangan"}],
            "door_to_door_logistics": {"primary_transit": "Zero transit day. 100% beach relaxation.", "departure_time": "N/A", "arrival_time": "N/A", "buffer_time": "N/A", "tips": "Paddleboards complimentary at resort."},
            "curated_daily_flow": {"morning": "Beachfront buffet breakfast. Paddleboarding on calm bay.", "afternoon": "2-hour signature Couple Aromatherapy Spa ritual.", "evening": "Buri Rasa Beach Club cocktail & Luna Lounge dinner."},
            "essential_checklist": ["Pre-book couple spa ritual"],
            "attached_documents": [],
            "google_maps_links": [{"label": "Luna Lounge Phangan", "url": "https://maps.google.com/?q=Luna+Lounge+Koh+Phangan"}]
        },
        {
            "day_number": 17,
            "date": "2026-09-27",
            "day_of_week": "Sunday",
            "destination": "Koh Phangan: Bottle Beach & Than Sadet",
            "phase": "Couple Trip - Southern Thailand Romance",
            "phase_short": "Phase 2: Couple Trip",
            "status": "[ACTION REQUIRED - VETTED / UNBOOKED]",
            "status_badge": "UNBOOKED",
            "booking_summary": "Phangan night 3 unbooked",
            "weather_radar": {"temp_range": "27°C - 32°C", "condition": "Sunny skies", "precipitation_pct": "15%", "humidity": "72%", "attire_advice": "Swimwear, water shoes"},
            "luggage_action": "Resort stay.",
            "accommodation_matrix": [{"hotel_name": "Anantara Rasananda Koh Phangan Villas", "status": "UNBOOKED_VETTED_OPTION", "room_spec": "Ocean Pool Suite (Romantic King Bed)", "critic_score": 9.6, "critic_notes": "Night 3 on Phangan.", "price_per_night": "Est. $260 USD", "booking_url": "https://www.anantara.com/en/rasananda-koh-phangan"}],
            "door_to_door_logistics": {"primary_transit": "Private longtail boat charter to Bottle Beach (15 mins). Vehicle excursion to Than Sadet Waterfall.", "departure_time": "09:30 AM", "arrival_time": "15:30 PM", "buffer_time": "Self-paced", "tips": "Bottle Beach accessible only by boat."},
            "curated_daily_flow": {"morning": "Private longtail boat past sea cliffs to secluded Bottle Beach.", "afternoon": "Fresh fruit smoothies on sand. Than Sadet royal waterfall granite boulders.", "evening": "Cliffside dinner at 2400 Bar overlooking the Gulf."},
            "essential_checklist": ["Dry bag for longtail boat"],
            "attached_documents": [],
            "google_maps_links": [{"label": "Bottle Beach", "url": "https://maps.google.com/?q=Bottle+Beach+Koh+Phangan"}]
        },
        {
            "day_number": 18,
            "date": "2026-09-28",
            "day_of_week": "Monday",
            "destination": "Koh Phangan: Koh Ma Reef & West Coast Sunset",
            "phase": "Couple Trip - Southern Thailand Romance",
            "phase_short": "Phase 2: Couple Trip",
            "status": "[ACTION REQUIRED - VETTED / UNBOOKED]",
            "status_badge": "UNBOOKED",
            "booking_summary": "Phangan night 4 unbooked",
            "weather_radar": {"temp_range": "27°C - 33°C", "condition": "Clear spectacular sunset", "precipitation_pct": "15%", "humidity": "71%", "attire_advice": "Beachwear day, sunset chic evening"},
            "luggage_action": "Resort stay.",
            "accommodation_matrix": [{"hotel_name": "Anantara Rasananda Koh Phangan Villas", "status": "UNBOOKED_VETTED_OPTION", "room_spec": "Ocean Pool Suite (Romantic King Bed)", "critic_score": 9.6, "critic_notes": "Night 4 on Phangan.", "price_per_night": "Est. $260 USD", "booking_url": "https://www.anantara.com/en/rasananda-koh-phangan"}],
            "door_to_door_logistics": {"primary_transit": "Private SUV hire for West Coast exploration.", "departure_time": "11:00 AM", "arrival_time": "20:30 PM", "buffer_time": "Self-paced", "tips": "Arrive at Top Rock Bar by 17:00."},
            "curated_daily_flow": {"morning": "Drive to Mae Haad; walk sandbar to Koh Ma for coral reef snorkeling.", "afternoon": "Lunch at Secret Beach / Karma Cafe.", "evening": "Top Rock Bar cliffside cushions watching fiery sunset over the sea."},
            "essential_checklist": ["Reef booties for Koh Ma coral"],
            "attached_documents": [],
            "google_maps_links": [{"label": "Koh Ma Sandbar", "url": "https://maps.google.com/?q=Koh+Ma+Koh+Phangan"}]
        },
        {
            "day_number": 19,
            "date": "2026-09-29",
            "day_of_week": "Tuesday",
            "destination": "Koh Phangan: Sri Thanu Wellness",
            "phase": "Couple Trip - Southern Thailand Romance",
            "phase_short": "Phase 2: Couple Trip",
            "status": "[ACTION REQUIRED - VETTED / UNBOOKED]",
            "status_badge": "UNBOOKED",
            "booking_summary": "Phangan night 5 unbooked",
            "weather_radar": {"temp_range": "27°C - 32°C", "condition": "Balmy sea breeze", "precipitation_pct": "20%", "humidity": "74%", "attire_advice": "Comfortable yoga/linen clothing"},
            "luggage_action": "Resort stay.",
            "accommodation_matrix": [{"hotel_name": "Anantara Rasananda Koh Phangan Villas", "status": "UNBOOKED_VETTED_OPTION", "room_spec": "Ocean Pool Suite (Romantic King Bed)", "critic_score": 9.6, "critic_notes": "Night 5 on Phangan.", "price_per_night": "Est. $260 USD", "booking_url": "https://www.anantara.com/en/rasananda-koh-phangan"}],
            "door_to_door_logistics": {"primary_transit": "Private SUV drive to Sri Thanu wellness village.", "departure_time": "09:30 AM", "arrival_time": "16:00 PM", "buffer_time": "Self-paced", "tips": "Sri Thanu is the island's wellness heart."},
            "curated_daily_flow": {"morning": "Couple sound healing session or oceanfront yoga. Barefoot stroll on Zen Beach.", "afternoon": "Organic lunch at Orion Healing Centre. Herbal steam at The Dome.", "evening": "Private beach candlelit dinner carved into sand by resort butler with tiki torches."},
            "essential_checklist": ["Book private beach dinner with hotel concierge"],
            "attached_documents": [],
            "google_maps_links": [{"label": "Zen Beach", "url": "https://maps.google.com/?q=Zen+Beach+Koh+Phangan"}]
        },
        {
            "day_number": 20,
            "date": "2026-09-30",
            "day_of_week": "Wednesday",
            "destination": "Koh Phangan: Haad Yuan Secret Cove",
            "phase": "Couple Trip - Southern Thailand Romance",
            "phase_short": "Phase 2: Couple Trip",
            "status": "[ACTION REQUIRED - VETTED / UNBOOKED]",
            "status_badge": "UNBOOKED",
            "booking_summary": "Phangan night 6 unbooked",
            "weather_radar": {"temp_range": "28°C - 33°C", "condition": "Tropical sun", "precipitation_pct": "10%", "humidity": "69%", "attire_advice": "Boho beachwear, flip flops"},
            "luggage_action": "Resort stay. Pack bags tonight for Lomprayah catamaran to Koh Tao tomorrow.",
            "accommodation_matrix": [{"hotel_name": "Anantara Rasananda Koh Phangan Villas", "status": "UNBOOKED_VETTED_OPTION", "room_spec": "Ocean Pool Suite (Romantic King Bed)", "critic_score": 9.6, "critic_notes": "Night 6 on Phangan (6 nights total in Phangan).", "price_per_night": "Est. $260 USD", "booking_url": "https://www.anantara.com/en/rasananda-koh-phangan"}],
            "door_to_door_logistics": {"primary_transit": "Longtail boat from Haad Rin around rocky headland to Haad Yuan.", "departure_time": "10:30 AM", "arrival_time": "16:30 PM", "buffer_time": "Boat only access", "tips": "Wooden cliff pathways of Eden Garden and Sanctuary."},
            "curated_daily_flow": {"morning": "Board longtail to Haad Yuan secret cove.", "afternoon": "Crystal aqua swimming. Stilt restaurant lunch overlooking bay.", "evening": "Japanese Teppanyaki & Robata grill at Yukinoya at Anantara. Pack for Koh Tao."},
            "essential_checklist": ["Confirm tomorrow's Lomprayah ferry to Koh Tao (11:00 AM)"],
            "attached_documents": [],
            "google_maps_links": [{"label": "Haad Yuan Beach", "url": "https://maps.google.com/?q=Haad+Yuan+Beach+Koh+Phangan"}]
        },

        # --- DAY 21: Koh Phangan -> Koh Tao ---
        {
            "day_number": 21,
            "date": "2026-10-01",
            "day_of_week": "Thursday",
            "destination": "Koh Phangan -> Koh Tao (Hillside Villa)",
            "phase": "Couple Trip - Southern Thailand Romance",
            "phase_short": "Phase 2: Couple Trip",
            "status": "[ACTION REQUIRED - VETTED / UNBOOKED]",
            "status_badge": "UNBOOKED",
            "booking_summary": "Phangan -> Tao ferry & Koh Tao villa unbooked",
            "weather_radar": {
                "temp_range": "27°C - 32°C",
                "condition": "Calm ocean swell, warm coastal sunshine",
                "precipitation_pct": "15%",
                "humidity": "72%",
                "attire_advice": "Light travel clothes, swimwear ready for instant dip into pool"
            },
            "luggage_action": "Bags transferred onto Lomprayah catamaran luggage cart; villa host pickup at Mae Haad Pier.",
            "accommodation_matrix": [
                {
                    "hotel_name": "The Place Luxury Boutique Villas Koh Tao",
                    "status": "UNBOOKED_VETTED_OPTION",
                    "room_spec": "One-Bedroom Private Pool Villa (King Bed + Private Horizon Pool)",
                    "critic_score": 9.7,
                    "critic_notes": "Vetted recommendation. Isolated hillside sanctuary, floor-to-ceiling glass, uninterrupted ocean panoramas, zero noise.",
                    "price_per_night": "Est. $240 USD / ~8,500 THB",
                    "booking_url": "https://theplacekohtao.com/",
                    "map_query": "The+Place+Luxury+Boutique+Villas+Koh+Tao"
                }
            ],
            "door_to_door_logistics": {
                "primary_transit": "Proposed: 09:45 AM transfer to Phangan Thong Sala. 11:00 AM Lomprayah catamaran to Koh Tao Mae Haad Pier (1 hr, arr 12:00 PM). Host greeting, SUV up to hillside villa.",
                "departure_time": "09:45 AM Phangan",
                "arrival_time": "12:30 PM Koh Tao villa",
                "buffer_time": "Luggage handled directly from pier to villa",
                "tips": "The Place provides a complimentary mobile phone with direct villa host contact."
            },
            "curated_daily_flow": {
                "morning": "Lomprayah catamaran skimming north across Gulf to Koh Tao.",
                "afternoon": "Check in The Place Luxury Boutique Villas. Infinity pool floating over jungle canopy with sweeping sea views.",
                "evening": "In-villa romantic barbecue prepared by private chef or casual dining at Sairee Beach (Barracuda snapper)."
            },
            "essential_checklist": [
                "Book Lomprayah catamaran (Phangan to Tao 11:00 AM)",
                "Book Koh Tao villa (The Place Luxury Villas for 6 nights)",
                "Koh Tao island fee: 20 THB / person at pier"
            ],
            "attached_documents": [],
            "google_maps_links": [
                {"label": "The Place Luxury Boutique Villas", "url": "https://maps.google.com/?q=The+Place+Luxury+Boutique+Villas+Koh+Tao"}
            ]
        },

        # --- DAYS 22-26: Koh Tao Stays (Days 22, 23, 24, 25, 26) ---
        {
            "day_number": 22,
            "date": "2026-10-02",
            "day_of_week": "Friday",
            "destination": "Koh Tao: Shark Bay Marine Life & Viewpoints",
            "phase": "Couple Trip - Southern Thailand Romance",
            "phase_short": "Phase 2: Couple Trip",
            "status": "[ACTION REQUIRED - VETTED / UNBOOKED]",
            "status_badge": "UNBOOKED",
            "booking_summary": "Koh Tao night 2 unbooked",
            "weather_radar": {"temp_range": "28°C - 33°C", "condition": "Turquoise visibility", "precipitation_pct": "10%", "humidity": "68%", "attire_advice": "Snorkel gear, rashguard, trainers for viewpoint"},
            "luggage_action": "Villa stay.",
            "accommodation_matrix": [{"hotel_name": "The Place Luxury Boutique Villas Koh Tao", "status": "UNBOOKED_VETTED_OPTION", "room_spec": "One-Bedroom Private Pool Villa (King Bed)", "critic_score": 9.7, "critic_notes": "Night 2 on Koh Tao.", "price_per_night": "Est. $240 USD", "booking_url": "https://theplacekohtao.com/"}],
            "door_to_door_logistics": {"primary_transit": "Private 4x4 down to Shark Bay (Thian Og) and Freedom Beach.", "departure_time": "09:00 AM", "arrival_time": "16:00 PM", "buffer_time": "Self-paced", "tips": "Morning high-tide provides optimal turtle sighting."},
            "curated_daily_flow": {"morning": "Snorkel Shark Bay alongside giant green sea turtles and blacktip reef sharks.", "afternoon": "Short hike up John-Suwan Viewpoint for Koh Tao's iconic twin-bay panorama.", "evening": "Sunset cocktails at Sun Suwan 360 bar. Fine Thai dining at The Gallery Restaurant."},
            "essential_checklist": ["Reef-safe sunscreen only (strictly enforced)"],
            "attached_documents": [],
            "google_maps_links": [{"label": "Shark Bay", "url": "https://maps.google.com/?q=Shark+Bay+Koh+Tao"}]
        },
        {
            "day_number": 23,
            "date": "2026-10-03",
            "day_of_week": "Saturday",
            "destination": "Koh Tao: Koh Nang Yuan Private Charter",
            "phase": "Couple Trip - Southern Thailand Romance",
            "phase_short": "Phase 2: Couple Trip",
            "status": "[ACTION REQUIRED - VETTED / UNBOOKED]",
            "status_badge": "UNBOOKED",
            "booking_summary": "Koh Tao night 3 unbooked",
            "weather_radar": {"temp_range": "28°C - 33°C", "condition": "Flat calm sea, 25m visibility", "precipitation_pct": "10%", "humidity": "67%", "attire_advice": "Swimwear, beach towel, reusable flask"},
            "luggage_action": "Villa stay.",
            "accommodation_matrix": [{"hotel_name": "The Place Luxury Boutique Villas Koh Tao", "status": "UNBOOKED_VETTED_OPTION", "room_spec": "One-Bedroom Private Pool Villa (King Bed)", "critic_score": 9.7, "critic_notes": "Night 3 on Koh Tao.", "price_per_night": "Est. $240 USD", "booking_url": "https://theplacekohtao.com/"}],
            "door_to_door_logistics": {"primary_transit": "Private longtail boat charter to Koh Nang Yuan (08:30 AM early start beats crowds).", "departure_time": "08:30 AM", "arrival_time": "13:30 PM", "buffer_time": "Early arrival guarantees empty sandbar photos", "tips": "No plastic bottles allowed on Nang Yuan."},
            "curated_daily_flow": {"morning": "Board private longtail boat to Koh Nang Yuan sand spit as gates open. Hike to summit postcard viewpoint.", "afternoon": "Snorkel Japanese Gardens reef (electric-blue clams, clownfish).", "evening": "Fizz Beach Lounge on Sairee sand with beanbags and mojitos. Dinner at Blue Water Cafe."},
            "essential_checklist": ["Koh Nang Yuan entrance fee (250 THB / person)"],
            "attached_documents": [],
            "google_maps_links": [{"label": "Koh Nang Yuan Viewpoint", "url": "https://maps.google.com/?q=Koh+Nang+Yuan+Viewpoint"}]
        },
        {
            "day_number": 24,
            "date": "2026-10-04",
            "day_of_week": "Sunday",
            "destination": "Koh Tao: Scuba / Tanote Bay & Cliffside Dining",
            "phase": "Couple Trip - Southern Thailand Romance",
            "phase_short": "Phase 2: Couple Trip",
            "status": "[ACTION REQUIRED - VETTED / UNBOOKED]",
            "status_badge": "UNBOOKED",
            "booking_summary": "Koh Tao night 4 unbooked",
            "weather_radar": {"temp_range": "27°C - 32°C", "condition": "Warm tropical sun", "precipitation_pct": "15%", "humidity": "71%", "attire_advice": "Swimwear, boat clothes, sunglasses"},
            "luggage_action": "Villa stay.",
            "accommodation_matrix": [{"hotel_name": "The Place Luxury Boutique Villas Koh Tao", "status": "UNBOOKED_VETTED_OPTION", "room_spec": "One-Bedroom Private Pool Villa (King Bed)", "critic_score": 9.7, "critic_notes": "Night 4 on Koh Tao.", "price_per_night": "Est. $240 USD", "booking_url": "https://theplacekohtao.com/"}],
            "door_to_door_logistics": {"primary_transit": "Dive boat excursion or taxi hop to wild east coast Tanote Bay.", "departure_time": "08:00 AM", "arrival_time": "15:00 PM", "buffer_time": "Self-paced", "tips": "Tanote Bay offers granite rock leaping and coral drop-offs."},
            "curated_daily_flow": {"morning": "Scuba dive / discover scuba at Chumphon Pinnacle or granite rock leaping at Tanote Bay.", "afternoon": "Poolside massage on private timber deck listening to jungle cicadas.", "evening": "Cliffside fine dining at Jamahkiri Restaurant perched 50m above Shark Bay."},
            "essential_checklist": ["No-fly buffer check: Flying Oct 07, so Oct 04 dive provides 65+ hrs buffer!"],
            "attached_documents": [],
            "google_maps_links": [{"label": "Jamahkiri Restaurant", "url": "https://maps.google.com/?q=Jamahkiri+Restaurant+Koh+Tao"}]
        },
        {
            "day_number": 25,
            "date": "2026-10-05",
            "day_of_week": "Monday",
            "destination": "Koh Tao: Hin Wong Bay Kayaking",
            "phase": "Couple Trip - Southern Thailand Romance",
            "phase_short": "Phase 2: Couple Trip",
            "status": "[ACTION REQUIRED - VETTED / UNBOOKED]",
            "status_badge": "UNBOOKED",
            "booking_summary": "Koh Tao night 5 unbooked",
            "weather_radar": {"temp_range": "27°C - 32°C", "condition": "Sunny morning, sea breeze", "precipitation_pct": "20%", "humidity": "73%", "attire_advice": "Swimwear, rashguard, strap-on sandals"},
            "luggage_action": "Villa stay.",
            "accommodation_matrix": [{"hotel_name": "The Place Luxury Boutique Villas Koh Tao", "status": "UNBOOKED_VETTED_OPTION", "room_spec": "One-Bedroom Private Pool Villa (King Bed)", "critic_score": 9.7, "critic_notes": "Night 5 on Koh Tao.", "price_per_night": "Est. $240 USD", "booking_url": "https://theplacekohtao.com/"}],
            "door_to_door_logistics": {"primary_transit": "Longtail boat or 4x4 to serene northeast coast Hin Wong Bay.", "departure_time": "10:00 AM", "arrival_time": "16:00 PM", "buffer_time": "Self-paced", "tips": "Hin Wong has massive boulder fields underwater."},
            "curated_daily_flow": {"morning": "Rent ocean kayaks at Hin Wong Bay, paddle along granite cliffs to secret coves.", "afternoon": "Snorkel through schools of thousands of glittering blue fusiliers.", "evening": "Sunset drinks at Sairee Cottage Beach Club. Dinner at Whitening (beachfront dining)."},
            "essential_checklist": ["Dry bag for kayak"],
            "attached_documents": [],
            "google_maps_links": [{"label": "Hin Wong Bay", "url": "https://maps.google.com/?q=Hin+Wong+Bay+Koh+Tao"}]
        },
        {
            "day_number": 26,
            "date": "2026-10-06",
            "day_of_week": "Tuesday",
            "destination": "Koh Tao: Island Finale & Sunset Toast",
            "phase": "Couple Trip - Southern Thailand Romance",
            "phase_short": "Phase 2: Couple Trip",
            "status": "[ACTION REQUIRED - VETTED / UNBOOKED]",
            "status_badge": "UNBOOKED",
            "booking_summary": "Koh Tao night 6 unbooked",
            "weather_radar": {"temp_range": "28°C - 33°C", "condition": "Glorious tropical sun", "precipitation_pct": "10%", "humidity": "69%", "attire_advice": "Resort casual, evening linen dinner wear"},
            "luggage_action": "Pack and zip suitcases for tomorrow's transfer to Bangkok (13 Gulf nights complete!).",
            "accommodation_matrix": [{"hotel_name": "The Place Luxury Boutique Villas Koh Tao", "status": "UNBOOKED_VETTED_OPTION", "room_spec": "One-Bedroom Private Pool Villa (King Bed)", "critic_score": 9.7, "critic_notes": "Night 6 on Koh Tao (6 nights total in Koh Tao; 13 nights Gulf total).", "price_per_night": "Est. $240 USD", "booking_url": "https://theplacekohtao.com/"}],
            "door_to_door_logistics": {"primary_transit": "Self-paced local transport. Confirm morning pier transfer.", "departure_time": "N/A", "arrival_time": "N/A", "buffer_time": "Island finale", "tips": "Confirm pier pickup time with villa manager tonight."},
            "curated_daily_flow": {"morning": "Lazy morning floating in private infinity pool with tropical fruit platter.", "afternoon": "Mae Haad boutique shopping for handcrafted Thai silver and linen. Couple herbal scrub.", "evening": "Gulf Grand Sunset Toast: Panoramic table at Sunset 360 Bar. Dinner at Hippo Bar & Grill."},
            "essential_checklist": ["Pack scuba gear and beach clothes into checked suitcase", "Set alarm for 08:00 AM checkout"],
            "attached_documents": [],
            "google_maps_links": [{"label": "Sunset 360 Bar", "url": "https://maps.google.com/?q=Sunset+360+Bar+Koh+Tao"}]
        },

        # --- DAY 27: Koh Tao -> Bangkok ---
        {
            "day_number": 27,
            "date": "2026-10-07",
            "day_of_week": "Wednesday",
            "destination": "Koh Tao -> Bangkok (Riverside Boutique)",
            "phase": "Couple Trip - Southern Thailand Romance",
            "phase_short": "Phase 2: Couple Trip",
            "status": "[ACTION REQUIRED - VETTED / UNBOOKED]",
            "status_badge": "UNBOOKED",
            "booking_summary": "Koh Tao -> Bangkok transit & hotel unbooked",
            "weather_radar": {
                "temp_range": "27°C - 33°C",
                "condition": "Warm urban sunset, clear skyline",
                "precipitation_pct": "25%",
                "humidity": "72%",
                "attire_advice": "Comfortable transit clothes, smart evening dress/collar shirt for rooftop bar"
            },
            "luggage_action": "Luggage transferred from ferry to airport transfer.",
            "accommodation_matrix": [
                {
                    "hotel_name": "Riva Arun Bangkok / The Mustang Blu",
                    "status": "UNBOOKED_VETTED_OPTION",
                    "room_spec": "Premium Chao Phraya River View King",
                    "critic_score": 9.4,
                    "critic_notes": "Vetted recommendation. Unrivaled view directly facing illuminated Wat Arun across the Chao Phraya river. Boutique romantic atmosphere.",
                    "price_per_night": "Est. $145 USD / ~5,100 THB",
                    "booking_url": "https://www.rivaarunbangkok.com/",
                    "map_query": "Riva+Arun+Bangkok"
                }
            ],
            "door_to_door_logistics": {
                "primary_transit": "Proposed: 09:30 AM Lomprayah catamaran Koh Tao -> Samui Pralarn Pier (arr 11:15 AM). 14:00 PM Bangkok Airways flight USM -> BKK (arr 15:15 PM). Transfer to Riva Arun Bangkok.",
                "departure_time": "09:00 AM Koh Tao",
                "arrival_time": "16:45 PM Bangkok hotel",
                "buffer_time": "Smooth flight connection back to Bangkok capital",
                "tips": "Book Lomprayah + Bangkok Airways combo 1-2 months prior."
            },
            "curated_daily_flow": {
                "morning": "Morning catamaran crossing to Samui open-air garden airport.",
                "afternoon": "Quick flight into Bangkok Suvarnabhumi. Private transfer to riverside boutique hotel Riva Arun.",
                "evening": "Private river balcony watching illuminated longtail boats on Chao Phraya. Octave Rooftop Lounge cocktails & Supanniga dinner."
            },
            "essential_checklist": [
                "Book Koh Tao to Bangkok transit (catamaran + flight)",
                "Book Bangkok riverside hotel (Riva Arun)"
            ],
            "attached_documents": [],
            "google_maps_links": [
                {"label": "Riva Arun Bangkok", "url": "https://maps.google.com/?q=Riva+Arun+Bangkok"},
                {"label": "Octave Rooftop Lounge", "url": "https://maps.google.com/?q=Octave+Rooftop+Bangkok"}
            ]
        },

        # --- DAY 28: Bangkok Finale ---
        {
            "day_number": 28,
            "date": "2026-10-08",
            "day_of_week": "Thursday",
            "destination": "Bangkok: Thonburi Khlongs, ICONSIAM & Fine Dining",
            "phase": "Couple Trip - Southern Thailand Romance",
            "phase_short": "Phase 2: Couple Trip",
            "status": "[ACTION REQUIRED - VETTED / UNBOOKED]",
            "status_badge": "UNBOOKED",
            "booking_summary": "Bangkok night 2 unbooked",
            "weather_radar": {
                "temp_range": "27°C - 33°C",
                "condition": "Warm urban sun, breezy riverside evening",
                "precipitation_pct": "20%",
                "humidity": "70%",
                "attire_advice": "Smart casual daywear, sophisticated evening attire for Michelin fine dining"
            },
            "luggage_action": "Evening full pack & weigh of checked suitcase + 55L pack. Finalize duty-free shopping.",
            "accommodation_matrix": [
                {
                    "hotel_name": "Riva Arun Bangkok / The Mustang Blu",
                    "status": "UNBOOKED_VETTED_OPTION",
                    "room_spec": "Premium Chao Phraya River View King",
                    "critic_score": 9.4,
                    "critic_notes": "Finale night in Thailand.",
                    "price_per_night": "Est. $145 USD / ~5,100 THB",
                    "booking_url": "https://www.rivaarunbangkok.com/",
                    "map_query": "Riva+Arun+Bangkok"
                }
            ],
            "door_to_door_logistics": {
                "primary_transit": "Chao Phraya Express boat & private longtail canal tour from Tha Tien. BTS Skytrain / Grab.",
                "departure_time": "10:00 AM",
                "arrival_time": "Self-paced",
                "buffer_time": "Pre-departure preparation day",
                "tips": "Gold Line train connects directly into ICONSIAM luxury mall without road traffic."
            },
            "curated_daily_flow": {
                "morning": "Private teak longtail boat cruise through tranquil Thonburi canals past stilt houses and giant golden Buddha at Wat Paknam.",
                "afternoon": "ICONSIAM luxury mall and indoor SookSiam artisan floating market.",
                "evening": "Thailand Grand Finale Michelin-Star Feast: Sühring (modern German glasshouse villa) or Paste Bangkok (refined royal Thai). Toast to 29 days!"
            },
            "essential_checklist": [
                "Pack all liquids over 100ml into checked suitcase",
                "Weigh bags: Ensure checked suitcase <= 23kg and backpack <= 7-10kg"
            ],
            "attached_documents": [],
            "google_maps_links": [
                {"label": "ICONSIAM Luxury Mall", "url": "https://maps.google.com/?q=ICONSIAM+Bangkok"}
            ]
        },

        # --- DAY 29: Bangkok Departure ---
        {
            "day_number": 29,
            "date": "2026-10-09",
            "day_of_week": "Friday",
            "destination": "Bangkok (BKK) Departure -> TLV via AUH",
            "phase": "Couple Trip - Southern Thailand Romance",
            "phase_short": "Trip Finale",
            "status": "[CONFIRMED - BOOKED]",
            "status_badge": "CONFIRMED",
            "booking_summary": "Return Flight BKK->TLV Confirmed (Booking: 9KDEH2)",
            "weather_radar": {
                "temp_range": "28°C - 33°C",
                "condition": "Warm tropical sun over Bangkok",
                "precipitation_pct": "20%",
                "humidity": "68%",
                "attire_advice": "Comfortable long-haul flight layers, compression socks, slip-on shoes"
            },
            "luggage_action": "All gear repacked: 1x 55L clamshell backpack + 1x checked suitcase. Checked in at BKK international departure hall.",
            "accommodation_matrix": [],
            "door_to_door_logistics": {
                "primary_transit": "Hotel checkout. Private express transfer to Suvarnabhumi International Airport (BKK, 40 mins). Check in 3.5 hours prior for international flight 9KDEH2 BKK -> TLV via Abu Dhabi (AUH).",
                "departure_time": "3.5 hours before flight departure",
                "arrival_time": "BKK International Terminal",
                "buffer_time": "3.5 hours for VAT refund inspection, bag drop, security, and duty-free",
                "tips": "Present VAT refund yellow forms (P.P.10) at customs desk BEFORE passport control."
            },
            "curated_daily_flow": {
                "morning": "Final riverfront breakfast watching boats on Chao Phraya. Last minute foot massage.",
                "afternoon": "Checkout, express highway transfer to Suvarnabhumi Airport Level 4 Departure Hall.",
                "evening": "Check-in for international departure flight 9KDEH2. Clear security and passport control. Board flight to Tel Aviv via Abu Dhabi. Safe travels!"
            },
            "essential_checklist": [
                "Flight booking reference 9KDEH2 ready",
                "Passports valid for at least 6 months",
                "VAT refund slips stamped before security"
            ],
            "attached_documents": [
                {
                    "doc_id": "FLIGHT-BKK-TLV-9KDEH2-EYAL",
                    "title": "Etihad Airways E-Ticket (Eyal Andreson)",
                    "ref": "Etihad: 9KDEH2",
                    "status": "Verified Official E-Ticket (Gmail)",
                    "badge": "CONFIRMED & DOWNLOADED",
                    "file_path": "documents/Etihad_BKK_TLV_9KDEH2_Eyal_Andreson.pdf",
                    "file_name": "Etihad_BKK_TLV_9KDEH2_Eyal_Andreson.pdf"
                },
                {
                    "doc_id": "FLIGHT-BKK-TLV-9KDEH2-MARIA",
                    "title": "Etihad Airways E-Ticket (Maria Miriam Malayev)",
                    "ref": "Etihad: 9KDEH2",
                    "status": "Verified Official E-Ticket (Gmail)",
                    "badge": "CONFIRMED & DOWNLOADED",
                    "file_path": "documents/Etihad_BKK_TLV_9KDEH2_Maria_Miriam_Malayev.pdf",
                    "file_name": "Etihad_BKK_TLV_9KDEH2_Maria_Miriam_Malayev.pdf"
                }
            ],
            "google_maps_links": [
                {"label": "Suvarnabhumi Airport Departures", "url": "https://maps.google.com/?q=Suvarnabhumi+Airport+Departures"}
            ]
        }
    ]

    master_payload = {
        "title": "Master Itinerary: Thailand & Vietnam [Live Travel OS]",
        "generated_at": "2026-09-09T04:03:00Z",
        "system_version": "2.5.0",
        "audit_note": "Audited: Only confirmed bookings from user profile are marked CONFIRMED. All other days marked UNBOOKED with vetted recommendations.",
        "confirmed_metrics": {
            "total_days": 29,
            "confirmed_days_count": 4,
            "unbooked_days_count": 25,
            "confirmed_references": [
                {"item": "TDAC Digital Arrival Card", "ref": "#30C4358"},
                {"item": "Sukhon Hotel Bangkok", "ref": "Booking: 697155847"},
                {"item": "BKK -> HAN Flight (Sep 12)", "ref": "Booking: 1145-554-179"},
                {"item": "HAN -> BKK Flight (Sep 24)", "ref": "Booking: 1145-554-179"},
                {"item": "BKK -> TLV Return Flight (Oct 09)", "ref": "Booking: 9KDEH2"}
            ]
        },
        "traveler_profile": {
            "party_phase_1": {
                "label": "Vietnam Expedition (Sep 11–24, 2026)",
                "party": "Traveler + Friend",
                "room_requirement": "Strictly Twin Beds / Two Separate Beds per room",
                "vibe": "Adventure, trekking, scenic loops, active transport, street cuisine",
                "luggage": "55L+ clamshell backpack ONLY"
            },
            "transition": {
                "date": "2026-09-24",
                "flight": "Hanoi (HAN) -> Bangkok (BKK) 12:45 PM (Booking: 1145-554-179 - CONFIRMED)",
                "separation": "Friend departs/separates at BKK",
                "luggage_retrieval": "Retrieve checked suitcase at AIRPORTELs Suvarnabhumi Basement (Floor B)",
                "reunion": "Traveler reunites with Girlfriend in Bangkok",
                "south_flight": "Bangkok (BKK) -> Koh Samui (USM) Direct (Bangkok Airways PG 169 - UNBOOKED, BUY IN JULY/AUG)"
            },
            "party_phase_2": {
                "label": "Gulf of Thailand & Bangkok Finale (Sep 24 – Oct 09, 2026)",
                "party": "Traveler + Girlfriend",
                "room_requirement": "Strictly Double / Romantic King Bed with Prime Ocean Views",
                "vibe": "Boutique romantic stays, beaches, high-end island dining, relaxed diving/snorkeling",
                "pacing": "13 nights Gulf (1 Samui + 6 Phangan + 6 Tao) + 2 nights Bangkok Finale = 15 nights total",
                "departure_flight": "Oct 09: BKK -> TLV via AUH (Booking: 9KDEH2 - CONFIRMED)"
            }
        },
        "luggage_storage_protocol": {
            "facility": "AIRPORTELs Luggage Storage (Suvarnabhumi Airport Floor B, Airport Rail Link Level)",
            "status": "RECOMMENDED_PLAN_UNBOOKED",
            "dropoff_date": "2026-09-12 (Morning, before 11:55 flight to HAN)",
            "pickup_date": "2026-09-24 (14:35 arrival from HAN)",
            "duration": "12 Days",
            "storage_cost": "~100-150 THB / day (pay at counter or online)",
            "item_deposited": "1x Large Checked Suitcase containing Phase 2 resort attire",
            "item_kept": "1x 55L Clamshell Backpack (strictly backpack-only throughout Vietnam)"
        },
        "flight_radar_bkk_usm": {
            "route": "Bangkok Suvarnabhumi (BKK) -> Koh Samui (USM)",
            "date": "2026-09-24",
            "status": "UNBOOKED_TRACKING",
            "recommended_flight": "Bangkok Airways PG 169 (Dep 17:15 BKK - Arr 18:20 USM)",
            "backup_flight": "Bangkok Airways PG 175 (Dep 18:00 BKK - Arr 19:05 USM)",
            "cheapest_bucket": "Web Saver (Approx. $115 - $135 USD / 4,100 - 4,800 THB)",
            "optimal_booking_window": "6 to 8 weeks prior to departure (Mid-July to Early August 2026)."
        },
        "total_days": len(days),
        "days": days
    }

    out_path = os.path.join(os.path.dirname(__file__), "itinerary_data.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(master_payload, f, indent=2, ensure_ascii=False)
    print(f"Successfully generated audited {out_path} with {len(days)} days!")

if __name__ == "__main__":
    build_itinerary()
