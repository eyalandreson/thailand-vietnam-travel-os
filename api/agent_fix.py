"""
Serverless Cloud Agent Endpoint (api/agent_fix.py)
Unified Cloud Backend for Thailand & Vietnam Travel OS
Accepts change requests from any mobile or desktop client with ZERO user pairing.
Executes Gemini Flash reasoning, audits against 3-Pass Adversarial Critic,
commits updates to GitHub repository via GitHub REST API, and returns live itinerary.
"""
import os
import sys
import json
import base64
import urllib.request
import urllib.error
from http.server import BaseHTTPRequestHandler
from typing import Dict, Any, Optional

# Ensure project root is in sys.path
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

try:
    from dotenv import load_dotenv
    load_dotenv(os.path.join(BASE_DIR, ".env"))
except Exception:
    pass

from core.agent_fixer import AgentFixerEngine


def commit_file_to_github(repo: str, file_path: str, content_str: str, commit_message: str, pat: str, branch: str = "main") -> bool:
    """Commits an updated file to GitHub repository using the GitHub Contents API."""
    if not pat or not repo:
        return False

    url = f"https://api.github.com/repos/{repo}/contents/{file_path}?ref={branch}"
    headers = {
        "Authorization": f"Bearer {pat}",
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "TravelOS-Cloud-Agent"
    }

    sha = None
    try:
        req = urllib.request.Request(url, headers=headers, method="GET")
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            sha = data.get("sha")
    except Exception as e:
        print(f"[CloudAgent] Notice: Could not fetch existing SHA for {file_path}: {e}")

    payload = {
        "message": commit_message,
        "content": base64.b64encode(content_str.encode("utf-8")).decode("utf-8"),
        "branch": branch
    }
    if sha:
        payload["sha"] = sha

    put_url = f"https://api.github.com/repos/{repo}/contents/{file_path}"
    try:
        data_bytes = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(put_url, data=data_bytes, headers=headers, method="PUT")
        with urllib.request.urlopen(req, timeout=15) as resp:
            return resp.status in (200, 201)
    except Exception as e:
        print(f"[CloudAgent] Error committing {file_path} to GitHub: {e}")
        return False


def process_cloud_request(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Unified entrypoint for processing change requests in the cloud.
    Executes AgentFixerEngine, synchronizes datasets, and commits to GitHub.
    """
    fixer = AgentFixerEngine()
    ticket_id = payload.get("id") or f"CR-{os.urandom(4).hex().upper()}"
    category = payload.get("category", "plan").lower()
    title = payload.get("title", "Travel Plan Modification")
    description = payload.get("description", "")
    target_day = payload.get("target_day")
    submitter = payload.get("submitter", "Traveler")

    ticket = {
        "id": ticket_id,
        "created_at": payload.get("created_at") or "2026-09-11T00:00:00Z",
        "category": category,
        "target_day": target_day,
        "priority": payload.get("priority", "normal"),
        "title": title,
        "description": description,
        "submitter": submitter,
        "status": "PROCESSING"
    }

    # Execute agent fixer logic
    combined_text = f"{title}\n{description}"
    if category == "plan":
        result = fixer._process_plan_change(ticket, combined_text)
    else:
        result = fixer._process_site_change(ticket, combined_text)

    # Load the updated itinerary to return to client
    updated_itinerary = fixer.load_itinerary()

    # Commit updated dataset to GitHub repository if GITHUB_PAT is present
    repo_name = os.environ.get("GITHUB_REPOSITORY", "eyalandreson/thailand-vietnam-travel-os")
    pat = os.environ.get("GITHUB_PAT") or os.environ.get("GITHUB_TOKEN")

    github_committed = False
    if pat and result.get("status") == "RESOLVED":
        itinerary_json_str = json.dumps(updated_itinerary, indent=2, ensure_ascii=False)
        commit_msg = f"feat(travel-os): cloud agent resolved {ticket_id} ({title}) [skip ci]"
        
        # 1. Commit to main branch (repository source of truth)
        github_committed = commit_file_to_github(repo_name, "core/itinerary_data.json", itinerary_json_str, commit_msg, pat, branch="main")
        commit_file_to_github(repo_name, "web/data.json", itinerary_json_str, commit_msg, pat, branch="main")
        
        # 2. Commit to gh-pages branch (live GitHub Pages site instantly reflects changes)
        try:
            commit_file_to_github(repo_name, "data.json", itinerary_json_str, commit_msg, pat, branch="gh-pages")
            js_data = f"// Autonomous Live Blueprint Data Sync\nwindow.TRAVEL_OS_DATA = {itinerary_json_str};\n"
            commit_file_to_github(repo_name, "itinerary_data.js", js_data, commit_msg, pat, branch="gh-pages")
        except Exception as e:
            print(f"[CloudAgent] Notice: gh-pages sync: {e}")

    return {
        "status": result.get("status", "RESOLVED"),
        "ticket_id": ticket_id,
        "resolution": result.get("resolution"),
        "critic_audit": result.get("critic_audit"),
        "diff_summary": result.get("diff_summary", []),
        "itinerary": updated_itinerary,
        "github_committed": github_committed
    }


class handler(BaseHTTPRequestHandler):
    """Vercel Serverless Function Handler"""

    def _send_cors_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization, X-Requested-With")

    def do_OPTIONS(self):
        self.send_response(200)
        self._send_cors_headers()
        self.end_headers()

    def do_GET(self):
        self.send_response(200)
        self._send_cors_headers()
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        response = {
            "service": "Travel OS Cloud Agent",
            "status": "ONLINE",
            "capabilities": ["gemini_flash", "adversarial_critic", "github_sync"]
        }
        self.wfile.write(json.dumps(response).encode("utf-8"))

    def do_POST(self):
        try:
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length)
            payload = json.loads(body.decode("utf-8"))
        except Exception as e:
            self.send_response(400)
            self._send_cors_headers()
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": f"Invalid JSON payload: {str(e)}"}).encode("utf-8"))
            return

        try:
            res = process_cloud_request(payload)
            self.send_response(200)
            self._send_cors_headers()
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(res).encode("utf-8"))
        except Exception as e:
            self.send_response(500)
            self._send_cors_headers()
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "ERROR", "error": str(e)}).encode("utf-8"))
