# Travel Documents Repository

Drop your real travel vouchers, e-tickets, and passes directly into this folder (documents/).

### Supported Document Types:
- **TDAC**: Thailand Digital Arrival Card confirmation / PDF / screenshot
- **Flight Tickets**: Bangkok -> Hanoi, Hanoi -> Bangkok, Bangkok -> Tel Aviv, etc.
- **Hotel Vouchers**: Sukhon Hotel Bangkok, or any newly booked accommodations
- **Visas**: Vietnam E-Visa approval PDF
- **Tour & Transit Vouchers**: Easy-Rider bookings, Cat Ba cruise vouchers, ferry tickets, AIRPORTELs storage slips

### How It Works:
1. When you drop a file here (e.g. TDAC_30C4358.pdf or Sukhon_Hotel_697155847.pdf), run python core/gmail_auth_ingest.py or python core/sync_engine.py.
2. The synchronizer will copy the file to web/documents/ and link the verified download button directly in your web dashboard and Google Doc view.
3. Alternatively, if you add your GMAIL_USER and GMAIL_APP_PASSWORD to .env, core/gmail_auth_ingest.py can automatically scan your Gmail inbox and download confirmed attachments directly.
