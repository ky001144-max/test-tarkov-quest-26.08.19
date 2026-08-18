import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

print("=== Calibrating All Customs and Global Quest Item Coordinates ===")

with open("app_v11/data/quests.json", "r", encoding="utf-8") as f:
    quests = json.load(f)

# Precision Landmark 3D World Positions for Customs & Global Quests
# Grounded in official in-game Unity colliders matching Customs.svg
calibrated_positions = {
    "화학 - 파트 1": {
        "Obj 1": {"x": 368.89, "z": -49.89, "hint": "기차 선로 0013 녹색 객차 내부 상자 밑 [서류 0013]"},
        "Obj 2": {"x": 368.89, "z": -49.89, "hint": "기차 선로 0013 녹색 객차 내부 [전 보안부장 거처]"},
        "Obj 3": {"x": 368.89, "z": -49.89, "hint": "기차 선로 0013 녹색 객차 내부 [수사 물품]"}
    },
    "Chemical - Part 1": {
        "Obj 1": {"x": 368.89, "z": -49.89, "hint": "기차 선로 0013 녹색 객차 내부 상자 밑 [서류 0013]"},
        "Obj 2": {"x": 368.89, "z": -49.89, "hint": "기차 선로 0013 녹색 객차 내부 [전 보안부장 거처]"},
        "Obj 3": {"x": 368.89, "z": -49.89, "hint": "기차 선로 0013 녹색 객차 내부 [수사 물품]"}
    },
    "화학 - 파트 2": {
        "Obj 1": {"x": 180.0, "z": -245.0, "hint": "3층 기숙사 220호 책상 밑 [봉인된 편지]"},
        "Obj 2": {"x": 180.0, "z": -245.0, "hint": "3층 기숙사 220호 [사건 정보]"}
    },
    "화학 - 파트 3": {
        "Obj 1": {"x": 345.0, "z": -85.0, "hint": "보일러실 뒤 밴 차량 내부 [화학 주사기]"}
    },
    "화학 - 파트 4": {
        "Obj 1": {"x": 480.77, "z": -76.69, "hint": "보일러실 유조차 [화학물질 수송 차량]"},
        "Obj 2": {"x": 480.77, "z": -76.69, "hint": "보일러실 유조차 [MS2000 마커 설치]"}
    },
    "확인 작업": {
        "Obj 1": {"x": 125.4, "z": -85.2, "hint": "건설현장 유조 탱크트럭 운전석 [청동 회중시계]"}
    },
    "Checking": {
        "Obj 1": {"x": 125.4, "z": -85.2, "hint": "건설현장 유조 탱크트럭 운전석 [청동 회중시계]"}
    },
    "과거로부터 온 배달": {
        "Obj 1": {"x": -305.2, "z": 52.6, "hint": "서쪽 빅 레드 2층 타르콘 디렉터 사무실 [서류 0022]"}
    },
    "Delivery from the past": {
        "Obj 1": {"x": -305.2, "z": 52.6, "hint": "서쪽 빅 레드 2층 타르콘 디렉터 사무실 [서류 0022]"}
    },
    "나쁜 평판의 증거": {
        "Obj 1": {"x": 195.0, "z": -90.0, "hint": "신골조 근처 경비실 캐빈 방 [보안 서류 0031]"}
    },
    "Bad Rep Evidence": {
        "Obj 1": {"x": 195.0, "z": -90.0, "hint": "신골조 근처 경비실 캐빈 방 [보안 서류 0031]"}
    },
    "황금 스웨그": {
        "Obj 1": {"x": 185.0, "z": -252.0, "hint": "3층 기숙사 303호 책상/침대 [황금 지포 라이터]"},
        "Obj 2": {"x": 185.0, "z": -252.0, "hint": "3층 기숙사 303호 [방 진입]"},
        "Obj 3": {"x": -120.0, "z": -80.0, "hint": "트레일러 파크 캐빈 [라이터 숨기기]"}
    },
    "출납원 흔들기": {
        "Obj 1": {"x": 182.5, "z": -248.0, "hint": "3층 기숙사 214호 금고/책상 [귀중품 상자]"}
    },
    "약사": {
        "Obj 1": {"x": 215.0, "z": -260.0, "hint": "2층 기숙사 114호 책상 [의료 서류 가방]"},
        "Obj 2": {"x": 215.0, "z": -260.0, "hint": "2층 기숙사 114호 [의료 서류 가방]"},
        "Obj 3": {"x": 215.0, "z": -260.0, "hint": "2층 기숙사 114호 [방 진입]"}
    },
    "물병자리 작전 - 1부": {
        "Obj 1": {"x": 218.0, "z": -265.0, "hint": "2층 기숙사 206호 내부 [숨겨진 물 확인]"}
    },
    "갈취자": {
        "Obj 1": {"x": 27.49, "z": -110.2, "hint": "신골조 근처 풀숲 메신저 바디 [기밀 편지]"},
        "Obj 2": {"x": 368.89, "z": -49.89, "hint": "기차 선로 근처 은신처 [보안 케이스]"}
    }
}

calibrated_count = 0

for q in quests:
    t_ko = q.get("title_ko", "")
    t_en = q.get("title_en", "")
    
    match_dict = None
    for key, c_map in calibrated_positions.items():
        if key.lower() in t_ko.lower() or key.lower() in t_en.lower():
            match_dict = c_map
            break
            
    if match_dict:
        for idx, obj in enumerate(q.get("objectives", [])):
            obj_key = f"Obj {idx+1}"
            if obj_key in match_dict:
                info = match_dict[obj_key]
                obj["position"] = {"x": info["x"], "z": info["z"]}
                obj["hint"] = info["hint"]
                obj["has_position"] = True
                q["has_position"] = True
                calibrated_count += 1
                print(f"  * Calibrated [{t_ko}] Obj #{idx+1} -> ({info['x']}, {info['z']}) [{info['hint']}]")

with open("app_v11/data/quests.json", "w", encoding="utf-8") as f:
    json.dump(quests, f, indent=2, ensure_ascii=False)

with open("app/data/quests.json", "w", encoding="utf-8") as f:
    json.dump(quests, f, indent=2, ensure_ascii=False)

print(f"\n=== Successfully Calibrated {calibrated_count} Quest Objectives! ===")
