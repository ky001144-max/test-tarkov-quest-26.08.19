import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open("map_data/tarkov dev/maps_ko.txt", "r", encoding="utf-8") as f:
    d = json.load(f)

print("Keys in maps_ko.txt:", list(d.keys()))
if "data" in d:
    print("data keys:", list(d["data"].keys())[:10])
    for k in list(d["data"].keys())[:10]:
        print(f"  {k}: {d['data'][k]}")
