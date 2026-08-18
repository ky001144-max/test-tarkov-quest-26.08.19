import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open("map_data/tasks.txt", "r", encoding="utf-8") as f:
    raw = json.load(f)

tasks_dict = raw["data"]["tasks"]
print("Type of tasks_dict:", type(tasks_dict))

if isinstance(tasks_dict, dict):
    print("Total tasks:", len(tasks_dict))
    for q_id, q in list(tasks_dict.items())[:5]:
        print(f"\nTask ID: {q_id}")
        print(f"  Name: {q.get('name')}")
        print(f"  Trader: {q.get('trader')}")
        print(f"  Map: {q.get('map')}")
        print(f"  Objectives: {len(q.get('objectives', []))}")
        for o in q.get('objectives', []):
            print(f"    - Type: {o.get('type')}, desc: '{o.get('description')}', zones: {len(o.get('zones', []))}")
            for z in o.get('zones', []):
                print(f"       zone: {z.get('id')}, pos: {z.get('position')}, map: {z.get('map')}")
