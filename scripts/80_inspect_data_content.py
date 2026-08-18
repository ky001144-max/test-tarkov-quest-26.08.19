import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open("map_data/tasks.txt", "r", encoding="utf-8") as f:
    raw_tasks = json.load(f)

data_content = raw_tasks.get("data")
print("data type:", type(data_content))

if isinstance(data_content, list):
    print("data is a list with length:", len(data_content))
    sample = data_content[0]
    print("Sample task:", sample.get("name"), "Trader:", sample.get("trader"), "Map:", sample.get("map"))
    print("Sample objectives:", len(sample.get("objectives", [])))
    for o in sample.get("objectives", []):
        print("  -", o.get("type"), o.get("description"), "zones:", len(o.get("zones", [])))
        for z in o.get("zones", []):
            print("     zone pos:", z.get("position"), "map:", z.get("map"))
elif isinstance(data_content, dict):
    print("data is a dict with keys:", list(data_content.keys())[:10])
