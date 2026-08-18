import os
import xml.etree.ElementTree as ET

maps_dir = "app/maps"
for f in os.listdir(maps_dir):
    if f.endswith(".svg"):
        path = os.path.join(maps_dir, f)
        try:
            tree = ET.parse(path)
            root = tree.getroot()
            width = root.attrib.get('width')
            height = root.attrib.get('height')
            viewBox = root.attrib.get('viewBox')
            print(f"{f:20s} | width: {str(width):10s} | height: {str(height):10s} | viewBox: {str(viewBox)}")
        except Exception as e:
            print(f"{f}: {e}")
