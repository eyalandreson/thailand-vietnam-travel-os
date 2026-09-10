"""
Adaptive Travel OS: Enrichment Dataset
Provides structured daily experiences (Primary Plan vs Agile Contingency),
door-to-door transport modules with direct booking links, Grab helpers,
persistent packing split architecture, translation phrases, and currency rates.
"""

DAY_EXPERIENCES = {
    1: {
        'primary': {
            'title': 'Jim Thompson House & Phetchaburi Soi 5 Street Food Crawl',
            'type': 'Cultural Silk Heritage & Culinary Walk',
            'duration': '3 - 4 hrs',
            'opening_hours': '10:00 - 18:00 (Last guided tour at 17:00)',
            'cost_estimate': '200 THB museum entry + ~150 THB street dinner',
            'time_sensitive_tip': 'Take BTS Skytrain from Phaya Thai to National Stadium (1 stop with interchange) or walk 15 mins down Soi Kasemsan 2. Avoid rush hour road taxis on Phaya Thai road.',
            'links': [
                {'label': 'Jim Thompson House Pin', 'url': 'https://maps.google.com/?q=Jim+Thompson+House+Bangkok', 'type': 'maps'},
                {'label': 'Pe Aor Tom Yum Kung Pin', 'url': 'https://maps.google.com/?q=Pe+Aor+Tom+Yum+Kung+Bangkok', 'type': 'maps'},
                {'label': 'Official Museum Info', 'url': 'https://www.jimthompsonhouse.org/', 'type': 'booking'}
            ]
        },
        'contingency': {
            'title': 'Siam Paragon Sea Life & CentralWorld Gourmet Hall (Sheltered)',
            'type': 'Fully Air-Conditioned Indoor Alternative',
            'duration': '3 hrs',
            'cost_estimate': 'Free mall browsing / 990 THB Sea Life aquarium',
            'trigger': 'Heavy afternoon tropical monsoon downpour upon landing',
            'time_sensitive_tip': 'Direct enclosed skybridge from BTS Siam to CentralWorld allows completely dry walking between all malls during heavy rain.',
            'links': [
                {'label': 'Sea Life Bangkok Map', 'url': 'https://maps.google.com/?q=Sea+Life+Bangkok+Ocean+World', 'type': 'maps'}
            ]
        }
    },
    2: {
        'primary': {
            'title': 'Noi Bai Airport Arrival & Direct VIP Sleeper Transit to Ha Giang City',
            'type': 'Airport Rendezvous & Northbound Sleeper Cabin',
            'duration': 'Flight: 1h 55m | Sleeper Bus from Airport: 5h 00m',
            'opening_hours': 'Airport pickup ~15:30 or 19:30; Ha Giang hotel check-in upon arrival',
            'cost_estimate': 'Ha Giang 3D Tour Package (Includes Airport Sleeper, Hotels, Easy-Riders, Meals)',
            'time_sensitive_tip': 'Landing at Noi Bai (HAN) at 13:50 PM. Deplane, clear e-visa customs. Meet Ha Giang tour driver directly at Terminal 2. The sleeper bus picks up right at the airport highway junction, bypassing downtown Hanoi gridlock entirely! Arrive in Ha Giang City and check into your tour hotel for a great night of sleep in twin beds before the loop starts tomorrow.',
            'links': [
                {'label': 'Noi Bai Airport Pin', 'url': 'https://maps.google.com/?q=Noi+Bai+International+Airport', 'type': 'maps'},
                {'label': 'Ha Giang 3D Tour Booking', 'url': 'https://cheershagiang.com/', 'type': 'booking'}
            ]
        },
        'contingency': {
            'title': 'Noi Bai Airport VIP Transit Lounge & Private Express Limousine Van',
            'type': 'Sheltered Airport Rest & Highway Limousine Van',
            'duration': '4.5 hrs transfer',
            'cost_estimate': 'Included in Tour package upgrade',
            'trigger': 'Flight delay or evening arrival needing faster private highway transfer',
            'time_sensitive_tip': 'Private 9-seater DCar VIP limousine van takes only 4.5 hours directly from the terminal to your Ha Giang City hotel with plush reclining leather massage seats.',
            'links': [
                {'label': 'Phoenix Hotel Ha Giang', 'url': 'https://maps.google.com/?q=Phoenix+Hotel+Ha+Giang', 'type': 'maps'}
            ]
        }
    },
    3: {
        'primary': {
            'title': 'Ha Giang Loop (Day 1): Bac Sum Pass, Heaven Gate & Dong Van Hotel Check-in',
            'type': 'Licensed Easy-Rider Alpine Tour (Hotels Included)',
            'duration': 'Full Day (08:30 - 17:30)',
            'opening_hours': 'Scenic mountain roads open daylight hours',
            'cost_estimate': 'All-inclusive in 3D Tour (Easy-Rider, fuel, hotel, lunch & dinner)',
            'time_sensitive_tip': 'Your 3-day tour includes private hotel rooms with twin beds (Dong Van Eco Stone House / Phoenix Dong Van). Gear up with DOT full-face helmet, knee and elbow armor. Ride Bac Sum pass, Quan Ba Heaven Gate, and Tham Ma switchbacks before reaching Dong Van Ancient Town.',
            'links': [
                {'label': 'Bac Sum Pass Viewpoint', 'url': 'https://maps.google.com/?q=Doc+Bac+Sum+Ha+Giang', 'type': 'maps'},
                {'label': 'Quan Ba Heaven Gate', 'url': 'https://maps.google.com/?q=Quan+Ba+Heaven+Gate', 'type': 'maps'},
                {'label': 'Dong Van Ancient Town', 'url': 'https://maps.google.com/?q=Dong+Van+Ancient+Town', 'type': 'maps'}
            ]
        },
        'contingency': {
            'title': 'Dong Van Ancient Fort Heritage Walk & Covered Hmong King Palace (Sa Phin)',
            'type': 'Sheltered Mountain Citadel & Fort Tour',
            'duration': '3.5 hrs',
            'cost_estimate': 'Included in Tour',
            'trigger': 'High mountain fog or rain reducing visibility on high ridges',
            'time_sensitive_tip': 'Hmong King Palace (Dinh Vua Meo) in Sa Phin features sheltered stone courtyards and heated tea rooms.',
            'links': [
                {'label': 'Hmong King Palace Map', 'url': 'https://maps.google.com/?q=Dinh+Vua+Meo+Ha+Giang', 'type': 'maps'}
            ]
        }
    },
    4: {
        'primary': {
            'title': 'Ha Giang Loop (Day 2): Ma Pi Leng Pass, Tu San Canyon Boat & Du Gia Hotel',
            'type': 'Legendary Pass, Emerald River Cruise & Valley Hotel',
            'duration': 'Full Day (08:00 - 17:30)',
            'opening_hours': 'Nho Que boat pier: 07:30 - 17:00',
            'cost_estimate': 'All-inclusive in 3D Tour (Private Twin Room in Du Gia, boat pass, meals)',
            'time_sensitive_tip': 'Highlight of the loop! Stop at the Ma Pi Leng monument, descend to the river for the motorboat cruise through Tu San Chasm (deepest canyon in SEA), then ride over mountain ridges to your private twin bungalow in Du Gia.',
            'links': [
                {'label': 'Ma Pi Leng Viewpoint', 'url': 'https://maps.google.com/?q=Ma+Pi+Leng+Pass', 'type': 'maps'},
                {'label': 'Tu San Canyon Pier', 'url': 'https://maps.google.com/?q=Nho+Que+River+Boat+Pier', 'type': 'maps'},
                {'label': 'Du Gia Valley View', 'url': 'https://maps.google.com/?q=Du+Gia+Ha+Giang', 'type': 'maps'}
            ]
        },
        'contingency': {
            'title': 'Covered Meo Vac Market Walk & Traditional Clay-Lodge Herbal Bath',
            'type': 'Indoor Cultural Market & Herbal Recovery',
            'duration': '3 hrs',
            'cost_estimate': 'Included in Tour',
            'trigger': 'Heavy rain warnings on the cliffside Sky Path',
            'time_sensitive_tip': 'Meo Vac clay lodges feature covered dining halls and medicinal herb baths infused with eucalyptus and ginger.',
            'links': [
                {'label': 'Meo Vac Market Map', 'url': 'https://maps.google.com/?q=Meo+Vac+Market', 'type': 'maps'}
            ]
        }
    },
    5: {
        'primary': {
            'title': 'Ha Giang Loop (Day 3: Du Gia to Base) & Sleeper Bus to Sa Pa Hotel (1 Night Sleep)',
            'type': 'Waterfall Swim, Return Loop & Sleeper Transit to Sa Pa',
            'duration': '4 hrs loop ride + 5 hrs evening sleeper bus',
            'opening_hours': 'Du Gia waterfall morning; sleeper bus departs ~18:30 PM',
            'cost_estimate': 'Included tour return + ~350,000 VND Ha Giang to Sa Pa sleeper bus',
            'time_sensitive_tip': 'Finish Day 3 of the loop at Ha Giang basecamp (~15:30). Take a warm shower, pack your 55L backpack, and board the direct evening sleeper bus to Sa Pa town! Arrive in Sa Pa, check into your town hotel (e.g. BB Hotel Sapa / Pao\'s Sapa) for a full night of solid, deep sleep in twin beds before the 2-day trek begins tomorrow.',
            'links': [
                {'label': 'Du Gia Waterfall Map', 'url': 'https://maps.google.com/?q=Du+Gia+Waterfall', 'type': 'maps'},
                {'label': 'Sa Pa Town Center', 'url': 'https://maps.google.com/?q=Sapa+Town+Square', 'type': 'maps'},
                {'label': 'BB Hotel Sapa', 'url': 'https://maps.google.com/?q=BB+Hotel+Sapa', 'type': 'maps'}
            ]
        },
        'contingency': {
            'title': 'Lung Tam Traditional Hemp Cooperative & Covered Highway Minibus to Sa Pa',
            'type': 'Sheltered Artisan Workshop & Direct Transfer',
            'duration': '4.5 hrs transfer',
            'cost_estimate': 'Standard transport fare',
            'trigger': 'Muddy mountain roads at Du Gia or rain during loop finish',
            'time_sensitive_tip': 'Lung Tam village features covered loom workshops where Hmong women weave hemp textiles using indigo dyes.',
            'links': [
                {'label': 'Lung Tam Weaving Village', 'url': 'https://maps.google.com/?q=Hop+Tac+Xa+Lanh+Lung+Tam', 'type': 'maps'}
            ]
        }
    },
    6: {
        'primary': {
            'title': '2-Day Guided Trek with Local Mamas (Day 1: Muong Hoa Valley to Ta Van Homestay)',
            'type': 'Authentic Ethnic Minority Guided Trek & Village Homestay',
            'duration': '6 hrs guided trail trek (09:00 - 15:30)',
            'opening_hours': 'Trek departs 09:00 AM from Sa Pa hotel',
            'cost_estimate': 'Guided trek package + homestay (~$40-$50 USD / 1M-1.2M VND per person including all meals)',
            'time_sensitive_tip': 'Wake up refreshed from your Sa Pa hotel. Meet your local Hmong Mama guide (authentic community trekking). Trek off-the-beaten-track ridge trails through Y Linh Ho and Lao Chai into Ta Van village. Stay at the Mama\'s family wooden homestay (twin mattresses with warm duvets). Cook and eat with the Mama: an authentic woodfire family feast (free-range roasted chicken, bamboo shoots, wild mountain greens, spring rolls, and happy water corn wine)!',
            'links': [
                {'label': 'Muong Hoa Valley Trailhead', 'url': 'https://maps.google.com/?q=Muong+Hoa+Valley+Sapa', 'type': 'maps'},
                {'label': 'Lao Chai Village', 'url': 'https://maps.google.com/?q=Lao+Chai+Village+Sapa', 'type': 'maps'},
                {'label': 'Ta Van Village Map', 'url': 'https://maps.google.com/?q=Ta+Van+Village+Sapa', 'type': 'maps'}
            ]
        },
        'contingency': {
            'title': 'Ta Van Covered Village Cultural Center & Traditional Herbal Foot Soak',
            'type': 'Sheltered Mountain Hamlet Sanctuary',
            'duration': '4 hrs',
            'cost_estimate': 'Included in homestay hospitality',
            'trigger': 'Heavy monsoon downpours making steep earthen trails slick',
            'time_sensitive_tip': 'The Mama leads along lower paved stone pathways directly to the homestay, followed by hot Red Dao herbal foot baths and hearthside cooking.',
            'links': [
                {'label': 'Ta Van Homestay', 'url': 'https://maps.google.com/?q=Ta+Van+Homestay+Sapa', 'type': 'maps'}
            ]
        }
    },
    7: {
        'primary': {
            'title': '2-Day Trek with Mamas (Day 2: Bamboo Forests & Waterfalls) -> Express Coach to Ninh Binh',
            'type': 'Guided Trail Walk, Farewell Lunch with Mama & Sequence A Highway Coach',
            'duration': '4 hrs morning trek + 6 hrs afternoon express coach',
            'opening_hours': 'Trek finishes 13:30; Express coach departs ~15:30-16:00',
            'cost_estimate': 'Trek package + 450,000 VND VIP express coach to Ninh Binh',
            'time_sensitive_tip': 'Wake up to misty mountain views. Enjoy Mama\'s homemade banana pancakes and mountain tea. Trek through dense giant bamboo forests to Giang Ta Chai waterfall and Red Dao village. Enjoy a farewell lunch with Mama, transfer back to Sa Pa town to shower and collect bags, then board the direct express coach to Ninh Binh (Tam Coc)! Arrive in Tam Coc for check-in at Tam Coc Garden Resort.',
            'links': [
                {'label': 'Giang Ta Chai Waterfall Pin', 'url': 'https://maps.google.com/?q=Giang+Ta+Chai+Waterfall', 'type': 'maps'},
                {'label': 'Tam Coc Garden Resort', 'url': 'https://maps.google.com/?q=Tam+Coc+Garden+Resort+Ninh+Binh', 'type': 'maps'}
            ]
        },
        'contingency': {
            'title': 'Giang Ta Chai Covered Tea House & Afternoon Highway Express Coach',
            'type': 'Sheltered Scenic Valley Route',
            'duration': '3 hrs morning + coach transit',
            'cost_estimate': 'Standard transport',
            'trigger': 'High river swell or slick waterfall rocks',
            'time_sensitive_tip': 'Short direct trail through the valley directly to vehicle pickup point for a clean, dry transfer back to Sa Pa town before the Ninh Binh coach.',
            'links': [
                {'label': 'Tam Coc Garden Resort', 'url': 'https://maps.google.com/?q=Tam+Coc+Garden+Resort+Ninh+Binh', 'type': 'maps'}
            ]
        }
    },
    8: {
        'primary': {
            'title': 'Trang An UNESCO Subterranean Karst Boat & Hang Mua Dragon Peak',
            'type': 'Water Cavern Rowboat & Panoramic Dragon Spine Climb',
            'duration': '6 hrs (07:15 - 14:00)',
            'opening_hours': 'Trang An: 07:00 - 17:00 | Hang Mua: 06:00 - 19:00',
            'cost_estimate': '250,000 VND Trang An boat + 100,000 VND Hang Mua pass',
            'time_sensitive_tip': 'Arrive at Trang An boat pier at 07:15 AM sharp to select Boat Route 3 (passes through 1,000m Dot Cave) before large tour buses arrive from Hanoi at 09:30.',
            'links': [
                {'label': 'Trang An Pier Map', 'url': 'https://maps.google.com/?q=Trang+An+Boat+Tour+Ninh+Binh', 'type': 'maps'},
                {'label': 'Hang Mua Dragon Peak', 'url': 'https://maps.google.com/?q=Hang+Mua+Ninh+Binh', 'type': 'maps'},
                {'label': 'Trang An Official Site', 'url': 'https://trangan.org.vn/en/', 'type': 'booking'}
            ]
        },
        'contingency': {
            'title': 'Bai Dinh Sacred Complex (Sheltered Arhat Corridors) & Van Long Wetland',
            'type': 'Covered Temple Corridor Exploration',
            'duration': '4 hrs',
            'cost_estimate': '150,000 VND electric buggy ticket',
            'trigger': 'High water levels in low caves or rain on slippery Hang Mua stone steps',
            'time_sensitive_tip': 'Bai Dinh has over 3 kilometers of sheltered, roofed stone corridors housing 500 hand-carved Arhat statues, completely rainproof.',
            'links': [
                {'label': 'Bai Dinh Pagoda Map', 'url': 'https://maps.google.com/?q=Bai+Dinh+Pagoda+Ninh+Binh', 'type': 'maps'}
            ]
        }
    },
    9: {
        'primary': {
            'title': 'Cat Co 3 Beach Swim, Perle d Orient Check-in & Cannon Fort Sunset',
            'type': 'Fast Coastal Transit & Sunset Citadel',
            'duration': '2.5 hrs transit + afternoon beach/views',
            'opening_hours': 'Cannon Fort: 08:00 - 18:30',
            'cost_estimate': '300,000 VND bus+ferry ticket + 40,000 VND Cannon Fort',
            'time_sensitive_tip': 'Under Sequence A, Ninh Binh to Cat Ba is only 2.5 hours total (direct bus + ferry channel). Arrive at your beachfront hotel before noon with zero fatigue!',
            'links': [
                {'label': 'Hotel Perle d Orient Cat Ba', 'url': 'https://maps.google.com/?q=Hotel+Perle+d+Orient+Cat+Ba', 'type': 'maps'},
                {'label': 'Cannon Fort Viewpoint', 'url': 'https://maps.google.com/?q=Cannon+Fort+Cat+Ba', 'type': 'maps'}
            ]
        },
        'contingency': {
            'title': 'Cannon Fort Subterranean Artillery Bunkers & Ocean Balcony Spa',
            'type': 'Historical Military Tunnels & Wellness',
            'duration': '3 hrs',
            'cost_estimate': 'Resort spa services',
            'trigger': 'Strong sea gusts or low visibility at sunset viewpoint',
            'time_sensitive_tip': 'The French and Vietnamese tunnel system inside Cannon Fort is dry, sheltered, and historically fascinating.',
            'links': [
                {'label': 'Cannon Fort Historical Site', 'url': 'https://maps.google.com/?q=Cannon+Fort+Cat+Ba', 'type': 'maps'}
            ]
        }
    },
    10: {
        'primary': {
            'title': 'Lan Ha Bay Wooden Junk Cruise, Dark & Bright Caves Kayak & Ba Trai Dao',
            'type': 'Emerald Secluded Bay Cruise & Sea Kayaking',
            'duration': '8 hrs (08:00 - 16:30)',
            'opening_hours': '08:00 pier departure from Ben Beo',
            'cost_estimate': '~$35 - $45 USD (850,000 - 1,100,000 VND) small group cruise',
            'time_sensitive_tip': 'Lan Ha Bay is far cleaner, quieter, and more pristine than commercial Ha Long Bay. Pack your 10L dry bag and camera float strap for paddling through limestone arches.',
            'links': [
                {'label': 'Ben Beo Pier Cat Ba', 'url': 'https://maps.google.com/?q=Ben+Beo+Pier+Cat+Ba', 'type': 'maps'},
                {'label': 'Ba Trai Dao Islets Pin', 'url': 'https://maps.google.com/?q=Ba+Trai+Dao+Beach+Lan+Ha+Bay', 'type': 'maps'},
                {'label': 'Vetted Cruise Provider', 'url': 'https://catbaventures.com/', 'type': 'booking'}
            ]
        },
        'contingency': {
            'title': 'Cat Ba National Park Rain Forest Boardwalk & Local Seafood Feast',
            'type': 'Sheltered Jungle Canopy Walk & Dining',
            'duration': '4 hrs',
            'cost_estimate': '80,000 VND park entry + 250,000 VND fresh seafood dinner',
            'trigger': 'Coast Guard small-craft marine storm flag prohibiting bay boats',
            'time_sensitive_tip': 'The interior island jungle is protected from open sea swells; enjoy dinner at Casa Bonita restaurant in town.',
            'links': [
                {'label': 'Cat Ba National Park', 'url': 'https://maps.google.com/?q=Cat+Ba+National+Park', 'type': 'maps'},
                {'label': 'Casa Bonita Cat Ba', 'url': 'https://maps.google.com/?q=Casa+Bonita+Cat+Ba', 'type': 'maps'}
            ]
        }
    },
    11: {
        'primary': {
            'title': 'Scooter Safari to Hospital Cave & Rainforest Ngu Lam Peak Hike',
            'type': 'Island Scooter Adventure & Secret War Bunker',
            'duration': '5 hrs (08:30 - 14:30)',
            'opening_hours': 'Hospital Cave: 08:00 - 17:00',
            'cost_estimate': '40,000 VND cave entry + ~120,000 VND scooter rental',
            'time_sensitive_tip': 'Hospital Cave was built inside a massive karst cavern during the American War; it contains 17 blast-proof rooms and operating theaters and stays a natural 20°C.',
            'links': [
                {'label': 'Hospital Cave Pin', 'url': 'https://maps.google.com/?q=Hospital+Cave+Cat+Ba', 'type': 'maps'},
                {'label': 'Ngu Lam Peak Trailhead', 'url': 'https://maps.google.com/?q=Ngu+Lam+Peak+Cat+Ba', 'type': 'maps'}
            ]
        },
        'contingency': {
            'title': 'Trung Trang Cave Geological Walk & MGallery Indochine High Tea',
            'type': 'Subterranean Cavern & Seaside Luxury',
            'duration': '3 hrs',
            'cost_estimate': '40,000 VND cave entry + high tea',
            'trigger': 'Rain making steep jungle rock scramble slippery',
            'time_sensitive_tip': 'Trung Trang Cave is a paved, illuminated 300-meter underground tunnel with centuries-old stalactites.',
            'links': [
                {'label': 'Trung Trang Cave Map', 'url': 'https://maps.google.com/?q=Trung+Trang+Cave+Cat+Ba', 'type': 'maps'}
            ]
        }
    },
    12: {
        'primary': {
            'title': 'Express Highway Return to Hanoi, Bun Cha Dac Kim & St. Joseph Cathedral',
            'type': 'Rapid 2.5h Highway Transit & Old Quarter Stroll',
            'duration': '2.5 hrs transit (09:00 - 11:30) + afternoon stroll',
            'opening_hours': 'Cat Ba Express departures at 09:00 AM',
            'cost_estimate': '320,000 VND express coach + 120,000 VND Bun Cha lunch',
            'time_sensitive_tip': 'Cat Ba Express drops off directly on Ma May street right in front of La Siesta Classic Ma May! You are in the heart of Hanoi before noon.',
            'links': [
                {'label': 'La Siesta Classic Ma May', 'url': 'https://maps.google.com/?q=La+Siesta+Classic+Ma+May+Hanoi', 'type': 'maps'},
                {'label': 'Bun Cha Dac Kim 1 Hang Manh', 'url': 'https://maps.google.com/?q=Bun+Cha+Dac+Kim+Hang+Manh', 'type': 'maps'},
                {'label': 'Cat Ba Express Booking', 'url': 'https://catbaexpress.com/', 'type': 'booking'}
            ]
        },
        'contingency': {
            'title': 'Hoa Lo Prison Historical Relic & Vietnam Women Museum (Air-Conditioned)',
            'type': 'Deep Cultural History & Air-Con Sanctuaries',
            'duration': '3 hrs',
            'cost_estimate': '30,000 VND + 40,000 VND entry fees',
            'trigger': 'Midday tropical downpour upon arriving in Hanoi',
            'time_sensitive_tip': 'Both museums are modern, air-conditioned, and provide outstanding English audio guides.',
            'links': [
                {'label': 'Hoa Lo Prison Relic Map', 'url': 'https://maps.google.com/?q=Hoa+Lo+Prison+Hanoi', 'type': 'maps'},
                {'label': 'Vietnam Women Museum', 'url': 'https://maps.google.com/?q=Vietnamese+Women+Museum', 'type': 'maps'}
            ]
        }
    },
    13: {
        'primary': {
            'title': 'Temple of Literature, Cha Ca Thang Long Feast & Craft Beer Flight',
            'type': '11th-Century Confucian Heritage & Guys Trip Finale',
            'duration': 'Leisurely across afternoon & evening',
            'opening_hours': 'Temple of Literature: 08:00 - 17:00',
            'cost_estimate': '30,000 VND Temple + 180,000 VND Cha Ca dinner',
            'time_sensitive_tip': 'Cha Ca Thang Long (6B Duong Thanh) sizzles freshwater fish tableside with golden turmeric and fresh mountain dill. Repack 55L packs tonight for tomorrow flight!',
            'links': [
                {'label': 'Temple of Literature Pin', 'url': 'https://maps.google.com/?q=Temple+of+Literature+Hanoi', 'type': 'maps'},
                {'label': 'Cha Ca Thang Long Map', 'url': 'https://maps.google.com/?q=Cha+Ca+Thang+Long+Duong+Thanh', 'type': 'maps'},
                {'label': 'Pasteur Street Craft Beer', 'url': 'https://maps.google.com/?q=Pasteur+Street+Brewing+Hanoi', 'type': 'maps'}
            ]
        },
        'contingency': {
            'title': 'Vietnam Museum of Ethnology & Covered Silk Shopping on Hang Gai',
            'type': 'Indoor Cultural Pavilions & Tailoring',
            'duration': '3.5 hrs',
            'cost_estimate': '40,000 VND museum entry',
            'trigger': 'Afternoon rain in Hanoi',
            'time_sensitive_tip': 'The Museum of Ethnology contains fascinating full-size tribal dwellings and artifacts from 54 ethnic groups; extensive covered pavilions.',
            'links': [
                {'label': 'Museum of Ethnology Map', 'url': 'https://maps.google.com/?q=Vietnam+Museum+of+Ethnology', 'type': 'maps'}
            ]
        }
    },
    14: {
        'primary': {
            'title': 'Hanoi Departure, BKK Basement Luggage Retrieval & Koh Samui Beach Dinner',
            'type': 'Seamless Multi-Modal Transition Day',
            'duration': 'Full day transition (Flight HAN-BKK arr 14:45 -> Evening flight to USM)',
            'opening_hours': 'AIRPORTELs BKK Floor B open 24/7',
            'cost_estimate': 'Bangkok Airways Web Saver fare ($115 - $135 USD)',
            'time_sensitive_tip': 'PG 169 (17:15) is FLAGGED HIGH RISK (only 2h30m connection). Recommend Bangkok Airways PG 177 (19:30) or PG 181 (20:00) with 4h45m buffer and free Boutique Lounge access!',
            'links': [
                {'label': 'AIRPORTELs BKK Basement', 'url': 'https://maps.google.com/?q=AIRPORTELs+Suvarnabhumi+Airport', 'type': 'maps'},
                {'label': 'Hansar Samui Resort', 'url': 'https://maps.google.com/?q=Hansar+Samui+Resort', 'type': 'maps'},
                {'label': 'Bangkok Airways Booking', 'url': 'https://www.bangkokair.com/booking', 'type': 'booking'}
            ]
        },
        'contingency': {
            'title': 'Bangkok Decompression Overnight at Riva Arun & Morning Flight to USM',
            'type': 'Fluid Flight Contingency Strategy',
            'duration': 'Overnight stay in Bangkok',
            'cost_estimate': 'Bangkok hotel stay + morning flight',
            'trigger': 'Evening Koh Samui flights sold out or severe flight delay out of Hanoi',
            'time_sensitive_tip': 'If Hanoi flight is delayed past 16:00, check into Riva Arun or Sukhon Hotel in Bangkok and book the 07:00 AM Bangkok Airways flight on Sep 25.',
            'links': [
                {'label': 'Sukhon Hotel Bangkok', 'url': 'https://maps.google.com/?q=Sukhon+Hotel+Bangkok', 'type': 'maps'}
            ]
        }
    },
    15: {
        'primary': {
            'title': 'Lomprayah Catamaran to Koh Phangan & Anantara Plunge Pool Villa Check-in',
            'type': 'Island Hop & Private Pool Villa Sanctuary',
            'duration': '25 mins boat + afternoon relaxation',
            'opening_hours': 'Lomprayah departures: 11:30 AM & 14:00 PM',
            'cost_estimate': '350 THB catamaran ticket per person',
            'time_sensitive_tip': 'Depart from Pralarn Pier (Maenam); it is only a 15-minute taxi from Bophut. Resort catamaran transfer delivers you to Thong Nai Pan Noi beach by early afternoon.',
            'links': [
                {'label': 'Pralarn Pier Maenam Map', 'url': 'https://maps.google.com/?q=Lomprayah+Pralarn+Pier+Samui', 'type': 'maps'},
                {'label': 'Anantara Rasananda Phangan', 'url': 'https://maps.google.com/?q=Anantara+Rasananda+Koh+Phangan', 'type': 'maps'},
                {'label': 'Lomprayah Catamaran Booking', 'url': 'https://www.lomprayah.com/', 'type': 'booking'}
            ]
        },
        'contingency': {
            'title': 'Rasananda Spa Coconut Body Scrub & Covered Beachside Wine Pairing',
            'type': 'Luxury Couple Wellness & Fine Dining',
            'duration': '3 hrs',
            'cost_estimate': 'Resort spa packages',
            'trigger': 'Swell or passing rainfall upon arrival on Koh Phangan',
            'time_sensitive_tip': 'The Anantara jungle spa is set amid towering tropical granite boulders with covered treatment salas overlooking the gentle sea.',
            'links': [
                {'label': 'Anantara Rasananda Spa', 'url': 'https://maps.google.com/?q=Anantara+Rasananda+Koh+Phangan', 'type': 'maps'}
            ]
        }
    },
    16: {
        'primary': {
            'title': 'Coastal Longtail Boat to Bottle Beach & Thong Nai Pan Snorkeling',
            'type': 'Private Secluded Lagoon & Reef Swim',
            'duration': '5 hrs (10:00 - 15:00)',
            'opening_hours': 'Longtail boats operate daylight hours',
            'cost_estimate': '200 THB per person roundtrip longtail boat',
            'time_sensitive_tip': 'Take a private wooden longtail boat directly from Thong Nai Pan beach around the northern headland to Bottle Beach (15 mins); avoids the bumpy dirt road.',
            'links': [
                {'label': 'Bottle Beach Pin', 'url': 'https://maps.google.com/?q=Bottle+Beach+Koh+Phangan', 'type': 'maps'},
                {'label': 'Thong Nai Pan Noi Beach', 'url': 'https://maps.google.com/?q=Thong+Nai+Pan+Noi', 'type': 'maps'}
            ]
        },
        'contingency': {
            'title': 'Private Thai Cooking Masterclass & Covered Beach Sala Yoga',
            'type': 'Resort Culinary & Wellness Sanctuary',
            'duration': '3 hrs',
            'cost_estimate': '1,500 THB cooking class for two',
            'trigger': 'High waves preventing smooth longtail beach landings',
            'time_sensitive_tip': 'Chef-led cooking masterclass teaches authentic southern Thai red curry and tom kha gai with organic resort herbs.',
            'links': [
                {'label': 'Anantara Culinary Pavilion', 'url': 'https://maps.google.com/?q=Anantara+Rasananda+Koh+Phangan', 'type': 'maps'}
            ]
        }
    },
    17: {
        'primary': {
            'title': 'Ang Thong National Marine Park Semi-Private Yacht & Emerald Lake',
            'type': 'Signature Yacht Cruise, Karst Kayak & Viewpoint',
            'duration': '8 hrs (08:30 - 16:30)',
            'opening_hours': 'Daily park opening',
            'cost_estimate': '300 THB park fee + ~$85 USD boutique cruise package',
            'time_sensitive_tip': 'Hike up to the Emerald Lake (Talay Nai) saltwater lagoon viewpoint. Choose a semi-private sailing yacht rather than 80-passenger cattle-boat tours.',
            'links': [
                {'label': 'Ang Thong Marine Park', 'url': 'https://maps.google.com/?q=Mu+Ko+Ang+Thong+National+Park', 'type': 'maps'},
                {'label': 'Boutique Yacht Booking', 'url': 'https://www.getyourguide.com/koh-samui-l169/ang-thong-marine-park-t12548/', 'type': 'booking'}
            ]
        },
        'contingency': {
            'title': 'Than Sadet Waterfall & King Rama V Royal Inscriptions with Beach Lunch',
            'type': 'Sheltered Rainforest Cascade & History',
            'duration': '4 hrs',
            'cost_estimate': 'Free waterfall access + casual beach lunch',
            'trigger': 'Marine weather flag restricting offshore cruises to Ang Thong',
            'time_sensitive_tip': 'Than Sadet was visited by three Thai kings who carved their royal monograms into the granite river boulders; easy shaded walk under dense rainforest canopy.',
            'links': [
                {'label': 'Than Sadet Waterfall Map', 'url': 'https://maps.google.com/?q=Than+Sadet+Waterfall', 'type': 'maps'}
            ]
        }
    },
    18: {
        'primary': {
            'title': 'Sri Thanu Bohemian Cafes, Haad Yao Snorkel & Zen Beach Sunset',
            'type': 'West Coast Bohemian Vibe & Barefoot Acoustic Sunset',
            'duration': 'Full afternoon & sunset (12:00 - 19:30)',
            'opening_hours': 'Zen Beach gathering: 17:30 - 19:00',
            'cost_estimate': 'Free beach access + ~400 THB organic cafe meal',
            'time_sensitive_tip': 'Arrive at Zen Beach by 17:30 PM. Local acoustic musicians, contact improvers, and barefoot yogis gather on the sand for a magical golden hour.',
            'links': [
                {'label': 'Zen Beach Pin', 'url': 'https://maps.google.com/?q=Zen+Beach+Koh+Phangan', 'type': 'maps'},
                {'label': 'Karma Cafe Sri Thanu', 'url': 'https://maps.google.com/?q=Karma+Cafe+Koh+Phangan', 'type': 'maps'},
                {'label': 'Haad Yao Beach', 'url': 'https://maps.google.com/?q=Haad+Yao+Beach+Koh+Phangan', 'type': 'maps'}
            ]
        },
        'contingency': {
            'title': 'The Dome Herbal Steam Sauna & Amsterdam Bar Hillside Terrace',
            'type': 'Herbal Detox & Covered Panoramic Sunset Deck',
            'duration': '4 hrs',
            'cost_estimate': '200 THB sauna + sunset drinks',
            'trigger': 'Overcast skies diminishing beach sunset',
            'time_sensitive_tip': 'The Dome features outdoor natural herbal steam infused with lemongrass and eucalyptus, with fire pits and soothing ambient music.',
            'links': [
                {'label': 'The Dome Herbal Sauna', 'url': 'https://maps.google.com/?q=The+Dome+Koh+Phangan', 'type': 'maps'},
                {'label': 'Amsterdam Bar Hillside', 'url': 'https://maps.google.com/?q=Amsterdam+Bar+Koh+Phangan', 'type': 'maps'}
            ]
        }
    },
    19: {
        'primary': {
            'title': 'East Coast Bohemian Longtail Cruise to Haad Yuan & Haad Thian',
            'type': 'Remote Road-Free Beach Sanctuary',
            'duration': '5 hrs (10:30 - 16:00)',
            'opening_hours': 'Longtail boats from Haad Rin / Thong Nai Pan',
            'cost_estimate': '300 THB longtail transfer per person',
            'time_sensitive_tip': 'Haad Yuan has zero car roads; all access is strictly by boat. It retains the enchanting, laid-back island atmosphere of Thailand 25 years ago.',
            'links': [
                {'label': 'Haad Yuan Beach Pin', 'url': 'https://maps.google.com/?q=Haad+Yuan+Koh+Phangan', 'type': 'maps'},
                {'label': 'The Sanctuary Thailand', 'url': 'https://maps.google.com/?q=The+Sanctuary+Thailand+Haad+Tien', 'type': 'maps'}
            ]
        },
        'contingency': {
            'title': 'Private In-Villa Couple Massage & Poolside Champagne Service',
            'type': 'Ultimate Villa Seclusion',
            'duration': 'Leisurely all afternoon',
            'cost_estimate': 'Resort spa billing',
            'trigger': 'Choppy easterly waves preventing longtail beach drop-offs',
            'time_sensitive_tip': 'Enjoy uninterrupted romance in your private Anantara plunge pool with customized Spotify island playlist and chilled wine.',
            'links': [
                {'label': 'Anantara Rasananda Villas', 'url': 'https://maps.google.com/?q=Anantara+Rasananda+Koh+Phangan', 'type': 'maps'}
            ]
        }
    },
    20: {
        'primary': {
            'title': 'Secret Beach Lagoon, Koh Raham Treehouse Bar & Cliffside Sunset',
            'type': 'Treehouse Sea Pavilion & Romantic Dinner',
            'duration': '5 hrs (14:00 - 20:30)',
            'opening_hours': 'Koh Raham open daily 10:00 - 23:00',
            'cost_estimate': '1,200 THB romantic dinner for two',
            'time_sensitive_tip': 'Koh Raham is built into living beachfront trees with over-water hammocks where you can feed tropical damselfish directly from your seat.',
            'links': [
                {'label': 'Secret Beach (Haad Son)', 'url': 'https://maps.google.com/?q=Secret+Beach+Haad+Son+Koh+Phangan', 'type': 'maps'},
                {'label': 'Koh Raham Restaurant Pin', 'url': 'https://maps.google.com/?q=Koh+Raham+Restaurant+and+Beach+Bar', 'type': 'maps'},
                {'label': 'Top Rock Bar Sunset', 'url': 'https://maps.google.com/?q=Top+Rock+Bar+Koh+Phangan', 'type': 'maps'}
            ]
        },
        'contingency': {
            'title': 'Thong Sala Covered Night Walking Street & Artisan Craft Crawl',
            'type': 'Covered Night Food Market Feast',
            'duration': '3 hrs',
            'cost_estimate': '250 THB street food feast',
            'trigger': 'Passing evening rain shower',
            'time_sensitive_tip': 'Thong Sala night market is fully covered with stalls serving fresh pad thai, grilled tiger prawns, and mango sticky rice.',
            'links': [
                {'label': 'Phantip Night Food Market', 'url': 'https://maps.google.com/?q=Phantip+Market+Koh+Phangan', 'type': 'maps'}
            ]
        }
    },
    21: {
        'primary': {
            'title': 'Lomprayah Catamaran to Koh Tao & The Place Luxury Villa Check-in',
            'type': 'Catamaran to Diver Mecca & Secluded Villa Hillside',
            'duration': '45 mins catamaran + afternoon check-in',
            'opening_hours': 'Lomprayah boat at 11:00 AM (arr 12:00 PM)',
            'cost_estimate': '550 THB catamaran ticket per person',
            'time_sensitive_tip': 'The Place Luxury Boutique Villas provides private transfer from Mae Haad pier. Each villa is totally secluded with its own private infinity plunge pool and glass-wrapped bathroom.',
            'links': [
                {'label': 'Mae Haad Pier Koh Tao', 'url': 'https://maps.google.com/?q=Mae+Haad+Pier+Koh+Tao', 'type': 'maps'},
                {'label': 'The Place Luxury Villas', 'url': 'https://maps.google.com/?q=The+Place+Luxury+Boutique+Villas', 'type': 'maps'},
                {'label': 'Lomprayah Booking Link', 'url': 'https://www.lomprayah.com/', 'type': 'booking'}
            ]
        },
        'contingency': {
            'title': 'Covered Hillside Villa Wine Service & Sunset Movie Terrace',
            'type': 'Private Hillside Villa Relaxation',
            'duration': 'Leisurely afternoon',
            'cost_estimate': 'In-villa grocery / dining delivery',
            'trigger': 'Midday rain upon arrival on Koh Tao',
            'time_sensitive_tip': 'The Place villas feature expansive covered wooden sundecks that allow outdoor dining and swimming even during tropical island rain.',
            'links': [
                {'label': 'The Place Villa Grounds', 'url': 'https://maps.google.com/?q=The+Place+Luxury+Boutique+Villas', 'type': 'maps'}
            ]
        }
    },
    22: {
        'primary': {
            'title': 'Shark Bay Turtle & Blacktip Reef Shark Snorkel + Freedom Beach',
            'type': 'World-Class Marine Snorkeling & Secluded Cove',
            'duration': '4.5 hrs (08:30 - 13:30)',
            'opening_hours': 'Morning snorkel window: 08:30 - 11:00',
            'cost_estimate': '100 THB private bay access fee',
            'time_sensitive_tip': 'Swim out 50 meters into the shallow bay over the sandy seagrass patches between 08:30 and 10:30 AM for guaranteed encounters with gentle 1-meter green sea turtles.',
            'links': [
                {'label': 'Shark Bay (Thian Og) Map', 'url': 'https://maps.google.com/?q=Shark+Bay+Koh+Tao', 'type': 'maps'},
                {'label': 'Freedom Beach Koh Tao', 'url': 'https://maps.google.com/?q=Freedom+Beach+Koh+Tao', 'type': 'maps'}
            ]
        },
        'contingency': {
            'title': 'Koh Tao Garden Cinema & Authentic Yin Yang Cooking School',
            'type': 'Sheltered Cultural & Culinary Workshop',
            'duration': '3.5 hrs',
            'cost_estimate': '1,200 THB cooking class for two',
            'trigger': 'Choppy bay swell reducing underwater visibility',
            'time_sensitive_tip': 'Yin Yang restaurant runs intimate indoor cooking workshops where you pound your own curry paste using stone mortars.',
            'links': [
                {'label': 'Yin Yang Thai Cooking', 'url': 'https://maps.google.com/?q=Yin+Yang+Restaurant+Koh+Tao', 'type': 'maps'}
            ]
        }
    },
    23: {
        'primary': {
            'title': 'Private Longtail to Koh Nang Yuan Sandbar & Japanese Gardens',
            'type': 'Iconic Three-Islet Sandbar & Giant Clam Coral Garden',
            'duration': '5 hrs (09:00 - 14:30)',
            'opening_hours': '09:00 - 16:00 (Daily island admission)',
            'cost_estimate': '250 THB island conservation fee + 150 THB longtail',
            'time_sensitive_tip': 'Single-use plastic water bottles are strictly banned on Koh Nang Yuan (checked at the pier). Carry your refillable metal canteens. Hike the wooden steps to the iconic viewpoint first!',
            'links': [
                {'label': 'Koh Nang Yuan Viewpoint', 'url': 'https://maps.google.com/?q=Koh+Nang+Yuan+Viewpoint', 'type': 'maps'},
                {'label': 'Japanese Gardens Snorkel', 'url': 'https://maps.google.com/?q=Japanese+Garden+Koh+Tao', 'type': 'maps'}
            ]
        },
        'contingency': {
            'title': 'Sun Suwan 360 Covered Viewpoint Lounge & Couple Massage',
            'type': 'Panoramic High-Altitude Deck & Spa',
            'duration': '3 hrs',
            'cost_estimate': '50 THB viewpoint + spa services',
            'trigger': 'High tide washing over sandbar or poor reef clarity',
            'time_sensitive_tip': 'Sun Suwan viewpoint features a large thatched roof bar perched 200m above the sea with stunning views of the entire southern coast.',
            'links': [
                {'label': 'Sun Suwan 360 Viewpoint', 'url': 'https://maps.google.com/?q=Sun+Suwan+360+Viewpoint+Koh+Tao', 'type': 'maps'}
            ]
        }
    },
    24: {
        'primary': {
            'title': 'Private Chartered Longtail to Mango Bay & Hin Wong Bay Reefs',
            'type': 'Private Boat Exploration to Deep Coral Pinnacles',
            'duration': '5.5 hrs (09:30 - 15:00)',
            'opening_hours': 'Private boat charter timing flexible',
            'cost_estimate': '1,800 - 2,200 THB private half-day longtail charter',
            'time_sensitive_tip': 'Hiring a private longtail captain at Sairee Beach lets you anchor in pristine turquoise coves 1 hour before commercial snorkel tours arrive.',
            'links': [
                {'label': 'Mango Bay Koh Tao Map', 'url': 'https://maps.google.com/?q=Mango+Bay+Koh+Tao', 'type': 'maps'},
                {'label': 'Hin Wong Bay Pin', 'url': 'https://maps.google.com/?q=Hin+Wong+Bay+Koh+Tao', 'type': 'maps'}
            ]
        },
        'contingency': {
            'title': 'Tanote Bay Cliff Jump (Sheltered East Side) & Factory Cafe',
            'type': 'Sheltered Bay Activity & Artisan Coffee',
            'duration': '3.5 hrs',
            'cost_estimate': 'Free beach + cafe dining',
            'trigger': 'Strong northerly wind making north cape rough',
            'time_sensitive_tip': 'When northern bays are windy, eastern Tanote Bay is typically glassy and calm with a massive granite boulder for safe cliff jumping into 4m deep water.',
            'links': [
                {'label': 'Tanote Bay Map', 'url': 'https://maps.google.com/?q=Tanote+Bay+Koh+Tao', 'type': 'maps'},
                {'label': 'Factory Cafe Sairee', 'url': 'https://maps.google.com/?q=Factory+Cafe+Koh+Tao', 'type': 'maps'}
            ]
        }
    },
    25: {
        'primary': {
            'title': 'John-Suwan Granite Ridge Viewpoint & Babaloo Beach Lunch',
            'type': 'Epic Dual-Bay Viewpoint & Rustic Beach Bar',
            'duration': '4 hrs (08:30 - 12:30)',
            'opening_hours': '08:00 - 18:00',
            'cost_estimate': '50 THB viewpoint entry + lunch on the sand',
            'time_sensitive_tip': 'Wear closed-toe trainers with grip; the last 50 meters of the ridge require holding fixed ropes over smooth granite rocks. View overlooks both Chalok and Shark bays at once!',
            'links': [
                {'label': 'John-Suwan Viewpoint Pin', 'url': 'https://maps.google.com/?q=John-Suwan+Viewpoint+Koh+Tao', 'type': 'maps'},
                {'label': 'Babaloo Beach Bar Map', 'url': 'https://maps.google.com/?q=Babaloo+Bar+Koh+Tao', 'type': 'maps'}
            ]
        },
        'contingency': {
            'title': 'Sairee Beachfront Covered Cafes & Kyo Yoga Studio',
            'type': 'Mindful Movement & Beachside Artisan Coffee',
            'duration': '3 hrs',
            'cost_estimate': '350 THB yoga drop-in',
            'trigger': 'Rain making granite rocks slippery and dangerous for hiking',
            'time_sensitive_tip': 'Kyo Yoga offers ocean-breeze indoor sessions; relax afterwards with fresh smoothie bowls at Living Juices Sairee.',
            'links': [
                {'label': 'Sairee Village Center', 'url': 'https://maps.google.com/?q=Sairee+Beach+Koh+Tao', 'type': 'maps'}
            ]
        }
    },
    26: {
        'primary': {
            'title': 'Stand-Up Paddleboarding in Sairee Bay & Sunset Dinner at Barracuda',
            'type': 'Calm Water SUP & Beachfront Fine Seafood',
            'duration': '4 hrs (16:30 - 21:00)',
            'opening_hours': 'Barracuda open: 17:30 - 22:30',
            'cost_estimate': '200 THB/hr SUP rental + 1,500 THB romantic dinner for two',
            'time_sensitive_tip': 'Book beachfront table at Barracuda at least 24 hours in advance for their legendary grilled seafood platter and passion fruit cocktails at sunset.',
            'links': [
                {'label': 'Barracuda Restaurant Map', 'url': 'https://maps.google.com/?q=Barracuda+Restaurant+Koh+Tao', 'type': 'maps'},
                {'label': 'Fizz Beachlounge Pin', 'url': 'https://maps.google.com/?q=Fizz+Beachlounge+Koh+Tao', 'type': 'maps'}
            ]
        },
        'contingency': {
            'title': 'Whitening Restaurant Covered Wooden Pier & Candlelit Seafood',
            'type': 'Covered Over-Water Dining Under Candlelight',
            'duration': '2.5 hrs',
            'cost_estimate': '1,400 THB couple dinner',
            'trigger': 'Evening drizzle on the open beach',
            'time_sensitive_tip': 'Whitening features elegant white-canopy roofed seating on wooden stilts directly above the lapping night surf in Mae Haad.',
            'links': [
                {'label': 'Whitening Restaurant Map', 'url': 'https://maps.google.com/?q=The+Whitening+Restaurant+Koh+Tao', 'type': 'maps'}
            ]
        }
    },
    27: {
        'primary': {
            'title': 'Catamaran + Flight Transit to Bangkok & Riva Arun Sunset over Wat Arun',
            'type': 'Boutique Island Departure & Riverside Temple View Check-in',
            'duration': 'Full afternoon transit + sunset drinks',
            'opening_hours': 'Lomprayah catamaran: 09:30 AM',
            'cost_estimate': 'Catamaran + Bangkok Airways domestic flight',
            'time_sensitive_tip': 'Riva Arun rooms look straight across the Chao Phraya River to the majestic spires of Wat Arun (Temple of Dawn). Watch the temple illuminate golden at 18:30 from Above Riva rooftop!',
            'links': [
                {'label': 'Riva Arun Bangkok Map', 'url': 'https://maps.google.com/?q=Riva+Arun+Bangkok', 'type': 'maps'},
                {'label': 'Above Riva Rooftop Bar', 'url': 'https://maps.google.com/?q=Above+Riva+Bangkok', 'type': 'maps'},
                {'label': 'Bangkok Airways Booking', 'url': 'https://www.bangkokair.com/booking', 'type': 'booking'}
            ]
        },
        'contingency': {
            'title': 'Central Embassy Luxury Cinema & Covered Gourmet Food Hall',
            'type': 'High-End Indoor Luxury Experience',
            'duration': '3.5 hrs',
            'cost_estimate': '1,800 THB VIP cinema reclining daybed for two',
            'trigger': 'Heavy Bangkok rain or evening thunderstorm on open rooftop',
            'time_sensitive_tip': 'The Embassy Diplomat Screens provide ultra-luxury private reclining pods with complimentary cocktails and canapes.',
            'links': [
                {'label': 'Central Embassy Bangkok', 'url': 'https://maps.google.com/?q=Central+Embassy+Bangkok', 'type': 'maps'}
            ]
        }
    },
    28: {
        'primary': {
            'title': 'Private Longtail Boat Tour of Thonburi Khlongs & Wat Pho Reclining Buddha',
            'type': 'Historic Canal Exploration & Golden Temple Finale',
            'duration': '5 hrs (09:30 - 14:30)',
            'opening_hours': 'Wat Pho: 08:00 - 18:30',
            'cost_estimate': '1,500 THB private 2hr canal boat + 200 THB Wat Pho pass',
            'time_sensitive_tip': 'Charter a private wooden longtail boat directly from Tha Tien pier. The Thonburi canals reveal teak stilt houses, water monitors, and hidden orchid farms untouched by modern high-rises.',
            'links': [
                {'label': 'Wat Pho Reclining Buddha', 'url': 'https://maps.google.com/?q=Wat+Pho+Bangkok', 'type': 'maps'},
                {'label': 'Tha Tien Pier Pin', 'url': 'https://maps.google.com/?q=Tha+Tien+Pier+Bangkok', 'type': 'maps'},
                {'label': 'The Deck by Arun Residence', 'url': 'https://maps.google.com/?q=The+Deck+by+Arun+Residence', 'type': 'maps'}
            ]
        },
        'contingency': {
            'title': 'ICONSIAM SookSiam Indoor Floating Market & Luxury River Walk',
            'type': 'Air-Conditioned Indoor Culinary Wonderland',
            'duration': '4 hrs',
            'cost_estimate': 'Free shuttle boat from Sathorn / ~300 THB food feast',
            'trigger': 'Afternoon downpour in Bangkok',
            'time_sensitive_tip': 'SookSiam inside ICONSIAM replicates authentic floating markets with hundreds of vendors from all 77 Thai provinces in climate-controlled indoor comfort.',
            'links': [
                {'label': 'ICONSIAM SookSiam Map', 'url': 'https://maps.google.com/?q=ICONSIAM+Bangkok', 'type': 'maps'}
            ]
        }
    },
    29: {
        'primary': {
            'title': 'Riverside Balcony Breakfast, ARL to Suvarnabhumi & Etihad Flight to TLV',
            'type': 'Relaxed Riverside Finale & Confirmed Return Departure',
            'duration': 'Leisurely morning + 15:55 PM Flight',
            'opening_hours': 'Check-in opens 3 hours prior at 12:55 PM',
            'cost_estimate': 'ARL train (45 THB) or Grab (~400 THB)',
            'time_sensitive_tip': 'Confirmed Etihad flight 9KDEH2 departs at 15:55 PM. Arrive at BKK airport by 12:45-13:00 PM to clear VAT refund customs inspection and security.',
            'links': [
                {'label': 'Suvarnabhumi Departures Map', 'url': 'https://maps.google.com/?q=Suvarnabhumi+Airport+Departures', 'type': 'maps'},
                {'label': 'Etihad Airways Booking', 'url': 'https://www.etihad.com/', 'type': 'booking'}
            ]
        },
        'contingency': {
            'title': 'Suvarnabhumi Miracle VIP Business Lounge Relaxation & Shower',
            'type': 'VIP Airport Lounge Comfort Prior to Flight',
            'duration': '2.5 hrs before boarding',
            'cost_estimate': 'Complimentary with select bank cards / ~1,200 THB pass',
            'trigger': 'Early airport arrival or heavy rain in Bangkok traffic',
            'time_sensitive_tip': 'Miracle Lounge at Concourse D features hot noodle bar, cold beers, complimentary Wi-Fi, and private rainfall shower suites.',
            'links': [
                {'label': 'Miracle Lounge Concourse D', 'url': 'https://maps.google.com/?q=Miracle+Lounge+Suvarnabhumi+Concourse+D', 'type': 'maps'}
            ]
        }
    }
}

DAY_TRANSPORTS = {
    1: {
        'route': 'BKK Suvarnabhumi Airport -> Sukhon Hotel Bangkok',
        'transit_type': 'Airport Rail Link (City Line) or Airport Metered Taxi',
        'pickup_hub': 'BKK Airport Basement (Floor B) for Train / Level 1 for Taxi',
        'dropoff_terminal': 'BTS Phaya Thai Station (Exit 2) / Sukhon Hotel Doorstep',
        'duration': '26 mins by ARL Train / 35-50 mins by Taxi',
        'baggage_allowance': 'Unrestricted on ARL train; fits all luggage',
        'booking_provider': 'Airport Rail Link Ticket Counter or Grab App',
        'booking_url': 'https://maps.google.com/?q=Phaya+Thai+Station+Bangkok',
        'grab_helper': {
            'pickup': 'Suvarnabhumi Airport (Level 1 Gate 4)',
            'dropoff': 'Sukhon Hotel Bangkok',
            'dropoff_local': 'โรงแรมสุคนธ์ 55/5-6 ถนนพญาไท ราชเทวี กรุงเทพฯ',
            'maps_url': 'https://maps.google.com/?q=Sukhon+Hotel+Bangkok'
        }
    },
    2: {
        'route': 'Bangkok (Sukhon) -> BKK Basement -> Hanoi Airport (HAN) -> Sleeper to Ha Giang City',
        'transit_type': 'International Flight (Mytrip 1145-554-179) + Direct Airport VIP Sleeper Bus',
        'pickup_hub': 'Sukhon Hotel -> BKK Level 4 Check-in -> Hanoi Noi Bai Airport (Terminal 2)',
        'dropoff_terminal': 'Ha Giang City Tour Hotel (Phoenix Hotel / Tour Base)',
        'duration': 'Flight: 1h 55m | Direct Airport Sleeper: 5h 00m',
        'baggage_allowance': 'Checked suitcase in BKK Floor B AIRPORTELs; strictly 55L backpack for flight and sleeper bus',
        'booking_provider': 'Confirmed Mytrip E-Ticket (Order: 1145-554-179) + Ha Giang Tour Airport Sleeper',
        'booking_url': 'documents/Flight_Mytrip_BKK_HAN_BKK_1145-554-179.pdf',
        'grab_helper': {
            'pickup': 'Noi Bai International Airport Terminal 2',
            'dropoff': 'Noi Bai Expressway Bus Point (Ha Giang Sleeper Pickup)',
            'dropoff_local': 'Điểm đón xe giường nằm đi Hà Giang tại sân bay Nội Bài',
            'maps_url': 'https://maps.google.com/?q=Noi+Bai+International+Airport'
        }
    },
    3: {
        'route': 'Ha Giang City -> Bac Sum Pass -> Quan Ba -> Tham Ma Pass -> Dong Van',
        'transit_type': '3-Day Ha Giang Tour: Licensed Easy-Riders (Hotels Included)',
        'pickup_hub': 'Ha Giang City Tour Base (08:30 AM)',
        'dropoff_terminal': 'Dong Van Ancient Town Hotel (Twin Room Included)',
        'duration': 'Scenic motorcade with guided stops across 145 km',
        'baggage_allowance': 'Bungee-strapped waterproof pack on rear motorcycle rack',
        'booking_provider': 'Ha Giang 3D Tour Operator (Cheers Ha Giang / QT / Road Kings)',
        'booking_url': 'https://cheershagiang.com/',
        'grab_helper': None
    },
    4: {
        'route': 'Dong Van -> Ma Pi Leng Pass -> Tu San Canyon Boat -> Meo Vac -> Du Gia',
        'transit_type': 'Licensed Easy-Riders + Nho Que Motorboat Cruise (Hotels Included)',
        'pickup_hub': 'Dong Van Hotel Doorstep (08:00 AM)',
        'dropoff_terminal': 'Du Gia Valley Hotel / Private Bungalow (Twin Beds Included)',
        'duration': 'Full-day scenic ride & canyon cruise',
        'baggage_allowance': 'Waterproof bag on bike rack',
        'booking_provider': 'Ha Giang 3D Tour Operator',
        'booking_url': 'https://cheershagiang.com/',
        'grab_helper': None
    },
    5: {
        'route': 'Du Gia -> Ha Giang Basecamp -> Direct Sleeper Bus to Sa Pa Town Hotel',
        'transit_type': 'Easy-Rider return leg + Direct Evening Sleeper Bus to Sa Pa',
        'pickup_hub': 'Du Gia (08:00 AM) -> Ha Giang Base (15:30 PM) -> Sa Pa Sleeper (18:30 PM)',
        'dropoff_terminal': 'Sa Pa Town Center Hotel (BB Hotel Sapa / Pao\'s Sapa) - 1 Night Deep Sleep',
        'duration': 'Ha Giang to Sa Pa Sleeper: ~5h 00m (Arrives Sa Pa ~23:30 PM)',
        'baggage_allowance': '55L clamshell backpack in bus luggage bay',
        'booking_provider': '12Go Asia / Truly Ha Giang / Bang Phan / Quang Nghi Sleeper',
        'booking_url': 'https://12go.asia/en/travel/ha-giang/sapa?date=2026-09-15',
        'grab_helper': None
    },
    6: {
        'route': 'Sa Pa Town Hotel -> 2-Day Trek Guided by Mamas -> Ta Van Village Homestay',
        'transit_type': 'Guided Mountain Trail Trek on Foot with Local Hmong Mama',
        'pickup_hub': 'Sa Pa Town Hotel Lobby (09:00 AM departure on foot)',
        'dropoff_terminal': 'Mama\'s Village Homestay (Ta Van / Hau Thao Village)',
        'duration': '6 hrs guided trail walk through Muong Hoa Valley',
        'baggage_allowance': 'Daypack for overnight at homestay; 55L pack safely transferred or stored',
        'booking_provider': 'Local Ethnic Minority Guide (Sapa Sisters / Mama Mu Community Trek)',
        'booking_url': 'https://sapasisters.com/',
        'grab_helper': None
    },
    7: {
        'route': 'Ta Van Mama\'s Homestay -> Bamboo Forest Trek -> Sa Pa -> Direct VIP Coach to Ninh Binh',
        'transit_type': 'Guided Trail Walk + Shuttle to Town + Direct Highway VIP Express Coach',
        'pickup_hub': 'Ta Van Homestay (09:00 AM) -> Sa Pa Town (14:00 PM) -> Express Coach (15:30 PM)',
        'dropoff_terminal': 'Tam Coc Garden Resort / Wharf Doorstep, Ninh Binh (21:30 PM)',
        'duration': 'Morning trek 4 hrs | Highway Express Coach to Ninh Binh: 6 hrs',
        'baggage_allowance': '55L backpack in undercarriage luggage compartment',
        'booking_provider': '12Go Asia / The Long Travel / Daily Limousine Express',
        'booking_url': 'https://12go.asia/en/travel/sapa/ninh-binh?date=2026-09-17',
        'grab_helper': None
    },
    8: {
        'route': 'Tam Coc -> Trang An UNESCO Pier -> Hang Mua -> Tam Coc',
        'transit_type': 'Local Resort Bicycles & Short Metered Taxi',
        'pickup_hub': 'Tam Coc Garden Resort (07:15 AM)',
        'dropoff_terminal': 'Trang An Boat Complex / Hang Mua Dragon Cave',
        'duration': '15 mins taxi between sights; scenic bicycle lanes',
        'baggage_allowance': 'Small 10L daypack for boat & hike',
        'booking_provider': 'Mai Linh Taxi Ninh Binh / Resort Reception',
        'booking_url': 'https://maps.google.com/?q=Trang+An+Boat+Tour+Ninh+Binh',
        'grab_helper': None
    },
    9: {
        'route': 'Ninh Binh (Tam Coc) -> Cat Ba Island (Lan Ha Bay)',
        'transit_type': 'Direct Tourist Coach + Speedboat Ferry Combined Ticket',
        'pickup_hub': 'Tam Coc Hotel Doorstep (09:00 AM)',
        'dropoff_terminal': 'Hôtel Perle d Orient MGallery Cat Ba Doorstep (12:00 PM)',
        'duration': 'Only 2.5 - 3.0 hrs total (Fast & effortless)',
        'baggage_allowance': '55L backpack automatically handled onto ferry',
        'booking_provider': 'Daiichi Travel / Good Morning Cat Ba / 12Go Asia',
        'booking_url': 'https://12go.asia/en/travel/ninh-binh/cat-ba?date=2026-09-19',
        'grab_helper': None
    },
    10: {
        'route': 'Cat Ba Resort -> Ben Beo Pier -> Lan Ha Bay & Ba Trai Dao',
        'transit_type': 'Resort Buggy + Traditional Wooden Junk Cruise Boat',
        'pickup_hub': 'Hôtel Perle d Orient Lobby (08:00 AM)',
        'dropoff_terminal': 'Ben Beo Harbor Pier (16:30 PM)',
        'duration': '8 hrs sailing & kayaking exploration',
        'baggage_allowance': '10L waterproof dry bag only',
        'booking_provider': 'Cat Ba Ventures / Blue Swimmer Adventures',
        'booking_url': 'https://catbaventures.com/',
        'grab_helper': None
    },
    11: {
        'route': 'Cat Co Beach -> Hospital Cave -> Cat Ba National Park -> Sunset Cove',
        'transit_type': 'Automatic Scooter Rental or Open-Air Buggy',
        'pickup_hub': 'Resort Front Desk (08:30 AM)',
        'dropoff_terminal': 'National Park Trailhead / Hospital Cave Entrance',
        'duration': '25 mins scenic island road ride',
        'baggage_allowance': 'Under-seat helmet storage + daypack',
        'booking_provider': 'Island Scooter Hire (~120,000 VND / $5 USD/day)',
        'booking_url': 'https://maps.google.com/?q=Hospital+Cave+Cat+Ba',
        'grab_helper': None
    },
    12: {
        'route': 'Cat Ba Island -> Hai Phong Expressway -> Hanoi Old Quarter',
        'transit_type': 'Cat Ba Express Combined Speedboat & Highway Coach',
        'pickup_hub': 'Resort Lobby Doorstep (09:00 AM)',
        'dropoff_terminal': 'La Siesta Classic Ma May Doorstep (11:30 AM)',
        'duration': 'Only 2.5 hrs flat via 5B Hai Phong Expressway',
        'baggage_allowance': '55L backpack in bus hold',
        'booking_provider': 'Cat Ba Express / 12Go Asia',
        'booking_url': 'https://12go.asia/en/travel/cat-ba/hanoi?date=2026-09-22',
        'grab_helper': {
            'pickup': 'Cat Ba Express Office (94 Ma May)',
            'dropoff': 'La Siesta Classic Ma May Hotel',
            'dropoff_local': '94 Mã Mây, Hoàn Kiếm, Hà Nội',
            'maps_url': 'https://maps.google.com/?q=La+Siesta+Classic+Ma+May+Hanoi'
        }
    },
    13: {
        'route': 'Hanoi Old Quarter Walkable Exploration & Grab Cross-City Hops',
        'transit_type': 'Walking + Grab Taxi / Traditional Cyclo',
        'pickup_hub': 'La Siesta Classic Ma May',
        'dropoff_terminal': 'Temple of Literature / Cha Ca Thang Long',
        'duration': '10-15 mins per hop',
        'baggage_allowance': 'Daypack; packing 55L bags in evening',
        'booking_provider': 'Grab App / Walkable streets',
        'booking_url': 'https://maps.google.com/?q=Temple+of+Literature+Hanoi',
        'grab_helper': {
            'pickup': 'La Siesta Classic Ma May',
            'dropoff': 'Cha Ca Thang Long',
            'dropoff_local': '6B Đường Thành, Hoàn Kiếm, Hà Nội',
            'maps_url': 'https://maps.google.com/?q=Cha+Ca+Thang+Long+Duong+Thanh'
        }
    },
    14: {
        'route': 'Hanoi (HAN) -> BKK Suvarnabhumi -> Floor B Locker -> Koh Samui (USM)',
        'transit_type': 'International Flight + Elevator to Floor B + Bangkok Airways Direct',
        'pickup_hub': 'Noi Bai Airport (12:45) -> BKK (14:45) -> Suvarnabhumi Level 4 Domestic',
        'dropoff_terminal': 'Hansar Samui Resort & Spa (Bophut Beach, Koh Samui)',
        'duration': 'HAN-BKK: 2h 00m | BKK-USM: 1h 05m (Recommended PG 177 / 181)',
        'baggage_allowance': 'Checked suitcase retrieved at BKK Floor B; 20kg included on Bangkok Airways',
        'booking_provider': 'Bangkok Airways PG 177 (19:30) / PG 181 (20:00)',
        'booking_url': 'https://www.bangkokair.com/booking',
        'grab_helper': {
            'pickup': 'Koh Samui Airport Arrivals',
            'dropoff': 'Hansar Samui Resort',
            'dropoff_local': 'โรงแรมหรรษา สมุย 101/28 หมู่ 1 บ่อผุด เกาะสมุย',
            'maps_url': 'https://maps.google.com/?q=Hansar+Samui+Resort'
        }
    },
    15: {
        'route': 'Koh Samui (Bophut) -> Pralarn Pier -> Koh Phangan (Thong Sala) -> Resort',
        'transit_type': 'Lomprayah High-Speed Catamaran + 4WD Resort Transfer',
        'pickup_hub': 'Pralarn Pier Maenam (11:30 AM departure)',
        'dropoff_terminal': 'Anantara Rasananda Koh Phangan Villas (13:00 PM)',
        'duration': '25 mins boat crossing + 35 mins scenic island transfer',
        'baggage_allowance': 'Full luggage allowed onboard Lomprayah',
        'booking_provider': 'Lomprayah High-Speed Ferries',
        'booking_url': 'https://www.lomprayah.com/',
        'grab_helper': None
    },
    16: {
        'route': 'Thong Nai Pan Beach -> Bottle Beach (Haad Khuat) -> Return',
        'transit_type': 'Private Wooden Longtail Boat Hop',
        'pickup_hub': 'Thong Nai Pan Beachfront (10:00 AM)',
        'dropoff_terminal': 'Bottle Beach Granite Cove',
        'duration': '15 mins exhilarating coastal boat ride',
        'baggage_allowance': 'Beach tote & snorkel dry-bag',
        'booking_provider': 'Local Boat Captain on Beachfront',
        'booking_url': 'https://maps.google.com/?q=Bottle+Beach+Koh+Phangan',
        'grab_helper': None
    },
    17: {
        'route': 'Koh Phangan Pier -> Ang Thong National Marine Park Archipelago',
        'transit_type': 'Boutique Yacht / Sailing Catamaran Day Charter',
        'pickup_hub': 'Thong Sala Harbor Pier (08:30 AM)',
        'dropoff_terminal': 'Emerald Lake (Talay Nai) & Wua Ta Lap Viewpoint',
        'duration': 'Full day sailing across 42 islands',
        'baggage_allowance': 'Day dry-bag with towel & sunscreen',
        'booking_provider': 'GetYourGuide / Orion Cruises',
        'booking_url': 'https://www.getyourguide.com/koh-samui-l169/ang-thong-marine-park-t12548/',
        'grab_helper': None
    },
    18: {
        'route': 'Thong Nai Pan -> Sri Thanu Wellness Hub -> Zen Beach -> Return',
        'transit_type': 'Island Open-Air Songthaew Taxi or Private 4WD',
        'pickup_hub': 'Anantara Rasananda Lobby (11:30 AM)',
        'dropoff_terminal': 'Zen Beach West Coast (19:30 PM)',
        'duration': '40 mins cross-island drive through jungle hills',
        'baggage_allowance': 'Casual daypack',
        'booking_provider': 'Resort Concierge Songthaew Taxi',
        'booking_url': 'https://maps.google.com/?q=Zen+Beach+Koh+Phangan',
        'grab_helper': None
    },
    19: {
        'route': 'Thong Nai Pan -> Haad Rin Pier -> Haad Yuan / Haad Thian',
        'transit_type': 'Coastal Longtail Boat Transfer',
        'pickup_hub': 'Haad Rin East Beach (10:30 AM)',
        'dropoff_terminal': 'Haad Yuan Bohemian Cove',
        'duration': '15 mins sea hop around southern cape',
        'baggage_allowance': 'Beach bag',
        'booking_provider': 'Haad Rin Longtail Taxi Pool',
        'booking_url': 'https://maps.google.com/?q=Haad+Yuan+Koh+Phangan',
        'grab_helper': None
    },
    20: {
        'route': 'Thong Nai Pan -> Secret Beach (Haad Son) -> Top Rock Bar',
        'transit_type': 'Private Island Taxi Songthaew',
        'pickup_hub': 'Anantara Lobby (13:30 PM)',
        'dropoff_terminal': 'Koh Raham / Secret Beach',
        'duration': '45 mins scenic drive',
        'baggage_allowance': 'Casual evening wear',
        'booking_provider': 'Local Taxi Desk',
        'booking_url': 'https://maps.google.com/?q=Secret+Beach+Haad+Son+Koh+Phangan',
        'grab_helper': None
    },
    21: {
        'route': 'Koh Phangan (Thong Sala) -> Koh Tao (Mae Haad) -> The Place Villas',
        'transit_type': 'Lomprayah High-Speed Catamaran + Resort 4WD Hillside Taxi',
        'pickup_hub': 'Thong Sala Pier (11:00 AM departure)',
        'dropoff_terminal': 'The Place Luxury Boutique Villas (12:30 PM arrival)',
        'duration': '45 mins boat ride + 10 mins villa transfer',
        'baggage_allowance': 'Full checked luggage permitted on catamaran',
        'booking_provider': 'Lomprayah High Speed Ferries',
        'booking_url': 'https://www.lomprayah.com/',
        'grab_helper': None
    },
    22: {
        'route': 'The Place Villas -> Shark Bay (Thian Og) -> Freedom Beach -> Return',
        'transit_type': 'Resort Private 4WD Shuttle / Local Taxi',
        'pickup_hub': 'Villa Gate (08:30 AM)',
        'dropoff_terminal': 'Shark Bay Reef Entrance',
        'duration': '12 mins drive across southern ridge',
        'baggage_allowance': 'Snorkel mask & dry bag',
        'booking_provider': 'The Place Villa Dedicated Driver',
        'booking_url': 'https://maps.google.com/?q=Shark+Bay+Koh+Tao',
        'grab_helper': None
    },
    23: {
        'route': 'Sairee Beach Wharf -> Koh Nang Yuan Island -> Japanese Gardens',
        'transit_type': 'Private Chartered Longtail Boat',
        'pickup_hub': 'Sairee Beachfront (09:00 AM)',
        'dropoff_terminal': 'Koh Nang Yuan Private Wooden Jetty',
        'duration': '15 mins peaceful boat hop',
        'baggage_allowance': 'Refillable water bottle & snorkel gear (No plastic allowed!)',
        'booking_provider': 'Local Longtail Boat Pool on Sairee Beach',
        'booking_url': 'https://maps.google.com/?q=Koh+Nang+Yuan+Viewpoint',
        'grab_helper': None
    },
    24: {
        'route': 'Koh Tao Western Coast -> Mango Bay & Hin Wong Bay (North Cape)',
        'transit_type': 'Private Half-Day Chartered Longtail Boat',
        'pickup_hub': 'Sairee Beach (09:30 AM)',
        'dropoff_terminal': 'Mango Bay Turquoise Lagoon',
        'duration': '5 hrs private coastal cruise',
        'baggage_allowance': 'Beach towels & dry bag',
        'booking_provider': 'Private Captain Direct Charter (~2,000 THB)',
        'booking_url': 'https://maps.google.com/?q=Mango+Bay+Koh+Tao',
        'grab_helper': None
    },
    25: {
        'route': 'The Place Villas -> John-Suwan Viewpoint -> Chalok Baan Kao',
        'transit_type': '4WD Island Taxi',
        'pickup_hub': 'Villa Driveway (08:30 AM)',
        'dropoff_terminal': 'Freedom Beach / John-Suwan Trailhead',
        'duration': '15 mins drive',
        'baggage_allowance': 'Hiking trainers & water pack',
        'booking_provider': 'Local Island Taxi Desk',
        'booking_url': 'https://maps.google.com/?q=John-Suwan+Viewpoint+Koh+Tao',
        'grab_helper': None
    },
    26: {
        'route': 'The Place Villas -> Sairee Beachfront Sunset & Dining Strip',
        'transit_type': 'Leisurely Downhill Stroll / Resort 4WD',
        'pickup_hub': 'Villa Gate (16:30 PM)',
        'dropoff_terminal': 'Barracuda Restaurant / Sairee Sand',
        'duration': '5 mins drive or 15 mins walk',
        'baggage_allowance': 'Evening resort attire',
        'booking_provider': 'The Place On-Call Driver',
        'booking_url': 'https://maps.google.com/?q=Barracuda+Restaurant+Koh+Tao',
        'grab_helper': None
    },
    27: {
        'route': 'Koh Tao (Mae Haad) -> Samui (USM) -> Bangkok (BKK) -> Riva Arun',
        'transit_type': 'Lomprayah Catamaran + Bangkok Airways Flight + ARL/Taxi',
        'pickup_hub': 'Mae Haad Pier (09:30 AM) -> USM Flight (14:30) -> BKK (15:35)',
        'dropoff_terminal': 'Riva Arun Bangkok Doorstep (17:30 PM)',
        'duration': 'Catamaran: 1h 45m | Flight: 1h 05m | City transfer: 45m',
        'baggage_allowance': 'Full luggage (20kg Bangkok Airways checked bag)',
        'booking_provider': 'Lomprayah + Bangkok Airways',
        'booking_url': 'https://www.bangkokair.com/booking',
        'grab_helper': {
            'pickup': 'Suvarnabhumi Airport Arrivals Level 1',
            'dropoff': 'Riva Arun Bangkok',
            'dropoff_local': 'โรงแรมริวา อรุณ 392/25-26 ถนนมหาราช พระบรมมหาราชวัง กรุงเทพฯ',
            'maps_url': 'https://maps.google.com/?q=Riva+Arun+Bangkok'
        }
    },
    28: {
        'route': 'Riva Arun -> Tha Tien Pier -> Thonburi Khlongs -> Wat Pho -> Return',
        'transit_type': 'Private Teak Longtail Boat + Walkable Temple Access',
        'pickup_hub': 'Tha Tien Pier (directly behind Riva Arun)',
        'dropoff_terminal': 'Wat Pho Reclining Buddha Sanctuary',
        'duration': '2 hrs private boat + 1.5 hrs temple stroll',
        'baggage_allowance': 'Daypack; temple appropriate attire (covered shoulders & knees)',
        'booking_provider': 'Tha Tien Pier Private Boatman Counter',
        'booking_url': 'https://maps.google.com/?q=Wat+Pho+Bangkok',
        'grab_helper': {
            'pickup': 'Riva Arun Bangkok',
            'dropoff': 'The Deck by Arun Residence',
            'dropoff_local': 'ร้าน เดอะ เดค บาย อรุณ เรสซิเดนซ์ ซอยประตูนกยูง มหาราช',
            'maps_url': 'https://maps.google.com/?q=The+Deck+by+Arun+Residence'
        }
    },
    29: {
        'route': 'Riva Arun Bangkok -> MRT/ARL or Grab Taxi -> BKK Suvarnabhumi',
        'transit_type': 'Grab Premium Taxi or MRT Sanam Chai -> ARL Makkasan -> BKK',
        'pickup_hub': 'Riva Arun Lobby (11:45 AM checkout)',
        'dropoff_terminal': 'BKK Suvarnabhumi International Departures Level 4 (12:45 PM)',
        'duration': '45 - 60 mins depending on city expressway traffic',
        'baggage_allowance': 'Full checked suitcases + carry-on backpacks',
        'booking_provider': 'Grab Taxi or Airport Rail Link / Confirmed Etihad E-Ticket 9KDEH2',
        'booking_url': 'documents/Etihad_BKK_TLV_9KDEH2_Eyal_Andreson.pdf',
        'grab_helper': {
            'pickup': 'Riva Arun Bangkok',
            'dropoff': 'Suvarnabhumi Airport Departures Level 4',
            'dropoff_local': 'ท่าอากาศยานสุวรรณภูมิ อาคารผู้โดยสารขาออก ชั้น 4',
            'maps_url': 'https://maps.google.com/?q=Suvarnabhumi+Airport+Departures'
        }
    }
}

PACKING_MASTER_LIST = {
    'bag_a_backpack': [
        {'id': 'bp_1', 'cat': 'Apparel', 'name': 'Quick-Dry Trekking Shirts (4x)', 'desc': 'Moisture wicking synthetic or merino wool for Ha Giang and Sa Pa', 'priority': 'HIGH'},
        {'id': 'bp_2', 'cat': 'Apparel', 'name': 'Convertible Trekking Pants & Shorts (2x)', 'desc': 'Reinforced knees and breathable fabric for mountain trails', 'priority': 'HIGH'},
        {'id': 'bp_3', 'cat': 'Apparel', 'name': 'Lightweight Windbreaker / Rain Shell', 'desc': 'Waterproof breathable jacket for mountain passes and boat spray', 'priority': 'CRITICAL'},
        {'id': 'bp_4', 'cat': 'Footwear', 'name': 'Trail Runner Shoes with Deep Lugs', 'desc': 'Vibram or grippy rubber sole for muddy terraced rice fields', 'priority': 'CRITICAL'},
        {'id': 'bp_5', 'cat': 'Gear', 'name': '55L High-Visibility Rain Cover', 'desc': 'Elastic waterproof pack cover for motorcycle racks in Ha Giang', 'priority': 'CRITICAL'},
        {'id': 'bp_6', 'cat': 'Gear', 'name': '10L & 20L Roll-Top Dry Bags', 'desc': 'Essential for Lan Ha Bay kayaking and Ang Thong yacht trips', 'priority': 'HIGH'},
        {'id': 'bp_7', 'cat': 'Gear', 'name': 'Microfiber Quick-Dry Towels (2x)', 'desc': 'Compact, lightweight, fast drying for homestays and boat dips', 'priority': 'MEDIUM'},
        {'id': 'bp_8', 'cat': 'Health', 'name': 'Travel Medical Kit (Imodium, ORS, Paracetamol, Antihistamines)', 'desc': 'Oral rehydration salts and digestive meds for street food', 'priority': 'CRITICAL'},
        {'id': 'bp_9', 'cat': 'Electronics', 'name': 'Universal Travel Plug Adapter & 20,000mAh Power Bank', 'desc': 'Keep phone and navigation charged during 8-hour loop rides', 'priority': 'CRITICAL'},
        {'id': 'bp_10', 'cat': 'Gear', 'name': 'Microfiber Neck Gaiter / Buff & Sunglasses', 'desc': 'Protects face from road dust and limestone glare on motorbike', 'priority': 'HIGH'}
    ],
    'bag_b_suitcase': [
        {'id': 'sc_1', 'cat': 'Resort Wear', 'name': 'Linen Shirts & Tailored Shorts (4x)', 'desc': 'Breathable chic evening resort attire for Koh Samui and Phangan', 'priority': 'HIGH'},
        {'id': 'sc_2', 'cat': 'Resort Wear', 'name': 'Smart Casual Dinner Shoes / Leather Sandals', 'desc': 'For fine dining at Above Riva and Barracuda seafood restaurant', 'priority': 'MEDIUM'},
        {'id': 'sc_3', 'cat': 'Resort Wear', 'name': 'Evening Linen Trousers & Light Evening Dress Shirt', 'desc': 'Sophisticated sunset rooftop and beach club dinners', 'priority': 'MEDIUM'},
        {'id': 'sc_4', 'cat': 'Romance', 'name': 'Girlfriend Travel Items & Island Gifts', 'desc': 'Pre-packed surprises and Phase 2 couple amenities', 'priority': 'HIGH'},
        {'id': 'sc_5', 'cat': 'Swimwear', 'name': 'UV Protection Rashguard & Premium Boardshorts (2x)', 'desc': 'Full sun protection for full-day snorkeling in Koh Tao and Ang Thong', 'priority': 'HIGH'},
        {'id': 'sc_6', 'cat': 'Toiletries', 'name': 'Bulk Sunscreen (Reef-Safe SPF 50+) & Skincare', 'desc': 'Reef-friendly sunscreen to protect corals in Koh Tao', 'priority': 'CRITICAL'},
        {'id': 'sc_7', 'cat': 'Apparel', 'name': 'Formal Temple Attire (Covered Shoulders & Knees)', 'desc': 'Polite respectful wear for Wat Pho and Grand Palace', 'priority': 'HIGH'},
        {'id': 'sc_8', 'cat': 'Water Gear', 'name': 'Waterproof Phone Dry Pouches (Lanyard Style)', 'desc': 'Touchscreen accessible dry bag for kayak and boat tours', 'priority': 'HIGH'},
        {'id': 'sc_9', 'cat': 'Accessories', 'name': 'Ultra-Compact Travel Steam Iron / Anti-Crease Spray', 'desc': 'Keep linen garments crisp after 12 days in luggage storage', 'priority': 'LOW'},
        {'id': 'sc_10', 'cat': 'Luggage', 'name': 'Heavy Duty TSA Luggage Locks & Contact Tags', 'desc': 'Secured for 12 days at BKK Floor B AIRPORTELs facility', 'priority': 'CRITICAL'}
    ],
    'pre_departure_inspection': [
        {'id': 'insp_1', 'cat': 'Immigration', 'name': 'Physical Passport (Valid > 6 Months)', 'desc': 'Verified valid with at least 4 blank visa stamp pages', 'priority': 'CRITICAL'},
        {'id': 'insp_2', 'cat': 'Immigration', 'name': 'Vietnam 30-Day Single Entry E-Visa Printouts (2x)', 'desc': 'Printed paper copies required at Noi Bai border checkpoint', 'priority': 'CRITICAL'},
        {'id': 'insp_3', 'cat': 'Immigration', 'name': 'Thailand Digital Arrival Card (TDAC #30C4358 QR Code)', 'desc': 'Saved offline on smartphone for rapid entry at BKK', 'priority': 'CRITICAL'},
        {'id': 'insp_4', 'cat': 'Transit', 'name': 'International Driving Permit (IDP 1968 Convention)', 'desc': 'For legal motorcycle transport validation in Southeast Asia', 'priority': 'HIGH'},
        {'id': 'insp_5', 'cat': 'Finance', 'name': 'Physical Zero-Foreign-Fee ATM Cards (Schwab/Wise/Revolut)', 'desc': 'Keep primary and backup cards in separate luggage compartments', 'priority': 'CRITICAL'},
        {'id': 'insp_6', 'cat': 'Tickets', 'name': 'E-Tickets Saved Offline (Emirates, Mytrip, Etihad)', 'desc': 'Verified PNRs: G5M8CF, 1145-554-179, 9KDEH2 stored on device', 'priority': 'CRITICAL'}
    ]
}

TRANSLATIONS_DICTIONARY = {
    'taxi_transit': [
        {
            'en': 'Please take me to Sukhon Hotel next to BTS Phaya Thai Exit 2.',
            'th': 'กรุณาไปส่งที่โรงแรมสุคนธ์ ใกล้ BTS พญาไท ทางออก 2 ครับ',
            'th_phonetic': 'Ga-roo-nah pai song tee rong-raem Soo-khon glai BTS Phaya Thai thang awk song khrap',
            'vi': 'Làm ơn đưa tôi đến khách sạn Sukhon gần ga BTS Phaya Thai.',
            'vi_phonetic': 'Lam on dua toi den khach san Sukhon gan ga BTS Phaya Thai'
        },
        {
            'en': 'Please turn on the meter.',
            'th': 'กรุณาเปิดมิเตอร์ด้วยครับ',
            'th_phonetic': 'Ga-roo-nah poet mee-ter dooay khrap',
            'vi': 'Làm ơn bật đồng hồ tính tiền giúp tôi.',
            'vi_phonetic': 'Lam on bat dong ho tinh tien giup toi'
        },
        {
            'en': 'Please take me to Suvarnabhumi Airport Floor B (AIRPORTELs luggage storage).',
            'th': 'กรุณาไปส่งที่สนามบินสุวรรณภูมิ ชั้น B (จุดรับฝากกระเป๋า AIRPORTELs) ครับ',
            'th_phonetic': 'Ga-roo-nah pai song tee sa-nahm-bin Soo-wan-na-phoom chun bee khrap',
            'vi': 'Làm ơn đưa tôi đến sân bay Suvarnabhumi tầng B (chỗ gửi hành lý AIRPORTELs).',
            'vi_phonetic': 'Lam on dua toi den san bay Suvarnabhumi tang B'
        },
        {
            'en': 'Please take me to Hanoi Old Quarter (94 Ma May Street).',
            'th': 'กรุณาไปส่งที่ย่านเมืองเก่าฮานอย ถนนหม่าเมย์',
            'th_phonetic': 'Ga-roo-nah pai song tee yahn meuang gao Ha-noy',
            'vi': 'Làm ơn đưa tôi đến 94 phố Mã Mây, Phố Cổ Hà Nội.',
            'vi_phonetic': 'Lam on dua toi den chin muoi tu pho Ma May, Pho Co Ha Noi'
        }
    ],
    'food_dietary': [
        {
            'en': 'No sugar and no condensed milk in my coffee, please.',
            'th': 'กาแฟดำ ไม่ใส่น้ำตาล ไม่ใส่นมข้นครับ',
            'th_phonetic': 'Gah-fae dam, mai sai nam-dtan, mai sai nom-khon khrap',
            'vi': 'Cho tôi cà phê không đường, không sữa đặc.',
            'vi_phonetic': 'Cho toi ca phe khong duong, khong sua dac'
        },
        {
            'en': 'Not too spicy, please / Little chili.',
            'th': 'เผ็ดน้อยครับ / ไม่ใส่พริก',
            'th_phonetic': 'Phet noy khrap / mai sai phrik',
            'vi': 'Làm ơn cho ít cay / không ăn cay.',
            'vi_phonetic': 'Lam on cho it cay / khong an cay'
        },
        {
            'en': 'No ice, please / Bottled water only.',
            'th': 'ไม่เอาน้ำแข็งครับ / ขอน้ำดื่มแบบขวดปิดสนิท',
            'th_phonetic': 'Mai ao nam-khaeng khrap / kho nam-deum baeb khuat bpit sa-nit',
            'vi': 'Làm ơn không lấy đá / Cho tôi nước đóng chai.',
            'vi_phonetic': 'Lam on khong lay da / Cho toi nuoc dong chai'
        },
        {
            'en': 'Does this dish contain pork or shell fish?',
            'th': 'จานนี้มีหมูหรือหอยไหมครับ?',
            'th_phonetic': 'Jahn nee mee moo reu hoi mai khrap?',
            'vi': 'Món này có thịt heo hoặc hải sản có vỏ không?',
            'vi_phonetic': 'Mon nay co thit heo hoac hai san co vo khong?'
        },
        {
            'en': 'May I please have the bill?',
            'th': 'เช็คบิลด้วยครับ / เก็บเงินด้วยครับ',
            'th_phonetic': 'Check bill dooay khrap / Gep ngern dooay khrap',
            'vi': 'Làm ơn tính tiền giúp tôi.',
            'vi_phonetic': 'Lam on tinh tien giup toi'
        }
    ],
    'emergency_medical': [
        {
            'en': 'I need urgent medical assistance. Please take me to the nearest hospital.',
            'th': 'ต้องการความช่วยเหลือทางการแพทย์ด่วน โปรดพาไปโรงพยาบาลที่ใกล้ที่สุดครับ',
            'th_phonetic': 'Dtong-gahn kwahm chuay-leua tahng gahn-phaet duan. Bproht pah pai rong-pha-ya-bahn tee glai tee-soot khrap',
            'vi': 'Tôi cần trợ giúp y tế khẩn cấp. Làm ơn đưa tôi đến bệnh viện gần nhất.',
            'vi_phonetic': 'Toi can tro giup y te khan cap. Lam on dua toi den benh vien gan nhat'
        },
        {
            'en': 'I feel dizzy / I have food poisoning.',
            'th': 'ผมรู้สึกเวียนศีรษะ / น่าจะอาหารเป็นพิษครับ',
            'th_phonetic': 'Phom roo-seuk wian see-sa / ah-hahn bpen phit khrap',
            'vi': 'Tôi bị chóng mặt / Tôi bị ngộ độc thực phẩm.',
            'vi_phonetic': 'Toi bi chong mat / Toi bi ngo doc thuc pham'
        },
        {
            'en': 'Where is the nearest pharmacy?',
            'th': 'ร้านขายยาที่ใกล้ที่สุดอยู่ที่ไหนครับ?',
            'th_phonetic': 'Rahn khai yah tee glai tee-soot yoo tee nai khrap?',
            'vi': 'Hiệu thuốc gần nhất ở đâu?',
            'vi_phonetic': 'Hieu thuoc gan nhat o dau?'
        },
        {
            'en': 'Please call the tourist police.',
            'th': 'โปรดโทรหาตำรวจท่องเที่ยว (1155) ด้วยครับ',
            'th_phonetic': 'Bproht toh hah dtam-ruat thong-thiao neung neung haa haa khrap',
            'vi': 'Làm ơn gọi cảnh sát du lịch giúp tôi.',
            'vi_phonetic': 'Lam on goi canh sat du lich giup toi'
        }
    ],
    'airport_luggage': [
        {
            'en': 'Where is the Airport Rail Link train to Phaya Thai?',
            'th': 'รถไฟฟ้า แอร์พอร์ต เรล ลิงก์ ไปพญาไท อยู่ทางไหนครับ?',
            'th_phonetic': 'Rot-fai-fah Airport Rail Link pai Phaya Thai yoo thahng nai khrap?',
            'vi': 'Tàu Airport Rail Link đi Phaya Thai ở hướng nào?',
            'vi_phonetic': 'Tau Airport Rail Link di Phaya Thai o huong nao?'
        },
        {
            'en': 'I have a suitcase stored at AIRPORTELs on Floor B.',
            'th': 'ผมมีกระเป๋าเดินทางฝากไว้ที่ AIRPORTELs ชั้น B ครับ',
            'th_phonetic': 'Phom mee gra-pao dern-tahng fahk wai tee AIRPORTELs chun bee khrap',
            'vi': 'Tôi có vali gửi tại quầy AIRPORTELs ở tầng B.',
            'vi_phonetic': 'Toi co vali gui tai quay AIRPORTELs o tang B'
        },
        {
            'en': 'Where is the Bangkok Airways domestic check-in counter?',
            'th': 'เคาน์เตอร์เช็คอินในประเทศของ บางกอกแอร์เวย์ส อยู่แถวไหนครับ?',
            'th_phonetic': 'Khown-ter check-in nai bproh-theht khawng Bangkok Airways yoo thaeo nai khrap?',
            'vi': 'Quầy làm thủ tục nội địa của Bangkok Airways ở đâu?',
            'vi_phonetic': 'Quay lam thu tuc noi dia cua Bangkok Airways o dau?'
        },
        {
            'en': 'Where is the Lomprayah High Speed Ferry pier?',
            'th': 'ท่าเรือเรือเร็วลมพระยาไปเกาะเต่า/เกาะพะงัน อยู่ตรงไหนครับ?',
            'th_phonetic': 'Thah-reua reua-reo Lomprayah pai Koh Tao / Koh Phangan yoo dtrong nai khrap?',
            'vi': 'Bến tàu cao tốc Lomprayah ở đâu?',
            'vi_phonetic': 'Ben tau cao toc Lomprayah o dau?'
        }
    ]
}

CURRENCY_BENCHMARKS = {
    'rates': {
        'USD': 1.0,
        'ILS': 3.70,
        'THB': 36.5,
        'VND': 25400.0
    },
    'advisory': [
        'Thai ATM Fee: Every foreign card withdrawal in Thailand incurs a mandatory 220 THB (~$6 USD) local bank fee. Always withdraw the maximum allowed (20,000 to 30,000 THB at yellow Krungsri Bank ATMs) to minimize fee ratio.',
        'Best Bangkok Cash Exchange: SuperRich (Green or Orange booths) located at BTS Phaya Thai, BTS Siam, and Suvarnabhumi Airport Basement (Floor B near ARL ticket gates) offer near-market interbank exchange rates.',
        'Vietnam ATM Fee: TPBank and VPBank ATMs charge 0 VND local ATM withdrawal fee for foreign Visa/Mastercard debit cards.',
        'Dynamic Currency Conversion (DCC) Trap: Always select \"Charge in Local Currency\" (THB or VND) on card machines and ATMs. Never accept the machine conversion rate to USD or ILS, which adds a hidden 4-7% markup!'
    ]
}
