import requests
import json
import re

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

url = "https://tarkov-market.com/maps/customs"
r = requests.get(url, headers=headers)

# Extract Nuxt data if present
nuxt_data = re.search(r'<script type="application/json" id="__NUXT_DATA__"[^>]*>(.*?)</script>', r.text)
if nuxt_data:
    raw_json = nuxt_data.group(1)
    print(f"Found __NUXT_DATA__ ({len(raw_json)} bytes)")
    try:
        data = json.loads(raw_json)
        print(f"Nuxt data elements: {len(data)}")
        # Check string contents for quest, extract, markers, coordinates
        markers_str = [str(x) for x in data if isinstance(x, (dict, list, str)) and any(k in str(x).lower() for k in ["quest", "marker", "pocket watch", "customs", "extract"])]
        print(f"Relevant data snippets ({len(markers_str)}):")
        for s in markers_str[:15]:
            print("  -", s[:120])
    except Exception as e:
        print("JSON parse error:", e)
else:
    print("No __NUXT_DATA__ found. Checking embedded JSON...")
    # Find all inline json
    inline_jsons = re.findall(r'window\.__[A-Z_]+__\s*=\s*(\{.*?\});', r.text)
    print(f"Found {len(inline_jsons)} inline JSON objects.")
