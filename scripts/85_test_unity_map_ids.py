import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open("map_data/tasks.txt", "r", encoding="utf-8") as f:
    raw = json.load(f)

tasks_dict = raw["data"]["tasks"]

with open("map_data/tasks_ko.txt", "r", encoding="utf-8") as f:
    i18n = json.load(f).get("data", {})

unity_map_ids = {
    "56f40101d2720b2a4d8b45d6": "customs",
    "55f2d3fd4bdc2d5f408b4567": "factory",
    "5704e4dad2720bb55b8b4567": "woods",
    "5704e554d2720bac5b8b456e": "shoreline",
    "5714dc692459777137212e12": "interchange",
    "5b0fc42d86f7744a585f9105": "lab",
    "5704e3c2d2720bac5b8b4567": "reserve",
    "5704e5fad2720bc05b8b4567": "lighthouse",
    "5714dbc024597771384a510d": "streetsoftarkov",
    "653e6760052c01c1c805532f": "groundzero",
    "65b8d6f5cdde2479cb2a3125": "groundzero"
}

# Count quests per map
map_counts = {}
for q_id, q in tasks_dict.items():
    m = q.get("map")
    norm_m = unity_map_ids.get(m, "any")
    map_counts[norm_m] = map_counts.get(norm_m, 0) + 1

print("Quests per Unity Map:")
for m, c in sorted(map_counts.items(), key=lambda x: x[1], reverse=True):
    print(f"  * {m:20s}: {c} quests")

# Check Checking and Delivery from past
checking_sample = []
for q_id, q in tasks_dict.items():
    raw_name_key = f"{q_id} name"
    name_ko = i18n.get(raw_name_key) or i18n.get(f"{q_id} Name") or ""
    if any(k in name_ko for k in ["확인 작업", "과거로부터", "두더지", "첫 번째"]):
        print(f"\nFound Quest: {name_ko} (id: {q_id}, map: {unity_map_ids.get(q.get('map'))})")
        for o in q.get("objectives", []):
            desc = i18n.get(o.get("description")) or o.get("description")
            print(f"  - Obj: {desc}")
            for z in o.get("zones", []):
                print(f"     zone pos: {z.get('position')} on map: {unity_map_ids.get(z.get('map'))}")
