# Railway Deployment Guide

## ✅ Railway Configuration Complete

The project is now configured for Railway deployment with:

1. **`Procfile`** - Defines the start command for Railway
2. **`requirements.txt`** - Includes `gunicorn` for production server
3. **Cleaned up code** - Removed Vercel-specific configurations

## 🚀 Deployment Steps

1. **Connect your GitHub repository to Railway:**
   - Go to [Railway](https://railway.app)
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository: `JamilPr1/Haraj`

2. **Railway will automatically:**
   - Detect Python
   - Install dependencies from `requirements.txt`
   - Use the `Procfile` to start the application
   - Assign a port via `$PORT` environment variable

3. **The app will start with:**
   ```
   gunicorn dashboard:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120
   ```

## 📋 Configuration Details

### Procfile
```
web: gunicorn dashboard:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120
```

- **`web:`** - Defines a web process
- **`gunicorn`** - Production WSGI server
- **`dashboard:app`** - Flask app from `dashboard.py`
- **`--bind 0.0.0.0:$PORT`** - Binds to Railway's assigned port
- **`--workers 2`** - Uses 2 worker processes
- **`--timeout 120`** - 120 second timeout (for scraping operations)

### Environment Variables

Railway automatically provides:
- **`$PORT`** - Port number for the application

Optional (can be set in Railway dashboard):
- No additional environment variables required for basic operation

## ✅ Advantages of Railway

1. **Better for Long-Running Processes:**
   - No execution time limits like Vercel
   - Supports background tasks and scraping

2. **Selenium Support:**
   - Can install Chrome/Chromium
   - Supports headless browser automation

3. **Persistent Storage:**
   - Files persist between deployments
   - Can store scraped data

4. **Easy Configuration:**
   - Simple Procfile setup
   - Automatic dependency detection

## 🔧 Troubleshooting

### Issue: "No start command was found"
**Solution:** Make sure `Procfile` exists in the root directory with:
```
web: gunicorn dashboard:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120
```

### Issue: Module not found errors
**Solution:** Check that all dependencies are in `requirements.txt`

### Issue: Port binding errors
**Solution:** Make sure the Procfile uses `$PORT` (Railway provides this)

### Issue: Timeout errors during scraping
**Solution:** Increase timeout in Procfile:
```
web: gunicorn dashboard:app --bind 0.0.0.0:$PORT --workers 2 --timeout 300
```

## 📝 Notes

- **Scraping:** Railway supports long-running scraping operations
- **Data Storage:** Scraped data will persist in the `scraped_data/` directory
- **Settings:** User credentials saved in `scraper_config.json` will persist
- **Logs:** Check Railway dashboard → Deployments → Logs for debugging

## 🎯 Next Steps

1. Push code to GitHub (already done)
2. Connect repository to Railway
3. Railway will automatically deploy
4. Access your dashboard at the Railway-provided URL
