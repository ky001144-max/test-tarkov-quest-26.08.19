import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open("primary_data/tarkov_dev_map_page_jsx.jsx", "r", encoding="utf-8") as f:
    jsx = f.read()

# Search for ImageOverlay in jsx
matches = [m.start() for m in re.finditer(r'ImageOverlay', jsx)]
print(f"Found {len(matches)} occurrences of ImageOverlay in tarkov_dev_map_page_jsx.jsx:")

for p in matches:
    snippet = jsx[max(0, p-100):min(len(jsx), p+300)]
    print("\n--- Match ---")
    print(snippet)
