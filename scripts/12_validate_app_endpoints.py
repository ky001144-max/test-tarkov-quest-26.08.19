import requests
import json

base_url = "http://localhost:8089"

endpoints = [
    "/index.html",
    "/style.css",
    "/map_viewer.js",
    "/quest_manager.js",
    "/app.js",
    "/data/maps.json",
    "/data/quests.json",
    "/data/traders.json",
    "/maps/Customs.svg",
    "/maps/Factory.svg",
    "/maps/GroundZero.svg",
    "/maps/Interchange.svg",
    "/maps/Labs.svg",
    "/maps/Lighthouse.svg",
    "/maps/Reserve.svg",
    "/maps/Shoreline.svg",
    "/maps/StreetsOfTarkov.svg",
    "/maps/Woods.svg"
]

print("Verifying Application Assets on Server...")
all_ok = True
for ep in endpoints:
    url = f"{base_url}{ep}"
    try:
        r = requests.get(url)
        status = r.status_code
        size = len(r.content)
        if status == 200:
            print(f"  [OK 200] {ep} ({size} bytes)")
        else:
            print(f"  [FAIL {status}] {ep}")
            all_ok = False
    except Exception as e:
        print(f"  [ERR] {ep}: {e}")
        all_ok = False

# Validate JSON data
quests_req = requests.get(f"{base_url}/data/quests.json")
quests = quests_req.json()
print(f"\nLoaded {len(quests)} quests from server.")
gps_count = sum(1 for q in quests if any(o.get('position') or o.get('gps') for o in q.get('objectives', [])))
print(f"Quests with 3D GPS coordinates: {gps_count} / {len(quests)}")

if all_ok:
    print("\n All assets, maps, and datasets are successfully validated and serving properly!")
else:
    print("\n Some assets failed to load.")
