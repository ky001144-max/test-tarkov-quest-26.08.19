import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

print("=== Inspecting 'Chemical - Part 1' in current quests.json and tasks.txt ===")

with open("app_v11/data/quests.json", "r", encoding="utf-8") as f:
    v11_quests = json.load(f)

for q in v11_quests:
    if "화학" in q.get("title_ko", "") or "Chemical" in q.get("title_en", ""):
        print(f"\nQuest: {q['title_ko']} ({q['title_en']})")
        for o in q.get("objectives", []):
            print(f"  - Obj #{o['id']} [{o.get('type')}]: {o.get('description_ko')} | Pos: {o.get('position')} | Hint: {o.get('hint')}")

print("\n--- Raw tasks.txt for Chemical Part 1 ---")
with open("map_data/tarkov dev/tasks.txt", "r", encoding="utf-8") as f:
    raw_tasks = json.load(f)["data"]["tasks"]

for q_id, q in raw_tasks.items():
    if "chemical" in q.get("name", "").lower() or "596b43eb86f77457cb5a8b29" in q_id:
        print(f"\nRaw Quest ID: {q_id}, Name: {q.get('name')}")
        for o in q.get("objectives", []):
            print(f"  - Raw Obj: {o.get('type')}, desc: {o.get('description')}, zones: {o.get('zones')}")
