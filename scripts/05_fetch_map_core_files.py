import requests
import json

headers = {"User-Agent": "Mozilla/5.0"}
files = [
    ("tarkov_dev_maps_json", "https://raw.githubusercontent.com/the-hideout/tarkov-dev/main/src/data/maps.json"),
    ("tarkov_dev_maps_static_json", "https://raw.githubusercontent.com/the-hideout/tarkov-dev/main/src/data/maps_static.json"),
    ("tarkov_dev_map_page_jsx", "https://raw.githubusercontent.com/the-hideout/tarkov-dev/main/src/pages/map/index.jsx"),
    ("tarkov_dev_map_images_mjs", "https://raw.githubusercontent.com/the-hideout/tarkov-dev/main/src/pages/map/map-images.mjs"),
]

for name, url in files:
    r = requests.get(url, headers=headers)
    print(f"{name}: status {r.status_code}")
    if r.status_code == 200:
        ext = ".json" if "json" in name else (".jsx" if "jsx" in name else ".mjs")
        with open(f"primary_data/{name}{ext}", "w", encoding="utf-8") as f:
            f.write(r.text)
        print(f"  Saved primary_data/{name}{ext} ({len(r.text)} bytes)")
