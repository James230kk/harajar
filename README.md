# Haraj.com.sa Web Scraper

A comprehensive web scraping tool to extract listing data from Haraj.com.sa, including descriptions, details, contact information, and images.

## Features

- ✅ Extract listing details (title, description, price, location, etc.)
- ✅ Extract seller information
- ✅ Extract contact information
- ✅ Download listing images
- ✅ Support for single listings or entire categories
- ✅ Export to JSON and CSV formats
- ✅ Two versions: BeautifulSoup (fast) and Selenium (for JavaScript-heavy pages)
- ✅ Proper handling of Arabic content
- ✅ **ToS-Compliant Scraping**: Automatic compliance measures after every 10 listings
  - User-Agent rotation
  - Extended delays (30-60 seconds)
  - Session reset (every 20 listings)
  - Random delays between requests (2-5 seconds)

## Installation

1. Install Python 3.7 or higher

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. For Selenium version, Chrome browser and ChromeDriver will be automatically installed via `webdriver-manager`

## Usage

### Basic Usage - Single Listing

Scrape a single listing:
```bash
python haraj_scraper.py --url "https://haraj.com.sa/11173528712/هيلكس_غمارتين/"
```

### Scrape Category/Page

Scrape multiple listings from a category:
```bash
python haraj_scraper.py --category "https://haraj.com.sa/tags/حراج السيارات" --max-listings 20
```

### Advanced Options

```bash
# Scrape with custom settings
python haraj_scraper.py \
  --category "https://haraj.com.sa/tags/حراج السيارات" \
  --max-listings 50 \
  --max-pages 5 \
  --output-dir my_data \
  --no-images
```

### Using Selenium Version (for JavaScript-heavy pages)

If the regular scraper doesn't work due to JavaScript rendering:

```bash
python haraj_scraper_selenium.py --url "https://haraj.com.sa/11173528712/هيلكس_غمارتين/"
```

With visible browser (for debugging):
```bash
python haraj_scraper_selenium.py --url "https://haraj.com.sa/11173528712/هيلكس_غمارتين/" --no-headless
```

## Command Line Arguments

### haraj_scraper.py / haraj_scraper_selenium.py

- `--url`: Single listing URL to scrape
- `--category`: Category URL to scrape multiple listings
- `--max-listings`: Maximum number of listings to scrape (default: 50)
- `--max-pages`: Maximum number of pages to scrape (default: 10)
- `--no-images`: Skip downloading images
- `--output-dir`: Output directory for scraped data (default: scraped_data)
- `--no-headless`: (Selenium only) Run browser in visible mode

## Output Structure

The scraper creates the following structure:

```
scraped_data/
├── listings.json          # All listings in JSON format
├── listings.csv           # All listings in CSV format
└── images/                # Downloaded images
    ├── 11173528712_0.jpg
    ├── 11173528712_1.jpg
    └── ...
```

## Data Fields Extracted

Each listing includes:

- `listing_id`: Unique listing ID
- `title`: Listing title
- `description`: Full description text
- `price`: Price (if available)
- `city`: City name
- `location`: Location information
- `posted_time`: When the listing was posted
- `seller_name`: Seller username
- `seller_url`: Link to seller profile
- `category`: Main category
- `tags`: All associated tags
- `images`: List of image URLs
- `downloaded_images`: Local paths to downloaded images
- `contact_info`: Contact information (phone numbers, etc.)
- `url`: Original listing URL

## Example Output (JSON)

```json
{
  "listing_id": "11173528712",
  "title": "هيلكس غمارتين",
  "description": "تويوتا هايلوكس 2014 قير عادي بنزين الممشى: 232 ألف كيلو",
  "price": "75000 ريال",
  "city": "العارضة",
  "location": "العارضة",
  "posted_time": "الآن",
  "seller_name": "عبدووووخ",
  "seller_url": "https://haraj.com.sa/users/عبدووووخ",
  "category": "حراج السيارات",
  "tags": ["حراج السيارات", "تويوتا", "هايلوكس"],
  "images": [
    "https://haraj.com.sa/images/listing1.jpg",
    "https://haraj.com.sa/images/listing2.jpg"
  ],
  "contact_info": {
    "has_contact_button": true
  },
  "url": "https://haraj.com.sa/11173528712/هيلكس_غمارتين/"
}
```

## ToS Compliance Features

The scraper automatically applies compliance measures to respect Haraj.com.sa's Terms of Service:

### Automatic Measures (Every 10 Listings)
- **User-Agent Rotation**: Changes browser user-agent to appear more natural
- **Extended Delays**: 30-60 second pause to reduce server load
- **Session Reset**: Every 20 listings, creates a new session (clears cookies)
- **Random Delays**: 2-5 seconds between each listing request
- **Image Download Delays**: 0.5-1.5 seconds between image downloads

### Why This Matters
These measures help:
- Prevent server overload
- Avoid being blocked or rate-limited
- Respect the website's resources
- Comply with Terms of Service
- Make scraping patterns appear more human-like

You'll see messages like:
```
[ToS Compliance] Applied measures after 10 listings...
  - Rotated User-Agent
  - Extended delay: 45 seconds
  - Continuing scraping...
```

## Important Notes

1. **Rate Limiting**: The scraper includes delays between requests to be respectful to the server. Don't modify these delays to scrape too aggressively.

2. **Legal & Ethical**: 
   - Always respect the website's Terms of Service
   - Don't scrape personal information without consent
   - Use scraped data responsibly
   - Consider reaching out to Haraj.com.sa for API access if available

3. **Website Changes**: Websites change their structure frequently. If the scraper stops working, you may need to update the selectors.

4. **Images**: Images are saved with the format `{listing_id}_{index}.{ext}`

5. **Arabic Content**: All text is properly encoded in UTF-8 to handle Arabic characters correctly.

6. **ToS Compliance**: The scraper automatically applies compliance measures. Don't disable these features.

## Troubleshooting

### BeautifulSoup version not working?
- Try the Selenium version: `haraj_scraper_selenium.py`
- The website might require JavaScript rendering

### Images not downloading?
- Check your internet connection
- Some images might be protected or require authentication
- Try running with `--no-headless` to see what's happening

### No listings found?
- Check if the URL is correct
- The website structure might have changed
- Try increasing `--max-pages`

## Requirements

- Python 3.7+
- requests
- beautifulsoup4
- lxml
- selenium (for Selenium version)
- webdriver-manager (for Selenium version)
- Chrome browser (for Selenium version)

## License

This tool is for educational purposes. Use responsibly and in accordance with Haraj.com.sa's Terms of Service.

## Contributing

Feel free to improve this scraper by:
- Adding more data fields
- Improving error handling
- Adding support for more export formats
- Optimizing performance

## Disclaimer

This scraper is provided as-is. The authors are not responsible for any misuse or violations of terms of service. Always respect website policies and use scraped data ethically.
