"""Restart dashboard and verify it works"""
import sys
import io
import subprocess
import time
import requests
from pathlib import Path

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

print("=" * 70)
print("Restarting Dashboard")
print("=" * 70)

# Check if port 5000 is in use
try:
    result = subprocess.run(['netstat', '-ano'], capture_output=True, text=True)
    if ':5000' in result.stdout:
        print("⚠️  Port 5000 is already in use")
        print("   Please stop any running dashboard (Ctrl+C) and try again")
        print("\nOr the dashboard is already running!")
        print("   Try accessing: http://localhost:5000")
        sys.exit(0)
except:
    pass

# Check templates
if not Path("templates/dashboard.html").exists():
    print("✗ Error: templates/dashboard.html not found!")
    sys.exit(1)

print("✓ Templates found")

# Check Flask
try:
    import flask
    print(f"✓ Flask {flask.__version__} installed")
except ImportError:
    print("✗ Flask not installed. Run: pip install flask")
    sys.exit(1)

# Create data directory
Path("scraped_data").mkdir(exist_ok=True)
print("✓ Data directory ready")

# Test dashboard import
try:
    from dashboard import app
    print("✓ Dashboard module loaded")
except Exception as e:
    print(f"✗ Error loading dashboard: {e}")
    sys.exit(1)

# Test route
try:
    with app.test_client() as client:
        response = client.get('/')
        if response.status_code == 200:
            print("✓ Dashboard route working")
        else:
            print(f"✗ Dashboard returned: {response.status_code}")
except Exception as e:
    print(f"✗ Error testing route: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 70)
print("Starting Dashboard Server...")
print("=" * 70)
print("\n📊 Dashboard will be available at:")
print("   http://localhost:5000")
print("   http://127.0.0.1:5000")
print("\n💡 If the page shows 'No data', run:")
print("   python run_scrape.py")
print("\n" + "=" * 70 + "\n")

# Start the server
from dashboard import app
app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)
