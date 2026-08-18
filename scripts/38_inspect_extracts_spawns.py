import json

with open("primary_data/tarkov_dev_maps_json.json", "r", encoding="utf-8") as f:
    maps_data = json.load(f)

for m in maps_data:
    if m.get("normalizedName") == "customs":
        print(f"Map: {m.get('name')} ({m.get('normalizedName')})")
        print(f"Extracts count: {len(m.get('extracts', []))}")
        for ext in m.get('extracts', [])[:5]:
            print(f"  - Extract: {ext.get('name')} -> pos: {ext.get('position')}, faction: {ext.get('faction')}")
        print(f"Spawns count: {len(m.get('spawns', []))}")
        for sp in m.get('spawns', [])[:3]:
            print(f"  - Spawn: {sp.get('zoneName')} -> pos: {sp.get('position')}")
