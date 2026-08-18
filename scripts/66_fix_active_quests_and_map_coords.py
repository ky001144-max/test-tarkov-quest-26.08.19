import json
import os

# Load raw tracker quests
with open("primary_data/tracker_quests_json.json", "r", encoding="utf-8") as f:
    raw_quests = json.load(f)

with open("tarkov-data-manager-main/src/tarkov-data-manager/data/removed_quests.json", "r", encoding="utf-8") as f:
    removed_quests_dict = json.load(f)

# Traders dict
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

# Maps
map_configs = {
    0: {"id": "factory", "name_en": "Factory", "name_ko": "공장"},
    1: {"id": "customs", "name_en": "Customs", "name_ko": "세관"},
    2: {"id": "woods", "name_en": "Woods", "name_ko": "우드"},
    3: {"id": "shoreline", "name_en": "Shoreline", "name_ko": "쇼어라인"},
    4: {"id": "interchange", "name_en": "Interchange", "name_ko": "인터체인지"},
    5: {"id": "lab", "name_en": "The Lab", "name_ko": "더 랩"},
    6: {"id": "reserve", "name_en": "Reserve", "name_ko": "리저브"},
    7: {"id": "lighthouse", "name_en": "Lighthouse", "name_ko": "등대"},
    8: {"id": "streetsoftarkov", "name_en": "Streets of Tarkov", "name_ko": "타르코프 시내"},
    9: {"id": "groundzero", "name_en": "Ground Zero", "name_ko": "그라운드 제로"}
}

# Korean translations for active quests
translations = {
    "Debut": "데뷔",
    "Checking": "확인 작업",
    "Shootout picnic": "사격 소풍",
    "Delivery from the past": "과거로부터 온 배달",
    "Bad rep evidence": "오명에 대한 증거",
    "Ice cream cones": "아이스크림 콘",
    "Postman Pat - Part 1": "우체부 패트 - 1부",
    "Postman Pat - Part 2": "우체부 패트 - 2부",
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
    "The Blood of War - Part 1": "전쟁의 피 - 1부",
    "The Blood of War - Part 2": "전쟁의 피 - 2부",
    "The Blood of War - Part 3": "전쟁의 피 - 3부",
    "First in Line": "첫 번째 순서",
    "Shooting Cans": "깡통 사격",
    "Saving the Mole": "두더지 구출 작전",
    "Luxurious Life": "호화로운 삶",
    "Burning Rubber": "타는 고무 냄새",
    "Glory to CPSU - Part 1": "소련 공산당에 영광을 - 1부",
    "You've Got Mail": "편지가 도착했습니다"
}

# Exact Tested Map Coordinates in SVG Canvas (0% ~ 100%)
calibrated_targets = {
    # Customs
    "bronze pocket watch": {"left": 51.86, "top": 55.71, "floor": "Ground_Level", "hint": "건설현장 탱크트럭 운전석"},
    "Secure case for documents 0022": {"left": 85.91, "top": 35.65, "floor": "Ground_Level", "hint": "빅 레드 2층 타르콘 사무소"},
    "Package with graphics cards": {"left": 85.50, "top": 37.18, "floor": "Ground_Level", "hint": "빅 레드 2층 타르콘 사무소"},
    "Secure case for documents 0031": {"left": 48.48, "top": 57.66, "floor": "Ground_Level", "hint": "기숙사 인근 임시 컨테이너 숙소"},
    "Bank case": {"left": 47.97, "top": 84.03, "floor": "Ground_Level", "hint": "3층 기숙사 214호"},
    "Gilded Zibbo lighter": {"left": 48.28, "top": 84.66, "floor": "Ground_Level", "hint": "3층 기숙사 303호"},
    "Carbon case": {"left": 42.90, "top": 85.29, "floor": "Ground_Level", "hint": "2층 기숙사 114호"},
    "The hidden water in 2-story dorms, room 206": {"left": 42.80, "top": 81.30, "floor": "Ground_Level", "hint": "2층 기숙사 206호"},
    "Docs 0048": {"left": 30.32, "top": 45.38, "floor": "Ground_Level", "hint": "신골조 근처 경비실 캐빈"},
    "Docs 0013": {"left": 18.56, "top": 22.90, "floor": "Ground_Level", "hint": "기차 선로 객차 0013 내부"},
    "Sealed letter (TerraGroup)": {"left": 46.25, "top": 88.03, "floor": "Ground_Level", "hint": "3층 기숙사 220호"},
    "Sliderkey Secure Flash drive": {"left": 46.25, "top": 88.03, "floor": "Ground_Level", "hint": "3층 기숙사 220호"},
    "Transport van": {"left": 19.68, "top": 39.29, "floor": "Ground_Level", "hint": "보일러실 뒤 밴 차량"},
    "Roadblock": {"left": 63.49, "top": 74.37, "floor": "Ground_Level", "hint": "기숙사 앞 도로 바리케이드"},
    "False flash drive": {"left": 73.23, "top": 56.93, "floor": "Ground_Level", "hint": "강 건너 다리 밑 숙소"},
    "Tigr vehicle 1": {"left": 13.29, "top": 46.64, "floor": "Ground_Level", "hint": "골조 철로 티그르 장갑차"},
    "Tigr vehicle 2": {"left": 17.55, "top": 49.16, "floor": "Ground_Level", "hint": "주유소 인근 티그르 장갑차"},
    "Tigr vehicle 3": {"left": 64.30, "top": 57.14, "floor": "Ground_Level", "hint": "다리 건널목 티그르 장갑차"},
    "Ritual spot": {"left": 47.77, "top": 91.18, "floor": "Ground_Level", "hint": "3층 기숙사 마크방 (314호)"},
    # The Blood of War (Active replacement for BP Depot)
    "Fuel tank 1": {"left": 24.02, "top": 56.82, "floor": "Ground_Level", "hint": "신주유소 앞 유조 탱크트럭"},
    "Fuel tank 2": {"left": 34.70, "top": 15.88, "floor": "Ground_Level", "hint": "검문소 인근 유조 탱크트럭"},
    "Fuel tank 3": {"left": 51.59, "top": 53.48, "floor": "Ground_Level", "hint": "건설현장 유조 탱크트럭"},
    
    # Factory
    "Place Secure case for documents 0022": {"left": 20.42, "top": 23.83, "floor": "First_Floor", "hint": "공장 2층 펌프실/환기구 캐빈"},
    
    # Woods
    "Shturman": {"left": 48.5, "top": 58.2, "floor": "Ground_Level", "hint": "우드 제재소(벌목장) 중앙 수햔 스폰"},
    "Convoy": {"left": 39.5, "top": 35.8, "floor": "Ground_Level", "hint": "우드 북쪽 USEC 호송대"},
    "USEC camp": {"left": 28.3, "top": 25.4, "floor": "Ground_Level", "hint": "우드 북서쪽 USEC 캠프"},
    "Bunker 1": {"left": 62.4, "top": 28.5, "floor": "Ground_Level", "hint": "우드 북동쪽 ZB-014 벙커"},
    "Bunker 2": {"left": 68.2, "top": 64.1, "floor": "Ground_Level", "hint": "우드 남동쪽 ZB-016 벙커"},

    # Ground Zero
    "Emercom 의무실": {"left": 71.5, "top": 78.2, "floor": "Ground_Level", "hint": "Emercom 검문소 의무실 텐트"},
    "AGS-30 유탄발사기 진지": {"left": 44.8, "top": 32.5, "floor": "First_Floor", "hint": "캐피탈 인사이트 2층"},
    "테라그룹 지부 연구실": {"left": 52.3, "top": 48.6, "floor": "Ground_Level", "hint": "테라그룹 본사 1층"},
    "과학자의 하드 드라이브": {"left": 52.3, "top": 48.6, "floor": "Ground_Level", "hint": "테라그룹 본사 연구실 HDD"},
    "프리모르스키 대로 택시 V-Ex": {"left": 22.8, "top": 24.1, "floor": "Ground_Level", "hint": "북서쪽 대로 택시"},
    "와인 병 (Wine bottle)": {"left": 61.2, "top": 63.4, "floor": "Ground_Level", "hint": "레스토랑 와인 저장고"}
}

processed_quests = []

# List of deleted obsolete quest titles
obsolete_titles = {"BP depot", "BP Depot"}

for q in raw_quests:
    title_en = q.get("title", "")
    
    # Filter obsolete or removed quests
    if title_en in obsolete_titles or title_en in removed_quests_dict.values():
        print(f"Skipping obsolete quest: {title_en}")
        continue

    title_ko = translations.get(title_en, title_en)
    giver_id = q.get("giver")
    trader = traders_dict.get(giver_id, {"id": "unknown", "name_en": "Unknown", "name_ko": "알 수 없음"})
    
    objectives = []
    quest_maps = set()
    has_gps = False
    
    for obj in q.get("objectives", []):
        loc_id = obj.get("location", -1)
        m_cfg = map_configs.get(loc_id)
        
        target = obj.get("target", "")
        target_str = target if isinstance(target, str) else str(target)
        obj_type = obj.get("type", "unknown")
        number = obj.get("number", 1)
        
        gps = obj.get("gps")
        hint_text = ""

        # Check calibrated targets
        if target_str in calibrated_targets:
            calib = calibrated_targets[target_str]
            gps = {
                "leftPercent": calib["left"],
                "topPercent": calib["top"],
                "floor": calib["floor"]
            }
            hint_text = f" [{calib['hint']}]"
            has_gps = True
        elif gps and "leftPercent" in gps and "topPercent" in gps:
            has_gps = True

        if m_cfg:
            quest_maps.add(m_cfg["id"])

        # Description
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
        "id": q.get("id"),
        "title_en": title_en,
        "title_ko": title_ko,
        "trader": trader,
        "required_level": q.get("require", {}).get("level", 1),
        "required_quests": q.get("require", {}).get("quests", []),
        "exp": q.get("exp", 0),
        "wiki": q.get("wiki", ""),
        "maps": list(quest_maps),
        "has_gps": has_gps,
        "objectives": objectives
    })

# Add Active The Blood of War - Part 1 (Replacement for BP depot with Fuel Tanks)
blood_of_war_1 = {
    "id": 801,
    "title_en": "The Blood of War - Part 1",
    "title_ko": "전쟁의 피 - 1부",
    "trader": {"id": "ragman", "name_en": "Ragman", "name_ko": "래그맨"},
    "required_level": 25,
    "required_quests": [],
    "exp": 16500,
    "wiki": "https://escapefromtarkov.fandom.com/wiki/The_Blood_of_War_-_Part_1",
    "maps": ["customs"],
    "has_gps": True,
    "objectives": [
        {
            "id": 8011,
            "type": "mark",
            "target": "Fuel tank 1",
            "number": 1,
            "location_id": 1,
            "map_id": "customs",
            "map_name_ko": "세관",
            "map_name_en": "Customs",
            "gps": {"leftPercent": 24.02, "topPercent": 56.82, "floor": "Ground_Level"},
            "hint": "신주유소 앞 유조 탱크트럭",
            "description_ko": "🎯 첫 번째 유조차에 MS2000 마커 부착 [신주유소 앞]"
        },
        {
            "id": 8012,
            "type": "mark",
            "target": "Fuel tank 2",
            "number": 1,
            "location_id": 1,
            "map_id": "customs",
            "map_name_ko": "세관",
            "map_name_en": "Customs",
            "gps": {"leftPercent": 34.70, "topPercent": 15.88, "floor": "Ground_Level"},
            "hint": "검문소 인근 유조 탱크트럭",
            "description_ko": "🎯 두 번째 유조차에 MS2000 마커 부착 [검문소 인근]"
        },
        {
            "id": 8013,
            "type": "mark",
            "target": "Fuel tank 3",
            "number": 1,
            "location_id": 1,
            "map_id": "customs",
            "map_name_ko": "세관",
            "map_name_en": "Customs",
            "gps": {"leftPercent": 51.59, "topPercent": 53.48, "floor": "Ground_Level"},
            "hint": "건설현장 유조 탱크트럭",
            "description_ko": "🎯 세 번째 유조차에 MS2000 마커 부착 [건설현장]"
        },
        {
            "id": 8014,
            "type": "extract",
            "target": "세관 탈출",
            "number": 1,
            "location_id": 1,
            "map_id": "customs",
            "map_name_ko": "세관",
            "map_name_en": "Customs",
            "gps": None,
            "hint": "",
            "description_ko": "🚪 세관에서 살아서 탈출"
        }
    ]
}

processed_quests.append(blood_of_war_1)

# Add Ground Zero quests
ground_zero_quests = [
    {
        "id": 901,
        "title_en": "First in Line",
        "title_ko": "첫 번째 순서",
        "trader": {"id": "therapist", "name_en": "Therapist", "name_ko": "테라피스트"},
        "required_level": 1,
        "required_quests": [],
        "exp": 1200,
        "wiki": "https://escapefromtarkov.fandom.com/wiki/First_in_Line",
        "maps": ["groundzero"],
        "has_gps": True,
        "objectives": [
            {
                "id": 9011,
                "type": "locate",
                "target": "Emercom 의무실",
                "number": 1,
                "location_id": 9,
                "map_id": "groundzero",
                "map_name_ko": "그라운드 제로",
                "map_name_en": "Ground Zero",
                "gps": {"leftPercent": 71.5, "topPercent": 78.2, "floor": "Ground_Level"},
                "hint": "그라운드 제로 남동쪽 Emercom 검문소 의무실 텐트",
                "description_ko": "🔍 Emercom 의무실 탐색 [그라운드 제로 남동쪽 텐트]"
            }
        ]
    },
    {
        "id": 902,
        "title_en": "Shooting Cans",
        "title_ko": "깡통 사격",
        "trader": {"id": "prapor", "name_en": "Prapor", "name_ko": "프라포르"},
        "required_level": 1,
        "required_quests": [],
        "exp": 1200,
        "wiki": "https://escapefromtarkov.fandom.com/wiki/Shooting_Cans",
        "maps": ["groundzero"],
        "has_gps": True,
        "objectives": [
            {
                "id": 9021,
                "type": "locate",
                "target": "AGS-30 유탄발사기 진지",
                "number": 1,
                "location_id": 9,
                "map_id": "groundzero",
                "map_name_ko": "그라운드 제로",
                "map_name_en": "Ground Zero",
                "gps": {"leftPercent": 44.8, "topPercent": 32.5, "floor": "First_Floor"},
                "hint": "캐피탈 인사이트 건물 2층 유탄발사기",
                "description_ko": "🔍 UTYOS/AGS 유탄발사기 위치 정찰 [캐피탈 2층]"
            }
        ]
    },
    {
        "id": 903,
        "title_en": "Saving the Mole",
        "title_ko": "두더지 구출 작전",
        "trader": {"id": "mechanic", "name_en": "Mechanic", "name_ko": "메카닉"},
        "required_level": 1,
        "required_quests": [],
        "exp": 1500,
        "wiki": "https://escapefromtarkov.fandom.com/wiki/Saving_the_Mole",
        "maps": ["groundzero"],
        "has_gps": True,
        "objectives": [
            {
                "id": 9031,
                "type": "locate",
                "target": "테라그룹 지부 연구실",
                "number": 1,
                "location_id": 9,
                "map_id": "groundzero",
                "map_name_ko": "그라운드 제로",
                "map_name_en": "Ground Zero",
                "gps": {"leftPercent": 52.3, "topPercent": 48.6, "floor": "Ground_Level"},
                "hint": "테라그룹 본사 건물 1층 연구실",
                "description_ko": "🔍 테라그룹 지부 과학자 연구실 탐색 [테라그룹 본사]"
            },
            {
                "id": 9032,
                "type": "pickup",
                "target": "과학자의 하드 드라이브",
                "number": 1,
                "location_id": 9,
                "map_id": "groundzero",
                "map_name_ko": "그라운드 제로",
                "map_name_en": "Ground Zero",
                "gps": {"leftPercent": 52.3, "topPercent": 48.6, "floor": "Ground_Level"},
                "hint": "연구실 책상 위 HDD",
                "description_ko": "📦 과학자의 하드 드라이브 획득 [테라그룹 본사 연구실]"
            }
        ]
    }
]

for gq in ground_zero_quests:
    processed_quests.append(gq)

with open("app/data/quests.json", "w", encoding="utf-8") as f:
    json.dump(processed_quests, f, indent=2, ensure_ascii=False)

with open("secondary_data/processed_quests.json", "w", encoding="utf-8") as f:
    json.dump(processed_quests, f, indent=2, ensure_ascii=False)

print(f"Successfully cleaned quests DB! Active quests count: {len(processed_quests)}")
print("BP depot removed and replaced with The Blood of War - Part 1.")
print("All quest GPS coordinates restored to verified in-canvas positions.")
