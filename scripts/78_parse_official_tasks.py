import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open("map_data/tasks.txt", "r", encoding="utf-8") as f:
    raw_tasks = json.load(f)

with open("map_data/tasks_ko.txt", "r", encoding="utf-8") as f:
    i18n_ko = json.load(f).get("data", {})

print(f"=== tasks.txt Parse Inspection ===")
print("Type of tasks.txt:", type(raw_tasks))

tasks_list = []
if isinstance(raw_tasks, dict):
    if "data" in raw_tasks and "tasks" in raw_tasks["data"]:
        tasks_list = raw_tasks["data"]["tasks"]
    elif "tasks" in raw_tasks:
        tasks_list = raw_tasks["tasks"]
    elif "data" in raw_tasks:
        tasks_list = raw_tasks["data"]
elif isinstance(raw_tasks, list):
    tasks_list = raw_tasks

print(f"Total Quests parsed: {len(tasks_list)}")

if len(tasks_list) > 0:
    sample = tasks_list[0]
    print("\nSample Task Keys:", list(sample.keys()))
    print(f"Sample Task: [{sample.get('trader', {}).get('name')}] {sample.get('name')} (id: {sample.get('id')})")
    print(f"Objectives count: {len(sample.get('objectives', []))}")
    for o in sample.get('objectives', []):
        print(f"  * Type: {o.get('type')}, desc: {o.get('description')}")
        if o.get("zones"):
            print(f"    - Zones: {len(o.get('zones'))} -> {o.get('zones')[:2]}")
        if o.get("items"):
            print(f"    - Items: {len(o.get('items'))}")
            
# Check total objectives with positions across all tasks
total_zones_count = 0
total_tasks_with_zones = 0
map_distribution = {}

for t in tasks_list:
    has_zone = False
    for obj in t.get("objectives", []):
        zones = obj.get("zones", [])
        if zones:
            for z in zones:
                if z.get("position"):
                    total_zones_count += 1
                    has_zone = True
                    zm = z.get("map", {}).get("name", "Unknown Map")
                    map_distribution[zm] = map_distribution.get(zm, 0) + 1
    if has_zone:
        total_tasks_with_zones += 1

print(f"\nTotal 3D Objective Positions found: {total_zones_count}")
print(f"Total Tasks with 3D Positions: {total_tasks_with_zones} / {len(tasks_list)}")
print("\n3D Objective Positions by Map:")
for mname, count in sorted(map_distribution.items(), key=lambda x: x[1], reverse=True):
    print(f"  * {mname:25s}: {count} targets")
