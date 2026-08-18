import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open("primary_data/market_main_bundle.js", "r", encoding="utf-8") as f:
    js = f.read()

# Search for where 'quests' response is handled or decrypted
matches = [m.start() for m in re.finditer(r'quests', js)]
print(f"Total 'quests' mentions in bundle: {len(matches)}")

for p in matches:
    snippet = js[max(0, p-60):min(len(js), p+150)]
    if any(term in snippet for term in ["decrypt", "decode", "parse", "JSON", "result", "hash"]):
        print(f"\n--- Snippet near index {p} ---")
        print(snippet)
