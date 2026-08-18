import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open("map_data/maps_ko.txt", "r", encoding="utf-8") as f:
    maps_raw = json.load(f)

with open("map_data/tasks_ko.txt", "r", encoding="utf-8") as f:
    tasks_raw = json.load(f)

print("1. maps_ko structure:")
if "data" in maps_raw:
    maps_list = maps_raw["data"]["maps"]
    print(f"   -> Found {len(maps_list)} maps in data.maps:")
    for m in maps_list:
        print(f"      * {m.get('name')} (id: {m.get('id')}, normalizedName: {m.get('normalizedName')})")
else:
    print("   -> maps_ko keys:", list(maps_raw.keys()))

print("\n2. tasks_ko structure:")
if "data" in tasks_raw:
    tasks_list = tasks_raw["data"]["tasks"]
    print(f"   -> Found {len(tasks_list)} tasks in data.tasks!")
    
    # Check sample task structure
    sample = tasks_list[0]
    print(f"      * Sample Task Name: {sample.get('name')}")
    print(f"      * Trader: {sample.get('trader')}")
    print(f"      * Objectives count: {len(sample.get('objectives', []))}")
    for obj in sample.get('objectives', []):
        print(f"         - Obj Type: {obj.get('type')}, desc: {obj.get('description')}")
        zones = obj.get('zones', [])
        print(f"           zones count: {len(zones)}")
        for z in zones:
            print(f"             pos: {z.get('position')}, map: {z.get('map')}")
