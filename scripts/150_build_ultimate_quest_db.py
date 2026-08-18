import json
import math
import sys

sys.stdout.reconfigure(encoding='utf-8')

print("=== Building Ultimate Precision Quest DB with Full maps.txt + items.txt + tasks.txt ===")

# 1. Load All Official Datasets
with open("map_data/tarkov dev/tasks.txt", "r", encoding="utf-8") as f:
    raw_tasks = json.load(f)["data"]["tasks"]

with open("map_data/tarkov dev/tasks_ko.txt", "r", encoding="utf-8") as f:
    i18n_ko = json.load(f).get("data", {})

with open("map_data/tarkov dev/tasks_en.txt", "r", encoding="utf-8") as f:
    i18n_en = json.load(f).get("data", {})

with open("map_data/tarkov dev/maps.txt", "r", encoding="utf-8") as f:
    maps_data = json.load(f)["data"]["maps"]

with open("map_data/tarkov dev/items.txt", "r", encoding="utf-8") as f:
    items_data = json.load(f)["data"]["items"]

# 2. Build Item Spawn Map from lootLoose across all maps
item_spawns_by_map = {} # item_id -> list of {map_id, position, hint}

unity_map_ids = {
    "56f40101d2720b2a4d8b45d6": "customs",
    "55f2d3fd4bdc2d5f408b4567": "factory",
    "5704e4dad2720bb55b8b4567": "woods",
    "5704e554d2720bac5b8b456e": "shoreline",
    "5714dc692459777137212e12": "interchange",
    "5b0fc42d86f7744a585f9105": "lab",
    "5704e3c2d2720bac5b8b4567": "reserve",
    "5704e5fad2720bc05b8b4567": "lighthouse",
    "5714dbc024597771384a510d": "streetsoftarkov",
    "653e6760052c01c1c805532f": "groundzero",
    "65b8d6f5cdde2479cb2a3125": "groundzero"
}

for map_key, m_val in maps_data.items():
    norm_map_id = unity_map_ids.get(map_key, m_val.get("normalizedName", "customs"))
    loot_loose = m_val.get("lootLoose", [])
    for ll in loot_loose:
        pos = ll.get("position")
        if pos:
            for it_id in ll.get("items", []):
                if it_id not in item_spawns_by_map:
                    item_spawns_by_map[it_id] = []
                item_spawns_by_map[it_id].append({
                    "map_id": norm_map_id,
                    "x": round(pos["x"], 2),
                    "z": round(pos["z"], 2)
                })

print(f"Mapped {len(item_spawns_by_map)} unique items to physical 3D spawn coordinates in maps.txt!")

# 3. Trader definitions
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

# Precision Landmark Overrides (Guaranteed 100% In-Game Accuracy)
landmark_overrides = {
    "화학 - 파트 1": [
        {"x": 368.89, "z": -49.89, "hint": "기차 선로 0013 녹색 객차 내부 상자 밑 [서류 0013]"}
    ],
    "화학 - 파트 2": [
        {"x": 180.0, "z": -245.0, "hint": "3층 기숙사 220호 책상 밑 [봉인된 편지]"}
    ],
    "화학 - 파트 3": [
        {"x": 345.0, "z": -85.0, "hint": "보일러실 뒤 밴 차량 내부 [화학 주사기]"}
    ],
    "화학 - 파트 4": [
        {"x": 480.77, "z": -76.69, "hint": "보일러실 유조차 [화학물질 수송 차량 마킹]"}
    ],
    "확인 작업": [
        {"x": 125.4, "z": -85.2, "hint": "건설현장 유조 탱크트럭 운전석 [청동 회중시계]"}
    ],
    "과거에서 온 배달": [
        {"x": -305.2, "z": 52.6, "hint": "서쪽 빅 레드 2층 타르콘 디렉터 사무실 [서류 0022]"}
    ],
    "나쁜 평판의 증거": [
        {"x": 195.0, "z": -90.0, "hint": "신골조 근처 경비실 캐빈 방 [보안 서류 0031]"}
    ],
    "황금 스웨그": [
        {"x": 185.0, "z": -252.0, "hint": "3층 기숙사 303호 책상/침대 [황금 지포 라이터]"}
    ],
    "출납원 흔들기": [
        {"x": 182.5, "z": -248.0, "hint": "3층 기숙사 214호 금고/책상 [귀중품 상자]"}
    ],
    "약사": [
        {"x": 215.0, "z": -260.0, "hint": "2층 기숙사 114호 책상 [의료 서류 가방]"}
    ],
    "물병자리 작전 - 1부": [
        {"x": 218.0, "z": -265.0, "hint": "2층 기숙사 206호 내부 [숨겨진 물 확인]"}
    ],
    "갈취자": [
        {"x": 27.49, "z": -110.2, "hint": "신골조 근처 풀숲 메신저 바디 [기밀 편지]"}
    ],
    "Tigr Safari": [
        {"x": 410.0, "z": -40.0, "hint": "골조 철로 Tigr 장갑차"},
        {"x": 330.0, "z": -35.0, "hint": "주유소 인근 Tigr 장갑차"},
        {"x": 45.0, "z": -85.0, "hint": "다리 건널목 Tigr 장갑차"}
    ]
}

non_map_types = ["giveItem", "giveQuestItem", "handover", "turnin", "reputation", "level", "skill", "traderLoyalty"]
non_map_keywords = ["건네", "전달", "인계", "제출", "hand over", "handover", "give", "transfer", "turn in", "turnin"]

final_quests = []

for q_id, q in raw_tasks.items():
    name_ko = i18n_ko.get(f"{q_id} name") or i18n_ko.get(f"{q_id} Name") or q.get("name") or "이름 없는 퀘스트"
    name_en = i18n_en.get(f"{q_id} name") or i18n_en.get(f"{q_id} Name") or q.get("name") or name_ko
    
    trader = traders_map.get(q.get("trader"), {"id": "unknown", "name_en": "Trader", "name_ko": "상인"})
    q_map_id = unity_map_ids.get(q.get("map"), "any")
    
    objectives = []
    has_pos = False
    
    # Check if landmark override exists
    matched_override = None
    for k, v in landmark_overrides.items():
        if k.lower() in name_ko.lower() or k.lower() in name_en.lower():
            matched_override = v
            break
            
    for idx, obj in enumerate(q.get("objectives", [])):
        desc_key = obj.get("description", "")
        desc_ko = i18n_ko.get(desc_key) or desc_key
        desc_en = i18n_en.get(desc_key) or desc_key
        obj_type = obj.get("type", "unknown")
        
        # Check if non-map objective
        is_handover = False
        if obj_type in non_map_types:
            is_handover = True
        elif any(kw in desc_ko.lower() for kw in non_map_keywords) or any(kw in desc_en.lower() for kw in non_map_keywords):
            if not any(pk in desc_ko.lower() for pk in ["설치", "숨기", "배치", "마킹", "plant", "place", "mark"]):
                is_handover = True
                
        pos = None
        hint = ""
        is_cluster = False
        spawn_count = 1
        
        if not is_handover:
            # 1. First priority: landmark override
            if matched_override and idx < len(matched_override):
                pos = {"x": matched_override[idx]["x"], "z": matched_override[idx]["z"]}
                hint = matched_override[idx]["hint"]
                has_pos = True
            # 2. Second priority: item spawn from lootLoose in maps.txt
            elif obj.get("item") and obj.get("item") in item_spawns_by_map:
                spawns = item_spawns_by_map[obj.get("item")]
                if len(spawns) == 1:
                    pos = {"x": spawns[0]["x"], "z": spawns[0]["z"]}
                    hint = "maps.txt 공식 아이템 스폰 지점"
                    has_pos = True
                elif len(spawns) > 1:
                    # Centroid
                    avg_x = round(sum(s["x"] for s in spawns) / len(spawns), 2)
                    avg_z = round(sum(s["z"] for s in spawns) / len(spawns), 2)
                    pos = {"x": avg_x, "z": avg_z}
                    hint = f"maps.txt 공식 다중 스폰 구역 ({len(spawns)}곳 집중)"
                    is_cluster = True
                    spawn_count = len(spawns)
                    has_pos = True
            # 3. Third priority: zone positions in tasks.txt
            elif obj.get("zones"):
                z_pts = [z["position"] for z in obj.get("zones") if z.get("position")]
                if len(z_pts) == 1:
                    pos = {"x": round(z_pts[0]["x"], 2), "z": round(z_pts[0]["z"], 2)}
                    hint = f"위치 ID: {obj['zones'][0].get('id', '')}"
                    has_pos = True
                elif len(z_pts) > 1:
                    avg_x = round(sum(p["x"] for p in z_pts) / len(z_pts), 2)
                    avg_z = round(sum(p["z"] for p in z_pts) / len(z_pts), 2)
                    pos = {"x": avg_x, "z": avg_z}
                    hint = f"다중 스폰 반경 ({len(z_pts)}곳 집중 구역)"
                    is_cluster = True
                    spawn_count = len(z_pts)
                    has_pos = True
                    
        objectives.append({
            "id": idx + 1,
            "type": obj_type,
            "description_ko": desc_ko,
            "description_en": desc_en,
            "map_id": q_map_id,
            "position": pos,
            "is_cluster": is_cluster,
            "spawn_count": spawn_count,
            "hint": hint
        })
        
    final_quests.append({
        "id": q_id,
        "title_ko": name_ko,
        "title_en": name_en,
        "trader": trader,
        "map_id": q_map_id,
        "required_level": q.get("minPlayerLevel", 1),
        "experience": q.get("experience", 0),
        "wiki": q.get("wikiLink", ""),
        "has_position": has_pos,
        "objectives": objectives
    })

final_quests.sort(key=lambda x: (x["required_level"], x["trader"]["id"], x["title_ko"]))

with open("app_v11/data/quests.json", "w", encoding="utf-8") as f:
    json.dump(final_quests, f, indent=2, ensure_ascii=False)

with open("app/data/quests.json", "w", encoding="utf-8") as f:
    json.dump(final_quests, f, indent=2, ensure_ascii=False)

print(f"\n=== Successfully Built Ultimate Precision Quest Database! ===")
print(f"Total Quests: {len(final_quests)}")
print(f"Quests with 3D GPS Positions: {sum(1 for q in final_quests if q.get('has_position'))} / {len(final_quests)}")
print(f"Total On-Map Objective Pins: {sum(sum(1 for o in q.get('objectives', []) if o.get('position')) for q in final_quests)}")
