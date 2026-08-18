import requests
import json
import os

os.makedirs("primary_data/maps_svg", exist_ok=True)
headers = {"User-Agent": "Mozilla/5.0"}

svg_maps = [
    "Customs.svg",
    "Factory.svg",
    "GroundZero.svg",
    "Interchange.svg",
    "Labs.svg",
    "Lighthouse.svg",
    "Reserve.svg",
    "Shoreline.svg",
    "StreetsOfTarkov.svg",
    "Terminal.svg",
    "Woods.svg"
]

print("Downloading SVG maps from the-hideout/tarkov-dev-svg-maps...")
for map_file in svg_maps:
    url = f"https://raw.githubusercontent.com/the-hideout/tarkov-dev-svg-maps/main/{map_file}"
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        with open(f"primary_data/maps_svg/{map_file}", "w", encoding="utf-8") as f:
            f.write(r.text)
        print(f"  Downloaded primary_data/maps_svg/{map_file} ({len(r.text)} bytes)")
    else:
        # Try master branch
        url = f"https://raw.githubusercontent.com/the-hideout/tarkov-dev-svg-maps/master/{map_file}"
        r = requests.get(url, headers=headers)
        if r.status_code == 200:
            with open(f"primary_data/maps_svg/{map_file}", "w", encoding="utf-8") as f:
                f.write(r.text)
            print(f"  Downloaded primary_data/maps_svg/{map_file} ({len(r.text)} bytes)")
        else:
            print(f"  Failed to download {map_file}: status {r.status_code}")

# Download additional tracker & tarkov metadata
more_files = [
    ("traders.json", "https://raw.githubusercontent.com/TarkovTracker/tarkovdata/master/traders.json"),
    ("items.json", "https://raw.githubusercontent.com/TarkovTracker/tarkovdata/master/items.json"),
    ("locales_ko.json", "https://raw.githubusercontent.com/TarkovTracker/tarkovdata/master/locales/ko.json"),
    ("locales_en.json", "https://raw.githubusercontent.com/TarkovTracker/tarkovdata/master/locales/en.json"),
]

for name, url in more_files:
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        with open(f"primary_data/{name}", "w", encoding="utf-8") as f:
            f.write(r.text)
        print(f"Downloaded primary_data/{name} ({len(r.text)} bytes)")
    else:
        print(f"Failed {name}: status {r.status_code}")
