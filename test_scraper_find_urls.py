"""Test finding listing URLs"""
import sys
import io

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from haraj_scraper_selenium import HarajScraperSelenium

print("Testing listing URL finding...")
print("=" * 70)

scraper = HarajScraperSelenium(
    output_dir="test_output",
    download_images=False,
    headless=True
)

try:
    category_url = "https://haraj.com.sa/tags/حراج السيارات"
    print(f"Testing URL: {category_url}")
    
    listing_urls = scraper.find_listing_urls(category_url, max_pages=2)
    
    print(f"\nFound {len(listing_urls)} listing URLs")
    
    if listing_urls:
        print("\nFirst 5 URLs:")
        for i, url in enumerate(listing_urls[:5], 1):
            print(f"  {i}. {url}")
        print("\nSUCCESS: URLs found!")
    else:
        print("\nERROR: No URLs found!")
        print("Possible issues:")
        print("  - Website structure changed")
        print("  - Network/connection issues")
        print("  - JavaScript not loading properly")
        
except Exception as e:
    print(f"\nERROR: {e}")
    import traceback
    traceback.print_exc()
finally:
    scraper.close()
