# Haraj Scraper Dashboard

A beautiful web dashboard to view and manage scraped listings from Haraj.com.sa.

## Features

✅ **View All Listings** - Beautiful card-based layout  
✅ **Contact Information** - Extracted phone numbers and WhatsApp links  
✅ **Statistics** - Real-time stats about scraped data  
✅ **Download Data** - Export to JSON or CSV  
✅ **Responsive Design** - Works on desktop and mobile  
✅ **Real-time Updates** - Refresh to see latest scraped data  

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Scrape Real Data

Run the scraper to collect listings:

```bash
python run_scrape.py
```

Or use the scraper directly:

```bash
python haraj_scraper_selenium.py --category "https://haraj.com.sa/tags/حراج السيارات" --max-listings 20 --output-dir scraped_data
```

### 3. Start Dashboard

```bash
python start_dashboard.py
```

Or:

```bash
python dashboard.py
```

### 4. Open in Browser

Navigate to: **http://localhost:5000**

## Dashboard Features

### Statistics Panel
- Total listings count
- Listings with contact information
- Total images found
- Listings with prices
- Number of different cities

### Listing Cards
Each card shows:
- Title and description
- City and category badges
- Contact information (if available)
- Seller name
- Number of images
- Price (if available)
- Link to original listing

### Download Options
- **Download JSON** - Complete data in JSON format
- **Download CSV** - Spreadsheet-friendly format with all fields including contact info

## Contact Information Extraction

The enhanced scraper now:
- ✅ Clicks the "تواصل" (Contact) button
- ✅ Extracts phone numbers from the contact modal
- ✅ Finds WhatsApp links
- ✅ Extracts email addresses
- ✅ Saves all contact info in the listing data

## Data Structure

The dashboard reads from: `scraped_data/listings.json`

Each listing includes:
```json
{
  "listing_id": "11173529334",
  "title": "يارس 14 قير عادي",
  "description": "...",
  "city": "القريات",
  "seller_name": "fahad 2397958",
  "contact_info": {
    "phone_numbers": ["0501234567"],
    "whatsapp_link": "https://wa.me/966501234567",
    "emails": ["seller@example.com"],
    "contact_extracted": true
  },
  "images": [...],
  "url": "https://haraj.com.sa/..."
}
```

## API Endpoints

- `GET /` - Main dashboard page
- `GET /api/listings` - JSON API for listings
- `GET /api/stats` - Statistics in JSON
- `GET /download/json` - Download listings as JSON
- `GET /download/csv` - Download listings as CSV
- `GET /listing/<id>` - View single listing details

## Troubleshooting

### No listings showing?
1. Make sure you've run the scraper first
2. Check that `scraped_data/listings.json` exists
3. Verify the file contains valid JSON

### Contact info not showing?
- The scraper needs to click the contact button
- Some listings may require login to view contact info
- Try using the Selenium version for better contact extraction

### Dashboard won't start?
- Make sure Flask is installed: `pip install flask`
- Check that port 5000 is not in use
- Try a different port by editing `dashboard.py`

## Screenshots

The dashboard features:
- Modern gradient background
- Card-based listing display
- Color-coded badges
- Responsive grid layout
- Download buttons
- Statistics overview

## Next Steps

1. **Scrape more data**: Increase `--max-listings` for more listings
2. **Download data**: Use the download buttons to export
3. **View details**: Click on listings to see full information
4. **Customize**: Edit `templates/dashboard.html` to customize the design

## Notes

- The dashboard reads data from `scraped_data/listings.json`
- Refresh the page to see newly scraped data
- Contact information is extracted using Selenium (requires browser automation)
- All data is stored locally in the `scraped_data` directory
