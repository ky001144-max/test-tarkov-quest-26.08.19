import re

with open("primary_data/tarkov_dev_map_page_jsx.jsx", "r", encoding="utf-8") as f:
    code = f.read()

# Look for coordinate, left, top, marker, percent, bounds
matches = re.findall(r"(?:left|top|x|y|transform|coord|marker|percent|viewBox)[\w\s\:\=\.\*\/\-\+]{1,100}", code, re.IGNORECASE)
print(f"Found {len(matches)} potential coordinate matches in JSX.")
for m in matches[:25]:
    if any(k in m for k in ['percent', 'left', 'top', 'transform', 'coord', 'viewBox', 'bounds']):
        print("  -", m.strip())
