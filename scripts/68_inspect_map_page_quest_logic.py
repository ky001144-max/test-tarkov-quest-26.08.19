with open("primary_data/tarkov_dev_map_page_jsx.jsx", "r", encoding="utf-8") as f:
    code = f.read()

lines = code.split("\n")
print(f"Total lines in tarkov_dev_map_page_jsx: {len(lines)}")

for i, line in enumerate(lines):
    if any(k in line.lower() for k in ["usequestsdata", "quest", "task", "objectives", "zone", "marker"]):
        if any(w in line for w in ["import", "const", "let", "function", "return", "map", "filter", "forEach"]):
            print(f"L{i+1}: {line.strip()}")
