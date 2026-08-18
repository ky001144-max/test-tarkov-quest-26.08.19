import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open("primary_data/tarkov_dev_map_page_jsx.jsx", "r", encoding="utf-8") as f:
    jsx = f.read()

# Search for customs in jsx
matches = [m.start() for m in re.finditer(r'"customs"', jsx, re.IGNORECASE)]
print(f"Found {len(matches)} occurrences of 'customs' in jsx:")
for p in matches[:3]:
    print("\n--- Match ---")
    print(jsx[max(0, p-60):min(len(jsx), p+250)])
