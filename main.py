"""
ORBITAL PULSE
NASA Space Apps Challenge 2026 — Master Project Proposal Implementation
A Story-Driven, Multidisciplinary Space Mission Design & Crisis Simulation Game

Main application entry point.
"""

import sys
import argparse
import webbrowser
import uvicorn


def parse_args():
    parser = argparse.ArgumentParser(description="ORBITAL PULSE - NASA Space Apps Challenge 2026")
    parser.add_argument("--host", default="0.0.0.0", help="Host interface (default: 0.0.0.0)")
    parser.add_argument("--port", type=int, default=8080, help="Port to bind (default: 8080)")
    parser.add_argument("--reload", action="store_true", help="Enable live auto-reload for development")
    parser.add_argument("--no-browser", action="store_true", help="Do not open web browser automatically")
    return parser.parse_args()


def main():
    args = parse_args()
    url = f"http://localhost:{args.port}"

    print("=" * 72)
    print("   🌌 ORBITAL PULSE — NASA SPACE APPS CHALLENGE 2026")
    print("   Space Mission Design & Crisis Simulation Game")
    print("   Modeled after NASA MDL & JPL Concept Maturity Levels (CML 1-5)")
    print("=" * 72)
    print(f"   [+] Server running at: {url}")
    print(f"   [+] WebSocket endpoint: ws://localhost:{args.port}/ws/<room>/<player>/<name>")
    print("=" * 72)

    if not args.no_browser:
        try:
            webbrowser.open(url)
        except Exception:
            pass

    uvicorn.run(
        "orbital_pulse.server.app:app",
        host=args.host,
        port=args.port,
        reload=args.reload
    )


if __name__ == "__main__":
    main()
