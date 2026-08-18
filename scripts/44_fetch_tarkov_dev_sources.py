import requests
import json
import os

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

# 1. Fetch complete tarkov.dev raw tasks/quests with zones and positions if available from GitHub / API
endpoints = [
    ("tarkov_dev_maps", "https://raw.githubusercontent.com/the-hideout/tarkov-dev/main/src/data/maps.json"),
    ("tarkov_dev_maps_static", "https://raw.githubusercontent.com/the-hideout/tarkov-dev/main/src/data/maps_static.json"),
]

for name, url in endpoints:
    try:
        r = requests.get(url, headers=headers)
        if r.status_code == 200:
            with open(f"primary_data/{name}.json", "w", encoding="utf-8") as f:
                f.write(r.text)
            print(f"Downloaded primary_data/{name}.json ({len(r.text)} bytes)")
    except Exception as e:
        print(f"Error {name}: {e}")

# Check local tarkov-data-manager datasets
quest_data_path = "tarkov-data-manager-main/src/tarkov-data-manager/public/data/quest-data.json"
if os.path.exists(quest_data_path):
    print(f"Found local quest-data.json ({os.path.getsize(quest_data_path)} bytes)")

print("Data source inspection complete.")
