import json
import os

with open("primary_data/tarkov_dev_maps.json", "r", encoding="utf-8") as f:
    raw_maps = json.load(f)

# Build official maps meta with tarkov.dev parameters
clean_maps = []

map_id_map = {
    "customs": {"id": "customs", "name_ko": "세관", "name_en": "Customs", "svg": "Customs.svg", "order": 1},
    "factory": {"id": "factory", "name_ko": "공장", "name_en": "Factory", "svg": "Factory.svg", "order": 2},
    "woods": {"id": "woods", "name_ko": "우드", "name_en": "Woods", "svg": "Woods.svg", "order": 3},
    "shoreline": {"id": "shoreline", "name_ko": "쇼어라인", "name_en": "Shoreline", "svg": "Shoreline.svg", "order": 4},
    "interchange": {"id": "interchange", "name_ko": "인터체인지", "name_en": "Interchange", "svg": "Interchange.svg", "order": 5},
    "reserve": {"id": "reserve", "name_ko": "리저브", "name_en": "Reserve", "svg": "Reserve.svg", "order": 6},
    "lighthouse": {"id": "lighthouse", "name_ko": "등대", "name_en": "Lighthouse", "svg": "Lighthouse.svg", "order": 7},
    "streets-of-tarkov": {"id": "streetsoftarkov", "name_ko": "타르코프 시내", "name_en": "Streets of Tarkov", "svg": "StreetsOfTarkov.svg", "order": 8},
    "ground-zero": {"id": "groundzero", "name_ko": "그라운드 제로", "name_en": "Ground Zero", "svg": "GroundZero.svg", "order": 9},
    "the-lab": {"id": "lab", "name_ko": "더 랩", "name_en": "The Lab", "svg": "Labs.svg", "order": 10},
    "terminal": {"id": "terminal", "name_ko": "터미널", "name_en": "Terminal", "svg": "Terminal.svg", "order": 11}
}

for m in raw_maps:
    norm_name = m.get("normalizedName")
    if norm_name not in map_id_map:
        continue
    
    meta_info = map_id_map[norm_name]
    
    # Find interactive or 2D submap with transform and bounds
    submaps = m.get("maps", [])
    interactive_submap = next((sm for sm in submaps if sm.get("projection") == "interactive"), submaps[0] if submaps else {})
    
    transform = interactive_submap.get("transform", [1, 0, 1, 0])
    rotation = interactive_submap.get("coordinateRotation", 0)
    bounds = interactive_submap.get("bounds", [[1000, -1000], [-1000, 1000]])
    
    clean_maps.append({
        "id": meta_info["id"],
        "normalizedName": norm_name,
        "name_ko": meta_info["name_ko"],
        "name_en": meta_info["name_en"],
        "svg": meta_info["svg"],
        "transform": transform,
        "coordinateRotation": rotation,
        "bounds": bounds,
        "order": meta_info["order"]
    })

clean_maps.sort(key=lambda x: x["order"])

with open("app/data/maps.json", "w", encoding="utf-8") as f:
    json.dump(clean_maps, f, indent=2, ensure_ascii=False)

print(f"Generated clean official maps.json with {len(clean_maps)} maps.")
for cm in clean_maps:
    print(f"  - {cm['name_ko']} ({cm['id']}): bounds={cm['bounds']}, transform={cm['transform']}, rotation={cm['coordinateRotation']}")
