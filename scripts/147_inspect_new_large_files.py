import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

print("=== 1. Inspecting maps.txt (30MB) ===")
with open("map_data/tarkov dev/maps.txt", "r", encoding="utf-8") as f:
    maps_raw = json.load(f)

print("maps.txt type:", type(maps_raw))
if isinstance(maps_raw, dict):
    print("maps.txt root keys:", list(maps_raw.keys()))
    if "data" in maps_raw:
        data_keys = list(maps_raw["data"].keys())
        print(f"data keys count: {len(data_keys)}")
        print("sample data keys:", data_keys[:10])
        # Check if maps list or dict
        if isinstance(maps_raw["data"], dict) and "maps" in maps_raw["data"]:
            maps_list = maps_raw["data"]["maps"]
            print(f"Maps count in data.maps: {len(maps_list)}")
            for m in maps_list:
                print(f"  - Map: {m.get('name')} ({m.get('normalizedName')}), bounds: {m.get('bounds')}, svgBounds: {m.get('svgBounds')}")
                if "layers" in m:
                    print(f"    Layers: {len(m['layers'])}")
                if "spawns" in m:
                    print(f"    Spawns: {len(m['spawns'])}")
                if "extracts" in m:
                    print(f"    Extracts: {len(m['extracts'])}")
                if "markers" in m:
                    print(f"    Markers: {len(m['markers'])}")

print("\n=== 2. Inspecting items.txt (34MB) ===")
with open("map_data/tarkov dev/items.txt", "r", encoding="utf-8") as f:
    items_raw = json.load(f)

print("items.txt type:", type(items_raw))
if isinstance(items_raw, dict):
    print("items.txt root keys:", list(items_raw.keys()))
    if "data" in items_raw and isinstance(items_raw["data"], dict):
        if "items" in items_raw["data"]:
            print(f"Total items count: {len(items_raw['data']['items'])}")
            sample_items = items_raw['data']['items'][:5]
            for it in sample_items:
                print(f"  - Item: {it.get('id')}, name: {it.get('name')}, shortName: {it.get('shortName')}")
