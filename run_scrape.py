"""Script to run a real scrape"""
import sys
import io
from haraj_scraper_selenium import HarajScraperSelenium

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

print("Starting real scrape...")
print("=" * 70)

scraper = HarajScraperSelenium(
    output_dir="scraped_data",
    download_images=False,  # Skip images for faster scraping
    headless=True
)

try:
    # Scrape real listings
    category_url = "https://haraj.com.sa/tags/حراج السيارات"
    listings = scraper.scrape_category(
        category_url,
        max_listings=10,  # Scrape 10 real listings
        max_pages=2
    )
    
    if listings:
        scraper.save_to_json(listings, "listings.json")
        scraper.save_to_csv(listings, "listings.csv")
        print(f"\n✓ Successfully scraped {len(listings)} real listings!")
        print("Data saved to scraped_data/listings.json")
    else:
        print("\n✗ No listings were scraped")
finally:
    scraper.close()
