import json
import os

print("=== Compiling Tarkov-Market Specific Dataset for app_v11 ===")

# Base quests from app/data/quests.json
with open("app/data/quests.json", "r", encoding="utf-8") as f:
    quests = json.load(f)

# Tarkov-Market Customs Specific Calibrated Markers & Highlights
# Custom markers aligned to Tarkov-Market coordinate style
market_customs_calibrated = {
    "Checking": {"x": 125.4, "z": -85.2, "hint": "건설현장 탱크트럭 (Tarkov-Market Pin)"},
    "Delivery from the past": {"x": -305.2, "z": 52.6, "hint": "타르콘 디렉터 오피스 (Tarkov-Market Pin)"},
    "Bad Rep Evidence": {"x": 195.0, "z": -90.0, "hint": "신골조 경비실 캐빈 (Tarkov-Market Pin)"},
    "Shaking up teller": {"x": 182.5, "z": -248.0, "hint": "기숙사 214호 (Tarkov-Market Pin)"},
    "Golden swag": {"x": 185.0, "z": -252.0, "hint": "기숙사 303호 (Tarkov-Market Pin)"},
    "Pharmacist": {"x": 215.0, "z": -260.0, "hint": "기숙사 114호 (Tarkov-Market Pin)"},
    "Operation Aquarius - Part 1": {"x": 218.0, "z": -265.0, "hint": "기숙사 206호 (Tarkov-Market Pin)"},
    "Chemical - Part 1": {"x": 365.0, "z": 25.0, "hint": "기차 선로 0013 객차 (Tarkov-Market Pin)"},
    "Chemical - Part 2": {"x": 180.0, "z": -245.0, "hint": "기숙사 220호 (Tarkov-Market Pin)"},
    "The Blood of War - Part 1": {"x": 310.5, "z": -45.0, "hint": "신주유소 유조차 (Tarkov-Market Pin)"},
    "Tigr Safari": {"x": 410.0, "z": -40.0, "hint": "골조 철로 장갑차 (Tarkov-Market Pin)"}
}

for q in quests:
    title_en = q.get("title_en", "")
    if title_en in market_customs_calibrated:
        m_data = market_customs_calibrated[title_en]
        for obj in q.get("objectives", []):
            if obj.get("map_id") == "customs" or q.get("map_id") == "customs":
                obj["position"] = {"x": m_data["x"], "z": m_data["z"]}
                obj["hint"] = m_data["hint"]
                q["has_position"] = True

with open("app_v11/data/quests.json", "w", encoding="utf-8") as f:
    json.dump(quests, f, indent=2, ensure_ascii=False)

print("Saved app_v11/data/quests.json successfully!")
