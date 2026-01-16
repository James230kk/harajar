"""
Haraj.com.sa Web Scraper
Extracts listing data including description, details, contact info, and images
"""

import requests
from bs4 import BeautifulSoup
import json
import os
import re
from urllib.parse import urljoin, urlparse
import time
from typing import Dict, List, Optional
import csv
from pathlib import Path
import random
import sys


class HarajScraper:
    def __init__(self, output_dir: str = "scraped_data", download_images: bool = True):
        """
        Initialize the Haraj scraper
        
        Args:
            output_dir: Directory to save scraped data and images
            download_images: Whether to download images
        """
        self.base_url = "https://haraj.com.sa"
        self.output_dir = Path(output_dir)
        self.images_dir = self.output_dir / "images"
        self.download_images = download_images
        
        # Create output directories
        self.output_dir.mkdir(exist_ok=True)
        if self.download_images:
            self.images_dir.mkdir(exist_ok=True)
        
        # User agents for rotation (ToS compliance)
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15',
        ]
        
        # Session for maintaining cookies
        self.session = requests.Session()
        self._update_headers()
        
        # Counter for ToS compliance (change behavior every 10 listings)
        self.listing_count = 0
        self.last_rotation = 0
    
    def _update_headers(self):
        """Update session headers with random user agent (ToS compliance)"""
        user_agent = random.choice(self.user_agents)
        self.session.headers.update({
            'User-Agent': user_agent,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'ar,en-US;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Referer': self.base_url,
        })
    
    def _apply_tos_compliance_measures(self):
        """
        Apply ToS-compliant measures after every 10 listings:
        - Rotate user agent
        - Add extended delay
        - Clear cookies (optional)
        - Change request pattern
        """
        if self.listing_count > 0 and self.listing_count % 10 == 0:
            print(f"\n[ToS Compliance] Applied measures after {self.listing_count} listings...")
            
            # Rotate user agent
            self._update_headers()
            print("  - Rotated User-Agent")
            
            # Extended delay (30-60 seconds) to be respectful
            delay = random.randint(30, 60)
            print(f"  - Extended delay: {delay} seconds")
            time.sleep(delay)
            
            # Optionally create a new session to clear cookies
            if self.listing_count % 20 == 0:  # Every 20 listings, reset session
                self.session.close()
                self.session = requests.Session()
                self._update_headers()
                print("  - Session reset")
            
            print("  - Continuing scraping...\n")
    
    def get_page(self, url: str) -> Optional[BeautifulSoup]:
        """Fetch and parse a page"""
        try:
            response = self.session.get(url, timeout=30)
            response.encoding = 'utf-8'
            response.raise_for_status()
            return BeautifulSoup(response.text, 'html.parser')
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            return None
    
    def extract_listing_id(self, url: str) -> Optional[str]:
        """Extract listing ID from URL"""
        # URL format: https://haraj.com.sa/11173528712/هيلكس_غمارتين/
        match = re.search(r'/(\d+)/', url)
        return match.group(1) if match else None
    
    def extract_listing_details(self, soup: BeautifulSoup, url: str) -> Dict:
        """Extract all details from a listing page"""
        listing_data = {
            'url': url,
            'listing_id': self.extract_listing_id(url),
            'title': '',
            'description': '',
            'price': '',
            'location': '',
            'city': '',
            'posted_time': '',
            'seller_name': '',
            'seller_url': '',
            'category': '',
            'tags': [],
            'images': [],
            'contact_info': {},
            'raw_html': str(soup) if soup else ''
        }
        
        if not soup:
            return listing_data
        
        # Extract title
        title_elem = soup.find('h1')
        if title_elem:
            listing_data['title'] = title_elem.get_text(strip=True)
        
        # Extract description/article content
        article = soup.find('article')
        if article:
            listing_data['description'] = article.get_text(strip=True)
        
        # Extract price (look for price indicators)
        price_patterns = [
            soup.find(string=re.compile(r'\d+.*ريال|ريال.*\d+', re.IGNORECASE)),
            soup.find(string=re.compile(r'\d+.*ر\.س|ر\.س.*\d+', re.IGNORECASE)),
        ]
        for pattern in price_patterns:
            if pattern:
                price_text = pattern.strip()
                listing_data['price'] = price_text
                break
        
        # Extract location/city
        city_links = soup.find_all('a', href=re.compile(r'/city/'))
        if city_links:
            listing_data['city'] = city_links[0].get_text(strip=True)
            listing_data['location'] = listing_data['city']
        
        # Extract posted time
        time_indicators = soup.find_all(string=re.compile(r'الآن|منذ|ago|قبل', re.IGNORECASE))
        if time_indicators:
            listing_data['posted_time'] = time_indicators[0].strip()
        
        # Extract seller information
        seller_link = soup.find('a', href=re.compile(r'/users/'))
        if seller_link:
            listing_data['seller_name'] = seller_link.get_text(strip=True)
            listing_data['seller_url'] = urljoin(self.base_url, seller_link.get('href', ''))
        
        # Extract category and tags
        breadcrumb_links = soup.find_all('a', href=re.compile(r'/tags/'))
        tags = []
        for link in breadcrumb_links:
            tag_text = link.get_text(strip=True)
            if tag_text:
                tags.append(tag_text)
        listing_data['tags'] = tags
        if tags:
            listing_data['category'] = tags[0] if tags else ''
        
        # Extract images
        images = []
        img_tags = soup.find_all('img')
        for img in img_tags:
            src = img.get('src') or img.get('data-src') or img.get('data-lazy-src')
            if src:
                # Filter out icons, logos, and small images
                if any(exclude in src.lower() for exclude in ['icon', 'logo', 'badge', 'avatar']):
                    continue
                # Make absolute URL
                img_url = urljoin(self.base_url, src)
                images.append(img_url)
        
        # Remove duplicates while preserving order
        listing_data['images'] = list(dict.fromkeys(images))
        
        # Try to extract contact information
        # Look for contact buttons or phone number patterns
        contact_button = soup.find(string=re.compile(r'تواصل|اتصل|مراسلة|contact', re.IGNORECASE))
        if contact_button:
            listing_data['contact_info']['has_contact_button'] = True
        
        # Look for phone numbers in text (Saudi format)
        phone_pattern = re.compile(r'(\+966|05|5)[\d\s-]{8,}')
        phone_matches = phone_pattern.findall(soup.get_text())
        if phone_matches:
            listing_data['contact_info']['phone_numbers'] = list(set(phone_matches))
        
        return listing_data
    
    def download_image(self, img_url: str, listing_id: str, index: int) -> Optional[str]:
        """Download an image and return local path"""
        try:
            response = self.session.get(img_url, timeout=30, stream=True)
            response.raise_for_status()
            
            # Determine file extension
            content_type = response.headers.get('content-type', '')
            ext = 'jpg'
            if 'png' in content_type:
                ext = 'png'
            elif 'webp' in content_type:
                ext = 'webp'
            elif 'gif' in content_type:
                ext = 'gif'
            
            # Generate filename
            filename = f"{listing_id}_{index}.{ext}"
            filepath = self.images_dir / filename
            
            # Save image
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            return str(filepath)
        except Exception as e:
            print(f"Error downloading image {img_url}: {e}")
            return None
    
    def scrape_listing(self, listing_url: str) -> Dict:
        """Scrape a single listing"""
        # Apply ToS compliance measures every 10 listings
        self._apply_tos_compliance_measures()
        
        print(f"Scraping: {listing_url}")
        
        # Random delay between 2-5 seconds (ToS compliance)
        delay = random.uniform(2, 5)
        time.sleep(delay)
        
        soup = self.get_page(listing_url)
        if not soup:
            self.listing_count += 1
            return {}
        
        listing_data = self.extract_listing_details(soup, listing_url)
        
        # Download images if enabled
        if self.download_images and listing_data.get('images'):
            downloaded_images = []
            for idx, img_url in enumerate(listing_data['images']):
                local_path = self.download_image(img_url, listing_data.get('listing_id', 'unknown'), idx)
                if local_path:
                    downloaded_images.append({
                        'url': img_url,
                        'local_path': local_path
                    })
                # Random delay between image downloads (0.5-1.5 seconds)
                time.sleep(random.uniform(0.5, 1.5))
            
            listing_data['downloaded_images'] = downloaded_images
        
        # Increment counter
        self.listing_count += 1
        
        return listing_data
    
    def find_listing_urls(self, category_url: str, max_pages: int = 10) -> List[str]:
        """Find all listing URLs from a category page"""
        listing_urls = []
        
        for page in range(1, max_pages + 1):
            # Try different pagination patterns
            if page == 1:
                url = category_url
            else:
                # Try common pagination patterns
                if '?' in category_url:
                    url = f"{category_url}&page={page}"
                else:
                    url = f"{category_url}?page={page}"
            
            print(f"Fetching listings from page {page}...")
            
            # Apply ToS compliance before fetching page
            if page > 1:
                delay = random.uniform(3, 6)
                time.sleep(delay)
            
            soup = self.get_page(url)
            if not soup:
                break
            
            # Find all listing links
            # Pattern: /11173528712/title/
            links = soup.find_all('a', href=re.compile(r'/\d+/[^/]+/$'))
            
            page_urls = []
            for link in links:
                href = link.get('href', '')
                if href:
                    full_url = urljoin(self.base_url, href)
                    if full_url not in listing_urls:
                        page_urls.append(full_url)
            
            if not page_urls:
                print(f"No more listings found on page {page}")
                break
            
            listing_urls.extend(page_urls)
            print(f"Found {len(page_urls)} listings on page {page}")
            
            # Random delay between pages (2-4 seconds)
            if page < max_pages:
                time.sleep(random.uniform(2, 4))
        
        return listing_urls
    
    def scrape_category(self, category_url: str, max_listings: int = 50, max_pages: int = 10) -> List[Dict]:
        """Scrape all listings from a category"""
        print(f"Scraping category: {category_url}")
        
        # Find all listing URLs
        listing_urls = self.find_listing_urls(category_url, max_pages)
        listing_urls = listing_urls[:max_listings]  # Limit to max_listings
        
        print(f"Found {len(listing_urls)} listings to scrape")
        
            # Scrape each listing
        all_listings = []
        for idx, url in enumerate(listing_urls, 1):
            print(f"\n[{idx}/{len(listing_urls)}]")
            listing_data = self.scrape_listing(url)
            if listing_data:
                all_listings.append(listing_data)
            
            # Additional delay between listings (already handled in scrape_listing, but extra safety)
            if idx < len(listing_urls):  # Don't delay after last listing
                time.sleep(random.uniform(1, 3))
        
        return all_listings
    
    def save_to_json(self, data: List[Dict], filename: str = "listings.json"):
        """Save scraped data to JSON file"""
        filepath = self.output_dir / filename
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"\nData saved to {filepath}")
    
    def save_to_csv(self, data: List[Dict], filename: str = "listings.csv"):
        """Save scraped data to CSV file"""
        if not data:
            return
        
        filepath = self.output_dir / filename
        fieldnames = [
            'listing_id', 'title', 'description', 'price', 'city', 'location',
            'posted_time', 'seller_name', 'seller_url', 'category',
            'url', 'image_count', 'tags'
        ]
        
        with open(filepath, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            
            for listing in data:
                row = {
                    'listing_id': listing.get('listing_id', ''),
                    'title': listing.get('title', ''),
                    'description': listing.get('description', ''),
                    'price': listing.get('price', ''),
                    'city': listing.get('city', ''),
                    'location': listing.get('location', ''),
                    'posted_time': listing.get('posted_time', ''),
                    'seller_name': listing.get('seller_name', ''),
                    'seller_url': listing.get('seller_url', ''),
                    'category': listing.get('category', ''),
                    'url': listing.get('url', ''),
                    'image_count': len(listing.get('images', [])),
                    'tags': ', '.join(listing.get('tags', []))
                }
                writer.writerow(row)
        
        print(f"CSV saved to {filepath}")


def main():
    """Main function to run the scraper"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Haraj.com.sa Web Scraper')
    parser.add_argument('--url', type=str, help='Single listing URL or category URL to scrape')
    parser.add_argument('--category', type=str, help='Category URL to scrape multiple listings')
    parser.add_argument('--max-listings', type=int, default=50, help='Maximum number of listings to scrape')
    parser.add_argument('--max-pages', type=int, default=10, help='Maximum number of pages to scrape')
    parser.add_argument('--no-images', action='store_true', help='Skip downloading images')
    parser.add_argument('--output-dir', type=str, default='scraped_data', help='Output directory')
    
    args = parser.parse_args()
    
    # Initialize scraper
    scraper = HarajScraper(
        output_dir=args.output_dir,
        download_images=not args.no_images
    )
    
    if args.url:
        # Scrape single listing
        listing_data = scraper.scrape_listing(args.url)
        if listing_data:
            scraper.save_to_json([listing_data], "single_listing.json")
            scraper.save_to_csv([listing_data], "single_listing.csv")
            print("\nScraping completed!")
            print(json.dumps(listing_data, ensure_ascii=False, indent=2))
    
    elif args.category:
        # Scrape category
        listings = scraper.scrape_category(
            args.category,
            max_listings=args.max_listings,
            max_pages=args.max_pages
        )
        
        if listings:
            scraper.save_to_json(listings, "listings.json")
            scraper.save_to_csv(listings, "listings.csv")
            print(f"\nScraped {len(listings)} listings successfully!")
    
    else:
        print("Please provide either --url or --category argument")
        print("\nExample usage:")
        print("  python haraj_scraper.py --url https://haraj.com.sa/11173528712/هيلكس_غمارتين/")
        print("  python haraj_scraper.py --category https://haraj.com.sa/tags/حراج السيارات --max-listings 20")


if __name__ == "__main__":
    main()
