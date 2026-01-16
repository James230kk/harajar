"""
Example usage of the Haraj scraper
"""

from haraj_scraper import HarajScraper
from haraj_scraper_selenium import HarajScraperSelenium
import json

# Example 1: Scrape a single listing using BeautifulSoup
print("Example 1: Scraping single listing with BeautifulSoup")
scraper = HarajScraper(output_dir="example_output", download_images=True)

listing_url = "https://haraj.com.sa/11173528712/هيلكس_غمارتين/"
listing_data = scraper.scrape_listing(listing_url)

if listing_data:
    print("\nScraped Data:")
    print(json.dumps(listing_data, ensure_ascii=False, indent=2))
    scraper.save_to_json([listing_data], "example_listing.json")

# Example 2: Scrape multiple listings from a category
print("\n\nExample 2: Scraping category with BeautifulSoup")
category_url = "https://haraj.com.sa/tags/حراج السيارات"
listings = scraper.scrape_category(category_url, max_listings=5, max_pages=2)

if listings:
    print(f"\nScraped {len(listings)} listings")
    scraper.save_to_json(listings, "example_category.json")
    scraper.save_to_csv(listings, "example_category.csv")

# Example 3: Using Selenium version (uncomment to use)
"""
print("\n\nExample 3: Scraping with Selenium")
selenium_scraper = HarajScraperSelenium(
    output_dir="example_output_selenium",
    download_images=True,
    headless=True
)

try:
    listing_data_selenium = selenium_scraper.scrape_listing(listing_url)
    if listing_data_selenium:
        print("\nScraped Data (Selenium):")
        print(json.dumps(listing_data_selenium, ensure_ascii=False, indent=2))
finally:
    selenium_scraper.close()
"""

print("\n\nExamples completed! Check the 'example_output' directory for results.")
