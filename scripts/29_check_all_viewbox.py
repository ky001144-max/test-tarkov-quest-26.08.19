import os
import xml.etree.ElementTree as ET

maps_dir = "app/maps"
for f in sorted(os.listdir(maps_dir)):
    if f.endswith(".svg"):
        path = os.path.join(maps_dir, f)
        tree = ET.parse(path)
        root = tree.getroot()
        vb = root.attrib.get('viewBox', '')
        parts = vb.split()
        print(f"{f:22s} -> viewBox: {vb}")
