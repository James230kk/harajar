# Fixing ChromeDriver Status Code 127 on Railway

## Problem
ChromeDriver is failing with **status code 127**, which means:
- The binary can't execute (missing shared libraries)
- OR the binary isn't found in PATH

## Current Situation
- ✅ Server is running (gunicorn started successfully)
- ❌ ChromeDriver from webdriver-manager is failing
- ❌ System ChromeDriver from nixpacks isn't being found

## Root Cause
The system ChromeDriver installed by nixpacks isn't in the PATH, so the code falls back to webdriver-manager's ChromeDriver, which doesn't have all required shared libraries.

## Solution Applied

### 1. nixpacks.toml Configuration
```toml
[phases.setup]
nixPkgs = ["python39", "chromium", "chromedriver", "libnss3", "libatk-bridge2.0-0", "libx11-xcb1", "libgbm1"]
```

This should install:
- ✅ Chromium (browser)
- ✅ ChromeDriver (driver)
- ✅ Required libraries

### 2. ChromeDriver Detection
The code now:
- Checks PATH first (`shutil.which('chromedriver')`)
- Checks nix store locations (`/nix/store/*/bin/chromedriver`)
- Checks standard system locations
- Falls back to webdriver-manager only if system driver not found

### 3. Diagnostic Endpoint
Visit: `https://your-railway-url.railway.app/api/chromedriver-check`

This will show:
- If system ChromeDriver is found
- Where it's located
- If it's executable
- If Chromium is installed

## Next Steps

1. **Wait for Railway to redeploy** (automatic after git push)

2. **Check Railway Build Logs:**
   - Look for messages about chromedriver installation
   - Verify nixpacks is installing the packages

3. **Check Railway Runtime Logs:**
   - Look for: "Found chromedriver in PATH: ..."
   - Or: "System ChromeDriver not found, using webdriver-manager..."
   - The new logging will show which paths were checked

4. **Test the Diagnostic Endpoint:**
   - After redeploy, visit: `/api/chromedriver-check`
   - This will show what ChromeDriver is available

## If System ChromeDriver Still Not Found

If the diagnostic endpoint shows system ChromeDriver is not found, we may need to:

1. **Add ChromeDriver to PATH explicitly:**
   - Modify the start command in nixpacks.toml
   - Or add an environment variable

2. **Use a different approach:**
   - Install ChromeDriver via apt-get instead of nixpacks
   - Or use a Dockerfile instead of nixpacks

## Expected Behavior After Fix

- System ChromeDriver should be found in PATH
- Should use system ChromeDriver (not webdriver-manager)
- Should work without status code 127 errors

## Current Status

- ✅ Code updated with better ChromeDriver detection
- ✅ Diagnostic endpoint added
- ⏳ Waiting for Railway redeploy
- ⏳ Need to check logs to see if system ChromeDriver is found
