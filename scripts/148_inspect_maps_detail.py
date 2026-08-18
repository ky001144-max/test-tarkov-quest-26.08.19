import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

print("=== 1. Inspecting maps.txt Detailed Structure ===")
with open("map_data/tarkov dev/maps.txt", "r", encoding="utf-8") as f:
    maps_raw = json.load(f)

data = maps_raw.get("data", {})
print("data keys:", list(data.keys()))

maps_obj = data.get("maps")
print("data.maps type:", type(maps_obj))

if isinstance(maps_obj, dict):
    print("Total maps in dict:", len(maps_obj))
    for k, m in list(maps_obj.items())[:5]:
        print(f"\nMap Key: {k}")
        if isinstance(m, dict):
            print(f"  Name: {m.get('name')}, normalizedName: {m.get('normalizedName')}")
            print(f"  Bounds: {m.get('bounds')}")
            print(f"  svgBounds: {m.get('svgBounds')}")
            print(f"  transform: {m.get('transform')}")
            print(f"  coordinateRotation: {m.get('coordinateRotation')}")
            print(f"  keys: {list(m.keys())}")
elif isinstance(maps_obj, list):
    print("Total maps in list:", len(maps_obj))
    for m in maps_obj[:5]:
        if isinstance(m, dict):
            print(f"\nMap Item: {m.get('name')}, keys: {list(m.keys())}")
        else:
            print("Map Item (str):", m)
