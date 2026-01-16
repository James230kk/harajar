# Quick Start Guide

## Installation

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

## Basic Usage

### 1. Scrape a Single Listing

```bash
python haraj_scraper.py --url "https://haraj.com.sa/11173528712/هيلكس_غمارتين/"
```

This will:
- Extract all listing details
- Download images (saved in `scraped_data/images/`)
- Save data to JSON and CSV files

### 2. Scrape Multiple Listings from a Category

```bash
python haraj_scraper.py --category "https://haraj.com.sa/tags/حراج السيارات" --max-listings 20
```

### 3. Test the Scraper

```bash
python test_scraper.py
```

## Output Files

After scraping, you'll find:

- `scraped_data/listings.json` - All data in JSON format
- `scraped_data/listings.csv` - Data in CSV format (Excel-friendly)
- `scraped_data/images/` - All downloaded images

## If BeautifulSoup Version Doesn't Work

Some pages require JavaScript. Use the Selenium version:

```bash
python haraj_scraper_selenium.py --url "https://haraj.com.sa/11173528712/هيلكس_غمارتين/"
```

**Note:** The Selenium version will automatically download ChromeDriver on first run.

## Common Issues

### "No module named 'requests'"
```bash
pip install -r requirements.txt
```

### Selenium ChromeDriver issues
- Make sure Chrome browser is installed
- The webdriver-manager will auto-download ChromeDriver

### No data extracted
- Try the Selenium version
- Check if the URL is correct
- The website structure might have changed

## What Data is Extracted?

✅ Title  
✅ Description  
✅ Price  
✅ Location/City  
✅ Seller name and profile  
✅ Category and tags  
✅ Images (downloaded locally)  
✅ Contact information (if available)  
✅ Posted time  
✅ Listing URL and ID  

## Example Output

```json
{
  "listing_id": "11173528712",
  "title": "هيلكس غمارتين",
  "description": "تويوتا هايلوكس 2014...",
  "price": "75000 ريال",
  "city": "العارضة",
  "seller_name": "عبدووووخ",
  "images": [...],
  "contact_info": {...}
}
```

## Next Steps

1. Run `test_scraper.py` to verify everything works
2. Try scraping a single listing first
3. Then move to scraping categories
4. Customize the output directory with `--output-dir`

For more details, see `README.md`.
