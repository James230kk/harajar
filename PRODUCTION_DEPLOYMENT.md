# Production Deployment Guide

## Settings/Credentials Functionality

The settings feature is **production-ready** and will work on live servers. Here's what has been implemented:

### ✅ Production-Ready Features

1. **Absolute Path Handling**
   - Uses `Path(__file__).parent.absolute()` to get the script's directory
   - Works regardless of current working directory
   - Works when deployed via WSGI, Gunicorn, or other production servers

2. **File Permissions**
   - Config file is created with restrictive permissions (600 on Unix)
   - Only owner can read/write the credentials file
   - Proper error handling for permission issues

3. **Error Handling**
   - Comprehensive error handling for file operations
   - Clear error messages for debugging
   - Graceful fallbacks if config file is corrupted

4. **Security**
   - Config file (`scraper_config.json`) is in `.gitignore`
   - Credentials are never exposed in API responses
   - Password field is never displayed when loading settings

5. **Directory Creation**
   - Automatically creates necessary directories
   - Works even if parent directories don't exist

### 📁 File Locations

- **Config File**: `scraper_config.json` (in project root)
- **Data Directory**: `scraped_data/` (in project root)
- **Base Directory**: Automatically detected from script location

### 🔒 Security Notes

1. **File Permissions**: The config file is created with restrictive permissions (600)
2. **Git Ignore**: `scraper_config.json` is in `.gitignore` to prevent committing credentials
3. **No Web Access**: Config file is not served via web server (not in static files)
4. **Password Handling**: Password is never returned in API responses

### 🚀 Deployment Checklist

- [x] Config file uses absolute paths (works in production)
- [x] Error handling for file operations
- [x] Directory creation on startup
- [x] Config file in `.gitignore`
- [x] Proper file permissions
- [x] Credentials validation
- [x] API error responses

### 📝 Usage

1. Deploy the application to your server
2. The config file will be created automatically when settings are saved
3. Credentials are stored locally on the server
4. Settings persist across server restarts

### ⚠️ Important Notes

1. **File Permissions**: Make sure the web server user has write permissions to the project directory
2. **Backup**: Consider backing up `scraper_config.json` separately (it's not in git)
3. **Environment Variables**: For additional security, you could use environment variables instead (future enhancement)

### 🔧 Troubleshooting

If settings don't save:
1. Check file permissions: `ls -la scraper_config.json`
2. Check directory permissions: `ls -la .`
3. Check web server user: `whoami` (when running as web server)
4. Check error logs for permission errors

### Example Server Setup

```bash
# On your production server
cd /path/to/Haraj-Scrapping
chmod 755 .  # Ensure directory is writable
python dashboard.py  # Or use gunicorn/wsgi
```

The settings will work automatically - no additional configuration needed!
