import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

print("=== Inspecting Customs lootLoose in maps.txt ===")
with open("map_data/tarkov dev/maps.txt", "r", encoding="utf-8") as f:
    maps_raw = json.load(f)

customs = maps_raw["data"]["maps"]["56f40101d2720b2a4d8b45d6"]
loot_loose = customs.get("lootLoose", [])

print(f"Total lootLoose spawn points in Customs: {len(loot_loose)}")
if loot_loose:
    print("Sample lootLoose item:", json.dumps(loot_loose[0], indent=2, ensure_ascii=False))

# Check items.txt for quest item definitions
with open("map_data/tarkov dev/items.txt", "r", encoding="utf-8") as f:
    items_raw = json.load(f)

items_dict = items_raw.get("data", {}).get("items", {})
print(f"\nTotal items in items.txt: {len(items_dict)}")
if isinstance(items_dict, dict):
    for k, it in list(items_dict.items())[:5]:
        print(f"  * {k}: {it.get('name')} [{it.get('types')}]")
