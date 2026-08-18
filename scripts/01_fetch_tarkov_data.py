import requests
import json

headers = {"User-Agent": "Mozilla/5.0"}
files = [
    ("api_tasks_mjs", "https://raw.githubusercontent.com/the-hideout/tarkov-api/main/datasources/tasks.mjs"),
    ("api_maps_mjs", "https://raw.githubusercontent.com/the-hideout/tarkov-api/main/datasources/maps.mjs"),
    ("tracker_maps_json", "https://raw.githubusercontent.com/TarkovTracker/tarkovdata/master/maps.json"),
    ("tracker_quests_json", "https://raw.githubusercontent.com/TarkovTracker/tarkovdata/master/quests.json"),
    ("tracker_tasks_json", "https://raw.githubusercontent.com/TarkovTracker/tarkovdata/master/tasks.json"),
]

for name, url in files:
    r = requests.get(url, headers=headers)
    print(f"{name}: status {r.status_code}")
    if r.status_code == 200:
        ext = ".mjs" if "mjs" in name else ".json"
        with open(f"primary_data/{name}{ext}", "w", encoding="utf-8") as f:
            f.write(r.text)
        print(f"  Saved primary_data/{name}{ext} ({len(r.text)} bytes)")
