import os
import shutil
import xml.etree.ElementTree as ET
import json
import re

source_dir = "tarkov-dev-svg-maps-main"
target_dir = "app/maps"
primary_maps_dir = "primary_data/maps"

os.makedirs(target_dir, exist_ok=True)
os.makedirs(primary_maps_dir, exist_ok=True)

# Map translation and metadata registry
maps_info = {
    "Customs.svg": {
        "id": "customs",
        "name_en": "Customs",
        "name_ko": "세관",
        "order": 1
    },
    "Factory.svg": {
        "id": "factory",
        "name_en": "Factory",
        "name_ko": "공장",
        "order": 2
    },
    "Woods.svg": {
        "id": "woods",
        "name_en": "Woods",
        "name_ko": "우드",
        "order": 3
    },
    "Shoreline.svg": {
        "id": "shoreline",
        "name_en": "Shoreline",
        "name_ko": "쇼어라인",
        "order": 4
    },
    "Interchange.svg": {
        "id": "interchange",
        "name_en": "Interchange",
        "name_ko": "인터체인지",
        "order": 5
    },
    "Reserve.svg": {
        "id": "reserve",
        "name_en": "Reserve",
        "name_ko": "리저브",
        "order": 6
    },
    "Lighthouse.svg": {
        "id": "lighthouse",
        "name_en": "Lighthouse",
        "name_ko": "등대",
        "order": 7
    },
    "StreetsOfTarkov.svg": {
        "id": "streetsoftarkov",
        "name_en": "Streets of Tarkov",
        "name_ko": "타르코프 시내",
        "order": 8
    },
    "GroundZero.svg": {
        "id": "groundzero",
        "name_en": "Ground Zero",
        "name_ko": "그라운드 제로",
        "order": 9
    },
    "Labs.svg": {
        "id": "lab",
        "name_en": "The Lab",
        "name_ko": "더 랩",
        "order": 10
    },
    "Terminal.svg": {
        "id": "terminal",
        "name_en": "Terminal",
        "name_ko": "터미널",
        "order": 11
    }
}

generated_maps_meta = []

print("Replacing map SVGs from tarkov-dev-svg-maps-main and extracting metadata...")

for filename, meta in sorted(maps_info.items(), key=lambda x: x[1]["order"]):
    src_path = os.path.join(source_dir, filename)
    if not os.path.exists(src_path):
        print(f"Warning: {src_path} not found.")
        continue

    # Copy to app/maps/ and primary_data/maps/
    dst_app_path = os.path.join(target_dir, filename)
    dst_prim_path = os.path.join(primary_maps_dir, filename)
    shutil.copy2(src_path, dst_app_path)
    shutil.copy2(src_path, dst_prim_path)

    # Parse SVG for viewBox and floor groups
    with open(src_path, "r", encoding="utf-8") as f:
        svg_content = f.read()

    # Extract viewBox
    vb_match = re.search(r'viewBox="([^"]+)"', svg_content)
    viewbox = [0, 0, 1000, 1000]
    if vb_match:
        parts = [float(p) for p in re.split(r'[\s,]+', vb_match.group(1).strip()) if p]
        if len(parts) == 4:
            viewbox = parts

    # Extract floor layer IDs (<g id="...">)
    g_ids = re.findall(r'<g[^>]*id="([^"]+)"', svg_content)
    floors = []
    
    # Common floor names
    floor_candidates = [
        "Basement", "Underground_Level", "Bunkers", "Garage",
        "Ground_Level", "Ground_Floor", "First_Floor", "Second_Floor", "Third_Floor"
    ]

    for fc in floor_candidates:
        if any(fc.lower() in gid.lower() for gid in g_ids):
            floors.append(fc)

    if not floors:
        floors = ["Ground_Level"]

    map_entry = {
        "id": meta["id"],
        "name_en": meta["name_en"],
        "name_ko": meta["name_ko"],
        "svg": filename,
        "viewBox": viewbox,
        "floors": floors,
        "width": viewbox[2],
        "height": viewbox[3]
    }
    generated_maps_meta.append(map_entry)
    print(f"  [OK] {filename:20s} -> {meta['name_ko']:10s} (viewBox: {viewbox[2]:.1f}x{viewbox[3]:.1f}, floors: {floors})")

# Save app/data/maps.json
with open("app/data/maps.json", "w", encoding="utf-8") as f:
    json.dump(generated_maps_meta, f, indent=2, ensure_ascii=False)

with open("secondary_data/maps.json", "w", encoding="utf-8") as f:
    json.dump(generated_maps_meta, f, indent=2, ensure_ascii=False)

print(f"\nSuccessfully replaced {len(generated_maps_meta)} map SVGs and saved app/data/maps.json.")
