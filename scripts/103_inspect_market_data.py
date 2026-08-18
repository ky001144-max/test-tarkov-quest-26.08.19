import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open("map_data/tarkov market/market_all.txt", "r", encoding="utf-8") as f:
    market_all = json.load(f)

with open("map_data/tarkov market/market_list.txt", "r", encoding="utf-8") as f:
    market_list = json.load(f)

print("=== 1. market_list.txt Inspection ===")
print("market_list type:", type(market_list))
if isinstance(market_list, dict):
    print("Keys in market_list:", list(market_list.keys()))
    print("Sample:", str(market_list)[:300])
elif isinstance(market_list, list):
    print(f"List with {len(market_list)} items:")
    for item in market_list[:10]:
        print("  -", item)

print("\n=== 2. market_all.txt Inspection ===")
print("market_all type:", type(market_all))
if isinstance(market_all, dict):
    print("Keys in market_all:", list(market_all.keys()))
    for k in list(market_all.keys())[:15]:
        v = market_all[k]
        print(f"  * Key [{k}]: type {type(v)}, len {len(v) if hasattr(v, '__len__') else 'N/A'}")
elif isinstance(market_all, list):
    print(f"List with {len(market_all)} items. Sample item 0:")
    print(market_all[0])
