import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open("map_data/tasks.txt", "r", encoding="utf-8") as f:
    raw = json.load(f)

tasks = raw["data"]["tasks"]
quest_items = raw["data"].get("questItems", [])

print(f"Total Tasks in tasks.txt: {len(tasks)}")
print(f"Total Quest Items in tasks.txt: {len(quest_items)}")

# Check Customs tasks
customs_tasks = [t for t in tasks if (t.get("map") and t["map"].get("normalizedName") == "customs") or any(any(m.get("normalizedName") == "customs" for m in o.get("maps", [])) for o in t.get("objectives", []))]
print(f"\nCustoms Tasks: {len(customs_tasks)}")

for t in customs_tasks[:8]:
    print(f"\n[{t.get('trader', {}).get('name')}] {t.get('name')} (id: {t.get('id')})")
    for o in t.get("objectives", []):
        print(f"  * Obj Type: {o.get('type')}, desc: '{o.get('description')}'")
        zones = o.get("zones", [])
        if zones:
            for z in zones:
                print(f"     -> Zone ID: {z.get('id')}, pos: {z.get('position')}, map: {z.get('map', {}).get('normalizedName')}")
        if o.get("questItem"):
            qi = o["questItem"]
            print(f"     -> QuestItem: {qi.get('name')} (id: {qi.get('id')})")
