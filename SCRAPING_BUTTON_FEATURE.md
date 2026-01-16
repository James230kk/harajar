# ✅ Scraping Button Feature Added!

## New Feature: Start Scraping from Dashboard

You can now start scraping listings directly from the dashboard without using the command line!

### Features

✅ **Input Field** - Set number of listings to scrape (1-100)  
✅ **Start Button** - Begin scraping with one click  
✅ **Stop Button** - Stop scraping if needed  
✅ **Real-time Progress** - See progress bar and status updates  
✅ **Auto-refresh** - Dashboard automatically refreshes when scraping completes  

### How to Use

1. **Open Dashboard**: http://localhost:5000

2. **Set Number of Listings**:
   - Enter a number between 1 and 100 in the input field
   - Default is 10 listings

3. **Click "🚀 بدء الاستخراج"** (Start Scraping):
   - Scraping starts in the background
   - Progress bar appears
   - Status updates every 2 seconds

4. **Monitor Progress**:
   - See current listing being scraped
   - Progress bar shows X / Total
   - Status text shows current action

5. **Wait for Completion**:
   - Dashboard automatically refreshes when done
   - New listings appear in the dashboard
   - Statistics update automatically

### UI Elements

**Scraping Controls:**
- Input field for number of listings
- "🚀 بدء الاستخراج" (Start Scraping) button
- "⏹️ إيقاف" (Stop) button (appears during scraping)

**Progress Display:**
- Status text showing current action
- Progress bar (0% to 100%)
- Progress counter (X / Total)

### Technical Details

- **Background Processing**: Scraping runs in a separate thread
- **Non-blocking**: Dashboard remains responsive during scraping
- **Real-time Updates**: Status checked every 2 seconds
- **Error Handling**: Errors displayed if scraping fails
- **Auto-save**: Data automatically saved to `scraped_data/listings.json`

### API Endpoints

- `POST /api/start-scraping` - Start scraping
  - Body: `{"max_listings": 10, "category_url": "..."}`
  
- `GET /api/scraping-status` - Get current status
  - Returns: `{"is_running": true, "progress": 5, "total": 10, ...}`
  
- `POST /api/stop-scraping` - Stop scraping

### Example Usage

1. Open dashboard
2. Enter "20" in the number field
3. Click "🚀 بدء الاستخراج"
4. Watch progress: "Scraping listing 5/20..."
5. Wait for completion
6. Dashboard refreshes showing 20 new listings!

### Notes

- Scraping respects ToS compliance (delays every 10 listings)
- Contact information is extracted automatically
- Images are not downloaded by default (faster scraping)
- Maximum 100 listings per scrape session
- Category is fixed to "حراج السيارات" (can be changed in code)

### Troubleshooting

**Button doesn't work?**
- Check browser console (F12) for errors
- Make sure dashboard server is running
- Verify Flask is installed

**Scraping stops unexpectedly?**
- Check terminal for error messages
- Verify Selenium/ChromeDriver is installed
- Check internet connection

**Progress not updating?**
- Refresh the page
- Check browser console for JavaScript errors
- Verify API endpoints are working

### Next Steps

The scraping button is fully functional! Just:
1. Start the dashboard: `python start_dashboard.py`
2. Open http://localhost:5000
3. Enter number of listings
4. Click the button and watch it scrape! 🚀
