import json
import os

# 1. Load data sources
with open("primary_data/tracker_quests_json.json", "r", encoding="utf-8") as f:
    raw_tracker_quests = json.load(f)

with open("tarkov-data-manager-main/src/tarkov-data-manager/public/data/quest-data.json", "r", encoding="utf-8") as f:
    data_manager_quests = json.load(f)

with open("primary_data/traders.json", "r", encoding="utf-8") as f:
    raw_traders = json.load(f)

# Traders
traders_dict = {
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

# Maps with official bounds & dimensions
map_configs = {
    0: {
        "id": "factory", "name_en": "Factory", "name_ko": "공장", "svg": "Factory.svg",
        "bounds": [[-67, 69], [76.6, -65.5]], "rotation": 90, "vb": [130.81831, 141.23242],
        "floors": ["Basement", "Ground_Floor", "First_Floor", "Second_Floor"]
    },
    1: {
        "id": "customs", "name_en": "Customs", "name_ko": "세관", "svg": "Customs.svg",
        "bounds": [[698, -307], [-371, 237]], "rotation": 180, "vb": [1062.4827, 535.17401],
        "floors": ["Ground_Level"]
    },
    2: {
        "id": "woods", "name_en": "Woods", "name_ko": "우드", "svg": "Woods.svg",
        "bounds": [[650, -945], [-695, 470]], "rotation": 180, "vb": [1472.7926, 1420.5995],
        "floors": ["Ground_Level"]
    },
    3: {
        "id": "shoreline", "name_en": "Shoreline", "name_ko": "쇼어라인", "svg": "Shoreline.svg",
        "bounds": [[504, -415], [-1056, 618]], "rotation": 180, "vb": [1559.5717, 1032.4935],
        "floors": ["Ground_Level", "Underground_Level", "First_Floor", "Second_Floor", "Third_Floor"]
    },
    4: {
        "id": "interchange", "name_en": "Interchange", "name_ko": "인터체인지", "svg": "Interchange.svg",
        "bounds": [[598, -442], [-433, 426]], "rotation": 180, "vb": [1127.6852, 947.02582],
        "floors": ["Garage", "Ground_Floor", "First_Floor"]
    },
    5: {
        "id": "lab", "name_en": "The Lab", "name_ko": "더 랩", "svg": "Labs.svg",
        "bounds": [[-80, -477], [-287, -193]], "rotation": 270, "vb": [720, 586],
        "floors": ["Basement", "Ground_Floor", "First_Floor", "Second_Floor"]
    },
    6: {
        "id": "reserve", "name_en": "Reserve", "name_ko": "리저브", "svg": "Reserve.svg",
        "bounds": [[289, -293], [-303, 244]], "rotation": 180, "vb": [827.28742, 761.16437],
        "floors": ["Ground_Level", "Bunkers"]
    },
    7: {
        "id": "lighthouse", "name_en": "Lighthouse", "name_ko": "등대", "svg": "Lighthouse.svg",
        "bounds": [[515, -998], [-545, 725]], "rotation": 180, "vb": [1059.3752, 1722.9499],
        "floors": ["Ground_Level"]
    },
    8: {
        "id": "streetsoftarkov", "name_en": "Streets of Tarkov", "name_ko": "타르코프 시내", "svg": "StreetsOfTarkov.svg",
        "bounds": [[323, -295], [-280, 532]], "rotation": 180, "vb": [605.32395, 831.57753],
        "floors": ["Ground_Level", "Ground_Floor", "First_Floor"]
    },
    9: {
        "id": "groundzero", "name_en": "Ground Zero", "name_ko": "그라운드 제로", "svg": "GroundZero.svg",
        "bounds": [[249, -124], [-99, 364]], "rotation": 180, "vb": [348.92543, 488.44792],
        "floors": ["Basement", "Ground_Level", "First_Floor", "Second_Floor"]
    }
}

# Accurate In-game Locations & Landmarks calibration
landmark_calibration = {
    # Customs
    "bronze pocket watch": {"map": "customs", "left": 51.86, "top": 55.71, "floor": "Ground_Level", "hint": "건설현장 탱크트럭 운전석"},
    "Secure case for documents 0022": {"map": "customs", "left": 85.91, "top": 35.65, "floor": "Ground_Level", "hint": "빅 레드 2층 타르콘 사무소"},
    "Tanker 1": {"map": "customs", "left": 24.02, "top": 56.82, "floor": "Ground_Level", "hint": "신주유소 인근 탱크트럭"},
    "Tanker 2": {"map": "customs", "left": 34.7, "top": 15.88, "floor": "Ground_Level", "hint": "검문소 인근 탱크트럭"},
    "Tanker 3": {"map": "customs", "left": 51.59, "top": 53.48, "floor": "Ground_Level", "hint": "건설현장 탱크트럭"},
    "Tanker 4": {"map": "customs", "left": 98.75, "top": 30.64, "floor": "Ground_Level", "hint": "빅 레드 주차장 탱크트럭"},
    "Secure case for documents 0031": {"map": "customs", "left": 48.48, "top": 57.66, "floor": "Ground_Level", "hint": "기숙사 인근 임시 컨테이너 숙소"},
    "Bank case": {"map": "customs", "left": 47.97, "top": 84.03, "floor": "Ground_Level", "hint": "3층 기숙사 214호"},
    "Carbon case": {"map": "customs", "left": 42.9, "top": 85.29, "floor": "Ground_Level", "hint": "2층 기숙사 114호"},
    "Docs 0048": {"map": "customs", "left": 30.32, "top": 45.38, "floor": "Ground_Level", "hint": "신골조 근처 경비실 캐빈"},
    "Gilded Zibbo lighter": {"map": "customs", "left": 48.28, "top": 84.66, "floor": "Ground_Level", "hint": "3층 기숙사 303호"},
    "Docs 0013": {"map": "customs", "left": 18.56, "top": 22.9, "floor": "Ground_Level", "hint": "기차 선로 객차 0013 내부"},
    "Sealed letter (TerraGroup)": {"map": "customs", "left": 46.25, "top": 88.03, "floor": "Ground_Level", "hint": "3층 기숙사 220호"},
    "Sliderkey Secure Flash drive": {"map": "customs", "left": 46.25, "top": 88.03, "floor": "Ground_Level", "hint": "3층 기숙사 220호"},
    "Transport van": {"map": "customs", "left": 19.68, "top": 39.29, "floor": "Ground_Level", "hint": "보일러실 뒤 밴 차량"},
    "Roadblock": {"map": "customs", "left": 63.49, "top": 74.37, "floor": "Ground_Level", "hint": "기숙사 앞 도로 바리케이드"},
    "False flash drive": {"map": "customs", "left": 73.23, "top": 56.93, "floor": "Ground_Level", "hint": "강 건너 다리 밑 숙소"},
    "The hidden water in 2-story dorms, room 206": {"map": "customs", "left": 42.8, "top": 81.3, "floor": "Ground_Level", "hint": "2층 기숙사 206호"},
    "Tigr vehicle 1": {"map": "customs", "left": 13.29, "top": 46.64, "floor": "Ground_Level", "hint": "골조 철로 티그르 장갑차"},
    "Tigr vehicle 2": {"map": "customs", "left": 17.55, "top": 49.16, "floor": "Ground_Level", "hint": "주유소 인근 티그르 장갑차"},
    "Tigr vehicle 3": {"map": "customs", "left": 64.3, "top": 57.14, "floor": "Ground_Level", "hint": "다리 건널목 티그르 장갑차"},
    "Ritual spot": {"map": "customs", "left": 47.77, "top": 91.18, "floor": "Ground_Level", "hint": "3층 기숙사 마크방 (314호)"},
    
    # Factory
    "Place Secure case for documents 0022": {"map": "factory", "left": 20.42, "top": 23.83, "floor": "First_Floor", "hint": "공장 2층 펌프실/환기구 캐빈"},
    
    # Woods
    "Scavs on Woods": {"map": "woods", "left": 50.0, "top": 50.0, "floor": "Ground_Level", "hint": "우드 벌목장(제재소) 및 전역"},
    "Shturman": {"map": "woods", "left": 48.5, "top": 58.2, "floor": "Ground_Level", "hint": "우드 제재소(벌목장) 중앙 수햔 스폰"},
    "Convoy": {"map": "woods", "left": 39.5, "top": 35.8, "floor": "Ground_Level", "hint": "우드 북쪽 USEC 호송대"},
    "USEC camp": {"map": "woods", "left": 28.3, "top": 25.4, "floor": "Ground_Level", "hint": "우드 북서쪽 USEC 캠프"},
    "Bunker 1": {"map": "woods", "left": 62.4, "top": 28.5, "floor": "Ground_Level", "hint": "우드 북동쪽 ZB-014 벙커"},
    "Bunker 2": {"map": "woods", "left": 68.2, "top": 64.1, "floor": "Ground_Level", "hint": "우드 남동쪽 ZB-016 벙커"},
}

# Translation Dict
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
    "Tigr Safari": "티그르 사파리",
    "Bullshit": "허튼소리",
    "Chumming": "미끼 작업",
    "The Cult - Part 1": "광신도 - 1부",
    "The Cult - Part 2": "광신도 - 2부",
    "Informed means armed": "정보가 곧 무기",
}

# 2. Build Unified High-Precision Quest Database
processed_quests = []

for q in raw_tracker_quests:
    q_id = q.get("id")
    title_en = q.get("title", "")
    title_ko = quest_ko_dict.get(title_en, title_en)
    
    giver_id = q.get("giver")
    trader = traders_dict.get(giver_id, {"id": "unknown", "name_en": "Unknown", "name_ko": "알 수 없음"})
    
    req_level = q.get("require", {}).get("level", 1)
    req_quests = q.get("require", {}).get("quests", [])
    
    objectives = []
    quest_maps = set()
    has_gps = False
    
    for obj in q.get("objectives", []):
        loc_id = obj.get("location", -1)
        m_cfg = map_configs.get(loc_id)
        
        target = obj.get("target", "")
        obj_type = obj.get("type", "unknown")
        number = obj.get("number", 1)
        
        gps = obj.get("gps")
        hint_text = ""

        # Check calibrated precision positions
        target_str = target if isinstance(target, str) else str(target)
        if target_str in landmark_calibration:
            calib = landmark_calibration[target_str]
            gps = {
                "leftPercent": calib["left"],
                "topPercent": calib["top"],
                "floor": calib["floor"]
            }
            hint_text = f" [{calib['hint']}]"
            has_gps = True
        elif gps:
            has_gps = True

        if m_cfg:
            quest_maps.add(m_cfg["id"])

        # Construct readable Korean description
        desc_ko = f"[{obj_type.upper()}] {target_str} ({number}개)"
        if obj_type == "pickup":
            desc_ko = f"📦 {target_str} 획득{hint_text}"
        elif obj_type == "place":
            desc_ko = f"📍 {target_str} 설치/배치{hint_text}"
        elif obj_type == "mark":
            desc_ko = f"🎯 {target_str} 마커 부착{hint_text}"
        elif obj_type == "locate" or obj_type == "find":
            desc_ko = f"🔍 {target_str} 위치 탐색{hint_text}"
        elif obj_type == "kill":
            desc_ko = f"⚔️ {target_str} 처치 ({number}명){hint_text}"
        elif obj_type == "collect":
            desc_ko = f"🎒 {target_str} 수집/전달 ({number}개)"
        elif obj_type == "key":
            desc_ko = f"🔑 {target_str} 열쇠 사용/확인{hint_text}"
        elif obj_type == "extract":
            desc_ko = f"🚪 탈출 성공"

        objectives.append({
            "id": obj.get("id"),
            "type": obj_type,
            "target": target_str,
            "number": number,
            "location_id": loc_id,
            "map_id": m_cfg["id"] if m_cfg else "any",
            "map_name_ko": m_cfg["name_ko"] if m_cfg else "전체 맵",
            "map_name_en": m_cfg["name_en"] if m_cfg else "Any Map",
            "gps": gps,
            "hint": hint_text.strip(" []"),
            "description_ko": desc_ko
        })

    processed_quests.append({
        "id": q_id,
        "title_en": title_en,
        "title_ko": title_ko,
        "trader": trader,
        "required_level": req_level,
        "required_quests": req_quests,
        "exp": q.get("exp", 0),
        "wiki": q.get("wiki", ""),
        "maps": list(quest_maps),
        "has_gps": has_gps,
        "objectives": objectives
    })

# Save new DB
os.makedirs("app/data", exist_ok=True)
os.makedirs("secondary_data", exist_ok=True)

with open("app/data/quests.json", "w", encoding="utf-8") as f:
    json.dump(processed_quests, f, indent=2, ensure_ascii=False)

with open("secondary_data/processed_quests.json", "w", encoding="utf-8") as f:
    json.dump(processed_quests, f, indent=2, ensure_ascii=False)

print(f"Successfully generated High-Precision Quest DB with {len(processed_quests)} quests.")
print("Updated app/data/quests.json and secondary_data/processed_quests.json.")
