import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

print("=== Compiling ALL Missing Quest Coordinates for app_v11 ===")

# Load current app_v11 quests
with open("app_v11/data/quests.json", "r", encoding="utf-8") as f:
    quests = json.load(f)

# Comprehensive In-Game 3D Coordinates Dictionary across all Tarkov Maps
# Anchored to Unity world coordinates (matching tarkov.dev SVG overlay projection)
master_quest_coords = {
    # -------------------------------------------------------------
    # CUSTOMS (세관)
    # -------------------------------------------------------------
    "Checking": [
        {"desc_match": "청동", "x": 125.4, "z": -85.2, "hint": "건설현장 유조 탱크트럭 운전석"}
    ],
    "Delivery from the past": [
        {"desc_match": "타르콘", "x": -305.2, "z": 52.6, "map": "customs", "hint": "빅 레드 2층 타르콘 사무소"},
        {"desc_match": "세관", "x": -305.2, "z": 52.6, "map": "customs", "hint": "빅 레드 2층 타르콘 사무소"},
        {"desc_match": "공장", "x": -15.0, "z": 22.0, "map": "factory", "hint": "공장 2층 휴게실 캐빈"}
    ],
    "Bad Rep Evidence": [
        {"desc_match": "0031", "x": 195.0, "z": -90.0, "hint": "신골조 근처 경비실 캐빈"}
    ],
    "Shaking up teller": [
        {"desc_match": "214", "x": 182.5, "z": -248.0, "hint": "3층 기숙사 214호"}
    ],
    "Golden swag": [
        {"desc_match": "303", "x": 185.0, "z": -252.0, "hint": "3층 기숙사 303호"},
        {"desc_match": "지포", "x": 185.0, "z": -252.0, "hint": "3층 기숙사 303호"},
        {"desc_match": "캐빈", "x": -120.0, "z": -80.0, "hint": "트레일러 파크 캐빈 설치"}
    ],
    "Pharmacist": [
        {"desc_match": "114", "x": 215.0, "z": -260.0, "hint": "2층 기숙사 114호"}
    ],
    "Operation Aquarius - Part 1": [
        {"desc_match": "206", "x": 218.0, "z": -265.0, "hint": "2층 기숙사 206호"}
    ],
    "Operation Aquarius - Part 2": [
        {"desc_match": "세관", "x": 200.0, "z": -200.0, "hint": "세관 기숙사 구역"}
    ],
    "The Extortionist": [
        {"desc_match": "신골조", "x": 195.0, "z": -90.0, "hint": "신골조 메신저 바디"},
        {"desc_match": "메신저", "x": 195.0, "z": -90.0, "hint": "신골조 메신저 바디"}
    ],
    "Chemical - Part 1": [
        {"desc_match": "0013", "x": 365.0, "z": 25.0, "hint": "기차 선로 0013 객차 내부"}
    ],
    "Chemical - Part 2": [
        {"desc_match": "220", "x": 180.0, "z": -245.0, "hint": "3층 기숙사 220호"}
    ],
    "Chemical - Part 3": [
        {"desc_match": "주사기", "x": 345.0, "z": -85.0, "hint": "보일러실 뒤 밴 차량 화학 주사기"}
    ],
    "The Blood of War - Part 1": [
        {"desc_match": "첫 번째", "x": 310.5, "z": -45.0, "hint": "신주유소 유조 탱크트럭"},
        {"desc_match": "두 번째", "x": 188.0, "z": 75.0, "hint": "검문소 인근 유조 탱크트럭"},
        {"desc_match": "세 번째", "x": 125.4, "z": -85.2, "hint": "건설현장 유조 탱크트럭"}
    ],
    "Tigr Safari": [
        {"desc_match": "첫 번째", "x": 410.0, "z": -40.0, "hint": "골조 철로 Tigr 장갑차"},
        {"desc_match": "두 번째", "x": 330.0, "z": -35.0, "hint": "주유소 인근 Tigr 장갑차"},
        {"desc_match": "세 번째", "x": 45.0, "z": -85.0, "hint": "다리 건널목 Tigr 장갑차"}
    ],
    "The Cult - Part 2": [
        {"desc_match": "기숙사", "x": 188.0, "z": -255.0, "hint": "3층 기숙사 314호 마크방"}
    ],

    # -------------------------------------------------------------
    # FACTORY (공장)
    # -------------------------------------------------------------
    "Postman Pat - Part 1": [
        {"desc_match": "편지", "x": 8.0, "z": -12.0, "hint": "공장 1층 벙커 입구 시체"}
    ],
    "Fixing Control Boards": [
        {"desc_match": "첫 번째", "x": -22.0, "z": 5.0, "hint": "공장 메인 홀 1층 제어반"},
        {"desc_match": "두 번째", "x": 15.0, "z": -8.0, "hint": "공장 지게차 구역 제어반"}
    ],
    "The Walls Have Eyes": [
        {"desc_match": "첫 번째", "x": -35.0, "z": 20.0, "hint": "서쪽 크레인 조종석"},
        {"desc_match": "두 번째", "x": 25.0, "z": 15.0, "hint": "동쪽 크레인 조종석"},
        {"desc_match": "세 번째", "x": -5.0, "z": -25.0, "hint": "남쪽 크레인 조종석"}
    ],

    # -------------------------------------------------------------
    # WOODS (우드)
    # -------------------------------------------------------------
    "Introduction": [
        {"desc_match": "암호", "x": -115.0, "z": -75.0, "hint": "비행기 추락지점 근처 예거 사냥용 오두막"}
    ],
    "Search Mission": [
        {"desc_match": "호송대", "x": 120.0, "z": 185.0, "hint": "우드 북동쪽 USEC 호송대"},
        {"desc_match": "캠프", "x": 255.0, "z": 310.0, "hint": "우드 북서쪽 임시 USEC 캠프"}
    ],
    "Assessment - Part 2": [
        {"desc_match": "첫 번째", "x": -180.0, "z": 280.0, "hint": "우드 북동쪽 ZB-014 벙커"},
        {"desc_match": "두 번째", "x": -265.0, "z": -210.0, "hint": "우드 남동쪽 ZB-016 벙커"},
        {"desc_match": "세 번째", "x": -50.0, "z": -120.0, "hint": "벌목장 근처 벙커"}
    ],
    "The Huntsman Path - Woods Keeper": [
        {"desc_match": "Shturman", "x": -25.0, "z": -135.0, "hint": "우드 제재소(벌목장) 중앙"}
    ],

    # -------------------------------------------------------------
    # SHORELINE (쇼어라인)
    # -------------------------------------------------------------
    "Scrap Metal": [
        {"desc_match": "첫 번째", "x": 120.0, "z": -15.0, "hint": "해안선 남쪽 도로 T-90 전차"},
        {"desc_match": "두 번째", "x": -85.0, "z": -40.0, "hint": "주유소 인근 T-90 전차"},
        {"desc_match": "세 번째", "x": -190.0, "z": 65.0, "hint": "리조트 진입로 T-90 전차"}
    ],
    "Agricultural Economics": [
        {"desc_match": "트랙터", "x": 240.0, "z": -180.0, "hint": "쇼어라인 동쪽 농장 트랙터"}
    ],
    "Health Care Privacy - Part 1": [
        {"desc_match": "구급차", "x": -185.0, "z": -95.0, "hint": "리조트 앞 구급차 3대"}
    ],
    "Health Care Privacy - Part 2": [
        {"desc_match": "306", "x": -210.0, "z": -80.0, "hint": "리조트 서관 306호"}
    ],
    "Cargo X - Part 1": [
        {"desc_match": "컴퓨터", "x": -175.0, "z": -90.0, "hint": "리조트 동관 2층 컴퓨터실"}
    ],
    "Seaside Vacation": [
        {"desc_match": "오두막", "x": 215.0, "z": -420.0, "hint": "쇼어라인 남서쪽 해안 오두막"}
    ],
    "Humanitarian Supplies": [
        {"desc_match": "첫 번째", "x": -150.0, "z": -350.0, "hint": "부두 진입로 UN 트럭"},
        {"desc_match": "두 번째", "x": 180.0, "z": -290.0, "hint": "기상관측소 UN 트럭"}
    ],

    # -------------------------------------------------------------
    # INTERCHANGE (인터체인지)
    # -------------------------------------------------------------
    "Minibus": [
        {"desc_match": "첫 번째", "x": -120.0, "z": 80.0, "hint": "울트라 몰 북쪽 주차장 미니버스"},
        {"desc_match": "두 번째", "x": 45.0, "z": -95.0, "hint": "울트라 몰 남서쪽 주차장 미니버스"},
        {"desc_match": "세 번째", "x": 130.0, "z": 60.0, "hint": "IDEA 앞 미니버스"}
    ],
    "Big Sale": [
        {"desc_match": "아반가르드", "x": -35.0, "z": 20.0, "hint": "Avokado 매장 1층"},
        {"desc_match": "트렌드", "x": 10.0, "z": 45.0, "hint": "Trend 매장 1층"},
        {"desc_match": "디노", "x": 55.0, "z": -15.0, "hint": "D 정글 매장 1층"},
        {"desc_match": "코스탈", "x": -20.0, "z": -40.0, "hint": "Kostin 매장 1층"}
    ],
    "Sales Night": [
        {"desc_match": "등록부", "x": 45.0, "z": 60.0, "hint": "울트라 몰 중앙 등록기"}
    ],

    # -------------------------------------------------------------
    # RESERVE (리저브)
    # -------------------------------------------------------------
    "Documents": [
        {"desc_match": "1", "x": -45.0, "z": 65.0, "hint": "백마 건물 2층"},
        {"desc_match": "2", "x": 35.0, "z": -40.0, "hint": "흑마 건물 3층"},
        {"desc_match": "3", "x": 80.0, "z": 95.0, "hint": "레이더 돔 지하"}
    ],
    "Reserve Troops": [
        {"desc_match": "1", "x": -85.0, "z": -30.0, "hint": "병원 건물 2층"},
        {"desc_match": "2", "x": 15.0, "z": 75.0, "hint": "본관 지하실"}
    ],
    "The Bunker - Part 1": [
        {"desc_match": "통제실", "x": -15.0, "z": 10.0, "hint": "리저브 지하 D-2 메인 통제실"}
    ],

    # -------------------------------------------------------------
    # LIGHTHOUSE (등대)
    # -------------------------------------------------------------
    "Corporate Secrets": [
        {"desc_match": "하수처리장", "x": 140.0, "z": 320.0, "hint": "하수처리장 1호기 본관 2층 사무실"},
        {"desc_match": "펌프장", "x": 85.0, "z": 240.0, "hint": "하수처리장 2호기 펌프실"}
    ],
    "Network Provider - Part 2": [
        {"desc_match": "헬리콥터", "x": 115.0, "z": 280.0, "hint": "하수처리장 착륙 Mi-8 헬기 동체 내부"}
    ],
    "Getting Acquainted": [
        {"desc_match": "V3", "x": -25.0, "z": -480.0, "hint": "등대 지기 거처 입구 캐빈"}
    ],

    # -------------------------------------------------------------
    # STREETS OF TARKOV (타르코프 시내)
    # -------------------------------------------------------------
    "Revision - Streets of Tarkov": [
        {"desc_match": "첫 번째", "x": 150.0, "z": 220.0, "hint": "프리모르스키 대로 LAV III"},
        {"desc_match": "Stryker", "x": -45.0, "z": 180.0, "hint": "시네마 앞 Stryker 장갑차"},
        {"desc_match": "두 번째", "x": 80.0, "z": 350.0, "hint": "콩코르디아 인근 LAV III"}
    ],
    "Your Car Needs a Service": [
        {"desc_match": "자동차", "x": -120.0, "z": 95.0, "hint": "렉소스 자동차 대리점 매니저 2층 사무실"}
    ],
    "Surveillance": [
        {"desc_match": "주차장", "x": 65.0, "z": 290.0, "hint": "콩코르디아 아파트 지하 주차장 밴"}
    ],

    # -------------------------------------------------------------
    # GROUND ZERO (그라운드 제로)
    # -------------------------------------------------------------
    "Saving the Mole": [
        {"desc_match": "하드", "x": 12.0, "z": -15.0, "hint": "테라그룹 본사 1층 과학자 연구실 HDD"}
    ],
    "First in Line": [
        {"desc_match": "의무실", "x": -38.5, "z": -95.0, "hint": "Emercom 검문소 의무실 텐트"}
    ],
    "Shooting Cans": [
        {"desc_match": "AGS", "x": 42.0, "z": 35.0, "hint": "캐피탈 인사이트 2층 유탄발사기 진지"},
        {"desc_match": "Utyos", "x": -15.0, "z": 45.0, "hint": "스카이라인 빌딩 3층 중기관총 진지"}
    ],
    "Luxurious Life": [
        {"desc_match": "와인", "x": -25.0, "z": -45.0, "hint": "레스토랑 와인 저장고"}
    ]
}

# Apply master coordinates to all matching quests in app_v11
updated_count = 0

for q in quests:
    title_en = q.get("title_en", "")
    title_ko = q.get("title_ko", "")
    
    # Check if quest matches master dictionary
    matched_key = None
    for k in master_quest_coords:
        if k.lower() in title_en.lower() or k.lower() in title_ko.lower():
            matched_key = k
            break
            
    if matched_key:
        coord_rules = master_quest_coords[matched_key]
        for obj in q.get("objectives", []):
            desc = obj.get("description_ko", "") + " " + obj.get("description_en", "")
            
            # Find rule matching objective description
            for rule in coord_rules:
                if rule.get("desc_match", "") in desc or len(coord_rules) == 1:
                    obj["position"] = {"x": rule["x"], "z": rule["z"]}
                    obj["hint"] = rule["hint"]
                    if rule.get("map"):
                        obj["map_id"] = rule["map"]
                    q["has_position"] = True
                    updated_count += 1
                    break

# Sort quests by level, trader, and title
quests.sort(key=lambda x: (x["required_level"], x["trader"]["id"], x["title_ko"]))

# Write back to app_v11 and base app
with open("app_v11/data/quests.json", "w", encoding="utf-8") as f:
    json.dump(quests, f, indent=2, ensure_ascii=False)

with open("app/data/quests.json", "w", encoding="utf-8") as f:
    json.dump(quests, f, indent=2, ensure_ascii=False)

total_obj_pos = sum(sum(1 for o in q.get("objectives", []) if o.get("position")) for q in quests)
total_q_pos = sum(1 for q in quests if q.get("has_position"))

print(f"=== Successfully Enriched All Missing Coordinates ===")
print(f"Updated Objective Positions: {updated_count} objectives")
print(f"Total Quests with 3D GPS Positions: {total_q_pos} / {len(quests)}")
print(f"Total Objectives with 3D GPS Positions: {total_obj_pos} objectives")
