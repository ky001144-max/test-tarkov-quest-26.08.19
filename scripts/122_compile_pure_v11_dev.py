import json
import sys
import os

sys.stdout.reconfigure(encoding='utf-8')

print("=== Compiling PURE v1.11 (Tarkov.dev Official Dataset) ===")

with open("map_data/tarkov dev/tasks.txt", "r", encoding="utf-8") as f:
    raw_tasks = json.load(f)

with open("map_data/tarkov dev/tasks_ko.txt", "r", encoding="utf-8") as f:
    i18n_ko = json.load(f).get("data", {})

with open("map_data/tarkov dev/tasks_en.txt", "r", encoding="utf-8") as f:
    i18n_en = json.load(f).get("data", {})

tasks_dict = raw_tasks["data"]["tasks"]

traders_map = {
    "54cb50c76803fa8b248b4571": {"id": "prapor", "name_en": "Prapor", "name_ko": "프라포르"},
    "54cb57776803fa99248b456e": {"id": "therapist", "name_en": "Therapist", "name_ko": "테라피스트"},
    "58330581ace78e27b8b10cee": {"id": "skier", "name_en": "Skier", "name_ko": "스키어"},
    "5935c25fb3acc3127c3d8cd9": {"id": "peacekeeper", "name_en": "Peacekeeper", "name_ko": "피스키퍼"},
    "5a7c2eca46aef81a7ca2145d": {"id": "mechanic", "name_en": "Mechanic", "name_ko": "메카닉"},
    "5ac3b934156ae10c4430e83c": {"id": "ragman", "name_en": "Ragman", "name_ko": "래그맨"},
    "5c0647fdd443bc2504c2d371": {"id": "jaeger", "name_en": "Jaeger", "name_ko": "예거"},
    "579dc571d53a0658a154fbec": {"id": "fence", "name_en": "Fence", "name_ko": "펜스"},
    "638f541a29ffd1183d187f57": {"id": "lightkeeper", "name_en": "Lightkeeper", "name_ko": "라이트키퍼"},
    "656f0f98d80a697f855d34b1": {"id": "btr", "name_en": "BTR Driver", "name_ko": "BTR 운전수"},
    "6617beeaa9cfa777ca915b7c": {"id": "ref", "name_en": "Ref", "name_ko": "레프"}
}

unity_map_ids = {
    "56f40101d2720b2a4d8b45d6": {"id": "customs", "name_ko": "세관", "name_en": "Customs"},
    "55f2d3fd4bdc2d5f408b4567": {"id": "factory", "name_ko": "공장", "name_en": "Factory"},
    "5704e4dad2720bb55b8b4567": {"id": "woods", "name_ko": "우드", "name_en": "Woods"},
    "5704e554d2720bac5b8b456e": {"id": "shoreline", "name_ko": "쇼어라인", "name_en": "Shoreline"},
    "5714dc692459777137212e12": {"id": "interchange", "name_ko": "인터체인지", "name_en": "Interchange"},
    "5b0fc42d86f7744a585f9105": {"id": "lab", "name_ko": "더 랩", "name_en": "The Lab"},
    "5704e3c2d2720bac5b8b4567": {"id": "reserve", "name_ko": "리저브", "name_en": "Reserve"},
    "5704e5fad2720bc05b8b4567": {"id": "lighthouse", "name_ko": "등대", "name_en": "Lighthouse"},
    "5714dbc024597771384a510d": {"id": "streetsoftarkov", "name_ko": "타르코프 시내", "name_en": "Streets of Tarkov"},
    "653e6760052c01c1c805532f": {"id": "groundzero", "name_ko": "그라운드 제로", "name_en": "Ground Zero"},
    "65b8d6f5cdde2479cb2a3125": {"id": "groundzero", "name_ko": "그라운드 제로", "name_en": "Ground Zero"}
}

v11_pure_quests = []

for q_id, q in tasks_dict.items():
    name_ko = i18n_ko.get(f"{q_id} name") or i18n_ko.get(f"{q_id} Name") or q.get("name") or "이름 없는 퀘스트"
    name_en = i18n_en.get(f"{q_id} name") or i18n_en.get(f"{q_id} Name") or q.get("name") or name_ko
    
    trader = traders_map.get(q.get("trader"), {"id": "unknown", "name_en": "Trader", "name_ko": "상인"})
    q_map_info = unity_map_ids.get(q.get("map"))
    main_map_id = q_map_info["id"] if q_map_info else "any"
    
    objectives = []
    has_pos = False
    
    for idx, obj in enumerate(q.get("objectives", [])):
        desc_key = obj.get("description", "")
        desc_ko = i18n_ko.get(desc_key) or desc_key
        desc_en = i18n_en.get(desc_key) or desc_key
        obj_type = obj.get("type", "unknown")
        
        pos = None
        hint = ""
        obj_map_id = main_map_id
        
        zones = obj.get("zones", [])
        if zones:
            for z in zones:
                if z.get("position"):
                    pos = {"x": round(z["position"]["x"], 2), "z": round(z["position"]["z"], 2)}
                    has_pos = True
                    zm = z.get("map")
                    if zm and zm in unity_map_ids:
                        obj_map_id = unity_map_ids[zm]["id"]
                    if z.get("id"):
                        hint = f"위치 ID: {z.get('id')}"
                    break
                    
        m_info = next((v for v in unity_map_ids.values() if v["id"] == obj_map_id), None)
        
        objectives.append({
            "id": idx + 1,
            "type": obj_type,
            "description_ko": desc_ko,
            "description_en": desc_en,
            "map_id": obj_map_id,
            "map_name_ko": m_info["name_ko"] if m_info else "전체 맵",
            "map_name_en": m_info["name_en"] if m_info else "Any Map",
            "position": pos,
            "hint": hint
        })
        
    v11_pure_quests.append({
        "id": q_id,
        "title_ko": name_ko,
        "title_en": name_en,
        "trader": trader,
        "map_id": main_map_id,
        "required_level": q.get("minPlayerLevel", 1),
        "experience": q.get("experience", 0),
        "wiki": q.get("wikiLink", ""),
        "has_position": has_pos,
        "objectives": objectives
    })

v11_pure_quests.sort(key=lambda x: (x["required_level"], x["trader"]["id"], x["title_ko"]))

with open("app_v11/data/quests.json", "w", encoding="utf-8") as f:
    json.dump(v11_pure_quests, f, indent=2, ensure_ascii=False)

print(f"-> Successfully compiled PURE v1.11 dataset to app_v11/data/quests.json ({len(v11_pure_quests)} quests)!")
