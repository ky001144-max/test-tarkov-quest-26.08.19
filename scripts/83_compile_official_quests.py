import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open("map_data/tasks.txt", "r", encoding="utf-8") as f:
    raw_tasks = json.load(f)

with open("map_data/tasks_ko.txt", "r", encoding="utf-8") as f:
    i18n = json.load(f).get("data", {})

tasks_dict = raw_tasks["data"]["tasks"]

# Check traders and map IDs
traders_ids = {
    "54cb50c76803fa8b248b4571": {"id": "prapor", "name_en": "Prapor", "name_ko": "프라포르"},
    "54cb57776803fa99248b456e": {"id": "therapist", "name_en": "Therapist", "name_ko": "테라피스트"},
    "579dc13424597735691d1359": {"id": "fence", "name_en": "Fence", "name_ko": "펜스"},
    "58330581ace78e27b8b10cee": {"id": "skier", "name_en": "Skier", "name_ko": "스키어"},
    "5935c25fb3acc9143c3d64bc": {"id": "peacekeeper", "name_en": "Peacekeeper", "name_ko": "피스키퍼"},
    "5a7c2eca46aef81a7ca2145d": {"id": "mechanic", "name_en": "Mechanic", "name_ko": "메카닉"},
    "5ac3b934156ae10c40042254": {"id": "ragman", "name_en": "Ragman", "name_ko": "래그맨"},
    "5c0647fdd443bc2504c2d371": {"id": "jaeger", "name_en": "Jaeger", "name_ko": "예거"},
    "6617beeaa9cfa777ca915b7c": {"id": "ref", "name_en": "Ref", "name_ko": "레프"},
    "656f0f98d61a19d70809b0b4": {"id": "btr", "name_en": "BTR Driver", "name_ko": "BTR 운전수"}
}

map_ids = {
    "55f2d3fd4bdc2d5f408b4567": "factory",
    "5704e3c2d432043e1d43ac5c": "customs",
    "5704e4dad432043e0852d204": "woods",
    "5704e554d432043e0422f781": "shoreline",
    "5704e5fed432043e0501bc99": "interchange",
    "5b0e793b86f77429483aa01c": "lab",
    "5714dc692459777137212e12": "reserve",
    "5704e3c2d432043e1d43ac5d": "lighthouse",
    "5704e554d432043e0422f782": "streetsoftarkov",
    "653e6760052c01c1c805532f": "groundzero",
    "65b8d6f5cdde2479cb2a3125": "groundzero"
}

# Translate and build complete unified dataset
compiled_quests = []

for q_id, q in tasks_dict.items():
    # Title resolution
    raw_name_key = f"{q_id} name"
    raw_name_key_cap = f"{q_id} Name"
    name_ko = i18n.get(raw_name_key) or i18n.get(raw_name_key_cap) or q.get("name") or "이름 없는 퀘스트"
    
    # Trader resolution
    trader_info = traders_ids.get(q.get("trader"), {"id": "unknown", "name_en": "Trader", "name_ko": "상인"})
    
    # Map resolution
    map_raw = q.get("map")
    q_map_id = map_ids.get(map_raw, "any")
    
    objectives = []
    has_pos = False
    
    for idx, obj in enumerate(q.get("objectives", [])):
        obj_desc_key = obj.get("description", "")
        desc_ko = i18n.get(obj_desc_key) or obj_desc_key
        
        obj_type = obj.get("type", "unknown")
        
        # Position extraction from zones
        pos = None
        obj_map = q_map_id
        
        zones = obj.get("zones", [])
        if zones:
            for z in zones:
                if z.get("position"):
                    pos = {"x": z["position"]["x"], "z": z["position"]["z"]}
                    has_pos = True
                    zm = z.get("map")
                    if zm and zm in map_ids:
                        obj_map = map_ids[zm]
                    break
                    
        objectives.append({
            "id": idx + 1,
            "type": obj_type,
            "description_ko": desc_ko,
            "map_id": obj_map,
            "position": pos
        })
        
    compiled_quests.append({
        "id": q_id,
        "title_ko": name_ko,
        "title_en": name_ko,
        "trader": trader_info,
        "map_id": q_map_id,
        "required_level": q.get("minPlayerLevel", 1),
        "experience": q.get("experience", 0),
        "wiki": q.get("wikiLink", ""),
        "has_position": has_pos,
        "objectives": objectives
    })

print(f"Compiled {len(compiled_quests)} official quests!")
quests_with_pos = [q for q in compiled_quests if q["has_position"]]
print(f"Quests with real 3D In-game Positions: {len(quests_with_pos)}")

# Check Customs sample
customs_sample = [q for q in quests_with_pos if any(o["map_id"] == "customs" for o in q["objectives"])]
print(f"Customs Quests with 3D positions: {len(customs_sample)}")
for q in customs_sample[:6]:
    print(f"\n[{q['trader']['name_ko']}] {q['title_ko']}")
    for o in q['objectives']:
        if o.get("position"):
            print(f"   * {o['description_ko']} -> pos: {o['position']}")
