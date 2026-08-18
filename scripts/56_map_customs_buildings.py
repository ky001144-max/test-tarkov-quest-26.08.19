import xml.etree.ElementTree as ET
import re
import json

tree = ET.parse("app/maps/Customs.svg")
root = tree.getroot()

vb_w = 1062.4827
vb_h = 535.17401

buildings_g = None
for g in root.iter("{http://www.w3.org/2000/svg}g"):
    if g.attrib.get("id") == "Buildings":
        buildings_g = g
        break

building_boxes = []

if buildings_g:
    for idx, path in enumerate(buildings_g.iter("{http://www.w3.org/2000/svg}path")):
        d = path.attrib.get("d", "")
        pid = path.attrib.get("id", f"building_{idx}")
        nums = [float(n) for n in re.findall(r'[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?', d)]
        if len(nums) >= 4:
            xs = nums[0::2]
            ys = nums[1::2]
            min_x, max_x = min(xs), max(xs)
            min_y, max_y = min(ys), max(ys)
            cx = (min_x + max_x) / 2
            cy = (min_y + max_y) / 2
            w = max_x - min_x
            h = max_y - min_y
            left_pct = (cx / vb_w) * 100
            top_pct = (cy / vb_h) * 100
            
            building_boxes.append({
                "index": idx,
                "id": pid,
                "cx": round(cx, 1),
                "cy": round(cy, 1),
                "w": round(w, 1),
                "h": round(h, 1),
                "left_pct": round(left_pct, 2),
                "top_pct": round(top_pct, 2)
            })

print(f"Total building blocks found in Customs: {len(building_boxes)}")
# Sort by left_pct to see west to east
building_boxes.sort(key=lambda b: b["left_pct"])

for b in building_boxes:
    print(f"  Building #{b['index']:2d}: center=({b['cx']:6.1f}, {b['cy']:6.1f}), size=({b['w']:5.1f}x{b['h']:5.1f}) -> left: {b['left_pct']:5.2f}%, top: {b['top_pct']:5.2f}%")
