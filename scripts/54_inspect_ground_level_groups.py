import xml.etree.ElementTree as ET
import re

tree = ET.parse("app/maps/Customs.svg")
root = tree.getroot()

vb_w = 1062.4827
vb_h = 535.17401

ground_level = next(c for c in root if c.attrib.get("id") == "Ground_Level")

for g in ground_level:
    gid = g.attrib.get("id", "no-id")
    gcls = g.attrib.get("class", "no-class")
    
    # Calculate bounding box of all paths in this group
    all_d = []
    for path in g.iter("{http://www.w3.org/2000/svg}path"):
        d = path.attrib.get("d", "")
        if d:
            all_d.append(d)
    
    if all_d:
        combined_d = " ".join(all_d)
        nums = [float(n) for n in re.findall(r'[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?', combined_d)]
        if len(nums) >= 2:
            xs = nums[0::2]
            ys = nums[1::2]
            min_x, max_x = min(xs), max(xs)
            min_y, max_y = min(ys), max(ys)
            w = max_x - min_x
            h = max_y - min_y
            print(f"Group: {gid:15s} (class: {gcls:20s}) -> X: [{min_x:6.1f} ~ {max_x:6.1f}] ({min_x/vb_w*100:4.1f}% ~ {max_x/vb_w*100:4.1f}%), Y: [{min_y:6.1f} ~ {max_y:6.1f}] ({min_y/vb_h*100:4.1f}% ~ {max_y/vb_h*100:4.1f}%)")
