"""Test the dashboard"""
import sys
import io
from pathlib import Path

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Test imports
try:
    from flask import Flask
    print("✓ Flask imported successfully")
except ImportError as e:
    print(f"✗ Flask import error: {e}")
    sys.exit(1)

# Test template directory
templates_dir = Path("templates")
if templates_dir.exists():
    print("✓ Templates directory exists")
    if (templates_dir / "dashboard.html").exists():
        print("✓ dashboard.html exists")
    else:
        print("✗ dashboard.html not found")
else:
    print("✗ Templates directory not found")

# Test data directory
data_dir = Path("scraped_data")
data_dir.mkdir(exist_ok=True)
print(f"✓ Data directory: {data_dir.absolute()}")

# Test loading dashboard
try:
    from dashboard import app, load_listings
    print("✓ Dashboard module imported")
    
    listings = load_listings()
    print(f"✓ Loaded {len(listings)} listings")
    
    # Test Flask app
    with app.test_client() as client:
        response = client.get('/')
        print(f"✓ Dashboard route returns: {response.status_code}")
        if response.status_code == 200:
            print("✓ Dashboard is working!")
        else:
            print(f"✗ Dashboard returned error: {response.status_code}")
            print(f"  Response: {response.data[:200]}")
            
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()
