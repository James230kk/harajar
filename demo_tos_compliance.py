"""
Demonstration script showing ToS compliance features
This script scrapes multiple listings and shows how the scraper
applies compliance measures after every 10 listings.
"""

import sys
import io
from haraj_scraper import HarajScraper
import json

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

def main():
    print("=" * 70)
    print("Haraj Scraper - ToS Compliance Demonstration")
    print("=" * 70)
    print("\nThis script demonstrates how the scraper applies compliance")
    print("measures after every 10 listings to respect Haraj.com.sa's ToS:")
    print("  - User-Agent rotation")
    print("  - Extended delays (30-60 seconds)")
    print("  - Session reset (every 20 listings)")
    print("  - Random delays between requests")
    print("\n" + "=" * 70 + "\n")
    
    # Initialize scraper
    scraper = HarajScraper(
        output_dir="demo_output",
        download_images=False  # Skip images for faster demo
    )
    
    # Example category URL - you can change this
    category_url = "https://haraj.com.sa/tags/حراج السيارات"
    
    print(f"Scraping category: {category_url}")
    print("Setting max_listings to 15 to demonstrate ToS compliance at 10th listing")
    print("\nStarting scrape...\n")
    
    # Scrape 15 listings to see the ToS compliance kick in at listing 10
    listings = scraper.scrape_category(
        category_url,
        max_listings=15,
        max_pages=2
    )
    
    if listings:
        print("\n" + "=" * 70)
        print(f"Scraping completed! Extracted {len(listings)} listings")
        print("=" * 70)
        
        # Save results
        scraper.save_to_json(listings, "demo_listings.json")
        scraper.save_to_csv(listings, "demo_listings.csv")
        
        # Show summary
        print("\nSummary:")
        print(f"  - Total listings: {len(listings)}")
        print(f"  - Listings with titles: {sum(1 for l in listings if l.get('title'))}")
        print(f"  - Listings with descriptions: {sum(1 for l in listings if l.get('description'))}")
        print(f"  - Listings with prices: {sum(1 for l in listings if l.get('price'))}")
        print(f"  - Total images found: {sum(len(l.get('images', [])) for l in listings)}")
        
        print("\nToS Compliance Events:")
        print(f"  - User-Agent rotations: {scraper.listing_count // 10}")
        print(f"  - Extended delays applied: {scraper.listing_count // 10}")
        if scraper.listing_count >= 20:
            print(f"  - Session resets: {scraper.listing_count // 20}")
        
        print("\nResults saved to:")
        print("  - demo_output/demo_listings.json")
        print("  - demo_output/demo_listings.csv")
    else:
        print("\nNo listings were extracted. This might be due to:")
        print("  - Network issues")
        print("  - Website structure changes")
        print("  - Rate limiting")
        print("\nTry using the Selenium version: haraj_scraper_selenium.py")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nScraping interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\nERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
