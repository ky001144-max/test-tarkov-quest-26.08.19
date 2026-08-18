import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open("app_v11/data/quests.json", "r", encoding="utf-8") as f:
    quests = json.load(f)

# Group missing position quests by Map
missing_by_map = {}

for q in quests:
    m = q.get("map_id", "any")
    for o in q.get("objectives", []):
        if not o.get("position") and o.get("type") in ["pickup", "plantItem", "plantQuestItem", "mark", "visit", "findQuestItem", "findItem", "useItem"]:
            obj_m = o.get("map_id", m)
            if obj_m not in missing_by_map:
                missing_by_map[obj_m] = []
            missing_by_map[obj_m].append({
                "quest_id": q["id"],
                "quest_title_ko": q["title_ko"],
                "quest_title_en": q["title_en"],
                "trader": q["trader"]["name_ko"],
                "obj_id": o["id"],
                "obj_type": o["type"],
                "desc_ko": o["description_ko"]
            })

print("=== Objectives with Missing Coordinates by Map ===")
for m_id, obj_list in sorted(missing_by_map.items(), key=lambda x: len(x[1]), reverse=True):
    print(f"\n[Map: {m_id.upper()}] - {len(obj_list)} objectives missing coordinates:")
    for item in obj_list[:8]:
        print(f"  * [{item['trader']}] {item['quest_title_ko']} (obj #{item['obj_id']}): {item['desc_ko']} [Type: {item['obj_type']}]")
