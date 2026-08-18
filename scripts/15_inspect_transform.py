with open("primary_data/tarkov_dev_map_page_jsx.jsx", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if "transform" in line or "percent" in line.lower() or "viewbox" in line.lower() or "leftpercent" in line.lower():
        print(f"L{i+1}: {line.strip()}")
