import sys

sys.stdout.reconfigure(encoding='utf-8')

with open("primary_data/tarkov_dev_map_page_jsx.jsx", "r", encoding="utf-8") as f:
    jsx = f.read()

# Inspect around index 33700-34500 (svgLayer creation)
print("=== SVGOverlay Creation in tarkov.dev ===")
print(jsx[33600:34600])

print("\n=== Bounds and Coordinate Transformation in tarkov.dev ===")
print(jsx[1600:3500])
