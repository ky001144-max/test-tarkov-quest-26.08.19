import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open("primary_data/tarkov_dev_map_page_jsx.jsx", "r", encoding="utf-8") as f:
    jsx = f.read()

# Search for overlay, svg, bounds, MapContainer
keywords = ["bounds", "svg", "overlay", "layers", "SVGOverlay", "imageOverlay", "MapContainer"]

for kw in keywords:
    matches = [m.start() for m in re.finditer(re.escape(kw), jsx, re.IGNORECASE)]
    print(f"Keyword '{kw}': {len(matches)} occurrences")
    for idx, p in enumerate(matches[:2]):
        snippet = jsx[max(0, p-60):min(len(jsx), p+200)]
        print(f"  Match #{idx+1} near {p}:")
        print(f"    {snippet}")
