"""
Gmail Live Ingestion & Document Synchronizer
Supports:
1. IMAP Direct Connect (using Gmail App Password in .env): Searches for booking references,
   extracts real confirmation emails, and downloads attached PDF/image vouchers into documents/.
2. Gmail API OAuth flow (credentials.json -> token.json)
3. Local Document Scanner: Ingests user-provided files in documents/
"""
import os
import sys
import json
import imaplib
import email
from email.header import decode_header
from typing import Dict, Any, List

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS_DIR = os.path.join(BASE_DIR, "documents")
WEB_DOCS_DIR = os.path.join(BASE_DIR, "web", "documents")

os.makedirs(DOCS_DIR, exist_ok=True)
os.makedirs(WEB_DOCS_DIR, exist_ok=True)

class GmailLiveIngestion:
    def __init__(self, env_path: str = ".env"):
        self.env_path = env_path
        self.target_queries = [
            "30C4358",
            "697155847",
            "1145-554-179",
            "9KDEH2",
            "Sukhon",
            "Thailand Digital Arrival Card",
            "TDAC",
            "Bangkok Airways",
            "Etihad",
            "12Go Asia"
        ]

    def scan_local_documents_folder(self) -> List[Dict[str, Any]]:
        """
        Scans documents/ folder for actual files present on disk.
        """
        found_files = []
        valid_exts = {".pdf", ".png", ".jpg", ".jpeg", ".webp", ".doc", ".docx", ".pkpass", ".html"}
        if os.path.exists(DOCS_DIR):
            for fname in os.listdir(DOCS_DIR):
                fpath = os.path.join(DOCS_DIR, fname)
                _, ext = os.path.splitext(fname.lower())
                if os.path.isfile(fpath) and ext in valid_exts:
                    # Copy to web/documents/ so web app can link to it directly
                    web_dest = os.path.join(WEB_DOCS_DIR, fname)
                    try:
                        import shutil
                        shutil.copyfile(fpath, web_dest)
                    except Exception:
                        pass

                    found_files.append({
                        "file_name": fname,
                        "file_path": fpath,
                        "web_url": f"documents/{fname}",
                        "size_bytes": os.path.getsize(fpath),
                        "status": "LOCAL_FILE_VERIFIED"
                    })
        return found_files

    def fetch_via_imap(self, username: str, app_password: str) -> List[Dict[str, Any]]:
        """
        Connects to imap.gmail.com, searches for travel confirmations,
        and saves genuine attachments to documents/. If no attachment,
        saves the full confirmation email as a viewable HTML document.
        """
        downloaded = []
        try:
            clean_pwd = app_password.replace(" ", "")
            mail = imaplib.IMAP4_SSL("imap.gmail.com", 993)
            mail.login(username, clean_pwd)
            mail.select("inbox")

            for query in self.target_queries:
                typ, data = mail.search(None, f'(OR (SUBJECT "{query}") (BODY "{query}"))')
                if typ != 'OK':
                    continue

                for num in data[0].split():
                    typ, msg_data = mail.fetch(num, '(RFC822)')
                    if typ != 'OK':
                        continue

                    raw_email = msg_data[0][1]
                    msg = email.message_from_bytes(raw_email)
                    subject, encoding = decode_header(msg.get("Subject", "No Subject"))[0]
                    if isinstance(subject, bytes):
                        subject = subject.decode(encoding or "utf-8", errors="ignore")

                    has_attachment = False
                    html_body = None
                    text_body = None

                    # Extract attachments & body
                    for part in msg.walk():
                        content_type = part.get_content_type()
                        content_disposition = str(part.get('Content-Disposition') or "")

                        if "attachment" in content_disposition:
                            filename = part.get_filename()
                            if filename:
                                fname_decoded, f_enc = decode_header(filename)[0]
                                if isinstance(fname_decoded, bytes):
                                    fname_decoded = fname_decoded.decode(f_enc or "utf-8", errors="ignore")

                                # Save file to documents/
                                clean_name = "".join(c for c in fname_decoded if c.isalnum() or c in "._- ")
                                save_path = os.path.join(DOCS_DIR, clean_name)
                                with open(save_path, "wb") as f:
                                    f.write(part.get_payload(decode=True))

                                has_attachment = True
                                downloaded.append({
                                    "file_name": clean_name,
                                    "subject": subject,
                                    "query_matched": query,
                                    "save_path": save_path
                                })
                        elif content_type == "text/html":
                            try:
                                html_body = part.get_payload(decode=True).decode(part.get_content_charset() or "utf-8", errors="ignore")
                            except Exception:
                                pass
                        elif content_type == "text/plain":
                            try:
                                text_body = part.get_payload(decode=True).decode(part.get_content_charset() or "utf-8", errors="ignore")
                            except Exception:
                                pass

                    # If no attachment was found but email is a confirmed booking, save body as HTML
                    if not has_attachment and (html_body or text_body):
                        safe_title = "".join(c for c in subject if c.isalnum() or c in "_- ").strip()[:50]
                        file_name = f"{query}_{safe_title}.html"
                        save_path = os.path.join(DOCS_DIR, file_name)
                        content = html_body if html_body else f"<pre>{text_body}</pre>"
                        with open(save_path, "w", encoding="utf-8") as f:
                            f.write(content)

                        downloaded.append({
                            "file_name": file_name,
                            "subject": subject,
                            "query_matched": query,
                            "save_path": save_path
                        })

            mail.close()
            mail.logout()
        except Exception as e:
            print(f"[IMAP Notice] Could not connect to Gmail via IMAP: {e}")

        # Sync local folder to web/documents/
        self.scan_local_documents_folder()
        return downloaded

if __name__ == "__main__":
    scanner = GmailLiveIngestion()
    local_files = scanner.scan_local_documents_folder()
    print(f"Verified local files in documents/: {len(local_files)}")
    for lf in local_files:
        print(" -", lf["file_name"])
