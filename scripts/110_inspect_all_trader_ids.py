import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

# Let's inspect all trader IDs in tasks.txt
with open("map_data/tarkov dev/tasks.txt", "r", encoding="utf-8") as f:
    raw = json.load(f)

tasks = raw["data"]["tasks"]
trader_counts = {}

for q_id, q in tasks.items():
    tr = q.get("trader")
    trader_counts[tr] = trader_counts.get(tr, 0) + 1

print("All Trader IDs in tasks.txt:")
for tr, cnt in trader_counts.items():
    print(f"  * {tr}: {cnt} quests")
