import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open("map_data/tasks.txt", "r", encoding="utf-8") as f:
    raw = json.load(f)

quest_items = raw["data"].get("questItems", [])
print(f"Total Quest Items: {len(quest_items)}")

# Inspect sample quest item
if quest_items:
    for qi in list(quest_items.items())[:5] if isinstance(quest_items, dict) else quest_items[:5]:
        print(f"QuestItem: {qi}")
