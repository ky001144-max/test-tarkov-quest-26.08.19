import xml.etree.ElementTree as ET
import re

tree = ET.parse("app/maps/Customs.svg")
root = tree.getroot()

vb = root.attrib.get("viewBox", "0 0 1062.4827 535.17401")
print("Customs.svg root attributes:", root.attrib)

# Find all g elements and their children
for child in root:
    tag = child.tag.split("}")[-1]
    cid = child.attrib.get("id", "no-id")
    ccls = child.attrib.get("class", "no-class")
    print(f"Child: <{tag}> id='{cid}' class='{ccls}' subelements={len(child)}")
    if cid in ["Ground_Level", "First_Floor", "Second_Floor", "Third_Floor"]:
        for sub in child[:5]:
            stag = sub.tag.split("}")[-1]
            sid = sub.attrib.get("id", "no-id")
            scls = sub.attrib.get("class", "no-class")
            print(f"   -> <{stag}> id='{sid}' class='{scls}'")
