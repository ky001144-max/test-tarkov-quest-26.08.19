import requests
import os

os.makedirs("app/libs/leaflet", exist_ok=True)

files = [
    ("leaflet.js", "https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"),
    ("leaflet.css", "https://unpkg.com/leaflet@1.9.4/dist/leaflet.css")
]

headers = {"User-Agent": "Mozilla/5.0"}

for fname, url in files:
    try:
        r = requests.get(url, headers=headers, timeout=10)
        if r.status_code == 200:
            with open(f"app/libs/leaflet/{fname}", "w", encoding="utf-8") as f:
                f.write(r.text)
            print(f"Downloaded app/libs/leaflet/{fname} ({len(r.text)} bytes)")
    except Exception as e:
        print(f"Error downloading {fname}: {e}")
