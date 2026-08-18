import xml.etree.ElementTree as ET
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

tree = ET.parse("app/maps/Customs.svg")
root = tree.getroot()

vb = root.attrib.get('viewBox').split()
vb_w = float(vb[2])
vb_h = float(vb[3])

def extract_coords(element):
    coords = []
    # check path d attribute
    for p in element.iter():
        if 'd' in p.attrib:
            nums = re.findall(r'[-+]?(?:\d*\.\d+|\d+)', p.attrib['d'])
            for i in range(0, len(nums)-1, 2):
                coords.append((float(nums[i]), float(nums[i+1])))
    return coords

for target in ['River', 'Gas_Station', 'Garages-2']:
    for el in root.iter():
        if el.attrib.get('id') == target:
            coords = extract_coords(el)
            if coords:
                min_x = min(c[0] for c in coords)
                max_x = max(c[0] for c in coords)
                min_y = min(c[1] for c in coords)
                max_y = max(c[1] for c in coords)
                print(f"Group [{target}]:")
                print(f"  X: {min_x:.1f} ~ {max_x:.1f} (left%: {min_x/vb_w*100:.1f}% ~ {max_x/vb_w*100:.1f}%)")
                print(f"  Y: {min_y:.1f} ~ {max_y:.1f} (top%: {min_y/vb_h*100:.1f}% ~ {max_y/vb_h*100:.1f}%)")
