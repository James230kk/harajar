"""Test phone number extraction from contact button"""
import sys
import io

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from haraj_scraper_selenium import HarajScraperSelenium

print("Testing phone number extraction...")
print("=" * 70)

# Test with a real listing URL
test_urls = [
    "https://haraj.com.sa/11173530291/لوحه_ASU_معروضه_في_ابشر/",
    "https://haraj.com.sa/11173530290/للبيع_مرسيدس_CLS/",
]

scraper = HarajScraperSelenium(
    output_dir="test_output",
    download_images=False,
    headless=False  # Visible to see what's happening
)

try:
    for url in test_urls[:1]:  # Test first one
        print(f"\nTesting: {url}")
        listing_data = scraper.scrape_listing(url)
        
        print(f"\nExtracted Data:")
        print(f"  Title: {listing_data.get('title', 'N/A')}")
        print(f"  Seller: {listing_data.get('seller_name', 'N/A')}")
        print(f"  Contact Info:")
        contact_info = listing_data.get('contact_info', {})
        if contact_info.get('phone_numbers'):
            print(f"    Phone: {contact_info['phone_numbers']}")
        else:
            print(f"    Phone: NOT FOUND")
        print(f"    Contact Extracted: {contact_info.get('contact_extracted', False)}")
        
        if contact_info.get('phone_numbers'):
            print("\n✓ SUCCESS: Phone number extracted!")
        else:
            print("\n✗ FAILED: No phone number found")
            
except Exception as e:
    print(f"\nERROR: {e}")
    import traceback
    traceback.print_exc()
finally:
    scraper.close()
