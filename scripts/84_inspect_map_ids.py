import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open("map_data/tasks.txt", "r", encoding="utf-8") as f:
    raw = json.load(f)

tasks_dict = raw["data"]["tasks"]

all_maps = set()
all_zone_maps = set()

for q_id, q in tasks_dict.items():
    m = q.get("map")
    if m:
        all_maps.add(m)
    for o in q.get("objectives", []):
        for z in o.get("zones", []):
            zm = z.get("map")
            if zm:
                all_zone_maps.add(zm)

print(f"Task Map IDs ({len(all_maps)}):", all_maps)
print(f"Zone Map IDs ({len(all_zone_maps)}):", all_zone_maps)

# Let's inspect map details from primary_data/tarkov_dev_maps.json to get exact id mapping
with open("primary_data/tarkov_dev_maps.json", "r", encoding="utf-8") as f:
    official_maps = json.load(f)

print("\nOfficial Maps ID mapping:")
for om in official_maps:
    print(f"  ID: {om.get('id')} -> name: {om.get('name')}, normalizedName: {om.get('normalizedName')}")
