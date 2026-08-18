import json

with open("primary_data/tarkov_dev_maps_json.json", "r", encoding="utf-8") as f:
    maps_data = json.load(f)

for m in maps_data:
    if m.get("normalizedName") == "customs":
        for sm in m.get("maps", []):
            print(f"Submap: {sm.get('name')} (projection: {sm.get('projection')})")
            print(f"  - extracts: {len(sm.get('extracts', []))}")
            for ext in sm.get('extracts', [])[:4]:
                print(f"     * {ext.get('name')}: {ext.get('position')}")
            print(f"  - spawns: {len(sm.get('spawns', []))}")
            for sp in sm.get('spawns', [])[:3]:
                print(f"     * {sp.get('zoneName')}: {sp.get('position')}")
            print(f"  - stationaryGuns: {len(sm.get('stationaryGuns', []))}")
            for gun in sm.get('stationaryGuns', [])[:3]:
                print(f"     * {gun.get('name')}: {gun.get('position')}")
