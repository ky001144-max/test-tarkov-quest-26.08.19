import json

with open("tarkov-data-manager-main/src/tarkov-data-manager/public/data/quest-data.json", "r", encoding="utf-8") as f:
    local_quest_data = json.load(f)

print(f"Total quests in data-manager: {len(local_quest_data)}")
bp_found = [q for q in local_quest_data if "bp depot" in q.get("name", "").lower()]
print(f"BP Depot in data-manager: {len(bp_found)}")

# Let's inspect active quests in data-manager
print("\nSample Quests in data-manager:")
for q in local_quest_data[:15]:
    print(f"  - [{q.get('trader')}] {q.get('name')} (id: {q.get('id')})")
