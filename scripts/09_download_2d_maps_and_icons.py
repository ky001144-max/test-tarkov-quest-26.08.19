import requests
import os

os.makedirs("primary_data/maps_2d", exist_ok=True)
os.makedirs("primary_data/interactive_icons", exist_ok=True)
headers = {"User-Agent": "Mozilla/5.0"}

base_url = "https://raw.githubusercontent.com/the-hideout/tarkov-dev/main/public/maps"

maps_2d = [
    "customs-2d.jpg",
    "factory-2d.jpg",
    "ground-zero-2d.jpg",
    "interchange-2d.jpg",
    "labs-2d.jpg",
    "lighthouse-2d.jpg",
    "reserve-2d.jpg",
    "shoreline-2d.jpg",
    "streets-2d.jpg",
    "woods-2d.jpg"
]

print("Downloading 2D map raster images...")
for m in maps_2d:
    url = f"{base_url}/{m}"
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        with open(f"primary_data/maps_2d/{m}", "wb") as f:
            f.write(r.content)
        print(f"  Downloaded primary_data/maps_2d/{m} ({len(r.content)} bytes)")
    else:
        print(f"  Failed {m}: {r.status_code}")

interactive_icons = [
    "quest_item.png",
    "quest_objective.png",
    "extract_pmc.png",
    "extract_scav.png",
    "extract_shared.png",
    "spawn_pmc.png",
    "spawn_scav.png",
    "spawn_boss.png",
    "hazard.png",
    "switch.png",
    "key.png"
]

print("\nDownloading interactive map icons...")
for icon in interactive_icons:
    url = f"{base_url}/interactive/{icon}"
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        with open(f"primary_data/interactive_icons/{icon}", "wb") as f:
            f.write(r.content)
        print(f"  Downloaded primary_data/interactive_icons/{icon} ({len(r.content)} bytes)")
    else:
        print(f"  Failed icon {icon}: {r.status_code}")
