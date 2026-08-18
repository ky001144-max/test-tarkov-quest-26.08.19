import urllib.request
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

url = "https://tarkov-market.com/api/v1/maps/map-doc?map=customs"
print(f"Fetching {url}...")

try:
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=10) as resp:
        content = resp.read().decode('utf-8')
        print(f"Response: {content}")
        with open("map_data/tarkov market/map_doc_customs.json", "w", encoding="utf-8") as f:
            f.write(content)
except Exception as e:
    print(f"Error fetching map-doc: {e}")
