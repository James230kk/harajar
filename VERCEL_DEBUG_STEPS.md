# Vercel Debugging Steps

## Current Status
- ✅ Build completes successfully
- ❌ Runtime error: "Internal Server Error"

## What We've Fixed
1. ✅ Added comprehensive error handling in `api/index.py`
2. ✅ Added health check endpoint at `/health`
3. ✅ Fixed template path initialization
4. ✅ Added safe directory creation
5. ✅ Improved error messages with tracebacks

## How to Debug the Runtime Error

### Step 1: Check Vercel Logs
1. Go to Vercel Dashboard → Your Project
2. Click on **"Logs"** tab
3. Look for the error message and stack trace
4. The error handler should show detailed information

### Step 2: Test Health Endpoint
Try accessing: `https://your-app.vercel.app/health`

This should return:
```json
{
  "status": "ok",
  "base_dir": "...",
  "data_dir": "...",
  "template_dir": "..."
}
```

If this works, the Flask app is loading correctly.

### Step 3: Check Common Issues

#### Issue 1: Template Not Found
**Symptom**: Error about missing template
**Fix**: Verify `templates/` directory exists in root
**Check**: Files should be:
- `templates/dashboard.html`
- `templates/listing_detail.html`

#### Issue 2: Import Error
**Symptom**: "Error importing dashboard"
**Fix**: Check that `dashboard.py` is in root directory
**Check**: All imports in `dashboard.py` should be available

#### Issue 3: Path Issues
**Symptom**: File not found errors
**Fix**: Paths are now handled with fallbacks
**Check**: Verify BASE_DIR calculation is correct

### Step 4: Check Vercel Function Logs
1. Go to Vercel Dashboard → Your Project → Functions
2. Click on the function (should be `api/index.py`)
3. Check the "Logs" tab for detailed error messages

## Expected Behavior

### If Health Endpoint Works:
- ✅ Flask app is loading
- ✅ Issue is likely in a specific route
- Check the main route (`/`) for errors

### If Health Endpoint Fails:
- ❌ Flask app is not loading
- Check import errors in logs
- Verify all dependencies are in `requirements.txt`

## Quick Test

Try accessing these URLs:
1. `https://your-app.vercel.app/health` - Should return JSON
2. `https://your-app.vercel.app/` - Should show dashboard or error message
3. `https://your-app.vercel.app/api/stats` - Should return JSON stats

## Next Steps

1. **Share the error message** from Vercel logs
2. **Test the health endpoint** and share the result
3. **Check if templates exist** in the repository

## Alternative: Test Locally with Vercel CLI

```bash
# Install Vercel CLI
npm i -g vercel

# Test locally
vercel dev
```

This will simulate the Vercel environment locally and show errors immediately.
