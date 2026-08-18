import os
import re
import json
import xml.etree.ElementTree as ET

maps_dir = "app/maps"
landmark_registry = {}

def parse_svg_landmarks(svg_path):
    landmarks = {}
    with open(svg_path, "r", encoding="utf-8") as f:
        svg_content = f.read()
    
    # Extract viewBox
    vb_match = re.search(r'viewBox="([^"]+)"', svg_content)
    vb = [0, 0, 1000, 1000]
    if vb_match:
        vb = [float(p) for p in re.split(r'[\s,]+', vb_match.group(1).strip()) if p]
    
    vb_w = vb[2]
    vb_h = vb[3]
    
    # Parse elements with ID or class
    # We find all tags that have an id
    pattern = re.compile(r'<([a-zA-Z0-9]+)\s+([^>]*id="([^"]+)"[^>]*)>', re.DOTALL)
    for match in pattern.finditer(svg_content):
        tag_name = match.group(1)
        attrs = match.group(2)
        elem_id = match.group(3)
        
        # skip generic container ids
        if elem_id in ["style_common", "defs1", "svg89", "Ground_Level", "Underground_Level", "First_Floor", "Second_Floor", "Third_Floor"]:
            continue
            
        d_match = re.search(r'd="([^"]+)"', attrs)
        if d_match:
            nums = [float(n) for n in re.findall(r'[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?', d_match.group(1))]
            if len(nums) >= 2:
                xs = nums[0::2]
                ys = nums[1::2]
                min_x, max_x = min(xs), max(xs)
                min_y, max_y = min(ys), max(ys)
                center_x = (min_x + max_x) / 2
                center_y = (min_y + max_y) / 2
                
                left_pct = (center_x / vb_w) * 100
                top_pct = (center_y / vb_h) * 100
                
                landmarks[elem_id] = {
                    "pixelX": round(center_x, 2),
                    "pixelY": round(center_y, 2),
                    "leftPercent": round(left_pct, 2),
                    "topPercent": round(top_pct, 2),
                    "bbox": [min_x, min_y, max_x, max_y]
                }
    return vb, landmarks

for svg_file in os.listdir(maps_dir):
    if svg_file.endswith(".svg"):
        p = os.path.join(maps_dir, svg_file)
        vb, lms = parse_svg_landmarks(p)
        map_key = svg_file.replace(".svg", "").lower()
        landmark_registry[map_key] = {
            "file": svg_file,
            "viewBox": vb,
            "landmarks": lms
        }
        print(f"Map: {svg_file:20s} (viewBox: {vb[2]:.1f}x{vb[3]:.1f}) -> Found {len(lms)} landmark IDs")
        for lm_id, lm_data in list(lms.items())[:6]:
            print(f"   * {lm_id:25s} -> ({lm_data['leftPercent']:5.2f}%, {lm_data['topPercent']:5.2f}%)")

with open("secondary_data/svg_landmarks.json", "w", encoding="utf-8") as f:
    json.dump(landmark_registry, f, indent=2)

print("\nSaved SVG landmarks to secondary_data/svg_landmarks.json")
