import urllib.request
import json
import re
from bs4 import BeautifulSoup
import sys

sys.stdout.reconfigure(encoding='utf-8')

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

market_url = "https://tarkov-market.com/maps/customs"
print(f"Fetching Tarkov-Market from {market_url}...")

try:
    req = urllib.request.Request(market_url, headers=headers)
    with urllib.request.urlopen(req, timeout=20) as resp:
        html = resp.read().decode('utf-8')
        with open("primary_data/market_customs_page.html", "w", encoding="utf-8") as f:
            f.write(html)
        print(f"Saved raw Tarkov-Market HTML ({len(html):,} chars) to primary_data/market_customs_page.html")
except Exception as e:
    print(f"Error fetching tarkov-market: {e}")
