import requests
import re

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

url = "https://tarkov-market.com/maps/customs"
r = requests.get(url, headers=headers)

# Find all scripts linked in the page
scripts = re.findall(r'src="(/_nuxt3/[^"]+\.js)"', r.text) + re.findall(r'href="(/_nuxt3/[^"]+\.js)"', r.text)
print(f"Nuxt3 JS files found: {len(scripts)}")

for s in set(scripts):
    js_url = f"https://tarkov-market.com{s}"
    try:
        res = requests.get(js_url, headers=headers, timeout=5)
        if res.status_code == 200:
            content = res.text
            if any(k in content.lower() for k in ["api/v", "/api/", "markers", "quest", "leaflet", "tilelayer", "coords", "latlng"]):
                print(f"Relevant JS: {s} ({len(content)} bytes)")
                # search for API endpoints or json urls
                endpoints = re.findall(r'["\'](/api/[^"\']+)["\']', content)
                map_urls = re.findall(r'["\'](https?://[^"\']*(?:map|quest|marker|tile)[^"\']*)["\']', content)
                if endpoints:
                    print("  Endpoints:", endpoints[:5])
                if map_urls:
                    print("  Map URLs:", map_urls[:5])
    except Exception as e:
        print(f"Error fetching {s}: {e}")
