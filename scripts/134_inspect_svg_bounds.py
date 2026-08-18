import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open("primary_data/tarkov_dev_map_page_jsx.jsx", "r", encoding="utf-8") as f:
    jsx = f.read()

matches = [m.start() for m in re.finditer(r'svgBounds', jsx)]
print(f"Found {len(matches)} occurrences of svgBounds:")
for p in matches:
    print("\n--- Match ---")
    print(jsx[max(0, p-100):min(len(jsx), p+200)])
