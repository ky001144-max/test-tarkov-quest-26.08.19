import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open("primary_data/market_main_bundle.js", "r", encoding="utf-8") as f:
    js = f.read()

# Search for occurrences of 'all?hash' or 'quests' or 'system' or 'map-doc'
keywords = ['map-doc', 'all?hash', 'quests', 'markers', 'decode(']

for kw in keywords:
    pos = 0
    print(f"\n--- Searching for keyword: '{kw}' ---")
    matches = [m.start() for m in re.finditer(re.escape(kw), js)]
    print(f"Found {len(matches)} occurrences.")
    for idx, p in enumerate(matches[:3]):
        snippet = js[max(0, p-150):min(len(js), p+250)]
        print(f"  Match #{idx+1} at index {p}:")
        print(f"    ... {snippet} ...")
