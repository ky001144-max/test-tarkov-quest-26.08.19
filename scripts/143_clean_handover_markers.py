import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

print("=== Analyzing Objectives for 'Handover / Give / Turn-in' False Markers ===")

with open("app_v11/data/quests.json", "r", encoding="utf-8") as f:
    quests = json.load(f)

# Non-map objective types & keywords
non_map_types = ["giveItem", "giveQuestItem", "handover", "turnin", "reputation", "level", "skill", "traderLoyalty"]
non_map_keywords = ["건네", "전달", "인계", "제출", "hand over", "handover", "give", "transfer", "turn in", "turnin", "기증"]

false_marker_count = 0

for q in quests:
    for o in q.get("objectives", []):
        o_type = o.get("type", "")
        desc_ko = o.get("description_ko", "").lower()
        desc_en = o.get("description_en", "").lower()
        
        is_handover = False
        if o_type in non_map_types:
            is_handover = True
        elif any(kw in desc_ko for kw in non_map_keywords) or any(kw in desc_en for kw in non_map_keywords):
            # Exception: if it's a plant/place objective (e.g. 설치하기, 숨기기) it is on-map
            if not any(pk in desc_ko for pk in ["설치", "숨기", "배치", "마킹", "plant", "place", "mark"]):
                is_handover = True
                
        if is_handover and o.get("position"):
            false_marker_count += 1
            print(f"Found False Marker: [{q['title_ko']}] Obj: {o['description_ko']} (Type: {o_type}, Pos: {o['position']})")
            o["position"] = None
            o["hint"] = ""
            o["has_position"] = False

# Re-evaluate has_position for all quests
for q in quests:
    q["has_position"] = any(bool(o.get("position")) for o in q.get("objectives", []))

with open("app_v11/data/quests.json", "w", encoding="utf-8") as f:
    json.dump(quests, f, indent=2, ensure_ascii=False)

with open("app/data/quests.json", "w", encoding="utf-8") as f:
    json.dump(quests, f, indent=2, ensure_ascii=False)

print(f"\n=== Cleanup Results ===")
print(f"Removed False 'Handover/Turn-in' Markers: {false_marker_count} objectives")
print(f"Total Clean Active Map Quests: {sum(1 for q in quests if q.get('has_position'))}")
print(f"Total Valid On-Map Objectives: {sum(sum(1 for o in q.get('objectives', []) if o.get('position')) for q in quests)}")
