with open("primary_data/tarkov_dev_map_page_jsx.jsx", "r", encoding="utf-8") as f:
    lines = f.readlines()

print("Lines 1 to 100 of tarkov_dev_map_page_jsx.jsx:")
for i in range(0, min(100, len(lines))):
    print(f"L{i+1}: {lines[i].rstrip()}")
