import re

with open("app/maps/Customs.svg", "r", encoding="utf-8") as f:
    svg_content = f.read()

# Find all tags with id attribute and their bounding positions
tags = re.findall(r'<([a-zA-Z0-9]+)\s+([^>]*id="([^"]+)"[^>]*)>', svg_content)

vb_w = 1062.4827
vb_h = 535.17401

print("Landmarks found in Customs.svg with exact SVG coordinates:")
for tag_name, attrs, elem_id in tags:
    # Look for paths or rects or polygons
    d_match = re.search(r'd="([^"]+)"', attrs)
    x_match = re.search(r'x="([^"]+)"', attrs)
    y_match = re.search(r'y="([^"]+)"', attrs)
    
    coords = []
    if d_match:
        # Extract numbers from path d
        nums = [float(n) for n in re.findall(r'[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?', d_match.group(1))]
        if len(nums) >= 2:
            xs = nums[0::2]
            ys = nums[1::2]
            min_x, max_x = min(xs), max(xs)
            min_y, max_y = min(ys), max(ys)
            avg_x = (min_x + max_x) / 2
            avg_y = (min_y + max_y) / 2
            print(f"  * ID: {elem_id:25s} -> SVG Pixel({avg_x:6.1f}, {avg_y:6.1f}) -> ({avg_x/vb_w*100:5.2f}%, {avg_y/vb_h*100:5.2f}%)")
    elif x_match and y_match:
        px = float(x_match.group(1))
        py = float(y_match.group(1))
        print(f"  * ID: {elem_id:25s} -> SVG Pixel({px:6.1f}, {py:6.1f}) -> ({px/vb_w*100:5.2f}%, {py/vb_h*100:5.2f}%)")
