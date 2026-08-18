import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open("secondary_data/processed_quests.json", "r", encoding="utf-8") as f:
    quests = json.load(f)

customs_quests = [q for q in quests if any(o.get("map_id") == "customs" and o.get("gps") for o in q.get("objectives", []))]
print(f"Total Customs Quests with GPS: {len(customs_quests)}")

for q in customs_quests[:10]:
    print(f"\nQuest: {q['title_ko']} ({q['title_en']})")
    for o in q['objectives']:
        if o.get("map_id") == "customs" and o.get("gps"):
            gps = o['gps']
            print(f"  - [{o['type']}] {o['target']} -> left: {gps.get('leftPercent')}%, top: {gps.get('topPercent')}%, floor: {gps.get('floor')}")
