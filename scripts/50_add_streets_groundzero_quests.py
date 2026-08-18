import json

with open("app/data/quests.json", "r", encoding="utf-8") as f:
    quests = json.load(f)

# Ground Zero & Streets Quests data with precise locations
new_quests = [
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
            },
            {
                "id": 9012,
                "type": "collect",
                "target": "의약품 아이템",
                "number": 3,
                "location_id": 9,
                "map_id": "groundzero",
                "map_name_ko": "그라운드 제로",
                "map_name_en": "Ground Zero",
                "gps": {"leftPercent": 71.5, "topPercent": 78.2, "floor": "Ground_Level"},
                "hint": "Emercom 텐트 내부 의약품 상자",
                "description_ko": "🎒 인레이드 의약품 3개 전달"
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
            },
            {
                "id": 9022,
                "type": "kill",
                "target": "그라운드 제로 스캐브",
                "number": 5,
                "location_id": 9,
                "map_id": "groundzero",
                "map_name_ko": "그라운드 제로",
                "map_name_en": "Ground Zero",
                "gps": {"leftPercent": 50.0, "topPercent": 50.0, "floor": "Ground_Level"},
                "hint": "그라운드 제로 전역",
                "description_ko": "⚔️ 그라운드 제로에서 적/스캐브 5명 처치"
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
    },
    {
        "id": 904,
        "title_en": "Burning Rubber",
        "title_ko": "타는 고무 냄새",
        "trader": {"id": "skier", "name_en": "Skier", "name_ko": "스키어"},
        "required_level": 1,
        "required_quests": [],
        "exp": 1100,
        "wiki": "https://escapefromtarkov.fandom.com/wiki/Burning_Rubber",
        "maps": ["groundzero"],
        "has_gps": True,
        "objectives": [
            {
                "id": 9041,
                "type": "extract",
                "target": "프리모르스키 대로 택시 V-Ex",
                "number": 1,
                "location_id": 9,
                "map_id": "groundzero",
                "map_name_ko": "그라운드 제로",
                "map_name_en": "Ground Zero",
                "gps": {"leftPercent": 22.8, "topPercent": 24.1, "floor": "Ground_Level"},
                "hint": "북서쪽 프리모르스키 대로 유료 택시",
                "description_ko": "🚪 유료 택시(V-Ex)를 이용하여 탈출 [북서쪽 대로]"
            }
        ]
    },
    {
        "id": 905,
        "title_en": "Luxurious Life",
        "title_ko": "호화로운 삶",
        "trader": {"id": "prapor", "name_en": "Prapor", "name_ko": "프라포르"},
        "required_level": 1,
        "required_quests": [],
        "exp": 1300,
        "wiki": "https://escapefromtarkov.fandom.com/wiki/Luxurious_Life",
        "maps": ["groundzero"],
        "has_gps": True,
        "objectives": [
            {
                "id": 9051,
                "type": "pickup",
                "target": "와인 병 (Wine bottle)",
                "number": 1,
                "location_id": 9,
                "map_id": "groundzero",
                "map_name_ko": "그라운드 제로",
                "map_name_en": "Ground Zero",
                "gps": {"leftPercent": 61.2, "topPercent": 63.4, "floor": "Ground_Level"},
                "hint": "레스토랑 와인 저장고 바닥",
                "description_ko": "📦 고급 와인 병 획득 [레스토랑 와인 저장고]"
            }
        ]
    },
    # Streets of Tarkov Quests
    {
        "id": 906,
        "title_en": "Glory to CPSU - Part 1",
        "title_ko": "소련 공산당에 영광을 - 1부",
        "trader": {"id": "prapor", "name_en": "Prapor", "name_ko": "프라포르"},
        "required_level": 15,
        "required_quests": [],
        "exp": 11500,
        "wiki": "https://escapefromtarkov.fandom.com/wiki/Glory_to_CPSU_-_Part_1",
        "maps": ["streetsoftarkov"],
        "has_gps": True,
        "objectives": [
            {
                "id": 9061,
                "type": "locate",
                "target": "프라포르 친구의 아파트",
                "number": 1,
                "location_id": 8,
                "map_id": "streetsoftarkov",
                "map_name_ko": "타르코프 시내",
                "map_name_en": "Streets of Tarkov",
                "gps": {"leftPercent": 42.5, "topPercent": 56.8, "floor": "Ground_Level"},
                "hint": "프리모르스키 아파트 단지",
                "description_ko": "🔍 프라포르 친구의 아파트 위치 정찰 [프리모르스키 대로]"
            }
        ]
    },
    {
        "id": 907,
        "title_en": "You've Got Mail",
        "title_ko": "편지가 도착했습니다",
        "trader": {"id": "prapor", "name_en": "Prapor", "name_ko": "프라포르"},
        "required_level": 15,
        "required_quests": [],
        "exp": 12000,
        "wiki": "https://escapefromtarkov.fandom.com/wiki/You%27ve_Got_Mail",
        "maps": ["streetsoftarkov"],
        "has_gps": True,
        "objectives": [
            {
                "id": 9071,
                "type": "pickup",
                "target": "봉인된 편지",
                "number": 1,
                "location_id": 8,
                "map_id": "streetsoftarkov",
                "map_name_ko": "타르코프 시내",
                "map_name_en": "Streets of Tarkov",
                "gps": {"leftPercent": 58.2, "topPercent": 41.3, "floor": "Ground_Level"},
                "hint": "우체국(Post Office) 내부 책상",
                "description_ko": "📦 봉인된 편지 획득 [타르코프 중앙 우체국]"
            }
        ]
    }
]

# Merge into quests
existing_ids = {q["id"] for q in quests}
for nq in new_quests:
    if nq["id"] not in existing_ids:
        quests.append(nq)

with open("app/data/quests.json", "w", encoding="utf-8") as f:
    json.dump(quests, f, indent=2, ensure_ascii=False)

with open("secondary_data/processed_quests.json", "w", encoding="utf-8") as f:
    json.dump(quests, f, indent=2, ensure_ascii=False)

print(f"Successfully added Ground Zero and Streets quests! Total quests now: {len(quests)}")
