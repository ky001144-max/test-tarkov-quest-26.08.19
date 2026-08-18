import re

with open("primary_data/tarkov_dev_map_page_jsx.jsx", "r", encoding="utf-8") as f:
    code = f.read()

# Let's inspect how tarkov-dev maps world coordinates (x, z) to SVG / Leaflet pixel coordinates
lines = code.split("\n")
for i, line in enumerate(lines[:120]):
    if any(k in line for k in ["transform", "scaleX", "scaleY", "marginX", "marginY", "crs", "Transformation", "project", "unproject"]):
        print(f"L{i+1}: {line}")
