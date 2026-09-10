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
import sys

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
            "booking_summary": "Emirates EK2451/EK384 (Booking: G5M8CF, arr 12:30 PM) • Sukhon Hotel (Booking: 697155847) • TDAC #30C4358",
            "weather_radar": {
                "temp_range": "27°C - 33°C",
                "condition": "Tropical sun with scattered clouds, passing evening shower",
                "precipitation_pct": "35%",
                "humidity": "75%",
                "attire_advice": "Breathable travel clothes, light trainers, compact umbrella in backpack"
            },
            "luggage_action": "Arrive at BKK with 1x 55L clamshell backpack + 1x checked suitcase. Prepare suitcase for basement storage tomorrow morning.",
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
                "primary_transit": "Emirates flight EK2451/EK384 (TLV dep Sep 10 17:25 -> DXB -> BKK arr Sep 11 12:30 PM on A380). Clear immigration, board Airport Rail Link (ARL) from BKK Suvarnabhumi Basement directly to Phaya Thai Station (45 THB / 26 mins). Walk 80m to Sukhon Hotel.",
                "departure_time": "Sep 10 17:25 (TLV) -> Sep 11 12:30 PM (BKK Landing)",
                "arrival_time": "14:00 PM check-in",
                "buffer_time": "90 mins for immigration, baggage claim, and ARL train ride",
                "tips": "Show TDAC #30C4358 at passport control. ARL trains run every 10-12 mins until midnight."
            },
            "curated_daily_flow": {
                "morning": "Flight arrival into Bangkok Suvarnabhumi (BKK) on Emirates A380 (12:30 PM). Pass immigration using verified TDAC pass.",
                "afternoon": "Board Airport Rail Link City Line to Phaya Thai terminus. Check-in at Sukhon Hotel, refresh, and unpack.",
                "evening": "Stroll down Phetchaburi Soi 5 for Pe Aor Tom Yum Kung Noodles, crispy pork, and iced Thai tea."
            },
            "essential_checklist": [
                "Have Thailand Digital Arrival Card (TDAC #30C4358) and Emirates boarding pass on phone",
                "Withdraw 5,000 THB from Krungsri ATM (yellow machine)",
                "Repack checked suitcase with all Phase 2 items; isolate 55L backpack for Vietnam"
            ],
            "attached_documents": [
                {
                    "doc_id": "FLIGHT-TLV-BKK-G5M8CF",
                    "title": "Flight: Tel Aviv (TLV) -> Bangkok (BKK) via Dubai",
                    "ref": "Emirates: G5M8CF",
                    "status": "Verified Official E-Ticket (Gmail)",
                    "badge": "CONFIRMED & DOWNLOADED",
                    "file_path": "documents/Emirates_Flight_TLV_BKK_G5M8CF.pdf",
                    "file_name": "Emirates_Flight_TLV_BKK_G5M8CF.pdf"
                },
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

        # --- DAY 2: Suitcase Drop, Flight to Hanoi & Airport Sleeper to Ha Giang ---
        {
            "day_number": 2,
            "date": "2026-09-12",
            "day_of_week": "Saturday",
            "destination": "Bangkok -> Hanoi Airport (HAN) -> Sleeper to Ha Giang",
            "phase": "Guys Trip - Vietnam Expedition",
            "phase_short": "Phase 1: Guys Trip",
            "status": "[FLIGHT BOOKED / HA GIANG TOUR UNBOOKED]",
            "status_badge": "PARTIAL",
            "booking_summary": "Flight BKK->HAN Confirmed (Order: 1145-554-179) • Ha Giang 3D Tour & Airport Sleeper Unbooked (Action Required)",
            "weather_radar": {
                "temp_range": "25°C - 32°C",
                "condition": "Warm with afternoon breeze at Noi Bai; cool mountain air upon Ha Giang arrival",
                "precipitation_pct": "30%",
                "humidity": "80%",
                "attire_advice": "Comfortable travel clothes, slip-on shoes for airport security, rain shell packed ready in top of 55L pack"
            },
            "luggage_action": "ACTION REQUIRED: Drop checked suitcase at AIRPORTELs Suvarnabhumi Basement (Floor B, next to ARL) for 12 days (Sep 12-24). Keep ONLY 55L clamshell backpack for flight and Ha Giang sleeper bus!",
            "accommodation_matrix": [
                {
                    "hotel_name": "Phoenix Hotel Ha Giang (Included in 3D Tour)",
                    "status": "UNBOOKED_VETTED_OPTION",
                    "room_spec": "Deluxe Twin Room (Two Separate Single Beds)",
                    "critic_score": 9.1,
                    "critic_notes": "Included in Ha Giang 3D Tour package. Located in Ha Giang City center, soundproof rooms, hot rainfall showers, AC, twin beds.",
                    "price_per_night": "Included in Ha Giang Tour Package ($170-$210 total for 3D/2N + transfers)",
                    "booking_url": "https://cheershagiang.com/",
                    "map_query": "Phoenix+Hotel+Ha+Giang"
                }
            ],
            "door_to_door_logistics": {
                "primary_transit": "08:30 AM: ARL from Phaya Thai -> BKK Airport. 09:15 AM: Drop suitcase at AIRPORTELs Floor B. 11:55 AM: Flight BKK->HAN (Confirmed). 13:50 PM: Land Noi Bai Airport (HAN). Clear e-visa. 15:30/19:30: Meet Ha Giang Tour representative directly at airport for direct sleeper bus to Ha Giang City.",
                "departure_time": "08:30 AM Sukhon checkout / 11:55 AM Flight",
                "arrival_time": "Late evening Ha Giang City hotel check-in",
                "buffer_time": "Airport pickup avoids traveling 1h into central Hanoi; heads directly north on expressway",
                "tips": "Tour includes direct sleeper pickup at Noi Bai airport terminal, bypassing Hanoi traffic completely."
            },
            "curated_daily_flow": {
                "morning": "ARL to Suvarnabhumi, drop suitcase at AIRPORTELs Floor B basement, board confirmed flight to Hanoi.",
                "afternoon": "Touchdown Noi Bai Airport (13:50). Fast-track e-visa clearance. Relax at airport cafe and rendezvous with Ha Giang tour shuttle.",
                "evening": "Board VIP sleeper cabin bus directly from Hanoi Airport on the highway north to Ha Giang City. Check into tour-included hotel (twin beds) for solid rest before Day 1 of the loop."
            },
            "essential_checklist": [
                "Deposit suitcase at AIRPORTELs BKK Basement; retain receipt",
                "Apply for Vietnam e-Visa approval letter online at least 2 weeks prior",
                "Withdraw 3M-5M VND from VPBank or TPBank ATM (no local ATM fee) at airport"
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

        # --- DAY 3: Ha Giang Loop (Day 1: Bac Sum Pass, Quan Ba & Dong Van) ---
        {
            "day_number": 3,
            "date": "2026-09-13",
            "day_of_week": "Sunday",
            "destination": "Ha Giang Loop: Bac Sum Pass, Quan Ba & Dong Van",
            "phase": "Guys Trip - Vietnam Expedition",
            "phase_short": "Phase 1: Guys Trip",
            "status": "[ACTION REQUIRED - VETTED / UNBOOKED]",
            "status_badge": "UNBOOKED",
            "booking_summary": "Ha Giang 3-Day Tour Day 1 • Easy-Riders & Dong Van Hotel Included",
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
                    "hotel_name": "Dong Van Eco Stone House / Phoenix Dong Van (Included in Tour)",
                    "status": "UNBOOKED_VETTED_OPTION",
                    "room_spec": "Deluxe Twin Room (Two Separate Single Beds)",
                    "critic_score": 9.2,
                    "critic_notes": "Included in 3-day loop package. Private twin room, ensuite bathroom, hot shower, electric heaters.",
                    "price_per_night": "Included in Tour Package",
                    "booking_url": "https://cheershagiang.com/",
                    "map_query": "Dong+Van+Ancient+Town"
                }
            ],
            "door_to_door_logistics": {
                "primary_transit": "08:30 AM: Gear fitting (DOT helmet, knee/elbow armor) at Ha Giang City base. 09:15 AM: Easy-Rider motorcade departs QL4C. Ascend Bac Sum pass, Quan Ba Heaven Gate, Twin Mountains, Tham Ma pass, and Hmong King's Palace. Arrive Dong Van Ancient Town.",
                "departure_time": "08:30 AM Ha Giang Base",
                "arrival_time": "17:30 PM Dong Van Town",
                "buffer_time": "Frequent photo stops and guided visits at cultural sites",
                "tips": "Hotels included in your 3-day tour package. Twin bed rooms confirmed for privacy and comfort."
            },
            "curated_daily_flow": {
                "morning": "Briefing with licensed Easy-Riders. Climb Bac Sum incline to Quan Ba Heaven Gate overlooking misty limestone towers.",
                "afternoon": "Carve through the 9-bend Tham Ma Pass. Explore the 100-year-old opium fortress of the Hmong King Palace in Sa Phin.",
                "evening": "Check into tour hotel in Dong Van Ancient Town (Twin Room). Mountain hotpot dinner and stroll through the ancient stone quarter."
            },
            "essential_checklist": [
                "Book Ha Giang 3D/2N Easy-Rider package with hotel & airport sleeper pickup",
                "Ha Giang Provincial Border Permit ($10 USD / arranged by tour operator)",
                "Full protective gear (DOT helmet + knee/elbow armor)",
                "Bring 3M VND cash for loop expenses (ATMs are rare)"
            ],
            "attached_documents": [],
            "google_maps_links": [
                {"label": "Bac Sum Pass", "url": "https://maps.google.com/?q=Doc+Bac+Sum+Ha+Giang"},
                {"label": "Quan Ba Heaven Gate", "url": "https://maps.google.com/?q=Quan+Ba+Heaven+Gate"},
                {"label": "Dong Van Ancient Town", "url": "https://maps.google.com/?q=Dong+Van+Ancient+Town"}
            ]
        },

        # --- DAY 4: Ha Giang Loop (Day 2: Ma Pi Leng Pass, Tu San Canyon & Du Gia) ---
        {
            "day_number": 4,
            "date": "2026-09-14",
            "day_of_week": "Monday",
            "destination": "Ha Giang Loop: Ma Pi Leng Pass, Tu San Canyon & Du Gia",
            "phase": "Guys Trip - Vietnam Expedition",
            "phase_short": "Phase 1: Guys Trip",
            "status": "[ACTION REQUIRED - VETTED / UNBOOKED]",
            "status_badge": "UNBOOKED",
            "booking_summary": "Ha Giang 3-Day Tour Day 2 • Easy-Riders & Du Gia Hotel Included",
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
                    "hotel_name": "Du Gia Panorama Lodge / Du Gia Waterfall Hotel (Included in Tour)",
                    "status": "UNBOOKED_VETTED_OPTION",
                    "room_spec": "Private Twin Bungalow (Two Separate Beds)",
                    "critic_score": 9.3,
                    "critic_notes": "Included in 3-day loop package. Private twin room overlooking rice terraces and mountain streams.",
                    "price_per_night": "Included in Tour Package",
                    "booking_url": "https://cheershagiang.com/",
                    "map_query": "Du+Gia+Ha+Giang"
                }
            ],
            "door_to_door_logistics": {
                "primary_transit": "08:00 AM: Ride from Dong Van onto Ma Pi Leng Pass. Stop at monumental viewpoint. 10:30 AM: Descend to Nho Que River for Tu San Canyon motorboat cruise. 13:00 PM: Ride through Meo Vac and across mountain ridges into Du Gia Valley.",
                "departure_time": "08:00 AM Dong Van",
                "arrival_time": "17:00 PM Du Gia Valley",
                "buffer_time": "1.5 hrs for Tu San Chasm canyon boat cruise",
                "tips": "Highlight of the entire loop. Emerald waters of Nho Que river between 1,000m sheer limestone cliffs."
            },
            "curated_daily_flow": {
                "morning": "Conquer Ma Pi Leng Pass ('The King of Mountain Passes'). Photograph the panoramic vista over the emerald Nho Que chasm.",
                "afternoon": "Motorboat cruise through Tu San Canyon beneath towering limestone walls. Ride the M-Pau pass toward Du Gia.",
                "evening": "Check into private twin bungalow in Du Gia Valley. Family feast with Easy-Riders (grilled pork, bamboo shoots, and 'happy water' corn wine toasts)."
            },
            "essential_checklist": [
                "Full battery charge on phone / camera for Ma Pi Leng panoramas",
                "Swimwear under trekking clothes for Du Gia stream dip"
            ],
            "attached_documents": [],
            "google_maps_links": [
                {"label": "Ma Pi Leng Pass Monument", "url": "https://maps.google.com/?q=Ma+Pi+Leng+Pass"},
                {"label": "Tu San Canyon Dock", "url": "https://maps.google.com/?q=Nho+Que+River+Boat+Dock"},
                {"label": "Du Gia Valley", "url": "https://maps.google.com/?q=Du+Gia+Ha+Giang"}
            ]
        },

        # --- DAY 5: Ha Giang Loop (Day 3: Du Gia to Base) -> Sleeper to Sa Pa Town Hotel ---
        {
            "day_number": 5,
            "date": "2026-09-15",
            "day_of_week": "Tuesday",
            "destination": "Du Gia -> Ha Giang City -> Sleeper to Sa Pa Town Hotel",
            "phase": "Guys Trip - Vietnam Expedition",
            "phase_short": "Phase 1: Guys Trip",
            "status": "[ACTION REQUIRED - VETTED / UNBOOKED]",
            "status_badge": "UNBOOKED",
            "booking_summary": "Ha Giang Loop Finish • Evening Sleeper to Sa Pa • Sa Pa Town Hotel (1 Night Sleep)",
            "weather_radar": {
                "temp_range": "17°C - 24°C",
                "condition": "Cool alpine mist in Sa Pa, crisp evening air",
                "precipitation_pct": "30%",
                "humidity": "82%",
                "attire_advice": "Fleece jacket, thermal mid-layer, sturdy hiking shoes for Sa Pa hills"
            },
            "luggage_action": "Reunite with main 55L clamshell pack at Ha Giang base camp; load onto sleeper bus to Sa Pa.",
            "accommodation_matrix": [
                {
                    "hotel_name": "BB Hotel Sapa (Sa Pa Town Center)",
                    "status": "UNBOOKED_VETTED_OPTION",
                    "room_spec": "Deluxe Twin Room (Two Separate Beds)",
                    "critic_score": 9.3,
                    "critic_notes": "1 Night decompression sleep in Sa Pa town center before the 2-day trek. Heated rooms, rainfall shower, right by town square.",
                    "price_per_night": "Est. $65 USD / 1,650,000 VND",
                    "booking_url": "https://bbhotelsresorts.com/",
                    "map_query": "BB+Hotel+Sapa"
                },
                {
                    "hotel_name": "Pao's Sapa Leisure Hotel",
                    "status": "UNBOOKED_VETTED_ALTERNATIVE",
                    "room_spec": "Deluxe Twin Room with Valley View (Two Beds)",
                    "critic_score": 9.2,
                    "critic_notes": "5-star hillside retreat overlooking Muong Hoa Valley. Heated indoor pool, stunning balcony views.",
                    "price_per_night": "Est. $85 USD / 2,150,000 VND",
                    "booking_url": "https://paoshotel.com/",
                    "map_query": "Paos+Sapa+Leisure+Hotel"
                }
            ],
            "door_to_door_logistics": {
                "primary_transit": "08:00 AM: Du Gia waterfall swim & Lung Tam linen village. 15:30 PM: Finish loop in Ha Giang City basecamp. Shower and repack. 18:30 PM: Direct VIP Sleeper Bus Ha Giang -> Sa Pa town (5 hrs, arr ~23:30 PM). Check into Sa Pa hotel for 1 night.",
                "departure_time": "18:30 PM Ha Giang City",
                "arrival_time": "23:30 PM Sa Pa Town Hotel",
                "buffer_time": "3 hours in Ha Giang basecamp for hot shower and packing",
                "tips": "User mandated: sleep 1 night in Sa Pa town hotel to fully recharge in a real bed before starting the 2-day guided trek!"
            },
            "curated_daily_flow": {
                "morning": "Dip in crystal-clear Du Gia waterfall. Visit Lung Tam traditional hemp-weaving village.",
                "afternoon": "Ride back to Ha Giang City basecamp. Return riding gear, hot shower, consolidate into 55L backpack.",
                "evening": "Board direct evening sleeper bus to Sa Pa town. Check into Sa Pa town hotel (Deluxe Twin Room). Deep, restful sleep in a real bed before the 2-day trek."
            },
            "essential_checklist": [
                "Book Ha Giang -> Sa Pa sleeper bus (via 12Go Asia or local operator)",
                "Reserve 1 night at BB Hotel Sapa for deep sleep before the trek"
            ],
            "attached_documents": [],
            "google_maps_links": [
                {"label": "Du Gia Waterfall", "url": "https://maps.google.com/?q=Du+Gia+Waterfall"},
                {"label": "Sa Pa Town Square", "url": "https://maps.google.com/?q=Sapa+Town+Square"},
                {"label": "BB Hotel Sapa", "url": "https://maps.google.com/?q=BB+Hotel+Sapa"}
            ]
        },

        # --- DAY 6: Sa Pa: 2-Day Guided Trek with Mamas (Day 1: Muong Hoa to Ta Van Homestay) ---
        {
            "day_number": 6,
            "date": "2026-09-16",
            "day_of_week": "Wednesday",
            "destination": "Sa Pa: 2-Day Guided Trek with Mamas (Day 1: Muong Hoa to Ta Van)",
            "phase": "Guys Trip - Vietnam Expedition",
            "phase_short": "Phase 1: Guys Trip",
            "status": "[ACTION REQUIRED - VETTED / UNBOOKED]",
            "status_badge": "UNBOOKED",
            "booking_summary": "2-Day Trek with Hmong Mamas • Stay at Mama's Village Homestay & Eat Mama's Food",
            "weather_radar": {
                "temp_range": "18°C - 25°C",
                "condition": "Clear mountain morning, dramatic afternoon cloud rolling over terraces",
                "precipitation_pct": "20%",
                "humidity": "75%",
                "attire_advice": "Trekking boots/shoes with good lugs, moisture-wicking shirt, sun hat, daypack"
            },
            "luggage_action": "Leave main 55L pack safely stored; carry light daypack with overnight essentials to the homestay.",
            "accommodation_matrix": [
                {
                    "hotel_name": "Mama's Traditional Village Homestay (Ta Van / Hau Thao Village)",
                    "status": "UNBOOKED_VETTED_OPTION",
                    "room_spec": "Authentic Wooden Stilt Homestay (Separate Twin Sleeping Mattresses with Mosquito Net)",
                    "critic_score": 9.6,
                    "critic_notes": "Authentic local minority homestay with the Mama and her family. Hearty homecooked meals, peaceful mountain atmosphere, woodfire hearth.",
                    "price_per_night": "Included in 2-Day Trek Package (~$40-$50 USD / 1M-1.2M VND per person with all meals)",
                    "booking_url": "https://sapasisters.com/",
                    "map_query": "Ta+Van+Village+Sapa"
                }
            ],
            "door_to_door_logistics": {
                "primary_transit": "09:00 AM: Meet local Black Hmong Mama guide at Sa Pa hotel. 12 km guided trek on foot through off-the-beaten-track ridge trails, Y Linh Ho, Lao Chai golden terraces into Ta Van village. Check in to Mama's family homestay.",
                "departure_time": "09:00 AM Sa Pa hotel on foot",
                "arrival_time": "15:30 PM Ta Van Mama's Homestay",
                "buffer_time": "Unrushed village trail stops, stream crossings, and panoramic valley overlooks",
                "tips": "User requested: Guided 2-day trek staying with Mamas and eating their food. Authentic ethnic immersion away from tourist buses."
            },
            "curated_daily_flow": {
                "morning": "Hearty breakfast in Sa Pa town. Meet your local Hmong Mama guide. Hike out of town along high mountain ridge trails above Muong Hoa Valley.",
                "afternoon": "Descend through golden terraced rice fields of Y Linh Ho and Lao Chai. Learn about traditional indigo fabric dyeing and mountain plants from the Mama.",
                "evening": "Arrive at Mama's family stilt wooden homestay in Ta Van village. Cook and eat an authentic homecooked family feast with the Mama (roasted free-range chicken, bamboo shoots, wild mountain greens, spring rolls, and happy water corn wine by the open hearth). Sleep in authentic village twin beds under warm quilts."
            },
            "essential_checklist": [
                "Book 2-Day Trek with local Hmong Mama guide (Sapa Sisters or independent Mama)",
                "Support local guide: 300k-500k VND customary tip for full 2-day trek",
                "Pack light daypack with overnight clothes and toiletries"
            ],
            "attached_documents": [],
            "google_maps_links": [
                {"label": "Muong Hoa Valley Trailhead", "url": "https://maps.google.com/?q=Muong+Hoa+Valley+Sapa"},
                {"label": "Lao Chai Village", "url": "https://maps.google.com/?q=Lao+Chai+Village+Sapa"},
                {"label": "Ta Van Village", "url": "https://maps.google.com/?q=Ta+Van+Village+Sapa"}
            ]
        },

        # --- DAY 7: Sa Pa: 2-Day Trek with Mamas (Day 2) -> Direct VIP Coach to Ninh Binh ---
        {
            "day_number": 7,
            "date": "2026-09-17",
            "day_of_week": "Thursday",
            "destination": "Sa Pa: 2-Day Trek with Mamas (Day 2) -> Direct VIP Coach to Ninh Binh",
            "phase": "Guys Trip - Vietnam Expedition",
            "phase_short": "Phase 1: Guys Trip",
            "status": "[ACTION REQUIRED - VETTED / UNBOOKED]",
            "status_badge": "UNBOOKED",
            "booking_summary": "Sa Pa Trek Day 2 • Farewell Lunch with Mama • Direct Coach to Ninh Binh (Sequence A)",
            "weather_radar": {
                "temp_range": "24°C - 31°C",
                "condition": "Warm sunshine over karst river valleys, gentle rural breeze in Ninh Binh",
                "precipitation_pct": "20%",
                "humidity": "74%",
                "attire_advice": "Comfortable travel clothes for bus, casual shorts and cycling sandals for evening"
            },
            "luggage_action": "55L backpacks ride in express coach lower cargo bay; direct drop at Tam Coc resort doorstep.",
            "accommodation_matrix": [
                {
                    "hotel_name": "Tam Coc Garden Resort",
                    "status": "UNBOOKED_VETTED_OPTION",
                    "room_spec": "Premium Twin Bungalow (Two Separate Beds)",
                    "critic_score": 9.5,
                    "critic_notes": "Vetted recommendation. Nestled among rice paddies and karst pinnacles. Complimentary bicycles, zero road noise, exceptional organic dining.",
                    "price_per_night": "Est. $140 USD / 3,550,000 VND",
                    "booking_url": "https://tamcocgarden.com/",
                    "map_query": "Tam+Coc+Garden+Resort+Ninh+Binh"
                },
                {
                    "hotel_name": "Ninh Binh Hidden Charm Hotel & Resort",
                    "status": "UNBOOKED_VETTED_ALTERNATIVE",
                    "room_spec": "Superior Twin Room (Two Single Beds)",
                    "critic_score": 9.2,
                    "critic_notes": "Boutique luxury resort 5 minutes from Tam Coc boat pier, large swimming pool, peaceful garden setting.",
                    "price_per_night": "Est. $75 USD / 1,900,000 VND",
                    "booking_url": "https://hiddencharmresort.com/",
                    "map_query": "Ninh+Binh+Hidden+Charm+Hotel"
                }
            ],
            "door_to_door_logistics": {
                "primary_transit": "09:00 AM: Day 2 guided trek through giant bamboo forests & Giang Ta Chai waterfall. 13:30 PM: Farewell lunch with Mama. 14:00 PM: Vehicle shuttle back to Sa Pa town center to shower and collect bags. 15:30 PM: Direct VIP Express Highway Coach Sa Pa -> Ninh Binh (Tam Coc) (6 hrs, arr 21:30 PM).",
                "departure_time": "09:00 AM Ta Van Homestay / 15:30 PM Sa Pa coach",
                "arrival_time": "21:30 PM Tam Coc Garden Resort",
                "buffer_time": "1.5 hours in Sa Pa town to shower, pack, and board express coach",
                "tips": "Direct highway coach to Ninh Binh avoids the 10-hour slog to Cat Ba, keeping Sequence A fast and smooth!"
            },
            "curated_daily_flow": {
                "morning": "Wake up to mist rising over the rice terraces. Homemade banana pancakes and mountain tea with the Mama. Trek through dense giant bamboo forests and suspension bridges.",
                "afternoon": "Visit Giang Ta Chai waterfall and Red Dao village. Enjoy a farewell homecooked lunch with Mama. Transfer back to Sa Pa town to shower and collect stored bags.",
                "evening": "Board comfortable VIP express highway coach speeding direct to Ninh Binh (Tam Coc). Check into Tam Coc Garden Resort surrounded by karst pinnacles."
            },
            "essential_checklist": [
                "Book Sa Pa to Ninh Binh direct express bus (The Long Travel / Truly)",
                "Reserve 2 nights in Tam Coc with Twin Bed configuration"
            ],
            "attached_documents": [],
            "google_maps_links": [
                {"label": "Tam Coc Garden Resort", "url": "https://maps.google.com/?q=Tam+Coc+Garden+Resort+Ninh+Binh"},
                {"label": "Bich Dong Pagoda", "url": "https://maps.google.com/?q=Bich+Dong+Pagoda+Ninh+Binh"}
            ]
        },

        # --- DAY 8: Ninh Binh Karst Exploration ---
        {
            "day_number": 8,
            "date": "2026-09-18",
            "day_of_week": "Friday",
            "destination": "Ninh Binh: Trang An UNESCO Karst Boat & Mua Cave Peak",
            "phase": "Guys Trip - Vietnam Expedition",
            "phase_short": "Phase 1: Guys Trip",
            "status": "[ACTION REQUIRED - VETTED / UNBOOKED]",
            "status_badge": "UNBOOKED",
            "booking_summary": "Trang An boat tour & Mua Cave entry on-site",
            "weather_radar": {
                "temp_range": "24°C - 31°C",
                "condition": "Bright morning sun, calm glassy waters, pleasant afternoon breeze",
                "precipitation_pct": "15%",
                "humidity": "72%",
                "attire_advice": "Breathable athletic wear, sun hat, grippy sneakers for 486 stone steps at Mua Cave, sunglasses"
            },
            "luggage_action": "Packs remain safely in Tam Coc bungalow; small dry-bag for boat trip.",
            "accommodation_matrix": [
                {
                    "hotel_name": "Tam Coc Garden Resort",
                    "status": "UNBOOKED_VETTED_OPTION",
                    "room_spec": "Premium Twin Bungalow (Two Separate Beds)",
                    "critic_score": 9.5,
                    "critic_notes": "Second night at this serene sanctuary. Superb breakfast and peaceful cycling paths.",
                    "price_per_night": "Est. $140 USD / 3,550,000 VND",
                    "booking_url": "https://tamcocgarden.com/",
                    "map_query": "Tam+Coc+Garden+Resort+Ninh+Binh"
                },
                {
                    "hotel_name": "Emeralda Resort Ninh Binh",
                    "status": "UNBOOKED_VETTED_ALTERNATIVE",
                    "room_spec": "Superior Twin Room (Two Single Beds)",
                    "critic_score": 9.1,
                    "critic_notes": "Traditional Tonkin village style near Van Long wetland, huge spa and lush gardens.",
                    "price_per_night": "Est. $90 USD / 2,300,000 VND",
                    "booking_url": "https://emeraldaresort.com/",
                    "map_query": "Emeralda+Resort+Ninh+Binh"
                }
            ],
            "door_to_door_logistics": {
                "primary_transit": "07:15 AM short 15-min taxi from hotel to Trang An UNESCO Boat Pier. 13:00 PM: 10-min taxi to Hang Mua. Return to resort by 17:00 PM.",
                "departure_time": "07:15 AM hotel",
                "arrival_time": "17:00 PM hotel",
                "buffer_time": "Arrive at Trang An by 07:30 AM to beat all tour buses from Hanoi",
                "tips": "Select Trang An Boat Route 3 (passes through 1,000m Dot Cave and Dia Linh Cave with scenic temple stops)."
            },
            "curated_daily_flow": {
                "morning": "07:30 AM: Glide through subterranean karst water caves on a traditional wooden sampan rowed by local boatwomen. Pure tranquility before crowds.",
                "afternoon": "Climb the iconic 486 dragon-spine stone steps to the peak of Hang Mua for panoramic 360-degree views of the Ngo Dong river valley and karst towers.",
                "evening": "Cycling through lotus ponds as twilight sets. Dinner in Tam Coc village, tasting crispy spring rolls and cold Bia Hanoi."
            },
            "essential_checklist": [
                "Start Trang An boat at 07:30 sharp to experience empty water caves",
                "Water bottle and sunscreen for Hang Mua dragon peak climb"
            ],
            "attached_documents": [],
            "google_maps_links": [
                {"label": "Trang An Boat Pier", "url": "https://maps.google.com/?q=Trang+An+Boat+Tour+Ninh+Binh"},
                {"label": "Hang Mua Cave Viewpoint", "url": "https://maps.google.com/?q=Hang+Mua+Ninh+Binh"}
            ]
        },

        # --- DAY 9: Ninh Binh -> Cat Ba Island (Short 2.5h Transit) ---
        {
            "day_number": 9,
            "date": "2026-09-19",
            "day_of_week": "Saturday",
            "destination": "Ninh Binh -> Cat Ba Island (Lan Ha Bay)",
            "phase": "Guys Trip - Vietnam Expedition",
            "phase_short": "Phase 1: Guys Trip",
            "status": "[ACTION REQUIRED - VETTED / UNBOOKED]",
            "status_badge": "UNBOOKED",
            "booking_summary": "Ninh Binh to Cat Ba express coach/ferry & island resort unbooked",
            "weather_radar": {
                "temp_range": "26°C - 32°C",
                "condition": "Sunny coastal breeze, calm turquoise waters in Lan Ha Bay",
                "precipitation_pct": "20%",
                "humidity": "78%",
                "attire_advice": "Linen shirts, board shorts, flip-flops, sunglasses, waterproof dry-bag"
            },
            "luggage_action": "55L clamshell backpack loaded onto express coach; transferred onto speedboat directly to Cat Ba hotel.",
            "accommodation_matrix": [
                {
                    "hotel_name": "Hôtel Perle d'Orient Cat Ba - MGallery",
                    "status": "UNBOOKED_VETTED_OPTION",
                    "room_spec": "Classic Twin Bay View (Two Single Beds)",
                    "critic_score": 9.3,
                    "critic_notes": "Vetted recommendation. Cliffside at Cat Co 3 beach overlooking Lan Ha Bay. Indochine design, private beach, zero noise, infinity pool.",
                    "price_per_night": "Est. $125 USD / 3,180,000 VND",
                    "booking_url": "https://all.accor.com/hotel/B557/index.en.shtml",
                    "map_query": "Hotel+Perle+d+Orient+Cat+Ba"
                },
                {
                    "hotel_name": "Cat Ba Eco Lodge",
                    "status": "UNBOOKED_VETTED_ALTERNATIVE",
                    "room_spec": "Superior Twin Mountain View (Two Beds)",
                    "critic_score": 9.0,
                    "critic_notes": "Nestled in jungle valley at edge of National Park, tranquil swimming pool, complete seclusion from town.",
                    "price_per_night": "Est. $55 USD / 1,400,000 VND",
                    "booking_url": "https://catba-ecolodge.com/",
                    "map_query": "Cat+Ba+Eco+Lodge"
                }
            ],
            "door_to_door_logistics": {
                "primary_transit": "09:00 AM: Daichi / Good Morning Cat Ba direct coach from Tam Coc hotel -> Highway -> Ferry channel / speedboat -> Cat Ba Island hotel doorstep (Only 2.5 to 3 hrs total, arr 12:00 PM). Fast, seamless, zero stress!",
                "departure_time": "09:00 AM Tam Coc",
                "arrival_time": "12:00 PM Cat Ba hotel",
                "buffer_time": "Combined coach + ferry ticket transfers luggage automatically across the water",
                "tips": "Book Cat Ba Express or Daichi bus via hotel reception or 12Go Asia."
            },
            "curated_daily_flow": {
                "morning": "Enjoy breakfast by the rice paddies. Board express coach for a quick 2.5-hour hop across the sea bridge and ferry to Cat Ba Island.",
                "afternoon": "Check into Hôtel Perle d'Orient at Cat Co 3 beach. Swim in the azure waters or lounge at the cliffside pool.",
                "evening": "Trek up to Cannon Fort peak for breathtaking sunset views over the thousands of karst towers of Lan Ha Bay. Fresh grilled seafood dinner in town."
            },
            "essential_checklist": [
                "Book Ninh Binh to Cat Ba direct express bus (Daichi / Cat Ba Express)",
                "Reserve 3 nights in Cat Ba with Twin Bed room spec"
            ],
            "attached_documents": [],
            "google_maps_links": [
                {"label": "Hôtel Perle d'Orient Cat Ba", "url": "https://maps.google.com/?q=Hotel+Perle+d+Orient+Cat+Ba"},
                {"label": "Cannon Fort Cat Ba", "url": "https://maps.google.com/?q=Cannon+Fort+Cat+Ba"}
            ]
        },

        # --- DAY 10: Lan Ha Bay & Ba Trai Dao Kayak Cruise ---
        {
            "day_number": 10,
            "date": "2026-09-20",
            "day_of_week": "Sunday",
            "destination": "Lan Ha Bay: Ba Trai Dao Archways & Hidden Lagoons",
            "phase": "Guys Trip - Vietnam Expedition",
            "phase_short": "Phase 1: Guys Trip",
            "status": "[ACTION REQUIRED - VETTED / UNBOOKED]",
            "status_badge": "UNBOOKED",
            "booking_summary": "Lan Ha Bay traditional junk boat & kayak tour unbooked",
            "weather_radar": {
                "temp_range": "27°C - 33°C",
                "condition": "Brilliant sunshine over emerald bay, calm sea swell, zero storm risk",
                "precipitation_pct": "10%",
                "humidity": "76%",
                "attire_advice": "Swimwear, quick-dry rashguard, water shoes, polarized sunglasses, 10L dry-bag"
            },
            "luggage_action": "55L packs stay in resort; only take 10L dry-bag on the boat.",
            "accommodation_matrix": [
                {
                    "hotel_name": "Hôtel Perle d'Orient Cat Ba - MGallery",
                    "status": "UNBOOKED_VETTED_OPTION",
                    "room_spec": "Classic Twin Bay View (Two Single Beds)",
                    "critic_score": 9.3,
                    "critic_notes": "Second night at Cat Co 3 private cove. Indochine elegance, ocean sound from balcony.",
                    "price_per_night": "Est. $125 USD / 3,180,000 VND",
                    "booking_url": "https://all.accor.com/hotel/B557/index.en.shtml",
                    "map_query": "Hotel+Perle+d+Orient+Cat+Ba"
                },
                {
                    "hotel_name": "Flamingo Cat Ba Beach Resort",
                    "status": "UNBOOKED_VETTED_ALTERNATIVE",
                    "room_spec": "Deluxe Ocean View Twin (Two Beds)",
                    "critic_score": 8.9,
                    "critic_notes": "Modern beachfront mega-resort on Cat Co 1, skywalks and rooftop hot tubs.",
                    "price_per_night": "Est. $110 USD / 2,800,000 VND",
                    "booking_url": "https://flamingoresorts.vn/catba/",
                    "map_query": "Flamingo+Cat+Ba+Resort"
                }
            ],
            "door_to_door_logistics": {
                "primary_transit": "08:00 AM hotel pickup to Ben Beo Pier (10 mins). Board traditional wooden sailing boat through Lan Ha Bay. Kayak into Dark & Bright Caves and swim at Ba Trai Dao. Return to pier by 16:30 PM.",
                "departure_time": "08:00 AM hotel",
                "arrival_time": "16:30 PM Ben Beo Pier",
                "buffer_time": "Private/small-group cruise avoids commercial Halong Bay routes",
                "tips": "Lan Ha Bay is far cleaner, quieter, and more dramatic than overcrowded Ha Long Bay."
            },
            "curated_daily_flow": {
                "morning": "Board boat at Ben Beo pier. Cruise through Cai Beo floating fishing village—one of the oldest in Asia.",
                "afternoon": "Kayak through limestone archways into secluded lagoon chambers. Anchor at Ba Trai Dao (Three Peaches) for swimming off pristine deserted beaches. Fresh seafood lunch on deck.",
                "evening": "Return to Cat Ba. Sunset drinks at Perle d'Orient rooftop bar, followed by dinner at a local harbor restaurant."
            },
            "essential_checklist": [
                "Book small-group Lan Ha Bay day cruise (Cat Ba Ventures or Blue Swimmer)",
                "Waterproof dry-bag and camera float strap for kayaking"
            ],
            "attached_documents": [],
            "google_maps_links": [
                {"label": "Ben Beo Boat Pier", "url": "https://maps.google.com/?q=Ben+Beo+Pier+Cat+Ba"},
                {"label": "Ba Trai Dao Islets", "url": "https://maps.google.com/?q=Ba+Trai+Dao+Beach+Lan+Ha+Bay"}
            ]
        },

        # --- DAY 11: Cat Ba National Park & Hidden Coves ---
        {
            "day_number": 11,
            "date": "2026-09-21",
            "day_of_week": "Monday",
            "destination": "Cat Ba Island: Jungle Trek, Hospital Cave & Sunset Cove",
            "phase": "Guys Trip - Vietnam Expedition",
            "phase_short": "Phase 1: Guys Trip",
            "status": "[ACTION REQUIRED - VETTED / UNBOOKED]",
            "status_badge": "UNBOOKED",
            "booking_summary": "Cat Ba third night & park entry on-site",
            "weather_radar": {
                "temp_range": "26°C - 32°C",
                "condition": "Warm tropical sun with coastal afternoon breeze",
                "precipitation_pct": "20%",
                "humidity": "75%",
                "attire_advice": "Trekking shorts, trail runners for park hike, swimwear for afternoon cove swim"
            },
            "luggage_action": "Packs remain in resort bungalow.",
            "accommodation_matrix": [
                {
                    "hotel_name": "Hôtel Perle d'Orient Cat Ba - MGallery",
                    "status": "UNBOOKED_VETTED_OPTION",
                    "room_spec": "Classic Twin Bay View (Two Single Beds)",
                    "critic_score": 9.3,
                    "critic_notes": "Final night on Cat Ba. Quiet, refined, pristine views.",
                    "price_per_night": "Est. $125 USD / 3,180,000 VND",
                    "booking_url": "https://all.accor.com/hotel/B557/index.en.shtml",
                    "map_query": "Hotel+Perle+d+Orient+Cat+Ba"
                },
                {
                    "hotel_name": "Secret Garden Cat Ba",
                    "status": "UNBOOKED_VETTED_ALTERNATIVE",
                    "room_spec": "Deluxe Twin Mountain View (Two Beds)",
                    "critic_score": 8.8,
                    "critic_notes": "Charming garden property, quiet atmosphere, friendly local hosts.",
                    "price_per_night": "Est. $45 USD / 1,150,000 VND",
                    "booking_url": "https://secretgardencatba.com/",
                    "map_query": "Secret+Garden+Cat+Ba"
                }
            ],
            "door_to_door_logistics": {
                "primary_transit": "Rent two automatic scooters or hire an open-air electric buggy to Cat Ba National Park (15km, 25 mins). Trek to Ngu Lam Peak. 5-min ride to historic Hospital Cave. Return to town.",
                "departure_time": "08:30 AM resort",
                "arrival_time": "15:00 PM return to beach",
                "buffer_time": "Island roads are quiet, paved, and scenic with zero heavy traffic",
                "tips": "Hospital Cave was a bomb-proof military hospital built inside a karst cavern during the American War."
            },
            "curated_daily_flow": {
                "morning": "Hike the rainforest trail to Ngu Lam Peak for an amphitheater view over the emerald canopy and jagged karst spikes.",
                "afternoon": "Explore the 17-room secret subterranean complex of Hospital Cave. Ride back to Cat Co 3 beach for relaxation and cold coconuts.",
                "evening": "Dinner at Casa Bonita restaurant (fresh fish steamed with lemongrass, morning glory with garlic, passionfruit mocktails)."
            },
            "essential_checklist": [
                "Confirm tomorrow morning express bus ticket back to Hanoi Old Quarter",
                "Repack 55L backpacks for return to Hanoi"
            ],
            "attached_documents": [],
            "google_maps_links": [
                {"label": "Cat Ba National Park", "url": "https://maps.google.com/?q=Cat+Ba+National+Park"},
                {"label": "Hospital Cave Cat Ba", "url": "https://maps.google.com/?q=Hospital+Cave+Cat+Ba"}
            ]
        },

        # --- DAY 12: Cat Ba Island -> Hanoi Old Quarter ---
        {
            "day_number": 12,
            "date": "2026-09-22",
            "day_of_week": "Tuesday",
            "destination": "Cat Ba Island -> Hanoi Old Quarter Base",
            "phase": "Guys Trip - Vietnam Expedition",
            "phase_short": "Phase 1: Guys Trip",
            "status": "[ACTION REQUIRED - VETTED / UNBOOKED]",
            "status_badge": "UNBOOKED",
            "booking_summary": "Cat Ba to Hanoi express coach & Old Quarter boutique hotel unbooked",
            "weather_radar": {
                "temp_range": "25°C - 32°C",
                "condition": "Balmy late-monsoon warmth in the capital, clear evening skies",
                "precipitation_pct": "25%",
                "humidity": "78%",
                "attire_advice": "Casual street clothes, comfortable walking sneakers for night market and street food exploration"
            },
            "luggage_action": "55L backpacks travel in coach luggage hold; drop-off at Hanoi hotel.",
            "accommodation_matrix": [
                {
                    "hotel_name": "La Siesta Classic Ma May (Hanoi Old Quarter)",
                    "status": "UNBOOKED_VETTED_OPTION",
                    "room_spec": "Deluxe Twin Room (Two Separate Beds)",
                    "critic_score": 9.4,
                    "critic_notes": "Vetted recommendation. The gold standard for boutique hospitality in Hanoi Old Quarter. Acoustic soundproofing, prime culinary location.",
                    "price_per_night": "Est. $85 USD / 2,150,000 VND",
                    "booking_url": "https://lasiestahotels.vn/mamay/",
                    "map_query": "La+Siesta+Classic+Ma+May+Hanoi"
                },
                {
                    "hotel_name": "Peridot Grand Luxury Hotel",
                    "status": "UNBOOKED_VETTED_ALTERNATIVE",
                    "room_spec": "Grand Deluxe Twin (Two Single Beds)",
                    "critic_score": 9.3,
                    "critic_notes": "High-end comfort, rooftop cocktail lounge, quiet Old Quarter side street.",
                    "price_per_night": "Est. $110 USD / 2,800,000 VND",
                    "booking_url": "https://peridotgrandhotel.com/",
                    "map_query": "Peridot+Grand+Hotel+Hanoi"
                }
            ],
            "door_to_door_logistics": {
                "primary_transit": "09:00 AM: Cat Ba Express coach from resort doorstep -> Speedboat to Hai Phong -> Express Highway to Hanoi Old Quarter (Only 2.5 hrs flat, arr 11:30 AM). Fast, modern, air-conditioned.",
                "departure_time": "09:00 AM Cat Ba resort",
                "arrival_time": "11:30 AM Hanoi Old Quarter hotel",
                "buffer_time": "Highway 5B connection is rapid and avoids city bottlenecks until Hanoi ring road",
                "tips": "Cat Ba Express drops right on Ma May street directly in front of La Siesta!"
            },
            "curated_daily_flow": {
                "morning": "Scenic ferry crossing away from Cat Ba. Fast highway cruise back to Hanoi. Arrive at hotel before noon.",
                "afternoon": "Lunch at Bun Cha Dac Kim on Hang Manh. Stroll through the French Quarter, Opera House, and St. Joseph Cathedral.",
                "evening": "Night food market crawl: sizzling Banh Xeo, fresh rice rolls at Banh Cuon Gia An, and craft IPAs on the rooftop of Standing Bar overlooking Truc Bach lake."
            },
            "essential_checklist": [
                "Book Cat Ba to Hanoi express coach ticket (Cat Ba Express)",
                "Reserve 2 nights at La Siesta Classic Ma May with Twin Beds"
            ],
            "attached_documents": [],
            "google_maps_links": [
                {"label": "La Siesta Classic Ma May", "url": "https://maps.google.com/?q=La+Siesta+Classic+Ma+May+Hanoi"},
                {"label": "Bun Cha Dac Kim", "url": "https://maps.google.com/?q=Bun+Cha+Dac+Kim+Hang+Manh"}
            ]
        },

        # --- DAY 13: Hanoi Culinary Finale & Repack ---
        {
            "day_number": 13,
            "date": "2026-09-23",
            "day_of_week": "Wednesday",
            "destination": "Hanoi: Culinary Tour, Craft Beer & Expedition Finale",
            "phase": "Guys Trip - Vietnam Expedition",
            "phase_short": "Phase 1: Guys Trip",
            "status": "[ACTION REQUIRED - VETTED / UNBOOKED]",
            "status_badge": "UNBOOKED",
            "booking_summary": "Final night in Hanoi Old Quarter before transition day",
            "weather_radar": {
                "temp_range": "25°C - 32°C",
                "condition": "Pleasant autumn breeze, warm sun over the tree-lined boulevards",
                "precipitation_pct": "20%",
                "humidity": "75%",
                "attire_advice": "Casual street clothes, walking trainers, sun hat"
            },
            "luggage_action": "Repack 55L backpacks tonight for tomorrow's international flight HAN -> BKK. Verify all souvenirs and dirty laundry packed.",
            "accommodation_matrix": [
                {
                    "hotel_name": "La Siesta Classic Ma May (Hanoi Old Quarter)",
                    "status": "UNBOOKED_VETTED_OPTION",
                    "room_spec": "Deluxe Twin Room (Two Separate Beds)",
                    "critic_score": 9.4,
                    "critic_notes": "Second night at La Siesta. Enjoy late checkout arrangements before flight tomorrow.",
                    "price_per_night": "Est. $85 USD / 2,150,000 VND",
                    "booking_url": "https://lasiestahotels.vn/mamay/",
                    "map_query": "La+Siesta+Classic+Ma+May+Hanoi"
                },
                {
                    "hotel_name": "The Chi Boutique Hotel Hanoi",
                    "status": "UNBOOKED_VETTED_ALTERNATIVE",
                    "room_spec": "Deluxe Twin Room (Two Beds)",
                    "critic_score": 9.0,
                    "critic_notes": "Steps from St. Joseph Cathedral, artistic boutique design, vibrant street life.",
                    "price_per_night": "Est. $75 USD / 1,900,000 VND",
                    "booking_url": "https://thechihotel.com/",
                    "map_query": "The+Chi+Boutique+Hotel+Hanoi"
                }
            ],
            "door_to_door_logistics": {
                "primary_transit": "Walkable Old Quarter exploration. Grab or traditional cyclo for cross-city hops to Temple of Literature and West Lake.",
                "departure_time": "Flexible leisurely schedule",
                "arrival_time": "Evening packing session",
                "buffer_time": "Pre-flight prep day with zero tight deadlines",
                "tips": "Try authentic egg coffee at Cafe Giang (39 Nguyen Huu Huan)—the birthplace of Vietnamese egg coffee since 1946."
            },
            "curated_daily_flow": {
                "morning": "Sip velvety egg coffee at Cafe Giang. Walk the leafy perimeter of Hoan Kiem Lake.",
                "afternoon": "Visit the serene 11th-century Temple of Literature and Vietnam National Museum of Fine Arts. Sip jasmine tea in ancient courtyard.",
                "evening": "Celebratory Guys Trip finale dinner: sizzled turmeric catfish with dill at Cha Ca Thang Long, followed by craft beer flight at Pasteur Street Brewing Co."
            },
            "essential_checklist": [
                "Book private airport transfer to Noi Bai Airport for 09:45 AM tomorrow",
                "Check-in online 24h prior for flight HAN -> BKK (Order: 1145-554-179)",
                "Confirm AIRPORTELs storage receipt is accessible on phone for BKK Floor B retrieval"
            ],
            "attached_documents": [],
            "google_maps_links": [
                {"label": "Cafe Giang Egg Coffee", "url": "https://maps.google.com/?q=Cafe+Giang+Nguyen+Huu+Huan"},
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
            "booking_summary": "Flight HAN->BKK Confirmed (Order: 1145-554-179, arr 14:45) • BKK Floor B Suitcase Retrieval • Recommended PG 177/181 (19:30-20:00)",
            "weather_radar": {
                "temp_range": "26°C - 32°C",
                "condition": "Balmy tropical sun over Gulf of Thailand, balmy coastal evening",
                "precipitation_pct": "20%",
                "humidity": "75%",
                "attire_advice": "Transition from trekking clothes to chic island resort attire: linen shirt, tailored shorts"
            },
            "luggage_action": "RETRIEVAL ACTION: Upon landing at BKK (14:45), proceed to Airport Rail Link level (Floor B) and retrieve checked suitcase from AIRPORTELs locker. Reunite with girlfriend at arrivals hall with all gear ready for the South!",
            "flight_connection_risk": {
                "hanoi_arrival": "14:45 PM at BKK Suvarnabhumi (Mytrip Order: 1145-554-179)",
                "suitcase_pickup": "Floor B AIRPORTELs (retrieval buffer: 15:45 - 16:15 PM)",
                "girlfriend_meeting": "Suvarnabhumi Arrival Hall Floor 2 (16:30 PM)",
                "pg169_warning": "Bangkok Airways PG 169 (17:15 PM) is FLAGGED HIGH RISK (only 2h30m window; check-in cutoffs close at 16:30). Any 20-min delay risks missing flight. NOT RECOMMENDED.",
                "pg177_pg181_recommendation": "Bangkok Airways PG 177 (19:30 PM) or PG 181 (20:00 PM) is RECOMMENDED STRESS-FREE PRIMARY (4h45m buffer; ample time for luggage, reunion, and boutique lounge).",
                "fluid_fallbacks": "Fallback 1: Overnight in Bangkok on Sep 24, morning flight Sep 25. Fallback 2: Surat Thani (URT) flight + Lomprayah catamaran."
            },
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
                "primary_transit": "09:45 AM: Taxi to Noi Bai Airport. 12:45 PM: Flight HAN -> BKK (Booking: 1145-554-179, arr 14:45). Friend departs. 15:15 PM: Retrieve suitcase from Floor B AIRPORTELs. 16:30 PM: Reunite with girlfriend at BKK Terminal. Board recommended Bangkok Airways PG 177 (19:30 PM) or PG 181 (20:00 PM) direct to Koh Samui (USM arr 20:35 / 21:05). Transfer to resort. (Note: PG 169 at 17:15 is flagged HIGH RISK due to tight connection).",
                "departure_time": "09:45 AM Hanoi / 19:30 PM BKK",
                "arrival_time": "21:30 PM Koh Samui resort",
                "buffer_time": "4h45m stress-free connection buffer at BKK terminal for bag retrieval, reunion, and check-in",
                "tips": "Bangkok Airways operates exclusive boutique lounges with complimentary snacks and espresso for all passengers at BKK Concourse A/F."
            },
            "curated_daily_flow": {
                "morning": "Checkout Hanoi hotel. Board confirmed flight 1145-554-179 to Bangkok. Bid farewell to friend as journeys branch.",
                "afternoon": "Land at Suvarnabhumi. Head to Floor B, retrieve checked suitcase. Reunite with girlfriend at arrivals hall! Drop bags for evening Koh Samui flight and enjoy treats in Bangkok Airways Boutique Lounge.",
                "evening": "Touchdown Koh Samui. Check-in to oceanfront King room at Hansar Samui. Late cocktails & dinner on the sand in Fisherman's Village."
            },
            "essential_checklist": [
                "Book Bangkok Airways PG 177 (19:30) or PG 181 (20:00) during Web Saver window in mid-July / early Aug",
                "Reserve 1 night arrival decompression at Hansar Samui Resort (King Ocean Room)",
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

    # Import enrichment data
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
    from core.enrichment_data import (
        DAY_EXPERIENCES,
        DAY_TRANSPORTS,
        PACKING_MASTER_LIST,
        TRANSLATIONS_DICTIONARY,
        CURRENCY_BENCHMARKS
    )

    # Enrich every day with experiences (Primary Plan vs Agile Contingency) and transport modules
    for d in days:
        d_num = d.get("day_number")
        if d_num in DAY_EXPERIENCES:
            d["experiences"] = DAY_EXPERIENCES[d_num]
        if d_num in DAY_TRANSPORTS:
            d["transport_module"] = DAY_TRANSPORTS[d_num]

    # Load confirmed registry items
    registry_path = os.path.join(os.path.dirname(__file__), "booking_registry.json")
    confirmed_items = []
    unbooked_action_items = []
    if os.path.exists(registry_path):
        with open(registry_path, "r", encoding="utf-8") as rf:
            reg_data = json.load(rf)
            confirmed_items = reg_data.get("confirmed_items", [])
            unbooked_action_items = reg_data.get("unbooked_action_items", [])

    master_payload = {
        "title": "Master Itinerary: Thailand & Vietnam [Adaptive Travel OS]",
        "generated_at": "2026-09-10T12:55:00Z",
        "system_version": "3.1.0 (Ground Companion & Experience Hub)",
        "operational_philosophy": "Hard Anchors, Fluid Routes: Only Gmail-verified bookings are immutable anchors. All intermediate routing, hotels, and timing dynamically adapt to live weather, transit buffers, and critic score thresholds.",
        "audit_note": "Audited: Only 6 genuine bookings verified from Gmail are marked CONFIRMED. All other days marked UNBOOKED with vetted recommendations.",
        "confirmed_metrics": {
            "total_days": 29,
            "confirmed_days_count": 5,
            "unbooked_days_count": 24,
            "confirmed_references": [
                {"item": "TLV -> BKK Emirates Flight EK2451/EK384 (Sep 10-11)", "ref": "Booking: G5M8CF"},
                {"item": "Thailand Digital Arrival Card (Sep 11)", "ref": "#30C4358"},
                {"item": "Sukhon Hotel Bangkok (Sep 11-12)", "ref": "Booking: 697155847"},
                {"item": "BKK -> HAN Flight (Sep 12)", "ref": "Booking: 1145-554-179"},
                {"item": "HAN -> BKK Flight (Sep 24)", "ref": "Booking: 1145-554-179"},
                {"item": "BKK -> TLV Etihad Flight (Oct 09)", "ref": "Booking: 9KDEH2"}
            ]
        },
        "route_resilience": {
            "active_sequence": "Sequence A (Mountain-First Triangle: Sa Pa -> Ninh Binh -> Cat Ba -> Hanoi)",
            "sequence_a": {
                "name": "Sequence A: Mountain-First Triangle (Recommended Primary)",
                "pacing": "Sa Pa (Sep 15-17) -> Ninh Binh (Sep 17-19) -> Cat Ba Island (Sep 19-22) -> Hanoi (Sep 22-24)",
                "rationale": "Eliminates brutal 10-hour Sa Pa to Cat Ba road slog. Sa Pa to Ninh Binh via direct express highway (6h). Ninh Binh to Cat Ba (2.5h direct bus+ferry). Cat Ba to Hanoi (2.5h direct bus via Hai Phong 5B expressway). Every leg post-Sa Pa is under 3 hours."
            },
            "sequence_b": {
                "name": "Sequence B: Coastal Inversion (Dynamic Fallback)",
                "pacing": "Hanoi (Sep 12-13) -> Cat Ba Island (Sep 13-16) -> Ninh Binh (Sep 16-18) -> Sa Pa (Sep 18-20) -> Ha Giang (Sep 20-23) -> Hanoi (Sep 23-24)",
                "trigger_condition": "Live satellite weather radar indicating heavy monsoon rainfall, road flooding, or landslide warnings on northern mountain passes (Ma Pi Leng / O Quy Ho) during Sep 12-15.",
                "rationale": "Inverts northern loop to enjoy calm waters in Lan Ha Bay first, delaying mountain passes until late September when conditions dry out."
            }
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
                "flight": "Hanoi (HAN) -> Bangkok (BKK) 12:45 PM (Booking: 1145-554-179 - CONFIRMED, arr 14:45)",
                "separation": "Friend departs/separates at BKK",
                "luggage_retrieval": "Retrieve checked suitcase at AIRPORTELs Suvarnabhumi Basement (Floor B)",
                "reunion": "Traveler reunites with Girlfriend in Bangkok arrivals hall",
                "south_flight": "Bangkok (BKK) -> Koh Samui (USM) (Recommended: Bangkok Airways PG 177 / PG 181; PG 169 flagged HIGH RISK)"
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
            "pickup_date": "2026-09-24 (14:45 arrival from HAN)",
            "duration": "12 Days",
            "storage_cost": "~100-150 THB / day (pay at counter or online)",
            "item_deposited": "1x Large Checked Suitcase containing Phase 2 resort attire",
            "item_kept": "1x 55L Clamshell Backpack (strictly backpack-only throughout Vietnam)"
        },
        "flight_radar_bkk_usm": {
            "route": "Bangkok Suvarnabhumi (BKK) -> Koh Samui (USM)",
            "date": "2026-09-24",
            "status": "UNBOOKED_TRACKING",
            "high_risk_flight": "Bangkok Airways PG 169 (Dep 17:15 BKK - Arr 18:20 USM) [HIGH RISK: Only 2h30m buffer for immigration, Floor B suitcase pickup, and 16:30 check-in cutoff]",
            "recommended_flight": "Bangkok Airways PG 177 (Dep 19:30 BKK - Arr 20:35 USM) or PG 181 (Dep 20:00 BKK - Arr 21:05 USM)",
            "connection_buffer": "4h45m stress-free window with free Bangkok Airways Boutique Lounge access (pastries, snacks, drinks)",
            "cheapest_bucket": "Web Saver (Approx. $115 - $135 USD / 4,100 - 4,800 THB)",
            "optimal_booking_window": "6 to 8 weeks prior to departure (Mid-July to Early August 2026).",
            "fluid_fallbacks": "Fallback 1: Overnight in Bangkok on Sep 24, morning flight Sep 25. Fallback 2: Surat Thani (URT) flight + Lomprayah catamaran."
        },
        "confirmed_items": confirmed_items,
        "unbooked_action_items": unbooked_action_items,
        "packing_master_list": PACKING_MASTER_LIST,
        "translations_dictionary": TRANSLATIONS_DICTIONARY,
        "currency_benchmarks": CURRENCY_BENCHMARKS,
        "total_days": len(days),
        "days": days
    }

    out_path = os.path.join(os.path.dirname(__file__), "itinerary_data.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(master_payload, f, indent=2, ensure_ascii=False)
    print(f"Successfully generated audited {out_path} with {len(days)} days!")

if __name__ == "__main__":
    build_itinerary()
