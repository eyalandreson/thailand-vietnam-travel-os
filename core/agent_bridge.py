"""
Antigravity Local Bridge Server (core/agent_bridge.py)
Provides a lightweight HTTP API for the web frontend to communicate directly with
Antigravity and the autonomous agent fixer engine.
Supports CORS for localhost, file://, and GitHub Pages.
"""
import os
import sys
import json
import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from typing import Dict, Any, List

# Ensure project root is in sys.path
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

REQUESTS_FILE = os.path.join(BASE_DIR, "change_requests.json")


def load_change_requests() -> List[Dict[str, Any]]:
    """Loads change requests from persistent JSON storage."""
    if not os.path.exists(REQUESTS_FILE):
        return []
    try:
        with open(REQUESTS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"[AgentBridge] Warning reading {REQUESTS_FILE}: {e}")
        return []


def save_change_requests(requests_list: List[Dict[str, Any]]) -> None:
    """Saves change requests to persistent JSON storage."""
    with open(REQUESTS_FILE, "w", encoding="utf-8") as f:
        json.dump(requests_list, f, indent=2, ensure_ascii=False)


def generate_ticket_id(category: str = "PLAN") -> str:
    """Generates a sequential or timestamp-based ticket ID (e.g. CR-20260911-001)."""
    now = datetime.datetime.utcnow()
    date_str = now.strftime("%Y%m%d")
    existing = load_change_requests()
    count = len([r for r in existing if r.get("id", "").startswith(f"CR-{date_str}")]) + 1
    prefix = "CR" if category.upper() == "PLAN" else "FEAT"
    return f"{prefix}-{date_str}-{count:03d}"


class AgentBridgeHandler(BaseHTTPRequestHandler):
    """HTTP Request Handler for Antigravity Agent Bridge."""

    def _set_headers(self, status_code: int = 200, content_type: str = "application/json"):
        self.send_response(status_code)
        self.send_header("Content-Type", f"{content_type}; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization, X-Requested-With")
        self.end_headers()

    def do_OPTIONS(self):
        """Handle CORS pre-flight requests."""
        self._set_headers(204)

    def do_GET(self):
        """Route GET requests."""
        parsed = urlparse(self.path)
        path = parsed.path

        if path == "/api/status" or path == "/":
            self.handle_status()
        elif path == "/api/change-requests":
            self.handle_list_requests()
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({"error": f"Endpoint not found: {path}"}).encode("utf-8"))

    def do_POST(self):
        """Route POST requests."""
        parsed = urlparse(self.path)
        path = parsed.path

        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length) if content_length > 0 else b"{}"

        try:
            payload = json.loads(body.decode("utf-8")) if body else {}
        except Exception:
            payload = {}

        if path == "/api/change-requests":
            self.handle_create_request(payload)
        elif path.startswith("/api/change-requests/") and path.endswith("/apply"):
            ticket_id = path.split("/")[3]
            self.handle_apply_request(ticket_id)
        elif path == "/api/generate-directive":
            self.handle_generate_directive(payload)
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({"error": f"Endpoint not found: {path}"}).encode("utf-8"))

    def handle_status(self):
        """Returns bridge and Antigravity system health."""
        requests_list = load_change_requests()
        pending = [r for r in requests_list if r.get("status") in ("QUEUED", "PENDING", "PROCESSING")]
        resolved = [r for r in requests_list if r.get("status") == "RESOLVED"]

        status_data = {
            "bridge": "ONLINE",
            "version": "1.0.0",
            "agent": "Antigravity Autonomous Travel OS Agent",
            "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
            "workspace": BASE_DIR,
            "stats": {
                "total_requests": len(requests_list),
                "pending_requests": len(pending),
                "resolved_requests": len(resolved)
            },
            "capabilities": [
                "itinerary_modification",
                "adversarial_critic_audit",
                "dual_blueprint_synchronization",
                "gh_pages_deployment",
                "gemini_directive_generation"
            ]
        }
        self._set_headers(200)
        self.wfile.write(json.dumps(status_data, indent=2).encode("utf-8"))

    def handle_list_requests(self):
        """Returns all change requests."""
        requests_list = load_change_requests()
        self._set_headers(200)
        self.wfile.write(json.dumps({
            "status": "SUCCESS",
            "count": len(requests_list),
            "requests": requests_list
        }, indent=2).encode("utf-8"))

    def handle_create_request(self, payload: Dict[str, Any]):
        """Creates a new change request ticket and queues it for the agent."""
        category = payload.get("category", "plan") # 'plan' or 'site'
        title = payload.get("title", "").strip()
        description = payload.get("description", "").strip()
        day = payload.get("day", None)
        priority = payload.get("priority", "normal")
        submitter = payload.get("submitter", "Traveler").strip() or "Traveler"

        if not title and not description:
            self._set_headers(400)
            self.wfile.write(json.dumps({"error": "Title or description is required"}).encode("utf-8"))
            return

        ticket_id = generate_ticket_id(category)
        now_iso = datetime.datetime.utcnow().isoformat() + "Z"

        new_request = {
            "id": ticket_id,
            "created_at": now_iso,
            "updated_at": now_iso,
            "category": category,
            "priority": priority,
            "target_day": day,
            "title": title or description[:40],
            "description": description,
            "submitter": submitter,
            "status": "QUEUED",
            "agent_resolution": None,
            "critic_audit": None,
            "diff_summary": None,
            "client_meta": payload.get("meta", {})
        }

        requests_list = load_change_requests()
        requests_list.insert(0, new_request)
        save_change_requests(requests_list)

        # Attempt immediate autonomous fix if auto_apply requested or for plan changes
        auto_applied = False
        fix_result = None
        if payload.get("auto_apply", True):
            try:
                from core.agent_fixer import AgentFixerEngine
                fixer = AgentFixerEngine()
                fix_result = fixer.process_ticket(ticket_id)
                auto_applied = fix_result.get("status") == "RESOLVED"
            except Exception as e:
                print(f"[AgentBridge] Auto-apply exception: {e}")

        # Reload updated request
        updated_list = load_change_requests()
        curr_req = next((r for r in updated_list if r.get("id") == ticket_id), new_request)

        self._set_headers(201)
        self.wfile.write(json.dumps({
            "status": "SUCCESS",
            "ticket_id": ticket_id,
            "auto_applied": auto_applied,
            "request": curr_req,
            "fix_result": fix_result
        }, indent=2).encode("utf-8"))

    def handle_apply_request(self, ticket_id: str):
        """Manually or externally triggers the agent fixer on a ticket."""
        try:
            from core.agent_fixer import AgentFixerEngine
            fixer = AgentFixerEngine()
            result = fixer.process_ticket(ticket_id)
            self._set_headers(200)
            self.wfile.write(json.dumps(result, indent=2).encode("utf-8"))
        except Exception as e:
            self._set_headers(500)
            self.wfile.write(json.dumps({"error": str(e)}).encode("utf-8"))

    def handle_generate_directive(self, payload: Dict[str, Any]):
        """Generates a structured Antigravity directive prompt from request details."""
        ticket_id = payload.get("id", "CR-DRAFT")
        category = payload.get("category", "plan")
        day = payload.get("day", "General")
        title = payload.get("title", "")
        description = payload.get("description", "")
        priority = payload.get("priority", "normal")

        prompt = (
            f"# [ANTIGRAVITY DIRECTIVE: {ticket_id}]\n\n"
            f"**Ticket ID**: `{ticket_id}`\n"
            f"**Category**: {category.upper()}\n"
            f"**Target**: Day {day}\n"
            f"**Priority**: {priority.upper()}\n"
            f"**Title**: {title}\n\n"
            f"## Traveler Instructions\n"
            f"{description}\n\n"
            f"## Execution Directives for Antigravity Agent\n"
            f"1. Read `core/itinerary_data.json` and examine target Day {day}.\n"
            f"2. Apply the requested modifications adhering to the travel profile constraints (e.g. Twin beds for Phase 1, Romantic King for Phase 2).\n"
            f"3. Run `core/critic_engine.py` to audit hotels and routes (must score >= 8.5/10).\n"
            f"4. Run `core/sync_engine.py` to synchronize `web/data.json`, `web/itinerary_data.js`, and `web/master_itinerary_doc.html`.\n"
            f"5. Update `{ticket_id}` in `change_requests.json` status to `RESOLVED` with diff summary.\n"
            f"6. Verify with `python -m unittest discover -s tests`.\n"
        )

        self._set_headers(200)
        self.wfile.write(json.dumps({"status": "SUCCESS", "directive": prompt}).encode("utf-8"))


def create_server(host: str = "127.0.0.1", port: int = 5055) -> HTTPServer:
    """Creates an instance of the Antigravity Agent Bridge HTTP server."""
    server_address = (host, port)
    return HTTPServer(server_address, AgentBridgeHandler)


if __name__ == "__main__":
    port = 5055
    if len(sys.argv) > 1 and sys.argv[1].isdigit():
        port = int(sys.argv[1])
    server = create_server("127.0.0.1", port)
    print(f"🚀 Antigravity Agent Bridge running on http://127.0.0.1:{port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping Antigravity Agent Bridge.")
        server.server_close()
