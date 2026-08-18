import json

# Let's inspect tarkov_dev_maps_json.json to see the exact transform matrix for each map
with open("primary_data/tarkov_dev_maps_json.json", "r", encoding="utf-8") as f:
    maps_data = json.load(f)

print("Tarkov.dev Official Map Transforms:")
for m in maps_data:
    norm = m.get("normalizedName")
    submaps = m.get("maps", [])
    for sm in submaps:
        if sm.get("projection") == "interactive":
            print(f"\nMap: {norm} ({sm.get('name')})")
            print(f"  - transform: {sm.get('transform')}")
            print(f"  - coordinateRotation: {sm.get('coordinateRotation')}")
            print(f"  - bounds: {sm.get('bounds')}")
