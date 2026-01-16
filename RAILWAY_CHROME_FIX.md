# Railway Chrome/ChromeDriver Fix

## Problem
ChromeDriver was failing with status code 127 (command not found) because Chrome/Chromium is not installed on Railway's Linux environment.

## Solution Applied

### 1. Updated Chrome Options
- Added detection for system Chrome/Chromium binaries
- Added Railway-specific Chrome arguments:
  - `--disable-setuid-sandbox`
  - `--disable-software-rasterizer`
  - `--disable-extensions`

### 2. Chrome Installation
- Created `nixpacks.toml` to install Chrome during Railway build
- Added fallback Chrome binary detection

### 3. ChromeDriver Initialization
- Added proper error handling
- Added fallback paths for ChromeDriver
- Made ChromeDriver executable with proper permissions

## Files Changed

1. **`haraj_scraper_selenium.py`**:
   - Added Chrome binary location detection
   - Improved ChromeDriver initialization with fallbacks
   - Better error messages

2. **`nixpacks.toml`**:
   - Added Chrome installation during build phase

3. **`setup_chrome.sh`**:
   - Standalone script to install Chrome (if needed)

## How It Works

1. **During Railway Build:**
   - `nixpacks.toml` installs Google Chrome Stable
   - Python dependencies are installed
   - ChromeDriver is downloaded by webdriver-manager

2. **During Runtime:**
   - Scraper detects Chrome binary location
   - ChromeDriver is initialized with proper permissions
   - Falls back to webdriver-manager if system Chrome not found

## Testing

After deployment, test scraping:
1. Go to your Railway dashboard
2. Click "Generate" or start scraping
3. Check logs for ChromeDriver initialization
4. Should see: "Chrome found at: /usr/bin/google-chrome" or similar

## Troubleshooting

If ChromeDriver still fails:

1. **Check Railway Logs:**
   - Look for Chrome installation messages
   - Check for ChromeDriver path errors

2. **Verify Chrome Installation:**
   - Railway should install Chrome during build
   - Check logs for: "Chrome installed successfully"

3. **Alternative: Use Chromium:**
   - If Chrome fails, the code will try Chromium
   - Chromium is lighter and may work better

## Next Steps

Railway will automatically redeploy with these changes. The scraper should now work correctly with Chrome/ChromeDriver.
