import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open("map_data/maps_ko.txt", "r", encoding="utf-8") as f:
    maps_raw = json.load(f)

with open("map_data/tasks_ko.txt", "r", encoding="utf-8") as f:
    tasks_raw = json.load(f)

print("maps_ko data keys:", list(maps_raw["data"].keys()) if "data" in maps_raw else list(maps_raw.keys()))
print("tasks_ko data keys:", list(tasks_raw["data"].keys()) if "data" in tasks_raw else list(tasks_raw.keys()))

if "data" in maps_raw:
    d = maps_raw["data"]
    for k in d:
        print(f"  maps_raw['data']['{k}'] type: {type(d[k])}, len: {len(d[k]) if hasattr(d[k], '__len__') else 'N/A'}")

if "data" in tasks_raw:
    d = tasks_raw["data"]
    for k in d:
        print(f"  tasks_raw['data']['{k}'] type: {type(d[k])}, len: {len(d[k]) if hasattr(d[k], '__len__') else 'N/A'}")
