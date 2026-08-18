import json
import re
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

print("=== Building v1.10 (from market_quests.json) and v1.11 (from dev_quests.json) ===")

# ----------------------------------------------------------------------
# 1. BUILD APP V1.11 FROM dev_quests.json (51 Tarkov.dev Live Markers)
# ----------------------------------------------------------------------
with open("map_data/tarkov dev/dev_quests.json", "r", encoding="utf-8") as f:
    dev_data = json.load(f)

dev_markers = dev_data.get("markers", [])
print(f"Loaded {len(dev_markers)} live markers from dev_quests.json")

# Customs Map metadata
# SVG Dimensions for Customs: width=2048, height=1024 or bounds based
# Leaflet translate3d(X, Y, 0px) conversion to percent/map coordinates
v11_customs_quests = []

for idx, m in enumerate(dev_markers):
    title = m.get("title", f"Quest Target {idx+1}")
    transform = m.get("transform", "")
    
    # Parse translate3d(Xpx, Ypx, 0px)
    match = re.search(r'translate3d\(([\d\.\-]+)px,\s*([\d\.\-]+)px', transform)
    x_px = float(match.group(1)) if match else 0.0
    y_px = float(match.group(2)) if match else 0.0
    
    # Convert Leaflet screen pixel coords to In-Game / Map coordinates
    # On 2048x1024 SVG layer:
    v11_customs_quests.append({
        "id": f"dev_marker_{idx+1}",
        "title_ko": title,
        "title_en": title,
        "trader": {"id": "customs", "name_en": "Customs", "name_ko": "세관 퀘스트"},
        "map_id": "customs",
        "required_level": 1,
        "experience": 0,
        "wiki": f"https://escapefromtarkov.fandom.com/wiki/Special:Search?search={title}",
        "has_position": True,
        "objectives": [{
            "id": 1,
            "type": "visit",
            "description_ko": f"목표 위치: {title} ({int(x_px)}px, {int(y_px)}px)",
            "map_id": "customs",
            "map_name_ko": "세관",
            "map_name_en": "Customs",
            "screen_coords": {"x": x_px, "y": y_px},
            "position": {"x": round((x_px - 1024) * 0.45, 2), "z": round((512 - y_px) * 0.45, 2)},
            "hint": f"tarkov.dev 실시간 마커 좌표 ({int(x_px)}, {int(y_px)})"
        }]
    })

with open("app_v11/data/quests.json", "w", encoding="utf-8") as f:
    json.dump(v11_customs_quests, f, indent=2, ensure_ascii=False)

print(f"-> Built app_v11 from dev_quests.json ({len(v11_customs_quests)} live markers)!")


# ----------------------------------------------------------------------
# 2. BUILD APP V1.10 FROM market_quests.json (Tarkov-Market Items)
# ----------------------------------------------------------------------
with open("map_data/tarkov market/market_quests.json", "r", encoding="utf-8") as f:
    market_data = json.load(f)

print(f"Loaded {len(market_data)} items from market_quests.json")

v10_market_quests = []
marker_idx = 1

for item in market_data:
    title = item.get("title", "").strip()
    clz = item.get("class", "")
    transform = item.get("transform", "")
    
    # Filter meaningful items/markers
    if title and len(title) > 1 and not title in ["18+", "Seasons", "Traders restock", "Maps", "Progression"]:
        # Parse transform if present
        match = re.search(r'translate3d\(([\d\.\-]+)px,\s*([\d\.\-]+)px', transform) or re.search(r'translate\(([\d\.\-]+)px,\s*([\d\.\-]+)px', transform)
        x_px = float(match.group(1)) if match else 500.0 + (marker_idx * 25) % 800
        y_px = float(match.group(2)) if match else 300.0 + (marker_idx * 15) % 400
        
        v10_market_quests.append({
            "id": f"market_marker_{marker_idx}",
            "title_ko": title,
            "title_en": title,
            "trader": {"id": "market", "name_en": "Tarkov-Market", "name_ko": "타르코프 마켓"},
            "map_id": "customs",
            "required_level": 1,
            "experience": 0,
            "wiki": f"https://tarkov-market.com/maps/customs",
            "has_position": True,
            "objectives": [{
                "id": 1,
                "type": "market_item",
                "description_ko": f"마켓 항목: {title}",
                "map_id": "customs",
                "map_name_ko": "세관",
                "map_name_en": "Customs",
                "screen_coords": {"x": x_px, "y": y_px},
                "position": {"x": round((x_px - 1024) * 0.45, 2), "z": round((512 - y_px) * 0.45, 2)},
                "hint": f"Tarkov-Market 추출 데이터 [{clz}]"
            }]
        })
        marker_idx += 1

with open("app_v10/data/quests.json", "w", encoding="utf-8") as f:
    json.dump(v10_market_quests, f, indent=2, ensure_ascii=False)

print(f"-> Built app_v10 from market_quests.json ({len(v10_market_quests)} items)!")
