"""
Quick test script to verify the scraper is working
"""

import sys
import io
from haraj_scraper import HarajScraper

# Fix Windows console encoding for Arabic text
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

def test_scraper():
    """Test the scraper with a single listing"""
    print("Testing Haraj Scraper...")
    print("=" * 50)
    
    # Initialize scraper
    scraper = HarajScraper(output_dir="test_output", download_images=False)
    
    # Test URL (you can change this to any valid listing URL)
    test_url = "https://haraj.com.sa/11173528712/هيلكس_غمارتين/"
    
    print(f"Testing URL: {test_url}")
    print("Fetching page...")
    
    # Scrape the listing
    listing_data = scraper.scrape_listing(test_url)
    
    if not listing_data:
        print("FAILED: No data extracted")
        return False
    
    # Check if we got the essential fields
    required_fields = ['listing_id', 'title', 'url']
    missing_fields = [field for field in required_fields if not listing_data.get(field)]
    
    if missing_fields:
        print(f"WARNING: Missing fields: {missing_fields}")
    else:
        print("All required fields present")
    
    # Display results
    print("\nExtracted Data:")
    print("-" * 50)
    print(f"Listing ID: {listing_data.get('listing_id', 'N/A')}")
    print(f"Title: {listing_data.get('title', 'N/A')}")
    print(f"Description: {listing_data.get('description', 'N/A')[:100]}...")
    print(f"City: {listing_data.get('city', 'N/A')}")
    print(f"Seller: {listing_data.get('seller_name', 'N/A')}")
    print(f"Images found: {len(listing_data.get('images', []))}")
    print(f"Tags: {', '.join(listing_data.get('tags', [])[:3])}")
    
    # Save test results
    scraper.save_to_json([listing_data], "test_result.json")
    print("\nTest completed! Results saved to test_output/test_result.json")
    
    return True

if __name__ == "__main__":
    try:
        success = test_scraper()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
