"""Run this to verify dashboard API routes without starting the server."""
import sys
from pathlib import Path

# Run from project root
if not Path("dashboard.py").exists():
    print("Run this from the project root (where dashboard.py is).")
    sys.exit(1)

try:
    from dashboard import app
except Exception as e:
    print(f"Failed to load dashboard: {e}")
    sys.exit(1)

api_routes = sorted(r.rule for r in app.url_map.iter_rules() if r.rule.startswith("/api/"))
required = ["/api/estimate-time", "/api/save-listings"]
missing = [r for r in required if r not in api_routes]

if missing:
    print("Missing routes:", missing)
    print("Registered API routes:", api_routes)
    sys.exit(1)

print("OK: /api/estimate-time and /api/save-listings are registered.")
print("If the browser still gets 404, restart the server from this folder:")
print("  1. Stop the current process (Ctrl+C)")
print("  2. Run: python dashboard.py   or   python start_dashboard.py")
