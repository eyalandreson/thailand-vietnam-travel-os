"""
Standalone Cloud Agent Server (cloud_server.py)
Can be run on any cloud platform, container (Docker), Google Cloud Run, Render, or Railway.
Provides a unified CORS-enabled HTTP endpoint on port 8080 (or $PORT).
"""
import os
import sys
import json
from socketserver import ThreadingMixIn
from http.server import HTTPServer, BaseHTTPRequestHandler

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from api.agent_fix import handler, process_cloud_request


class ThreadingHTTPServer(ThreadingMixIn, HTTPServer):
    daemon_threads = True


class CloudServerHandler(handler):
    """Extends Vercel handler with routing for health and status checks."""

    def do_GET(self):
        self._send_cors_headers()
        if self.path in ("/api/health", "/health", "/"):
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({
                "service": "Travel OS Cloud Agent",
                "status": "HEALTHY",
                "env": "production",
                "zero_pairing": True,
                "endpoints": {
                    "agent_fix": "/api/agent_fix",
                    "health": "/api/health"
                }
            }).encode("utf-8"))
        elif self.path in ("/api/agent_fix", "/api/agent-fix", "/api/status"):
            super().do_GET()
        else:
            self.send_response(404)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Route not found"}).encode("utf-8"))

    def do_POST(self):
        if self.path in ("/api/agent_fix", "/api/agent-fix", "/api/change-requests"):
            super().do_POST()
        else:
            self.send_response(404)
            self._send_cors_headers()
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": f"Unknown endpoint {self.path}"}).encode("utf-8"))


def run_server(port: int = 8080):
    port = int(os.environ.get("PORT", port))
    server_address = ("0.0.0.0", port)
    httpd = ThreadingHTTPServer(server_address, CloudServerHandler)
    print(f"==================================================")
    print(f"🚀 Travel OS Cloud Agent Server running on port {port}")
    print(f"   Zero User Pairing: ACTIVE")
    print(f"   Endpoints: POST /api/agent_fix | GET /api/health")
    print(f"==================================================")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping Cloud Agent Server...")
        httpd.server_close()


if __name__ == "__main__":
    port_arg = 8080
    if len(sys.argv) > 1 and sys.argv[1].isdigit():
        port_arg = int(sys.argv[1])
    run_server(port_arg)
