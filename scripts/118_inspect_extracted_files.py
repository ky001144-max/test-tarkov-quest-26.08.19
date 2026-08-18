import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

print("=== 1. Inspecting map_data/tarkov market/market_quests.json ===")
with open("map_data/tarkov market/market_quests.json", "r", encoding="utf-8") as f:
    market_data = json.load(f)

print("market_data type:", type(market_data))
if isinstance(market_data, list):
    print(f"Total items in market_quests.json: {len(market_data)}")
    for item in market_data[:5]:
        print("  *", item)
elif isinstance(market_data, dict):
    print("Keys in market_quests.json:", list(market_data.keys()))
    print("Sample:", str(market_data)[:300])

print("\n=== 2. Inspecting map_data/tarkov dev/dev_quests.json ===")
with open("map_data/tarkov dev/dev_quests.json", "r", encoding="utf-8") as f:
    dev_data = json.load(f)

print("dev_data type:", type(dev_data))
if isinstance(dev_data, list):
    print(f"Total items in dev_quests.json: {len(dev_data)}")
    for item in dev_data[:5]:
        print("  *", item)
elif isinstance(dev_data, dict):
    print("Keys in dev_quests.json:", list(dev_data.keys()))
    if "markers" in dev_data:
        print(f"Markers count: {len(dev_data['markers'])}")
        for m in dev_data['markers'][:5]:
            print("  *", m)
