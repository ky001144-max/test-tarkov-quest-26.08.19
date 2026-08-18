import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open("map_data/tasks.txt", "r", encoding="utf-8") as f:
    raw_tasks = json.load(f)

print(f"=== tasks.txt Dictionary Structure ===")
print("Keys count:", len(raw_tasks))
keys = list(raw_tasks.keys())
print("Sample keys (Task IDs):", keys[:10])

# Inspect first task value
first_id = keys[0]
first_task = raw_tasks[first_id]
print(f"\nTask ID: {first_id}")
print(f"Task Name: {first_task.get('name')}")
print(f"Trader: {first_task.get('trader')}")
print(f"Map: {first_task.get('map')}")
print(f"Min Player Level: {first_task.get('minPlayerLevel')}")
print(f"Experience: {first_task.get('experience')}")
print(f"Wiki Link: {first_task.get('wikiLink')}")
print(f"Objectives Count: {len(first_task.get('objectives', []))}")

for i, obj in enumerate(first_task.get('objectives', [])):
    print(f"  * Obj #{i+1}: Type={obj.get('type')}, desc='{obj.get('description')}'")
    print(f"    maps={obj.get('maps')}")
    print(f"    zones={obj.get('zones')}")
    print(f"    questItem={obj.get('questItem')}")
