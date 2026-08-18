import xml.etree.ElementTree as ET
import re

tree = ET.parse("app/maps/Customs.svg")
root = tree.getroot()

vb = root.attrib.get("viewBox", "0 0 1062.4827 535.17401")
print("Customs.svg root attributes:", root.attrib)

# Let's inspect the main background/ground rect or path
for elem in root.iter():
    tag = elem.tag.split("}")[-1]
    eid = elem.attrib.get("id", "")
    ecls = elem.attrib.get("class", "")
    if any(k in eid.lower() or k in ecls.lower() for k in ["ground", "land", "map_border", "border", "rect"]):
        print(f"Elem: <{tag}> id='{eid}' class='{ecls}' attribs={elem.attrib}")

# Let's check Dorms in Customs.svg
# Where are the dorms paths located in the SVG?
for g in root.iter("{http://www.w3.org/2000/svg}g"):
    gid = g.attrib.get("id", "")
    if "dorm" in gid.lower() or "3s" in gid.lower() or "2s" in gid.lower():
        print(f"Dorm Group: <g id='{gid}'>")
        for p in g.iter("{http://www.w3.org/2000/svg}path"):
            d = p.attrib.get("d", "")
            nums = [float(n) for n in re.findall(r'[-+]?\d*\.?\d+', d)]
            if len(nums) >= 4:
                xs = nums[0::2]
                ys = nums[1::2]
                print(f"   path: X=[{min(xs):.1f} ~ {max(xs):.1f}], Y=[{min(ys):.1f} ~ {max(ys):.1f}]")
