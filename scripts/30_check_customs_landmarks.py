import xml.etree.ElementTree as ET
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

tree = ET.parse("app/maps/Customs.svg")
root = tree.getroot()

vb = root.attrib.get('viewBox').split()
vb_w = float(vb[2])
vb_h = float(vb[3])

def get_group_bbox(group_id):
    coords = []
    for el in root.iter():
        if el.attrib.get('id') == group_id:
            for p in el.iter():
                if 'd' in p.attrib:
                    nums = re.findall(r'[-+]?(?:\d*\.\d+|\d+)', p.attrib['d'])
                    for i in range(0, len(nums)-1, 2):
                        coords.append((float(nums[i]), float(nums[i+1])))
    if coords:
        min_x = min(c[0] for c in coords)
        max_x = max(c[0] for c in coords)
        min_y = min(c[1] for c in coords)
        max_y = max(c[1] for c in coords)
        return min_x, max_x, min_y, max_y
    return None

print("Key groups in Customs.svg:")
for gid in ['River', 'Dorms-1', 'Streamers-1f', 'Big_Buildings-2', 'Sniper', 'Garages-2']:
    bbox = get_group_bbox(gid)
    if bbox:
        print(f"  {gid:20s}: X={bbox[0]:.1f}~{bbox[1]:.1f} ({bbox[0]/vb_w*100:.1f}%~{bbox[1]/vb_w*100:.1f}%), Y={bbox[2]:.1f}~{bbox[3]:.1f} ({bbox[2]/vb_h*100:.1f}%~{bbox[3]/vb_h*100:.1f}%)")
