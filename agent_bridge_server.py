"""
Antigravity Agent Bridge Server CLI Launcher
Usage:
    python agent_bridge_server.py [--port 5055]
"""
import sys
import argparse

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from core.agent_bridge import create_server

def main():
    parser = argparse.ArgumentParser(description="Antigravity Agent Bridge Server for Thailand & Vietnam Travel OS")
    parser.add_argument("--host", default="127.0.0.1", help="Host interface to bind (default: 127.0.0.1)")
    parser.add_argument("--port", type=int, default=5055, help="Port to listen on (default: 5055)")
    args = parser.parse_args()

    server = create_server(args.host, args.port)
    print("================================================================")
    print(f"[ONLINE] Antigravity Agent Bridge running at http://{args.host}:{args.port}")
    print("Endpoints:")
    print("  - GET  /api/status            : Bridge health & Antigravity status")
    print("  - GET  /api/change-requests   : List all submitted change requests")
    print("  - POST /api/change-requests   : Submit new change request (auto-resolves)")
    print("================================================================")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping Antigravity Agent Bridge Server.")
        server.server_close()

if __name__ == "__main__":
    main()
