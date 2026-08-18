import requests
import json
from bs4 import BeautifulSoup
import re

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
}

try:
    url = "https://tarkov-market.com/maps/customs"
    r = requests.get(url, headers=headers, timeout=10)
    print(f"Status for {url}: {r.status_code}")
    if r.status_code == 200:
        html = r.text
        print(f"HTML length: {len(html)}")
        # Check script tags
        scripts = re.findall(r'<script[^>]*src="([^"]+)"', html)
        print("Script srcs in page:")
        for s in scripts[:10]:
            print("  -", s)
            
        # Check if there are api or json calls mentioned
        api_matches = re.findall(r'https?://[^\s"\']+(?:api|json|maps|coords|markers)[^\s"\']*', html)
        print(f"API/JSON/Map matches found: {len(api_matches)}")
        for m in api_matches[:10]:
            print("  *", m)
    else:
        print(r.text[:500])
except Exception as e:
    print("Error connecting to tarkov-market.com:", e)
