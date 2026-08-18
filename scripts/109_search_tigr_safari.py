import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open("map_data/tarkov dev/tasks.txt", "r", encoding="utf-8") as f:
    raw_tasks = json.load(f)

with open("map_data/tarkov dev/tasks_ko.txt", "r", encoding="utf-8") as f:
    i18n = json.load(f).get("data", {})

tasks_dict = raw_tasks["data"]["tasks"]

print("=== Searching for 'Tigr Safari' in tarkov dev tasks.txt ===")
for q_id, q in tasks_dict.items():
    name_ko = i18n.get(f"{q_id} name") or i18n.get(f"{q_id} Name") or q.get("name")
    wiki_link = q.get("wikiLink", "")
    if "tigr" in str(name_ko).lower() or "tigr" in wiki_link.lower() or "사파리" in str(name_ko):
        print(f"\nFound Quest ID: {q_id}")
        print(f"  Title KO: {name_ko}")
        print(f"  Trader: {q.get('trader')}")
        print(f"  Map: {q.get('map')}")
        print(f"  Wiki Link: {wiki_link}")
        print(f"  Objectives ({len(q.get('objectives', []))}):")
        for o in q.get('objectives', []):
            desc = i18n.get(o.get('description')) or o.get('description')
            print(f"    - Type: {o.get('type')}, Desc: {desc}")
            print(f"      Maps: {o.get('maps')}")
            print(f"      Zones: {o.get('zones')}")
