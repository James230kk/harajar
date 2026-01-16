# Dashboard Fix Guide

## ✅ Dashboard is Working!

The dashboard is running and accessible. Here's how to access it:

### Access Methods

1. **http://localhost:5000** (try this first)
2. **http://127.0.0.1:5000** (if localhost doesn't work)
3. **http://0.0.0.0:5000** (alternative)

### If Dashboard Shows "No Data"

This is normal if you haven't scraped any listings yet. The dashboard will show:
- "لا توجد بيانات" (No data)
- Instructions on how to scrape data

### Steps to Get Data

1. **Run the scraper:**
```bash
python run_scrape.py
```

Or:
```bash
python haraj_scraper_selenium.py --category "https://haraj.com.sa/tags/حراج السيارات" --max-listings 10 --output-dir scraped_data
```

2. **Wait for scraping to complete** (it may take a few minutes)

3. **Refresh the dashboard** in your browser

### Troubleshooting

#### Dashboard won't load
- Check if server is running: Look for "Running on http://..." in terminal
- Try stopping and restarting: Press Ctrl+C, then run `python start_dashboard.py` again
- Check firewall: Make sure port 5000 is not blocked

#### "Connection refused" error
- Make sure the dashboard is running
- Check the terminal for any error messages
- Try a different port by editing `dashboard.py` line 172: `app.run(debug=True, host='0.0.0.0', port=5001)`

#### Browser shows blank page
- Check browser console (F12) for errors
- Try a different browser
- Clear browser cache

#### Template errors
- Make sure `templates/` directory exists
- Make sure `templates/dashboard.html` exists
- Check for any error messages in terminal

### Quick Test

Run this to verify everything works:
```bash
python test_dashboard.py
```

You should see all checkmarks (✓).

### Start Dashboard Properly

1. **Stop any running dashboard** (Ctrl+C in terminal)

2. **Start fresh:**
```bash
python start_dashboard.py
```

3. **Look for this message:**
```
🚀 Starting Haraj Scraper Dashboard
======================================================================
📊 Dashboard will be available at: http://localhost:5000
```

4. **Open browser** and go to http://localhost:5000

### Common Issues

**Issue:** "ModuleNotFoundError: No module named 'flask'"
**Fix:** `pip install flask`

**Issue:** "Template not found"
**Fix:** Make sure you're in the project directory and `templates/` folder exists

**Issue:** Port 5000 already in use
**Fix:** Change port in `dashboard.py` line 172 to `port=5001`

### Verify Server is Running

Check if port 5000 is listening:
```bash
netstat -ano | findstr :5000
```

You should see a LISTENING entry.

### Still Not Working?

1. Check terminal output for error messages
2. Make sure you're in the correct directory: `D:\Haraj-Scrapping`
3. Try accessing via IP: `http://127.0.0.1:5000`
4. Check Windows Firewall settings
5. Try a different browser

The dashboard is confirmed working - the issue is likely with browser access or you need to scrape data first!
