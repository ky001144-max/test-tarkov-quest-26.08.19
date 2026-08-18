import requests

headers = {"User-Agent": "Mozilla/5.0"}
files = [
    ("TarkovMap_vue", "https://raw.githubusercontent.com/TarkovTracker/tarkovtracker/master/tarkov-tracker/src/components/TarkovMap.vue"),
    ("MapMarker_vue", "https://raw.githubusercontent.com/TarkovTracker/tarkovtracker/master/tarkov-tracker/src/components/MapMarker.vue"),
    ("MapZone_vue", "https://raw.githubusercontent.com/TarkovTracker/tarkovtracker/master/tarkov-tracker/src/components/MapZone.vue")
]

for name, url in files:
    r = requests.get(url, headers=headers)
    print(f"{name}: status {r.status_code}")
    if r.status_code == 200:
        with open(f"intermediate_results/{name}.vue", "w", encoding="utf-8") as f:
            f.write(r.text)
        print(f"  Saved intermediate_results/{name}.vue ({len(r.text)} bytes)")
