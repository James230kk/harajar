"""Test all imports"""
import sys
import io

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

try:
    from dashboard import app, run_scraper
    print("OK: Dashboard imports OK")
except Exception as e:
    print(f"ERROR: Dashboard import error: {e}")

try:
    from haraj_scraper_selenium import HarajScraperSelenium
    print("OK: Selenium scraper imports OK")
except Exception as e:
    print(f"ERROR: Selenium scraper import error: {e}")

print("\nAll dependencies should be installed now!")
