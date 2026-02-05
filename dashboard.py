"""
Flask Dashboard for viewing scraped Haraj listings
"""

from flask import Flask, render_template, jsonify, send_file, request, make_response
import json
import os
import re
from pathlib import Path
import csv
import io
import threading
import time
import subprocess
import sys
from urllib.parse import quote

try:
    import requests
except ImportError:
    requests = None

# Get the directory where this script is located
_script_dir = Path(__file__).parent.absolute()
BASE_DIR = _script_dir

# Initialize Flask app with explicit template folder
_template_dir = BASE_DIR / "templates"
app = Flask(__name__, template_folder=str(_template_dir))

# Data paths: use env vars in production so you can point to a persistent volume
_data_dir_env = os.environ.get("HARAJ_DATA_DIR") or os.environ.get("DATA_DIR")
_config_env = os.environ.get("HARAJ_CONFIG_FILE") or os.environ.get("CONFIG_FILE")
DATA_DIR = Path(_data_dir_env) if _data_dir_env else (BASE_DIR / "scraped_data")
CONFIG_FILE = Path(_config_env) if _config_env else (BASE_DIR / "scraper_config.json")
SAVED_LISTINGS_FILE = DATA_DIR / "saved_listings.json"
LISTINGS_DB = DATA_DIR / "listings.db"

# Haraj.com.sa – scrape leads from https://haraj.com.sa/ (exact tag names from site)
HARAJ_SITE = "https://haraj.com.sa"
HARAJ_BASE = "https://haraj.com.sa/tags/"
HARAJ_CATEGORIES = [
    {"id": "cars", "name_ar": "حراج السيارات", "name_en": "Cars", "tag": "حراج السيارات"},
    {"id": "realestate", "name_ar": "حراج العقار", "name_en": "Real Estate", "tag": "حراج العقار"},
    {"id": "devices", "name_ar": "حراج الأجهزة", "name_en": "Devices / Electronics", "tag": "حراج الأجهزة"},
    {"id": "animals", "name_ar": "مواشي وحيوانات وطيور", "name_en": "Animals", "tag": "مواشي وحيوانات وطيور"},
    {"id": "furniture", "name_ar": "اثاث", "name_en": "Furniture", "tag": "اثاث"},
    {"id": "jobs", "name_ar": "وظائف", "name_en": "Jobs", "tag": "وظائف"},
    {"id": "services", "name_ar": "خدمات", "name_en": "Services", "tag": "خدمات"},
    {"id": "fashion", "name_ar": "مستلزمات شخصية", "name_en": "Fashion", "tag": "مستلزمات شخصية"},
    {"id": "games", "name_ar": "العاب وترفيه", "name_en": "Games", "tag": "العاب وترفيه"},
    {"id": "videogames", "name_ar": "العاب فيديو", "name_en": "Video Games", "tag": "العاب وترفيه"},
    {"id": "rarities", "name_ar": "نوادر و تراثيات", "name_en": "Rarities", "tag": "نوادر و تراثيات"},
    {"id": "arts", "name_ar": "مكتبة وفنون", "name_en": "Arts", "tag": "مكتبة وفنون"},
    {"id": "trips", "name_ar": "صيد ورحلات", "name_en": "Trips", "tag": "صيد ورحلات"},
    {"id": "food", "name_ar": "اطعمة ومشروبات", "name_en": "Foods", "tag": "اطعمة ومشروبات"},
    {"id": "gardens", "name_ar": "زراعة وحدائق", "name_en": "Gardens", "tag": "زراعة وحدائق"},
    {"id": "occasions", "name_ar": "حفلات ومناسبات", "name_en": "Occasions", "tag": "حفلات ومناسبات"},
    {"id": "tourism", "name_ar": "سفر وسياحة", "name_en": "Tourism", "tag": "سفر وسياحة"},
    {"id": "lost", "name_ar": "مفقودات", "name_en": "Lost", "tag": "مفقودات"},
    {"id": "coach", "name_ar": "تعليم وتدريب", "name_en": "Coach / Training", "tag": "تعليم وتدريب"},
    {"id": "code", "name_ar": "برمجة وتصاميم", "name_en": "Code / Programming", "tag": "برمجة وتصاميم"},
    {"id": "fund", "name_ar": "مشاريع واستثمارات", "name_en": "Fund / Projects", "tag": "مشاريع واستثمارات"},
    {"id": "other", "name_ar": "قسم غير مصنف", "name_en": "More", "tag": "قسم غير مصنف"},
]


def get_categories_with_urls():
    """Return categories with full Haraj tag URLs (tag part URL-encoded)."""
    return [
        {**c, "url": HARAJ_BASE + quote(c["tag"])}
        for c in HARAJ_CATEGORIES
    ]


# Create data directory if it doesn't exist
try:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
except:
    pass  # Continue even if directory creation fails

# Scraping status
scraping_status = {
    'is_running': False,
    'progress': 0,
    'total': 0,
    'current_listing': '',
    'error': None
}

def load_config():
    """Load scraper configuration. OpenAI API key is stored until user adds or changes it in Settings."""
    try:
        if CONFIG_FILE.exists():
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                config = json.load(f)
                if isinstance(config, dict):
                    return {
                        'username': config.get('username', ''),
                        'password': config.get('password', ''),
                    }
    except json.JSONDecodeError:
        pass
    except PermissionError:
        print(f"Warning: Permission denied reading config file: {CONFIG_FILE}")
    except Exception as e:
        print(f"Warning: Error loading config: {e}")
    return {'username': '', 'password': ''}

def save_config(config):
    """Save scraper configuration (Haraj credentials only)."""
    try:
        CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
        if not isinstance(config, dict):
            return False
        payload = {
            'username': config.get('username', ''),
            'password': config.get('password', ''),
        }
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(payload, f, indent=2)
        
        # Set restrictive permissions (Unix-like systems)
        try:
            import stat
            os.chmod(CONFIG_FILE, stat.S_IRUSR | stat.S_IWUSR)  # 600 - read/write for owner only
        except (AttributeError, OSError):
            # Windows doesn't support chmod the same way, that's okay
            pass
        
        return True
    except PermissionError:
        print(f"Error: Permission denied writing config file: {CONFIG_FILE}")
        return False
    except Exception as e:
        print(f"Error saving config: {e}")
        import traceback
        traceback.print_exc()
        return False

def _sanitize_listing_text(text, max_len=50000):
    """Remove script/code from scraped title or description for display."""
    if not text or not isinstance(text, str):
        return (text or '').strip()
    s = text.strip()
    for pat in [
        r'<script[\s\S]*?</script>', r'document\.write\s*\(', r'window\.onload\s*=',
        r'parent\.postMessage\s*\(', r'function\s*\([^)]*\)\s*\{', r'<iframe[\s\S]*?</iframe>',
        r'javascript:', r'\.style\.\w+\s*=',
    ]:
        s = re.sub(pat, ' ', s, flags=re.IGNORECASE | re.DOTALL)
    s = re.sub(r'\s+', ' ', s).strip()
    return s[:max_len] if len(s) > max_len else s


def _sanitize_posted_time(posted_time, max_display_len=80):
    """Show only a short time/date; if value is JSON-LD, extract datePosted and format."""
    if not posted_time or not isinstance(posted_time, str):
        return ''
    s = posted_time.strip()
    if len(s) <= max_display_len and not s.startswith('{') and '"@context"' not in s:
        return s
    # Likely JSON-LD schema: try to extract datePosted
    if s.startswith('{') or '"datePosted"' in s or '"dateModified"' in s:
        try:
            data = json.loads(s)
            dt = data.get('datePosted') or data.get('dateModified') or ''
            if dt:
                # Format ISO "2026-01-18T05:39:54.000Z" -> "2026-01-18" or "Jan 18, 2026"
                if 'T' in dt:
                    dt = dt.split('T')[0]
                return dt
        except (json.JSONDecodeError, TypeError):
            pass
    return ''


def load_listings():
    """Load listings from JSON file (sanitize title/description to remove script content)."""
    json_file = DATA_DIR / "listings.json"
    if json_file.exists():
        with open(json_file, 'r', encoding='utf-8') as f:
            listings = json.load(f)
        for L in listings:
            if L.get('title'):
                L['title'] = _sanitize_listing_text(L['title'], max_len=2000)
            if L.get('description'):
                L['description'] = _sanitize_listing_text(L['description'], max_len=50000)
            if L.get('posted_time'):
                L['posted_time'] = _sanitize_posted_time(L['posted_time'])
        return listings
    return []


def _init_listings_db():
    """Create SQLite DB and table if not exists."""
    import sqlite3
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(LISTINGS_DB))
    conn.execute("""
        CREATE TABLE IF NOT EXISTS listings (
            listing_id TEXT PRIMARY KEY,
            url TEXT,
            data TEXT NOT NULL,
            updated_at TEXT DEFAULT (datetime('now'))
        )
    """)
    conn.commit()
    conn.close()


def _load_saved_listings_from_db():
    """Load all listings from SQLite. Returns list of dicts or empty list."""
    import sqlite3
    if not LISTINGS_DB.exists():
        return []
    try:
        conn = sqlite3.connect(str(LISTINGS_DB))
        conn.row_factory = sqlite3.Row
        rows = conn.execute("SELECT data FROM listings ORDER BY updated_at ASC").fetchall()
        conn.close()
        listings = []
        for row in rows:
            try:
                listings.append(json.loads(row[0]))
            except (json.JSONDecodeError, TypeError):
                continue
        return listings
    except Exception:
        return []


def _save_saved_listings_to_db(listings):
    """Upsert all listings into SQLite."""
    import sqlite3
    import re
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    _init_listings_db()
    conn = sqlite3.connect(str(LISTINGS_DB))
    for L in listings:
        lid = (str(L.get('listing_id') or '')).strip()
        url = (L.get('url') or '').strip()[:2000]
        pk = lid if lid else ('url_' + re.sub(r'[^\w\-.]', '_', (url or '')[:120]))
        data = json.dumps(L, ensure_ascii=False)
        conn.execute(
            "INSERT OR REPLACE INTO listings (listing_id, url, data, updated_at) VALUES (?, ?, ?, datetime('now'))",
            (pk, url or None, data)
        )
    conn.commit()
    conn.close()


def load_saved_listings():
    """Load saved listings from DB first; if empty, load from JSON and migrate to DB."""
    _init_listings_db()
    listings = _load_saved_listings_from_db()
    if listings:
        for L in listings:
            if L.get('title'):
                L['title'] = _sanitize_listing_text(L['title'], max_len=2000)
            if L.get('description'):
                L['description'] = _sanitize_listing_text(L['description'], max_len=50000)
            if L.get('posted_time'):
                L['posted_time'] = _sanitize_posted_time(L['posted_time'])
        return listings
    if SAVED_LISTINGS_FILE.exists():
        try:
            with open(SAVED_LISTINGS_FILE, 'r', encoding='utf-8') as f:
                listings = json.load(f)
        except (json.JSONDecodeError, IOError):
            return load_listings()
        for L in listings:
            if L.get('title'):
                L['title'] = _sanitize_listing_text(L['title'], max_len=2000)
            if L.get('description'):
                L['description'] = _sanitize_listing_text(L['description'], max_len=50000)
            if L.get('posted_time'):
                L['posted_time'] = _sanitize_posted_time(L['posted_time'])
        _save_saved_listings_to_db(listings)
        return listings
    return load_listings()


def save_saved_listings(listings):
    """Persist saved listings to SQLite DB and to JSON (sync for production and backup)."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    _save_saved_listings_to_db(listings)
    with open(SAVED_LISTINGS_FILE, 'w', encoding='utf-8') as f:
        json.dump(listings, f, ensure_ascii=False, indent=2)


def merge_saved_listings(new_listings):
    """Merge new listings into saved; skip duplicates by listing_id (and url). Returns (merged_list, added_count, skipped_count)."""
    saved = load_saved_listings()
    seen_ids = {str(L.get('listing_id')) for L in saved if L.get('listing_id')}
    seen_urls = {L.get('url', '').strip().rstrip('/') for L in saved if L.get('url')}
    added = 0
    skipped = 0
    for L in new_listings:
        lid = str(L.get('listing_id') or '')
        url = (L.get('url') or '').strip().rstrip('/')
        if lid in seen_ids or url in seen_urls:
            skipped += 1
            continue
        seen_ids.add(lid)
        if url:
            seen_urls.add(url)
        saved.append(L)
        added += 1
    return saved, added, skipped


def get_listings_stats(listings):
    """Calculate statistics about listings"""
    if not listings:
        return {
            'total': 0,
            'with_contact': 0,
            'with_images': 0,
            'with_prices': 0,
            'cities': {},
            'categories': {}
        }
    
    stats = {
        'total': len(listings),
        'with_contact': 0,
        'with_images': 0,
        'with_prices': 0,
        'cities': {},
        'categories': {}
    }
    
    for listing in listings:
        # Contact info
        if listing.get('contact_info', {}).get('phone_numbers'):
            stats['with_contact'] += 1
        
        # Images
        if listing.get('images'):
            stats['with_images'] += len(listing.get('images', []))
        
        # Prices
        if listing.get('price'):
            stats['with_prices'] += 1
        
        # Cities
        city = listing.get('city', 'Unknown')
        stats['cities'][city] = stats['cities'].get(city, 0) + 1
        
        # Categories
        category = listing.get('category', 'Unknown')
        stats['categories'][category] = stats['categories'].get(category, 0) + 1
    
    return stats

@app.route('/health')
def health():
    """Health check endpoint; includes API routes so you can verify the right app is running."""
    rules = [r.rule for r in app.url_map.iter_rules() if r.rule.startswith('/api/')]
    return jsonify({
        'status': 'ok',
        'base_dir': str(BASE_DIR),
        'data_dir': str(DATA_DIR),
        'template_dir': str(_template_dir),
        'api_routes': sorted(rules),
    }), 200

@app.route('/favicon.ico')
def favicon():
    """Avoid 404 in console when browser requests favicon."""
    return '', 204

@app.route('/api/chromedriver-check')
def chromedriver_check():
    """Check ChromeDriver availability for debugging"""
    import shutil
    import glob
    import os
    
    results = {
        'system_chromedriver': None,
        'nix_store_chromedrivers': [],
        'standard_locations': {},
        'chromium_found': False,
        'chromium_path': None
    }
    
    # Check PATH
    system_chromedriver = shutil.which('chromedriver')
    if system_chromedriver:
        results['system_chromedriver'] = system_chromedriver
        results['system_chromedriver_exists'] = os.path.exists(system_chromedriver)
        results['system_chromedriver_executable'] = os.access(system_chromedriver, os.X_OK) if system_chromedriver else False
    
    # Check nix store
    nix_matches = glob.glob('/nix/store/*/bin/chromedriver')
    results['nix_store_chromedrivers'] = nix_matches[:5]  # Limit to first 5
    
    # Check standard locations
    standard_paths = ['/usr/bin/chromedriver', '/usr/local/bin/chromedriver', '/opt/chromedriver/chromedriver']
    for path in standard_paths:
        results['standard_locations'][path] = {
            'exists': os.path.exists(path),
            'executable': os.access(path, os.X_OK) if os.path.exists(path) else False
        }
    
    # Check for Chromium
    chromium_paths = [
        shutil.which('chromium'),
        shutil.which('chromium-browser'),
        '/usr/bin/chromium',
        '/usr/bin/chromium-browser',
    ]
    for path in chromium_paths:
        if path and os.path.exists(path):
            results['chromium_found'] = True
            results['chromium_path'] = path
            break
    
    return jsonify(results), 200

def _listings_for_cards(listings):
    """Return listings with description stripped so cards never show description bar."""
    out = []
    for L in listings:
        card = dict(L)
        card.pop('description', None)
        out.append(card)
    return out


@app.route('/')
def index():
    """Main dashboard page – shows saved listings (cards only); full description on View page."""
    try:
        listings = load_saved_listings()
        stats = get_listings_stats(listings)
        config = load_config()
        card_listings = _listings_for_cards(listings)
        resp = render_template('dashboard.html', listings=card_listings, stats=stats, config=config)
        response = make_response(resp)
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        return response
    except Exception as e:
        import traceback
        error_msg = f"Error loading dashboard: {str(e)}\n\n{traceback.format_exc()}"
        return error_msg, 500


@app.route('/saved-listings')
def saved_listings_page():
    """Dedicated page for all saved (scraped) leads."""
    try:
        listings = load_saved_listings()
        stats = get_listings_stats(listings)
        config = load_config()
        card_listings = _listings_for_cards(listings)
        return render_template('saved_listings.html', listings=card_listings, stats=stats, config=config)
    except Exception as e:
        import traceback
        return f"Error loading saved listings: {str(e)}\n\n{traceback.format_exc()}", 500

@app.route('/api/categories')
def api_categories():
    """API endpoint to get Haraj categories with URLs for scraping"""
    return jsonify(get_categories_with_urls())


@app.route('/api/listings')
def api_listings():
    """API endpoint to get listings (saved leads)"""
    listings = load_saved_listings()
    return jsonify(listings)

@app.route('/api/stats')
def api_stats():
    """API endpoint to get statistics (from saved)"""
    listings = load_saved_listings()
    stats = get_listings_stats(listings)
    return jsonify(stats)


@app.route('/api/save-listings', methods=['POST'])
def api_save_listings():
    """Explicitly save all current listings to DB and JSON (for production sync)."""
    try:
        listings = load_saved_listings()
        save_saved_listings(listings)
        return jsonify({
            'success': True,
            'message': f'تم حفظ {len(listings)} إعلان في قاعدة البيانات',
            'count': len(listings),
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e), 'count': 0}), 500


@app.route('/listing/<listing_id>/download-images')
def download_listing_images(listing_id):
    """Download all images for a listing as a ZIP file"""
    import zipfile
    import requests
    listings = load_saved_listings()
    listing = next((l for l in listings if str(l.get('listing_id')) == str(listing_id)), None)
    if not listing:
        return "Listing not found", 404
    images = listing.get('images') or []
    if not images:
        return "No images for this listing", 404
    mem = io.BytesIO()
    with zipfile.ZipFile(mem, 'w', zipfile.ZIP_DEFLATED) as zf:
        for idx, url in enumerate(images[:30]):  # limit 30 to avoid timeout
            try:
                r = requests.get(url, timeout=15, stream=True)
                r.raise_for_status()
                ext = 'jpg'
                ct = r.headers.get('content-type', '')
                if 'png' in ct:
                    ext = 'png'
                elif 'webp' in ct:
                    ext = 'webp'
                elif 'gif' in ct:
                    ext = 'gif'
                zf.writestr(f"{listing_id}_{idx}.{ext}", r.content)
            except Exception:
                continue
    mem.seek(0)
    return send_file(
        mem,
        mimetype='application/zip',
        as_attachment=True,
        download_name=f'haraj_listing_{listing_id}_images.zip'
    )


@app.route('/listing/<listing_id>')
def view_listing(listing_id):
    """View individual listing details (from saved)"""
    listings = load_saved_listings()
    listing = next((l for l in listings if str(l.get('listing_id')) == str(listing_id)), None)
    
    if not listing:
        return "Listing not found", 404
    
    return render_template('listing_detail.html', listing=listing)


@app.route('/download/json')
def download_json():
    """Download saved listings as JSON"""
    if SAVED_LISTINGS_FILE.exists():
        return send_file(str(SAVED_LISTINGS_FILE), as_attachment=True, download_name='haraj_saved_listings.json')
    json_file = DATA_DIR / "listings.json"
    if json_file.exists():
        return send_file(str(json_file), as_attachment=True, download_name='haraj_listings.json')
    return "No data file found", 404

@app.route('/download/csv')
def download_csv():
    """Download saved listings as CSV with contact information"""
    import re
    listings = load_saved_listings()
    if not listings:
        return "No listings found", 404
    
    # Create CSV in memory
    output = io.StringIO()
    fieldnames = [
        'listing_id', 'title', 'description', 'price', 'city', 'location',
        'posted_time', 'seller_name', 'seller_url', 'category',
        'url', 'image_count', 'tags', 'phone_number', 'whatsapp_number', 'email'
    ]
    
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    writer.writeheader()
    
    for listing in listings:
        contact_info = listing.get('contact_info', {})
        phone_numbers = contact_info.get('phone_numbers', [])
        phone_number = ', '.join(phone_numbers) if phone_numbers else ''
        
        # Extract WhatsApp number from link
        whatsapp_number = ''
        whatsapp_link = contact_info.get('whatsapp_link', '')
        if whatsapp_link:
            # Extract phone from WhatsApp link
            whatsapp_match = re.search(r'(?:wa\.me/|whatsapp.*phone=)(\d+)', whatsapp_link)
            if whatsapp_match:
                whatsapp_number = whatsapp_match.group(1)
                # Remove country code if present
                if whatsapp_number.startswith('966') and len(whatsapp_number) > 9:
                    whatsapp_number = whatsapp_number[3:]
        
        # Extract email
        emails = contact_info.get('emails', [])
        email = ', '.join(emails) if emails else ''
        
        row = {
            'listing_id': listing.get('listing_id', ''),
            'title': listing.get('title', ''),
            'description': listing.get('description', ''),
            'price': listing.get('price', ''),
            'city': listing.get('city', ''),
            'location': listing.get('location', ''),
            'posted_time': listing.get('posted_time', ''),
            'seller_name': listing.get('seller_name', ''),
            'seller_url': listing.get('seller_url', ''),
            'category': listing.get('category', ''),
            'url': listing.get('url', ''),
            'image_count': len(listing.get('images', [])),
            'tags': ', '.join(listing.get('tags', [])),
            'phone_number': phone_number,
            'whatsapp_number': whatsapp_number,
            'email': email
        }
        writer.writerow(row)
    
    # Create response
    output.seek(0)
    mem = io.BytesIO()
    mem.write(output.getvalue().encode('utf-8-sig'))
    mem.seek(0)
    
    return send_file(
        mem,
        mimetype='text/csv',
        as_attachment=True,
        download_name='haraj_listings.csv'
    )

def run_scraper(max_listings, category_url):
    """Run the scraper in background"""
    global scraping_status
    scraping_status['is_running'] = True
    scraping_status['progress'] = 0
    scraping_status['total'] = max_listings
    scraping_status['current_listing'] = 'Starting...'
    scraping_status['error'] = None
    
    try:
        # Import scraper (may fail in Vercel due to Selenium)
        try:
            from haraj_scraper_selenium import HarajScraperSelenium
        except ImportError as e:
            scraping_status['error'] = f"Selenium scraper not available in this environment: {str(e)}"
            scraping_status['is_running'] = False
            return
        
        # Load credentials from config
        config = load_config()
        username = config.get('username', '') or None
        password = config.get('password', '') or None
        
        try:
            scraper = HarajScraperSelenium(
                output_dir="scraped_data",
                download_images=False,
                headless=True,
                username=username,
                password=password
            )
        except Exception as e:
            error_msg = str(e)
            # Provide more helpful error message for ChromeDriver issues
            if "Status code was: 127" in error_msg or "chromedriver" in error_msg.lower():
                scraping_status['error'] = f"ChromeDriver initialization failed: {error_msg}\n\n" \
                    "This usually means Chrome/ChromeDriver is not installed on the server.\n" \
                    "Please check Railway build logs to ensure Chrome and ChromeDriver are installed."
            else:
                scraping_status['error'] = f"Failed to initialize scraper: {error_msg}"
            scraping_status['is_running'] = False
            return
        
        try:
            # Find listing URLs: request exact target so we scrape the requested count
            max_pages = max(5, (max_listings + 19) // 20)
            scraping_status['current_listing'] = 'Finding listings...'
            try:
                listing_urls = scraper.find_listing_urls(
                    category_url, max_pages=max_pages, target_count=max_listings
                )
                listing_urls = listing_urls[:max_listings]
            except Exception as e:
                scraping_status['error'] = f"Failed to find listings: {str(e)}"
                scraping_status['is_running'] = False
                try:
                    scraper.close()
                except:
                    pass
                return
            
            scraping_status['total'] = len(listing_urls)
            scraping_status['current_listing'] = f'Found {len(listing_urls)} listings. Starting to scrape...'

            # Load saved listings for duplicate check
            saved = load_saved_listings()
            existing_ids = {str(L.get('listing_id')) for L in saved if L.get('listing_id')}
            existing_urls = {(L.get('url') or '').strip().rstrip('/') for L in saved if L.get('url')}

            all_listings = []
            skipped_dupes = 0
            for idx, url in enumerate(listing_urls, 1):
                if not scraping_status['is_running']:
                    break
                scraping_status['progress'] = idx
                scraping_status['current_listing'] = f'Scraping listing {idx}/{len(listing_urls)}...'

                listing_data = scraper.scrape_listing(url)
                # Retry once if no data (page load or selector timing)
                if (not listing_data or (not listing_data.get('listing_id') and not listing_data.get('url'))):
                    time.sleep(1.5)
                    listing_data = scraper.scrape_listing(url)
                if not listing_data or (not listing_data.get('listing_id') and not listing_data.get('url')):
                    print(f"  Skipping listing - no data extracted: {url}")
                    continue
                lid = str(listing_data.get('listing_id') or '')
                url_norm = (listing_data.get('url') or '').strip().rstrip('/')
                if lid in existing_ids or url_norm in existing_urls:
                    skipped_dupes += 1
                    continue
                all_listings.append(listing_data)
                if lid:
                    existing_ids.add(lid)
                if url_norm:
                    existing_urls.add(url_norm)

            if all_listings or skipped_dupes:
                scraping_status['current_listing'] = 'Saving to saved listings...'
                try:
                    merged, added, skipped_merge = merge_saved_listings(all_listings)
                    save_saved_listings(merged)
                    scraper.save_to_json(merged, "listings.json")
                    scraper.save_to_csv(merged, "listings.csv")
                    scraping_status['current_listing'] = f'Completed! New: {added}, duplicates skipped: {skipped_dupes + skipped_merge}'
                except Exception as e:
                    scraping_status['error'] = f"Failed to save data: {str(e)}"
                scraping_status['progress'] = len(listing_urls)
            else:
                if listing_urls:
                    scraping_status['error'] = f"Found {len(listing_urls)} listing URLs but no new data saved (duplicates or no match)."
                else:
                    scraping_status['error'] = f"No listing URLs found. The website structure may have changed or the category URL is invalid: {category_url}"
        finally:
            try:
                scraper.close()
            except:
                pass
            
    except Exception as e:
        scraping_status['error'] = str(e)
        import traceback
        error_trace = traceback.format_exc()
        scraping_status['error'] = error_trace[:1000]  # Limit error length but show more
        print(f"Scraping error: {error_trace}")
    finally:
        scraping_status['is_running'] = False
        scraping_status['current_listing'] = 'Finished'

@app.route('/api/start-scraping', methods=['POST'])
def start_scraping():
    """Start scraping listings. When prompt is provided, resolve best category from prompt (OpenAI or keyword fallback)."""
    global scraping_status
    
    if scraping_status['is_running']:
        return jsonify({'error': 'Scraping is already running'}), 400
    
    try:
        data = request.get_json() or {}
        max_listings = int(data.get('max_listings', 10))
        category_url = (data.get('category_url') or '').strip()
        if not category_url:
            category_url = HARAJ_BASE + quote('حراج السيارات')
        if max_listings < 1 or max_listings > 500:
            return jsonify({'error': 'Number of listings must be between 1 and 500'}), 400

        thread = threading.Thread(target=run_scraper, args=(max_listings, category_url))
        thread.daemon = True
        thread.start()
        return jsonify({
            'status': 'started',
            'message': f'Scraping started for {max_listings} listings from Haraj',
            'category_used': category_url,
        })
    except Exception as e:
        return jsonify({'error': f'Failed to start scraping: {str(e)}'}), 500

@app.route('/api/estimate-time', methods=['GET'])
def estimate_time_api():
    """Estimate scrape time for given max_listings and login state (for big batches: 200, 300, 500)."""
    try:
        max_listings = int(request.args.get('max_listings', 10))
        max_listings = max(1, min(500, max_listings))
        config = load_config()
        has_login = bool(config.get('username') and config.get('password'))
        try:
            from haraj_scraper_selenium import estimate_scrape_time
            est = estimate_scrape_time(max_listings, use_compliance_delays=has_login, download_images=False)
            return jsonify({
                'ok': True,
                'max_listings': max_listings,
                'has_login': has_login,
                'min_minutes': est['min_minutes'],
                'max_minutes': est['max_minutes'],
                'min_seconds': est['min_seconds'],
                'max_seconds': est['max_seconds'],
                'description': est['description'],
            })
        except ImportError:
            return jsonify({
                'ok': False,
                'error': 'Scraper module not available',
                'max_listings': max_listings,
                'has_login': has_login,
            })
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)}), 400


@app.route('/api/scraping-status')
def scraping_status_api():
    """Get current scraping status"""
    return jsonify(scraping_status)

@app.route('/api/stop-scraping', methods=['POST'])
def stop_scraping():
    """Stop scraping (if possible)"""
    global scraping_status
    # Note: This is a simple implementation. For full control, you'd need process management
    scraping_status['is_running'] = False
    scraping_status['error'] = "Scraping stopped by user (may take a moment to fully halt current task)."
    return jsonify({'message': 'Scraping stop requested', 'status': scraping_status})

@app.route('/api/settings', methods=['GET'])
def get_settings():
    """Get scraper settings (credentials only)."""
    config = load_config()
    return jsonify({
        'username': config.get('username', ''),
        'has_password': bool(config.get('password', '')),
    })

@app.route('/api/settings', methods=['POST'])
def save_settings():
    """Save scraper settings (Haraj credentials only)."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'message': 'No data provided', 'success': False}), 400
        username = data.get('username', '').strip()
        password = data.get('password', '').strip()
        config = load_config()
        if password:
            config['password'] = password
        config['username'] = username
        if save_config(config):
            return jsonify({
                'message': 'Settings saved successfully',
                'success': True,
                'config_path': str(CONFIG_FILE),
            })
        return jsonify({
            'message': f'Failed to save settings. Check file permissions for: {CONFIG_FILE}',
            'success': False,
            'error': 'File write error'
        }), 500
    except Exception as e:
        return jsonify({
            'message': f'Error saving settings: {str(e)}',
            'success': False,
            'error': str(e)
        }), 500

def _log_registered_api_routes():
    """Log API routes at startup so you can confirm /api/estimate-time and /api/save-listings exist."""
    api_routes = sorted(r.rule for r in app.url_map.iter_rules() if r.rule.startswith('/api/'))
    if '/api/estimate-time' in api_routes and '/api/save-listings' in api_routes:
        print("  API routes OK: /api/estimate-time, /api/save-listings, ...")
    else:
        print("  WARNING: Missing API routes! Registered:", api_routes)


if __name__ == '__main__':
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
    print("=" * 70)
    print("Haraj Scraper Dashboard")
    print("=" * 70)
    _log_registered_api_routes()
    print(f"\nDashboard running at: http://localhost:5000")
    print(f"Data directory: {DATA_DIR.absolute()}")
    print("\nMake sure you have scraped some listings first!")
    print("Run: python haraj_scraper_selenium.py --category <URL> --max-listings 20")
    print("=" * 70 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
