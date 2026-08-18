import xml.etree.ElementTree as ET
import sys

sys.stdout.reconfigure(encoding='utf-8')

tree = ET.parse("app/maps/Customs.svg")
root = tree.getroot()

vb = root.attrib.get('viewBox').split()
vb_w = float(vb[2])
vb_h = float(vb[3])
print(f"Customs SVG viewBox: width={vb_w}, height={vb_h}")

texts = []
for el in root.iter():
    if el.tag.endswith('text') or el.tag.endswith('tspan'):
        txt = "".join(el.itertext()).strip()
        x = el.attrib.get('x')
        y = el.attrib.get('y')
        transform = el.attrib.get('transform')
        if txt and len(txt) > 2:
            texts.append((txt, x, y, transform))

print(f"Found {len(texts)} text labels in Customs.svg. Sample labels:")
for t in texts[:20]:
    print("  -", t)
