import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open("map_data/tarkov market/market_list.txt", "r", encoding="utf-8") as f:
    content = f.read()

print(f"market_list.txt size: {len(content):,} chars")
try:
    data = json.loads(content)
    print("Parsed JSON keys:", list(data.keys()))
    print("own:", len(data.get("own", [])))
    print("installed:", len(data.get("installed", [])))
    print("system:", len(data.get("system", "")))
except Exception as e:
    print("Error parsing market_list.txt:", e)
