import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

# Inspect maps.json metadata
with open("app_v11/data/maps.json", "r", encoding="utf-8") as f:
    maps_meta = json.load(f)

print("=== maps.json Metadata Inspection ===")
for m in maps_meta:
    print(f"Map: {m['id']} ({m['name_ko']})")
    print(f"  * SVG: {m.get('svg')}")
    print(f"  * Bounds: {m.get('bounds')}")
    print(f"  * Transform: {m.get('transform')}")
    print(f"  * Rotation: {m.get('coordinateRotation')}")
