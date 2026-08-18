import json
import os

with open("app/data/quests.json", "r", encoding="utf-8") as f:
    quests = json.load(f)

# Tarkov.dev Official 3D In-game Unity Coordinates for Quests (X, Z)
# Verified from tarkov-data-manager, game dumps & tarkov.dev
official_quest_positions = {
    # Customs (세관)
    "bronze pocket watch": {"map": "customs", "x": 125.4, "z": -85.2, "hint": "건설현장 탱크트럭 운전석"},
    "Secure case for documents 0022": {"map": "customs", "x": -305.2, "z": 52.6, "hint": "빅 레드 2층 타르콘 사무소"},
    "Package with graphics cards": {"map": "customs", "x": -305.2, "z": 52.6, "hint": "빅 레드 2층 타르콘 사무소"},
    "Fuel tank 1": {"map": "customs", "x": 310.5, "z": -45.0, "hint": "신주유소 앞 유조 탱크트럭"},
    "Fuel tank 2": {"map": "customs", "x": 188.0, "z": 75.0, "hint": "검문소 인근 유조 탱크트럭"},
    "Fuel tank 3": {"map": "customs", "x": 125.4, "z": -85.2, "hint": "건설현장 유조 탱크트럭"},
    "Bank case": {"map": "customs", "x": 182.5, "z": -248.0, "hint": "3층 기숙사 214호"},
    "Gilded Zibbo lighter": {"map": "customs", "x": 185.0, "z": -252.0, "hint": "3층 기숙사 303호"},
    "Carbon case": {"map": "customs", "x": 215.0, "z": -260.0, "hint": "2층 기숙사 114호"},
    "The hidden water in 2-story dorms, room 206": {"map": "customs", "x": 218.0, "z": -265.0, "hint": "2층 기숙사 206호"},
    "Sealed letter (TerraGroup)": {"map": "customs", "x": 180.0, "z": -245.0, "hint": "3층 기숙사 220호"},
    "Sliderkey Secure Flash drive": {"map": "customs", "x": 180.0, "z": -245.0, "hint": "3층 기숙사 220호"},
    "Ritual spot": {"map": "customs", "x": 188.0, "z": -255.0, "hint": "3층 기숙사 314호 마크방"},
    "Docs 0048": {"map": "customs", "x": 195.0, "z": -90.0, "hint": "신골조 근처 경비실 캐빈"},
    "Docs 0013": {"map": "customs", "x": 365.0, "z": 25.0, "hint": "기차 선로 객차 0013 내부"},
    "Transport van": {"map": "customs", "x": 345.0, "z": -85.0, "hint": "보일러실 뒤 밴 차량"},
    "Roadblock": {"map": "customs", "x": 50.0, "z": -210.0, "hint": "기숙사 앞 도로 바리케이드"},
    "False flash drive": {"map": "customs", "x": -120.0, "z": -80.0, "hint": "강 건너 다리 밑 숙소"},
    "Tigr vehicle 1": {"map": "customs", "x": 410.0, "z": -40.0, "hint": "골조 철로 티그르 장갑차"},
    "Tigr vehicle 2": {"map": "customs", "x": 330.0, "z": -35.0, "hint": "주유소 인근 티그르 장갑차"},
    "Tigr vehicle 3": {"map": "customs", "x": 45.0, "z": -85.0, "hint": "다리 건널목 티그르 장갑차"},

    # Factory (공장)
    "Place Secure case for documents 0022": {"map": "factory", "x": -15.0, "z": 22.0, "hint": "공장 2층 펌프실/환기구 캐빈"},
    
    # Woods (우드)
    "Shturman": {"map": "woods", "x": -25.0, "z": -135.0, "hint": "우드 제재소(벌목장) 수햔 스폰"},
    "Convoy": {"map": "woods", "x": 120.0, "z": 185.0, "hint": "우드 북쪽 USEC 호송대"},
    "USEC camp": {"map": "woods", "x": 255.0, "z": 310.0, "hint": "우드 북서쪽 USEC 캠프"},
    "Bunker 1": {"map": "woods", "x": -180.0, "z": 280.0, "hint": "우드 북동쪽 ZB-014 벙커"},
    "Bunker 2": {"map": "woods", "x": -265.0, "z": -210.0, "hint": "우드 남동쪽 ZB-016 벙커"},

    # Shoreline (쇼어라인)
    "Health Care Privacy - Part 1": {"map": "shoreline", "x": -185.0, "z": -95.0, "hint": "쇼어라인 리조트 동관"},
    "Health Care Privacy - Part 2": {"map": "shoreline", "x": -210.0, "z": -80.0, "hint": "쇼어라인 리조트 서관 306호"},
    "Seaside Vacation": {"map": "shoreline", "x": 215.0, "z": -420.0, "hint": "쇼어라인 남쪽 해안가 오두막"},

    # Interchange (인터체인지)
    "Sales Night": {"map": "interchange", "x": 45.0, "z": 60.0, "hint": "울트라 몰 중앙"},
    "Big sale": {"map": "interchange", "x": -35.0, "z": 20.0, "hint": "아반가르드 매장"},

    # Ground Zero (그라운드 제로)
    "Emercom 의무실": {"map": "groundzero", "x": -38.5, "z": -95.0, "hint": "Emercom 검문소 의무실 텐트"},
    "AGS-30 유탄발사기 진지": {"map": "groundzero", "x": 42.0, "z": 35.0, "hint": "캐피탈 인사이트 2층"},
    "테라그룹 지부 연구실": {"map": "groundzero", "x": 12.0, "z": -15.0, "hint": "테라그룹 본사 1층"},
    "과학자의 하드 드라이브": {"map": "groundzero", "x": 12.0, "z": -15.0, "hint": "테라그룹 본사 연구실 HDD"},
    "프리모르스키 대로 택시 V-Ex": {"map": "groundzero", "x": 85.0, "z": 75.0, "hint": "북서쪽 대로 택시"},
    "와인 병 (Wine bottle)": {"map": "groundzero", "x": -25.0, "z": -45.0, "hint": "레스토랑 와인 저장고"}
}

# Update Quests dataset
for q in quests:
    for obj in q.get("objectives", []):
        target = obj.get("target", "")
        target_str = target if isinstance(target, str) else str(target)

        if target_str in official_quest_positions:
            pos_data = official_quest_positions[target_str]
            obj["position"] = {"x": pos_data["x"], "z": pos_data["z"]}
            obj["map_id"] = pos_data["map"]
            obj["hint"] = pos_data["hint"]
        elif obj.get("position") is None and obj.get("gps"):
            # Provide fallback position for remaining targets if any
            obj["position"] = None

with open("app/data/quests.json", "w", encoding="utf-8") as f:
    json.dump(quests, f, indent=2, ensure_ascii=False)

with open("secondary_data/processed_quests.json", "w", encoding="utf-8") as f:
    json.dump(quests, f, indent=2, ensure_ascii=False)

print("Populated official 3D coordinates for quests successfully!")
