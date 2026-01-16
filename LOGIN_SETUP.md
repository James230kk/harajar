# 🔐 Login Setup for Haraj Scraper

## Why Login is Needed

**Yes, you need an account to get contact details** from Haraj.com.sa. The website requires users to be logged in before revealing seller contact information (phone numbers, WhatsApp, email).

## How to Use Login

### Option 1: Command Line

```bash
python haraj_scraper_selenium.py \
    --category "https://haraj.com.sa/tags/حراج السيارات" \
    --max-listings 20 \
    --username "your_email@example.com" \
    --password "your_password"
```

### Option 2: Python Code

```python
from haraj_scraper_selenium import HarajScraperSelenium

scraper = HarajScraperSelenium(
    output_dir="scraped_data",
    download_images=False,
    headless=True,
    username="your_email@example.com",  # Your Haraj account email
    password="your_password"             # Your Haraj account password
)

# Scraper will automatically login when initialized
listings = scraper.scrape_category(
    "https://haraj.com.sa/tags/حراج السيارات",
    max_listings=20
)
```

### Option 3: Dashboard (Coming Soon)

Login credentials can be added to the dashboard interface in a future update.

## Important Notes

1. **Credentials are optional** - If you don't provide login credentials, the scraper will still work but may not be able to extract contact information.

2. **Security** - Never commit your credentials to version control. Use environment variables or config files that are in `.gitignore`.

3. **Account Creation** - If you don't have a Haraj.com.sa account:
   - Go to https://haraj.com.sa
   - Click "تسجيل" (Register)
   - Create a free account
   - Verify your email if required

4. **Login Detection** - The scraper will detect if login is required and show a warning message.

## Troubleshooting

- **Login fails**: Check your credentials and make sure your account is active
- **Still no contact info**: Some listings may not have contact information even when logged in
- **Rate limiting**: Being logged in may help avoid some rate limits, but still respect ToS compliance delays
