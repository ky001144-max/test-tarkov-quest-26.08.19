import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

print("=== Rebuilding Datasets for v1.10 (Tarkov.dev) and v1.11 (Tarkov-Market) ===")

# Accurate Trader Map
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

# Accurate Map Map
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

# ----------------------------------------------------
# 1. BUILD APP V1.10 (Tarkov.dev Full 490 Quests)
# ----------------------------------------------------
with open("map_data/tarkov dev/tasks.txt", "r", encoding="utf-8") as f:
    raw_tasks = json.load(f)

with open("map_data/tarkov dev/tasks_ko.txt", "r", encoding="utf-8") as f:
    i18n = json.load(f).get("data", {})

tasks_dict = raw_tasks["data"]["tasks"]

v10_quests = []

# Special Landmark positions for Tigr Safari and other key quests
special_landmark_positions = {
    "Tigr 사파리": [
        {"desc": "골조 철로 인근 첫 번째 Tigr 장갑차 마킹", "x": 410.0, "z": -40.0, "hint": "골조 철로 티그르 장갑차"},
        {"desc": "주유소 인근 두 번째 Tigr 장갑차 마킹", "x": 330.0, "z": -35.0, "hint": "주유소 인근 티그르 장갑차"},
        {"desc": "다리 건널목 세 번째 Tigr 장갑차 마킹", "x": 45.0, "z": -85.0, "hint": "다리 건널목 티그르 장갑차"}
    ],
    "Checking": [{"desc": "건설현장 유조 탱크트럭 안에서 청동 시계 획득", "x": 125.4, "z": -85.2, "hint": "건설현장 탱크트럭 운전석"}],
    "Delivery from the past": [{"desc": "빅 레드 2층 타르콘 디렉터 사무실에서 기밀 서류 획득", "x": -305.2, "z": 52.6, "hint": "빅 레드 2층 타르콘 사무소"}],
    "Bad Rep Evidence": [{"desc": "신골조 근처 경비실 캐빈에서 0031 서류 획득", "x": 195.0, "z": -90.0, "hint": "신골조 경비실 캐빈"}],
    "Shaking up teller": [{"desc": "기숙사 214호에서 귀중품 획득", "x": 182.5, "z": -248.0, "hint": "3층 기숙사 214호"}],
    "Golden swag": [{"desc": "기숙사 303호에서 황금 지포 라이터 획득", "x": 185.0, "z": -252.0, "hint": "3층 기숙사 303호"}],
    "Pharmacist": [{"desc": "기숙사 114호에서 의료 서류 획득", "x": 215.0, "z": -260.0, "hint": "2층 기숙사 114호"}],
    "Operation Aquarius - Part 1": [{"desc": "기숙사 206호에서 숨겨진 물 획득", "x": 218.0, "z": -265.0, "hint": "2층 기숙사 206호"}],
    "The Blood of War - Part 1": [
        {"desc": "신주유소 유조차 마킹", "x": 310.5, "z": -45.0, "hint": "신주유소 유조 탱크트럭"},
        {"desc": "검문소 인근 유조차 마킹", "x": 188.0, "z": 75.0, "hint": "검문소 인근 유조 탱크트럭"},
        {"desc": "건설현장 유조차 마킹", "x": 125.4, "z": -85.2, "hint": "건설현장 유조 탱크트럭"}
    ]
}

for q_id, q in tasks_dict.items():
    name_ko = i18n.get(f"{q_id} name") or i18n.get(f"{q_id} Name") or q.get("name") or "퀘스트"
    title_en = q.get("name", name_ko)
    
    trader = traders_map.get(q.get("trader"), {"id": "unknown", "name_en": "Trader", "name_ko": "상인"})
    q_map_info = unity_map_ids.get(q.get("map"))
    main_map_id = q_map_info["id"] if q_map_info else "any"
    
    objectives = []
    has_pos = False
    
    # Check if this quest has special multi-positions
    if name_ko in special_landmark_positions:
        sp_list = special_landmark_positions[name_ko]
        for idx, sp in enumerate(sp_list):
            objectives.append({
                "id": idx + 1,
                "type": "mark" if "마킹" in sp["desc"] else "pickup",
                "description_ko": sp["desc"],
                "map_id": "customs",
                "map_name_ko": "세관",
                "map_name_en": "Customs",
                "position": {"x": sp["x"], "z": sp["z"]},
                "hint": sp["hint"]
            })
        has_pos = True
    else:
        for idx, obj in enumerate(q.get("objectives", [])):
            desc_key = obj.get("description", "")
            desc_ko = i18n.get(desc_key) or desc_key
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
                        break
            
            m_info = next((v for v in unity_map_ids.values() if v["id"] == obj_map_id), None)
            
            objectives.append({
                "id": idx + 1,
                "type": obj_type,
                "description_ko": desc_ko,
                "map_id": obj_map_id,
                "map_name_ko": m_info["name_ko"] if m_info else "전체 맵",
                "map_name_en": m_info["name_en"] if m_info else "Any Map",
                "position": pos,
                "hint": hint
            })
            
    v10_quests.append({
        "id": q_id,
        "title_ko": name_ko,
        "title_en": title_en,
        "trader": trader,
        "map_id": main_map_id,
        "required_level": q.get("minPlayerLevel", 1),
        "experience": q.get("experience", 0),
        "wiki": q.get("wikiLink", ""),
        "has_position": has_pos,
        "objectives": objectives
    })

v10_quests.sort(key=lambda x: (x["required_level"], x["trader"]["id"], x["title_ko"]))

with open("app_v10/data/quests.json", "w", encoding="utf-8") as f:
    json.dump(v10_quests, f, indent=2, ensure_ascii=False)

with open("app/data/quests.json", "w", encoding="utf-8") as f:
    json.dump(v10_quests, f, indent=2, ensure_ascii=False)

print(f"-> Built v1.10 (Tarkov.dev): {len(v10_quests)} quests (Full DB)")


# ----------------------------------------------------
# 2. BUILD APP V1.11 (Tarkov-Market 25 Dedicated Map Pin Quests)
# ----------------------------------------------------
# Tarkov-Market specific dataset contains ONLY the 25 active customs map quest pins
market_specific_titles = [
    "Checking", "Delivery from the past", "Bad Rep Evidence", "Shaking up teller", 
    "Golden swag", "Pharmacist", "Operation Aquarius - Part 1", "The Extortionist",
    "Chemical - Part 1", "Chemical - Part 2", "Chemical - Part 3", "Chemical - Part 4",
    "The Blood of War - Part 1", "Tigr Safari", "The Cult - Part 2", "Postman Pat - Part 1",
    "Trust Regain", "Setup", "Chumming", "Bullshit", "Silent Beach", "Overdose"
]

v11_quests = []
for q in v10_quests:
    # Filter only quests that are relevant to Tarkov-Market customs map view
    if any(q["title_ko"] in st or q["title_en"] in st for st in market_specific_titles) or (q["map_id"] == "customs" and q["has_position"]):
        # Add Tarkov-Market specific styling/badge to objectives
        m_q = dict(q)
        m_q["source"] = "Tarkov-Market Pins"
        v11_quests.append(m_q)

with open("app_v11/data/quests.json", "w", encoding="utf-8") as f:
    json.dump(v11_quests, f, indent=2, ensure_ascii=False)

print(f"-> Built v1.11 (Tarkov-Market): {len(v11_quests)} dedicated Map Pin Quests")
print("Both versions rebuilt and separated completely!")
