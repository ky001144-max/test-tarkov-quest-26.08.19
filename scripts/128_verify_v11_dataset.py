import json

with open("app_v11/data/quests.json", "r", encoding="utf-8") as f:
    quests = json.load(f)

pos_count = sum(1 for q in quests if q.get("has_position"))
total_obj = sum(len(q.get("objectives", [])) for q in quests)
obj_pos = sum(sum(1 for o in q.get("objectives", []) if o.get("position")) for q in quests)

print(f"=== app_v11 Validation Summary ===")
print(f"Total Quests: {len(quests)}")
print(f"Quests with 3D GPS Positions: {pos_count} / {len(quests)}")
print(f"Total Objectives: {total_obj}")
print(f"Objectives with 3D GPS Positions: {obj_pos} / {total_obj}")

# Check sample Customs quests
print("\nSample Customs Quests in app_v11:")
for q in quests:
    if q.get("map_id") == "customs" and q.get("has_position"):
        print(f"  * [{q['trader']['name_ko']}] {q['title_ko']}")
        for o in q['objectives']:
            if o.get("position"):
                print(f"     - {o['description_ko']} -> pos: {o['position']} ({o.get('hint')})")
