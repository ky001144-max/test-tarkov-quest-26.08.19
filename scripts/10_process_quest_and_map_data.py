import json
import os

# 1. Load raw datasets
with open("primary_data/tracker_quests_json.json", "r", encoding="utf-8") as f:
    raw_quests = json.load(f)

with open("primary_data/tracker_maps_json.json", "r", encoding="utf-8") as f:
    raw_maps = json.load(f)

with open("primary_data/traders.json", "r", encoding="utf-8") as f:
    raw_traders = json.load(f)

# Trader Info
trader_info = {
    0: {"id": "prapor", "name_en": "Prapor", "name_ko": "프라포르"},
    1: {"id": "therapist", "name_en": "Therapist", "name_ko": "테라피스트"},
    2: {"id": "skier", "name_en": "Skier", "name_ko": "스키어"},
    3: {"id": "peacekeeper", "name_en": "Peacekeeper", "name_ko": "피스키퍼"},
    4: {"id": "mechanic", "name_en": "Mechanic", "name_ko": "메카닉"},
    5: {"id": "ragman", "name_en": "Ragman", "name_ko": "래그맨"},
    6: {"id": "jaeger", "name_en": "Jaeger", "name_ko": "예거"},
    7: {"id": "fence", "name_en": "Fence", "name_ko": "펜스"},
    8: {"id": "ref", "name_en": "Ref", "name_ko": "레프"},
    9: {"id": "btr", "name_en": "BTR Driver", "name_ko": "BTR 운전수"}
}

# Map Mapping: ID -> Metadata
map_meta = {
    0: {"id": "factory", "name_en": "Factory", "name_ko": "공장", "svg": "Factory.svg", "floors": ["Basement", "Ground_Floor", "First_Floor", "Second_Floor"]},
    1: {"id": "customs", "name_en": "Customs", "name_ko": "세관", "svg": "Customs.svg", "floors": ["Ground_Level"]},
    2: {"id": "woods", "name_en": "Woods", "name_ko": "우드", "svg": "Woods.svg", "floors": ["Ground_Level"]},
    3: {"id": "shoreline", "name_en": "Shoreline", "name_ko": "쇼어라인", "svg": "Shoreline.svg", "floors": ["Ground_Level", "Underground_Level", "First_Floor", "Second_Floor", "Third_Floor"]},
    4: {"id": "interchange", "name_en": "Interchange", "name_ko": "인터체인지", "svg": "Interchange.svg", "floors": ["Garage", "Ground_Floor", "First_Floor"]},
    5: {"id": "lab", "name_en": "The Lab", "name_ko": "더 랩", "svg": "Labs.svg", "floors": ["Basement", "Ground_Floor", "First_Floor", "Second_Floor"]},
    6: {"id": "reserve", "name_en": "Reserve", "name_ko": "리저브", "svg": "Reserve.svg", "floors": ["Ground_Level", "Bunkers"]},
    7: {"id": "lighthouse", "name_en": "Lighthouse", "name_ko": "등대", "svg": "Lighthouse.svg", "floors": ["Ground_Level"]},
    8: {"id": "streetsoftarkov", "name_en": "Streets of Tarkov", "name_ko": "타르코프 시내", "svg": "StreetsOfTarkov.svg", "floors": ["Ground_Level", "Ground_Floor", "First_Floor"]},
    9: {"id": "groundzero", "name_en": "Ground Zero", "name_ko": "그라운드 제로", "svg": "GroundZero.svg", "floors": ["Basement", "Ground_Level", "First_Floor", "Second_Floor"]}
}

# Korean quest title translation dictionary
quest_ko_dict = {
    "Debut": "데뷔",
    "Checking": "확인 작업",
    "Shootout picnic": "사격 소풍",
    "Delivery from the past": "과거로부터 온 배달",
    "BP depot": "BP 보급소",
    "Bad rep evidence": "오명에 대한 증거",
    "Ice cream cones": "아이스크림 콘",
    "Postman Pat - Part 1": "우체부 패트 - 1부",
    "Postman Pat - Part 2": "우체부 패트 - 2부",
    "Shaking up Teller": "출납원 털기",
    "Shaking up teller": "출납원 털기",
    "The Punisher - Part 1": "처벌자 - 1부",
    "The Punisher - Part 2": "처벌자 - 2부",
    "The Punisher - Part 3": "처벌자 - 3부",
    "The Punisher - Part 4": "처벌자 - 4부",
    "The Punisher - Part 5": "처벌자 - 5부",
    "The Punisher - Part 6": "처벌자 - 6부",
    "Polikhim hobo": "폴리킴의 부랑자",
    "Grenadier": "척탄병",
    "Perfect mediator": "완벽한 중재자",
    "Insomnia": "불면증",
    "Test drive - Part 1": "시승 - 1부",
    "Test drive - Part 2": "시승 - 2부",
    "Operation Aquarius - Part 1": "물병자리 작전 - 1부",
    "Operation Aquarius - Part 2": "물병자리 작전 - 2부",
    "Shortage": "부족",
    "Sanitary Standards - Part 1": "위생 기준 - 1부",
    "Sanitary Standards - Part 2": "위생 기준 - 2부",
    "Painkiller": "진통제",
    "Pharmacist": "약사",
    "Supply plans": "보급 계획",
    "General wares": "일반 잡화",
    "Carpentry": "목공",
    "Sales Night": "세일의 밤",
    "Big sale": "대규모 세일",
    "Database - Part 1": "데이터베이스 - 1부",
    "Database - Part 2": "데이터베이스 - 2부",
    "Seaside Vacation": "해변 휴가",
    "Lost Contact": "연락 두절",
    "Farming - Part 1": "파밍 - 1부",
    "Farming - Part 2": "파밍 - 2부",
    "Farming - Part 3": "파밍 - 3부",
    "Farming - Part 4": "파밍 - 4부",
    "Gunsmith - Part 1": "총기 제작자 - 1부",
    "Gunsmith - Part 2": "총기 제작자 - 2부",
    "Gunsmith - Part 3": "총기 제작자 - 3부",
    "Gunsmith - Part 4": "총기 제작자 - 4부",
    "Gunsmith - Part 5": "총기 제작자 - 5부",
    "Gunsmith - Part 6": "총기 제작자 - 6부",
    "Gunsmith - Part 7": "총기 제작자 - 7부",
    "Gunsmith - Part 8": "총기 제작자 - 8부",
    "Gunsmith - Part 9": "총기 제작자 - 9부",
    "Gunsmith - Part 10": "총기 제작자 - 10부",
    "Signal - Part 1": "신호 - 1부",
    "Signal - Part 2": "신호 - 2부",
    "Signal - Part 3": "신호 - 3부",
    "Signal - Part 4": "신호 - 4부",
    "Scout": "정찰",
    "The survivalist path - Unprotected but dangerous": "생존주의자의 길 - 무방비하지만 위험한",
    "The survivalist path - Thrifty": "생존주의자의 길 - 검소함",
    "The survivalist path - Zhivchik": "생존주의자의 길 - 지브칙",
    "The survivalist path - Wounded beast": "생존주의자의 길 - 상처 입은 야수",
    "The survivalist path - Tough guy": "생존주의자의 길 - 터프가이",
    "The Tarkov shooter - Part 1": "타르코프 사수 - 1부",
    "The Tarkov shooter - Part 2": "타르코프 사수 - 2부",
    "The Tarkov shooter - Part 3": "타르코프 사수 - 3부",
    "The Tarkov shooter - Part 4": "타르코프 사수 - 4부",
    "The Tarkov shooter - Part 5": "타르코프 사수 - 5부",
    "The Tarkov shooter - Part 6": "타르코프 사수 - 6부",
    "The Tarkov shooter - Part 7": "타르코프 사수 - 7부",
    "The Tarkov shooter - Part 8": "타르코프 사수 - 8부",
    "First in Line": "첫 번째 순서",
    "Shooting Cans": "깡통 사격",
    "Saving the Mole": "두더지 구출 작전",
    "Luxurious Life": "호화로운 삶",
    "Burning Rubber": "타는 고무 냄새",
    "The Extortionist": "갈취자",
    "Golden swag": "황금 목걸이",
    "Chemical - Part 1": "케미컬 - 1부",
    "Chemical - Part 2": "케미컬 - 2부",
    "Chemical - Part 3": "케미컬 - 3부",
    "Chemical - Part 4": "케미컬 - 4부",
    "Vitamins - Part 1": "비타민 - 1부",
    "Vitamins - Part 2": "비타민 - 2부",
}

# 2. Process Quests with precise map-to-objective indexing
processed_quests = []
for q in raw_quests:
    q_id = q.get("id")
    title_en = q.get("title", "")
    title_ko = quest_ko_dict.get(title_en, title_en)
    
    giver_id = q.get("giver")
    trader = trader_info.get(giver_id, {"id": "unknown", "name_en": "Unknown", "name_ko": "알 수 없음"})
    
    req_level = q.get("require", {}).get("level", 1)
    req_quests = q.get("require", {}).get("quests", [])
    
    objectives = []
    quest_maps = set()
    has_gps = False
    
    for obj in q.get("objectives", []):
        loc_id = obj.get("location", -1)
        m_info = map_meta.get(loc_id)
        
        gps = obj.get("gps")
        if gps:
            has_gps = True
            
        if m_info:
            quest_maps.add(m_info["id"])
            
        obj_type = obj.get("type", "unknown")
        target = obj.get("target", "")
        number = obj.get("number", 1)
        
        # Build Korean description
        desc_ko = f"[{obj_type.upper()}] {target} ({number}개)"
        if obj_type == "pickup":
            desc_ko = f"📦 {target} 획득"
        elif obj_type == "place":
            desc_ko = f"📍 {target} 설치/배치"
        elif obj_type == "mark":
            desc_ko = f"🎯 {target} 마커 설치"
        elif obj_type == "locate" or obj_type == "find":
            desc_ko = f"🔍 {target} 위치 탐색/발견"
        elif obj_type == "kill":
            desc_ko = f"⚔️ {target} 처치 ({number}명)"
        elif obj_type == "collect":
            desc_ko = f"🎒 {target} 수집/전달 ({number}개)"
        elif obj_type == "key":
            desc_ko = f"🔑 {target} 열쇠 사용/확인"
        elif obj_type == "extract":
            desc_ko = f"🚪 탈출 성공"

        objectives.append({
            "id": obj.get("id"),
            "type": obj_type,
            "target": target,
            "number": number,
            "location_id": loc_id,
            "map_id": m_info["id"] if m_info else ("any" if loc_id == -1 else f"map_{loc_id}"),
            "map_name_ko": m_info["name_ko"] if m_info else ("전체 맵" if loc_id == -1 else "기타"),
            "map_name_en": m_info["name_en"] if m_info else ("Any Map" if loc_id == -1 else "Other"),
            "gps": gps,
            "description_ko": desc_ko
        })

    maps_list = list(quest_maps)
    
    processed_quests.append({
        "id": q_id,
        "title_en": title_en,
        "title_ko": title_ko,
        "trader": trader,
        "required_level": req_level,
        "required_quests": req_quests,
        "exp": q.get("exp", 0),
        "wiki": q.get("wiki", ""),
        "maps": maps_list,
        "has_gps": has_gps,
        "objectives": objectives
    })

# Save datasets
os.makedirs("secondary_data", exist_ok=True)
os.makedirs("app/data", exist_ok=True)

with open("secondary_data/processed_quests.json", "w", encoding="utf-8") as f:
    json.dump(processed_quests, f, indent=2, ensure_ascii=False)

with open("secondary_data/processed_maps.json", "w", encoding="utf-8") as f:
    json.dump(list(map_meta.values()), f, indent=2, ensure_ascii=False)

with open("app/data/quests.json", "w", encoding="utf-8") as f:
    json.dump(processed_quests, f, indent=2, ensure_ascii=False)

with open("app/data/maps.json", "w", encoding="utf-8") as f:
    json.dump(list(map_meta.values()), f, indent=2, ensure_ascii=False)

print(f"Reprocessed {len(processed_quests)} quests.")
print("Updated secondary_data and app/data successfully.")
