import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open("primary_data/tarkov_dev_map_page_jsx.jsx", "r", encoding="utf-8") as f:
    jsx = f.read()

idx = jsx.find("function getBounds(bounds)")
print(jsx[idx:idx+400])
