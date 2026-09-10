"""
Antigravity Agent Bridge Server CLI Launcher
Usage:
    python agent_bridge_server.py [--port 5055]
"""
import sys
import argparse
from core.agent_bridge import create_server

def main():
    parser = argparse.ArgumentParser(description="Antigravity Agent Bridge Server for Thailand & Vietnam Travel OS")
    parser.add_argument("--host", default="127.0.0.1", help="Host interface to bind (default: 127.0.0.1)")
    parser.add_argument("--port", type=int, default=5055, help="Port to listen on (default: 5055)")
    args = parser.parse_args()

    server = create_server(args.host, args.port)
    print(f"================================================================")
    print(f"⚡ ANTIGRAVITY AGENT BRIDGE RUNNING AT http://{args.host}:{args.port}")
    print(f"Endpoints:")
    print(f"  - GET  /api/status            : Bridge health & Antigravity status")
    print(f"  - GET  /api/change-requests   : List all submitted change requests")
    print(f"  - POST /api/change-requests   : Submit new change request (auto-resolves)")
    print(f"================================================================")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping Antigravity Agent Bridge Server.")
        server.server_close()

if __name__ == "__main__":
    main()
