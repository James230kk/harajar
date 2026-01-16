"""Quick script to show extracted data"""
import json
import sys
import io

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Load the demo results
with open('demo_output/demo_listings.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print("=" * 70)
print("EXTRACTED DATA SAMPLE")
print("=" * 70)
print(f"\nTotal Listings: {len(data)}\n")

# Show first 3 listings
for i, listing in enumerate(data[:3], 1):
    print(f"\nListing {i}:")
    print("-" * 70)
    print(f"ID: {listing.get('listing_id', 'N/A')}")
    print(f"Title: {listing.get('title', 'N/A')}")
    print(f"Description: {listing.get('description', 'N/A')[:80]}...")
    print(f"City: {listing.get('city', 'N/A')}")
    print(f"Location: {listing.get('location', 'N/A')}")
    print(f"Seller: {listing.get('seller_name', 'N/A')}")
    print(f"Posted: {listing.get('posted_time', 'N/A')}")
    print(f"Category: {listing.get('category', 'N/A')}")
    print(f"Tags: {', '.join(listing.get('tags', [])[:5])}")
    print(f"Images: {len(listing.get('images', []))} found")
    print(f"URL: {listing.get('url', 'N/A')[:60]}...")

print("\n" + "=" * 70)
print("All data saved to:")
print("  - demo_output/demo_listings.json")
print("  - demo_output/demo_listings.csv")
print("=" * 70)
