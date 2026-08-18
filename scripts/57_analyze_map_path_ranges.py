import xml.etree.ElementTree as ET
import os
import re
import json

maps_dir = "app/maps"
map_bounds_report = {}

for svg_name in os.listdir(maps_dir):
    if not svg_name.endswith(".svg"):
        continue
    svg_path = os.path.join(maps_dir, svg_name)
    tree = ET.parse(svg_path)
    root = tree.getroot()
    
    vb = root.attrib.get("viewBox", "0 0 1000 1000")
    vb_parts = [float(p) for p in re.split(r'[\s,]+', vb.strip()) if p]
    
    all_d = []
    for path in root.iter("{http://www.w3.org/2000/svg}path"):
        d = path.attrib.get("d", "")
        if d:
            all_d.append(d)
            
    if all_d:
        combined = " ".join(all_d)
        nums = [float(n) for n in re.findall(r'[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?', combined)]
        if len(nums) >= 2:
            xs = nums[0::2]
            ys = nums[1::2]
            min_x, max_x = min(xs), max(xs)
            min_y, max_y = min(ys), max(ys)
            
            map_bounds_report[svg_name] = {
                "viewBox": vb_parts,
                "real_x_range": [round(min_x, 1), round(max_x, 1)],
                "real_y_range": [round(min_y, 1), round(max_y, 1)],
                "real_width": round(max_x - min_x, 1),
                "real_height": round(max_y - min_y, 1)
            }
            print(f"Map: {svg_name:20s}")
            print(f"  - viewBox: {vb_parts}")
            print(f"  - Real Path Range X: [{min_x:6.1f} ~ {max_x:6.1f}] (span: {max_x - min_x:6.1f} vs vbW: {vb_parts[2]:6.1f})")
            print(f"  - Real Path Range Y: [{min_y:6.1f} ~ {max_y:6.1f}] (span: {max_y - min_y:6.1f} vs vbH: {vb_parts[3]:6.1f})")

with open("secondary_data/map_bounds_report.json", "w", encoding="utf-8") as f:
    json.dump(map_bounds_report, f, indent=2)
