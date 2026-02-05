# Vercel Deployment Guide (deprecated)

**This project is deployed on Railway, not Vercel.** Vercel config (index.py, vercel.json, pyproject.toml) has been removed. For deployment and subdomain setup, see **SUBDOMAIN_LIVE.md**.

---

## Legacy: Vercel Configuration (removed)

The following were removed in favor of Railway:

- ~~`index.py`~~ – Vercel entrypoint (removed)
- ~~`vercel.json`~~ – (removed)
- ~~`pyproject.toml`~~ – (removed)

## Deploy on Railway

See **SUBDOMAIN_LIVE.md** for steps: connect GitHub repo to Railway, add a volume, set `HARAJ_DATA_DIR`, and use your subdomain.

## ⚠️ Important Notes

### Selenium Limitations on Vercel

**Vercel serverless functions have limitations that may affect scraping:**

1. **Execution Timeout**: Vercel free tier has 10-second timeout, Pro has 60 seconds
2. **Memory Limits**: Limited memory may not be enough for Selenium/Chrome
3. **Chrome/Chromium**: May not be available in Vercel's serverless environment
4. **File System**: Ephemeral file system (files don't persist between invocations)

### Recommended Solutions

1. **For Dashboard Only** (Viewing scraped data):
   - ✅ Works perfectly on Vercel
   - Dashboard can view and download existing scraped data
   - Settings can be saved (though may not persist across deployments)

2. **For Scraping** (Active scraping):
   - ❌ May not work reliably on Vercel due to Selenium requirements
   - Consider using:
     - **Railway** (supports long-running processes)
     - **Render** (supports background workers)
     - **Heroku** (supports Selenium)
     - **DigitalOcean App Platform** (supports Docker)
     - **AWS EC2** or **Google Cloud Compute** (full control)

### Alternative: Hybrid Approach

- Deploy dashboard to Vercel (for viewing data)
- Run scraper on a separate service (Railway, Render, etc.)
- Scraper saves data to shared storage (database, S3, etc.)
- Dashboard reads from shared storage

## 📝 Current Configuration

- **Entrypoint**: `index.py` (re-exports `app` from `dashboard.py`)
- **Flask App**: Exported as `app` (Vercel detects it from `pyproject.toml` → `index:app`)
- **Routes**: All routes handled by Flask app
- **Data on Vercel**: Writes go to `/tmp` (ephemeral; use Railway for persistent data)

## 🔧 Troubleshooting

If deployment fails:

1. Check Vercel build logs
2. Ensure all dependencies are in `requirements.txt`
3. Check that `index.py` exists and exports `app` (from dashboard)
4. Verify `vercel.json` and `pyproject.toml` are in the repo

## 📚 Resources

- [Vercel Flask Documentation](https://vercel.com/docs/frameworks/backend/flask)
- [Vercel Python Runtime](https://vercel.com/docs/functions/runtimes/python)
