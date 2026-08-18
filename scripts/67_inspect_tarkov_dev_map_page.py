import requests
import json
import re

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

urls = [
    "https://tarkov.dev/map/customs",
    "https://tarkov.dev/maps/customs"
]

for url in urls:
    try:
        r = requests.get(url, headers=headers, timeout=10)
        print(f"Status for {url}: {r.status_code}")
        if r.status_code == 200:
            print(f"HTML Length: {len(r.text)}")
            # Search for task or quest markers json or bundle files
            scripts = re.findall(r'<script[^>]*src="([^"]+)"', r.text)
            print(f"Scripts in {url}:")
            for s in scripts:
                print("  -", s)
    except Exception as e:
        print(f"Error for {url}: {e}")
