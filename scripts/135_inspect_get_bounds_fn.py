import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open("primary_data/tarkov_dev_map_page_jsx.jsx", "r", encoding="utf-8") as f:
    jsx = f.read()

# Search getBounds definition
match = re.search(r'function getBounds\([^)]*\)\s*\{[^}]*\}', jsx)
if match:
    print("getBounds definition:")
    print(match.group(0))
