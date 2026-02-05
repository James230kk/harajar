# Put the Dashboard Live on Your Subdomain

This guide gets the Haraj Scraper Dashboard running on **your subdomain** (e.g. `haraj.yourdomain.com`) with **all saved data** (listings, database, settings) persisting across deploys.

---

## 1. Deploy to Railway (recommended)

Your project already has a **Dockerfile** and **railway.toml**, so Railway can run it as-is.

1. **Push your code to GitHub** (if not already).
2. Go to [railway.app](https://railway.app) → **New Project** → **Deploy from GitHub repo**.
3. Select this repo. Railway will build from the **Dockerfile** (Chrome + app).
4. If Railway uses Nixpacks instead of Docker, follow **FORCE_DOCKER_ON_RAILWAY.md** so it uses the Dockerfile.

---

## 2. Add persistent storage (so data survives redeploys)

Without a volume, the container’s filesystem is reset on each deploy, so listings and settings would be lost.

1. In Railway: open your **project** → select the **service** (your app).
2. Go to the **Variables** tab and add:
   - `HARAJ_DATA_DIR` = `/data`
3. Go to the **Volumes** tab (or **Settings** → **Volumes**):
   - Click **Add Volume**.
   - Mount path: **`/data`** (must match `HARAJ_DATA_DIR`).
   - Create the volume.
4. **Redeploy** the service so the new volume and env are applied.

All of this will now live on the volume and persist:

- `listings.db` (SQLite)
- `saved_listings.json`
- `scraper_config.json` (if you put it in `/data` — see below)

**Optional:** Store config on the same volume by adding:

- `HARAJ_CONFIG_FILE` = `/data/scraper_config.json`

Then both data and Haraj credentials persist in `/data`.

---

## 3. Use your subdomain

You can use either Railway’s default subdomain or your own.

### Option A: Railway’s default subdomain

1. In the service, open **Settings** → **Networking** / **Domains**.
2. Railway will show a URL like:  
   `https://your-service.up.railway.app`
3. Use that URL; no DNS changes needed.

### Option B: Your own subdomain (e.g. `haraj.yourdomain.com`)

1. In the same **Settings** → **Domains** (or **Networking**):
   - Click **Custom Domain** (or **Add domain**).
   - Enter your subdomain, e.g. **`haraj.yourdomain.com`**.
2. Railway will show a **CNAME** target (e.g. `something.up.railway.app`).
3. In your DNS provider (where you manage `yourdomain.com`):
   - Add a **CNAME** record:
     - **Name/host:** `haraj` (or `haraj.yourdomain.com` depending on the provider).
     - **Value/target:** the CNAME Railway gave you.
   - Save and wait for DNS to propagate (often 5–30 minutes).
4. In Railway, confirm the domain shows as active/verified.  
   Your app will then be live at **https://haraj.yourdomain.com**.

---

## 4. Environment variables summary

| Variable             | Required | Example        | Purpose |
|----------------------|----------|----------------|---------|
| `HARAJ_DATA_DIR`     | Yes*     | `/data`        | Where to store DB + JSON; use the volume mount path. |
| `HARAJ_CONFIG_FILE`  | No       | `/data/scraper_config.json` | Optional: store settings on the volume too. |

\* Required for persistence on Railway; optional locally (defaults to `scraped_data/`).

---

## 5. Check that everything works

1. Open your live URL (Railway subdomain or your custom subdomain).
2. **Settings:** Save Haraj username/password; reload the page and confirm they’re still there.
3. **Scrape:** Run a small scrape (e.g. 5–10 listings).
4. **Saved data:** Open “المحفوظات / Saved listings” and use “حفظ في قاعدة البيانات” — confirm listings and counts.
5. **Redeploy** the service in Railway, then reload the app: listings and settings should still be there (they’re on the volume).

---

## 6. If you use another host (VPS, Render, etc.)

- **Render:** Add a **Disk** (persistent volume), set mount path (e.g. `/data`), and set `HARAJ_DATA_DIR=/data`.
- **VPS (Linux):** Run with Docker or gunicorn; set `HARAJ_DATA_DIR` to a path on the server (e.g. `/var/lib/haraj-data`) and put the DB/JSON there. Point your subdomain at this server (nginx/Caddy + reverse proxy to the app).

The app reads **`HARAJ_DATA_DIR`** (or **`DATA_DIR`**) and **`HARAJ_CONFIG_FILE`** (or **`CONFIG_FILE`**) from the environment, so any host that supports env vars and a persistent path can keep all save data and show it on your subdomain.
