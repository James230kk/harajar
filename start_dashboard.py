"""Start the dashboard server"""
import sys
import io
from pathlib import Path

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Verify setup
if not Path("templates/dashboard.html").exists():
    print("✗ ERROR: templates/dashboard.html not found!")
    print("   Make sure you're in the project directory")
    sys.exit(1)

try:
    from dashboard import app
except Exception as e:
    print(f"✗ ERROR loading dashboard: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

if __name__ == '__main__':
    # Create data directory
    Path("scraped_data").mkdir(exist_ok=True)
    
    # Ensure config file directory exists (for production)
    config_dir = Path(__file__).parent.absolute()
    config_dir.mkdir(parents=True, exist_ok=True)
    
    print("=" * 70)
    print("🚀 Starting Haraj Scraper Dashboard")
    print("=" * 70)
    print("\n📊 Dashboard URLs:")
    print("   http://localhost:5000")
    print("   http://127.0.0.1:5000")
    print("\n📁 Data directory: scraped_data/")
    
    # Check if data exists
    if Path("scraped_data/listings.json").exists():
        print("✓ Found scraped data")
    else:
        print("⚠️  No data found yet")
        print("\n💡 To scrape data, run:")
        print("   python run_scrape.py")
    
    print("\n" + "=" * 70)
    print("Press Ctrl+C to stop the server")
    print("=" * 70 + "\n")
    
    try:
        app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)
    except OSError as e:
        if "Address already in use" in str(e) or "Only one usage" in str(e):
            print("\n✗ ERROR: Port 5000 is already in use!")
            print("   Another dashboard instance is running.")
            print("   Stop it first or use a different port.")
        else:
            print(f"\n✗ ERROR: {e}")
        sys.exit(1)
