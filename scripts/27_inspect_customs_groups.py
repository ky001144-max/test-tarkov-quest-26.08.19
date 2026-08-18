import xml.etree.ElementTree as ET
import sys

sys.stdout.reconfigure(encoding='utf-8')

tree = ET.parse("app/maps/Customs.svg")
root = tree.getroot()

g_ids = []
for el in root.iter():
    if el.tag.endswith('g') and 'id' in el.attrib:
        g_ids.append(el.attrib['id'])

print(f"Total <g> with id: {len(g_ids)}")
print("Sample g_ids:", g_ids[:30])
