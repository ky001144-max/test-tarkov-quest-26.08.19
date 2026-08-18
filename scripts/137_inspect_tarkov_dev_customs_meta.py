import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

# Check primary_data/tarkov_dev_maps.json or maps_ko.txt
with open("map_data/tarkov dev/maps_ko.txt", "r", encoding="utf-8") as f:
    maps_ko = json.load(f)

print("=== maps_ko.txt Inspection ===")
for m in maps_ko.get("data", {}).get("maps", []):
    if m.get("normalizedName") == "customs":
        print("Customs map from tarkov dev maps_ko:")
        print(json.dumps(m, indent=2, ensure_ascii=False))
