import json

with open("primary_data/tarkov_dev_maps_json.json", "r", encoding="utf-8") as f:
    data = json.load(f)

print(f"Total maps: {len(data)}")
for m in data:
    print(f"\nMap: {m.get('name')} (id: {m.get('id')}, norm: {m.get('normalizedName')})")
    print(f"  - Keys: {list(m.keys())}")
    if 'maps' in m:
        print(f"  - Submaps / variants: {len(m['maps'])}")
        for sm in m['maps']:
            print(f"     * {sm.get('name')} | projection: {sm.get('projection')} | svg: {sm.get('svg')}")
    if 'spawns' in m:
        print(f"  - Spawns: {len(m.get('spawns', []))}")
    if 'extracts' in m:
        print(f"  - Extracts: {len(m.get('extracts', []))}")
    if 'stationaryGuns' in m:
        print(f"  - StationaryGuns: {len(m.get('stationaryGuns', []))}")
    if 'hazards' in m:
        print(f"  - Hazards: {len(m.get('hazards', []))}")
