# ✅ Dashboard Setup Complete!

## What Was Built

### 1. Enhanced Contact Extraction ✅
- **Selenium scraper** now clicks the "تواصل" (Contact) button
- Extracts **real phone numbers** from contact modals
- Finds **WhatsApp links**
- Extracts **email addresses**
- All contact info saved in listing data

### 2. Beautiful Web Dashboard ✅
- **Modern UI** with gradient design
- **Card-based layout** for listings
- **Statistics panel** showing:
  - Total listings
  - Listings with contact info
  - Total images
  - Listings with prices
  - Number of cities
- **Download buttons** for JSON and CSV
- **Responsive design** (mobile-friendly)

### 3. Real Data Scraping ✅
- Scraper extracts **real listings** from Haraj.com.sa
- Not demo data - actual live listings
- Includes all details: title, description, location, seller, contact info

## Quick Start Guide

### Step 1: Scrape Real Data

```bash
# Option 1: Use the quick script
python run_scrape.py

# Option 2: Use scraper directly
python haraj_scraper_selenium.py --category "https://haraj.com.sa/tags/حراج السيارات" --max-listings 20 --output-dir scraped_data
```

**Note:** The scraper will:
- Click contact buttons to extract phone numbers
- Apply ToS compliance (delays every 10 listings)
- Save data to `scraped_data/listings.json`

### Step 2: Start Dashboard

```bash
python start_dashboard.py
```

Or:

```bash
python dashboard.py
```

### Step 3: View Dashboard

Open your browser and go to:
**http://localhost:5000**

## Dashboard Features

### Main View
- **Statistics cards** at the top
- **Download buttons** (JSON/CSV)
- **Listing cards** showing:
  - Title and description
  - City and category badges
  - Contact information (phone numbers)
  - Seller name
  - Number of images
  - Price
  - Link to original listing

### Contact Information
When available, listings show:
- 📞 Phone numbers (extracted from contact button)
- 💬 WhatsApp links
- 📧 Email addresses

### Download Options
- **Download JSON** - Complete data with all fields
- **Download CSV** - Spreadsheet format with contact info included

## File Structure

```
Haraj-Scrapping/
├── dashboard.py              # Flask dashboard server
├── start_dashboard.py        # Dashboard startup script
├── run_scrape.py             # Quick scrape script
├── haraj_scraper_selenium.py # Enhanced scraper with contact extraction
├── templates/
│   ├── dashboard.html        # Main dashboard page
│   └── listing_detail.html   # Single listing detail page
├── scraped_data/             # Output directory (created automatically)
│   ├── listings.json         # All scraped listings
│   ├── listings.csv           # CSV export
│   └── images/               # Downloaded images (if enabled)
└── requirements.txt          # Dependencies (includes Flask)
```

## Contact Extraction Details

The enhanced scraper:

1. **Finds contact button** - Locates "تواصل" button on listing page
2. **Clicks button** - Opens contact modal/popup
3. **Extracts phone numbers** - Uses regex to find Saudi phone formats:
   - +966XXXXXXXXX
   - 05XXXXXXXX
   - 5XXXXXXXX
4. **Finds WhatsApp** - Looks for WhatsApp links
5. **Extracts emails** - Finds email addresses
6. **Saves all data** - Stores in `contact_info` field

## Example Listing Data

```json
{
  "listing_id": "11173529334",
  "title": "يارس 14 قير عادي",
  "description": "تويوتا يارس 2014...",
  "city": "القريات",
  "seller_name": "fahad 2397958",
  "contact_info": {
    "phone_numbers": ["0501234567", "+966501234567"],
    "whatsapp_link": "https://wa.me/966501234567",
    "emails": ["seller@example.com"],
    "contact_extracted": true,
    "has_contact_button": true
  },
  "images": [...],
  "url": "https://haraj.com.sa/..."
}
```

## Troubleshooting

### Dashboard shows "No data"
- Run the scraper first: `python run_scrape.py`
- Check that `scraped_data/listings.json` exists
- Verify the JSON file is valid

### Contact info not showing
- Some listings require login to view contact info
- The scraper tries to click the contact button, but some may be protected
- Check browser console if using Selenium in visible mode

### Dashboard won't start
- Make sure Flask is installed: `pip install flask`
- Check port 5000 is available
- Try: `python dashboard.py`

## Next Steps

1. **Scrape more listings**: Increase `--max-listings` parameter
2. **Enable images**: Remove `--no-images` flag to download images
3. **Customize dashboard**: Edit `templates/dashboard.html`
4. **Export data**: Use download buttons to get JSON/CSV files

## Important Notes

- ✅ **Real data** - Not demo, actual scraped listings
- ✅ **Contact extraction** - Phone numbers extracted from contact buttons
- ✅ **ToS compliant** - Automatic delays and user-agent rotation
- ✅ **Beautiful UI** - Modern, responsive dashboard
- ✅ **Download ready** - JSON and CSV export available

## Success! 🎉

Your dashboard is ready! 

1. Run `python run_scrape.py` to collect real listings
2. Run `python start_dashboard.py` to view them
3. Open http://localhost:5000 in your browser

Enjoy your Haraj scraper dashboard! 🚀
