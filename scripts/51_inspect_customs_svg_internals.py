import xml.etree.ElementTree as ET
import re

with open("app/maps/Customs.svg", "r", encoding="utf-8") as f:
    svg_content = f.read()

# Let's search for known text or IDs or classes in Customs.svg to find landmark locations:
# e.g., dorms, big red, bridge, gas, etc.
labels = re.findall(r'<text[^>]*>([^<]+)</text>', svg_content)
print(f"Total text labels in Customs.svg: {len(labels)}")
print("Sample labels:", labels[:30])

# Let's search for circles, rectangles or paths with IDs
elements_with_id = re.findall(r'<[a-zA-Z0-9]+[^>]*id="([^"]+)"[^>]*>', svg_content)
print(f"\nTotal elements with ID in Customs.svg: {len(elements_with_id)}")
print("Sample IDs:", [eid for eid in elements_with_id if any(k in eid.lower() for k in ["dorm", "truck", "tanker", "red", "gas", "boiler", "bridge", "custom", "office", "task", "quest", "extract"])][:30])
