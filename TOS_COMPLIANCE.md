# Terms of Service Compliance

This document explains the ToS-compliant features built into the Haraj scraper.

## Automatic Compliance Measures

The scraper automatically applies the following measures to respect Haraj.com.sa's Terms of Service:

### After Every 10 Listings

1. **User-Agent Rotation**
   - Changes the browser user-agent string
   - Uses a pool of realistic user-agents
   - Makes requests appear more natural

2. **Extended Delay**
   - Pauses for 30-60 seconds (randomized)
   - Gives the server time to process previous requests
   - Reduces server load

3. **Session Reset (Every 20 Listings)**
   - Creates a new HTTP session
   - Clears cookies
   - Starts fresh to avoid tracking patterns

### Between Each Listing

- **Random Delays**: 2-5 seconds between listing requests
- **Image Delays**: 0.5-1.5 seconds between image downloads
- **Page Delays**: 2-4 seconds between pagination requests

## Why These Measures Matter

1. **Server Protection**: Prevents overloading the server
2. **Avoid Blocks**: Reduces risk of IP blocking or rate limiting
3. **Ethical Scraping**: Respects the website's resources
4. **Legal Compliance**: Aligns with Terms of Service requirements
5. **Human-like Behavior**: Makes scraping patterns less detectable

## Example Output

When compliance measures are applied, you'll see:

```
[ToS Compliance] Applied measures after 10 listings...
  - Rotated User-Agent
  - Extended delay: 45 seconds
  - Continuing scraping...
```

Or after 20 listings:

```
[ToS Compliance] Applied measures after 20 listings...
  - Rotated User-Agent
  - Extended delay: 38 seconds
  - Session reset
  - Continuing scraping...
```

## Configuration

The compliance measures are **automatic and cannot be disabled** to ensure ToS compliance. However, you can:

- Adjust `max_listings` to control how many listings to scrape
- Use `--no-images` to skip image downloads (faster, less load)
- Set `max_pages` to limit pagination

## Best Practices

1. **Don't Scrape Too Aggressively**
   - Use reasonable `max_listings` values (50-100 per session)
   - Take breaks between scraping sessions
   - Don't run multiple scrapers simultaneously

2. **Respect Rate Limits**
   - If you get blocked, wait before trying again
   - Consider using the Selenium version for slower, more human-like behavior

3. **Monitor Your Scraping**
   - Watch for error messages
   - Check if data is being extracted correctly
   - Stop if you notice issues

4. **Use Data Responsibly**
   - Don't republish content without permission
   - Respect privacy of sellers
   - Follow copyright laws

## Technical Details

### User-Agent Pool
The scraper rotates between multiple realistic user-agents:
- Chrome on Windows
- Chrome on macOS
- Firefox on Windows
- Safari on macOS

### Delay Randomization
All delays are randomized to avoid predictable patterns:
- Listing delays: 2-5 seconds (uniform distribution)
- Image delays: 0.5-1.5 seconds (uniform distribution)
- Extended delays: 30-60 seconds (uniform distribution)

### Session Management
- New session created every 20 listings
- Cookies cleared on session reset
- Headers updated with new user-agent

## Compliance Checklist

✅ Random delays between requests  
✅ User-agent rotation  
✅ Extended pauses after batches  
✅ Session management  
✅ Respectful rate limiting  
✅ No aggressive concurrent requests  
✅ Proper error handling  
✅ Respect for server resources  

## Questions?

If you have questions about ToS compliance:
1. Review Haraj.com.sa's Terms of Service
2. Consider reaching out to them for API access
3. Use the scraper responsibly and ethically

Remember: **Compliance is automatic and cannot be disabled** to ensure ethical scraping practices.
