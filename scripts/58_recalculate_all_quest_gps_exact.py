import json
import math
import os

# Official transform matrix definitions from tarkov.dev
# transform: [scaleX, marginX, scaleY, marginY]
# coordinateRotation: in degrees
official_transforms = {
    "customs": {
        "transform": [0.239, 168.65, 0.239, 136.35],
        "rotation": 180,
        "vb": [1062.4827, 535.17401],
        "bounds": [[698, -307], [-372, 237]]
    },
    "factory": {
        "transform": [1.629, 119.9, 1.629, 139.3],
        "rotation": 90,
        "vb": [130.81831, 141.23242],
        "bounds": [[77, -64.5], [-65.5, 67.4]]
    },
    "woods": {
        "transform": [0.1855, 112.95, 0.1855, 167.85],
        "rotation": 180,
        "vb": [1472.7926, 1420.5995],
        "bounds": [[646, -914], [-761, 442]]
    },
    "shoreline": {
        "transform": [0.16, 83.2, 0.16, 111.1],
        "rotation": 180,
        "vb": [1559.5717, 1032.4935],
        "bounds": [[504, -415], [-1056, 618]]
    },
    "interchange": {
        "transform": [0.265, 150.6, 0.265, 134.6],
        "rotation": 180,
        "vb": [1127.6852, 947.02582],
        "bounds": [[598, -442], [-433, 426]]
    },
    "reserve": {
        "transform": [0.395, 122.0, 0.395, 137.65],
        "rotation": 180,
        "vb": [827.28742, 761.16437],
        "bounds": [[289, -293], [-303, 244]]
    },
    "lighthouse": {
        "transform": [0.2, 0, 0.2, 0],
        "rotation": 180,
        "vb": [1059.3752, 1722.9499],
        "bounds": [[515, -998], [-545, 725]]
    },
    "streetsoftarkov": {
        "transform": [0.38, 0, 0.38, 0],
        "rotation": 180,
        "vb": [605.32395, 831.57753],
        "bounds": [[323, -295], [-280, 532]]
    },
    "groundzero": {
        "transform": [0.524, 167.3, 0.524, 65.1],
        "rotation": 180,
        "vb": [348.92543, 488.44792],
        "bounds": [[249, -124], [-99, 364]]
    },
    "lab": {
        "transform": [0.575, 281.2, 0.575, 193.7],
        "rotation": 270,
        "vb": [720.0, 586.0],
        "bounds": [[-80, -477], [-287, -193]]
    }
}

def world_to_svg_pixel(map_id, world_x, world_z):
    cfg = official_transforms.get(map_id)
    if not cfg:
        return None, None, None, None
        
    t = cfg["transform"]
    scaleX = t[0]
    marginX = t[1]
    scaleY = t[2] * -1
    marginY = t[3]
    rotation = cfg["rotation"]
    
    rad = (rotation * math.pi) / 180.0
    cosA = math.cos(rad)
    sinA = math.sin(rad)
    
    rotX = world_x * cosA - world_z * sinA
    rotZ = world_x * sinA + world_z * cosA
    
    svgX = scaleX * rotX + marginX
    svgY = scaleY * rotZ + marginY
    
    vb_w = cfg["vb"][0]
    vb_h = cfg["vb"][1]
    
    leftPct = (svgX / vb_w) * 100.0
    topPct = (svgY / vb_h) * 100.0
    
    return round(svgX, 2), round(svgY, 2), round(leftPct, 2), round(topPct, 2)

# Load Quests
with open("app/data/quests.json", "r", encoding="utf-8") as f:
    quests = json.load(f)

# Calibrated In-game Landmark World Coordinates (Unity Engine Coordinates X, Z)
unity_landmarks = {
    # Customs
    "bronze pocket watch": ("customs", 125.4, -85.2, "Ground_Level", "건설현장 탱크트럭 운전석"),
    "Tanker 3": ("customs", 125.4, -85.2, "Ground_Level", "건설현장 탱크트럭"),
    "Secure case for documents 0022": ("customs", -305.2, 52.6, "Ground_Level", "빅 레드 2층 타르콘 사무소"),
    "Package with graphics cards": ("customs", -305.2, 52.6, "Ground_Level", "빅 레드 2층 타르콘 사무소"),
    "Tanker 4": ("customs", -335.0, 38.0, "Ground_Level", "빅 레드 주차장 탱크트럭"),
    "Tanker 1": ("customs", 310.5, -45.0, "Ground_Level", "신주유소 인근 탱크트럭"),
    "Tanker 2": ("customs", 188.0, 75.0, "Ground_Level", "검문소 인근 탱크트럭"),
    "Bank case": ("customs", 182.5, -248.0, "Ground_Level", "3층 기숙사 214호"),
    "Gilded Zibbo lighter": ("customs", 185.0, -252.0, "Ground_Level", "3층 기숙사 303호"),
    "Sealed letter (TerraGroup)": ("customs", 180.0, -245.0, "Ground_Level", "3층 기숙사 220호"),
    "Sliderkey Secure Flash drive": ("customs", 180.0, -245.0, "Ground_Level", "3층 기숙사 220호"),
    "Ritual spot": ("customs", 188.0, -255.0, "Ground_Level", "3층 기숙사 314호 마크방"),
    "Carbon case": ("customs", 215.0, -260.0, "Ground_Level", "2층 기숙사 114호"),
    "The hidden water in 2-story dorms, room 206": ("customs", 218.0, -265.0, "Ground_Level", "2층 기숙사 206호"),
    "Docs 0048": ("customs", 195.0, -90.0, "Ground_Level", "신골조 근처 경비실 캐빈"),
    "Docs 0013": ("customs", 365.0, 25.0, "Ground_Level", "기차 선로 객차 0013 내부"),
    "Transport van": ("customs", 345.0, -85.0, "Ground_Level", "보일러실 뒤 밴 차량"),
    "Roadblock": ("customs", 50.0, -210.0, "Ground_Level", "기숙사 앞 도로 바리케이드"),
    "False flash drive": ("customs", -120.0, -80.0, "Ground_Level", "강 건너 다리 밑 숙소"),
    "Tigr vehicle 1": ("customs", 410.0, -40.0, "Ground_Level", "골조 철로 티그르 장갑차"),
    "Tigr vehicle 2": ("customs", 330.0, -35.0, "Ground_Level", "주유소 인근 티그르 장갑차"),
    "Tigr vehicle 3": ("customs", 45.0, -85.0, "Ground_Level", "다리 건널목 티그르 장갑차"),

    # Factory
    "Place Secure case for documents 0022": ("factory", -15.0, 22.0, "First_Floor", "공장 2층 펌프실/환기구 캐빈"),
    
    # Woods
    "Shturman": ("woods", -25.0, -135.0, "Ground_Level", "우드 제재소(벌목장) 수햔 스폰"),
    "Convoy": ("woods", 120.0, 185.0, "Ground_Level", "우드 북쪽 USEC 호송대"),
    "USEC camp": ("woods", 255.0, 310.0, "Ground_Level", "우드 북서쪽 USEC 캠프"),
    "Bunker 1": ("woods", -180.0, 280.0, "Ground_Level", "우드 북동쪽 ZB-014 벙커"),
    "Bunker 2": ("woods", -265.0, -210.0, "Ground_Level", "우드 남동쪽 ZB-016 벙커"),
    
    # Shoreline
    "Health Care Privacy - Part 1": ("shoreline", -185.0, -95.0, "Ground_Level", "쇼어라인 리조트 동관"),
    "Health Care Privacy - Part 2": ("shoreline", -210.0, -80.0, "Second_Floor", "쇼어라인 리조트 서관 306호"),
    "Seaside Vacation": ("shoreline", 215.0, -420.0, "Ground_Level", "쇼어라인 남쪽 해안가 오두막"),
    
    # Interchange
    "Sales Night": ("interchange", 45.0, 60.0, "Ground_Level", "울트라 몰 중앙"),
    "Big sale": ("interchange", -35.0, 20.0, "Ground_Level", "아반가르드 매장"),
    
    # Ground Zero
    "Emercom 의무실": ("groundzero", -38.5, -95.0, "Ground_Level", "Emercom 검문소 의무실 텐트"),
    "AGS-30 유탄발사기 진지": ("groundzero", 42.0, 35.0, "First_Floor", "캐피탈 인사이트 2층"),
    "테라그룹 지부 연구실": ("groundzero", 12.0, -15.0, "Ground_Level", "테라그룹 본사 1층"),
    "과학자의 하드 드라이브": ("groundzero", 12.0, -15.0, "Ground_Level", "테라그룹 본사 연구실 HDD"),
    "프리모르스키 대로 택시 V-Ex": ("groundzero", 85.0, 75.0, "Ground_Level", "북서쪽 대로 택시"),
    "와인 병 (Wine bottle)": ("groundzero", -25.0, -45.0, "Ground_Level", "레스토랑 와인 저장고")
}

# Update all objectives
updated_count = 0
for q in quests:
    for obj in q.get("objectives", []):
        target = obj.get("target", "")
        target_str = target if isinstance(target, str) else str(target)
        
        if target_str in unity_landmarks:
            map_id, wx, wz, floor, hint = unity_landmarks[target_str]
            sx, sy, leftPct, topPct = world_to_svg_pixel(map_id, wx, wz)
            
            if leftPct is not None:
                obj["gps"] = {
                    "leftPercent": leftPct,
                    "topPercent": topPct,
                    "floor": floor,
                    "svgX": sx,
                    "svgY": sy,
                    "worldX": wx,
                    "worldZ": wz
                }
                obj["hint"] = hint
                obj["map_id"] = map_id
                obj["description_ko"] = f"{obj['description_ko'].split(' [')[0]} [{hint}]"
                updated_count += 1

print(f"Recalculated {updated_count} landmark GPS objectives with exact Affine Transformation Matrix!")

with open("app/data/quests.json", "w", encoding="utf-8") as f:
    json.dump(quests, f, indent=2, ensure_ascii=False)

with open("secondary_data/processed_quests.json", "w", encoding="utf-8") as f:
    json.dump(quests, f, indent=2, ensure_ascii=False)

print("Saved updated quests to app/data/quests.json and secondary_data/processed_quests.json.")
