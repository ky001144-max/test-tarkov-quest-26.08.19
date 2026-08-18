import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open("primary_data/tarkov_dev_maps.json", "r", encoding="utf-8") as f:
    maps_data = json.load(f)

# Search for quest items or quest markers inside maps_data
quest_items_in_maps = {}

for m in maps_data:
    map_norm = m.get("normalizedName")
    for sm in m.get("maps", []):
        # check loot, items, static markers
        submap_name = sm.get("name")
        print(f"Map: {map_norm} (submap: {submap_name})")
        for key in sm:
            if isinstance(sm[key], list) and len(sm[key]) > 0:
                print(f"   - {key}: {len(sm[key])} items")
                sample_item = sm[key][0]
                if isinstance(sample_item, dict) and "position" in sample_item:
                    print(f"     sample pos: {sample_item.get('position')}, name/type: {sample_item.get('name') or sample_item.get('type')}")
