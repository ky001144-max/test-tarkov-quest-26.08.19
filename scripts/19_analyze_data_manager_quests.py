import json

path = "tarkov-data-manager-main/src/tarkov-data-manager/public/data/quest-data.json"
with open(path, "r", encoding="utf-8") as f:
    data = json.load(f)

print(f"Total Quests in quest-data.json: {len(data)}")
sample = data[0] if isinstance(data, list) else list(data.values())[0]
print("\nSample Quest Structure:")
print(json.dumps(sample, indent=2, ensure_ascii=False)[:1000])

# Check how maps and objectives/positions are structured in quest-data.json
maps_found = set()
quests_with_map = 0
quests_with_zones_or_positions = 0

for q in (data if isinstance(data, list) else data.values()):
    if 'map' in q or 'maps' in q or 'location' in q:
        quests_with_map += 1
        m = q.get('map') or q.get('maps') or q.get('location')
        if isinstance(m, list):
            for item in m:
                maps_found.add(str(item))
        else:
            maps_found.add(str(m))
            
    for obj in q.get('objectives', []):
        if any(k in obj for k in ['zone', 'position', 'gps', 'location', 'coordinates', 'marker', 'places']):
            quests_with_zones_or_positions += 1
            break

print(f"\nQuests with Map info: {quests_with_map} / {len(data)}")
print(f"Maps found: {maps_found}")
print(f"Quests with zone/position info: {quests_with_zones_or_positions}")
