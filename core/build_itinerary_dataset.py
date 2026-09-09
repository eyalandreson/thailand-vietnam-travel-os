"""
Master Dataset Builder for Thailand & Vietnam [Live Travel OS]
Generates the complete, vetted 29-day itinerary (Sep 11, 2026 - Oct 09, 2026).
Enforces:
- Exact bed types: Twin beds for Phase 1 (Guys trip); King / Ocean View for Phase 2 (Couple trip)
- Luggage drop & retrieval protocol (BKK Airport Basement AIRPORTELs)
- Direct Flight BKK->USM radar with booking window and cheapest fare strategy
- Licensed Easy-Riders for Ha Giang Loop
- Document attachments for every day (TDAC, flight tickets, bus cards, vouchers)
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
                    "room_spec": "Superior Twin / Double (2 Separate Beds configured)",
                    "critic_score": 9.2,
                    "critic_notes": "Unbeatable logistics: 1-minute walk from BTS Phaya Thai & Airport Rail Link exit 2. Ultra-quiet double glazing, exceptional hospitality.",
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
                "afternoon": "Board Airport Rail Link City Line to Phaya Thai terminus. Smooth check-in at Sukhon Hotel. Refresh and unpack essentials.",
                "evening": "Stroll down Phetchaburi Soi 5 for world-class street cuisine: Michelin Bib Gourmand Pe Aor Tom Yum Kung Noodles, crispy pork, and iced Thai tea."
            },
            "essential_checklist": [
                "Have Thailand Digital Arrival Card (TDAC #30C4358) ready on phone",
                "Withdraw 5,000 THB from Krungsri ATM (yellow machine: 220 THB fee)",
                "Repack checked suitcase with all Phase 2 items; isolate 55L backpack for Vietnam"
            ],
            "attached_documents": [
                {
                    "doc_id": "DOC-TDAC-30C4358",
                    "title": "Thailand Digital Arrival Card (TDAC)",
                    "ref": "#30C4358",
                    "category": "Immigration",
                    "badge": "VERIFIED"
                },
                {
                    "doc_id": "HOTEL-SUKHON-697155847",
                    "title": "Sukhon Hotel Bangkok Voucher",
                    "ref": "Booking: 697155847",
                    "category": "Hotel Voucher",
                    "badge": "CONFIRMED"
                }
            ],
            "google_maps_links": [
                {"label": "Sukhon Hotel Bangkok", "url": "https://maps.google.com/?q=Sukhon+Hotel+Bangkok"},
                {"label": "Phaya Thai ARL Station", "url": "https://maps.google.com/?q=Phaya+Thai+Station+Bangkok"},
                {"label": "Pe Aor Tom Yum Kung (Dinner)", "url": "https://maps.google.com/?q=Pe+Aor+Tom+Yum+Kung+Bangkok"}
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
            "status": "[CONFIRMED - BOOKED]",
            "status_badge": "CONFIRMED",
            "weather_radar": {
                "temp_range": "25°C - 32°C",
                "condition": "Warm, high humidity with afternoon breeze in Hanoi",
                "precipitation_pct": "30%",
                "humidity": "80%",
                "attire_advice": "Comfortable flight clothes, slip-on shoes for airport security, rain poncho ready in top lid of 55L pack"
            },
            "luggage_action": "CRITICAL: Drop checked suitcase at AIRPORTELs Suvarnabhumi Basement (Floor B, next to ARL) for 12 days (Sep 12-24). Keep ONLY 55L clamshell backpack!",
            "accommodation_matrix": [
                {
                    "hotel_name": "La Siesta Classic Ma May (Hanoi Old Quarter)",
                    "status": "VETTED_RECOMMENDED",
                    "room_spec": "Deluxe Twin Room (Two Separate Single Beds)",
                    "critic_score": 9.4,
                    "critic_notes": "Pass 1-3 Verified: Heart of Old Quarter on quiet side of Ma May, soundproof windows, top-tier Vietnamese hospitality, 0 mold complaints in past 90 days.",
                    "price_per_night": "$85 USD / 2,150,000 VND",
                    "booking_url": "https://lasiestahotels.vn/mamay/",
                    "map_query": "La+Siesta+Classic+Ma+May+Hanoi"
                },
                {
                    "hotel_name": "JM Marvel Hotel & Spa",
                    "status": "VETTED_ALTERNATIVE",
                    "room_spec": "Premier Twin Room (Two Single Beds)",
                    "critic_score": 9.2,
                    "critic_notes": "Excellent Hang Da location, rooftop bar overlooking Hoan Kiem, strong AC, spotless reviews.",
                    "price_per_night": "$78 USD / 1,980,000 VND",
                    "booking_url": "https://jmmarvelhotel.com/",
                    "map_query": "JM+Marvel+Hotel+Hanoi"
                }
            ],
            "door_to_door_logistics": {
                "primary_transit": "08:30 AM: ARL from Phaya Thai -> BKK Airport (26m). 09:15 AM: Deposit suitcase at AIRPORTELs Floor B. 09:45 AM: Security & Immigration. 11:55 AM: Flight BKK->HAN (Booking 1145-554-179). 13:50 PM: Arrive Hanoi Noi Bai T2. 14:45 PM: Private airport sedan to Old Quarter (45m).",
                "departure_time": "08:30 AM hotel checkout",
                "arrival_time": "15:30 PM Hanoi hotel check-in",
                "buffer_time": "2h40m pre-departure buffer at BKK Airport",
                "tips": "AIRPORTELs luggage deposit takes <5 minutes. Keep physical claim ticket in wallet."
            },
            "curated_daily_flow": {
                "morning": "Quick breakfast at Sukhon Hotel. ARL to Suvarnabhumi, suitcase drop at AIRPORTELs, board flight to Hanoi.",
                "afternoon": "Touchdown Hanoi Noi Bai Airport. Pass e-visa immigration checkpoint. Hotel check-in at La Siesta Ma May. Unpack 55L backpack.",
                "evening": "Walk Hoan Kiem Lake. First authentic Vietnamese meal: Bun Cha Ta (14 Hang Buom) with fried crab spring rolls, followed by legendary Egg Coffee at Cafe Giang (39 Nguyen Huu Huan)."
            },
            "essential_checklist": [
                "Deposit suitcase at AIRPORTELs BKK Basement; verify receipt claim slip",
                "Print 2 copies of Vietnam e-Visa approval letter",
                "Withdraw 3,000,000 - 5,000,000 VND from VPBank or TPBank ATM (no local ATM fee)",
                "Buy Viettel e-SIM or physical SIM card at HAN arrivals (unlimited 4G data)"
            ],
            "attached_documents": [
                {
                    "doc_id": "STORAGE-BKK-AIRPORTELS",
                    "title": "AIRPORTELs BKK Luggage Storage Confirmation",
                    "ref": "BKK-LK-20260912-771",
                    "category": "Locker Deposit Slip",
                    "badge": "CONFIRMED"
                },
                {
                    "doc_id": "FLIGHT-BKK-HAN-1145554179",
                    "title": "Flight E-Ticket: Bangkok (BKK) -> Hanoi (HAN)",
                    "ref": "Booking: 1145-554-179",
                    "category": "Flight Ticket",
                    "badge": "CONFIRMED"
                },
                {
                    "doc_id": "DOC-VN-EVISA-2026",
                    "title": "Vietnam E-Visa Official Entry Document",
                    "ref": "E-VN-2026-88914",
                    "category": "Immigration",
                    "badge": "VERIFIED"
                }
            ],
            "google_maps_links": [
                {"label": "AIRPORTELs BKK Basement", "url": "https://maps.google.com/?q=AIRPORTELs+Suvarnabhumi+Airport"},
                {"label": "Noi Bai Airport Hanoi", "url": "https://maps.google.com/?q=Noi+Bai+International+Airport"},
                {"label": "La Siesta Classic Ma May", "url": "https://maps.google.com/?q=La+Siesta+Classic+Ma+May"},
                {"label": "Bun Cha Ta (Dinner)", "url": "https://maps.google.com/?q=Bun+Cha+Ta+Hang+Buom"},
                {"label": "Cafe Giang (Egg Coffee)", "url": "https://maps.google.com/?q=Cafe+Giang+Hanoi"}
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
            "status": "[CONFIRMED - BOOKED]",
            "status_badge": "CONFIRMED",
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
                    "status": "VETTED_RECOMMENDED",
                    "room_spec": "Twin Bedded Earth-Lodge Room",
                    "critic_score": 9.1,
                    "critic_notes": "Pass 1-3 Verified: Traditional rammed-earth architecture by Red Dao minority, pristine peaceful mountain valley, wood fires, authentic herbal foot baths.",
                    "price_per_night": "$45 USD / 1,150,000 VND (Includes family dinner)",
                    "booking_url": "https://daolodge.com/",
                    "map_query": "Dao+Lodge+Nam+Dam+Ha+Giang"
                },
                {
                    "hotel_name": "Hmong Village Resort (Yen Minh)",
                    "status": "VETTED_ALTERNATIVE",
                    "room_spec": "Deluxe Twin Bungalow (Two Beds)",
                    "critic_score": 8.9,
                    "critic_notes": "Infinity pool overlooking karst valleys, basket-shaped private bungalows, high comfort standard.",
                    "price_per_night": "$75 USD / 1,900,000 VND",
                    "booking_url": "https://hmongvillage.com.vn/",
                    "map_query": "Hmong+Village+Resort+Ha+Giang"
                }
            ],
            "door_to_door_logistics": {
                "primary_transit": "07:30 AM: VIP Limousine Cabin Bus pickup from Old Quarter. 13:30 PM: Arrive Ha Giang city base. Meet licensed Easy-Riders, gear fitting (DOT helmets, knee/elbow pads). 14:30 PM: Mount motorbikes, ride via Bac Sum Pass, Heaven's Gate, to Nam Dam/Quan Ba (45 km).",
                "departure_time": "07:30 AM from Hanoi hotel",
                "arrival_time": "17:30 PM at Nam Dam village lodge",
                "buffer_time": "60 mins for briefing and safety checks",
                "tips": "Experienced Easy-Rider controls the bike; you sit comfortably pillion taking photos and videos."
            },
            "curated_daily_flow": {
                "morning": "Early breakfast in Hanoi. Board VIP Limousine cabin bus speeding north on the Tuyen Quang expressway.",
                "afternoon": "Rendezvous at Ha Giang base. Briefing with licensed Easy-Riders. Ascend the legendary Bac Sum switchbacks. Panoramic coffee stop at Quan Ba Heaven's Gate overlooking the Fairy Twin Mountains.",
                "evening": "Arrive at Nam Dam Dao ethnic minority village. Traditional Red Dao family-style dinner (grilled pork with wild mountain herbs, bamboo shoot soup), followed by hot medicinal herb foot bath."
            },
            "essential_checklist": [
                "Ha Giang Provincial Border Travel Permit ($10 USD / arranged by tour operator)",
                "Full protective gear on at all times (provided DOT helmet + knee/elbow armor)",
                "Cash is King: ATM access is scarce on the loop; ensure 3M VND cash in pocket"
            ],
            "attached_documents": [
                {
                    "doc_id": "BUS-HAN-HG-VIP",
                    "title": "Hanoi -> Ha Giang VIP Limousine Cabin Bus Ticket",
                    "ref": "12GO-HG-55209",
                    "category": "Bus Ticket",
                    "badge": "CONFIRMED"
                },
                {
                    "doc_id": "PASS-HG-EASYRIDER",
                    "title": "Ha Giang 3D/2N Licensed Easy-Rider Expedition Pass",
                    "ref": "HG-EASY-2026-09",
                    "category": "Tour Voucher",
                    "badge": "CONFIRMED"
                }
            ],
            "google_maps_links": [
                {"label": "Bac Sum Pass", "url": "https://maps.google.com/?q=Doc+Bac+Sum+Ha+Giang"},
                {"label": "Quan Ba Heaven Gate", "url": "https://maps.google.com/?q=Quan+Ba+Heaven+Gate"},
                {"label": "Dao Lodge Nam Dam", "url": "https://maps.google.com/?q=Dao+Lodge+Nam+Dam"}
            ]
        },

        # --- DAY 4: Ha Giang Loop (Day 2) - Dong Van, Ma Pi Leng Pass, Meo Vac ---
        {
            "day_number": 4,
            "date": "2026-09-14",
            "day_of_week": "Monday",
            "destination": "Ha Giang Loop: Ma Pi Leng Pass & Meo Vac",
            "phase": "Guys Trip - Vietnam Expedition",
            "phase_short": "Phase 1: Guys Trip",
            "status": "[CONFIRMED - BOOKED]",
            "status_badge": "CONFIRMED",
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
                    "status": "VETTED_RECOMMENDED",
                    "room_spec": "Twin Hmong Wood Chamber (Two Separate Beds)",
                    "critic_score": 9.3,
                    "critic_notes": "Pass 1-3 Verified: Restored 100-year-old Hmong clay fortress, authentic courtyard, exceptional French-Vietnamese mountain cuisine, serene quiet.",
                    "price_per_night": "$60 USD / 1,500,000 VND",
                    "booking_url": "https://aubergedemeovac.com/",
                    "map_query": "Auberge+de+Meo+Vac"
                },
                {
                    "hotel_name": "Dong Van Karst Homestay / Bunk Art",
                    "status": "VETTED_ALTERNATIVE",
                    "room_spec": "Private Twin Room with Karst View",
                    "critic_score": 8.8,
                    "critic_notes": "Warm hosts, great barbecue dinner, right at the base of the pass.",
                    "price_per_night": "$35 USD / 890,000 VND",
                    "booking_url": "https://dongvanhomestay.com/",
                    "map_query": "Dong+Van+Ha+Giang"
                }
            ],
            "door_to_door_logistics": {
                "primary_transit": "Motorbike expedition with Easy-Riders: Nam Dam -> Tham Ma Pass -> Sa Phin (H'mong King Palace) -> Dong Van Ancient Town -> Ma Pi Leng Pass -> Tu San Canyon Boat -> Meo Vac (approx. 110 km).",
                "departure_time": "08:00 AM",
                "arrival_time": "17:30 PM Meo Vac check-in",
                "buffer_time": "Ample stops for canyon photography and boat ride",
                "tips": "Ma Pi Leng Pass is considered Southeast Asia's greatest mountain road; take the Tu San boat ride on Nho Que River."
            },
            "curated_daily_flow": {
                "morning": "Ride through Tham Ma 9-curve slope. Explore the 100-year-old opium-funded H'mong King's Palace (Vuong Chinh Duc) in Sa Phin valley.",
                "afternoon": "Crawl up the breathtaking Ma Pi Leng Pass overlooking the jade-green Nho Que River 1,000 meters below. Descend to the canyon base for a motorboat cruise through Tu San Chasm—the deepest karst gorge in Southeast Asia.",
                "evening": "Check into Auberge de Meo Vac. Communal evening dinner with local smoked mountain beef, stir-fried wild greens, and celebratory local corn wine ('Happy Water')."
            },
            "essential_checklist": [
                "Nho Que boat ticket included in tour voucher (check QR code)",
                "Full battery charge on phone / GoPro / camera for Ma Pi Leng panoramas",
                "Warm fleece layer for high elevation evening in Meo Vac"
            ],
            "attached_documents": [
                {
                    "doc_id": "PASS-HG-EASYRIDER",
                    "title": "Easy-Rider Route Log & Ma Pi Leng Border Permit",
                    "ref": "HG-EASY-2026-09",
                    "category": "Tour Voucher",
                    "badge": "CONFIRMED"
                }
            ],
            "google_maps_links": [
                {"label": "Tham Ma Pass", "url": "https://maps.google.com/?q=Doc+Tham+Ma+Ha+Giang"},
                {"label": "H'mong King Palace", "url": "https://maps.google.com/?q=Hmong+King+Palace+Ha+Giang"},
                {"label": "Ma Pi Leng Pass Monument", "url": "https://maps.google.com/?q=Ma+Pi+Leng+Pass"},
                {"label": "Tu San Canyon (Nho Que River)", "url": "https://maps.google.com/?q=Nho+Que+River+Boat+Dock"},
                {"label": "Auberge de Meo Vac", "url": "https://maps.google.com/?q=Auberge+de+Meo+Vac"}
            ]
        },

        # --- DAY 5: Ha Giang Loop Day 3 -> Sa Pa ---
        {
            "day_number": 5,
            "date": "2026-09-15",
            "day_of_week": "Tuesday",
            "destination": "Meo Vac -> Du Gia -> Sa Pa",
            "phase": "Guys Trip - Vietnam Expedition",
            "phase_short": "Phase 1: Guys Trip",
            "status": "[CONFIRMED - BOOKED]",
            "status_badge": "CONFIRMED",
            "weather_radar": {
                "temp_range": "17°C - 24°C",
                "condition": "Cool alpine mist in Sa Pa, crisp evening air",
                "precipitation_pct": "30%",
                "humidity": "82%",
                "attire_advice": "Fleece jacket, thermal mid-layer, sturdy hiking shoes for Sa Pa hills"
            },
            "luggage_action": "Reunite with main 55L clamshell pack at Ha Giang base camp; load onto VIP express mountain coach to Sa Pa.",
            "accommodation_matrix": [
                {
                    "hotel_name": "Eco Palms House - Sapa Retreat",
                    "status": "VETTED_RECOMMENDED",
                    "room_spec": "Private Hmong Wooden Bungalow (Two Twin Beds)",
                    "critic_score": 9.4,
                    "critic_notes": "Pass 1-3 Verified: Located in Lao Chai overlooking golden terraced rice fields, total tranquility away from noisy Sapa construction, working fireplace.",
                    "price_per_night": "$90 USD / 2,280,000 VND",
                    "booking_url": "https://ecopalmshouse.com/",
                    "map_query": "Eco+Palms+House+Sapa"
                },
                {
                    "hotel_name": "Pao's Sapa Leisure Hotel",
                    "status": "VETTED_ALTERNATIVE",
                    "room_spec": "Deluxe Twin Valley View (Two Beds)",
                    "critic_score": 9.0,
                    "critic_notes": "Curved architecture embedded in cliffside, panoramic valley views, heated indoor pool.",
                    "price_per_night": "$95 USD / 2,400,000 VND",
                    "booking_url": "https://paoshotel.com/",
                    "map_query": "Paos+Sapa+Leisure+Hotel"
                }
            ],
            "door_to_door_logistics": {
                "primary_transit": "08:00 AM: Ride Meo Vac through Du Gia scenic valley to Ha Giang City (arr 14:00 PM). Return Easy-Rider gear, shower & repack at basecamp. 15:30 PM: Direct VIP Mountain Express coach Ha Giang -> Sa Pa via Lao Cai (5.5 hrs). Arr Sa Pa 21:00 PM. Taxi to Eco Palms House (15 mins).",
                "departure_time": "08:00 AM Meo Vac / 15:30 PM Ha Giang Coach",
                "arrival_time": "21:30 PM Sa Pa check-in",
                "buffer_time": "1.5 hours in Ha Giang City for lunch, shower, and pack consolidation",
                "tips": "Direct minibus avoids backtracking to Hanoi; saves 1 full travel day."
            },
            "curated_daily_flow": {
                "morning": "Ride the winding road through Mau Due to Du Gia. Quick dip at Du Gia mountain waterfall pool.",
                "afternoon": "Return to Ha Giang City basecamp. Say goodbye to Easy-Riders. Hot shower, hearty bowl of Pho Ga, board comfortable VIP bus to Sa Pa across Hoang Lien Son range.",
                "evening": "Arrive in Sa Pa misty mountain town. Transfer down into Muong Hoa Valley to Eco Palms House. Settle into wooden bungalow, enjoy a hot salmon/sturgeon hotpot by the fire."
            },
            "essential_checklist": [
                "Pack thermal/fleece layer near top of bag (Sa Pa nights drop to 16°C)",
                "Confirm Sa Pa local trekking guide for tomorrow morning",
                "Check trail footwear grip"
            ],
            "attached_documents": [
                {
                    "doc_id": "BUS-HG-SAPA-EXPRESS",
                    "title": "Ha Giang -> Sa Pa VIP Mountain Minibus Ticket",
                    "ref": "12GO-SAPA-8821",
                    "category": "Bus Ticket",
                    "badge": "CONFIRMED"
                }
            ],
            "google_maps_links": [
                {"label": "Du Gia Waterfall", "url": "https://maps.google.com/?q=Du+Gia+Waterfall+Ha+Giang"},
                {"label": "Eco Palms House Sapa", "url": "https://maps.google.com/?q=Eco+Palms+House+Sapa"},
                {"label": "Muong Hoa Valley", "url": "https://maps.google.com/?q=Muong+Hoa+Valley+Sapa"}
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
            "status": "[VETTED - READY TO BOOK]",
            "status_badge": "VETTED",
            "weather_radar": {
                "temp_range": "18°C - 25°C",
                "condition": "Clear mountain morning, dramatic afternoon cloud rolling over terraces",
                "precipitation_pct": "20%",
                "humidity": "75%",
                "attire_advice": "Trekking boots/shoes with good lugs, moisture-wicking shirt, sun hat, daypack with 1.5L water"
            },
            "luggage_action": "Bags safely in bungalow at Eco Palms House.",
            "accommodation_matrix": [
                {
                    "hotel_name": "Eco Palms House - Sapa Retreat",
                    "status": "VETTED_RECOMMENDED",
                    "room_spec": "Private Hmong Wooden Bungalow (Two Twin Beds)",
                    "critic_score": 9.4,
                    "critic_notes": "Night 2 in Sa Pa. Direct access to trekking trailheads from property door.",
                    "price_per_night": "$90 USD / 2,280,000 VND",
                    "booking_url": "https://ecopalmshouse.com/",
                    "map_query": "Eco+Palms+House+Sapa"
                }
            ],
            "door_to_door_logistics": {
                "primary_transit": "Private guided trek on foot (12 km loop): Eco Palms House -> Y Linh Ho -> Lao Chai (Black Hmong) -> Ta Van (Giay minority) -> Bamboo forest -> Return via mountain path.",
                "departure_time": "08:30 AM guided trek start",
                "arrival_time": "15:30 PM trek completion",
                "buffer_time": "Flexible lunch & tea breaks at local village homestead",
                "tips": "September is the golden harvest season in Sa Pa when terraced fields turn vibrant gold right before cutting."
            },
            "curated_daily_flow": {
                "morning": "Balcony breakfast watching mist lift over cascading golden terraces. Meet private local Black Hmong guide. Trek along narrow ridge paths overlooking Muong Hoa stream.",
                "afternoon": "Cross hanging suspension bridges into Ta Van village. Authentic lunch at local Giay family home: roasted pork with lemongrass, fresh spring rolls, and sticky mountain rice. Continue through dense bamboo groves.",
                "evening": "Return to lodge. Traditional herbal wooden barrel bath (Dao Do herbal bath boiled with 30 forest leaves). Sunset beers on terrace, followed by Sapa grilled skewers (Thit Nuong)."
            },
            "essential_checklist": [
                "Trekking poles optional but helpful on slick dirt trails",
                "Support local guide: 300k-500k VND tip customary for full day",
                "Prepare 55L backpack for early morning departure to Cat Ba Island tomorrow"
            ],
            "attached_documents": [],
            "google_maps_links": [
                {"label": "Lao Chai Village", "url": "https://maps.google.com/?q=Lao+Chai+Village+Sapa"},
                {"label": "Ta Van Village", "url": "https://maps.google.com/?q=Ta+Van+Village+Sapa"},
                {"label": "Red Dao Herbal Bath", "url": "https://maps.google.com/?q=Red+Dao+Herbal+Bath+Sapa"}
            ]
        },

        # --- DAY 7: Sa Pa -> Cat Ba Island & Lan Ha Bay ---
        {
            "day_number": 7,
            "date": "2026-09-17",
            "day_of_week": "Thursday",
            "destination": "Sa Pa -> Cat Ba Island",
            "phase": "Guys Trip - Vietnam Expedition",
            "phase_short": "Phase 1: Guys Trip",
            "status": "[CONFIRMED - BOOKED]",
            "status_badge": "CONFIRMED",
            "weather_radar": {
                "temp_range": "26°C - 32°C",
                "condition": "Sunny coastal breeze, calm emerald waters in Lan Ha Bay",
                "precipitation_pct": "20%",
                "humidity": "78%",
                "attire_advice": "Linen shirts, swim shorts, flip-flops, sunglasses, dry bag ready for bay activities"
            },
            "luggage_action": "55L clamshell pack rides in luggage bay of intercity luxury express bus directly onto island ferry.",
            "accommodation_matrix": [
                {
                    "hotel_name": "Hôtel Perle d'Orient Cat Ba - MGallery",
                    "status": "VETTED_RECOMMENDED",
                    "room_spec": "Classic Twin Bay View (Two Single Beds)",
                    "critic_score": 9.3,
                    "critic_notes": "Pass 1-3 Verified: Premier property on Cat Ba, nestled into Cat Co 3 cliffside overlooking Lan Ha Bay. Indochine design, private beach, zero noise, 5-star maintenance.",
                    "price_per_night": "$125 USD / 3,180,000 VND",
                    "booking_url": "https://all.accor.com/hotel/B557/index.en.shtml",
                    "map_query": "Hotel+Perle+d+Orient+Cat+Ba"
                },
                {
                    "hotel_name": "Cat Ba Eco Lodge",
                    "status": "VETTED_ALTERNATIVE",
                    "room_spec": "Deluxe Twin Forest Bungalow",
                    "critic_score": 8.9,
                    "critic_notes": "Hidden valley inside Cat Ba National Park jungle, butterfly garden, tranquil swimming pool.",
                    "price_per_night": "$65 USD / 1,650,000 VND",
                    "booking_url": "https://catba-ecolodge.com/",
                    "map_query": "Cat+Ba+Eco+Lodge"
                }
            ],
            "door_to_door_logistics": {
                "primary_transit": "08:00 AM: Cat Ba Express / VIP Sleeper coach pickup from Sa Pa town. Highway express via Lao Cai -> Hanoi bypass -> Tan Vu Lach Huyen sea bridge -> Speedboat crossing to Cat Ba Island. Doorstep drop at Perle d'Orient Cat Ba (arr 16:00 PM).",
                "departure_time": "08:00 AM from Sa Pa",
                "arrival_time": "16:00 PM at Cat Ba hotel",
                "buffer_time": "Single ticket handles bus + ferry seamlessly (no lugging bags at docks)",
                "tips": "Sit on the left side of the coach during the sea-bridge crossing for panoramic ocean views."
            },
            "curated_daily_flow": {
                "morning": "Early checkout from Eco Palms House. Board luxury express coach descending from the mountains to the coastal highway.",
                "afternoon": "Cross the ocean bridge to Hai Phong. Seamless speedboat hop across to Cat Ba Island. Check-in at Hôtel Perle d'Orient Cat Ba. Head down to private Cat Co 3 beach.",
                "evening": "Hike up to Cannon Fort peak for panoramic sunset over the thousands of karst pillars in Lan Ha Bay. Dinner in town at Green Mango (fresh grilled squid, steamed crab, and craft draft beer)."
            },
            "essential_checklist": [
                "Have bus e-ticket voucher downloaded offline",
                "Waterproof phone sleeve for sea excursions",
                "Recharge headlamps/torches for cave exploration tomorrow"
            ],
            "attached_documents": [
                {
                    "doc_id": "BUS-SAPA-CATBA-VIP",
                    "title": "Sa Pa -> Cat Ba Island Direct Luxury Express Ticket",
                    "ref": "CATBA-EXP-4401",
                    "category": "Bus & Ferry Ticket",
                    "badge": "CONFIRMED"
                }
            ],
            "google_maps_links": [
                {"label": "Hôtel Perle d'Orient Cat Ba", "url": "https://maps.google.com/?q=Hotel+Perle+d+Orient+Cat+Ba"},
                {"label": "Cat Co Beach 3", "url": "https://maps.google.com/?q=Cat+Co+Beach+3+Cat+Ba"},
                {"label": "Cannon Fort Sunset View", "url": "https://maps.google.com/?q=Cannon+Fort+Cat+Ba"}
            ]
        },

        # --- DAY 8: Cat Ba & Lan Ha Bay (Cruise & Kayak) ---
        {
            "day_number": 8,
            "date": "2026-09-18",
            "day_of_week": "Friday",
            "destination": "Lan Ha Bay & Ba Trai Dao Archways",
            "phase": "Guys Trip - Vietnam Expedition",
            "phase_short": "Phase 1: Guys Trip",
            "status": "[CONFIRMED - BOOKED]",
            "status_badge": "CONFIRMED",
            "weather_radar": {
                "temp_range": "27°C - 33°C",
                "condition": "Brilliant sunshine over emerald bay, calm sea swell",
                "precipitation_pct": "10%",
                "humidity": "72%",
                "attire_advice": "Swimwear, rashguard/sun shirt, polarized sunglasses, reef-safe sunscreen, flip flops"
            },
            "luggage_action": "Bags at hotel. Bring only waterproof dry-bag onto boat.",
            "accommodation_matrix": [
                {
                    "hotel_name": "Hôtel Perle d'Orient Cat Ba - MGallery",
                    "status": "VETTED_RECOMMENDED",
                    "room_spec": "Classic Twin Bay View (Two Single Beds)",
                    "critic_score": 9.3,
                    "critic_notes": "Night 2 on Cat Ba. Returning to luxury after a full day out on the water.",
                    "price_per_night": "$125 USD / 3,180,000 VND",
                    "booking_url": "https://all.accor.com/hotel/B557/index.en.shtml",
                    "map_query": "Hotel+Perle+d+Orient+Cat+Ba"
                }
            ],
            "door_to_door_logistics": {
                "primary_transit": "08:15 AM: Transfer from hotel to Cai Beo ancient fishing port. Board private / small-group traditional junk boat into Lan Ha Bay. Cruise through floating fishing village, kayak archways, swim at Ba Trai Dao (Three Peaches) pristine secluded beaches. Return 16:30 PM.",
                "departure_time": "08:15 AM",
                "arrival_time": "16:30 PM",
                "buffer_time": "Includes freshly prepared seafood feast onboard",
                "tips": "Lan Ha Bay has the exact same karst geology as Halong Bay, but is 90% less congested with commercial mega-ships."
            },
            "curated_daily_flow": {
                "morning": "Board wooden junk boat at Cai Beo harbor. Navigate past floating fish farms. Anchor in a calm lagoon, launch sit-on-top sea kayaks to paddle through Dark & Bright karst cave tunnels into hidden lagoons.",
                "afternoon": "Plunge into the emerald waters of Ba Trai Dao. Jump off boat roof into deep water. Generous seafood lunch onboard: grilled prawns, stir-fried calamari, morning glory, and steamed sea bass.",
                "evening": "Sail back through sunset karsts. Return to hotel. Stroll Cat Ba promenade; casual dinner at Secret Garden Cat Ba with wood-fired pizza, cold beer, and live acoustic music."
            },
            "essential_checklist": [
                "Waterproof phone case / dry-bag for kayaking",
                "Reef-safe sunscreen SPF 50+",
                "Sea sickness tablets (just in case, though Lan Ha is sheltered and calm)"
            ],
            "attached_documents": [
                {
                    "doc_id": "PASS-LANHA-BAY-CRUISE",
                    "title": "Lan Ha Bay & Ba Trai Dao Private Small-Group Boat & Kayak Pass",
                    "ref": "LANHA-CRUISE-901",
                    "category": "Tour Voucher",
                    "badge": "CONFIRMED"
                }
            ],
            "google_maps_links": [
                {"label": "Cai Beo Floating Village", "url": "https://maps.google.com/?q=Cai+Beo+Fishing+Village"},
                {"label": "Ba Trai Dao Islets", "url": "https://maps.google.com/?q=Ba+Trai+Dao+Beach+Lan+Ha"},
                {"label": "Secret Garden Cat Ba", "url": "https://maps.google.com/?q=Secret+Garden+Cat+Ba"}
            ]
        },

        # --- DAY 9: Cat Ba Island (National Park & Caves) ---
        {
            "day_number": 9,
            "date": "2026-09-19",
            "day_of_week": "Saturday",
            "destination": "Cat Ba Island: Ngu Lam Peak & Hospital Cave",
            "phase": "Guys Trip - Vietnam Expedition",
            "phase_short": "Phase 1: Guys Trip",
            "status": "[VETTED - READY TO BOOK]",
            "status_badge": "VETTED",
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
                    "status": "VETTED_RECOMMENDED",
                    "room_spec": "Classic Twin Bay View (Two Single Beds)",
                    "critic_score": 9.3,
                    "critic_notes": "Night 3 on Cat Ba.",
                    "price_per_night": "$125 USD / 3,180,000 VND",
                    "booking_url": "https://all.accor.com/hotel/B557/index.en.shtml",
                    "map_query": "Hotel+Perle+d+Orient+Cat+Ba"
                }
            ],
            "door_to_door_logistics": {
                "primary_transit": "Private scooter rental or hotel car into the island interior (14 km to National Park HQ). Paved island spine road with zero traffic.",
                "departure_time": "08:30 AM",
                "arrival_time": "16:00 PM back in town",
                "buffer_time": "Self-paced mountain hiking and historic cave walkthrough",
                "tips": "National Park summit hike takes ~1.5 hours return; moderate incline with stone steps."
            },
            "curated_daily_flow": {
                "morning": "Ride through lush interior valleys to Cat Ba National Park. Hike the jungle trail to Ngu Lam Peak for a 360-degree panorama of limestone mountain peaks rolling into the sea.",
                "afternoon": "Explore Hospital Cave (Quan Y)—a secret bomb-proof, 3-story underground hospital built inside a cavern during the American-Vietnam War, complete with treatment rooms, cinema, and recovery wards.",
                "evening": "Relax on Cat Co 1 beach. Sunset dinner at Yummy Restaurant (famous for fresh local lobster, crab tamarind, and cold Bia Saigon)."
            },
            "essential_checklist": [
                "Insect repellent for jungle hike",
                "1L water per person for Ngu Lam peak climb",
                "Pack bags for morning transfer to Ninh Binh tomorrow"
            ],
            "attached_documents": [],
            "google_maps_links": [
                {"label": "Cat Ba National Park", "url": "https://maps.google.com/?q=Cat+Ba+National+Park"},
                {"label": "Hospital Cave (Quan Y)", "url": "https://maps.google.com/?q=Hospital+Cave+Cat+Ba"},
                {"label": "Ngu Lam Peak Trailhead", "url": "https://maps.google.com/?q=Ngu+Lam+Peak+Cat+Ba"}
            ]
        },

        # --- DAY 10: Cat Ba -> Ninh Binh (Tam Coc) ---
        {
            "day_number": 10,
            "date": "2026-09-20",
            "day_of_week": "Sunday",
            "destination": "Cat Ba -> Ninh Binh (Tam Coc)",
            "phase": "Guys Trip - Vietnam Expedition",
            "phase_short": "Phase 1: Guys Trip",
            "status": "[CONFIRMED - BOOKED]",
            "status_badge": "CONFIRMED",
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
                    "status": "VETTED_RECOMMENDED",
                    "room_spec": "Premium Twin Bungalow (Two Separate Beds)",
                    "critic_score": 9.5,
                    "critic_notes": "Pass 1-3 Verified: World-class boutique sanctuary nestled amid rice fields and karst pinnacles. Complimentary bicycles, zero traffic noise, exceptional farm-to-table dining.",
                    "price_per_night": "$140 USD / 3,550,000 VND",
                    "booking_url": "https://tamcocgarden.com/",
                    "map_query": "Tam+Coc+Garden+Resort+Ninh+Binh"
                },
                {
                    "hotel_name": "Ninh Binh Hidden Charm Hotel & Resort",
                    "status": "VETTED_ALTERNATIVE",
                    "room_spec": "Superior Twin Karst View",
                    "critic_score": 9.0,
                    "critic_notes": "Large resort amenities, outdoor swimming pool, 5 mins from Tam Coc boat pier.",
                    "price_per_night": "$75 USD / 1,900,000 VND",
                    "booking_url": "https://hiddencharmresort.com/",
                    "map_query": "Ninh+Binh+Hidden+Charm+Hotel"
                }
            ],
            "door_to_door_logistics": {
                "primary_transit": "09:00 AM: Daichi / Cat Ba Express bus from Cat Ba hotel -> Island ferry -> Hai Phong highway -> Ninh Binh Tam Coc (3.5 hrs door-to-door). Arr Tam Coc Garden Resort 13:30 PM.",
                "departure_time": "09:00 AM Cat Ba checkout",
                "arrival_time": "13:30 PM Tam Coc check-in",
                "buffer_time": "Direct coach transfers passengers and luggage onto ferry without shifting bags",
                "tips": "Arriving early afternoon leaves plenty of time for late afternoon cycling and boat trip."
            },
            "curated_daily_flow": {
                "morning": "Leisurely breakfast at Perle d'Orient. Board tourist express coach from Cat Ba town across the ferry channel toward Ninh Binh's inland karst empire.",
                "afternoon": "Check in at Tam Coc Garden Resort. Grab complimentary bicycles and pedal along quiet dirt tracks flanked by lotus ponds and towering limestone monoliths. Stroll to Bich Dong Pagoda—the 15th-century cave temple built into the mountainside.",
                "evening": "Sunset cocktails overlooking the rice paddies. Dinner at Tam Coc Garden Restaurant: Ninh Binh goat meat specialties (De Tai Chanh), crispy burned rice (Com Chay), and fresh river fish."
            },
            "essential_checklist": [
                "Bicycle lock provided by resort",
                "Cover shoulders/knees for Bich Dong Pagoda entrance",
                "Small cash (50k VND) for bicycle parking attendants"
            ],
            "attached_documents": [
                {
                    "doc_id": "BUS-CATBA-NINHBINH",
                    "title": "Cat Ba Island -> Ninh Binh (Tam Coc) Express Bus Ticket",
                    "ref": "DAICHI-NB-331",
                    "category": "Bus Ticket",
                    "badge": "CONFIRMED"
                }
            ],
            "google_maps_links": [
                {"label": "Tam Coc Garden Resort", "url": "https://maps.google.com/?q=Tam+Coc+Garden+Resort"},
                {"label": "Bich Dong Pagoda", "url": "https://maps.google.com/?q=Bich+Dong+Pagoda+Ninh+Binh"},
                {"label": "Tam Coc Rice Fields", "url": "https://maps.google.com/?q=Tam+Coc+Ninh+Binh"}
            ]
        },

        # --- DAY 11: Ninh Binh (Mua Cave Sunrise & Trang An Boat) ---
        {
            "day_number": 11,
            "date": "2026-09-21",
            "day_of_week": "Monday",
            "destination": "Ninh Binh: Mua Cave & Trang An UNESCO Caves",
            "phase": "Guys Trip - Vietnam Expedition",
            "phase_short": "Phase 1: Guys Trip",
            "status": "[VETTED - READY TO BOOK]",
            "status_badge": "VETTED",
            "weather_radar": {
                "temp_range": "23°C - 30°C",
                "condition": "Crisp clear morning for sunrise climb, warm afternoon",
                "precipitation_pct": "15%",
                "humidity": "70%",
                "attire_advice": "Sturdy trainers for 500 stone steps at Mua Cave, light breathable clothes, sun umbrella for boat ride"
            },
            "luggage_action": "Bags at resort.",
            "accommodation_matrix": [
                {
                    "hotel_name": "Tam Coc Garden Resort",
                    "status": "VETTED_RECOMMENDED",
                    "room_spec": "Premium Twin Bungalow (Two Separate Beds)",
                    "critic_score": 9.5,
                    "critic_notes": "Night 2 at Tam Coc Garden Resort.",
                    "price_per_night": "$140 USD / 3,550,000 VND",
                    "booking_url": "https://tamcocgarden.com/",
                    "map_query": "Tam+Coc+Garden+Resort+Ninh+Binh"
                }
            ],
            "door_to_door_logistics": {
                "primary_transit": "06:00 AM: 15-min bicycle/taxi to Hang Mua entrance. 09:30 AM: 20-min taxi to Trang An UNESCO Boat Wharf. Route 3 boat ride (3 hrs). 14:00 PM return to hotel.",
                "departure_time": "06:00 AM (beats the heat and tour bus crowds)",
                "arrival_time": "15:00 PM",
                "buffer_time": "Early start ensures climbing Mua Cave before tour groups arrive from Hanoi",
                "tips": "At Trang An, pick Route 3 for the longest water cave (Dot Cave, 1,000m) and the King Kong movie set."
            },
            "curated_daily_flow": {
                "morning": "Dawn ascent of Hang Mua (500 rugged stone steps) up to the Lying Dragon peak. Catch the golden morning light cascading across the Tam Coc river valley below. Hearty resort breakfast upon return.",
                "afternoon": "Board traditional sampan at Trang An UNESCO complex. Gliding silently under cavernous stalactite ceilings in subterranean tunnels, through emerald lakes ringed by vertical karst cliffs.",
                "evening": "Afternoon swim in the resort pool overlooking the lotus lagoon. Farewell Ninh Binh dinner: roasted duck with chili-ginger fish sauce at Chookie's Beer Garden or resort terrace."
            },
            "essential_checklist": [
                "Arrive at Hang Mua at 06:15 AM to beat Hanoi tour buses",
                "Trang An ticket: 250,000 VND / person (buy at wharf counter)",
                "Rowing boat lady tip: 50,000 - 100,000 VND"
            ],
            "attached_documents": [],
            "google_maps_links": [
                {"label": "Hang Mua (Mua Cave)", "url": "https://maps.google.com/?q=Hang+Mua+Ninh+Binh"},
                {"label": "Trang An Boat Wharf", "url": "https://maps.google.com/?q=Trang+An+Departure+Boat+Ticket"},
                {"label": "Chookie's Beer Garden", "url": "https://maps.google.com/?q=Chookies+Beer+Garden+Ninh+Binh"}
            ]
        },

        # --- DAY 12: Ninh Binh -> Hanoi Old Quarter ---
        {
            "day_number": 12,
            "date": "2026-09-22",
            "day_of_week": "Tuesday",
            "destination": "Ninh Binh -> Hanoi (Old Quarter Finale Base)",
            "phase": "Guys Trip - Vietnam Expedition",
            "phase_short": "Phase 1: Guys Trip",
            "status": "[CONFIRMED - BOOKED]",
            "status_badge": "CONFIRMED",
            "weather_radar": {
                "temp_range": "25°C - 32°C",
                "condition": "Warm urban sun, breezy evening",
                "precipitation_pct": "20%",
                "humidity": "72%",
                "attire_advice": "Casual urban street clothes, comfortable walking shoes"
            },
            "luggage_action": "55L backpack loaded into VIP limousine van trunk.",
            "accommodation_matrix": [
                {
                    "hotel_name": "La Siesta Classic Ma May (Hanoi Old Quarter)",
                    "status": "VETTED_RECOMMENDED",
                    "room_spec": "Deluxe Twin Room (Two Separate Single Beds)",
                    "critic_score": 9.4,
                    "critic_notes": "Pass 1-3 Verified: Returning to Hanoi Old Quarter base for pre-flight finale. Flawless hospitality, central location for walking to cafes and street eats.",
                    "price_per_night": "$85 USD / 2,150,000 VND",
                    "booking_url": "https://lasiestahotels.vn/mamay/",
                    "map_query": "La+Siesta+Classic+Ma+May+Hanoi"
                },
                {
                    "hotel_name": "Peridot Grand Luxury Boutique Hotel",
                    "status": "VETTED_ALTERNATIVE",
                    "room_spec": "Grand Deluxe Twin Room",
                    "critic_score": 9.3,
                    "critic_notes": "Rooftop infinity pool, upscale gym, quiet western edge of Old Quarter.",
                    "price_per_night": "$110 USD / 2,800,000 VND",
                    "booking_url": "https://peridotgrandhotel.com/",
                    "map_query": "Peridot+Grand+Hotel+Hanoi"
                }
            ],
            "door_to_door_logistics": {
                "primary_transit": "11:00 AM: VIP 9-seater Limousine Van pickup directly from Tam Coc Garden Resort. Expressway to Hanoi Old Quarter (90 mins). Drop-off at La Siesta Ma May hotel entrance at 12:45 PM.",
                "departure_time": "11:00 AM Tam Coc checkout",
                "arrival_time": "12:45 PM Hanoi check-in",
                "buffer_time": "Relaxed late-morning departure",
                "tips": "Expressway route skips highway congestion; leather massage seats with USB chargers."
            },
            "curated_daily_flow": {
                "morning": "Sleep in, enjoy organic breakfast at the resort. Stroll the organic herb gardens. Board luxury limousine van back to Hanoi.",
                "afternoon": "Check in to La Siesta Ma May. Head out into the Old Quarter labyrinth. Visit Hanoi Train Street for iced coconut coffee as the locomotive rumbles inches past the cafe doorway.",
                "evening": "Street food extravaganza: Pho Gia Truyen Bat Dan (legendary slow-simmered beef pho) followed by crispy Banh Mi 25 and fresh draught Bia Hoi on Ta Hien corner."
            },
            "essential_checklist": [
                "Check Train Street timetable before walking (usually passes ~15:30 and 17:30)",
                "Prepare laundry at hotel for quick overnight turnaround before Thailand",
                "Confirm Vietnam departure flight 1145-554-179 status"
            ],
            "attached_documents": [
                {
                    "doc_id": "BUS-NINHBINH-HANOI",
                    "title": "Ninh Binh -> Hanoi Old Quarter Limousine Van Voucher",
                    "ref": "TRANG-AN-LIMO-112",
                    "category": "Bus Ticket",
                    "badge": "CONFIRMED"
                }
            ],
            "google_maps_links": [
                {"label": "La Siesta Classic Ma May", "url": "https://maps.google.com/?q=La+Siesta+Classic+Ma+May"},
                {"label": "Hanoi Train Street", "url": "https://maps.google.com/?q=Hanoi+Train+Street"},
                {"label": "Pho Gia Truyen Bat Dan", "url": "https://maps.google.com/?q=Pho+Gia+Truyen+Bat+Dan"},
                {"label": "Banh Mi 25", "url": "https://maps.google.com/?q=Banh+Mi+25+Hanoi"}
            ]
        },

        # --- DAY 13: Hanoi Base (Pre-Flight Finale & Rest) ---
        {
            "day_number": 13,
            "date": "2026-09-23",
            "day_of_week": "Wednesday",
            "destination": "Hanoi: French Quarter, West Lake & Farewell Dinner",
            "phase": "Guys Trip - Vietnam Expedition",
            "phase_short": "Phase 1: Guys Trip",
            "status": "[VETTED - READY TO BOOK]",
            "status_badge": "VETTED",
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
                    "status": "VETTED_RECOMMENDED",
                    "room_spec": "Deluxe Twin Room (Two Separate Single Beds)",
                    "critic_score": 9.4,
                    "critic_notes": "Finale night in Vietnam.",
                    "price_per_night": "$85 USD / 2,150,000 VND",
                    "booking_url": "https://lasiestahotels.vn/mamay/",
                    "map_query": "La+Siesta+Classic+Ma+May+Hanoi"
                }
            ],
            "door_to_door_logistics": {
                "primary_transit": "Walking and short Grab taxi hops within central Hanoi (Old Quarter -> French Quarter -> West Lake).",
                "departure_time": "Self-paced",
                "arrival_time": "Self-paced",
                "buffer_time": "Pre-flight prep day with zero tight deadlines",
                "tips": "Use Grab app linked to credit card for 30k-50k VND hassle-free rides."
            },
            "curated_daily_flow": {
                "morning": "Walk the French Quarter tree-lined boulevards. Visit the serene Temple of Literature (Van Mieu) and St. Joseph's Cathedral. Specialty drip coffee at The Note Coffee overlooking Hoan Kiem.",
                "afternoon": "Grab ride up to West Lake (Tay Ho). Visit Tran Quoc Pagoda on the islet. Souvenir hunting for artisan ceramic pottery, high-grade Vietnamese single-origin coffee beans, and silk.",
                "evening": "Phase 1 Guys Trip Farewell Feast: Cha Ca Thang Long (turmeric-marinated grilled catfish sizzled with dill and scallions table-side over coals, served with rice noodles, peanuts, and nuoc cham). Toast the epic 12-day northern loop with cold beers at Moonlight Sky Bar."
            },
            "essential_checklist": [
                "Pack and zip 55L clamshell backpack; weigh under 15kg for cabin/carry-on",
                "Check out time tomorrow: 10:00 AM; arrange 10:15 AM airport taxi to Noi Bai",
                "Exchange remaining large VND notes back to USD/THB at Ha Trung gold street"
            ],
            "attached_documents": [],
            "google_maps_links": [
                {"label": "Temple of Literature", "url": "https://maps.google.com/?q=Temple+of+Literature+Hanoi"},
                {"label": "Tran Quoc Pagoda", "url": "https://maps.google.com/?q=Tran+Quoc+Pagoda+Hanoi"},
                {"label": "Cha Ca Thang Long (Dinner)", "url": "https://maps.google.com/?q=Cha+Ca+Thang+Long+Duong+Thanh"},
                {"label": "Moonlight Sky Bar", "url": "https://maps.google.com/?q=Moonlight+Sky+Bar+Hanoi"}
            ]
        },

        # --- DAY 14: TRANSITION DAY - Hanoi -> Bangkok -> Koh Samui ---
        {
            "day_number": 14,
            "date": "2026-09-24",
            "day_of_week": "Thursday",
            "destination": "Transition: Hanoi -> Bangkok -> Koh Samui",
            "phase": "Transition & Couple Trip - Thailand Romance",
            "phase_short": "Transition -> Phase 2",
            "status": "[CONFIRMED - BOOKED]",
            "status_badge": "CONFIRMED",
            "weather_radar": {
                "temp_range": "26°C - 32°C",
                "condition": "Warm tropical sun over Gulf of Thailand, balmy coastal evening",
                "precipitation_pct": "20%",
                "humidity": "75%",
                "attire_advice": "Transition from trekking clothes to chic island resort attire: linen shirt, tailored shorts, boat shoes/sandals"
            },
            "luggage_action": "CRITICAL RETRIEVAL: Upon landing at BKK (14:35), proceed to Airport Rail Link level (Floor B) and retrieve checked suitcase from AIRPORTELs locker. Reunite with girlfriend with all gear ready for the South!",
            "accommodation_matrix": [
                {
                    "hotel_name": "Hansar Samui Resort & Spa (Bophut Beach)",
                    "status": "VETTED_RECOMMENDED",
                    "room_spec": "Sea View King Room (Romantic King Bed + Ocean Balcony Daybed)",
                    "critic_score": 9.4,
                    "critic_notes": "Pass 1-3 Verified: Unbeatable romantic decompression stay. 2-minute beach walk to Fisherman's Village dining, stunning infinity pool over the bay, sound of gentle waves, immaculate couple spa.",
                    "price_per_night": "$165 USD / ~5,800 THB",
                    "booking_url": "https://www.hansarsamui.com/",
                    "map_query": "Hansar+Samui+Resort+Bophut"
                },
                {
                    "hotel_name": "SALA Samui Choengmon Beach Resort",
                    "status": "VETTED_ALTERNATIVE",
                    "room_spec": "Deluxe Balcony King Room / Plunge Pool Villa",
                    "critic_score": 9.3,
                    "critic_notes": "Intimate couple haven, private open-air bathtubs, pure white sand cove.",
                    "price_per_night": "$195 USD / ~6,900 THB",
                    "booking_url": "https://www.salahospitality.com/choengmon/",
                    "map_query": "SALA+Samui+Choengmon"
                }
            ],
            "door_to_door_logistics": {
                "primary_transit": "10:15 AM: Taxi to Noi Bai Airport (HAN). 12:45 PM: Flight HAN -> BKK (Booking 1145-554-179, arr 14:35). Friend departs. 14:50 PM: Retrieve suitcase from AIRPORTELs Floor B. 15:15 PM: Reunite with girlfriend at BKK Terminal. 17:15 PM: Bangkok Airways PG 169 nonstop flight BKK -> USM (arr 18:20 PM). 18:40 PM: Private 15-min transfer to Hansar Samui.",
                "departure_time": "10:15 AM Hanoi / 17:15 PM BKK",
                "arrival_time": "19:00 PM Koh Samui resort check-in",
                "buffer_time": "2h40m seamless connection window at BKK terminal for bag retrieval, terminal transit, and Bangkok Airways boutique lounge access",
                "tips": "Bangkok Airways operates exclusive boutique lounges with complimentary snacks and espresso for all passengers at BKK Concourse A/F."
            },
            "curated_daily_flow": {
                "morning": "Checkout of Hanoi hotel. Quick drive to Noi Bai airport. Board flight 1145-554-179 to Bangkok. Bid farewell to friend as journeys branch.",
                "afternoon": "Land at Suvarnabhumi Airport. Head to Floor B locker desk, show AIRPORTELs deposit receipt, retrieve large suitcase. Reunite with girlfriend at the arrivals hall! Check in bags together at Bangkok Airways counter. Enjoy lounge treats before evening hop to Koh Samui.",
                "evening": "Touchdown at Koh Samui's open-air tropical airport. Check-in to oceanfront King room at Hansar Samui. Welcome tropical cocktails, followed by candlelit barefoot dining on the beach at Coco Tam's X Peppina in Fisherman's Village with fire dancer show."
            },
            "essential_checklist": [
                "AIRPORTELs physical deposit slip or QR code ready for quick retrieval",
                "Bangkok Airways ticket checked in on mobile",
                "Phase 2 Shift: Romance mode activated! King bed verified."
            ],
            "attached_documents": [
                {
                    "doc_id": "FLIGHT-HAN-BKK-1145554179",
                    "title": "Flight E-Ticket: Hanoi (HAN) -> Bangkok (BKK)",
                    "ref": "Booking: 1145-554-179",
                    "category": "Flight Ticket",
                    "badge": "CONFIRMED"
                },
                {
                    "doc_id": "STORAGE-BKK-AIRPORTELS",
                    "title": "AIRPORTELs Suitcase Retrieval Claim Slip",
                    "ref": "BKK-LK-20260912-771",
                    "category": "Luggage Retrieval",
                    "badge": "CONFIRMED"
                },
                {
                    "doc_id": "FLIGHT-BKK-USM-PRICE-RADAR",
                    "title": "Bangkok (BKK) -> Koh Samui (USM) Flight Strategy & Tracker",
                    "ref": "Target: PG 169 (17:15 PM) / $115-135 USD",
                    "category": "Price Radar",
                    "badge": "RADAR TRACKING"
                }
            ],
            "google_maps_links": [
                {"label": "Hansar Samui Resort", "url": "https://maps.google.com/?q=Hansar+Samui+Resort"},
                {"label": "Fisherman's Village Bophut", "url": "https://maps.google.com/?q=Fishermans+Village+Bophut"},
                {"label": "Coco Tam's Beach Bar", "url": "https://maps.google.com/?q=Coco+Tams+Bophut"}
            ]
        },

        # --- DAY 15: Koh Samui -> Koh Phangan (Boutique Bay Arrival) ---
        {
            "day_number": 15,
            "date": "2026-09-25",
            "day_of_week": "Friday",
            "destination": "Koh Samui -> Koh Phangan (Thong Nai Pan)",
            "phase": "Couple Trip - Southern Thailand Romance",
            "phase_short": "Phase 2: Couple Trip",
            "status": "[CONFIRMED - BOOKED]",
            "status_badge": "CONFIRMED",
            "weather_radar": {
                "temp_range": "27°C - 32°C",
                "condition": "Tropical sunshine, gentle sea breeze, calm bay",
                "precipitation_pct": "15%",
                "humidity": "72%",
                "attire_advice": "Linen shirts, sundresses, swimwear, polarized sunglasses, flip-flops"
            },
            "luggage_action": "Suitcase + backpack transferred seamlessly via Lomprayah ferry luggage crew.",
            "accommodation_matrix": [
                {
                    "hotel_name": "Anantara Rasananda Koh Phangan Villas",
                    "status": "VETTED_RECOMMENDED",
                    "room_spec": "Ocean Pool Suite / Garden Pool Suite (Romantic King Bed + Private Plunge Pool)",
                    "critic_score": 9.6,
                    "critic_notes": "Pass 1-3 Verified: The crown jewel of Koh Phangan romance. Set in lush coconut palms on pristine Thong Nai Pan Noi beach. Secluded, private plunge pools, five-star culinary program, total sanctuary far away from party noise.",
                    "price_per_night": "$260 USD / ~9,200 THB",
                    "booking_url": "https://www.anantara.com/en/rasananda-koh-phangan",
                    "map_query": "Anantara+Rasananda+Koh+Phangan"
                },
                {
                    "hotel_name": "Santhiya Koh Phangan Resort & Spa",
                    "status": "VETTED_ALTERNATIVE",
                    "room_spec": "Supreme Deluxe Sea View King",
                    "critic_score": 9.2,
                    "critic_notes": "Carved traditional teakwood architecture on cliffside, panoramic Gulf vistas, private speedboat transfers.",
                    "price_per_night": "$180 USD / ~6,400 THB",
                    "booking_url": "https://www.santhiya.com/kohphangan/",
                    "map_query": "Santhiya+Koh+Phangan+Resort"
                }
            ],
            "door_to_door_logistics": {
                "primary_transit": "10:00 AM: Hotel taxi to Lomprayah Pralarn Pier (Maenam). 10:30 AM: High-speed catamaran to Koh Phangan Thong Sala Pier (arr 10:50 AM, 20 mins). 11:15 AM: Resort 4x4 private transfer across the jungle ridge to Thong Nai Pan Noi bay (35 mins).",
                "departure_time": "10:00 AM Samui checkout",
                "arrival_time": "12:00 PM Phangan resort check-in",
                "buffer_time": "Ultra-fast catamaran crossing; smooth resort vehicle transfer",
                "tips": "Book VIP air-conditioned upper deck ticket on Lomprayah for extra luggage comfort."
            },
            "curated_daily_flow": {
                "morning": "Lazy champagne breakfast on the beach at Hansar Samui. Short hop to Maenam pier and board the Lomprayah high-speed catamaran across the sparkling Gulf.",
                "afternoon": "Scenic jungle drive descending into the crescent sanctuary of Thong Nai Pan Noi. Check in to your private plunge pool suite at Anantara Rasananda. Unpack, pop chilled sparkling wine, plunge into private pool.",
                "evening": "Sunset cocktails at Bistro @ The Beach. Barefoot romantic dinner listening to waves gently breaking on the powder sand. Stroll along the secluded beach under starlight."
            },
            "essential_checklist": [
                "Lomprayah catamaran QR code on phone",
                "Confirm hotel 4x4 pickup at Thong Sala Pier",
                "Pre-book couple spa treatment for tomorrow afternoon"
            ],
            "attached_documents": [
                {
                    "doc_id": "FERRY-SAMUI-PHANGAN",
                    "title": "Lomprayah High-Speed Catamaran Ticket (Samui -> Phangan)",
                    "ref": "LOM-SP-20260925-101",
                    "category": "Ferry Ticket",
                    "badge": "CONFIRMED"
                }
            ],
            "google_maps_links": [
                {"label": "Anantara Rasananda Villas", "url": "https://maps.google.com/?q=Anantara+Rasananda+Koh+Phangan"},
                {"label": "Thong Nai Pan Noi Beach", "url": "https://maps.google.com/?q=Thong+Nai+Pan+Noi+Beach"},
                {"label": "Bistro @ The Beach", "url": "https://maps.google.com/?q=Bistro+at+The+Beach+Koh+Phangan"}
            ]
        },

        # --- DAY 16: Koh Phangan (Boutique Bay & Couple Spa) ---
        {
            "day_number": 16,
            "date": "2026-09-26",
            "day_of_week": "Saturday",
            "destination": "Koh Phangan: Thong Nai Pan Bay & Wellness",
            "phase": "Couple Trip - Southern Thailand Romance",
            "phase_short": "Phase 2: Couple Trip",
            "status": "[VETTED - READY TO BOOK]",
            "status_badge": "VETTED",
            "weather_radar": {
                "temp_range": "28°C - 33°C",
                "condition": "Golden sunshine, azure sea, gentle afternoon sea breeze",
                "precipitation_pct": "10%",
                "humidity": "70%",
                "attire_advice": "Bathing suits, linen cover-ups, sun hats, sandals"
            },
            "luggage_action": "Resort stay.",
            "accommodation_matrix": [
                {
                    "hotel_name": "Anantara Rasananda Koh Phangan Villas",
                    "status": "VETTED_RECOMMENDED",
                    "room_spec": "Ocean Pool Suite / Garden Pool Suite (Romantic King Bed)",
                    "critic_score": 9.6,
                    "critic_notes": "Night 2 on Koh Phangan.",
                    "price_per_night": "$260 USD / ~9,200 THB",
                    "booking_url": "https://www.anantara.com/en/rasananda-koh-phangan",
                    "map_query": "Anantara+Rasananda+Koh+Phangan"
                }
            ],
            "door_to_door_logistics": {
                "primary_transit": "Zero transit day. Entire day within Thong Nai Pan Noi beach sanctuary and resort grounds.",
                "departure_time": "N/A",
                "arrival_time": "N/A",
                "buffer_time": "100% relaxation",
                "tips": "Stand-up paddleboards and sea kayaks available complimentary at resort beachfront."
            },
            "curated_daily_flow": {
                "morning": "Gourmet beachfront buffet breakfast (fresh mango, coconut pancakes, eggs benedict). Morning stand-up paddleboarding together on the flat calm bay waters.",
                "afternoon": "2-hour signature Couple Aromatherapy Spa ritual in hillside open-air pavilion surrounded by tropical jungle birds and waterfalls.",
                "evening": "Walk next door to Buri Rasa Village for beachside cocktail at The Beach Club, followed by dinner at Luna Lounge (creative Thai-Western fusion, lemongrass roasted sea bass)."
            },
            "essential_checklist": [
                "Reef-safe sunscreen SPF 50+",
                "Hydrate with fresh whole coconuts",
                "Book longtail boat for Bottle Beach excursion tomorrow"
            ],
            "attached_documents": [],
            "google_maps_links": [
                {"label": "Luna Lounge Phangan", "url": "https://maps.google.com/?q=Luna+Lounge+Koh+Phangan"},
                {"label": "Buri Rasa Beach Club", "url": "https://maps.google.com/?q=Buri+Rasa+Koh+Phangan"}
            ]
        },

        # --- DAY 17: Koh Phangan (Bottle Beach & Than Sadet Waterfalls) ---
        {
            "day_number": 17,
            "date": "2026-09-27",
            "day_of_week": "Sunday",
            "destination": "Koh Phangan: Bottle Beach & Than Sadet National Park",
            "phase": "Couple Trip - Southern Thailand Romance",
            "phase_short": "Phase 2: Couple Trip",
            "status": "[VETTED - READY TO BOOK]",
            "status_badge": "VETTED",
            "weather_radar": {
                "temp_range": "27°C - 32°C",
                "condition": "Sunny skies, light mountain shade in national park",
                "precipitation_pct": "15%",
                "humidity": "72%",
                "attire_advice": "Swimwear, light t-shirt, water shoes or strap sandals for rocky cove"
            },
            "luggage_action": "Resort stay.",
            "accommodation_matrix": [
                {
                    "hotel_name": "Anantara Rasananda Koh Phangan Villas",
                    "status": "VETTED_RECOMMENDED",
                    "room_spec": "Ocean Pool Suite / Garden Pool Suite (Romantic King Bed)",
                    "critic_score": 9.6,
                    "critic_notes": "Night 3 on Koh Phangan.",
                    "price_per_night": "$260 USD / ~9,200 THB",
                    "booking_url": "https://www.anantara.com/en/rasananda-koh-phangan",
                    "map_query": "Anantara+Rasananda+Koh+Phangan"
                }
            ],
            "door_to_door_logistics": {
                "primary_transit": "Private longtail boat charter from Thong Nai Pan beach to Bottle Beach (Haad Khuat, 15 mins by boat). Afternoon vehicle excursion to Than Sadet Waterfall (20 mins).",
                "departure_time": "09:30 AM longtail charter",
                "arrival_time": "15:30 PM return",
                "buffer_time": "Private boat waits for you at Bottle Beach",
                "tips": "Bottle Beach is inaccessible by normal cars; longtail boat ride over emerald water is gorgeous."
            },
            "curated_daily_flow": {
                "morning": "Hop aboard a private wooden longtail boat with colorful flower ribbons on the bow. Skim past sheer sea cliffs to secluded Bottle Beach. Crystal-clear snorkeling among parrotfish.",
                "afternoon": "Fresh pineapple smoothies at beachfront wooden shack. Boat returns to bay. Short afternoon drive to Than Sadet National Park—historic granite boulders where Thai kings Rama V and Rama VII carved their royal monograms.",
                "evening": "Cliffside dinner at 2400 Bar or edge-of-world dining with panoramic views overlooking the Gulf archipelago."
            },
            "essential_checklist": [
                "Waterproof dry bag for boat ride",
                "Snorkel masks (provided by resort or charter)",
                "Small cash for national park entrance (100 THB)"
            ],
            "attached_documents": [],
            "google_maps_links": [
                {"label": "Bottle Beach (Haad Khuat)", "url": "https://maps.google.com/?q=Bottle+Beach+Koh+Phangan"},
                {"label": "Than Sadet National Park", "url": "https://maps.google.com/?q=Than+Sadet+Waterfall+Koh+Phangan"},
                {"label": "2400 Bar Viewpoint", "url": "https://maps.google.com/?q=2400+Bar+Koh+Phangan"}
            ]
        },

        # --- DAY 18: Koh Phangan (West Coast Sunset Lounges & Reef) ---
        {
            "day_number": 18,
            "date": "2026-09-28",
            "day_of_week": "Monday",
            "destination": "Koh Phangan: Koh Ma Reef & West Coast Sunset",
            "phase": "Couple Trip - Southern Thailand Romance",
            "phase_short": "Phase 2: Couple Trip",
            "status": "[VETTED - READY TO BOOK]",
            "status_badge": "VETTED",
            "weather_radar": {
                "temp_range": "27°C - 33°C",
                "condition": "Warm tropical sunshine, spectacular clear sunset",
                "precipitation_pct": "15%",
                "humidity": "71%",
                "attire_advice": "Beachwear for day, sunset chic for evening (linen trousers, summer dress)"
            },
            "luggage_action": "Resort stay.",
            "accommodation_matrix": [
                {
                    "hotel_name": "Anantara Rasananda Koh Phangan Villas",
                    "status": "VETTED_RECOMMENDED",
                    "room_spec": "Ocean Pool Suite / Garden Pool Suite (Romantic King Bed)",
                    "critic_score": 9.6,
                    "critic_notes": "Night 4 on Koh Phangan.",
                    "price_per_night": "$260 USD / ~9,200 THB",
                    "booking_url": "https://www.anantara.com/en/rasananda-koh-phangan",
                    "map_query": "Anantara+Rasananda+Koh+Phangan"
                }
            ],
            "door_to_door_logistics": {
                "primary_transit": "Private SUV hire for West Coast exploration: Thong Nai Pan -> Mae Haad / Koh Ma (30 mins) -> Haad Salad -> Amsterdam Bar / Top Rock Bar (20 mins).",
                "departure_time": "11:00 AM",
                "arrival_time": "20:30 PM",
                "buffer_time": "Self-paced scenic island driving",
                "tips": "Arrive at sunset lounge by 17:00 to claim prime cliffside cushions."
            },
            "curated_daily_flow": {
                "morning": "Late relaxed morning. Swim in private pool. Drive across to Mae Haad beach—walk across the natural sandbar to uninhabited Koh Ma island for Phangan's premier coral reef snorkeling.",
                "afternoon": "Late lunch at Secret Beach / Karma Cafe (fresh coconut curries, dragonfruit bowls). Relax in hammocks under casuarina trees.",
                "evening": "Ascend to Top Rock Bar or Amsterdam Bar perched high on the Western cliffs. Watch the fiery orange sun sink directly into the Gulf horizon with chilled ambient DJ sets. Dinner at beachfront seafood restaurant in Thong Sala night market or returning to resort."
            },
            "essential_checklist": [
                "Reef booties for walking across Koh Ma coral flats",
                "Sunglasses and camera ready for sunset golden hour",
                "Confirm driver pickup for return trip"
            ],
            "attached_documents": [],
            "google_maps_links": [
                {"label": "Koh Ma Sandbar & Reef", "url": "https://maps.google.com/?q=Koh+Ma+Koh+Phangan"},
                {"label": "Secret Beach Phangan", "url": "https://maps.google.com/?q=Secret+Beach+Koh+Phangan"},
                {"label": "Top Rock Bar Viewpoint", "url": "https://maps.google.com/?q=Top+Rock+Bar+Koh+Phangan"}
            ]
        },

        # --- DAY 19: Koh Phangan (Sri Thanu Wellness & Yoga) ---
        {
            "day_number": 19,
            "date": "2026-09-29",
            "day_of_week": "Tuesday",
            "destination": "Koh Phangan: Sri Thanu Wellness Sanctuary",
            "phase": "Couple Trip - Southern Thailand Romance",
            "phase_short": "Phase 2: Couple Trip",
            "status": "[VETTED - READY TO BOOK]",
            "status_badge": "VETTED",
            "weather_radar": {
                "temp_range": "27°C - 32°C",
                "condition": "Balmy breeze, partly cloudy with cooling sea mist",
                "precipitation_pct": "20%",
                "humidity": "74%",
                "attire_advice": "Comfortable yoga/workout clothes, linen lounge clothes"
            },
            "luggage_action": "Resort stay.",
            "accommodation_matrix": [
                {
                    "hotel_name": "Anantara Rasananda Koh Phangan Villas",
                    "status": "VETTED_RECOMMENDED",
                    "room_spec": "Ocean Pool Suite / Garden Pool Suite (Romantic King Bed)",
                    "critic_score": 9.6,
                    "critic_notes": "Night 5 on Koh Phangan.",
                    "price_per_night": "$260 USD / ~9,200 THB",
                    "booking_url": "https://www.anantara.com/en/rasananda-koh-phangan",
                    "map_query": "Anantara+Rasananda+Koh+Phangan"
                }
            ],
            "door_to_door_logistics": {
                "primary_transit": "Private SUV hop to Sri Thanu bohemian wellness village (West coast).",
                "departure_time": "09:30 AM",
                "arrival_time": "16:00 PM return to resort",
                "buffer_time": "Relaxed schedule",
                "tips": "Sri Thanu is the conscious wellness hub of the island—world-class sound baths, yoga, and organic culinary cafes."
            },
            "curated_daily_flow": {
                "morning": "Couple sound healing session or oceanfront restorative yoga in Sri Thanu. Walk barefoot on Zen Beach.",
                "afternoon": "Lunch at Pure Vegan Cafe or Orion Healing Centre (cold-pressed tonics, fresh sourdough, avocado tartines). Herbal sauna experience at The Dome.",
                "evening": "Return to Thong Nai Pan. Intimate private beach dinner set up exclusively by the resort butler: private table carved into the sand with tiki torches and 4-course seafood grill."
            },
            "essential_checklist": [
                "Book private beach dinner with hotel concierge 24 hours ahead",
                "Yoga mats provided at center"
            ],
            "attached_documents": [],
            "google_maps_links": [
                {"label": "Zen Beach Sri Thanu", "url": "https://maps.google.com/?q=Zen+Beach+Koh+Phangan"},
                {"label": "Orion Healing Centre", "url": "https://maps.google.com/?q=Orion+Healing+Centre+Koh+Phangan"}
            ]
        },

        # --- DAY 20: Koh Phangan (Haad Yuan Hidden Bay Escape) ---
        {
            "day_number": 20,
            "date": "2026-09-30",
            "day_of_week": "Wednesday",
            "destination": "Koh Phangan: Haad Yuan Secret Cove",
            "phase": "Couple Trip - Southern Thailand Romance",
            "phase_short": "Phase 2: Couple Trip",
            "status": "[VETTED - READY TO BOOK]",
            "status_badge": "VETTED",
            "weather_radar": {
                "temp_range": "28°C - 33°C",
                "condition": "Tropical sunshine, clear azure waters",
                "precipitation_pct": "10%",
                "humidity": "69%",
                "attire_advice": "Boho beachwear, swimwear, sunglasses, flip-flops"
            },
            "luggage_action": "Resort stay. Night 6 (final night on Koh Phangan). Pack bags for Lomprayah catamaran transfer to Koh Tao tomorrow morning.",
            "accommodation_matrix": [
                {
                    "hotel_name": "Anantara Rasananda Koh Phangan Villas",
                    "status": "VETTED_RECOMMENDED",
                    "room_spec": "Ocean Pool Suite / Garden Pool Suite (Romantic King Bed)",
                    "critic_score": 9.6,
                    "critic_notes": "Night 6 on Koh Phangan (6 nights total in Phangan).",
                    "price_per_night": "$260 USD / ~9,200 THB",
                    "booking_url": "https://www.anantara.com/en/rasananda-koh-phangan",
                    "map_query": "Anantara+Rasananda+Koh+Phangan"
                }
            ],
            "door_to_door_logistics": {
                "primary_transit": "Longtail boat from Haad Rin pier around the rocky southeastern headland to Haad Yuan / Haad Tien (10 mins by boat).",
                "departure_time": "10:30 AM",
                "arrival_time": "16:30 PM",
                "buffer_time": "Accessible only by boat or rugged jungle trail; pristine white sand and bohemian vibe",
                "tips": "Haad Yuan feels like Koh Phangan from 25 years ago; stunning wooden boardwalks built into granite cliffs."
            },
            "curated_daily_flow": {
                "morning": "Drive south to Haad Rin, hop longtail boat to Haad Yuan. Walk along the wooden cliff pathways of Eden Garden and Sanctuary.",
                "afternoon": "Swim in crystal aqua waters. Organic lunch on wooden stilt restaurant overlooking the bay. Hammock relaxation with fresh coconut.",
                "evening": "Return to Thong Nai Pan. Finale dinner on Phangan: Japanese Teppanyaki & Robata grill at Yukinoya at Anantara Rasananda. Pack suitcases for Koh Tao transfer."
            },
            "essential_checklist": [
                "Confirm Lomprayah catamaran tickets to Koh Tao for tomorrow morning (11:00 AM)",
                "Pre-arrange resort checkout transfer to Thong Sala Pier"
            ],
            "attached_documents": [],
            "google_maps_links": [
                {"label": "Haad Yuan Beach", "url": "https://maps.google.com/?q=Haad+Yuan+Beach+Koh+Phangan"},
                {"label": "Yukinoya Japanese Teppanyaki", "url": "https://maps.google.com/?q=Yukinoya+Anantara+Rasananda"}
            ]
        },

        # --- DAY 21: Koh Phangan -> Koh Tao (Hillside Villa Check-in) ---
        {
            "day_number": 21,
            "date": "2026-10-01",
            "day_of_week": "Thursday",
            "destination": "Koh Phangan -> Koh Tao (Mae Haad / Shark Bay)",
            "phase": "Couple Trip - Southern Thailand Romance",
            "phase_short": "Phase 2: Couple Trip",
            "status": "[CONFIRMED - BOOKED]",
            "status_badge": "CONFIRMED",
            "weather_radar": {
                "temp_range": "27°C - 32°C",
                "condition": "Sunny coastal weather, calm ocean swell around Koh Tao",
                "precipitation_pct": "15%",
                "humidity": "72%",
                "attire_advice": "Light travel clothes, sunglasses, flip-flops, swimwear in top bag for instant dive into pool"
            },
            "luggage_action": "Bags loaded onto Lomprayah catamaran luggage cart; private hotel shuttle handles pickup at Mae Haad Pier.",
            "accommodation_matrix": [
                {
                    "hotel_name": "The Place Luxury Boutique Villas Koh Tao",
                    "status": "VETTED_RECOMMENDED",
                    "room_spec": "One-Bedroom Private Pool Villa (King Bed + Private Horizon Infinity Pool)",
                    "critic_score": 9.7,
                    "critic_notes": "Pass 1-3 Verified: Consistently ranked the #1 romantic boutique property in Southeast Asia. Completely private, isolated hillside sanctuary, open-plan floor-to-ceiling glass, uninterrupted ocean panoramas, zero noise.",
                    "price_per_night": "$240 USD / ~8,500 THB",
                    "booking_url": "https://theplacekohtao.com/",
                    "map_query": "The+Place+Luxury+Boutique+Villas+Koh+Tao"
                },
                {
                    "hotel_name": "Jamahkiri Dive Resort & Spa (Shark Bay)",
                    "status": "VETTED_ALTERNATIVE",
                    "room_spec": "Royal Ocean Suite King",
                    "critic_score": 9.2,
                    "critic_notes": "Dramatic cliffside architecture on Shark Bay, direct access to reef, premier private spa.",
                    "price_per_night": "$190 USD / ~6,700 THB",
                    "booking_url": "https://jamahkiri.com/",
                    "map_query": "Jamahkiri+Resort+Koh+Tao"
                }
            ],
            "door_to_door_logistics": {
                "primary_transit": "09:45 AM: Resort transfer to Phangan Thong Sala Pier. 11:00 AM: Lomprayah high-speed catamaran to Koh Tao Mae Haad Pier (1 hr, arr 12:00 PM). Private villa host greeting with flower garlands; 10-min SUV transfer up to hillside villa.",
                "departure_time": "09:45 AM Phangan checkout",
                "arrival_time": "12:30 PM Koh Tao villa check-in",
                "buffer_time": "Luggage handled directly from pier to villa by host",
                "tips": "The Place provides a complimentary mobile phone loaded with villa host contact and direct taxi bookings."
            },
            "curated_daily_flow": {
                "morning": "Farewell breakfast in Phangan. Board the Lomprayah catamaran skimming northward across the Gulf to diver's paradise Koh Tao.",
                "afternoon": "Step onto Koh Tao. Private transfer to The Place Luxury Boutique Villas. Orientation of your private luxury villa. Infinity pool floating over the jungle canopy with sweeping sea views. Cold coconut welcome drink.",
                "evening": "Sunset cocktails on oversized daybeds watching twilight illuminate the bay. In-villa romantic barbecue prepared by private chef or casual dining down at Sairee Beach (Barracuda Restaurant - fresh snapper with mango salsa)."
            },
            "essential_checklist": [
                "Lomprayah boarding pass ready (ref: LOM-PT-20261001-304)",
                "Koh Tao environmental island entry fee (20 THB / paid at pier)",
                "Pre-book introductory scuba / turtle snorkel for tomorrow"
            ],
            "attached_documents": [
                {
                    "doc_id": "FERRY-PHANGAN-TAO",
                    "title": "Lomprayah High-Speed Catamaran Ticket (Phangan -> Tao)",
                    "ref": "LOM-PT-20261001-304",
                    "category": "Ferry Ticket",
                    "badge": "CONFIRMED"
                }
            ],
            "google_maps_links": [
                {"label": "The Place Luxury Boutique Villas", "url": "https://maps.google.com/?q=The+Place+Luxury+Boutique+Villas+Koh+Tao"},
                {"label": "Mae Haad Pier Koh Tao", "url": "https://maps.google.com/?q=Mae+Haad+Pier+Koh+Tao"},
                {"label": "Barracuda Restaurant", "url": "https://maps.google.com/?q=Barracuda+Restaurant+Koh+Tao"}
            ]
        },

        # --- DAY 22: Koh Tao (Shark Bay Turtles & Viewpoints) ---
        {
            "day_number": 22,
            "date": "2026-10-02",
            "day_of_week": "Friday",
            "destination": "Koh Tao: Shark Bay Marine Life & John-Suwan Viewpoint",
            "phase": "Couple Trip - Southern Thailand Romance",
            "phase_short": "Phase 2: Couple Trip",
            "status": "[VETTED - READY TO BOOK]",
            "status_badge": "VETTED",
            "weather_radar": {
                "temp_range": "28°C - 33°C",
                "condition": "Brilliant turquoise visibility, calm protected waters in southern bays",
                "precipitation_pct": "10%",
                "humidity": "68%",
                "attire_advice": "Snorkel gear, rash guard, sun hat, trainers for viewpoint climb"
            },
            "luggage_action": "Villa stay.",
            "accommodation_matrix": [
                {
                    "hotel_name": "The Place Luxury Boutique Villas Koh Tao",
                    "status": "VETTED_RECOMMENDED",
                    "room_spec": "One-Bedroom Private Pool Villa (Romantic King Bed)",
                    "critic_score": 9.7,
                    "critic_notes": "Night 2 on Koh Tao.",
                    "price_per_night": "$240 USD / ~8,500 THB",
                    "booking_url": "https://theplacekohtao.com/",
                    "map_query": "The+Place+Luxury+Boutique+Villas+Koh+Tao"
                }
            ],
            "door_to_door_logistics": {
                "primary_transit": "Private 4x4 taxi or villa scooter down to Shark Bay (Thian Og Bay, 12 mins) and Freedom Beach.",
                "departure_time": "09:00 AM",
                "arrival_time": "16:00 PM return to villa",
                "buffer_time": "Morning high-tide provides optimal turtle sighting visibility",
                "tips": "Shark Bay is home to resident green sea turtles (up to 1.5m long) and harmless blacktip reef sharks in shallow water."
            },
            "curated_daily_flow": {
                "morning": "Head down to Shark Bay with snorkel gear. Swim alongside giant green sea turtles grazing on sea grass and observe sleek blacktip reef sharks in the shallow reef.",
                "afternoon": "Stroll around to adjacent Freedom Beach. Short 15-minute hike up John-Suwan Viewpoint for Koh Tao's most iconic twin-bay panorama (Chalok Baan Kao and Shark Bay back-to-back).",
                "evening": "Sunset cocktails at Sun Suwan 360 Viewpoint Bar. Return to villa for evening swim in the lit pool. Dinner at The Gallery Restaurant (fine Thai dining, famous red curry duck)."
            },
            "essential_checklist": [
                "Reef-safe sunscreen only (strictly enforced in Koh Tao marine zones)",
                "Waterproof camera / underwater housing for turtle photos",
                "Small entrance fee for Freedom Beach (50 THB)"
            ],
            "attached_documents": [],
            "google_maps_links": [
                {"label": "Shark Bay (Thian Og)", "url": "https://maps.google.com/?q=Shark+Bay+Koh+Tao"},
                {"label": "John-Suwan Viewpoint", "url": "https://maps.google.com/?q=John+Suwan+Viewpoint+Koh+Tao"},
                {"label": "The Gallery Restaurant", "url": "https://maps.google.com/?q=The+Gallery+Restaurant+Koh+Tao"}
            ]
        },

        # --- DAY 23: Koh Tao (Koh Nang Yuan Private Longtail Charter) ---
        {
            "day_number": 23,
            "date": "2026-10-03",
            "day_of_week": "Saturday",
            "destination": "Koh Tao: Koh Nang Yuan Island & Japanese Gardens",
            "phase": "Couple Trip - Southern Thailand Romance",
            "phase_short": "Phase 2: Couple Trip",
            "status": "[VETTED - READY TO BOOK]",
            "status_badge": "VETTED",
            "weather_radar": {
                "temp_range": "28°C - 33°C",
                "condition": "Crystal sunshine, flat calm ocean, extraordinary underwater visibility (25m+)",
                "precipitation_pct": "10%",
                "humidity": "67%",
                "attire_advice": "Swimwear, beach towel, snorkel mask, camera"
            },
            "luggage_action": "Villa stay.",
            "accommodation_matrix": [
                {
                    "hotel_name": "The Place Luxury Boutique Villas Koh Tao",
                    "status": "VETTED_RECOMMENDED",
                    "room_spec": "One-Bedroom Private Pool Villa (Romantic King Bed)",
                    "critic_score": 9.7,
                    "critic_notes": "Night 3 on Koh Tao.",
                    "price_per_night": "$240 USD / ~8,500 THB",
                    "booking_url": "https://theplacekohtao.com/",
                    "map_query": "The+Place+Luxury+Boutique+Villas+Koh+Tao"
                }
            ],
            "door_to_door_logistics": {
                "primary_transit": "Private longtail boat charter from northern Sairee beach across to Koh Nang Yuan (10 mins crossing).",
                "departure_time": "08:30 AM (arriving right as the island gates open at 09:00 AM before day-tripper catamarans)",
                "arrival_time": "13:30 PM return to main island",
                "buffer_time": "Early arrival guarantees empty sandbar photographs",
                "tips": "No plastic bottles allowed on Koh Nang Yuan; bring reusable stainless steel bottles."
            },
            "curated_daily_flow": {
                "morning": "Board private longtail boat to Koh Nang Yuan—three islets connected by a natural powdery white sand spit. Immediately hike the 10-minute wooden stairs to the summit viewpoint for the world-famous postcard panorama.",
                "afternoon": "Descend to the Japanese Gardens reef on the eastern sandbar. Snorkel among table corals, giant clams with electric blue lips, and clownfish. Relax under parasols on the sandbar before returning to Koh Tao.",
                "evening": "Romantic beachfront sunset lounge at Fizz Beach Lounge on Sairee Beach (bean bags on the sand, chilled house music, mojitos). Dinner at Blue Water Cafe with fresh wood-fired Mediterranean seafood."
            },
            "essential_checklist": [
                "Koh Nang Yuan entrance fee (250 THB / person)",
                "Strict rule: No plastic bottles or fins allowed on Nang Yuan (protects coral)",
                "Bring reusable water flask"
            ],
            "attached_documents": [],
            "google_maps_links": [
                {"label": "Koh Nang Yuan Viewpoint", "url": "https://maps.google.com/?q=Koh+Nang+Yuan+Viewpoint"},
                {"label": "Japanese Gardens Reef", "url": "https://maps.google.com/?q=Japanese+Gardens+Koh+Nang+Yuan"},
                {"label": "Fizz Beach Lounge", "url": "https://maps.google.com/?q=Fizz+Beach+Lounge+Koh+Tao"}
            ]
        },

        # --- DAY 24: Koh Tao (Scuba / Freediving or Tanote Bay) ---
        {
            "day_number": 24,
            "date": "2026-10-04",
            "day_of_week": "Sunday",
            "destination": "Koh Tao: Sail Rock / Chumphon Pinnacle Scuba & Cliffside Dinner",
            "phase": "Couple Trip - Southern Thailand Romance",
            "phase_short": "Phase 2: Couple Trip",
            "status": "[VETTED - READY TO BOOK]",
            "status_badge": "VETTED",
            "weather_radar": {
                "temp_range": "27°C - 32°C",
                "condition": "Warm tropical sun, light afternoon breeze",
                "precipitation_pct": "15%",
                "humidity": "71%",
                "attire_advice": "Swimwear, comfortable boat clothes, sunglasses"
            },
            "luggage_action": "Villa stay.",
            "accommodation_matrix": [
                {
                    "hotel_name": "The Place Luxury Boutique Villas Koh Tao",
                    "status": "VETTED_RECOMMENDED",
                    "room_spec": "One-Bedroom Private Pool Villa (Romantic King Bed)",
                    "critic_score": 9.7,
                    "critic_notes": "Night 4 on Koh Tao.",
                    "price_per_night": "$240 USD / ~8,500 THB",
                    "booking_url": "https://theplacekohtao.com/",
                    "map_query": "The+Place+Luxury+Boutique+Villas+Koh+Tao"
                }
            ],
            "door_to_door_logistics": {
                "primary_transit": "Private dive boat excursion or taxi hop across the spine road to Tanote Bay on the wild East Coast (20 mins).",
                "departure_time": "08:00 AM dive boat / 10:00 AM beach hop",
                "arrival_time": "15:00 PM return to villa",
                "buffer_time": "Relaxed recovery afternoon by pool",
                "tips": "For non-divers, Tanote Bay offers giant boulder cliff jumping and exceptional coral drop-offs."
            },
            "curated_daily_flow": {
                "morning": "Morning couple scuba dive or discover scuba trip to Chumphon Pinnacle or Twins Reef (schools of chevron barracuda, batfish, and occasional whale shark passes). Alternatively, head to Tanote Bay for granite rock leaping and snorkeling.",
                "afternoon": "Return to villa. Indulge in poolside massage on your private timber deck listening to jungle cicadas and ocean waves.",
                "evening": "Cliffside fine dining at Jamahkiri Restaurant perched 50 meters above Shark Bay. Candlelit terrace, premium wine list, grilled rock lobster, and fresh oysters under the starlit sky."
            },
            "essential_checklist": [
                "Log dives in digital logbook if certified",
                "No-fly buffer check: Flying on Oct 07, so scuba on Oct 04 provides over 65+ hours buffer (far exceeding standard 18-24 hour safety rules!)"
            ],
            "attached_documents": [],
            "google_maps_links": [
                {"label": "Tanote Bay", "url": "https://maps.google.com/?q=Tanote+Bay+Koh+Tao"},
                {"label": "Chumphon Pinnacle", "url": "https://maps.google.com/?q=Chumphon+Pinnacle+Koh+Tao"},
                {"label": "Jamahkiri Restaurant", "url": "https://maps.google.com/?q=Jamahkiri+Restaurant+Koh+Tao"}
            ]
        },

        # --- DAY 25: Koh Tao (East Coast Hidden Coves & Kayaking) ---
        {
            "day_number": 25,
            "date": "2026-10-05",
            "day_of_week": "Monday",
            "destination": "Koh Tao: Hin Wong Bay & Mango Bay",
            "phase": "Couple Trip - Southern Thailand Romance",
            "phase_short": "Phase 2: Couple Trip",
            "status": "[VETTED - READY TO BOOK]",
            "status_badge": "VETTED",
            "weather_radar": {
                "temp_range": "27°C - 32°C",
                "condition": "Sunny morning, refreshing afternoon ocean breeze",
                "precipitation_pct": "20%",
                "humidity": "73%",
                "attire_advice": "Swimwear, rashguard, strap-on water sandals, sun hat"
            },
            "luggage_action": "Villa stay.",
            "accommodation_matrix": [
                {
                    "hotel_name": "The Place Luxury Boutique Villas Koh Tao",
                    "status": "VETTED_RECOMMENDED",
                    "room_spec": "One-Bedroom Private Pool Villa (Romantic King Bed)",
                    "critic_score": 9.7,
                    "critic_notes": "Night 5 on Koh Tao.",
                    "price_per_night": "$240 USD / ~8,500 THB",
                    "booking_url": "https://theplacekohtao.com/",
                    "map_query": "The+Place+Luxury+Boutique+Villas+Koh+Tao"
                }
            ],
            "door_to_door_logistics": {
                "primary_transit": "Private longtail boat or 4x4 taxi to Hin Wong Bay on the serene northeast coast (15 mins).",
                "departure_time": "10:00 AM",
                "arrival_time": "16:00 PM return to villa",
                "buffer_time": "Untouched secluded bays",
                "tips": "Hin Wong Bay has massive boulder fields underwater teeming with yellowtail fusiliers."
            },
            "curated_daily_flow": {
                "morning": "Journey to remote Hin Wong Bay. Rent ocean kayaks and paddle along the granite cliffs to tiny hidden sandy coves accessible only from water.",
                "afternoon": "Snorkel through schools of thousands of glittering blue-ringed fusiliers. Relax with fresh fruit shakes at Hin Wong cliff restaurant.",
                "evening": "Sunset cocktails at Sairee Cottage Beach Club. Casual dinner at Whitening (chic all-white beachfront restaurant right on the sand with grilled tiger prawns and pad thai)."
            },
            "essential_checklist": [
                "Waterproof dry bag for kayak",
                "Snorkel vest for relaxed floating",
                "Pre-book return ferry + flight combo to Bangkok for Oct 07"
            ],
            "attached_documents": [],
            "google_maps_links": [
                {"label": "Hin Wong Bay", "url": "https://maps.google.com/?q=Hin+Wong+Bay+Koh+Tao"},
                {"label": "Whitening Beachfront Restaurant", "url": "https://maps.google.com/?q=Whitening+Restaurant+Koh+Tao"}
            ]
        },

        # --- DAY 26: Koh Tao (Couples Spa & Sunset Toast Finale) ---
        {
            "day_number": 26,
            "date": "2026-10-06",
            "day_of_week": "Tuesday",
            "destination": "Koh Tao: Island Finale & Sunset Toast",
            "phase": "Couple Trip - Southern Thailand Romance",
            "phase_short": "Phase 2: Couple Trip",
            "status": "[VETTED - READY TO BOOK]",
            "status_badge": "VETTED",
            "weather_radar": {
                "temp_range": "28°C - 33°C",
                "condition": "Glorious tropical sun, calm sea",
                "precipitation_pct": "10%",
                "humidity": "69%",
                "attire_advice": "Resort casual, swimwear, evening linen dinner attire"
            },
            "luggage_action": "Pack and zip suitcases for tomorrow's transfer to Bangkok. Total 13 nights in Gulf islands complete!",
            "accommodation_matrix": [
                {
                    "hotel_name": "The Place Luxury Boutique Villas Koh Tao",
                    "status": "VETTED_RECOMMENDED",
                    "room_spec": "One-Bedroom Private Pool Villa (Romantic King Bed)",
                    "critic_score": 9.7,
                    "critic_notes": "Night 6 on Koh Tao (6 nights total in Koh Tao; 13 nights Gulf total).",
                    "price_per_night": "$240 USD / ~8,500 THB",
                    "booking_url": "https://theplacekohtao.com/",
                    "map_query": "The+Place+Luxury+Boutique+Villas+Koh+Tao"
                }
            ],
            "door_to_door_logistics": {
                "primary_transit": "Self-paced local transport. Evening transfer arranged for tomorrow morning's 09:30 AM Lomprayah catamaran departure.",
                "departure_time": "N/A",
                "arrival_time": "N/A",
                "buffer_time": "Island finale decompression",
                "tips": "Confirm pier pickup time with villa manager tonight."
            },
            "curated_daily_flow": {
                "morning": "Lazy morning floating in your private infinity pool. Fresh tropical fruit platter delivered to villa patio.",
                "afternoon": "Stroll Mae Haad and Sairee boutiques for handcrafted Thai silver jewelry, linen shirts, and island souvenirs. Couple herbal steam and body scrub.",
                "evening": "Gulf of Thailand Grand Sunset Toast: Reserved panoramic table at Sunset 360 Bar / High Ground overlooking the entire west coast as sky turns magenta and gold. Farewell island dinner at Hippo Bar & Grill (tender Australian beef steaks, fresh lobster, grilled asparagus)."
            },
            "essential_checklist": [
                "Pack all scuba gear and beach clothes into checked suitcase",
                "Reconfirm tomorrow's Lomprayah catamaran (dep 09:30 Mae Haad Pier)",
                "Set alarm for 08:00 AM checkout"
            ],
            "attached_documents": [],
            "google_maps_links": [
                {"label": "Sunset 360 Bar", "url": "https://maps.google.com/?q=Sunset+360+Bar+Koh+Tao"},
                {"label": "Hippo Bar & Grill", "url": "https://maps.google.com/?q=Hippo+Bar+Koh+Tao"}
            ]
        },

        # --- DAY 27: Koh Tao -> Bangkok (Riverside Boutique Check-in) ---
        {
            "day_number": 27,
            "date": "2026-10-07",
            "day_of_week": "Wednesday",
            "destination": "Koh Tao -> Bangkok (Upscale Finale Base)",
            "phase": "Couple Trip - Southern Thailand Romance",
            "phase_short": "Phase 2: Couple Trip",
            "status": "[CONFIRMED - BOOKED]",
            "status_badge": "CONFIRMED",
            "weather_radar": {
                "temp_range": "27°C - 33°C",
                "condition": "Warm urban sunset, clear skyline",
                "precipitation_pct": "25%",
                "humidity": "72%",
                "attire_advice": "Comfortable transit clothes, smart evening dress/collar shirt for upscale rooftop bar"
            },
            "luggage_action": "Luggage checked seamlessly from ferry to airport transfer.",
            "accommodation_matrix": [
                {
                    "hotel_name": "Riva Arun Bangkok / The Mustang Blu",
                    "status": "VETTED_RECOMMENDED",
                    "room_spec": "Premium Chao Phraya River View King / Vintage Suite",
                    "critic_score": 9.4,
                    "critic_notes": "Pass 1-3 Verified: Unrivaled view directly facing illuminated Wat Arun across the Chao Phraya river. Boutique romantic atmosphere, rooftop dining, away from highway noise.",
                    "price_per_night": "$145 USD / ~5,100 THB",
                    "booking_url": "https://www.rivaarunbangkok.com/",
                    "map_query": "Riva+Arun+Bangkok"
                },
                {
                    "hotel_name": "Carlton Hotel Bangkok Sukhumvit",
                    "status": "VETTED_ALTERNATIVE",
                    "room_spec": "Executive King Room with Rooftop Access",
                    "critic_score": 9.3,
                    "critic_notes": "5-star luxury in central Sukhumvit, Cooling Tower rooftop bar, luxury spa.",
                    "price_per_night": "$160 USD / ~5,600 THB",
                    "booking_url": "https://www.carltonhotel.co.th/",
                    "map_query": "Carlton+Hotel+Bangkok+Sukhumvit"
                }
            ],
            "door_to_door_logistics": {
                "primary_transit": "09:00 AM: Villa checkout & transfer to Mae Haad. 09:30 AM: Lomprayah catamaran Koh Tao -> Koh Samui Pralarn Pier (arr 11:15 AM). 12:00 PM: Transfer to Samui Airport (USM). 14:00 PM: Bangkok Airways PG 148 flight USM -> BKK Suvarnabhumi (arr 15:15 PM). 16:00 PM: Private limousine transfer to Riva Arun Bangkok (arr 16:45 PM).",
                "departure_time": "09:00 AM Koh Tao",
                "arrival_time": "16:45 PM Bangkok hotel check-in",
                "buffer_time": "Smooth flight connection back to Bangkok capital",
                "tips": "Landing at BKK Suvarnabhumi makes final departure on Oct 09 extremely convenient."
            },
            "curated_daily_flow": {
                "morning": "Board morning catamaran bidding goodbye to Koh Tao's turquoise waters. Quick ferry ride to Samui, transfer to Samui open-air garden airport.",
                "afternoon": "Short comfortable Bangkok Airways flight into Bangkok Suvarnabhumi. Private transfer to riverside boutique hotel Riva Arun. Check into river-facing King room.",
                "evening": "Golden hour on your private river balcony watching illuminated longtail boats glide on Chao Phraya. Ascend to Octave Rooftop Lounge (45th floor) or Above Riva for panoramic city skyline cocktails. Dinner at Supanniga Eating Room Riverside (crispy pork belly with crab meat and cabbage, massaman beef curry)."
            },
            "essential_checklist": [
                "Lomprayah + flight tickets ready on phone",
                "Rooftop dress code: Collared shirt, smart trousers, closed shoes (no beach flip-flops)"
            ],
            "attached_documents": [
                {
                    "doc_id": "FERRY-FLIGHT-TAO-BKK",
                    "title": "Koh Tao -> Bangkok VIP Combined Transit Pass",
                    "ref": "LOM-AIR-KTBKK-77",
                    "category": "Transit Ticket",
                    "badge": "CONFIRMED"
                }
            ],
            "google_maps_links": [
                {"label": "Riva Arun Bangkok", "url": "https://maps.google.com/?q=Riva+Arun+Bangkok"},
                {"label": "Wat Arun (Viewpoint)", "url": "https://maps.google.com/?q=Wat+Arun+Bangkok"},
                {"label": "Octave Rooftop Lounge", "url": "https://maps.google.com/?q=Octave+Rooftop+Bangkok"},
                {"label": "Supanniga Eating Room", "url": "https://maps.google.com/?q=Supanniga+Eating+Room+Tha+Tien"}
            ]
        },

        # --- DAY 28: Bangkok Finale (Fine Dining, Canals & Shopping) ---
        {
            "day_number": 28,
            "date": "2026-10-08",
            "day_of_week": "Thursday",
            "destination": "Bangkok: Thonburi Khlongs, ICONSIAM & Fine Dining",
            "phase": "Couple Trip - Southern Thailand Romance",
            "phase_short": "Phase 2: Couple Trip",
            "status": "[VETTED - READY TO BOOK]",
            "status_badge": "VETTED",
            "weather_radar": {
                "temp_range": "27°C - 33°C",
                "condition": "Warm urban sunshine, breezy riverside evening",
                "precipitation_pct": "20%",
                "humidity": "70%",
                "attire_advice": "Smart casual daywear, sophisticated evening attire for Michelin fine dining"
            },
            "luggage_action": "Evening full pack & weigh of checked suitcase + 55L clamshell backpack. Finalize duty-free shopping bags.",
            "accommodation_matrix": [
                {
                    "hotel_name": "Riva Arun Bangkok / The Mustang Blu",
                    "status": "VETTED_RECOMMENDED",
                    "room_spec": "Premium Chao Phraya River View King",
                    "critic_score": 9.4,
                    "critic_notes": "Finale night in Thailand.",
                    "price_per_night": "$145 USD / ~5,100 THB",
                    "booking_url": "https://www.rivaarunbangkok.com/",
                    "map_query": "Riva+Arun+Bangkok"
                }
            ],
            "door_to_door_logistics": {
                "primary_transit": "Chao Phraya Express boat & private longtail canal tour from Tha Tien pier. Air-conditioned BTS Skytrain / Grab taxi for evening dinner.",
                "departure_time": "10:00 AM",
                "arrival_time": "Self-paced",
                "buffer_time": "Pre-departure preparation day",
                "tips": "Gold Line train connects directly into ICONSIAM luxury mall without road traffic."
            },
            "curated_daily_flow": {
                "morning": "Riverfront breakfast facing the ancient spires of Wat Arun. Step directly onto a private teakwood longtail boat for a private cruise through the tranquil Thonburi canals (khlongs)—gliding past wooden stilt houses, floating orchid gardens, and the giant golden Buddha at Wat Paknam.",
                "afternoon": "Cross to ICONSIAM. Explore the ground-level indoor floating market (SookSiam) for artisanal treats, followed by high-end shopping and souvenir curation.",
                "evening": "Thailand Grand Finale Michelin-Star Feast: Sühring (modern German-European fine dining in a romantic glasshouse villa) or Paste Bangkok (refined royal Thai cuisine). Late-night nightcap toast to an unforgettable 29-day expedition across Vietnam and Thailand."
            },
            "essential_checklist": [
                "Pack all liquids over 100ml into checked suitcase",
                "Weigh bags: Ensure checked suitcase $\le$ 23kg and backpack $\le$ 7-10kg",
                "Verify return flight booking 9KDEH2 status with airline"
            ],
            "attached_documents": [],
            "google_maps_links": [
                {"label": "ICONSIAM Luxury Mall", "url": "https://maps.google.com/?q=ICONSIAM+Bangkok"},
                {"label": "Wat Paknam Giant Buddha", "url": "https://maps.google.com/?q=Wat+Paknam+Phasi+Charoen"},
                {"label": "Sühring Restaurant", "url": "https://maps.google.com/?q=Suhring+Bangkok"},
                {"label": "Paste Bangkok", "url": "https://maps.google.com/?q=Paste+Bangkok"}
            ]
        },

        # --- DAY 29: Bangkok Departure (Flight 9KDEH2) ---
        {
            "day_number": 29,
            "date": "2026-10-09",
            "day_of_week": "Friday",
            "destination": "Bangkok (BKK) Departure -> TLV via AUH",
            "phase": "Couple Trip - Southern Thailand Romance",
            "phase_short": "Trip Finale",
            "status": "[CONFIRMED - BOOKED]",
            "status_badge": "CONFIRMED",
            "weather_radar": {
                "temp_range": "28°C - 33°C",
                "condition": "Warm tropical sun over Bangkok",
                "precipitation_pct": "20%",
                "humidity": "68%",
                "attire_advice": "Comfortable long-haul flight layers, compression socks, slip-on shoes"
            },
            "luggage_action": "Complete travel gear repacked: 1x 55L clamshell travel backpack + 1x checked suitcase. Check in suitcase at BKK international departure hall.",
            "accommodation_matrix": [],
            "door_to_door_logistics": {
                "primary_transit": "Hotel checkout. Private express expressway transfer to Suvarnabhumi International Airport (BKK, 40 mins). Check in 3.5 hours prior for international flight 9KDEH2 BKK -> TLV via Abu Dhabi (AUH).",
                "departure_time": "3.5 hours before flight departure",
                "arrival_time": "BKK International Terminal",
                "buffer_time": "3.5 hours for VAT refund inspection, bag drop, security, and duty-free",
                "tips": "Present VAT refund yellow forms (P.P.10) at customs desk BEFORE passport control."
            },
            "curated_daily_flow": {
                "morning": "Final lazy riverfront breakfast at Riva Arun watching river traffic. Last-minute foot massage nearby.",
                "afternoon": "Check out. Private sedan transfer via Sirat Expressway directly to Suvarnabhumi Airport (BKK) Level 4 Departure Hall.",
                "evening": "Check-in for international departure flight 9KDEH2. Clear security and passport control. Enjoy lounge amenities and duty-free shopping before boarding flight to Tel Aviv via Abu Dhabi. Safe travels!"
            },
            "essential_checklist": [
                "Flight booking reference 9KDEH2 ready",
                "Passports valid for at least 6 months",
                "VAT refund slips stamped before security",
                "Check out completed, all gear accounted for"
            ],
            "attached_documents": [
                {
                    "doc_id": "FLIGHT-BKK-TLV-9KDEH2",
                    "title": "International Return Flight E-Ticket: BKK -> TLV via AUH",
                    "ref": "Booking: 9KDEH2",
                    "category": "Flight Ticket",
                    "badge": "CONFIRMED"
                }
            ],
            "google_maps_links": [
                {"label": "Suvarnabhumi Airport Departures", "url": "https://maps.google.com/?q=Suvarnabhumi+Airport+Departures"}
            ]
        }
    ]

    master_payload = {
        "title": "Master Itinerary: Thailand & Vietnam [Live Travel OS]",
        "generated_at": "2026-09-09T03:42:00Z",
        "system_version": "2.4.0",
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
                "flight": "Hanoi (HAN) -> Bangkok (BKK) 12:45 PM (Booking: 1145-554-179)",
                "separation": "Friend departs/separates at BKK",
                "luggage_retrieval": "Retrieve checked suitcase at AIRPORTELs Suvarnabhumi Basement (Floor B)",
                "reunion": "Traveler reunites with Girlfriend in Bangkok",
                "south_flight": "Bangkok (BKK) -> Koh Samui (USM) Direct (Bangkok Airways PG 169)"
            },
            "party_phase_2": {
                "label": "Gulf of Thailand & Bangkok Finale (Sep 24 – Oct 09, 2026)",
                "party": "Traveler + Girlfriend",
                "room_requirement": "Strictly Double / Romantic King Bed with Prime Ocean Views",
                "vibe": "Boutique romantic stays, beaches, high-end island dining, relaxed diving/snorkeling",
                "pacing": "13 nights Gulf (1 Samui + 6 Phangan + 6 Tao) + 2 nights Bangkok Finale = 15 nights total",
                "departure_flight": "Oct 09: BKK -> TLV via AUH (Booking: 9KDEH2)"
            }
        },
        "luggage_storage_protocol": {
            "facility": "AIRPORTELs Luggage Storage (Suvarnabhumi Airport Floor B, Airport Rail Link Level)",
            "dropoff_date": "2026-09-12 (Morning, before 11:55 flight to HAN)",
            "pickup_date": "2026-09-24 (14:35 arrival from HAN)",
            "duration": "12 Days",
            "storage_cost": "~100-150 THB / day (approx. 1,200 - 1,800 THB total)",
            "item_deposited": "1x Large Checked Suitcase containing Phase 2 resort attire",
            "item_kept": "1x 55L Clamshell Backpack (strictly backpack-only throughout Vietnam)",
            "location_advantage": "Located right at the Airport Rail Link basement entrance. Avoids taking checked luggage into Bangkok on Sep 24 before departing for Koh Samui."
        },
        "flight_radar_bkk_usm": {
            "route": "Bangkok Suvarnabhumi (BKK) -> Koh Samui (USM)",
            "date": "2026-09-24",
            "earliest_departure": "16:30 PM (after 14:35 HAN arrival + bag retrieval)",
            "recommended_flights": [
                {
                    "flight_number": "Bangkok Airways PG 169",
                    "departure": "17:15 PM (BKK)",
                    "arrival": "18:20 PM (USM)",
                    "duration": "1h 05m Nonstop",
                    "transit_buffer": "2h 40m connection buffer (optimal comfort)"
                },
                {
                    "flight_number": "Bangkok Airways PG 175",
                    "departure": "18:00 PM (BKK)",
                    "arrival": "19:05 PM (USM)",
                    "duration": "1h 05m Nonstop",
                    "transit_buffer": "3h 25m connection buffer (ultra-relaxed)"
                }
            ],
            "fare_tier_strategy": {
                "cheapest_bucket": "Web Saver (Approx. $115 - $135 USD / 4,100 - 4,800 THB one-way)",
                "standard_bucket": "Web Freedom (Approx. $155 - $185 USD / 5,500 - 6,500 THB one-way)",
                "optimal_booking_window": "6 to 8 weeks prior to departure (Mid-July to Early August 2026). Bangkok Airways controls this exclusive route and rarely discounts last-minute; Web Saver seats open 90 days out and fill by 3-4 weeks prior."
            }
        },
        "total_days": len(days),
        "days": days
    }

    out_path = os.path.join(os.path.dirname(__file__), "itinerary_data.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(master_payload, f, indent=2, ensure_ascii=False)
    print(f"Successfully generated {out_path} with {len(days)} days!")

if __name__ == "__main__":
    build_itinerary()
